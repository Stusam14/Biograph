# BioGraph



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.


# Packages

```shell
pip install biomodels-restful-api-client
pip install html2text
pip install -U voyageai
export VOYAGE_API_KEY="<your secret key>"
```

# Docker
```shell
docker run -d \--publish=7474:7474 --publish=7687:7687 \                                                          biograph
    --volume=$HOME/neo4j/data:/data \
    --env NEO4J_AUTH=neo4j/capstone-biograph --env NEO4J_PLUGINS='["apoc","graph-data-science"]' neo4j:latest
```
