import os
from dotenv import load_dotenv

load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")

AZURE_OPEN_SOURCE_KEY = os.getenv("AZURE_OPEN_SOURCE_KEY")
AZURE_OPEN_SOURCE_ENDPOINT = os.getenv("AZURE_OPEN_SOURCE_ENDPOINT")
AZURE_OPEN_SOURCE_DEPLOYMENT_NAME = os.getenv("OPEN_SOURCE_DEPLOYMENT_NAME")

# Models: GPT-4o-mini, Llama-3.3-70B-Instruct
DEPLOYMENT_NAME = "gpt-4o-mini"

BIOONTOLOGY_API_KEY = os.getenv("API_KEY_BIOONTOLOGY")
BIOONTOLOGY_API_URL = "https://data.bioontology.org"

NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_INSTANCE = os.getenv("NEO4J_INSTANCE")

# FAIR=True or Non-FAIR=False
FAIR_GRAPH = True

if FAIR_GRAPH:
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD_FAIR")
    NEO4J_URL = os.getenv("NEO4J_URL_FAIR")
else:
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD_NON-FAIR")
    NEO4J_URL = os.getenv("NEO4J_URL_NON-FAIR")

# User-defined entities
ENTITY_CLASS_LIST = ["pathway", "GO-BP"]
