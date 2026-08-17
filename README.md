# Graph Research Corpus

**Evidence base for graphwiz.ai** — Analysis of 20,008 research papers across 20 graph disciplines.

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
| **Papers Analyzed** | 20,008 |
| **Graph Disciplines** | 20 |
| **Time Span** | 1980-2027 |
| **Research Aspects** | 8 |
| **Taxonomy Cells** | 160 |
| **Saturation** | 100.0% (160/160 cells) |

### Top Evidence Areas

1. **Graph Neural Networks** — 2583 papers
2. **Knowledge Graphs** — 1626 papers
3. **Network Science** — 1586 papers
4. **Graph Applications** — 1580 papers
5. **Graph Theory** — 1096 papers
6. **Graph Algorithms** — 1083 papers

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
| Knowledge Graphs | 1626 |
| Graph RAG | 1078 |
| Graph Databases | 614 |
| Graph Query Languages | 409 |
| Graph Algorithms | 1083 |
| Graph Neural Networks | 2583 |
| Graph Theory | 1096 |
| Network Science | 1586 |
| Graph Embeddings | 1058 |
| KG Construction & IE | 952 |
| Semantic Web & Linked Data | 499 |
| Ontologies & Schema | 1009 |
| Graph Analytics | 307 |
| Community Detection | 840 |
| Graph Visualization | 435 |
| Graph Machine Learning | 1072 |
| Temporal & Dynamic Graphs | 691 |
| Distributed Graph Processing | 516 |
| Graph Security & OSINT | 974 |
| Graph Applications | 1580 |

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
| Theory | 2576 |
| Mechanism | 2140 |
| Method | 3384 |
| Application | 5634 |
| Development | 495 |
| Systems & Technology | 3501 |
| Evaluation & Benchmarks | 1599 |
| Reviews & Surveys | 679 |

---

## 🚀 Emerging Themes (Last 12 Months)

1. **osint** — 2 papers
2. **agentic** — 248 papers
3. **graphrag** — 199 papers
4. **agent** — 786 papers
5. **graph rag** — 48 papers
6. **retrieval** — 940 papers

## 📈 Category Momentum (Last 12 Months)

Ranked by output density × year-over-year growth — the strongest leading indicator for what to cover next:

| Category | Total | Last 12m | Growth | 12-m share |
|----------|------:|---------:|-------:|-----------:|
| Graph RAG | 1078 | 706 | +145.1% | 66% |
| Ontologies & Schema | 1009 | 458 | +122.3% | 45% |
| Graph Query Languages | 409 | 177 | +124.1% | 43% |
| Graph Databases | 614 | 242 | +83.3% | 39% |
| Graph Security & OSINT | 974 | 356 | +58.9% | 37% |
| Graph Neural Networks | 2583 | 790 | +58.0% | 31% |

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers are prime opportunities for graphwiz.ai articles:

- `distributed-graphs/review` — 5 papers
- `graph-analytics/development` — 8 papers
- `graph-theory/development` — 9 papers
- `temporal-graphs/review` — 9 papers
- `community-detection/development` — 9 papers
- `graph-analytics/review` — 10 papers
- `graph-theory/evaluation` — 11 papers
- `graph-embeddings/development` — 11 papers

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

This corpus synthesizes 20,008 papers across 1980-2027 to create a
comprehensive evidence base for graph-focused content and product decisions.

---

**Want to turn this corpus into articles?**
`cd tools && python3 topic_planner.py`
