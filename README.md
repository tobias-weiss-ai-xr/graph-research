# Graph Research Corpus

**Evidence base for graphwiz.ai** — Analysis of 16,979 research papers across 20 graph disciplines.

**Author:** Tobias Weiss
**Contact:** tobias@graphwiz.ai
**Website:** [graphwiz.ai](https://graphwiz.ai)

---

## 🎯 Overview

This repository contains the research corpus and tooling for the AI-and-Graphs
content site [graphwiz.ai](https://graphwiz.ai): knowledge graphs, GraphRAG,
graph databases, graph neural networks, network science and every adjacent
discipline. It mirrors the structure of the
[learning-research](https://github.com/tobias-weiss-ai-xr/learning-research)
corpus and feeds evidence-based article topics into the graphwiz-reporter
pipeline.

### Research Scope

| Metric | Value |
|--------|-------|
| **Papers Analyzed** | 16,979 |
| **Graph Disciplines** | 20 |
| **Time Span** | 2021-2026 |
| **Research Aspects** | 8 |
| **Taxonomy Cells** | 160 |
| **Saturation** | 100.0% (160/160 cells) |

### Top Evidence Areas

1. **Graph Neural Networks** — 2240 papers
2. **Graph Applications** — 1441 papers
3. **Knowledge Graphs** — 1440 papers
4. **Network Science** — 1394 papers
5. **Graph RAG** — 956 papers
6. **Graph Embeddings** — 948 papers

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
| Knowledge Graphs | 1440 |
| Graph RAG | 956 |
| Graph Databases | 504 |
| Graph Query Languages | 288 |
| Graph Algorithms | 945 |
| Graph Neural Networks | 2240 |
| Graph Theory | 892 |
| Network Science | 1394 |
| Graph Embeddings | 948 |
| KG Construction & IE | 883 |
| Semantic Web & Linked Data | 361 |
| Ontologies & Schema | 932 |
| Graph Analytics | 244 |
| Community Detection | 683 |
| Graph Visualization | 201 |
| Graph Machine Learning | 920 |
| Temporal & Dynamic Graphs | 536 |
| Distributed Graph Processing | 350 |
| Graph Security & OSINT | 821 |
| Graph Applications | 1441 |

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
| Theory | 2299 |
| Mechanism | 1807 |
| Method | 2631 |
| Application | 4881 |
| Development | 431 |
| Systems & Technology | 2998 |
| Evaluation & Benchmarks | 1439 |
| Reviews & Surveys | 493 |

---

## 🚀 Emerging Themes (Last 12 Months)

1. **LLM** — 1295 papers
2. **agent** — 674 papers
3. **temporal** — 484 papers
4. **heterogeneous** — 423 papers
5. **scalable** — 386 papers
6. **GraphRAG** — 199 papers

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers are prime opportunities for graphwiz.ai articles:

- `distributed-graphs/review` — 5 papers
- `graph-theory/development` — 6 papers
- `graph-algorithms/review` — 7 papers
- `graph-analytics/development` — 7 papers
- `graph-analytics/review` — 7 papers
- `temporal-graphs/review` — 7 papers
- `distributed-graphs/method` — 7 papers
- `community-detection/development` — 7 papers

---

## 📁 Repository Structure

```
graph-research/
├── README.md                          # This file
├── papers.json                        # Paper metadata (JSON export)
├── papers.yaml                        # Paper metadata (source of truth)
├── statistics.json                    # Analysis statistics
├── requirements.txt                   # Python dependencies
│
├── assets/visualizations/             # Generated charts and graphs
│
├── docs/
│   ├── research/                      # Literature review, taxonomy, trend reports
│   └── topics/                        # Generated article topics for graphwiz.ai
│
├── tools/                             # Article planning tools
│   ├── topic_planner.py               # Article topic planner ✨
│   ├── trend_scanner.py               # Emerging trend scanner ✨
│   └── brief_generator.py             # Article brief generator ✨
│
├── scripts/                           # Research pipeline
│   ├── fetch/fetch_new_papers.py      # arXiv discovery (auto-classified)
│   ├── analysis/generate_analysis.py  # Statistics + visualizations
│   ├── validate_papers.py             # Corpus validation
│   └── generate_readme.py             # README generator
│
└── examples/                          # Usage examples
```

---

## 🛠️ Tools

### 1. Article Topic Planner

Generate evidence-based article topics for graphwiz.ai from the corpus.

```bash
cd tools
python3 topic_planner.py --top 10
```

### 2. Trend Scanner

Detect emerging research trends from recent papers (keyword burst analysis).

```bash
cd tools
python3 trend_scanner.py --months 6
```

### 3. Article Brief Generator

Turn a topic into a ready-to-write article brief (angle, outline, key papers).

```bash
cd tools
python3 brief_generator.py "GraphRAG at scale" --papers 5
```

---

## 🔄 Research Pipeline

1. **Discover** — `python3 scripts/fetch/fetch_new_papers.py --months 3`
   (arXiv search across 110+ queries, auto-classified into the taxonomy)
2. **Validate** — `python3 scripts/validate_papers.py`
3. **Analyze** — `python3 scripts/analysis/generate_analysis.py`
4. **Visualize** — `python3 scripts/visualize_statistics.py`
5. **Generate** — `python3 scripts/generate_readme.py`

CI (`.github/workflows/validate.yml`) validates and regenerates on every push;
a weekly scheduled job opens a PR with newly discovered papers.

---

## 🔗 Related Repositories

- **Content site:** [next-graphwiz-ai](https://github.com/tobias-weiss-ai-xr/next-graphwiz-ai) — graphwiz.ai
- **Graph library:** [graphwiz-graph-lib](https://github.com/tobias-weiss-ai-xr/graphwiz-graph-lib)
- **Analogous corpus:** [learning-research](https://github.com/tobias-weiss-ai-xr/learning-research)

---

## 📄 License

**© 2026 GraphWiz | Tobias Weiss**

- **Research corpus:** Proprietary
- **Tools:** MIT License

---

## 🙏 Acknowledgments

This corpus synthesizes 16,979 papers across 2021-2026 to create a
comprehensive evidence base for graph-focused content and product decisions.

---

**Want to turn this corpus into articles?**
`cd tools && python3 topic_planner.py`
