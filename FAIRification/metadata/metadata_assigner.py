import re
import os
from utils.helper import read_json, save_json


def assign_metadata(schema_dir, metadata_dir):
    for file_name in os.listdir(schema_dir):
        if file_name.startswith("table_") and file_name.endswith(".json"):
            match = re.match(r"table_(\d+)\.json", file_name)
            if not match:
                print(f"⚠️ Skipped: Could not extract number from {file_name}")
                continue
            num = match.group(1)

            schema_path = os.path.join(schema_dir, file_name)
            schema_data = read_json(schema_path)
            changed = False

            # For dataset_X.json: add to first-level properties
            dataset_meta_path = os.path.join(metadata_dir, f"dataset_{num}.json")
            if os.path.exists(dataset_meta_path):
                metadata = read_json(dataset_meta_path)
                # If you want pid here too (add if needed)
                schema_data["metadata"] = metadata

            # For sample_X.json: add to each second-level properties object and include pid
            sample_meta_path = os.path.join(metadata_dir, f"sample_{num}.json")
            if os.path.exists(sample_meta_path):
                metadata = read_json(sample_meta_path)
                for obj in schema_data["properties"].values():
                    if "properties" in obj and isinstance(obj["properties"], dict):
                        # Make a shallow copy of metadata to avoid mutating the original
                        metadata_copy = metadata.copy()
                        if "pid" in obj:
                            metadata_copy["pid"] = obj["pid"]
                        obj["properties"]["metadata"] = metadata_copy
                        changed = True

            if changed:
                save_json(schema_path, schema_data)
            else:
                print(f"⚠️ Skipped: No matching metadata for {file_name}")
