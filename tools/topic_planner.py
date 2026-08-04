#!/usr/bin/env python3
"""Evidence-based article topic planner for graphwiz.ai.

Scans the graph research corpus and produces ranked article topics by
combining: corpus density (hot cells), recent growth (12-month velocity),
research gaps (thin cells) and emerging keyword themes. Output is written
to docs/topics/ARTICLE_TOPICS.md and printed to the terminal.

Usage:
    python3 tools/topic_planner.py --top 10
    python3 tools/topic_planner.py --category graphrag
    python3 tools/topic_planner.py --json
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime

import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

# Editorial topic templates per category. {{angle}}, {{n}} and {{year}} are substituted.
TOPIC_TEMPLATES = {
    "graphrag": [
        "GraphRAG in production: {{angle}}",
        "GraphRAG variants compared {{year}}: {{angle}}",
        "When graphs beat vectors in RAG: {{angle}}",
        "The real cost of GraphRAG at scale: {{angle}}",
        "Agentic retrieval over knowledge graphs: {{angle}}",
    ],
    "knowledge-graphs": [
        "Knowledge graphs as the context layer for AI agents: {{angle}}",
        "From knowledge graphs to context graphs: {{angle}}",
        "LLM-generated knowledge graphs: {{angle}}",
        "Knowledge graph construction from unstructured data: {{angle}}",
        "Knowledge graphs vs. vector stores: {{angle}}",
    ],
    "graph-databases": [
        "Graph databases compared {{year}}: {{angle}}",
        "Neo4j production patterns: {{angle}}",
        "When to choose a graph database: {{angle}}",
        "Property graphs vs. RDF stores: {{angle}}",
        "Graph database benchmarks {{year}}: {{angle}}",
    ],
    "graph-neural-networks": [
        "Graph neural networks in production: {{angle}}",
        "GNN expressivity limits: {{angle}}",
        "Scaling GNNs to billion-edge graphs: {{angle}}",
        "Graph transformers vs. message passing: {{angle}}",
        "Explainable GNNs: {{angle}}",
    ],
    "graph-algorithms": [
        "Graph algorithms with Neo4j GDS: {{angle}}",
        "Shortest path at scale: {{angle}}",
        "PageRank and beyond: {{angle}}",
        "Choosing the right graph algorithm: {{angle}}",
        "Centrality measures explained: {{angle}}",
    ],
    "graph-query-languages": [
        "GQL vs. Cypher vs. SPARQL: {{angle}}",
        "Cypher query optimization: {{angle}}",
        "Graph query performance tuning: {{angle}}",
        "The expressiveness gap in graph query languages: {{angle}}",
        "Writing better graph queries: {{angle}}",
    ],
    "graph-construction": [
        "Knowledge graph construction pipelines: {{angle}}",
        "From documents to knowledge graphs with LLMs: {{angle}}",
        "Entity resolution for knowledge graphs: {{angle}}",
        "Schema induction from unstructured text: {{angle}}",
        "Information extraction, 2026 edition: {{angle}}",
    ],
    "temporal-graphs": [
        "Temporal knowledge graphs: {{angle}}",
        "Dynamic graphs in production: {{angle}}",
        "Time-aware graph analytics: {{angle}}",
        "Event-driven knowledge graph updates: {{angle}}",
    ],
    "graph-machine-learning": [
        "Link prediction with graph ML: {{angle}}",
        "Graph foundation models: {{angle}}",
        "Self-supervised graph learning: {{angle}}",
        "Graph ML benchmarks and leaderboards: {{angle}}",
        "Node classification at scale: {{angle}}",
    ],
    "graph-security": [
        "Fraud detection with knowledge graphs: {{angle}}",
        "Graph-powered OSINT: {{angle}}",
        "Attack graph analysis: {{angle}}",
        "Using graphs to stop financial crime: {{angle}}",
        "Graph neural networks for security: {{angle}}",
    ],
    "community-detection": [
        "Community detection algorithms compared: {{angle}}",
        "Finding clusters in knowledge graphs: {{angle}}",
        "Community detection at scale: {{angle}}",
        "Overlapping communities: {{angle}}",
    ],
    "graph-applications": [
        "Graph-based recommendation systems: {{angle}}",
        "Knowledge graphs in the enterprise: {{angle}}",
        "Graphs in life sciences: {{angle}}",
        "Graph databases in the enterprise: {{angle}}",
        "Graphs in supply chain and logistics: {{angle}}",
    ],
    "ontology": [
        "Ontology design in {{year}}: {{angle}}",
        "Ontology matching with LLMs: {{angle}}",
        "Why ontologies matter for AI agents: {{angle}}",
        "Schema design for knowledge graphs: {{angle}}",
    ],
    "graph-visualization": [
        "Graph visualization: {{angle}}",
        "Interactive knowledge graph visualizations: {{angle}}",
        "Visualizing billion-node graphs: {{angle}}",
        "Graph drawing algorithms: {{angle}}",
    ],
    "semantic-web": [
        "The semantic web, still relevant: {{angle}}",
        "Linked data patterns in {{year}}: {{angle}}",
        "RDF vs. property graphs revisited: {{angle}}",
    ],
    "network-science": [
        "Network science for engineers: {{angle}}",
        "Complex networks in production: {{angle}}",
        "Influence maximization and virality: {{angle}}",
        "Scale-free networks explained: {{angle}}",
    ],
    "graph-embeddings": [
        "Knowledge graph embeddings: {{angle}}",
        "Graph embeddings vs. GNNs: {{angle}}",
        "Node embeddings in practice: {{angle}}",
        "Embedding-based link prediction: {{angle}}",
    ],
    "distributed-graphs": [
        "Distributed graph processing: {{angle}}",
        "Graph partitioning at scale: {{angle}}",
        "GPU graph analytics: {{angle}}",
        "Pregel and beyond: {{angle}}",
    ],
    "graph-analytics": [
        "Graph analytics cookbook: {{angle}}",
        "Graph summarization and sampling: {{angle}}",
        "Graph analytics in the enterprise: {{angle}}",
        "Graph analytics: {{angle}}",
    ],
    "graph-theory": [
        "Graph theory for software engineers: {{angle}}",
        "Spectral graph theory, explained: {{angle}}",
        "Random graphs and real-world networks: {{angle}}",
        "Graph colouring in practice: {{angle}}",
    ],
}

ANGLE_BANK = [
    "benchmarks vs. reality",
    "what the papers actually say",
    "production lessons",
    "a practical guide",
    "the state of the art",
    "common pitfalls",
    "a comparison you can use",
    "what changed this year",
    "the 80/20 of implementation",
    "open-source options",
    "cost and scale trade-offs",
]

PRIORITY_ANGLE = {
    "graphrag": "deployment realities and cost models",
    "graph-databases": "production patterns and benchmarks",
    "knowledge-graphs": "LLM integration and agent context",
    "graph-neural-networks": "scaling and real-world adoption",
    "graph-construction": "LLM-driven pipelines and quality",
    "graph-machine-learning": "from benchmarks to production",
    "graph-security": "real-world cases and pitfalls",
    "graph-applications": "what works in production",
}


def load_papers():
    with open(os.path.join(BASE, "papers.yaml"), encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("papers", [])


def build_cell_stats(papers, now):
    cell_total = Counter()
    cell_recent = Counter()
    cat_total = Counter()
    theme_counter = Counter()

    # Extract focus terms per category from titles
    focus_by_cat = defaultdict(Counter)
    for p in papers:
        cat = p.get("category", "")
        sub = p.get("subcategory", "")
        cell_total[(cat, sub)] += 1
        cat_total[cat] += 1
        date = p.get("date", "")
        if date >= now[:4] + "-0" or (len(date) >= 7 and date >= f"{int(now[:4]) - 1}-01"):
            cell_recent[(cat, sub)] += 1
            text = (p.get("title", "") + " " + p.get("abstract", "")[:300]).lower()
            for kw in FOCUS_KEYWORDS.get(cat, []):
                if kw in text:
                    focus_by_cat[cat][kw] += 1

    return cell_total, cell_recent, cat_total, focus_by_cat


FOCUS_KEYWORDS = {
    "graphrag": ["graphrag", "graph rag", "retrieval-augmented", "retrieval augmented"],
    "knowledge-graphs": ["knowledge graph", "kg completion", "kg reasoning"],
    "graph-databases": ["graph database", "neo4j", "tigergraph", "memgraph", "property graph"],
    "graph-neural-networks": ["graph neural", "gnn", "graph transformer", "message passing"],
    "graph-construction": ["information extraction", "entity linking", "relation extraction", "construction"],
    "temporal-graphs": ["temporal", "dynamic graph", "evolving"],
    "graph-machine-learning": ["link prediction", "node classification", "foundation model", "self-supervised"],
    "graph-security": ["fraud", "threat", "attack graph", "cyber", "osint"],
    "graph-query-languages": ["cypher", "gql", "sparql", "query optimization"],
    "graph-algorithms": ["page rank", "pagerank", "centrality", "shortest path", "community detection"],
    "community-detection": ["community detection", "graph clustering"],
}


def plan_topics(papers, category_filter=None, top=10):
    now = datetime.now().isoformat()[:10]
    cat_total = Counter(p.get("category", "") for p in papers)
    recent_by_cat = Counter(
        p.get("category", "") for p in papers if p.get("date", "") >= f"{int(now[:4]) - 1}-01"
    )

    categories = [c for c in CATEGORY_DISPLAY if cat_total.get(c, 0) > 0]
    if category_filter:
        categories = [c for c in categories if c == category_filter or category_filter in c]

    topics = []
    for cat in categories:
        n_total = cat_total.get(cat, 0)
        recent_n = recent_by_cat.get(cat, 0)
        velocity = recent_n / n_total if n_total else 0
        angle = PRIORITY_ANGLE.get(cat) or ANGLE_BANK[min(len(ANGLE_BANK) - 1, list(CATEGORY_DISPLAY).index(cat) % len(ANGLE_BANK))]

        templates = TOPIC_TEMPLATES.get(cat, ["{name}: {{angle}}"])
        for t in templates:
            title = (
                t.replace("{{angle}}", angle)
                .replace("{{n}}", str(n_total))
                .replace("{{year}}", now[:4])
            )
            topics.append(
                {
                    "category": cat,
                    "category_name": CATEGORY_DISPLAY[cat],
                    "papers": n_total,
                    "velocity_12m": round(velocity, 2),
                    "title": title,
                    "angle": angle,
                }
            )

    # rank: density (papers) * velocity, with a small boost for hot categories
    topics.sort(key=lambda t: (t["papers"] * (0.5 + t["velocity_12m"]), t["papers"]), reverse=True)
    # diversity: cap at 2 topics per category in the top list
    seen = {}
    diverse = []
    for t in topics:
        seen[t["category"]] = seen.get(t["category"], 0) + 1
        if seen[t["category"]] <= 2:
            diverse.append(t)
    return diverse[:top]


def render_markdown(topics, papers, now):
    lines = [
        "# Article Topics for graphwiz.ai",
        "",
        f"**Generated:** {now}  ",
        f"**Corpus:** {len(papers):,} papers | **Topics:** {len(topics)}",
        "",
        "> Topics are ranked by corpus density × 12-month research velocity.",
        "> Each topic is backed by the cited paper counts — research first, then write.",
        "",
        "---",
        "",
        "## 🏆 Top Article Topics",
        "",
    ]
    for i, t in enumerate(topics, 1):
        lines += [
            f"### {i}. {t['title']}",
            "",
            f"- **Category:** {t['category_name']} (`{t['category']}`)",
            f"- **Evidence:** {t['papers']} papers in corpus | {round(t['velocity_12m'] * 100)}% published in last 12 months",
            f"- **Angle:** {t['angle']}",
            "",
        ]
    lines += [
        "---",
        "",
        "## 🛠️ Workflow",
        "",
        "1. Pick a topic above.",
        "2. `python3 tools/brief_generator.py \"<topic title>\" --papers 5` for a full brief.",
        "3. Write and publish via the `graphwiz-reporter` pipeline.",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Article topic planner for graphwiz.ai")
    parser.add_argument("--top", type=int, default=10, help="Number of topics (default: 10)")
    parser.add_argument("--category", default=None, help="Filter by category key")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    papers = load_papers()
    now = datetime.now().isoformat()[:10]
    topics = plan_topics(papers, category_filter=args.category, top=args.top)

    if args.json:
        print(json.dumps(topics, indent=2))
        return

    md = render_markdown(topics, papers, now)
    out_path = os.path.join(BASE, "docs", "topics", "ARTICLE_TOPICS.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Wrote {len(topics)} topics to {out_path}\n")
    print(md)


if __name__ == "__main__":
    main()
