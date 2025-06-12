# Evaluation with RAGAS

## RAGAS
- Collect sample queries, reference answers, and context documents.
- For each query, retrieve relevant docs and generate an answer.
- Build an evaluation dataset with queries, contexts, answers, and references.
- Evaluate using Ragas with chosen metrics (e.g., Recall, Faithfulness, Factual Correctness).
- Output the evaluation results.

## Evaluation Dataset
Header: gene,gene_id,biotype,strand,locus,GroupB_FPKM,GroupA_FPKM,Fold change,log2(fold change),p_value,FDR,Regulation,GeneID,Synonyms,dbXrefs,chromosome,map_location,description,pathway,GO-CC,GO-MF,GO-BP

## Description
Gene Expression Dataset (GSE280797) - Summary
- **Organism:** Human (Homo sapiens), advanced perihilar cholangiocarcinoma (pCCA)
- **Samples:** Bile from patients pre-chemotherapy (good vs. poor prognosis groups)
- **Data columns:** Gene info, expression values (FPKM), fold change, statistics, regulation, functional annotations (pathway, GO)
- **Each row:** Represents one gene (node in graph RAG) with all features above
- **Goal:** Identify genes and pathways linked to chemotherapy response and prognosis

## Plan
- evaluation on a gene dataset
- collect sample queries reference answers 
- treat each row as a context, because in the graph rag knowledge graph, each row is represented as a single node.

Step-by-step:
1. Treat Each Row as a Context: Each row = one context chunk, containing all details for a specific gene.
2. Create Sample Queries: Write natural language queries you expect your RAG to answer, for example:
- What is the biotype of TSPAN6?
- Which chromosome is FGR located on?
- What pathways is WNT16 involved in?
- What is the fold change of expression for TNMD?
- Which gene is described as “sorting nexin 11”?
1. Reference Answers: For each query, use the relevant value or brief summary from the correct row (context).
Examples:
- Query: What is the fold change of expression for TNMD? Reference: 5.36
- Query: Which gene is described as “sorting nexin 11”? Reference: SNX11
1. Link Each Query to Its Context
For each query, context should be the full row (or formatted text) for the relevant gene.
1. Format for RAGAS
- user_input: the query
- retrieved_contexts: the context row(s)
- response: the model’s answer
- reference: your reference answer

## Which Aspects to Cover (Chemotherapy Response and Prognosis)

- **Chemotherapy Response**
  - Ask which genes show the highest up- or down-regulation between Group A (good prognosis) and Group B (poor prognosis).
    - Example: “Which gene is most upregulated in poor prognosis patients?”
    - Example: “List genes downregulated in Group A compared to Group B.”

- **Prognostic Markers**
  - Queries about genes or pathways specifically associated with good or poor prognosis.
    - Example: “Which pathways are enriched in good prognosis samples?”
    - Example: “What gene is a marker for poor prognosis?”

- **Pathway Enrichment and Significance**
  - Questions about over-represented pathways or GO terms in either prognosis group.
    - Example: “Which biological processes are over-represented in Group B?”

- **Gene-Drug Interaction**
  - Inquire about genes potentially involved in drug resistance (e.g., related to oxaliplatin or 5-FU).
    - Example: “Are any genes linked to oxaliplatin resistance?”

- **Statistical Significance**
  - Ask about genes or pathways with significant p-value or FDR.
    - Example: “Which genes are differentially expressed with p-value < 0.05?”

- **Clinical Relevance**
  - Queries about clinical utility, such as predictive biomarkers or potential therapeutic targets.
    - Example: “Which genes might serve as predictive biomarkers for HAIC efficacy?”


## Linking procedure that work towards this goal
- Decide what should be nodes, realized by user defined entities (e.g., gene, Pathway, GO term), this is highly relevant for question answering
- For each row, create a node with the remaining cols as properties
- For each additional node entity type, create nodes (e.g. Create node for “Chemokine signaling pathway” (Pathway))
- For each row create links of the form (:)-[:HAS_Entity_Class]-(:)
- Links should be drawn if property values of entities that originate from the first object (in schema.json) match with property values of other entities

