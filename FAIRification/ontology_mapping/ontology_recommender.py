"""
Recommends biomedical ontologies based on input.

"""

import json
import csv
import urllib.request
import urllib.parse
from dotenv import load_dotenv
from re import finditer
from .helper import get_meaningful_term
from utils.helper import extract_schema_keywords, read_json
from config.config import BIOONTOLOGY_API_KEY, BIOONTOLOGY_API_URL

load_dotenv()
API_KEY = BIOONTOLOGY_API_KEY
REST_URL = BIOONTOLOGY_API_URL


def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [("Authorization", "apikey token=" + API_KEY)]
    response = opener.open(url)
    data = json.loads(response.read().decode("utf-8"))
    return data


def extract_ontology_acronym(ontology_url):
    return ontology_url.rstrip("/").split("/")[-1]


def call_bioontology(encoded_key):
    url = f"{REST_URL}/search?q={encoded_key}&require_exact_match=true"
    results = []
    try:
        results = get_json(url).get("collection", [])
    except Exception as e:
        print(f"Error retrieving data {e}")
    return results


def camel_case_split(identifier):
    """
    Splits an identifier into its camel case (and numeric) parts.
    Examples: splitting "resultId" into ["result", "Id"], also handles
    "Data.her2Chr17Ratio", "Her2Signals" and "Chr17Signals".
    """
    segments = []
    # Split by dot first; dots are used as delimiters.
    for part in identifier.split("."):
        pattern = (
            r".+?(?:(?<=[a-z])(?=[A-Z])|"  # lowercase letter followed by uppercase
            r"(?<=[A-Z])(?=[A-Z][a-z])|"  # uppercase followed by uppercase then lowercase
            r"(?<=\d)(?=[A-Za-z])|"  # digit followed by a letter
            r"$)"  # or end of string
        )
        matches = finditer(pattern, part)
        segments.extend(m.group(0) for m in matches)
    return segments


def write_header(writer):
    """
    Writes the header to the CSV file.
    """
    writer.writerow(
        [
            "OriginalJsonKey",
            "NewJsonKey",
            "PrefLabel",
            "ExactMatch",
            "Ontology",
            "OntologyLink",
        ]
    )


def write_key_results(results, key, old_key, exact_match, writer):

    for r in results:
        pref_label = r.get("prefLabel", "")
        ontology_term_link = r.get("links", {}).get("self", "")
        ontology_link = r.get("links", {}).get("ontology", "")
        if ontology_link:
            ontology_acronym = extract_ontology_acronym(ontology_link)
        else:
            ontology_acronym = ""

        writer.writerow(
            [
                old_key,
                key,
                pref_label,
                exact_match,
                ontology_acronym,
                ontology_term_link,
            ]
        )


def write_no_match(key, writer):
    writer.writerow([key, "", "", "", "", ""])
    writer.writerow([])


def recommend_ontologies(input_json, output_csv):

    data = read_json(input_json)

    keys = extract_schema_keywords(data)
    print(f"Found {len(keys)} unique keys in 'properties' from {input_json}.")

    with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        write_header(writer)

        for raw_key in keys:
            exact_match = True
            old_key = raw_key
            if not raw_key.strip():
                continue
            key = " ".join(camel_case_split(raw_key))
            encoded_key = urllib.parse.quote(key)
            results = call_bioontology(encoded_key)

            # Handle terms without match
            if not results:
                new_key = get_meaningful_term(key)
                exact_match = False
                print(f"NO MATCH: {key}. New key: {new_key}")
                key = new_key
                encoded_key = urllib.parse.quote(key)
                results = call_bioontology(encoded_key)
            if results:
                write_key_results(results, key, old_key, exact_match, writer)
            else:
                write_no_match(key, writer)

    print(f"Done! Mappings written to {output_csv}")
