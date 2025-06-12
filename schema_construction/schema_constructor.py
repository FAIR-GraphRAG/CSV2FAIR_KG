import os
import json
from language_model.chat_client_factory import client_selector
from utils.helper import save_json, read_json, find_docs_in_folder

# Make sure ENTITY_CLASS_LIST is defined in your config.py
from config.config import ENTITY_CLASS_LIST


def create_schema():
    """
    1. Generate an initial schema via LLM (client_selector).
    2. Save it to data/schema/schema.json.
    3. Re-open schema.json, append an object for each class in ENTITY_CLASS_LIST,
       using the initial_schema_object template from initial_schema.json.
    4. Write back the augmented schema.
    """
    # 1) Step 1: call your LLM to build the base schema
    data_dir = "data/hepatic"
    csv_dir = "csv_data"
    documents = find_docs_in_folder(csv_dir, data_dir)
    base_schema = client_selector("schema_construction", documents)

    output_path = "data/schema/schema.json"

    # 4) Load the `initial_schema_object` template from initial_schema.json
    #    This file should have a structure like:
    #    {
    #      "initial_schema_object": {
    #        "$schema": "...",
    #        "title": "Title",
    #        "description": "Description",
    #        "properties": ["list", "of", "keys"]
    #      },
    #      "initial_schema_wrapper": { … },
    #      "example_schema": { … }
    #    }
    template_path = "data/schema/initial_schema.json"
    try:
        with open(template_path, "r") as f:
            initial_wrapper = json.load(f)
    except Exception as e:
        print("Error loading initial_schema.json:", e)
        return

    if "initial_schema_object" not in initial_wrapper:
        print("initial_schema.json is missing the key 'initial_schema_object'")
        return

    obj_template = initial_wrapper["initial_schema_object"]

    # 5) Ensure our base_schema has a top‐level "properties" dict
    if "properties" not in base_schema or not isinstance(
        base_schema["properties"], dict
    ):
        print(
            "The loaded schema.json does not have a valid top‐level 'properties' object."
        )
        return

    # 6) For each entity class in ENTITY_CLASS_LIST, append a new object if not already present
    for entity in ENTITY_CLASS_LIST:
        # If the schema already contains this key, skip it
        if entity in base_schema["properties"]:
            continue

        # Make a deep copy of the template so we don’t overwrite the original
        new_obj = json.loads(json.dumps(obj_template))

        # Fill in "title" (capitalize the entity) and a generic description
        new_obj["title"] = entity
        new_obj["description"] = f"Information related to {entity}"

        # The template’s "properties" list should be replaced by a single‐item list [entity]
        new_obj["properties"] = [entity]

        # Insert the new object under the top‐level key = entity
        base_schema["properties"][entity] = new_obj

    # 7) Write the augmented schema back to disk
    try:
        save_json(output_path, base_schema)
        print(f"Schema successfully augmented and saved to {output_path}")
    except Exception as e:
        print("Error saving the augmented schema:", e)
