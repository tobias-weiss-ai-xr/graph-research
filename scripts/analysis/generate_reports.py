#!/usr/bin/env python3
"""Generate research reports from the corpus:
  - docs/research/literature_review.md   (synthesis + top papers per category)
  - docs/research/graph_trends_2026.md   (trend report from trend scanner)

Usage:
    python3 scripts/analysis/generate_reports.py
"""

import os
import sys
from collections import Counter, defaultdict
from datetime import datetime

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "tools"))
from trend_scanner import scan as scan_trends  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE)

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

KEY_INSIGHTS = {
    "knowledge-graphs": (
        "Knowledge graphs are consolidating as the context layer for LLM agents. "
        "The LLM×KG intersection dominates recent output: KG-augmented reasoning, "
        "hallucination mitigation and KG completion with LLMs."
    ),
    "graphrag": (
        "GraphRAG is the fastest-moving category: a flood of method papers "
        "(hierarchical, agentic, adaptive retrieval) but relatively few "
        "production benchmarks — a gap worth covering on graphwiz.ai."
    ),
    "graph-databases": (
        "Graph database research clusters around query performance, indexing and "
        "benchmarks; native-graph engines and GQL adoption are recurring themes."
    ),
    "graph-query-languages": (
        "The move toward a GQL standard plus Cypher/SPARQL interop is the main "
        "story; query optimisation remains the core research problem."
    ),
    "graph-neural-networks": (
        "GNN research has shifted from new architectures toward expressivity "
        "limits, scalability and explainability — maturity signals for production."
    ),
    "graph-machine-learning": (
        "Graph foundation models and self-supervised pre-training are emerging as "
        "the next wave, replacing task-specific GNN training."
    ),
    "graph-security": (
        "Fraud detection, attack graphs and threat intelligence are the dominant "
        "applications; graph + GNN approaches increasingly beat tabular baselines."
    ),
    "temporal-graphs": (
        "Temporal and dynamic knowledge graphs are a clear growth cell — "
        "time-aware embeddings and event-driven KG updates are active frontiers."
    ),
}


def render_literature_review(papers, now):
    total = len(papers)
    lines = [
        "# Graph Research — Literature Review",
        "",
        f"**Generated:** {now}  ",
        f"**Corpus:** {total:,} papers across {len(CATEGORY_DISPLAY)} categories",
        "",
        "> Synthesis of the graph research corpus. Category insights are drawn "
        "from title/abstract analysis of the papers themselves.",
        "",
        "---",
        "",
        "## Corpus Overview",
        "",
    ]
    cat_counter = Counter(p.get("category", "unknown") for p in papers)
    sub_counter = Counter(p.get("subcategory", "unknown") for p in papers)
    year_counter = Counter(p.get("date", "")[:4] for p in papers if p.get("date"))
    top_cats = sorted(cat_counter.items(), key=lambda kv: -kv[1])[:5]

    lines.append("| Rank | Category | Papers |")
    lines.append("|------|----------|--------|")
    for i, (c, n) in enumerate(top_cats, 1):
        lines.append(f"| {i} | {CATEGORY_DISPLAY.get(c, c)} | {n} |")

    years = sorted(y for y in year_counter if y)
    lines += [
        "",
        f"**Time span:** {years[0]}–{years[-1]} (median year {years[len(years)//2] if years else '—'})",
        f"**Dominant aspects:** {', '.join(f'{SUBCATEGORY_DISPLAY.get(s, s)} ({n})' for s, n in sub_counter.most_common(3))}",
        "",
        "---",
        "",
        "## Category Insights",
        "",
    ]
    for c in sorted(cat_counter, key=lambda c: -cat_counter[c]):
        if cat_counter[c] == 0:
            continue
        insight = KEY_INSIGHTS.get(c, "Category is still saturating — see `statistics.json` for cell counts.")
        # top recent papers
        cat_papers = [p for p in papers if p.get("category") == c and p.get("date", "") >= "2025-01"]
        cat_papers.sort(key=lambda p: p.get("date", ""), reverse=True)
        top3 = cat_papers[:3]
        lines += [
            f"### {CATEGORY_DISPLAY.get(c, c)} (`{c}`)",
            "",
            f"{insight}",
            "",
            f"**Corpus size:** {cat_counter[c]} papers",
        ]
        if top3:
            lines += ["", "**Recent papers:**", ""]
            for p in top3:
                lines.append(f"- [{p['date']}] {p['title'][:100]} — {p.get('url', '')}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines += [
        "## Methodology",
        "",
        "1. Papers are discovered via taxonomy-aware arXiv queries and "
        "auto-classified into the 20×8 taxonomy.",
        "2. Category insights above are editorially curated but grounded in "
        "corpus statistics.",
        "3. Regenerate this document with `scripts/analysis/generate_reports.py`.",
        "",
    ]
    return "\n".join(lines)


def render_trend_report(papers, now):
    result = scan_trends(papers, months=12, top=15)
    lines = [
        "# Graph Research Trends (12-Month View)",
        "",
        f"**Generated:** {now}  ",
        f"**Window:** since {result['cutoff']} — {result['recent_papers']} of {len(papers)} papers",
        "",
        "## 🔥 Keyword Bursts",
        "",
        "| Keyword | Recent | Total | Burst |",
        "|---------|--------|-------|-------|",
    ]
    for t in result["trends"]:
        lines.append(f"| {t['keyword']} | {t['recent_papers']} | {t['total_papers']} | {t['burst_score']}× |")

    lines += [
        "",
        "## 📈 Fastest-Growing Cells",
        "",
        "| Cell | Recent | Total | Recent Share |",
        "|------|--------|-------|--------------|",
    ]
    for g in result["growing_cells"]:
        lines.append(f"| `{g['cell']}` | {g['recent']} | {g['total']} | {g['recent_share']*100:.0f}% |")

    lines += [
        "",
        "## What This Means for graphwiz.ai",
        "",
        "- Categories with high burst scores are the safest article bets "
        "(reader interest follows research momentum).",
        "- Fast-growing cells with few total papers are white-space opportunities: "
        "early coverage builds topical authority.",
        "- Thin cells in `statistics.json` mark research gaps where evidence is "
        "thin — write with appropriate caution.",
        "",
        "Regenerate with `python3 tools/trend_scanner.py --months 12`.",
        "",
    ]
    return "\n".join(lines)


def main():
    with open(os.path.join(BASE, "papers.yaml"), encoding="utf-8") as f:
        data = yaml.safe_load(f)
    papers = data.get("papers", [])
    now = datetime.now().isoformat()[:10]

    lit_path = os.path.join(BASE, "docs", "research", "literature_review.md")
    with open(lit_path, "w", encoding="utf-8") as f:
        f.write(render_literature_review(papers, now))
    print(f"Wrote {lit_path}")

    trend_path = os.path.join(BASE, "docs", "research", "graph_trends_2026.md")
    with open(trend_path, "w", encoding="utf-8") as f:
        f.write(render_trend_report(papers, now))
    print(f"Wrote {trend_path}")


if __name__ == "__main__":
    main()
