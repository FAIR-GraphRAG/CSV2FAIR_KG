"""
See Cool URIs for KGs.
example: https:// purl. example.com /a9/ e42 (Scheme, Subdomain, Domain, Context, Accession identifier)
This module create PIDs for research objects/components
"""

import random
import string
import json
import os
import shortuuid

base_URI = "https://fair-graph.org/"
folder_path = "data/extracted_data/filled_schema"


def generate_random_sequence(k_num):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=k_num))


def get_uri(section_key, doc_num):
    return f"{base_URI}{section_key.replace(' ', '_')}/r{doc_num}/{generate_random_sequence(3)}"


def get_pid_urn(dataset_id, title):
    pid = shortuuid.uuid()
    return pid, f"urn:{title.lower()}:{dataset_id}/{pid}"


def add_pid_to_json(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return
    for i, filename in enumerate(sorted(os.listdir(folder_path))):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                if isinstance(data, dict):
                    for (
                        subkey,
                        subvalue,
                    ) in data.items():  # $schema, title, properties
                        if subkey == "properties":
                            for prop_key, prop_value in subvalue.items():
                                new_pid, new_urn = get_pid_urn(
                                    filename.split(".")[0], prop_value["title"]
                                )
                                print(new_urn)
                                new_value = {
                                    "pid": new_pid,
                                    "urn": new_urn,
                                    **prop_value,
                                }
                                data[subkey][prop_key] = new_value

                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)

                print(f"Updated: {file_path}")

            except Exception as e:
                print(f"Unexpected error processing {file_path}: {e}")


if __name__ == "__main__":
    add_pid_to_json(folder_path)
