# Evaluation

## Idea
- Compare FAIR GraphRAG against non-FAIR GraphRAG on GSE280797 series

## Steps
- Improve metadata modeling
  - Create separate metadata JSON files for document and entity node
  - Use domain-specific metadata format of file, if available, else fill backup metadata schema and add uncovered entries
- Update FAIR RAG
- Create Non-FAIR RAG
- Assist FAIRness of FAIR RAG and Non-FAIR RAG
- Create QAs for evaluation
- Compare approaches