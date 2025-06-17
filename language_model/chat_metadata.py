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
    You are given a document with metadata. Extract structured metadata as a **single valid JSON object**.

    Respond with only one of the following:

    Example for dataset:
    {{
    "dataset": {{
        "identifier": "GSE123456",
        "title": "...",
        ...
    }}
    }}

    Example for sample:
    {{
    "samples": {{
        "identifier": "GSM123456",
        "title": "...",
        ...
    }}
    }}

    Only return JSON. No comments, no explanation.

    Document:
    {page_content}
    """
    return initial_template


def get_parser():
    class DictSchema(BaseModel):
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
        input_variables=["page_content"],
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
