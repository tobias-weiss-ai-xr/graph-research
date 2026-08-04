# Graph Research Corpus

**Evidence base for graphwiz.ai** — Analysis of 8,329 research papers across 20 graph disciplines.

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
| **Papers Analyzed** | 8,329 |
| **Graph Disciplines** | 20 |
| **Time Span** | 2023-2026 |
| **Research Aspects** | 8 |
| **Taxonomy Cells** | 160 |
| **Saturation** | 100.0% (160/160 cells) |

### Top Evidence Areas

1. **Graph Neural Networks** — 1100 papers
2. **Graph Applications** — 783 papers
3. **Network Science** — 680 papers
4. **Knowledge Graphs** — 638 papers
5. **Graph RAG** — 552 papers
6. **Graph Machine Learning** — 514 papers

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
| Knowledge Graphs | 638 |
| Graph RAG | 552 |
| Graph Databases | 249 |
| Graph Query Languages | 103 |
| Graph Algorithms | 429 |
| Graph Neural Networks | 1100 |
| Graph Theory | 420 |
| Network Science | 680 |
| Graph Embeddings | 465 |
| KG Construction & IE | 391 |
| Semantic Web & Linked Data | 155 |
| Ontologies & Schema | 366 |
| Graph Analytics | 100 |
| Community Detection | 353 |
| Graph Visualization | 78 |
| Graph Machine Learning | 514 |
| Temporal & Dynamic Graphs | 292 |
| Distributed Graph Processing | 164 |
| Graph Security & OSINT | 497 |
| Graph Applications | 783 |

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
| Theory | 1247 |
| Mechanism | 967 |
| Method | 1035 |
| Application | 2456 |
| Development | 216 |
| Systems & Technology | 1488 |
| Evaluation & Benchmarks | 714 |
| Reviews & Surveys | 206 |

---

## 🚀 Emerging Themes (Last 12 Months)

1. **LLM** — 840 papers
2. **agent** — 387 papers
3. **temporal** — 362 papers
4. **heterogeneous** — 321 papers
5. **scalable** — 285 papers
6. **multimodal** — 138 papers

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers are prime opportunities for graphwiz.ai articles:

- `distributed-graphs/method` — 1 papers
- `graph-algorithms/review` — 2 papers
- `graph-theory/development` — 2 papers
- `temporal-graphs/review` — 2 papers
- `distributed-graphs/review` — 2 papers
- `graph-visualization/review` — 2 papers
- `semantic-web/review` — 3 papers
- `community-detection/review` — 3 papers

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

This corpus synthesizes 8,329 papers across 2023-2026 to create a
comprehensive evidence base for graph-focused content and product decisions.

---

**Want to turn this corpus into articles?**
`cd tools && python3 topic_planner.py`
