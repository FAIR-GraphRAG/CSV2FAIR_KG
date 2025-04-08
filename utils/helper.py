import json
from langchain_community.document_loaders.csv_loader import CSVLoader
import os


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)  # data will be a Python dict
    return data


def save_json(file_path, json_data):
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)
    print(f"\nJSON saved to {file_path}")


def load_docs(report_folder, cut_file=True):
    documents = []
    for filename in os.listdir(report_folder):

        if filename.endswith(".csv"):
            file_path = os.path.join(report_folder, filename)
            loader = CSVLoader(file_path=file_path)
            data = loader.load()
            if data:  # Make sure there's at least one row
                if cut_file:
                    documents.append(data[0])  # Append the header + first row
                else:
                    documents.append(data)  # Append all rows
        elif filename.endswith("_GSE.soft"):  # GEO soft file
            file_path = os.path.join(report_folder, filename)
            with open(file_path, "r") as file:
                lines = file.readlines()
                if lines:  # Ensure the file isn’t empty
                    documents.append(lines)
    return documents


def find_docs_in_folder(csv_dir, data_dir, cut_file=True):
    """
    For each csv_dir in data_dir call load_doc function
    return list of Documents: [Document, Document]
    """
    documents = []
    for current_root, dirs, files in os.walk(data_dir):
        for dir_name in dirs:
            if dir_name == csv_dir:
                csv_data_path = os.path.join(current_root, dir_name)
                documents.extend(load_docs(csv_data_path, cut_file=cut_file))
    return documents
