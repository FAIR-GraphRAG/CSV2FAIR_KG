"""
Input: .csv files
Based on the header of the .csv files, the schema_constructor will generate a schema for the data.
- The schema levels can be found in schema/levels.json.
- The initial schema can be found in schema/initial_template.json.
- The schema will be saved in schema/schema.json.
"""

from langchain_community.document_loaders.csv_loader import CSVLoader
import os
from language_model.chat_client_factory import client_selector
from utils.helper import save_json


def load_docs(report_folder):
    documents = []
    for filename in os.listdir(report_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(report_folder, filename)
            loader = CSVLoader(file_path=file_path)
            data = loader.load()
            if data:  # Make sure there's at least one row
                documents.append(data[0])  # Append the header/first row
    return documents


def find_docs_in_folder(csv_dir, data_dir):
    """
    For each csv_dir in data_dir call load_doc function
    return list of Documents: [Document, Document]
    """
    documents = []
    for current_root, dirs, files in os.walk(data_dir):
        for dir_name in dirs:
            if dir_name == csv_dir:
                csv_data_path = os.path.join(current_root, dir_name)
                documents.extend(load_docs(csv_data_path))
    return documents


def create_schema():
    """
    Input: langchain documents
    """
    data_dir = "data/hepatic"
    csv_dir = "csv_data"
    documents = find_docs_in_folder(csv_dir, data_dir)
    response = client_selector("schema_construction", documents)

    # Save the schema
    output_path = "data/schema/schema.json"
    try:
        save_json(output_path, response)
    except Exception as e:
        print("Error in create_initial_schema:", e)
