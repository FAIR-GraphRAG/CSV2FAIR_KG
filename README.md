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


## Pipeline Overview

This section describes the stages of the system.

---

### 1. Document Collection to Schema

- **Component-Level Definition:**  
  - Define components in Component-Level in `data/schema/levels.json`.
  - Iteratively extract keywords using `levels.json` and `.csv` tables.
  - Save schema as `schema.json`.

- **Unified Vocabulary Creation:**  
  - Build a unified vocabulary from the extracted keywords.
  - Map schema keys to the vocabulary and update the schema accordingly.

---

### 2. Schema to Extracted Entities

- **Entity Extraction:**  
  - Leverage LLM to perform extraction based on the schema.
  - Fill the schema with the extracted entities.

---

### 3. Extracted Entities to FAIR DO Entities

- **Metadata Enrichment:**  
  - **GEO Metadata:**  
    - Retrieve geographical metadata using `geofetch`.
    - Metadata is available in the PEP format, including `_GSE.soft` for experiments and `_GSM.soft` for individual samples.
    - Testing was performed with datasets: **GSE244832** and **GSE280797**.
  - **Additional Data Formats:**  
    - **GSE244832:** Provided as both biomedical `.bed` files and processed file formats.
  - **Challenges and Solutions:**  
    - **Problem:** Sample metadata cannot be directly assigned to specific rows.
    - **Solution:**  
      - Define mandatory metadata at the row/component level; store the remainder at the document level.
      - Utilize the Dublin Core Metadata Elements standard.
      - Employ an LLM to enrich the Dublin schema with information from `_GSE.soft`.
      - Save remaining metadata at the Document-Level FAIR DO.

- **Ontology Mapping:**  
  - Map schema keys to the UMLS vocabulary.
  - Integrate additional or new ontology based on the mapped vocabulary and table values.

---

### 4. FAIR DO Entities to FAIR DO Entities & Relations

- **Embedding of Entities:**  
  - Generate embeddings using an embedding model.
- **Relation Extraction:**  
  - Extract relations based on the generated embeddings.
  - Perform extraction across multiple levels:
    - Cross-level
    - Inner-level
    - Inner-document

---

### 5. FAIR DO Entities & Relations to FAIR Knowledge Graph

- **Graph Integration:**  
  - Integrate entities (nodes) and relations (edges) into a Neo4j knowledge graph.
  - Validate integration using SHACL tests.

---

### Todos

- **Document-Level Nodes:**  
  - Construct Document-Level nodes that encapsulate full document content


## Legal Notice

This project utilizes data from the [Unified Medical Language System (UMLS) Metathesaurus](https://www.nlm.nih.gov/research/umls/) provided by the [National Library of Medicine (NLM)](https:/www.nlm.nih.gov/). 

**Version:** 2024-01-08

Use of the UMLS Metathesaurus is governed by the [UMLS Knowledge Sources Terms of Use](https://www.nlm.nih.gov/databases/download/terms_and_conditions.html). All users must comply with these terms and provide the correct attribution as specified in the official guidelines.

For the most up-to-date citation information, please consult the NLM documentation.
