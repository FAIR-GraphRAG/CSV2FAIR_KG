import os
import json
from langchain_core.prompts import PromptTemplate
from config.config import AZURE_ENDPOINT, AZURE_OPENAI_API_KEY
from language_model.shared import get_openai_llm

# Set environment variables for Azure OpenAI
os.environ["AZURE_OPENAI_ENDPOINT"] = AZURE_ENDPOINT
os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY


def get_initial_template():
    initial_template = """
    You are provided with json containing keys and values.
    These are biomedical data with example values. Please identify the keys that have numeric values
    and are suitable for vectorization to find similarities between data.

    Data:
    {page_content}
    Please return a list containing only the keys that are numeric and suitable for vectorization.
    Example: ["key1", "key2"]
    """
    return initial_template


def identify_openai_keys(document):
    llm = get_openai_llm()

    initial_template = get_initial_template()

    initial_prompt = PromptTemplate(
        input_variables=["page_content"],
        template=initial_template,
    )

    chain = initial_prompt | llm

    try:
        result = chain.invoke({"page_content": document})
        return result.content
    except Exception as e:
        print("Error in chain: ", e)
