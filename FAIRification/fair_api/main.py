from fastapi import FastAPI, Request
from FAIRification.fair_api.views import dataset_landing, research_obj_landing

app = FastAPI()


@app.get("/")
async def dataset_page():
    return "Hello, World!"


@app.get("/{namespace}/{dataset_id}")
async def dataset_page(namespace: str, dataset_id: str):
    full_id = f"{namespace}/{dataset_id}"
    return await dataset_landing(full_id)


@app.get("/{namespace}/{dataset_id}/{research_obj_id}")
async def research_obj_page(
    request: Request, namespace: str, dataset_id: str, research_obj_id: str
):
    full_id = f"{namespace}/{dataset_id}"
    return await research_obj_landing(full_id, research_obj_id, request)
