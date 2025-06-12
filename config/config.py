import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")

AZURE_OPEN_SOURCE_KEY = os.getenv("AZURE_OPEN_SOURCE_KEY")
AZURE_OPEN_SOURCE_ENDPOINT = os.getenv("AZURE_OPEN_SOURCE_ENDPOINT")
AZURE_OPEN_SOURCE_DEPLOYMENT_NAME = os.getenv("OPEN_SOURCE_DEPLOYMENT_NAME")

UMLS_API_KEY = os.getenv("UMLS_API_KEY")
UMLS_USERNAME = os.getenv("UMLS_USERNAME")
UMLS_LICENSE_CODE = os.getenv("UMLS_LICENSE_CODE")

# Threshold for cosine similarity (relation extraction)
SIMILARITY_THRESHOLD_INNER = 0.5
SIMILARITY_THRESHOLD_CROSS = 0.2

# Num of test documents schema
NUM_TEST_DOCUMENTS = 3

# available models OpenAI: gpt-4o-mini, gpt-4
# available models open source: llama3.2:3b, deepseek-r1:7b, deepseek-r1:70b, llama3.3:70b
# gpt-4o-mini, gpt-4, Llama-3.3-70B-Instruct
DEPLOYMENT_NAME = "gpt-4o-mini"

BIOONTOLOGY_API_KEY = os.getenv("API_KEY_BIOONTOLOGY")
BIOONTOLOGY_API_URL = "https://data.bioontology.org"

NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_INSTANCE = os.getenv("NEO4J_INSTANCE")
NEO4J_URL = os.getenv("NEO4J_URL")

ENTITY_CLASS_LIST = ["pathway", "GO-BP"]
