from fastapi import FastAPI, Request
from FAIRification.fair_api.views import dataset_landing

app = FastAPI()


@app.get("/")
async def dataset_page():
    return "Hello, World!"


@app.get("/ds/{dataset_id}")
async def dataset_page(dataset_id: str, request: Request):
    return await dataset_landing(dataset_id, request)
