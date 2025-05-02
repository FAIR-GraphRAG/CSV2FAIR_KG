"""
Creates dummy DOIs via sandbox.zenodo for datasets
"""

import requests
import dotenv
import os
import json

dotenv.load_dotenv()

base_url = "https://sandbox.zenodo.org"
ACCESS_TOKEN = os.getenv("ZENODO_SANDBOX_TOKEN")


def request_zenodo_doi(metadata):
    data = {metadata: metadata}
    headers = {"Content-Type": "application/json"}
    params = {"access_token": ACCESS_TOKEN}
    r = requests.post(
        "{base_url}/api/deposit/depositions",
        params=params,
        data=json.dumps(data),
        headers=headers,
    )
    # print(r.json())
    assigned_doi = r.json()["prereserve_doi"]["doi"]
    print("\nDOI: ", assigned_doi)
    return assigned_doi
