# Graph Research Taxonomy

The corpus is organised as a 20×8 taxonomy: **20 categories** (research
domains) × **8 subcategories** (research aspects) = **160 cells**.

## Categories (20)

| # | Key | Display Name | Coverage |
|---|-----|--------------|----------|
| 1 | `knowledge-graphs` | Knowledge Graphs | KG construction, completion, reasoning, QA, LLM×KG |
| 2 | `graphrag` | Graph RAG | Graph-based retrieval-augmented generation, GraphRAG variants |
| 3 | `graph-databases` | Graph Databases | Neo4j, TigerGraph, Memgraph, storage, indexing, benchmarks |
| 4 | `graph-query-languages` | Graph Query Languages | Cypher, openCypher, GQL, SPARQL, PGQL, query optimisation |
| 5 | `graph-algorithms` | Graph Algorithms | PageRank, centrality, shortest path, matching, cuts |
| 6 | `graph-neural-networks` | Graph Neural Networks | GNNs, message passing, graph transformers, scalability |
| 7 | `graph-theory` | Graph Theory | Graph colouring, minors, spectral theory, random graphs |
| 8 | `network-science` | Network Science | Complex networks, scale-free networks, influence dynamics |
| 9 | `graph-embeddings` | Graph Embeddings | KG embeddings, node/graph embedding, representation learning |
| 10 | `graph-construction` | KG Construction & IE | IE, entity linking, relation/event extraction, schema induction |
| 11 | `semantic-web` | Semantic Web & Linked Data | RDF, linked data, SPARQL endpoints, semantic reasoning |
| 12 | `ontology` | Ontologies & Schema | Ontology alignment/matching/learning, schema design |
| 13 | `graph-analytics` | Graph Analytics | Analytics workloads, summarisation, sampling |
| 14 | `community-detection` | Community Detection | Clustering, overlapping communities, graph clustering |
| 15 | `graph-visualization` | Graph Visualization | Graph drawing, layout, force-directed, visual analytics |
| 16 | `graph-machine-learning` | Graph Machine Learning | Link prediction, node classification, foundation models |
| 17 | `temporal-graphs` | Temporal & Dynamic Graphs | Temporal KGs, dynamic graphs, evolving networks |
| 18 | `distributed-graphs` | Distributed Graph Processing | Pregel-style systems, partitioning, GPU processing |
| 19 | `graph-security` | Graph Security & OSINT | Fraud detection, attack graphs, threat intelligence, OSINT |
| 20 | `graph-applications` | Graph Applications | Recommendation, life sciences, finance, supply chain, code |

## Subcategories (8)

| # | Key | Meaning |
|---|-----|---------|
| 1 | `theory` | Theoretical foundations, complexity, expressivity |
| 2 | `mechanism` | How methods work internally, interpretability |
| 3 | `method` | New methods and approaches |
| 4 | `application` | Applied in real-world domains |
| 5 | `development` | Tools, libraries, open-source implementations |
| 6 | `systems` | Engines, platforms, infrastructure |
| 7 | `evaluation` | Benchmarks, datasets, empirical comparisons |
| 8 | `review` | Surveys, overviews, state-of-the-art |

## Cell Example

`graphrag/method` = new GraphRAG methods; `graph-databases/evaluation` =
graph database benchmarks; `graph-neural-networks/theory` = GNN expressivity
results.

## Auto-Classification

The fetch pipeline (`scripts/fetch/fetch_new_papers.py`) assigns categories
from the query that discovered each paper and subcategories via keyword rules
(`scripts/fetch/fetch_new_papers.py` → `SUBCATEGORY_RULES`). Manual curation
in PRs improves accuracy over time.
