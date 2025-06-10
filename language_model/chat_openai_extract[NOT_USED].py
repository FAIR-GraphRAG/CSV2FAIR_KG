import os
import json
from langchain_core.prompts import PromptTemplate
from config.config import AZURE_ENDPOINT, AZURE_OPENAI_API_KEY, DEPLOYMENT_NAME
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from language_model.shared import get_openai_llm, get_open_source_llm
from utils.helper import read_json

# Set environment variables for Azure OpenAI
os.environ["AZURE_OPENAI_ENDPOINT"] = AZURE_ENDPOINT
os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY


def get_initial_template():
    initial_template = """
    You are provided with a table and a json schema.

    Please select from the properties of the "Study Object" in the json schema {schema} which study object
    the table belongs to. The table contains information about a medical report.
    Please return a json object with the following structure: {{"table": "study_object_name"}}.
    The study object name should be the one you selected from the json schema.
    Do not return any additional text or information.

    Table:
    {page_content}

    """
    return initial_template


def get_parser():
    class DictSchema(BaseModel):
        table: str

    parser = JsonOutputParser(pydantic_object=DictSchema)
    return parser


def extract_openai_entities(documents):
    if DEPLOYMENT_NAME == "Llama-3.3-70B-Instruct":
        llm = get_open_source_llm()
    else:
        llm = get_openai_llm()
    initial_template = get_initial_template()

    initial_prompt = PromptTemplate(
        input_variables=["page_content", "schema"],
        template=initial_template,
    )

    schema = read_json("data/schema/schema.json")

    parser = get_parser()

    chain = initial_prompt | llm | parser

    table_semantics = []
    for i, doc in enumerate(documents):
        try:
            result = chain.invoke({"page_content": doc.page_content, "schema": schema})
            print("\nParsed JSON Schema:")
            print(json.dumps(result, indent=4))
            table_semantics.append(result)
        except Exception as e:
            print("Error parsing JSON:", e)
            continue
    return table_semantics
