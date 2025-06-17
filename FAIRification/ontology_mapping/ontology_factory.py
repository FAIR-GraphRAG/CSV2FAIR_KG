from .ontology_recommender import recommend_ontologies
from .ontology_selector import select_ontologies
from .ontology2json import save_ontology2json
from .json_enricher import enrich_with_ontology

"""
Process Ist:
1. for each term in JSON schema, list all suitable ontology mappings
2. select the most suitable ontology for each term
3. create JSON schema with ontology mappings
4. enrich JSON schema with ontology information

Process Soll:
- use bioontology to map keywords to ontology terms
- use LLM to verify the mappings
- use LLM to create custom mappings for remaining keys
- save custom vocabulary
"""


def add_ontology_mappings(
    INPUT_JSON, CSV_MATCHES, CSV_SELECTIONS, ONTOLOGY_SCHEMA, EXTRACTED_JSON
):
    recommend_ontologies(INPUT_JSON, CSV_MATCHES)
    select_ontologies(CSV_MATCHES, CSV_SELECTIONS)
    save_ontology2json(CSV_SELECTIONS, INPUT_JSON, ONTOLOGY_SCHEMA)
    enrich_with_ontology(EXTRACTED_JSON, ONTOLOGY_SCHEMA)
