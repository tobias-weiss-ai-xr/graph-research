#!/usr/bin/env python3
"""Generate statistics.json, papers.json and D3.js visualization data from papers.yaml."""

import json
import os
import yaml
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

CATEGORY_ORDER = list(CATEGORY_DISPLAY.keys())

SUBCATEGORY_ORDER = [
    "theory",
    "mechanism",
    "method",
    "application",
    "development",
    "systems",
    "evaluation",
    "review",
]

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

CAT_COLORS = [
    "#58a6ff", "#3fb950", "#d29922", "#f0883e", "#db6d8a",
    "#7ee787", "#a5d6ff", "#79c0ff", "#ffa657", "#ff7b72",
    "#d2a8ff", "#79c0ff", "#56d4dd", "#b392f0", "#ffc680",
    "#85e89d", "#f778ba", "#68a4ff", "#ffdf5d", "#a371f7",
]


def main():
    with open(os.path.join(BASE, "papers.yaml"), encoding="utf-8") as f:
        data = yaml.safe_load(f)
    entries = data.get("papers", [])
    print(f"Parsed {len(entries)} papers")

    cat_counter = Counter()
    subcat_counter = Counter()
    cell_counter = Counter()
    year_counter = Counter()
    pub_dates = []

    for e in entries:
        cat = e.get("category", "unknown")
        sub = e.get("subcategory", "unknown")
        cat_counter[cat] += 1
        subcat_counter[sub] += 1
        cell = f"{cat}/{sub}"
        cell_counter[cell] += 1
        d = e.get("date", "")
        if d and len(d) >= 7:
            year = d[:4]
            year_counter[year] += 1
            pub_dates.append((d[:7], cat, sub))
        else:
            year_counter["unknown"] += 1

    total = len(entries)
    total_cells = len(CATEGORY_ORDER) * len(SUBCATEGORY_ORDER)
    filled_cells = len(cell_counter)
    saturation = round(filled_cells / total_cells * 100, 1)

    # 2026 emerging themes: top keyword clusters in last 12 months
    recent = [e for e in entries if e.get("date", "") >= "2025-07"]
    theme_keywords = [
        "GraphRAG", "agent", "foundation model", "LLM", "temporal", "scalable",
        "heterogeneous", "multimodal", "causal", "federated", "quantum",
        "explainability", "streaming", "graph database",
    ]
    themes = {}
    for kw in theme_keywords:
        n = sum(1 for e in recent if kw.lower() in (e.get("title", "") + " " + e.get("abstract", "")).lower())
        if n > 0:
            themes[kw] = n
    top_themes = sorted(themes.items(), key=lambda kv: -kv[1])[:10]

    by_year = {y: year_counter[y] for y in sorted(year_counter, key=lambda x: (x == "unknown", x))}

    stats = {
        "metadata": {
            "total_papers": total,
            "generated_date": max((e.get("date", "") for e in entries if e.get("date")), default=""),
            "taxonomy": {
                "categories": len(CATEGORY_ORDER),
                "subcategories": len(SUBCATEGORY_ORDER),
                "total_cells": total_cells,
                "filled_cells": filled_cells,
                "saturation": saturation,
                "empty_cells": total_cells - filled_cells,
            },
        },
        "by_category": {
            c: cat_counter.get(c, 0) for c in CATEGORY_ORDER
        },
        "by_subcategory": {
            s: subcat_counter.get(s, 0) for s in SUBCATEGORY_ORDER
        },
        "by_year": by_year,
        "by_cell": {
            cell: cell_counter[cell]
            for cell in sorted(cell_counter, key=lambda c: -cell_counter[c])
        },
        "emerging_themes_12m": [{"keyword": k, "papers": v} for k, v in top_themes],
    }

    with open(os.path.join(BASE, "statistics.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"Wrote statistics.json ({total} papers, {saturation}% saturation)")

    # papers.json export (plain list, newest first)
    export = []
    for e in entries:
        export.append(
            {
                "title": e.get("title", ""),
                "date": e.get("date", ""),
                "url": e.get("url", ""),
                "category": e.get("category", ""),
                "subcategory": e.get("subcategory", ""),
                "authors": e.get("authors", []),
                "abstract": e.get("abstract", ""),
                "tags": e.get("tags", []),
            }
        )
    export.sort(key=lambda p: p.get("date", ""), reverse=True)
    with open(os.path.join(BASE, "papers.json"), "w", encoding="utf-8") as f:
        json.dump(export, f, indent=1)
    print(f"Wrote papers.json ({len(export)} papers)")

    # D3 visualization data
    viz = {
        "categories": [
            {
                "id": c,
                "name": CATEGORY_DISPLAY[c],
                "color": CAT_COLORS[i % len(CAT_COLORS)],
                "count": cat_counter.get(c, 0),
                "subcategories": [
                    {"id": s, "name": SUBCATEGORY_DISPLAY[s], "count": cell_counter.get(f"{c}/{s}", 0)}
                    for s in SUBCATEGORY_ORDER
                ],
            }
            for i, c in enumerate(CATEGORY_ORDER)
        ],
        "subcategories": [
            {"id": s, "name": SUBCATEGORY_DISPLAY[s], "count": subcat_counter.get(s, 0)}
            for s in SUBCATEGORY_ORDER
        ],
        "timeline": sorted(pub_dates),
    }
    os.makedirs(os.path.join(BASE, "assets"), exist_ok=True)
    with open(os.path.join(BASE, "assets", "graph_analysis.json"), "w", encoding="utf-8") as f:
        json.dump(viz, f, indent=1)
    print("Wrote assets/graph_analysis.json")


if __name__ == "__main__":
    main()
