from asyncio.tasks import sleep
from copy import Error
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Any, Tuple
import asyncio
import neo4j
from biomodels_restful_api_client import services as bmservice
import html2text

from service import SBMLService, AppController

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sbml_service = SBMLService()
app_controller = AppController(sbml_service=sbml_service)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}


def set_model_description(ids: List[str]) :
    for id in ids :
        try:
            desc = bmservice.get_model_info(id)
            if desc:
                desc['description']
                text = html2text.html2text(desc)
                sbml_service.templated_query(tag=id, description=desc)

        except Exception:
            print("Server is down")

@app.post("/process-sbmls")
async def process_sbml(sbml_files: List[UploadFile] = File(...)):
    _bytes, file_names = await read_all_async(sbml_files)

    decoded_contents = [item.decode() for item in _bytes]
    await app_controller.process_files_async(decoded_contents, file_names)
    await merge_molecules()

    sbml_service.vector_index()
    sbml_service.populate_vector_index()
    set_model_description(file_names)


    return {"message": "OK"}

@app.get("/source-data")
async def get_nodes_links() :
    await create_graph_projection()
    await write_community()
    res =  sbml_service.execute_query("""
       MATCH (n)-->(m)
       WITH
         COLLECT(DISTINCT {id: id(n), name: n.name, community: head(n.community), group: head(labels(n))}) AS sourceNodes,
         COLLECT(DISTINCT {id: id(m), name: m.name, community: head(m.community), group: head(labels(m))}) AS targetNodes,
         COLLECT({source: id(n), target: id(m), value: 1}) AS links
       RETURN {
         nodes: sourceNodes + targetNodes,  // Combine source and target nodes
         links: links  // Return links
       } AS graphData;
       """, True)
    await drop_graph_projection()
    if res:
        return res[0]["graphData"]
    return {}

@app.get('/species')
async def get_all_communities() :
    return sbml_service.execute_query("""
        MATCH (n:Species)
        RETURN n.name as name, head(n.community) as cluster
    """, True)

async def read_all_async(sbml_files: List[UploadFile]) -> Tuple[List[bytes], List[str]]:
    # Read the file content asynchronously
    file_contents = await asyncio.gather(*[sbml_file.read() for sbml_file in sbml_files])

    # Get the filenames (this is not an asynchronous operation)
    filenames = [
        sbml_file.filename[0: sbml_file.filename.index('_')]
        if sbml_file.filename else '' for sbml_file in sbml_files
    ]

    return file_contents, filenames

@app.get('/chat')
async def chat(question: str):
   return sbml_service.similarity_search(question)

async def merge_molecules() :
    return sbml_service.execute_query("""
    MATCH (n:Species)
    WITH n.name as name, collect(n) as nodes
    WHERE size(nodes) > 1
    CALL apoc.refactor.mergeNodes(nodes, {properties : "combine"}) YIELD node
    RETURN node
    """, True, neo4j.WRITE_ACCESS)

async def create_graph_projection():
    sbml_service.execute_query("""
        CALL gds.graph.exists('moleculeGraph')
        YIELD exists
        WITH exists
        WHERE exists = false
        CALL gds.graph.project(
            'moleculeGraph',
            ['Species', 'Reaction', 'Compartment', 'Model', 'KineticLaw', 'Unit', 'UnitDefinition', 'Parameter'],
            {
                HAS_COMPARTMENT: {orientation: 'UNDIRECTED'},
                IS_REACTANT: {orientation: 'UNDIRECTED'},
                HAS_REACTION: {orientation: 'UNDIRECTED'},
                HAS_PRODUCT: {orientation: 'UNDIRECTED'},
                HAS_SPECIES: {orientation: 'UNDIRECTED'},
                IS_COMPOSED: {orientation: 'UNDIRECTED'},
                HAS_UNITDEFINITION: {orientation: 'UNDIRECTED'},
                HAS_KENETICLAW: {orientation: 'UNDIRECTED'},
                IN_COMPARTMENT: {orientation: 'UNDIRECTED'}
            }
        )
        YIELD graphName, nodeProjection, relationshipProjection
        RETURN graphName, nodeProjection, relationshipProjection;
""" ,False)

async def write_community():
    sbml_service.execute_query("""
    CALL gds.louvain.write(
        'moleculeGraph',
        {
            writeProperty: 'community',
            maxIterations: 10,
            includeIntermediateCommunities: true
        }
    )
    YIELD communityCount, modularity
    """, True, neo4j.WRITE_ACCESS)

async def drop_graph_projection():
    sbml_service.execute_query("CALL gds.graph.drop('moleculeGraph') YIELD graphName;", False)
