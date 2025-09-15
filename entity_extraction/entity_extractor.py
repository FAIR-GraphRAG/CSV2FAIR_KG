from utils.helper import find_docs_in_folder, read_json, save_json
import copy


def extract_field(document, field_name):
    if hasattr(document, "page_content"):
        content = document.page_content
        for line in content.splitlines():
            if line.startswith(f"{field_name}:"):
                return line.split(":", 1)[1].strip()
        return None
    return document.get(field_name, None)


def extract_entities(data_dir, csv_dir, output_dir, json_file):
    # For each table row fill each schema object by extracting information using matching property keys
    # If values include separators (e.g., //) then split and create separate entities if it is not the full row entity class
    # For each table fill one schema that maintains the main structure as the original base schema

    base_schema = read_json(json_file)
    table_documents = find_docs_in_folder(csv_dir, data_dir, cut_file=False)

    # List all types in order as per schema
    all_types = list(base_schema["properties"].keys())
    first_type = all_types[0]

    for i, table in enumerate(table_documents):
        table_name = f"table_{i + 1}"

        filled_schema = {
            "$schema": base_schema["$schema"],
            "title": base_schema["title"],
            "description": base_schema["description"],
            "properties": {},
        }
        type_counters = {k: 0 for k in base_schema["properties"].keys()}

        for record in table:
            for obj_type, obj_schema in base_schema["properties"].items():
                obj_props = obj_schema["properties"]
                property_list = []
                for prop in obj_props:
                    val = extract_field(record, prop)
                    if val is not None:
                        if obj_type != first_type and "//" in val:
                            # Split for all but the first type
                            split_values = [
                                v.strip() for v in val.split("//") if v.strip()
                            ]
                            for idx, split_val in enumerate(split_values):
                                # Key format: type_counter is 2 digits, e.g., GO-BP_00, GO-BP_01
                                key = f"{obj_type}_{type_counters[obj_type]:02d}"
                                type_counters[obj_type] += 1
                                filled_schema["properties"][key] = {
                                    "$schema": obj_schema["$schema"],
                                    "title": obj_schema["title"],
                                    "description": obj_schema["description"],
                                    "properties": [{prop: split_val}],
                                }
                        else:
                            property_list.append({prop: val})

                # Only add if there are properties and it's the first type,
                # or if it's not the first type and splitting was not needed
                if property_list and obj_type == first_type:
                    key = f"{obj_type}_{type_counters[obj_type]}"
                    type_counters[obj_type] += 1
                    filled_schema["properties"][key] = {
                        "$schema": obj_schema["$schema"],
                        "title": obj_schema["title"],
                        "description": obj_schema["description"],
                        "properties": property_list,
                    }
        save_json(f"{output_dir}/{table_name}.json", filled_schema)
