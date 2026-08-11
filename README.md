# Graph Research Corpus

**Evidence base for graphwiz.ai** — Analysis of 18,143 research papers across 20 graph disciplines.

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
| **Papers Analyzed** | 18,143 |
| **Graph Disciplines** | 20 |
| **Time Span** | 1980-2027 |
| **Research Aspects** | 8 |
| **Taxonomy Cells** | 160 |
| **Saturation** | 100.0% (160/160 cells) |

### Top Evidence Areas

1. **Graph Neural Networks** — 2433 papers
2. **Knowledge Graphs** — 1530 papers
3. **Graph Applications** — 1526 papers
4. **Network Science** — 1467 papers
5. **Graph RAG** — 1047 papers
6. **Graph Embeddings** — 980 papers

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
| Knowledge Graphs | 1530 |
| Graph RAG | 1047 |
| Graph Databases | 516 |
| Graph Query Languages | 333 |
| Graph Algorithms | 962 |
| Graph Neural Networks | 2433 |
| Graph Theory | 952 |
| Network Science | 1467 |
| Graph Embeddings | 980 |
| KG Construction & IE | 887 |
| Semantic Web & Linked Data | 409 |
| Ontologies & Schema | 971 |
| Graph Analytics | 259 |
| Community Detection | 717 |
| Graph Visualization | 262 |
| Graph Machine Learning | 959 |
| Temporal & Dynamic Graphs | 578 |
| Distributed Graph Processing | 409 |
| Graph Security & OSINT | 946 |
| Graph Applications | 1526 |

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
| Theory | 2432 |
| Mechanism | 1943 |
| Method | 2826 |
| Application | 5186 |
| Development | 452 |
| Systems & Technology | 3199 |
| Evaluation & Benchmarks | 1508 |
| Reviews & Surveys | 597 |

---

## 🚀 Emerging Themes (Last 12 Months)

1. **osint** — 2 papers
2. **agentic** — 245 papers
3. **graphrag** — 192 papers
4. **agent** — 760 papers
5. **graph rag** — 46 papers
6. **retrieval** — 926 papers

## 📈 Category Momentum (Last 12 Months)

Ranked by output density × year-over-year growth — the strongest leading indicator for what to cover next:

| Category | Total | Last 12m | Growth | 12-m share |
|----------|------:|---------:|-------:|-----------:|
| Graph Query Languages | 333 | 144 | +220.0% | 43% |
| Graph RAG | 1047 | 676 | +135.5% | 65% |
| Graph Databases | 516 | 218 | +150.6% | 42% |
| Ontologies & Schema | 971 | 439 | +134.8% | 45% |
| Graph Visualization | 262 | 82 | +95.2% | 31% |
| Semantic Web & Linked Data | 409 | 128 | +93.9% | 31% |

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers are prime opportunities for graphwiz.ai articles:

- `distributed-graphs/review` — 5 papers
- `graph-theory/development` — 6 papers
- `graph-algorithms/review` — 7 papers
- `graph-analytics/review` — 7 papers
- `graph-analytics/development` — 8 papers
- `temporal-graphs/review` — 8 papers
- `community-detection/development` — 8 papers
- `graph-query-languages/review` — 10 papers

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

This corpus synthesizes 18,143 papers across 1980-2027 to create a
comprehensive evidence base for graph-focused content and product decisions.

---

**Want to turn this corpus into articles?**
`cd tools && python3 topic_planner.py`
