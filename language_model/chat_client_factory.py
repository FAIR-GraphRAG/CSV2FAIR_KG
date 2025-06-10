from language_model.chat_openai_schema import create_openai_schema
from language_model.chat_openai_metadata import extract_openai_metadata
from config.config import DEPLOYMENT_NAME


def client_selector(task_name, documents):
    print("DEPLOYMENT: ", DEPLOYMENT_NAME)

    if task_name == "schema_construction":
        try:
            response = create_openai_schema(documents)
        except Exception as e:
            response = str(e)
    elif task_name == "metadata_extraction":
        try:
            response = extract_openai_metadata(documents)
        except Exception as e:
            print(e)
    else:
        print(f'Task name "{task_name}" not found.')
        return None
    return response
