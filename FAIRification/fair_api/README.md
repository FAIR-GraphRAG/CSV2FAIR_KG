## Serve Landing Pages
* Goal: for each dataset serve own landing page with metadata, description, link to GEO etc.
* Goal: for each research object (cell, gene) serve own landing page

## Start FastAPI Server
  ```bash
  uvicorn FAIRification.fair_api.main:app --reload
  ```

## Working Endpoints
* http://127.0.0.1:8000/ds/table_1.json
* http://127.0.0.1:8000/ds/table_2.json
* http://127.0.0.1:8000/ds/table_1.json/fuq44rNaw6wZDMoEaxHZMB
* http://127.0.0.1:8000/ds/table_2.json/Cy6AjG4tjds8NvZNa2D7jX

## Endpoints To Implement
* /cell/table_1/cellA123