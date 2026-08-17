#!/usr/bin/env python3
"""Generate README.md from statistics.json.

Usage:
    python3 scripts/generate_readme.py          # write README.md
    python3 scripts/generate_readme.py --check  # verify README is up to date (CI)
"""

STATS_ONLY = False  # Set True to skip full paper list generation
import argparse
import json
import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

CATEGORY_DISPLAY = {
    "knowledge-graphs": "Knowledge Graphs",
    "graphrag": "Graph RAG",
    "graph-databases": "Graph Databases",
    "graph-query-languages": "Graph Query Languages",
    "graph-algorithms": "Graph Algorithms",
    "graph-neural-networks": "Graph Neural Networks",
    "graph-theory": "Graph Theory",
    "network-science": "Network Science",
    "graph-embeddings": "Graph Embeddings",
    "graph-construction": "KG Construction & IE",
    "semantic-web": "Semantic Web & Linked Data",
    "ontology": "Ontologies & Schema",
    "graph-analytics": "Graph Analytics",
    "community-detection": "Community Detection",
    "graph-visualization": "Graph Visualization",
    "graph-machine-learning": "Graph Machine Learning",
    "temporal-graphs": "Temporal & Dynamic Graphs",
    "distributed-graphs": "Distributed Graph Processing",
    "graph-security": "Graph Security & OSINT",
    "graph-applications": "Graph Applications",
}

SUBCATEGORY_DISPLAY = {
    "theory": "Theory",
    "mechanism": "Mechanism",
    "method": "Method",
    "application": "Application",
    "development": "Development",
    "systems": "Systems & Technology",
    "evaluation": "Evaluation & Benchmarks",
    "review": "Reviews & Surveys",
}


def render_readme(stats):
    meta = stats["metadata"]
    total = meta["total_papers"]
    saturation = meta["taxonomy"]["saturation"]
    filled = meta["taxonomy"]["filled_cells"]
    total_cells = meta["taxonomy"]["total_cells"]
    by_cat = stats["by_category"]
    by_sub = stats["by_subcategory"]
    by_year = stats["by_year"]
    by_cell = stats["by_cell"]
    themes = stats.get("emerging_themes_12m", [])

    years = [y for y in by_year if y != "unknown"]
    ymin = min(years, default="—")
    ymax = max(years, default="—")

    top_cats = sorted(by_cat.items(), key=lambda kv: -kv[1])[:6]
    top_cats_rows = "\n".join(
        f"{i+1}. **{CATEGORY_DISPLAY[c]}** — {n} papers" for i, (c, n) in enumerate(top_cats)
    )

    theme_rows = "\n".join(
        f"{i+1}. **{t['keyword']}** — {t['papers']} papers" for i, t in enumerate(themes[:6])
    )

    momentum = stats.get("momentum", [])[:6]
    mom_rows = "\n".join(
        f"| {m['name']} | {m['total']} | {m['recent']} | "
        + (f"{m['growth_pct']:+}%" if m['growth_pct'] is not None else "—")
        + f" | {m['recent_share']*100:.0f}% |"
        for m in momentum
    )

    empty_cells = [c for c in by_cell if by_cell[c] == 0]
    thin = sorted(by_cell.items(), key=lambda kv: kv[1])[:8]
    gap_rows = "\n".join(f"- `{c}` — {n} papers" for c, n in thin)

    cat_table = "\n".join(
        f"| {CATEGORY_DISPLAY[c]} | {by_cat.get(c, 0)} |"
        for c in CATEGORY_DISPLAY
    )
    sub_table = "\n".join(
        f"| {SUBCATEGORY_DISPLAY[s]} | {by_sub.get(s, 0)} |"
        for s in SUBCATEGORY_DISPLAY
    )

    return f"""# Graph Research Corpus

**Evidence base for graphwiz.ai** — Analysis of {total:,} research papers across 20 graph disciplines.

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
| **Papers Analyzed** | {total:,} |
| **Graph Disciplines** | {len(CATEGORY_DISPLAY)} |
| **Time Span** | {ymin}-{ymax} |
| **Research Aspects** | {len(SUBCATEGORY_DISPLAY)} |
| **Taxonomy Cells** | {total_cells} |
| **Saturation** | {saturation}% ({filled}/{total_cells} cells) |

### Top Evidence Areas

{top_cats_rows}

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
{cat_table}

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
{sub_table}

---

## 🚀 Emerging Themes (Last 12 Months)

{theme_rows}

## 📈 Category Momentum (Last 12 Months)

Ranked by output density × year-over-year growth — the strongest leading indicator for what to cover next:

| Category | Total | Last 12m | Growth | 12-m share |
|----------|------:|---------:|-------:|-----------:|
{mom_rows}

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers are prime opportunities for graphwiz.ai articles:

{gap_rows if gap_rows else "- (corpus still saturating — see `statistics.json`) *"}

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

This corpus synthesizes {total:,} papers across {ymin}-{ymax} to create a
comprehensive evidence base for graph-focused content and product decisions.

---

**Want to turn this corpus into articles?**
`cd tools && python3 topic_planner.py`
"""


def main():
    parser = argparse.ArgumentParser(description="Generate README.md")
    parser.add_argument("--check", action="store_true", help="Verify README is current")
    args = parser.parse_args()

    stats_path = BASE / "statistics.json"
    if not stats_path.exists():
        print("ERROR: statistics.json not found — run scripts/analysis/generate_analysis.py first")
        sys.exit(1)

    with open(stats_path, encoding="utf-8") as f:
        stats = json.load(f)

    readme = render_readme(stats)
    readme_path = BASE / "README.md"

    if args.check:
        if readme_path.exists() and readme_path.read_text(encoding="utf-8") == readme:
            print("README.md is up to date")
        else:
            print("README.md is OUT OF DATE — run scripts/generate_readme.py")
            sys.exit(1)
    else:
        readme_path.write_text(readme, encoding="utf-8")
        print(f"Wrote README.md ({len(readme)} chars)")


if __name__ == "__main__":
    main()
