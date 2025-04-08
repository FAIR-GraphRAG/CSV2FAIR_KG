"""
- From folder metadata_PEP extract _GSE.soft and _GSM.soft
- Feed _GSE.soft (experiment metadata) to the LLM factory
- LLM extracts metadata for Component-Level FAIR DOs
- Save metadata in json file
"""

from language_model.chat_client_factory import client_selector
from utils.helper import save_json, find_docs_in_folder


def extract_metadata():
    metadata_dir = "metadata_PEP"
    data_dir = "data/hepatic"
    output_path = "data/extracted_data/"

    documents = find_docs_in_folder(metadata_dir, data_dir)
    for i, doc in enumerate(documents):
        response = client_selector("metadata_extraction", doc)
        # Save the schema
        if response:
            try:
                save_json(output_path + f"metadata_table_{i+1}.json", response)
            except Exception as e:
                print("Error in create_initial_schema:", e)
