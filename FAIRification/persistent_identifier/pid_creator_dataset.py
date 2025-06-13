"""
Creates dummy DOIs via sandbox.zenodo for datasets
"""

import requests
from dotenv import load_dotenv
import os
import json
import langcodes
from utils.helper import read_json, save_json

load_dotenv()

zenodo_base_url = "https://sandbox.zenodo.org"
doi_base_url = "https://doi.org/"
dataset_metadata_dir = "data/extracted_data/metadata"
dataset_dir = "data/extracted_data/filled_schema"

ACCESS_TOKEN = os.getenv("ZENODO_SANDBOX_TOKEN")


def get_iso639_1_code(language_name):
    try:
        # Normalize and retrieve the language code
        language = langcodes.find(language_name)
        iso_code = language.language
        return iso_code
    except LookupError:
        print(f"Language '{language_name}' not recognized.")
        return None


def request_zenodo_doi(metadata):
    try:
        if "language" not in metadata:
            metadata["language"] = "en"
        elif metadata["language"] and len(metadata["language"]) != (2 or 3):
            # Language code mapping to ISO-639-1 or ISO-639-2
            iso_code = get_iso639_1_code(metadata["language"])
            metadata["language"] = iso_code
        data = {"metadata": metadata}
        headers = {"Content-Type": "application/json"}
        params = {"access_token": ACCESS_TOKEN}
        r = requests.post(
            f"{zenodo_base_url}/api/deposit/depositions",
            params=params,
            data=json.dumps(data),
            headers=headers,
        )
        # print(r.json())
        json_result = r.json()
        assigned_doi = json_result["metadata"]["prereserve_doi"]["doi"]
        print("\nDOI: ", assigned_doi)
        return assigned_doi
    except requests.exceptions.RequestException as e:
        print(f"Error requesting DOI: {e}")


def update_with_doi():
    for i, filename in enumerate(sorted(os.listdir(dataset_metadata_dir))):
        if filename.startswith("dataset") and filename.endswith(".json"):
            file_path = os.path.join(dataset_metadata_dir, filename)
            try:
                metadata = read_json(file_path)

                doi = request_zenodo_doi(metadata)

                # --- Updated filename logic here ---
                # dataset_X.json → table_X.json
                table_filename = filename.replace("dataset_", "table_")
                dataset_json_path = os.path.join(dataset_dir, table_filename)
                # -----------------------------------

                json_data = read_json(dataset_json_path)
                update_json_data = {
                    "pid": doi,
                    "pid_url": doi_base_url + doi,
                    **json_data,
                }
                save_json(dataset_json_path, update_json_data)

                updated_data = {
                    "pid": doi,
                    "pid_url": doi_base_url + doi,
                    **metadata,
                }
                save_json(file_path, updated_data)
                print("Updated with PID and PID URL")
            except Exception as e:
                print(f"Unexpected error processing {file_path}: {e}")
