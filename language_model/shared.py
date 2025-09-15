import re
from langchain_openai import AzureChatOpenAI
from config.config import (
    AZURE_API_VERSION,
    AZURE_OPEN_SOURCE_ENDPOINT,
    AZURE_OPEN_SOURCE_KEY,
    DEPLOYMENT_NAME,
    AZURE_ENDPOINT,
)
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel


def get_openai_llm():
    llm = AzureChatOpenAI(
        azure_deployment=DEPLOYMENT_NAME,
        azure_endpoint=AZURE_ENDPOINT,
        api_version=AZURE_API_VERSION,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return llm


def get_open_source_llm():
    llm = AzureAIChatCompletionsModel(
        endpoint=AZURE_OPEN_SOURCE_ENDPOINT,
        credential=AZURE_OPEN_SOURCE_KEY,
        model=DEPLOYMENT_NAME,
        max_tokens=1024,
        temperature=0.0,
        streaming=False,
    )
    return llm


def postprocess(raw_output):
    # Extract text between curly braces if extra text is present
    json_match = re.search(r"\{.*\}", raw_output, re.DOTALL)
    json_text = json_match.group(0) if json_match else raw_output
    return json_text
