# PID Management Concept for Datasets and Research Objects

## Task
* The goal is to create a FAIR knowledge graph
* The nodes should serve as FAIR Digital Objects
* Datasets are represented as FAIR DOs, but also research objects such as cells or genes
* A FAIR DO needs a persistent identifier
* Create a PID management concept for datasets and research objects

## Datasets
* Register metadata with [Zenodo Sandbox](https://sandbox.zenodo.org/)
* Create a dataset DOI at one of these services
* The DOI resolves to a landing page (hosted by me), which:
  * Describes the dataset
  * Links to original GEO page
  * Contains provenance/licensing information
  * Links to derived research objects

## Research Objects (Cells, genes etc.)
* Use internal/custom URN (Uniform Resource Name)
* e.g. urn:cell:<dataset_id>:<cell_id>
* Set up a resolver for URNs:
  * Use w3id.org
  * Fork their GitHub repo
  * Create a redirect rule: /cell/gse0001/cellA123 → https://fair-graph.org/cell/gse0001/cellA123
  * Serve a landing page or API for the cell
  * Return JSON-LD
  
## Landing Page
* Use FastAPI to realize it

## Receipt
* Find best practice to construct the DOI/URL in literature
* Assign dummy DOI to dataset, which should resolve to landing page
* Assign internal PIDs/URNs to cells DONE
* Set up FastAPI server DONE
* Provide metadata, description, link to GEO page etc.
* Serve a landing page for each cell with its metadata and link to dataset
* Example path from literature: https://purl.example.com/a9/e42
