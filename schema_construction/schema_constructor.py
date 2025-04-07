"""
Input: .csv files
Based on the header of the .csv files, the schema_constructor will generate a schema for the data.
- The schema levels can be found in schema/levels.json.
- The initial schema can be found in schema/initial_template.json.
- The schema will be saved in schema/schema.json.
"""

from language_model.chat_client_factory import client_selector
from utils.helper import save_json, find_docs_in_folder


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
