# Table2FAIR_KG
The **Table2FAIR_KG** module expects tables as input data and finally constructs a FAIR-compliant knowledge graph.

## Environment & Requirements
### Setup Environment
    ```bash
    python3 -m venv venv-tab2g
    source venv-tab2g/bin/activate
    ```
    ```bash
    pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    ```

## Functionality
- document collection -> schema construction:
  - definition of levels for Component-Level (data/schema/levels.json)
  - iterative keyword extraction based on levels.json and .csv tables
  - saving as schema.json
  - creation of a unified vocabulary based on keywords
  - map schema keys to vocabulary, save updated schema
- schema -> extracted entities:
  - use LLM for extraction, fill schema
- ontology mapping:
  - use ontology from mapped vocabulary/find new ontology
  - ontology based on values of tables
  - schema keys are mapped to UMLS vocabulary
- embedding of entities
  - using some embedding model
- relation extraction
  - based on embeddings
  - cross-level
  - inner-level
  - inner-document
- Todo: construct Document-Level nodes based on full doc content
- Integration:
  - integrate entities/relations as nodes/edges into neo4j
  - Test integration using SHACL
  - Add user interface using neoconverse (use built-in solution)
  - Try/evaluate complete RAG system


## Legal
- Use of UML Metathesaurus from National Library of Medicine (NLM)
- Version: 2024-01-08
- TODO: look-up correct citation