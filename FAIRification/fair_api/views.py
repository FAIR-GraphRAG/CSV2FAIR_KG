from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from utils.helper import read_json
import os

templates = Jinja2Templates(directory="templates")
path_metadata = "data/extracted_data/metadata/"
path_research_obj = "data/extracted_data/filled_schema/{filename}"


def find_matching_json_file(dataset_id: str):
    for i, filename in enumerate(sorted(os.listdir(path_metadata))):
        if filename.endswith(".json"):
            file_path = os.path.join(path_metadata, filename)
            try:
                metadata = read_json(file_path)
                if metadata["pid"] == dataset_id:
                    return filename
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")


async def dataset_landing(dataset_id: str):
    filename = find_matching_json_file(dataset_id)
    data = read_json(path_metadata + filename)
    return JSONResponse(content=data, media_type="application/json")


async def research_obj_landing(dataset_id: str, research_obj_id: str):
    filename = find_matching_json_file(dataset_id)
    metadata = read_json(path_metadata + filename)
    data = read_json(path_research_obj.format(filename=filename))
    # Check if research_obj_id exists in data
    item = [v for v in data["properties"].values() if v.get("pid") == research_obj_id]
    if item:
        modified_item = item[0]
        modified_item["properties"] = ""
        obj_metadata = {**modified_item, "dataset": metadata}
        return JSONResponse(content=obj_metadata, media_type="application/json")
