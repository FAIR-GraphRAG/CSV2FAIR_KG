from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from utils.helper import read_json

templates = Jinja2Templates(directory="templates")
path_metadata = "data/extracted_data/metadata/"
path_research_obj = "data/extracted_data/filled_schema/{dataset_id}"


async def dataset_landing(dataset_id: str):
    data = read_json(path_metadata + dataset_id)
    return JSONResponse(content=data, media_type="application/json")


async def research_obj_landing(dataset_id: str, research_obj_id: str):
    metadata = read_json(path_metadata + dataset_id)
    data = read_json(path_research_obj.format(dataset_id=dataset_id))
    # Check if research_obj_id exists in data
    item = [
        v
        for v in data["level_1"]["properties"].values()
        if v.get("pid") == research_obj_id
    ]
    modified_item = item[0]
    modified_item["properties"] = ""
    obj_metadata = {**modified_item, "dataset": metadata}

    if item:
        return JSONResponse(content=obj_metadata, media_type="application/json")
