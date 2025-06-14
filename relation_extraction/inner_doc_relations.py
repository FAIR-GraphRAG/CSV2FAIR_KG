import os
from utils.helper import read_json, save_json

JSON_DIR = "data/extracted_data/filled_schema"


def _append_relation(section: dict, rel_obj: dict):
    section.setdefault("relations", []).append(rel_obj)


def _split_values(raw_val: str) -> set[str]:
    """
    Given a raw string (possibly containing "//"-separated entries),
    split on "//", strip whitespace, and return a set of non-empty tokens.
    """
    if not isinstance(raw_val, str):
        return set()
    parts = [p.strip() for p in raw_val.split("//")]
    return {p for p in parts if p}


def add_entity_links(data, first_type_name):
    # Collect entities by their type prefix (e.g. "gene", "GO-BP", etc.)
    entities_by_type: dict[str, list[dict]] = {}
    for key, section in data.get("properties", {}).items():
        entity_type = key.split("_", 1)[0]
        entities_by_type.setdefault(entity_type, []).append(section)

    if first_type_name not in entities_by_type:
        return

    # For each first-type entity (e.g. each "gene_X")
    for first_section in entities_by_type[first_type_name]:
        first_pid = first_section.get("pid")
        first_props = first_section.get("properties", {})

        # Build a set of all atomic values in the first entity
        first_values_atoms: set[str] = set()
        for v_dict in first_props.values():
            if isinstance(v_dict, dict) and "value" in v_dict:
                raw = v_dict["value"]
                first_values_atoms.update(_split_values(raw))

        # For each other entity type
        for other_type, other_entities in entities_by_type.items():
            if other_type == first_type_name:
                continue

            for other_section in other_entities:
                other_pid = other_section.get("pid")
                other_props = other_section.get("properties", {})

                # Build a set of all atomic values in the other entity
                other_values_atoms: set[str] = set()
                for v_dict in other_props.values():
                    if isinstance(v_dict, dict) and "value" in v_dict:
                        raw = v_dict["value"]
                        other_values_atoms.update(_split_values(raw))

                # If any atomic token overlaps, create a relation
                if first_values_atoms & other_values_atoms:
                    rel_obj = {
                        "node1": first_pid,
                        "relation_label": f"HAS_{other_type.replace('-', '_').upper()}",
                        "node2": other_pid,
                    }
                    _append_relation(first_section, rel_obj)

                    # Optional reverse relation:
                    # rel_obj_rev = {
                    #     "node1": other_pid,
                    #     "relation_label": f"IS_{other_type.replace('-', '_').upper()}_OF",
                    #     "node2": first_pid,
                    # }
                    # _append_relation(other_section, rel_obj_rev)


def add_belongs_to(data):
    dataset_pid = data.get("pid", "")
    for section in data.get("properties", {}).values():
        pid = section.get("pid")
        if not pid:
            continue
        rel_obj = {
            "node1": pid,
            "relation_label": "BELONGS_TO",
            "node2": dataset_pid,
        }
        _append_relation(section, rel_obj)


def find_relations():
    # Read the top‐level schema in order to identify the "first type"
    schema_path = "data/schema/schema.json"
    from utils.helper import read_json as read_json_schema

    schema = read_json_schema(schema_path)
    first_type_name = list(schema["properties"].keys())[0]

    for filename in os.listdir(JSON_DIR):
        if not filename.endswith(".json"):
            continue
        file_path = os.path.join(JSON_DIR, filename)
        data = read_json(file_path)

        add_entity_links(data, first_type_name=first_type_name)
        add_belongs_to(data)

        save_json(file_path, data)
        print(f"Linked entities in {filename}")
