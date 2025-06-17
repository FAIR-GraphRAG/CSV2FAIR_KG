import re
import glob
import json
from dotenv import load_dotenv
from neo4j import GraphDatabase
from config.config import NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD

load_dotenv()


driver = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


def normalize_properties(props):
    """
    If properties is a list of dicts, turn it into a dict.
    If it's already a dict, return as is.
    """
    if isinstance(props, list):
        norm = {}
        for d in props:
            if isinstance(d, dict):
                norm.update(d)
        return norm
    elif isinstance(props, dict):
        return props
    return {}


def flatten_dict(d, parent_key="", sep="_"):
    """
    Flatten a nested dictionary. If value is a dict, recurse.
    If value is primitive, keep as is.
    """
    items = []
    for k_space, v in d.items():
        k = k_space.replace(" ", "_")
        if k == "relations":
            continue

        # Keep top-level property keys as they are
        new_key = k if not parent_key else f"{parent_key}{sep}{k}"

        if isinstance(v, dict):
            # If the value is a flat dict (e.g., {"gene": "TSPAN6"}), flatten all pairs
            if all(
                isinstance(inner_v, (str, int, float, bool, type(None)))
                for inner_v in v.values()
            ):
                for inner_k, inner_v in v.items():
                    compound_key = f"{new_key}{sep}{inner_k}"
                    items.append((compound_key, inner_v))
            # If it's a { "value": ... } only, just take the value
            elif set(v.keys()) == {"value"}:
                items.append((new_key, v["value"]))
            else:
                items.extend(flatten_dict(v, new_key, sep).items())
        elif isinstance(v, (str, int, float, bool)) or v is None:
            items.append((new_key, v))
        else:
            # If v is something Neo4j won't accept (like a list of dicts), convert to string
            items.append((new_key, str(v)))
    return dict(items)


def sanitize_label(raw: str, default: str = "Research_Object") -> str:
    if not raw:
        return default
    label = re.sub(r"[^\w]", "_", raw.strip())
    if label[0].isdigit():
        label = f"_{label}"
    return label or default


def upsert_node(tx, label, node_key, props):
    if not node_key:
        return

    tx.run(
        f"""
        MERGE (n:Object {{ node_key: $node_key }})
        ON CREATE SET n += $props
        ON MATCH  SET n += $props
        SET n:`{label}`
        """,
        node_key=node_key,
        props={**props, "node_key": node_key},
    )


def upsert_rel(tx, node1, rel_type, sim, node2):
    if not (node1 and node2 and rel_type):
        return
    tx.run(
        f"""
        MERGE (a:Object {{ node_key: $p1 }})
        MERGE (b:Object {{ node_key: $p2 }})
        MERGE (a)-[r:`{rel_type}`]->(b)
        SET r.similarity = $sim
        """,
        p1=node1,
        p2=node2,
        sim=sim,
    )


def build_metadata_cache(metadata_glob):
    cache = {}
    for path in glob.glob(metadata_glob):
        with open(path, encoding="utf-8") as f:
            meta = json.load(f)
        doc_key = meta.get("title") or path
        cache[doc_key] = flatten_dict(meta)
    return cache


def non_fair_insert_data(json_glob, metadata_glob):
    meta_cache = build_metadata_cache(metadata_glob)
    with driver.session() as session:
        for path in glob.glob(json_glob):
            with open(path, encoding="utf-8") as f:
                doc = json.load(f)

            doc_key = doc.get("title", path)
            doc_flat = flatten_dict({k: v for k, v in doc.items() if k != "properties"})

            if doc_key in meta_cache:
                doc_flat.update(meta_cache[doc_key])

            # Insert dataset root node using doc_key
            session.write_transaction(
                upsert_node,
                sanitize_label(doc.get("title", "Dataset")),
                doc_key,
                doc_flat,
            )

            for obj_key, obj in doc.get("properties", {}).items():
                # Flatten top-level fields (excluding 'properties')
                obj_top_flat = flatten_dict(
                    {k: v for k, v in obj.items() if k != "properties"}
                )
                # Flatten normalized 'properties', if present
                prop_flat = {}
                if "properties" in obj:
                    norm_props = normalize_properties(obj["properties"])
                    prop_flat = flatten_dict(norm_props)
                # Merge so property keys (e.g. "gene") are at top level
                full_obj_flat = {**obj_top_flat, **prop_flat}
                obj_label = sanitize_label(obj.get("title", obj_key))

                # Insert property node using key (e.g., gene_0)
                session.write_transaction(
                    upsert_node,
                    obj_label,
                    obj_key,
                    full_obj_flat,
                )

                # Add internal semantic relations (if any)
                for rel in obj.get("relations", []):
                    session.write_transaction(
                        upsert_rel,
                        rel.get("node1"),
                        rel.get("relation_label"),
                        rel.get("similarity", ""),
                        rel.get("node2"),
                    )

                # Connect this entity to the dataset node
                session.write_transaction(
                    upsert_rel,
                    obj_key,
                    "belongs_to",
                    "",
                    doc_key,
                )

    driver.close()
