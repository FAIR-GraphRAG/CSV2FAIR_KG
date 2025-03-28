import os
import json
from langchain_core.documents import Document
from langchain.chains import LLMChain, RefineDocumentsChain
from langchain_core.prompts import PromptTemplate
from config.config import AZURE_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_API_VERSION
from langchain_core.output_parsers import JsonOutputParser
from typing import List
from pydantic import BaseModel, Field
from language_model.shared import postprocess, get_openai_llm

# Set environment variables for Azure OpenAI
os.environ["AZURE_OPENAI_ENDPOINT"] = AZURE_ENDPOINT
os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY


def get_initial_template():
    initial_template = """
    You are provided with the first two rows of a biomedical table and a set of predefined levels.
    Predefined levels: {levels}

    Generate a JSON schema such that for level 2, you create an object with the following structure:
    {initial_schema_study_object}
    The list of objects contains the json object of the object of study (such as gene, cell) that is described in the biomedical table below.
    For the object of study, you create an object with the following structure:
    {initial_schema}

    Biomedical Table:
    {page_content}

    Here is an example of what is expected:
    {example_schema}

    Generate the JSON schema accordingly. Follow the instructions.\n{format_instructions}.
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
    table above and if it already exists in the properties of level 2, add it's properties to the existing object. 
    If the object of study is not in the properties of level 2, create a new object with the following structure:
    {initial_schema}.
    Do not remove any existing keys. Ensure that the output remains valid JSON and follows 
    the same structure as before. Follow the instructions.\n{format_instructions}.
    """
    return refine_template


def get_parser():
    # Definition of data structures
    class ObjectSchema(BaseModel):
        # Use an alias for "$schema" since it's not a valid Python identifier
        schema_: str = Field(..., alias="$schema")
        title: str
        description: str
        properties: List[str]

        class Config:
            populate_by_name = True

    class LevelSchema(BaseModel):
        # Use an alias for "$schema" since it's not a valid Python identifier
        schema_: str = Field(..., alias="$schema")
        title: str
        description: str
        properties: dict[str, ObjectSchema]

        class Config:
            populate_by_name = True

    class FlexibleSchema(BaseModel):
        """
        This model can hold an arbitrary number of levels
        (e.g., 'level 1', 'level 2', 'level 3', ...), each
        of which is parsed into a `LevelSchema`.

        The __root__ field is a "catch-all" for keys at the top level.
        """

        output_schema: dict[str, LevelSchema]

    # Set up parser
    parser = JsonOutputParser(pydantic_object=FlexibleSchema)
    return parser


def create_openai_schema(documents: List[Document]):
    # Instantiate your LLM
    llm = get_openai_llm()

    # --- Load Predefined Levels ---
    with open("data/schema/levels.json", "r") as f:
        levels = json.load(f)

    # --- Load Initial Template ---
    with open("data/schema/initial_schema.json", "r") as f:
        initial_schema = json.load(f)

    # --- Define the Initial Prompt ---
    # This prompt generates the initial JSON schema from the first report.
    initial_template = get_initial_template()

    parser = get_parser()

    initial_prompt = PromptTemplate(
        input_variables=["page_content"],
        template=initial_template,
        partial_variables={
            "levels": json.dumps(levels),
            "format_instructions": parser.get_format_instructions(),
            "initial_schema": json.dumps(initial_schema["initial_schema"]),
            "initial_schema_study_object": json.dumps(
                initial_schema["initial_schema_study_object"]
            ),
            "example_schema": json.dumps(initial_schema["example_schema"]),
        },
    )
    initial_chain = LLMChain(llm=llm, prompt=initial_prompt)

    # --- Define the Refine Prompt ---
    # This prompt refines the existing JSON schema by adding new keys found in the report.
    refine_template = get_refine_template()
    refine_prompt = PromptTemplate(
        input_variables=["existing_schema", "page_content"],
        template=refine_template,
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
            "initial_schema": json.dumps(initial_schema["initial_schema"]),
        },
    )
    refine_chain = LLMChain(llm=llm, prompt=refine_prompt)

    # --- Create the RefineDocumentsChain ---
    refine_documents_chain = RefineDocumentsChain(
        initial_llm_chain=initial_chain,
        refine_llm_chain=refine_chain,
        # Now we use "page_content" as the variable since each Document has a "page_content" field.
        document_prompt=PromptTemplate(
            input_variables=["page_content"], template="{page_content}"
        ),
        document_variable_name="page_content",
        initial_response_name="existing_schema",
    )

    # --- Run the Chain ---
    result = refine_documents_chain.invoke(documents)

    raw_output = result["output_text"]

    json_text = postprocess(raw_output)

    # Optionally, verify that the output is valid JSON
    try:
        refined_schema = json.loads(json_text)
        print("\nParsed JSON Schema:")
        print(json.dumps(refined_schema["output_schema"], indent=4))
        return refined_schema["output_schema"]
    except Exception as e:
        print("postprocessed json_text:", json_text)
        print("Error parsing JSON:", e)
