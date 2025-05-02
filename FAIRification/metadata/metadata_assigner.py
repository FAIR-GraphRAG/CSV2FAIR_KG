"""
- NOT IN USE (up to now, component metadata do not differ from dataset metadata)
- Assigns metadata to Component-Level FAIR DOs
- Each Component-Level is assigned with the tables minimal metadata
"""

from utils.helper import read_json, save_json
import os

schema_dir = "data/extracted_data/filled_schema"
metadata_dir = "data/extracted_data/metadata"


def assign_metadata():
    # Iterate through schema files
    for file_name in os.listdir(schema_dir):
        if file_name.endswith(".json"):
            schema_path = os.path.join(schema_dir, file_name)
            metadata_path = os.path.join(metadata_dir, file_name)

            if os.path.exists(metadata_path):
                schema_data = read_json(schema_path)
                metadata = read_json(metadata_path)

                # Add metadata to each study object
                properties = schema_data.get("properties", {})
                for obj in properties.values():
                    obj["metadata"] = metadata

                save_json(schema_path, schema_data)

            else:
                print(f"⚠️ Skipped: No metadata for {file_name}")
