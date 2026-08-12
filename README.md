# Graph Research Corpus

**Evidence base for graphwiz.ai** — Analysis of 17,926 research papers across 20 graph disciplines.

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
| **Papers Analyzed** | 17,926 |
| **Graph Disciplines** | 20 |
| **Time Span** | 1980-2027 |
| **Research Aspects** | 8 |
| **Taxonomy Cells** | 160 |
| **Saturation** | 100.0% (160/160 cells) |

### Top Evidence Areas

1. **Graph Neural Networks** — 2368 papers
2. **Graph Applications** — 1507 papers
3. **Knowledge Graphs** — 1480 papers
4. **Network Science** — 1435 papers
5. **Graph RAG** — 1040 papers
6. **Graph Embeddings** — 972 papers

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
| Knowledge Graphs | 1480 |
| Graph RAG | 1040 |
| Graph Databases | 524 |
| Graph Query Languages | 350 |
| Graph Algorithms | 948 |
| Graph Neural Networks | 2368 |
| Graph Theory | 948 |
| Network Science | 1435 |
| Graph Embeddings | 972 |
| KG Construction & IE | 891 |
| Semantic Web & Linked Data | 413 |
| Ontologies & Schema | 954 |
| Graph Analytics | 258 |
| Community Detection | 713 |
| Graph Visualization | 261 |
| Graph Machine Learning | 944 |
| Temporal & Dynamic Graphs | 572 |
| Distributed Graph Processing | 408 |
| Graph Security & OSINT | 940 |
| Graph Applications | 1507 |

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
| Theory | 2405 |
| Mechanism | 1915 |
| Method | 2813 |
| Application | 5110 |
| Development | 452 |
| Systems & Technology | 3147 |
| Evaluation & Benchmarks | 1484 |
| Reviews & Surveys | 600 |

---

## 🚀 Emerging Themes (Last 12 Months)

1. **osint** — 2 papers
2. **agentic** — 230 papers
3. **graphrag** — 188 papers
4. **agent** — 718 papers
5. **graph rag** — 45 papers
6. **retrieval** — 883 papers

## 📈 Category Momentum (Last 12 Months)

Ranked by output density × year-over-year growth — the strongest leading indicator for what to cover next:

| Category | Total | Last 12m | Growth | 12-m share |
|----------|------:|---------:|-------:|-----------:|
| Graph Query Languages | 350 | 161 | +257.8% | 46% |
| Graph Databases | 524 | 226 | +159.8% | 43% |
| Graph RAG | 1040 | 669 | +133.1% | 64% |
| Ontologies & Schema | 954 | 422 | +125.7% | 44% |
| Semantic Web & Linked Data | 413 | 132 | +100.0% | 32% |
| Graph Visualization | 261 | 81 | +92.9% | 31% |

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers are prime opportunities for graphwiz.ai articles:

- `distributed-graphs/review` — 5 papers
- `graph-algorithms/review` — 7 papers
- `graph-theory/development` — 7 papers
- `graph-analytics/review` — 7 papers
- `graph-analytics/development` — 8 papers
- `temporal-graphs/review` — 8 papers
- `community-detection/development` — 8 papers
- `graph-theory/evaluation` — 11 papers

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

This corpus synthesizes 17,926 papers across 1980-2027 to create a
comprehensive evidence base for graph-focused content and product decisions.

---

**Want to turn this corpus into articles?**
`cd tools && python3 topic_planner.py`
