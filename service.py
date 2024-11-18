import asyncio
import logging
from neo4jsbml import arrows, connect, sbml
import libsbml
from concurrent.futures import ProcessPoolExecutor
import neo4j
from typing import Optional, List
import voyageai
from neo4jsbml.srelationship import Dict


def get_connection () -> Optional[connect.Connect]:
    connection = connect.Connect.from_config("config/connect.ini")
    if connection.is_connected():
        return connection
    else:
        return None

class SBMLService:
    def from_sbml_custom(self, xml: str, tag=None) -> sbml.SbmlToNeo4j:
        doc = libsbml.readSBMLFromString(xml)
        errors = doc.getNumErrors()
        if errors > 0 :
            logging.error(doc.printErrors())
            raise ValueError("Error when parsing SBML string -> arbot")

        return sbml.SbmlToNeo4j(tag=tag, document=doc)

    def process_model(self, xml_string, tag):
        connection = get_connection()
        arr = arrows.Arrows.from_json("config/schema.json")
        if connection  and  connection.is_connected():
            sbm = self.from_sbml_custom(xml_string, tag=tag)
            node = sbm.format_nodes(arr.nodes)
            relationship = sbm.format_relationships(arr.relationships)
            connection.create_nodes(nodes=node)
            connection.create_relationships(relationships=relationship)
        else:
            raise ConnectionError("Failed to connect to Neo4j")

    def execute_query(self, query_str: str , return_results:bool=False, operation:str=neo4j.READ_ACCESS) -> Optional[List]:
        conn = get_connection()
        if conn :
            return conn.query(value=query_str, expect_data=return_results, access=operation)
        print("Connection down!!!")


    def get_embedding(self ,texts:str, query="document"):
        vo  = voyageai.Client()
        result = vo.embed([texts], model="voyage-2", input_type=query)
        return result.embeddings[0]

    def templated_query(self, tag, description):
        conn = get_connection()
        if conn:
            with conn.driver.session(database=conn.database,default_access_mode=neo4j.WRITE_ACCESS) as session:
                res = session.run("""
                    MATCH(n:Model)
                    WHERE n.tag = $tag
                    SET n.description = $description
                    """, tag=tag, description=description)
                return res.data()

    def vector_index(self):
        conn = get_connection()
        if conn:
            with conn.driver.session(database=conn.database,default_access_mode=neo4j.WRITE_ACCESS) as session:
                session.run("""
                    CREATE VECTOR INDEX `desc_embedding` IF NOT EXISTS
                        FOR (m:Model) ON (m.descEmbedding)
                        OPTIONS {
                            indexConfig :{
                                `vector.dimensions`: 1024,
                                `vector.similarity_function`: 'cosine'
                                }
                        }
                      """)

    def populate_vector_index(self):
        conn = get_connection()
        if conn:
            with conn.driver.session(database=conn.database,default_access_mode=neo4j.WRITE_ACCESS) as session:
                # Fetch all models where descEmbedding is NULL
                result = session.run("""
                    MATCH (m:Model)
                    WHERE m.descEmbedding IS NULL
                    RETURN m.description AS description, id(m) AS model_id
                """)

                for record in result:
                    description = record["description"]
                    model_id = record["model_id"]
                    if description:
                        embedding = self.get_embedding(description)
                        session.run("""
                            MATCH (m:Model) WHERE id(m) = $model_id
                            SET m.descEmbedding = $embedding
                            """, model_id=model_id, embedding=embedding)

    def similarity_search(self, question: str):
        conn = get_connection()
        embbeding = self.get_embedding(question, query='query')

        if conn:
            with conn.driver.session(database=conn.database,default_access_mode=neo4j.WRITE_ACCESS) as session:
                res = session.run(
                    """
                    CALL db.index.vector.queryNodes(
                        'desc_embedding',
                        $topK,
                        $question_embedding
                    ) YIELD node AS model, score
                    RETURN model.name as name, model.description as desc, score
                    """, topK=10, question_embedding=embbeding).data()
                return res
        return {"message": "Connection Down "}

class AppController:
    def __init__(self, sbml_service):
        self.sbml_service:SBMLService = sbml_service

    async def process_files_async(self, xml_strings: List[str] ,tags: List[str]):
        loop = asyncio.get_running_loop()
        print(tags)
        tasks = [
            loop.run_in_executor(ProcessPoolExecutor(max_workers=5), self.process_uploaded_file, xml_str, tags[index])
            for index, xml_str in enumerate(xml_strings)
        ]
        await asyncio.gather(*tasks)

    def process_uploaded_file(self, xml_string, tag=None):
        try:
            self.sbml_service.process_model(xml_string, tag)
            return {"message": "Success!"}
        except Exception as e:
            return {"error": str(e)}
