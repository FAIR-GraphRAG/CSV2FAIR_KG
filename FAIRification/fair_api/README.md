## Serve Landing Pages
* Goal: for each dataset serve own landing page with metadata, description, link to GEO etc.
* Goal: for each entity/research object (cell, gene) serve own landing page

## Start FastAPI Server
  ```bash
  uvicorn FAIRification.fair_api.main:app --reload
  ```

## Example Endpoints (exchange with actual identifiers)
* dataset: http://127.0.0.1:8000/10.5281/zenodo.213278
* dataset: http://127.0.0.1:8000/10.5281/zenodo.213280
* entity: http://127.0.0.1:8000/10.5281/zenodo.213278/nht5QgsLp2U4j9yCM9Thou
