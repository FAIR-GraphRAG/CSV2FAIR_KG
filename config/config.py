import os
from dotenv import load_dotenv

load_dotenv()

DEPLOYMENT = os.getenv("DEPLOYMENT")
OLLAMA_URL = os.getenv("OLLAMA_URL")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
NUM_TEST_DOCUMENTS = int(os.getenv("NUM_TEST_DOCUMENTS"))
