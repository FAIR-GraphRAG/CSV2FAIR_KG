import json
import csv


def save_ontology2json(ontology_csv_path, schema_path, output_json_path):
    # Load the existing dataset schema
    with open(schema_path, "r") as f:
        dataset_data = json.load(f)

    # Load ontology mappings from CSV
    mappings = {}
    with open(ontology_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            mappings[row["OldJSONKey"]] = {
                "value": "",
                "ontology_term": row["OntologyTerm"],
                "ontology_name": row["SelectedOntology"],
                "ontology_link": row["OntologyLink"],
            }

    # Work on a copy
    result = dataset_data.copy()

    # Iterate through each study object and enrich its properties
    for study_obj_key, study_obj in result.get("properties", {}).items():
        study_obj_properties = study_obj.get("properties", {})

        # If properties is a list, convert it to a dict with enrichment
        if isinstance(study_obj_properties, list):
            new_props = {}
            for prop in study_obj_properties:
                if prop in mappings:
                    new_props[prop] = mappings[prop].copy()
                else:
                    new_props[prop] = {"value": ""}
            # Replace properties list with the new dict
            result["properties"][study_obj_key]["properties"] = new_props
        elif isinstance(study_obj_properties, dict):
            # If it's already a dict, update/enrich each property
            for prop in study_obj_properties:
                if prop in mappings:
                    study_obj_properties[prop].update(mappings[prop])
                else:
                    if "value" not in study_obj_properties[prop]:
                        study_obj_properties[prop]["value"] = ""
            result["properties"][study_obj_key]["properties"] = study_obj_properties

    # Save enriched schema
    with open(output_json_path, "w", encoding="utf-8") as out:
        json.dump(result, out, indent=2, ensure_ascii=False)

    print("Enrichment done and schema saved to:", output_json_path)


# Usage:
# save_ontology2json('ontology.csv', 'schema.json', 'output.json')
