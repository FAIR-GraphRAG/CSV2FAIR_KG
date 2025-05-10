import os
import itertools
from typing import Dict, List, Tuple

from utils.helper import read_json, save_json, extract_list
from language_model.chat_client_factory import client_selector

JSON_DIR = "data/extracted_data/filled_schema"


def get_key_values(data):
    # Get the keys and values from the first research study object
    if not data or "properties" not in data or not data["properties"]:
        return {}

    # Grab the *first* study object (ordering in Py ≥3.7 is guaranteed)
    first_section = next(iter(data["properties"].values()), {})
    nested_props = first_section.get("properties", {})

    # Flatten to {key: value}
    return {
        prop_key: prop_dict.get("value")
        for prop_key, prop_dict in nested_props.items()
        if isinstance(prop_dict, dict) and "value" in prop_dict
    }


def create_vectors(data, relevant_keys):
    vectors: Dict[str, List[str]] = {}

    for section in data.get("properties", {}).values():
        pid = section.get("pid")
        if pid is None:
            # Skip malformed sections – no PID ⇒ cannot be referenced later
            continue

        section_props = section.get("properties", {})
        vector = [
            section_props.get(k, {}).get("value")  # value if present
            for k in relevant_keys
        ]
        vectors[pid] = vector

    return vectors


# --------------------------------------------------------------------------- #
#  Fast bucket‑based similarity (same as last version, but new output format) #
# --------------------------------------------------------------------------- #
def compare_vectors(
    filename: str,
    vectors: Dict[str, List[str]],
    similarity_threshold: float = 0.8,
) -> Dict[str, List[str]]:
    """
    Very fast relation finder that stores results like

        "relations": [
            {
              "node1": "<pid_i>",
              "relation_label": "similar_values",
              "similarity": "1.00",
              "node2": "<pid_j>"
            },
            ...
        ]

    Two *directed* objects are written ( i→j and j→i ) so look‑ups stay simple.
    """
    file_path = os.path.join(JSON_DIR, filename)
    data = read_json(file_path)
    properties = data.get("properties", {})

    # ---------- 1.  build aligned lists ---------------------------------- #
    prop_keys: List[str] = list(properties.keys())  # order is preserved
    pid_list: List[str] = []  # idx → pid
    vec_list: List[Tuple] = []  # idx → tuple(vector)

    for k in prop_keys:
        pid = properties[k].get("pid")
        if pid not in vectors:
            continue
        pid_list.append(pid)
        vec_list.append(tuple(vectors[pid]))  # tuple = hashable

    if not pid_list:  # nothing to do
        return {}

    n_features = len(vec_list[0])
    min_matches = max(1, int((similarity_threshold * n_features) + 0.9999))

    # ---------- 2.  bucket rows by the min‑match fields ------------------- #
    # For threshold 0.8 and three features this == the full tuple.
    buckets: Dict[Tuple, List[int]] = {}
    for idx, vec in enumerate(vec_list):
        key = vec[:min_matches] if min_matches < n_features else vec
        buckets.setdefault(key, []).append(idx)

    # ---------- 3.  compare only inside buckets --------------------------- #
    relations_written: Dict[str, List[str]] = {}

    for bucket_idxs in buckets.values():
        if len(bucket_idxs) < 2:
            continue

        for i, j in itertools.combinations(bucket_idxs, 2):
            vec_i, vec_j = vec_list[i], vec_list[j]

            matches = sum(1 for x, y in zip(vec_i, vec_j) if x == y)
            similarity = matches / n_features
            if similarity < similarity_threshold:
                continue

            pid_i, pid_j = pid_list[i], pid_list[j]
            _write_relation(properties[prop_keys[i]], pid_i, pid_j, similarity)
            _write_relation(properties[prop_keys[j]], pid_j, pid_i, similarity)

            relations_written.setdefault(pid_i, []).append(pid_j)
            relations_written.setdefault(pid_j, []).append(pid_i)

    save_json(file_path, data)
    return relations_written


# --------------------------------------------------------------------------- #
#  Helper: append one directed relation object to a section                   #
# --------------------------------------------------------------------------- #
def _write_relation(section: dict, node1: str, node2: str, sim: float) -> None:
    rel_obj = {
        "node1": node1,
        "relation_label": "similar_values",
        "similarity": f"{sim:.2f}",
        "node2": node2,
    }
    section.setdefault("relations", []).append(rel_obj)


def find_relations():
    """
    For each file in json_folder:
      1) Load the data as json
      2) Paste the properties to LLM and get the relevant ones for similarity back
      3) Use pid and relevant properties
      4) For the relevant properties, create a vector
      5) Compare the vectors for each pair of entries
      6) Save similar vectors with their pid in this format:
         - <pid_of_section_i, belongs_to_same_doc_as, pid_of_section_j>
         - <pid_of_section_j, belongs_to_same_doc_as, pid_of_section_i>

    """
    for filename in os.listdir(JSON_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(JSON_DIR, filename)
            data = read_json(file_path)
            key_values = get_key_values(data)
            relevant_keys = client_selector("inner_doc_relations", key_values)
            processed_keys = extract_list(relevant_keys)

            vectors = create_vectors(data, processed_keys)
            relations = compare_vectors(filename, vectors)
            print(f"Relations written for {filename}: {relations}")
