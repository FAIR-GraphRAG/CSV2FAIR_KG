import json
from langchain_community.document_loaders.csv_loader import CSVLoader
import os
import re


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def save_json(file_path, json_data):
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)
    print(f"\nJSON saved to {file_path}")


def extract_schema_keywords(schema):
    properties_list = []

    if isinstance(schema, dict):
        # If the current dictionary has a "properties" key and is a list, add its value
        if "properties" in schema and isinstance(schema["properties"], list):
            properties_list.extend(schema["properties"])
        # Recursively search through each value in the dictionary
        for key, value in schema.items():
            properties_list.extend(extract_schema_keywords(value))
    return properties_list


def load_docs(report_folder, cut_file=True):
    documents = []
    for filename in os.listdir(report_folder):

        if filename.endswith(".csv"):
            file_path = os.path.join(report_folder, filename)
            loader = CSVLoader(file_path=file_path)
            data = loader.load()
            if data:
                if cut_file:
                    documents.append(data[0])  # Append the header + first row
                else:
                    documents.append(data)
        elif filename.endswith(".soft"):  # GEO soft file
            file_path = os.path.join(report_folder, filename)
            with open(file_path, "r") as file:
                lines = file.readlines()
                if lines:  # Ensure the file isn’t empty
                    documents.append(lines)
    return documents


def find_docs_in_folder(csv_dir, data_dir, cut_file=True):
    """
    For each csv_dir in data_dir call load_doc function
    return list of Documents: [Document, Document]
    """
    documents = []
    for current_root, dirs, files in os.walk(data_dir):
        for dir_name in dirs:
            if dir_name == csv_dir:
                csv_data_path = os.path.join(current_root, dir_name)
                documents.extend(load_docs(csv_data_path, cut_file=cut_file))
    return documents


def extract_list(llm_output: str) -> list:
    """
    Extract a JSON-style Python list from an LLM output string.
    Handles markdown-style formatting like ```json [ ... ] ```.

    Parameters:
        llm_output (str): Raw string from the LLM (e.g., result.content)

    Returns:
        list: Python list of keys, or [] if parsing fails
    """
    try:
        # Find the first bracketed list
        match = re.search(r"\[.*?\]", llm_output, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except json.JSONDecodeError as e:
        print("JSON parsing error:", e)
    return []


def greedy_like_for_demonstration():
    data = {"UO": ["height", "weight"], "PATO": ["height", "age"], "CHMO": ["age"]}
    uncovered = set(["height", "weight", "age"])
    assignment = {}
    selected_ontologies = set()

    while uncovered:
        best_ontology = None
        best_cover = set()

        for ontology, terms in data.items():
            cover = uncovered.intersection(terms)
            if len(cover) > len(best_cover):
                best_cover = cover
                best_ontology = ontology

        if not best_cover:
            break

        for term in best_cover:
            assignment[term] = best_ontology

        uncovered -= best_cover
        selected_ontologies.add(best_ontology)

    print("Assignment:", assignment)
    print("Selected Ontologies:", selected_ontologies)
