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
- adding metadata
  - use geofetch to fetch GEO metadata
  - metadata is available in PEP format
  - PEP contains _GSE.soft for the experiment and _GSM.soft for the individual samples 
  - For testing I used: GSE244832 and GSE280797
  - GSE244832 is available as .bed (biomedical format) and also as processed files
  - Problem: the sample metadata can't be assigned to specific rows
  - Solution: 
    - define mandatory metadata for row/component level, save the rest in document level
    - use of Dublin Core Metadata Elements standard
    - use LLM to map fill dublin schema with information from _GSE.soft
    - rest of metadata are saved in Document-Level FAIR DO
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