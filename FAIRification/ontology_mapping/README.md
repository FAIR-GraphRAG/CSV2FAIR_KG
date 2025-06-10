# Ontology Mapping Pipeline

This pipeline adds ontology mappings to a JSON schema and enriches associated data files to support semantic interoperability in FAIR knowledge graphs. The goal is to link schema terms (e.g., fields in biomedical datasets) to standardized ontology terms, using both automated services and customizable logic.

---

## Pipeline Overview

The ontology mapping process follows four key stages:

### 1. Extract and Recommend Ontologies
- Extracts all keys from the `properties` section of a JSON schema.
- Splits complex identifiers into readable keywords using camelCase splitting.
- Queries the BioPortal API (bioontology.org) to retrieve ontology terms that exactly match the extracted keywords.
- If no exact match is found, the pipeline applies a fallback heuristic using part-of-speech tagging (via `TextBlob`) to identify the most meaningful noun from compound terms (e.g., `test_Name`, `short_Histological_Findings`) for a second attempt at matching.
- The result is a list of candidate ontology terms per key, including labels, ontology sources, and URIs, stored in a CSV file.

### 2. Select the Most Suitable Mappings
- Candidate terms are grouped by JSON key and filtered to include only exact matches.
- A greedy algorithm selects a minimal set of ontologies that collectively cover the most terms.
- Each key is assigned a preferred ontology term, producing a concise and consistent mapping.

### 3. Generate a Schema with Ontology Annotations
- The selected mappings are merged with the original JSON schema.
- Each key is annotated with:
  - `ontology_term`
  - `ontology_name`
  - `ontology_link`
- This creates a semantically enriched schema suitable for FAIR-aligned data sharing and integration.

### 4. Enrich Data Files with Ontology Information
- Each JSON data file is enriched using the annotated schema.
- For each property, the corresponding ontology metadata is added alongside its value.
- The result is a set of JSON files with embedded, machine-readable semantic context.

---

## Use Cases
- Creating FAIR-compliant metadata for biomedical datasets.
- Supporting semantic search, integration, and inference in knowledge graphs.
- Enabling downstream tasks like automated reasoning, entity linking, and LLM-based concept alignment.

---

## Input & Output Summary

| Step                         | Input                          | Output                          |
|------------------------------|--------------------------------|---------------------------------|
| Ontology recommendation      | JSON schema                    | Candidate ontology CSV          |
| Ontology selection           | Candidate CSV                  | Final selection CSV             |
| Schema enrichment            | Selection CSV + schema         | Ontology-annotated JSON schema  |
| Data enrichment              | Annotated schema + data files  | Enriched JSON data files        |

---

## Notes
- BioPortal (via the NCBO BioOntology API) is used for ontology term discovery.
- A fallback mechanism identifies the most meaningful noun when exact matches fail, using part-of-speech analysis.
- Custom or LLM-verified mappings can later be added for unmapped terms.
- Designed for modular reuse and extension in FAIR data infrastructures.

