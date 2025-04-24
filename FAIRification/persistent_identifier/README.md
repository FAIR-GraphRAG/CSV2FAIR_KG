# PID Management Concept for Datasets and Research Objects

## Datasets
* Register metadata with DataCite, Zenodo or Figshare
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
