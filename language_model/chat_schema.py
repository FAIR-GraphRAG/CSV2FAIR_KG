import os
import json
from langchain_core.documents import Document
from langchain.chains import LLMChain, RefineDocumentsChain
from langchain_core.prompts import PromptTemplate
from config.config import (
    DEPLOYMENT_NAME,
)
from langchain_core.output_parsers import JsonOutputParser
from typing import List
from pydantic import BaseModel, Field
from language_model.shared import postprocess, get_openai_llm, get_open_source_llm


class ObjectSchema(BaseModel):
    schema_: str = Field(..., alias="$schema")
    title: str
    description: str
    properties: List[str]

    class Config:
        populate_by_name = True


class DatasetSchema(BaseModel):
    schema_: str = Field(..., alias="$schema")
    title: str
    description: str
    properties: dict[str, ObjectSchema]

    class Config:
        populate_by_name = True


class FlexibleSchema(BaseModel):
    output_schema: DatasetSchema


def get_parser():
    return JsonOutputParser(pydantic_object=FlexibleSchema)


def get_initial_template():
    initial_template = """
    You are provided with the first two rows of a biomedical table and should generate a JSON dataset object.

    Generate a JSON object with the following structure:
    {initial_schema_wrapper}
    The list of objects contains the json object of the object of study (such as gene, cell) that is described in the biomedical table below.
    For the object of study, you create an object with the following structure:
    {initial_schema_object}

    Biomedical Table:
    {page_content}

    Here is an example of what is expected:
    {example_schema}

    Generate the JSON schema accordingly. Follow the instructions.\n{format_instructions}.
    **Output must be ONLY the final JSON, with no extra explanation.**

    """
    return initial_template


def get_refine_template():
    refine_template = """
    You are provided with an existing JSON schema and a new biomedical table.
    Existing JSON schema:
    {existing_schema}

    New Biomedical Table:
    {page_content}

    Try to identify the object of study (such as cell, gene) in the
    table above and if it already exists in the properties, add it's properties to the existing object. 
    If the object of study is not in the properties , create a new object with the following structure:
    {initial_schema_object}.
    Do not remove any existing keys. Ensure that the output remains valid JSON and follows 
    the same structure as before. Follow the instructions.\n{format_instructions}.
    **Output must be ONLY the final JSON, with no extra explanation.**

    """
    return refine_template


def create_schema(documents: List[Document]):
    
    if DEPLOYMENT_NAME == "Llama-3.3-70B-Instruct":
        llm = get_open_source_llm()
    else:
        llm = get_openai_llm()

    with open("data/schema/initial_schema.json", "r") as f:
        initial_schema = json.load(f)

    # Define the Initial Prompt
    initial_template = get_initial_template()

    parser = get_parser()

    initial_prompt = PromptTemplate(
        input_variables=["page_content"],
        template=initial_template,
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
            "initial_schema_object": json.dumps(
                initial_schema["initial_schema_object"]
            ),
            "initial_schema_wrapper": json.dumps(
                initial_schema["initial_schema_wrapper"]
            ),
            "example_schema": json.dumps(initial_schema["example_schema"]),
        },
    )
    initial_chain = LLMChain(llm=llm, prompt=initial_prompt)

    # Define the Refine Prompt
    refine_template = get_refine_template()
    refine_prompt = PromptTemplate(
        input_variables=["existing_schema", "page_content"],
        template=refine_template,
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
            "initial_schema_object": json.dumps(
                initial_schema["initial_schema_object"]
            ),
        },
    )
    refine_chain = LLMChain(llm=llm, prompt=refine_prompt)

    # Create the RefineDocumentsChain
    refine_documents_chain = RefineDocumentsChain(
        initial_llm_chain=initial_chain,
        refine_llm_chain=refine_chain,
        # Now we use "page_content" as the variable since each document has a "page_content" field.
        document_prompt=PromptTemplate(
            input_variables=["page_content"], template="{page_content}"
        ),
        document_variable_name="page_content",
        initial_response_name="existing_schema",
    )

    result = refine_documents_chain.invoke(documents)

    raw_output = result["output_text"]
    print("RAW", raw_output)
    json_text = postprocess(raw_output)
    try:
        refined_schema = json.loads(json_text)
        print("\nParsed JSON Schema:")
        if DEPLOYMENT_NAME == "Llama-3.3-70B-Instruct":
            return refined_schema
        else:
            print(json.dumps(refined_schema["output_schema"], indent=4))
            return refined_schema["output_schema"]
    except Exception as e:
        print("postprocessed json_text:", json_text)
        print("Error parsing JSON:", e)
