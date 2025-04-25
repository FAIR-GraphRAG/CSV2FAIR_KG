from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from utils.helper import read_json

templates = Jinja2Templates(directory="templates")
path_metadata = "data/extracted_data/metadata/"


async def dataset_landing(dataset_id: str, request: Request):
    data = read_json(path_metadata + dataset_id)
    return JSONResponse(content=data, media_type="application/json")
