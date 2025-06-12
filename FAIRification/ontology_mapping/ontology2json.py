import json
import csv


def save_ontology2json(ontology_csv_folder, schema_folder, json_folder):
    """
    Process:
    1. Load the json schema
    2. Load CSV ontology mappings
    3. Create a JSON object with the ontology mappings
    4. Write the JSON object to a file
    """
    with open(schema_folder, "r") as f:
        dataset_data = json.load(f)

    mappings = {}
    with open(ontology_csv_folder, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mappings[row["OldJSONKey"]] = {
                "value": "",
                "ontology_term": row["OntologyTerm"],
                "ontology_name": row["SelectedOntology"],
                "ontology_link": row["OntologyLink"],
            }

    result = {}
    dataset_properties = dataset_data["properties"]  # study objects
    print(dataset_properties)
    for study_obj in dataset_properties.values():
        study_obj_properties = study_obj["properties"]  # for each study obj
        study_obj_dict = {}
        for prop in study_obj_properties:  # for each study obj
            if prop in mappings:
                study_obj_dict[prop] = mappings[prop]
            else:
                study_obj_dict[prop] = {}
        result.update(study_obj_dict)

    with open(json_folder, "w") as out:
        json.dump(result, out, indent=2)
