import os
import json
from langchain_core.prompts import PromptTemplate
from config.config import AZURE_ENDPOINT, AZURE_OPENAI_API_KEY, DEPLOYMENT_NAME
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from language_model.shared import get_openai_llm, get_open_source_llm
from utils.helper import read_json
from typing import Optional

# Set environment variables for Azure OpenAI
os.environ["AZURE_OPENAI_ENDPOINT"] = AZURE_ENDPOINT
os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY


def get_initial_template():
    initial_template = """
    You are provided with a document and a json schema.

    Please fill the json schema with the information from the document.
    Document:
    {page_content}
    JSON Schema:
    {schema}
    Please ensure that the JSON schema is valid and follows the structure provided in the document.
    """
    return initial_template


def get_parser():
    class DictSchema(BaseModel):
        identifier: str
        contributor: Optional[str] = None
        coverage: Optional[str] = None
        creator: Optional[str] = None
        date: Optional[str] = None
        description: Optional[str] = None
        format: Optional[str] = None
        language: Optional[str] = None
        publisher: Optional[str] = None
        relation: Optional[str] = None
        rights: Optional[str] = None
        source: Optional[str] = None
        subject: Optional[str] = None
        title: Optional[str] = None
        type: Optional[str] = None

    parser = JsonOutputParser(pydantic_object=DictSchema)
    return parser


def extract_openai_metadata(document):
    if DEPLOYMENT_NAME == "Llama-3.3-70B-Instruct":
        llm = get_open_source_llm()
    else:
        llm = get_openai_llm()

    initial_template = get_initial_template()

    initial_prompt = PromptTemplate(
        input_variables=["page_content", "schema"],
        template=initial_template,
    )

    schema = read_json("data/schema/component-level_metadata.json")

    parser = get_parser()

    chain = initial_prompt | llm | parser

    try:
        result = chain.invoke({"page_content": document, "schema": schema})
        print("\nParsed JSON Schema:")
        print(json.dumps(result, indent=4))
        return result
    except Exception as e:
        print("Error parsing JSON:", e)
