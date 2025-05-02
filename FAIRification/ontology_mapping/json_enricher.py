import os
import json
from utils.helper import read_json


def write_properties(properties, ontology_schema, out_f):
    for i, (study_obj_name, study_obj_content) in enumerate(properties.items()):
        if i > 0:
            out_f.write(",\n")

        new_stud_obj = {}

        for sub_key, sub_value in study_obj_content.items():
            if sub_key in ["pid", "metadata", "$schema", "title", "description"]:
                new_stud_obj[sub_key] = sub_value
            elif sub_key == "properties" and isinstance(sub_value, list):
                new_props = {}

                for prop in sub_value:
                    for prop_key, prop_value in prop.items():
                        if prop_key in ontology_schema:
                            enriched_prop = {
                                **ontology_schema[prop_key],
                                "value": prop_value,
                            }
                            new_props[prop_key] = enriched_prop
                        else:
                            new_props[prop_key] = prop_value

                new_stud_obj["properties"] = new_props

        # Write enriched study object
        out_f.write(f'      "{study_obj_name}": {json.dumps(new_stud_obj)}')


def enrich_and_stream_write(file_path, data, ontology_schema):
    properties = data.get("properties", {})

    # Prepare non-properties metadata
    enriched_metadata = {
        key: data[key]
        for key in ["pid", "metadata", "$schema", "title", "description"]
        if key in data
    }

    with open(file_path, "w") as out_f:
        out_f.write("{\n")

        # Write metadata
        meta_items = [
            f'    "{k}": {json.dumps(v)}' for k, v in enriched_metadata.items()
        ]
        out_f.write(",\n".join(meta_items))

        # Writing properties
        out_f.write(',\n    "properties": {\n')
        write_properties(properties, ontology_schema, out_f)

        # Close JSON structure
        out_f.write("\n    }\n  }")


def enrich_with_ontology(data_path, schema_path):
    schema = read_json(schema_path)
    for filename in os.listdir(data_path):
        if filename.endswith(".json"):
            file_path = os.path.join(data_path, filename)
            data = read_json(file_path)
            enrich_and_stream_write(file_path, data, schema)
