import csv
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()


def read_csv_groups(input_csv):
    """
    Splits rows into groups, one group for each JSON key.
    An empty row marks the end of a group.
    Returns a list of groups.
    """
    groups = []
    with open(input_csv, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader, None)
        # If header exists but does not start with "OriginalJsonKey", assume no header
        if header and header[0].strip().lower() != "OriginalJsonKey":
            infile.seek(0)
            reader = csv.reader(infile)

        current_group = []
        for row in reader:
            # Check if row is empty
            if not any(cell.strip() for cell in row):
                if current_group:
                    groups.append(current_group)
                    current_group = []
            else:
                current_group.append(row)
        if current_group:
            groups.append(current_group)
    return groups


def collect_group_candidates(rows):
    """
    Processes a group and returns a dictionary of the form:
      {
          json_key: {
              "old_json_key": <old_json_key>,
              "ontologies": {
                  <ontology_name>: (candidate_term, ontology_link),
                  ...
              }
          },
          ...
      }

    """
    candidates = {}
    for row in rows:
        if len(row) < 6:
            continue

        old_json_key = row[0].strip()
        json_key = row[1].strip()
        candidate_term = row[2].strip()
        ontology = row[4].strip()
        ontology_link = row[5].strip()

        # Only keep exact matches
        if json_key.lower() != candidate_term.lower():
            continue
        if not json_key or not ontology:
            continue

        # If the same JSON key appears multiple times, merge candidate ontologies
        if json_key not in candidates:
            candidates[json_key] = {"old_json_key": old_json_key, "ontologies": {}}
        candidates[json_key]["ontologies"][ontology] = (candidate_term, ontology_link)

    return candidates


def collect_all_candidates(groups):
    """
    Combine the group candidates into a global dictionary with keys:
       (group_index, json_key)
    and values of the form:
       {
         "old_json_key": ...,
         "ontologies": { ontology: (candidate_term, ontology_link), ... }
       }
    """
    all_candidates = {}
    for group_index, rows in enumerate(groups):
        group_candidates = collect_group_candidates(rows)
        for json_key, cand_dict in group_candidates.items():
            # Use (group_index, json_key) as a unique key
            all_candidates[(group_index, json_key)] = cand_dict
    return all_candidates


def assign_ontologies(global_candidates):
    """
    Greedy set cover-like algorithm to select a minimal set of ontologies
    covering all (group_index, json_key) occurrences.

    Returns:
        assignment: dict mapping (group_index, json_key) -> (candidate_term, ontology, ontology_link, old_json_key)
        selected_ontologies: set of ontologies used in the final assignment
    """
    # Build a reverse mapping: ontology -> set of (group_index, json_key) occurrences
    ontology_to_occurrences = defaultdict(set)
    for occurrence, cand_dict in global_candidates.items():
        for ontology in cand_dict["ontologies"]:
            ontology_to_occurrences[ontology].add(occurrence)

    uncovered = set(global_candidates.keys())
    assignment = {}
    selected_ontologies = set()

    # Greedy algorithm: pick the ontology that covers the largest number
    while uncovered:
        best_ontology = None
        best_cover = set()
        for ontology, occ_set in ontology_to_occurrences.items():
            cover = occ_set & uncovered
            if len(cover) > len(best_cover):
                best_cover = cover
                best_ontology = ontology

        if best_ontology is None or not best_cover:
            break

        # Assign best_ontology to all occurrences it covers
        for occurrence in best_cover:
            cand_dict = global_candidates[occurrence]
            candidate_term, ontology_link = cand_dict["ontologies"][best_ontology]
            old_json_key = cand_dict["old_json_key"]
            assignment[occurrence] = (
                candidate_term,
                best_ontology,
                ontology_link,
                old_json_key,
            )
        uncovered -= best_cover
        selected_ontologies.add(best_ontology)

    return assignment, selected_ontologies


def write_assignments_by_group(assignment, output_csv):
    """
    Writes the final ontology selections grouped by group_index, with the following columns:
        Old JSON Key, JSON Key, OntologyTerm, Selected Ontology, Ontology Link
    """
    groups_assignment = defaultdict(list)
    for (group_index, json_key), (
        candidate_term,
        ontology,
        ontology_link,
        old_json_key,
    ) in assignment.items():
        groups_assignment[group_index].append(
            (old_json_key, candidate_term, ontology, ontology_link)
        )

    header = ["OldJSONKey", "OntologyTerm", "SelectedOntology", "OntologyLink"]
    with open(output_csv, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        for group_index in sorted(groups_assignment.keys()):
            # Sort by JSON key, or old_json_key, or whichever order you prefer
            for row_tuple in sorted(groups_assignment[group_index], key=lambda x: x[1]):
                writer.writerow(row_tuple)


def select_ontologies(input_csv, output_csv):
    groups = read_csv_groups(input_csv)
    if not groups:
        print("No groups found in input.")

    global_candidates = collect_all_candidates(groups)
    if not global_candidates:
        print("No exact match found.")

    assignment, selected_ontologies = assign_ontologies(global_candidates)

    write_assignments_by_group(assignment, output_csv)

    total_occurrences = len(global_candidates)
    print(
        "Created '{}' with assignments for {} JSON key occurrences across {} groups.".format(
            output_csv, total_occurrences, len(groups)
        )
    )
    print("Number of distinct ontologies used: {}".format(len(selected_ontologies)))
