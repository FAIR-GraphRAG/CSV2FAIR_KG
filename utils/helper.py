import json


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)  # data will be a Python dict
    return data


def save_json(file_path, json_data):
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)
    print(f"\nJSON saved to {file_path}")
