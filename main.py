from schema_construction.schema_constructor import create_schema
from entity_extraction.entity_extractor import extract_entities
from FAIRification.persistent_identifier.pid_creator_dataset import update_with_doi
from FAIRification.persistent_identifier.pid_creator_component import add_pid_to_json
from FAIRification.ontology_mapping.ontology_factory import add_ontology_mappings
from FAIRification.metadata.metadata_extractor import extract_metadata
from FAIRification.metadata.metadata_assigner import assign_metadata
from relation_extraction.inner_doc_relations import find_relations
from relation_extraction.non_fair_inner_doc_relations import non_fair_find_relations
from graph_DB.neo4j_json_client import insert_data
from graph_DB.non_fair_neo4j_json_client import non_fair_insert_data
from config.config import FAIR_GRAPH

# input data
DATA_DIR = "data/hepatic"
CSV_DIR = "csv_data"
# ontology
CSV_MATCHES = "data/ontology/ontology_matches.csv"
CSV_SELECTIONS = "data/ontology/ontology_selections.csv"
# schema
ONTOLOGY_SCHEMA = "data/schema/ontology_schema.json"
JSON_FILE = "data/schema/schema.json"
INITIAL_SCHEMA = "data/schema/initial_schema.json"
JSON_DIR = "data/extracted_data/filled_schema"
JSON_GLOB = "data/extracted_data/filled_schema/*.json"
# metadata
METADATA_INPUT = "metadata_PEP"
METADATA_DIR = "data/extracted_data/metadata"
METADATA_GLOB = "data/extracted_data/metadata/*.json"


if __name__ == "__main__":
    print(
        """
        ----------------------
        GRAPH CONSTRUCTION
        ----------------------
        """
    )

    if FAIR_GRAPH:
        create_schema(JSON_FILE, INITIAL_SCHEMA)
        extract_entities(DATA_DIR, CSV_DIR, JSON_DIR)
        update_with_doi(METADATA_DIR, JSON_DIR)
        add_pid_to_json(JSON_DIR)
        add_ontology_mappings(
            JSON_FILE, CSV_MATCHES, CSV_SELECTIONS, ONTOLOGY_SCHEMA, JSON_DIR
        )
        extract_metadata(METADATA_INPUT, DATA_DIR, METADATA_DIR)
        assign_metadata(JSON_DIR, METADATA_DIR)
        find_relations(JSON_DIR)
        # insert_data(JSON_GLOB, METADATA_GLOB)
    else:
        create_schema(METADATA_DIR, JSON_FILE)
        extract_entities(DATA_DIR, CSV_DIR, JSON_DIR)
        non_fair_find_relations(JSON_DIR)
        # non_fair_insert_data(JSON_GLOB, METADATA_GLOB)
