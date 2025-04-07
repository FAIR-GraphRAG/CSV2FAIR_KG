from language_model.chat_openai_schema import create_openai_schema
from language_model.chat_openai_extract import extract_openai_entities
from config.config import DEPLOYMENT


def client_selector(task_name, documents):
    print("DEPLOYMENT: ", DEPLOYMENT)

    open_source_models = [
        "llama3.2:3b",
        "deepseek-r1:7b",
        "deepseek-r1:70b",
        "llama3.3:70b",
    ]

    openai_models = ["gpt-4o-mini", "gpt-4"]

    if task_name == "schema_construction":
        if DEPLOYMENT in openai_models:
            try:
                response = create_openai_schema(documents)
            except Exception as e:
                response = str(e)
        elif DEPLOYMENT in open_source_models:
            # DUMMY
            response = str(e)
        else:
            response = "Model not found"
    elif task_name == "entity_extraction":
        if DEPLOYMENT in openai_models:
            try:
                response = extract_openai_entities(documents)
            except Exception as e:
                print(e)
        elif DEPLOYMENT in open_source_models:
            # DUMMY
            response = str(e)
    return response
