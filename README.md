# Graph Research Corpus

**Evidence base for graphwiz.ai** — Analysis of 3,160 research papers across 20 graph disciplines.

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
| **Papers Analyzed** | 3,160 |
| **Graph Disciplines** | 20 |
| **Time Span** | 2023-2026 |
| **Research Aspects** | 8 |
| **Taxonomy Cells** | 160 |
| **Saturation** | 94.4% (151/160 cells) |

### Top Evidence Areas

1. **Graph Neural Networks** — 283 papers
2. **Graph Applications** — 245 papers
3. **Graph Machine Learning** — 244 papers
4. **Graph Algorithms** — 229 papers
5. **Knowledge Graphs** — 226 papers
6. **Graph RAG** — 217 papers

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
| Knowledge Graphs | 226 |
| Graph RAG | 217 |
| Graph Databases | 126 |
| Graph Query Languages | 66 |
| Graph Algorithms | 229 |
| Graph Neural Networks | 283 |
| Graph Theory | 178 |
| Network Science | 203 |
| Graph Embeddings | 153 |
| KG Construction & IE | 162 |
| Semantic Web & Linked Data | 86 |
| Ontologies & Schema | 135 |
| Graph Analytics | 54 |
| Community Detection | 144 |
| Graph Visualization | 27 |
| Graph Machine Learning | 244 |
| Temporal & Dynamic Graphs | 132 |
| Distributed Graph Processing | 55 |
| Graph Security & OSINT | 195 |
| Graph Applications | 245 |

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
| Theory | 500 |
| Mechanism | 217 |
| Method | 154 |
| Application | 55 |
| Development | 54 |
| Systems & Technology | 238 |
| Evaluation & Benchmarks | 1116 |
| Reviews & Surveys | 826 |

---

## 🚀 Emerging Themes (Last 12 Months)

1. **LLM** — 310 papers
2. **agent** — 143 papers
3. **temporal** — 114 papers
4. **heterogeneous** — 114 papers
5. **scalable** — 96 papers
6. **multimodal** — 50 papers

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers are prime opportunities for graphwiz.ai articles:

- `graph-query-languages/mechanism` — 1 papers
- `graph-query-languages/application` — 1 papers
- `graph-neural-networks/development` — 1 papers
- `graph-embeddings/development` — 1 papers
- `semantic-web/development` — 1 papers
- `semantic-web/application` — 1 papers
- `graph-visualization/method` — 1 papers
- `graph-applications/method` — 1 papers

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

This corpus synthesizes 3,160 papers across 2023-2026 to create a
comprehensive evidence base for graph-focused content and product decisions.

---

**Want to turn this corpus into articles?**
`cd tools && python3 topic_planner.py`
