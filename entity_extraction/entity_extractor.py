"""
- Prerequisites: constructed schema
- Goal: fill schema for each table
- Process:
1. Iterate over each table
2. Hand over table and schema to LLM
3. Instruct LLM to find semantic meaning
4. Programmatically fill schema based on semantic meaning
"""

from utils.helper import find_docs_in_folder, read_json, save_json
from language_model.chat_client_factory import client_selector
import copy


def extract_field(document, field_name):
    content = getattr(document, "page_content", document)
    for line in content.splitlines():
        if line.startswith(f"{field_name}:"):
            return line.split(":", 1)[1].strip()
    return None


def extract_entities():
    """
    - For each table create a filled schema using its semantic meaning (see table_semantics)
    - For each table row create one study object using the row values, assuming the header (first row) defines the property names
    - The filled schema maintains the main structure as the original base schema
    """
    data_dir = "data/hepatic"
    csv_dir = "csv_data"
    output_dir = "data/extracted_data/"

    # Load (header + first row) for table-level semantic extraction
    sample_documents = find_docs_in_folder(csv_dir, data_dir)
    # Example expected output from LLM: [{'table': 'Gene'}, ...]
    table_semantics = client_selector("entity_extraction", sample_documents)

    base_schema = read_json("data/schema/schema.json")

    # Load full table documents (all rows)
    table_documents = find_docs_in_folder(csv_dir, data_dir, cut_file=False)

    schema_copy = copy.deepcopy(base_schema)
    schema_copy["level_1"]["properties"] = {}

    for i, table in enumerate(table_documents):
        table_name = f"table_{i + 1}"

        # Iterate through records
        for j, record in enumerate(table):
            object_study_name = table_semantics[i]["table"]
            study_object_schema = base_schema["level_1"]["properties"][
                object_study_name
            ]

            study_object_list = []
            if isinstance(study_object_schema["properties"], list):
                for entry in study_object_schema["properties"]:
                    list_match = extract_field(record, entry)
                    if list_match:
                        study_object_list.append({entry: list_match})

            # Create new study object
            table_study_object = {
                "$schema": study_object_schema["$schema"],
                "title": study_object_schema["title"],
                "description": study_object_schema["description"],
                "properties": study_object_list,
            }
            # Update filled schema
            schema_copy["level_1"]["properties"][
                f"{object_study_name}_{j}"
            ] = table_study_object
        save_json(f"{output_dir}{table_name}.json", schema_copy)
