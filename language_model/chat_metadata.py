import os
import json
from langchain_core.prompts import PromptTemplate
from config.config import DEPLOYMENT_NAME
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from language_model.shared import get_openai_llm, get_open_source_llm
from typing import Optional


def get_initial_template():
    initial_template = """
    You get a metadata file and you have to decide if it is metadata for my samples or for my whole dataset/series.

    - If the metadata contains information on one or multiple samples in more detail, create an object with the key "sample" and include each key just once with one corresponding value
    - If the metadata describes the dataset, create an object with the key "dataset" and include each key just once with one corresponding value

    Document:
    {page_content}

    Ensure that the resulting JSON schema is valid and adheres to the structure outlined in the document.
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


def extract_metadata(document):
    if DEPLOYMENT_NAME == "Llama-3.3-70B-Instruct":
        llm = get_open_source_llm()
    else:
        llm = get_openai_llm()

    initial_template = get_initial_template()

    initial_prompt = PromptTemplate(
        input_variables=["page_content", "schema_dublin_core", "schema"],
        template=initial_template,
    )

    parser = get_parser()

    chain = initial_prompt | llm | parser

    try:
        result = chain.invoke(
            {
                "page_content": document,
            }
        )
        print("\nParsed JSON Schema:")
        print(json.dumps(result, indent=4))
        return result
    except Exception as e:
        print("Error parsing JSON:", e)
