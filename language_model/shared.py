import glob
import os
import re
from langchain_openai import AzureChatOpenAI
from config.config import AZURE_API_VERSION

azure_deployment = "gpt-4o-mini"


def get_openai_llm():
    # Instantiate your LLM
    llm = AzureChatOpenAI(
        azure_deployment=azure_deployment,
        api_version=AZURE_API_VERSION,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return llm


def postprocess(raw_output):
    # Extract text between curly braces if extra text is present
    json_match = re.search(r"\{.*\}", raw_output, re.DOTALL)
    json_text = json_match.group(0) if json_match else raw_output
    return json_text
