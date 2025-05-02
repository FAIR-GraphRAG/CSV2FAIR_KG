base_url = "https://sandbox.zenodo.org"

import requests
import dotenv
import os
import json

dotenv.load_dotenv()
ACCESS_TOKEN = os.getenv("ZENODO_SANDBOX_TOKEN")

data = {
    "metadata": {
        "title": "My first upload",
        "upload_type": "poster",
        "description": "This is my first upload",
        "creators": [{"name": "Doe, John", "affiliation": "Zenodo"}],
    }
}

headers = {"Content-Type": "application/json"}
params = {"access_token": ACCESS_TOKEN}
r = requests.post(
    "https://sandbox.zenodo.org/api/deposit/depositions",
    params=params,
    data=json.dumps(data),
    headers=headers,
)
r.status_code
# 201
print(r.json())
print("\nDOI", r.json()["prereserve_doi"]["doi"])
