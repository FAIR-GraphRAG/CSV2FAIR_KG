# Install the following dependencies: azure.identity and azure-ai-inference
from config.config import (
    AZURE_OPEN_SOURCE_ENDPOINT,
    AZURE_OPEN_SOURCE_KEY,
    AZURE_OPEN_SOURCE_DEPLOYMENT_NAME,
)

from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_core.messages import HumanMessage, SystemMessage


def run_open_source():
    model = AzureAIChatCompletionsModel(
        endpoint=AZURE_OPEN_SOURCE_ENDPOINT,
        credential=AZURE_OPEN_SOURCE_KEY,  # if using Entra ID you can should use DefaultAzureCredential() instead
        model=AZURE_OPEN_SOURCE_DEPLOYMENT_NAME,
        max_tokens=1024,
    )

    messages = [
        SystemMessage(content="You are an assistant. Answer the question."),
        HumanMessage(content="Who was Albert Einstein?"),
    ]

    res = model.invoke(messages)
    print(res.content)
