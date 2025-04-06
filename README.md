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
- schema construction:
  - definition of levels for Component-Level (data/schema/levels.json)
  - iterative schema construction based on levels.json and .csv tables
- common vocabulary mapping:
  - uses UMLS from US Medicine Language System
  - maps each term to UMLS vocabulary
  - compares terms
  - Problem: some terms are not mapped correctly, no semantic context used
  - Try: LLM for context-aware mapping
- ontology mapping:
  - use ontology from mapped vocabulary/find new ontology
  - ontology based on values of tables
  - schema keys are mapped to UMLS vocabulary
- entity extraction
  - using LLM
- embedding of entities
  - using some embedding model
- relation extraction
  - based on embeddings
  - cross-level
  - inner-level
  - inner-document
- Todo: construct Document-Level nodes
- Integration:
  - integrate entities/relations as nodes/edges into neo4j
  - Test integration using SHACL
  - Add user interface using neoconverse (use built-in solution)
  - Try/evaluate complete RAG system


## Legal
- Use of UML Metathesaurus from National Library of Medicine (NLM)
- Version: 2024-01-08
- TODO: look-up correct citation