import re
import glob
import json
from dotenv import load_dotenv
from neo4j import GraphDatabase
from config.config import NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD

load_dotenv()

driver = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


def flatten_dict2(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        if k == "relations":
            continue
        if parent_key == "properties":
            new_key = k
        else:
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def flatten_dict(d, parent_key="", sep="_"):
    items = []
    for k_space, v in d.items():
        k = k_space.replace(" ", "_")
        if k == "relations":
            continue
        if parent_key == "properties":
            new_key = k
        else:
            if parent_key:
                if k == "value":
                    new_key = parent_key
                else:
                    new_key = f"{parent_key}{sep}{k}"
            else:
                new_key = k

        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def sanitize_label(raw: str, default: str = "Research_Object") -> str:
    if not raw:
        return default
    label = re.sub(r"[^\w]", "_", raw.strip())
    if label[0].isdigit():
        label = f"_{label}"
    return label or default


def upsert_node(tx, label, props):
    pid = props.get("pid")
    if not pid:
        return

    # Merge only on the generic label and pid,
    # then attach the domain‑specific label in a separate SET.
    tx.run(
        f"""
        MERGE (n:FAIR_Digital_Object {{ pid: $pid }})
        ON  CREATE SET n += $props
        ON  MATCH  SET n += $props
        SET n:`{label}`
        """,
        pid=pid,
        props=props,
    )


def upsert_rel(tx, pid1, rel_type, sim, pid2):
    if not (pid1 and pid2 and rel_type):
        return
    tx.run(
        f"""
        MERGE (a:FAIR_Digital_Object {{ pid: $p1 }})
        MERGE (b:FAIR_Digital_Object {{ pid: $p2 }})
        MERGE (a)-[r:`{rel_type}`]->(b)
        SET  r.similarity = $sim
        """,
        p1=pid1,
        p2=pid2,
        sim=sim,
    )


def build_metadata_cache(metadata_glob):
    cache = {}
    for path in glob.glob(metadata_glob):
        with open(path, encoding="utf-8") as f:
            meta = json.load(f)
        pid = meta.get("pid")
        if pid:
            cache[pid] = flatten_dict(meta)
    return cache


def insert_data(json_glob, metadata_glob):
    meta_cache = build_metadata_cache(metadata_glob)
    with driver.session() as session:
        for path in glob.glob(json_glob):
            with open(path, encoding="utf-8") as f:
                doc = json.load(f)

            dataset_pid = doc.get("pid", "")
            dataset_flat = flatten_dict(
                {k: v for k, v in doc.items() if k != "properties"}
            )
            if dataset_pid in meta_cache:
                dataset_flat.update(meta_cache[dataset_pid])
            session.write_transaction(
                upsert_node,
                sanitize_label(doc.get("title", "Dataset")),
                dataset_flat,
            )

            for obj in doc.get("properties", {}).values():
                obj_pid = obj.get("pid")
                obj_label = sanitize_label(obj.get("title"))
                session.write_transaction(
                    upsert_node,
                    obj_label,
                    flatten_dict(obj),
                )

                for rel in obj.get("relations", []):
                    session.write_transaction(
                        upsert_rel,
                        rel.get("node1"),
                        rel.get("relation_label"),
                        rel.get("similarity", ""),
                        rel.get("node2"),
                    )

    driver.close()
