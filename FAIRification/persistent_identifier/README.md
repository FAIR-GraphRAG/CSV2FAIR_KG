# PID Management Concept for Datasets and Research Objects

## Datasets
* Register metadata with [Zenodo Sandbox](https://sandbox.zenodo.org/)
* Find full API documentation (works also for Sandbox): https://developers.zenodo.org/#representation22
* Create a dataset DOI at one of these services
* The DOI resolves to a landing page (hosted by me), which:
  * Describes the dataset
  * Links to original GEO page
  * Contains provenance/licensing information
  * Links to derived research objects

## Research Objects (Cells, genes etc.)
* Use internal/custom URN (Uniform Resource Name)
* e.g. urn:cell:<dataset_id>:<cell_id>
  
## Receipt
* Assign dummy DOI to dataset, which should resolve to landing page
* Assign internal PIDs/URNs to cells
* Set up FastAPI server
* Provide metadata, description, link to GEO page etc.
* Serve a landing page for each cell with its metadata and link to dataset
* Example path from literature: https://purl.example.com/a9/e42
