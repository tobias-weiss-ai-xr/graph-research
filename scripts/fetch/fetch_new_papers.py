#!/usr/bin/env python3
"""Discover graph research papers from the arXiv API across all 20 taxonomy categories.

Runs 100+ queries spanning knowledge graphs, GraphRAG, graph databases, GNNs,
network science and all other categories in the taxonomy. Each query carries a
category (and keyword-derived subcategory) so new papers are auto-classified
into the 20x8 taxonomy on discovery.

Usage:
    python3 scripts/fetch/fetch_new_papers.py --months 3 --dry-run
    python3 scripts/fetch/fetch_new_papers.py --months 1 --create-pr
"""

import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
import yaml

ARXIV_ID_PATTERN = re.compile(r"(\d{4}\.\d{4,5})")
ARXIV_SEARCH_API = (
    "https://export.arxiv.org/api/query?search_query={}&start={}&max_results={}"
)

# (query, category, subcategory-hint). Subcategory is refined by keyword scoring
# on title/abstract; the hint is used as a fallback when nothing matches.
QUERIES = [
    # --- knowledge-graphs ---
    ('cat:cs.AI AND abs:"knowledge graph" AND abs:"survey"', "knowledge-graphs", "review"),
    ('cat:cs.CL AND abs:"knowledge graph"', "knowledge-graphs", "method"),
    ('cat:cs.AI AND abs:"knowledge graph" AND abs:"reasoning"', "knowledge-graphs", "method"),
    ('cat:cs.AI AND abs:"knowledge graph" AND abs:"completion"', "knowledge-graphs", "method"),
    ('cat:cs.AI AND abs:"knowledge graph" AND abs:"question answering"', "knowledge-graphs", "application"),
    ('cat:cs.IR AND abs:"knowledge graph"', "knowledge-graphs", "application"),
    ('cat:cs.AI AND abs:"large language model" AND abs:"knowledge graph"', "knowledge-graphs", "method"),
    ('cat:cs.AI AND abs:"LLM" AND abs:"knowledge graph"', "knowledge-graphs", "method"),
    ('cat:cs.AI AND abs:"knowledge graph" AND abs:"hallucination"', "knowledge-graphs", "application"),
    ('cat:cs.DB AND abs:"knowledge graph"', "knowledge-graphs", "systems"),
    # --- graphrag ---
    ('all:"GraphRAG"', "graphrag", "method"),
    ('all:"graph RAG"', "graphrag", "method"),
    ('cat:cs.CL AND abs:"retrieval-augmented" AND abs:"graph"', "graphrag", "method"),
    ('cat:cs.AI AND abs:"retrieval-augmented generation" AND abs:"graph"', "graphrag", "method"),
    ('cat:cs.CL AND abs:"knowledge graph" AND abs:"retrieval" AND abs:"generation"', "graphrag", "method"),
    ('cat:cs.CL AND abs:"graph-based retrieval"', "graphrag", "method"),
    ('cat:cs.AI AND abs:"retrieval" AND abs:"graph" AND abs:"LLM"', "graphrag", "method"),
    ('cat:cs.CL AND abs:"retrieval-augmented" AND abs:"knowledge graph"', "graphrag", "method"),
    ('cat:cs.IR AND abs:"hybrid retrieval" AND abs:"graph"', "graphrag", "evaluation"),
    ('cat:cs.CL AND abs:"agentic" AND abs:"graph" AND abs:"retrieval"', "graphrag", "method"),
    # --- graph-databases ---
    ('cat:cs.DB AND abs:"graph database"', "graph-databases", "systems"),
    ('cat:cs.DB AND abs:"graph database" AND abs:"benchmark"', "graph-databases", "evaluation"),
    ('cat:cs.DB AND abs:"property graph"', "graph-databases", "systems"),
    ('cat:cs.DB AND abs:"graph storage"', "graph-databases", "systems"),
    ('cat:cs.DB AND abs:"native graph"', "graph-databases", "systems"),
    ('cat:cs.DB AND abs:"graph index"', "graph-databases", "method"),
    ('cat:cs.DB AND abs:"graph query processing"', "graph-databases", "systems"),
    ('cat:cs.DB AND abs:"RDF" AND abs:"database"', "graph-databases", "systems"),
    # --- graph-query-languages ---
    ('cat:cs.DB AND abs:"Cypher"', "graph-query-languages", "method"),
    ('all:"openCypher"', "graph-query-languages", "method"),
    ('cat:cs.DB AND abs:"GQL" AND abs:"graph"', "graph-query-languages", "method"),
    ('cat:cs.DB AND abs:"graph query language"', "graph-query-languages", "method"),
    ('cat:cs.DB AND abs:"SPARQL"', "graph-query-languages", "method"),
    ('cat:cs.DB AND abs:"subgraph matching"', "graph-query-languages", "method"),
    ('cat:cs.DB AND abs:"graph pattern matching"', "graph-query-languages", "method"),
    ('cat:cs.DB AND abs:"graph query optimization"', "graph-query-languages", "method"),
    # --- graph-algorithms ---
    ('cat:cs.DS AND abs:"graph algorithm"', "graph-algorithms", "method"),
    ('cat:cs.DS AND abs:"shortest path" AND abs:"graph"', "graph-algorithms", "method"),
    ('cat:cs.DS AND abs:"PageRank"', "graph-algorithms", "method"),
    ('cat:cs.DS AND abs:"centrality"', "graph-algorithms", "method"),
    ('cat:cs.LG AND abs:"graph algorithm"', "graph-algorithms", "method"),
    ('cat:cs.DS AND abs:"graph matching" AND abs:"algorithm"', "graph-algorithms", "method"),
    ('cat:cs.DS AND abs:"graph partition"', "graph-algorithms", "method"),
    ('cat:cs.DS AND abs:"minimum cut"', "graph-algorithms", "theory"),
    ('cat:cs.DS AND abs:"maximum flow" AND abs:"graph"', "graph-algorithms", "theory"),
    # --- graph-neural-networks ---
    ('cat:cs.LG AND abs:"graph neural network"', "graph-neural-networks", "method"),
    ('cat:cs.LG AND abs:"GNN"', "graph-neural-networks", "method"),
    ('cat:cs.LG AND abs:"graph transformer"', "graph-neural-networks", "method"),
    ('cat:cs.LG AND abs:"graph neural network" AND abs:"survey"', "graph-neural-networks", "review"),
    ('cat:cs.LG AND abs:"graph neural network" AND abs:"expressivity"', "graph-neural-networks", "theory"),
    ('cat:cs.LG AND abs:"message passing" AND abs:"graph"', "graph-neural-networks", "mechanism"),
    ('cat:cs.LG AND abs:"graph neural network" AND abs:"scalable"', "graph-neural-networks", "systems"),
    ('cat:cs.LG AND abs:"graph neural network" AND abs:"explainability"', "graph-neural-networks", "mechanism"),
    ('cat:cs.LG AND abs:"heterogeneous graph neural"', "graph-neural-networks", "method"),
    ('cat:cs.LG AND abs:"dynamic graph neural"', "graph-neural-networks", "method"),
    # --- graph-theory ---
    ('cat:math.CO AND abs:"graph theory"', "graph-theory", "theory"),
    ('cat:math.CO AND abs:"graph coloring"', "graph-theory", "theory"),
    ('cat:cs.DS AND abs:"graph theory"', "graph-theory", "theory"),
    ('cat:math.CO AND abs:"random graphs"', "graph-theory", "theory"),
    ('cat:math.CO AND abs:"expander graphs"', "graph-theory", "theory"),
    ('cat:math.CO AND abs:"graph minor"', "graph-theory", "theory"),
    ('cat:cs.DS AND abs:"spectral graph"', "graph-theory", "theory"),
    # --- network-science ---
    ('cat:cs.SI AND abs:"complex network"', "network-science", "method"),
    ('cat:physics.soc-ph AND abs:"complex network"', "network-science", "method"),
    ('cat:cs.SI AND abs:"network science"', "network-science", "theory"),
    ('cat:cs.SI AND abs:"scale-free"', "network-science", "theory"),
    ('cat:cs.SI AND abs:"network analysis"', "network-science", "method"),
    ('cat:cs.SI AND abs:"influence maximization"', "network-science", "method"),
    ('cat:cs.SI AND abs:"graphlet"', "network-science", "method"),
    ('cat:physics.soc-ph AND abs:"network" AND abs:"dynamics"', "network-science", "mechanism"),
    # --- graph-embeddings ---
    ('cat:cs.LG AND abs:"knowledge graph embedding"', "graph-embeddings", "method"),
    ('cat:cs.CL AND abs:"knowledge graph embedding"', "graph-embeddings", "method"),
    ('cat:cs.LG AND abs:"graph embedding"', "graph-embeddings", "method"),
    ('cat:cs.LG AND abs:"node embedding"', "graph-embeddings", "method"),
    ('cat:cs.LG AND abs:"graph representation learning"', "graph-embeddings", "method"),
    ('cat:cs.LG AND abs:"link prediction" AND abs:"embedding"', "graph-embeddings", "application"),
    ('cat:cs.LG AND abs:"translation-based" AND abs:"knowledge"', "graph-embeddings", "method"),
    # --- graph-construction ---
    ('cat:cs.CL AND abs:"knowledge graph construction"', "graph-construction", "method"),
    ('cat:cs.CL AND abs:"information extraction" AND abs:"graph"', "graph-construction", "method"),
    ('cat:cs.CL AND abs:"entity linking"', "graph-construction", "method"),
    ('cat:cs.CL AND abs:"relation extraction" AND abs:"knowledge"', "graph-construction", "method"),
    ('cat:cs.CL AND abs:"event extraction" AND abs:"graph"', "graph-construction", "method"),
    ('cat:cs.CL AND abs:"LLM" AND abs:"information extraction"', "graph-construction", "method"),
    ('cat:cs.CL AND abs:"ontology" AND abs:"knowledge graph construction"', "graph-construction", "method"),
    ('cat:cs.CL AND abs:"entity resolution"', "graph-construction", "method"),
    ('cat:cs.CL AND abs:"schema induction"', "graph-construction", "method"),
    # --- semantic-web ---
    ('cat:cs.DB AND abs:"semantic web"', "semantic-web", "technology"),
    ('cat:cs.AI AND abs:"semantic web"', "semantic-web", "technology"),
    ('cat:cs.DB AND abs:"linked data"', "semantic-web", "technology"),
    ('cat:cs.DB AND abs:"RDF" AND abs:"reasoning"', "semantic-web", "method"),
    ('cat:cs.DB AND abs:"SPARQL" AND abs:"query"', "semantic-web", "method"),
    ('cat:cs.AI AND abs:"RDF" AND abs:"knowledge"', "semantic-web", "technology"),
    ('cat:cs.DB AND abs:"knowledge graph" AND abs:"RDF"', "semantic-web", "technology"),
    # --- ontology ---
    ('cat:cs.AI AND abs:"ontology" AND abs:"alignment"', "ontology", "method"),
    ('cat:cs.AI AND abs:"ontology matching"', "ontology", "method"),
    ('cat:cs.AI AND abs:"ontology" AND abs:"LLM"', "ontology", "method"),
    ('cat:cs.AI AND abs:"ontology learning"', "ontology", "method"),
    ('cat:cs.AI AND abs:"ontological" AND abs:"reasoning"', "ontology", "method"),
    ('cat:cs.AI AND abs:"schema" AND abs:"knowledge graph"', "ontology", "method"),
    ('cat:cs.CL AND abs:"taxonomy" AND abs:"construction"', "ontology", "method"),
    # --- graph-analytics ---
    ('cat:cs.DB AND abs:"graph analytics"', "graph-analytics", "application"),
    ('cat:cs.LG AND abs:"graph analytics"', "graph-analytics", "application"),
    ('cat:cs.DB AND abs:"graph processing" AND abs:"analytics"', "graph-analytics", "systems"),
    ('cat:cs.DB AND abs:"graph summarization"', "graph-analytics", "method"),
    ('cat:cs.DB AND abs:"graph sampling"', "graph-analytics", "method"),
    ('cat:cs.SI AND abs:"graph analytics"', "graph-analytics", "application"),
    # --- community-detection ---
    ('cat:cs.SI AND abs:"community detection"', "community-detection", "method"),
    ('cat:cs.LG AND abs:"community detection"', "community-detection", "method"),
    ('cat:physics.soc-ph AND abs:"community detection"', "community-detection", "method"),
    ('cat:cs.SI AND abs:"community discovery"', "community-detection", "method"),
    ('cat:cs.SI AND abs:"overlapping community"', "community-detection", "method"),
    ('cat:cs.SI AND abs:"graph clustering"', "community-detection", "method"),
    ('cat:cs.LG AND abs:"graph clustering"', "community-detection", "method"),
    # --- graph-visualization ---
    ('cat:cs.GR AND abs:"graph drawing"', "graph-visualization", "method"),
    ('cat:cs.GR AND abs:"graph visualization"', "graph-visualization", "method"),
    ('cat:cs.HC AND abs:"graph visualization"', "graph-visualization", "method"),
    ('cat:cs.GR AND abs:"force-directed"', "graph-visualization", "method"),
    ('cat:cs.GR AND abs:"graph layout"', "graph-visualization", "method"),
    ('cat:cs.GR AND abs:"network visualization"', "graph-visualization", "method"),
    ('cat:cs.GR AND abs:"visualization" AND abs:"knowledge graph"', "graph-visualization", "application"),
    # --- graph-machine-learning ---
    ('cat:cs.LG AND abs:"link prediction"', "graph-machine-learning", "method"),
    ('cat:cs.LG AND abs:"node classification"', "graph-machine-learning", "method"),
    ('cat:cs.LG AND abs:"graph classification"', "graph-machine-learning", "method"),
    ('cat:cs.LG AND abs:"graph self-supervised"', "graph-machine-learning", "method"),
    ('cat:cs.LG AND abs:"graph contrastive learning"', "graph-machine-learning", "method"),
    ('cat:cs.LG AND abs:"graph foundation model"', "graph-machine-learning", "method"),
    ('cat:cs.LG AND abs:"graph pre-training"', "graph-machine-learning", "method"),
    ('cat:cs.LG AND abs:"graph generative model"', "graph-machine-learning", "method"),
    ('cat:cs.LG AND abs:"graph learning" AND abs:"survey"', "graph-machine-learning", "review"),
    # --- temporal-graphs ---
    ('cat:cs.SI AND abs:"temporal graph"', "temporal-graphs", "method"),
    ('cat:cs.LG AND abs:"temporal graph"', "temporal-graphs", "method"),
    ('cat:cs.LG AND abs:"dynamic graph" AND abs:"learning"', "temporal-graphs", "method"),
    ('cat:cs.DB AND abs:"temporal graph"', "temporal-graphs", "method"),
    ('cat:cs.LG AND abs:"dynamic knowledge graph"', "temporal-graphs", "method"),
    ('cat:cs.SI AND abs:"evolving network"', "temporal-graphs", "mechanism"),
    ('cat:cs.LG AND abs:"temporal knowledge graph"', "temporal-graphs", "method"),
    # --- distributed-graphs ---
    ('cat:cs.DB AND abs:"distributed graph processing"', "distributed-graphs", "systems"),
    ('cat:cs.DC AND abs:"graph processing"', "distributed-graphs", "systems"),
    ('cat:cs.DB AND abs:"graph partitioning"', "distributed-graphs", "method"),
    ('cat:cs.DB AND abs:"Pregel"', "distributed-graphs", "systems"),
    ('cat:cs.DC AND abs:"distributed graph"', "distributed-graphs", "systems"),
    ('cat:cs.DB AND abs:"GPU" AND abs:"graph processing"', "distributed-graphs", "systems"),
    ('cat:cs.DB AND abs:"graph systems"', "distributed-graphs", "systems"),
    # --- graph-security ---
    ('cat:cs.CR AND abs:"fraud detection" AND abs:"graph"', "graph-security", "application"),
    ('cat:cs.LG AND abs:"fraud detection" AND abs:"graph"', "graph-security", "application"),
    ('cat:cs.CR AND abs:"graph" AND abs:"cyber"', "graph-security", "application"),
    ('cat:cs.CR AND abs:"threat intelligence" AND abs:"graph"', "graph-security", "application"),
    ('cat:cs.LG AND abs:"anomaly detection" AND abs:"graph"', "graph-security", "method"),
    ('cat:cs.SI AND abs:"graph" AND abs:"cybersecurity"', "graph-security", "application"),
    ('cat:cs.CR AND abs:"attack graph"', "graph-security", "method"),
    ('cat:cs.LG AND abs:"graph neural network" AND abs:"security"', "graph-security", "application"),
    # --- graph-applications ---
    ('cat:cs.IR AND abs:"graph" AND abs:"recommender"', "graph-applications", "application"),
    ('cat:cs.LG AND abs:"graph neural network" AND abs:"recommendation"', "graph-applications", "application"),
    ('cat:q-bio.MN AND abs:"graph neural network"', "graph-applications", "application"),
    ('cat:cs.LG AND abs:"molecular graph"', "graph-applications", "application"),
    ('cat:cs.LG AND abs:"drug discovery" AND abs:"graph"', "graph-applications", "application"),
    ('cat:cs.SI AND abs:"social network" AND abs:"graph" AND abs:"learning"', "graph-applications", "application"),
    ('cat:cs.CE AND abs:"graph" AND abs:"supply chain"', "graph-applications", "application"),
    ('cat:cs.AI AND abs:"knowledge graph" AND abs:"medicine"', "graph-applications", "application"),
    ('cat:cs.AI AND abs:"knowledge graph" AND abs:"financial"', "graph-applications", "application"),
    ('cat:cs.LG AND abs:"graph" AND abs:"software" AND abs:"dependency"', "graph-applications", "application"),
    ('cat:cs.SE AND abs:"graph" AND abs:"code" AND abs:"analysis"', "graph-applications", "application"),
    # --- saturation pass: deepen thin + hot categories ---
    ('cat:cs.HC AND abs:"network visualization"', "graph-visualization", "method"),
    ('cat:cs.GR AND abs:"visual analytics" AND abs:"graph"', "graph-visualization", "method"),
    ('cat:cs.HC AND abs:"knowledge graph" AND abs:"visual"', "graph-visualization", "application"),
    ('cat:cs.GR AND abs:"graph layout" AND abs:"algorithm"', "graph-visualization", "method"),
    ('cat:cs.HC AND abs:"node-link"', "graph-visualization", "method"),
    ('cat:cs.GR AND abs:"graph drawing" AND abs:"planar"', "graph-visualization", "theory"),
    ('cat:cs.DB AND abs:"graph summarization"', "graph-analytics", "method"),
    ('cat:cs.LG AND abs:"graph summarization"', "graph-analytics", "method"),
    ('cat:cs.DB AND abs:"graph sampling"', "graph-analytics", "method"),
    ('cat:cs.DB AND abs:"graph compression"', "graph-analytics", "method"),
    ('cat:cs.LG AND abs:"graph kernel"', "graph-analytics", "method"),
    ('cat:cs.DB AND abs:"approximate graph" AND abs:"query"', "graph-analytics", "method"),
    ('cat:cs.DC AND abs:"parallel graph"', "distributed-graphs", "systems"),
    ('cat:cs.DB AND abs:"graph engine"', "distributed-graphs", "systems"),
    ('cat:cs.DB AND abs:"graph join"', "distributed-graphs", "systems"),
    ('cat:cs.DC AND abs:"graph processing" AND abs:"streaming"', "distributed-graphs", "systems"),
    ('cat:cs.DB AND abs:"subgraph query"', "distributed-graphs", "systems"),
    ('cat:cs.DB AND abs:"regular path query"', "graph-query-languages", "method"),
    ('cat:cs.DB AND abs:"graph database" AND abs:"query" AND abs:"optimization"', "graph-query-languages", "method"),
    ('cat:cs.DB AND abs:"graph algebra"', "graph-query-languages", "theory"),
    ('cat:cs.DB AND abs:"query planning" AND abs:"graph"', "graph-query-languages", "systems"),
    ('cat:cs.DB AND abs:"graph query" AND abs:"benchmark"', "graph-query-languages", "evaluation"),
    ('cat:cs.DB AND abs:"RDF stream"', "semantic-web", "systems"),
    ('cat:cs.AI AND abs:"linked data" AND abs:"query"', "semantic-web", "method"),
    ('cat:cs.DB AND abs:"ontology-based data access"', "semantic-web", "method"),
    ('cat:cs.AI AND abs:"description logic" AND abs:"reasoning"', "semantic-web", "theory"),
    ('cat:cs.LG AND abs:"graph neural network" AND abs:"embedding"', "graph-embeddings", "method"),
    ('cat:cs.LG AND abs:"knowledge graph completion" AND abs:"embedding"', "graph-embeddings", "method"),
    ('cat:cs.LG AND (abs:"TransE" OR abs:"TransH")', "graph-embeddings", "method"),
    ('cat:cs.CL AND abs:"entity embedding" AND abs:"graph"', "graph-embeddings", "method"),
    ('cat:cs.CL AND abs:"knowledge graph" AND abs:"LLM" AND abs:"retrieval"', "graphrag", "method"),
    ('cat:cs.CL AND abs:"graph-augmented"', "graphrag", "method"),
    ('all:"hierarchical graphrag"', "graphrag", "method"),
    ('cat:cs.CL AND abs:"entity-centric" AND abs:"retrieval"', "graphrag", "method"),
    ('cat:cs.CL AND abs:"graph" AND abs:"chunking" AND abs:"retrieval"', "graphrag", "method"),
    ('cat:cs.LG AND abs:"graph attention"', "graph-neural-networks", "method"),
    ('cat:cs.LG AND abs:"graph convolution"', "graph-neural-networks", "method"),
    ('cat:cs.LG AND abs:"hypergraph neural"', "graph-neural-networks", "method"),
    ('cat:cs.LG AND abs:"graph unlearning"', "graph-neural-networks", "method"),
    ('cat:cs.LG AND abs:"equivariant graph"', "graph-neural-networks", "theory"),
    ('cat:cs.AI AND abs:"knowledge graph" AND abs:"LLM" AND abs:"reasoning"', "knowledge-graphs", "method"),
    ('cat:cs.AI AND abs:"knowledge graph" AND abs:"alignment"', "knowledge-graphs", "method"),
    ('cat:cs.CL AND abs:"multimodal knowledge graph"', "knowledge-graphs", "method"),
    ('cat:cs.AI AND abs:"commonsense knowledge graph"', "knowledge-graphs", "method"),
    ('cat:cs.AI AND abs:"knowledge graph" AND abs:"fusion"', "knowledge-graphs", "method"),
    ('cat:cs.DS AND abs:"subgraph isomorphism"', "graph-theory", "theory"),
    ('cat:math.CO AND abs:"graph" AND abs:"embedding" AND abs:"topological"', "graph-theory", "theory"),
    ('cat:cs.SI AND abs:"label propagation"', "community-detection", "method"),
    ('cat:cs.LG AND abs:"graph partition" AND abs:"community"', "community-detection", "method"),
    ('cat:cs.SI AND abs:"graph neural network" AND abs:"community"', "community-detection", "method"),
    ('cat:cs.CR AND abs:"knowledge graph" AND abs:"security"', "graph-security", "application"),
    ('cat:cs.CR AND abs:"graph" AND abs:"intrusion"', "graph-security", "application"),
    ('cat:cs.LG AND abs:"graph" AND abs:"malware"', "graph-security", "application"),
    ('cat:cs.CR AND abs:"dependency graph" AND abs:"supply chain"', "graph-security", "application"),
    ('cat:cs.LG AND abs:"continuous-time graph"', "temporal-graphs", "method"),
    ('cat:cs.SI AND abs:"link prediction" AND abs:"temporal"', "temporal-graphs", "method"),
    ('cat:cs.AI AND abs:"event knowledge graph"', "temporal-graphs", "method"),
    ('cat:cs.LG AND abs:"graph neural network" AND abs:"protein"', "graph-applications", "application"),
    ('cat:cs.LG AND abs:"graph neural network" AND abs:"traffic"', "graph-applications", "application"),
    ('cat:cs.LG AND abs:"graph" AND abs:"materials" AND abs:"machine learning"', "graph-applications", "application"),
    ('cat:physics.soc-ph AND abs:"temporal network"', "network-science", "mechanism"),
    ('cat:cs.SI AND abs:"higher-order network"', "network-science", "method"),
    ('cat:cs.SI AND abs:"hypergraph" AND abs:"learning"', "network-science", "method"),
    ('cat:cs.SI AND abs:"link prediction" AND abs:"network"', "network-science", "method"),
    ('cat:cs.DB AND abs:"graph data management"', "graph-databases", "systems"),
    ('cat:cs.DB AND abs:"subgraph query" AND abs:"index"', "graph-databases", "systems"),
    ('cat:cs.DB AND abs:"graph database" AND abs:"survey"', "graph-databases", "review"),
    ('cat:cs.DB AND abs:"graph" AND abs:"indexing" AND abs:"query"', "graph-databases", "systems"),
    ('cat:cs.DB AND abs:"graph" AND abs:"benchmark" AND abs:"database"', "graph-databases", "evaluation"),
    # --- gap filling: graph-analytics + distributed-graphs thin cells ---
    ('cat:cs.DB AND abs:"graph analytics" AND abs:"application"', "graph-analytics", "application"),
    ('cat:cs.SI AND abs:"graph analytics" AND abs:"social"', "graph-analytics", "application"),
    ('cat:cs.DB AND abs:"graph analytics" AND abs:"industry"', "graph-analytics", "application"),
    ('cat:cs.DB AND abs:"graph analytics" AND abs:"tool"', "graph-analytics", "development"),
    ('cat:cs.DB AND abs:"graph analytics" AND abs:"open-source"', "graph-analytics", "development"),
    ('cat:cs.DB AND abs:"graph processing" AND abs:"framework"', "distributed-graphs", "development"),
    ('cat:cs.DC AND abs:"graph" AND abs:"distributed" AND abs:"application"', "distributed-graphs", "application"),
    ('cat:cs.DB AND abs:"graph database" AND abs:"cloud"', "distributed-graphs", "application"),
    ('cat:cs.DB AND abs:"graph" AND abs:"partitioning" AND abs:"load balance"', "distributed-graphs", "method"),
    ('cat:cs.DB AND abs:"graph" AND abs:"placement" AND abs:"distributed"', "distributed-graphs", "method"),
    # --- final two gap cells (forced subcategory) ---
    ('cat:cs.DB AND abs:"survey" AND abs:"graph query"', "graph-query-languages", "review", "review"),
    ('cat:cs.DB AND abs:"survey" AND (abs:"Cypher" OR abs:"SPARQL" OR abs:"GQL")', "graph-query-languages", "review", "review"),
    ('cat:cs.DB AND abs:"benchmark" AND abs:"graph processing"', "distributed-graphs", "evaluation", "evaluation"),
    ('cat:cs.DB AND abs:"graph" AND abs:"evaluation" AND abs:"distributed" AND abs:"system"', "distributed-graphs", "evaluation", "evaluation"),
    ('cat:cs.DB AND abs:"survey" AND (abs:"graph" OR abs:"RDF" OR abs:"knowledge graph")', "graph-query-languages", "review", "review"),
]

# Subcategory keyword rules, applied in order. First match wins.
# Each rule: (subcategory, keywords, title_only?) — title_only restricts
# matching to the paper title (for strong signals like "survey").
SUBCATEGORY_RULES = [
    ("review", ["survey", "systematic review", "state-of-the-art", "sota", "overview of"], True),
    ("review", ["a survey of", "review of", "bibliographic review"], False),
    ("theory", ["expressivity", "expressiveness", "theoretical", "complexity of", "bounds", "fundamental limits", "axiomat", "computational complexity", "approximation guarantees"], False),
    ("application", ["application to", "application of", "case study", "real-world", "in practice", "production", "clinical", "medical", "fraud detection", "drug discovery", "recommender", "supply chain", "bioinformatics", "proteomics", "genomics", "diagnosis", "osint", "cybersecurity", "deployment"], False),
    ("development", ["open-source", "library", "toolkit", "implementation of", "software package", "benchmarking tool", "api for", "python library"], False),
    ("mechanism", ["interpretab", "explainab", "understanding why", "analysis of", "inner workings", "attention analysis", "probing", "mechanism", "why graph"], False),
    ("systems", ["system", "engine", "platform", "infrastructure", "architecture", "pipeline", "distributed", "scalable", "indexing", "storage", "gpu", "parallel"], False),
    ("evaluation", ["benchmark", "empirical study", "empirical comparison", "experimental evaluation", "evaluating", "comparative analysis", "dataset"], False),
]

SUBCATEGORY_FALLBACK = "method"


def classify_subcategory(title, abstract):
    """Assign a subcategory using keyword rules against title + abstract."""
    t_lower = title.lower()
    text = f"{title} {abstract}".lower()
    for subcat, keywords, title_only in SUBCATEGORY_RULES:
        haystack = t_lower if title_only else text
        for kw in keywords:
            if kw in haystack:
                return subcat
    return SUBCATEGORY_FALLBACK


def load_existing_papers(yaml_path):
    if not yaml_path.exists():
        return {}, []
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f) or {}
    papers = data.get("papers", [])
    by_id = {}
    titles_lower = []
    for p in papers:
        url = p.get("url", "")
        match = ARXIV_ID_PATTERN.search(url)
        if match:
            by_id[match.group(1)] = p
        titles_lower.append(p.get("title", "").lower().strip())
    return by_id, titles_lower


def search_arxiv(query, months, start=0, max_results=100, max_retries=4):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    cutoff = now - timedelta(days=months * 30)
    date_start = cutoff.strftime("%Y%m%d0000")
    date_end = now.strftime("%Y%m%d") + "2359"

    full_query = f"({query}) AND submittedDate:[{date_start} TO {date_end}]"
    try:
        resp = None
        for attempt in range(max_retries):
            resp = requests.get(
                ARXIV_SEARCH_API.format(
                    requests.utils.quote(full_query), start, max_results
                ),
                timeout=30,
            )
            if resp.status_code == 429:
                wait = 8 * (attempt + 1)
                print(f"    rate-limited (429), waiting {wait}s...", flush=True)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            break
        if resp is None:
            return []
        if resp.status_code != 200:
            print(f"  WARNING: arXiv returned HTTP {resp.status_code}", flush=True)
            return []
        entries = []
        root = resp.text
        for match in re.finditer(r"<entry>(.*?)</entry>", root, re.DOTALL):
            entry_xml = match.group(1)
            entry = {}
            title_m = re.search(r"<title>(.*?)</title>", entry_xml, re.DOTALL)
            if title_m:
                entry["title"] = re.sub(r"\s+", " ", title_m.group(1).strip())
            id_m = re.search(r"<id>(.*?)</id>", entry_xml)
            if id_m:
                entry["url"] = id_m.group(1).strip().replace("http://", "https://")
            published_m = re.search(r"<published>(.*?)</published>", entry_xml)
            if published_m:
                entry["date"] = published_m.group(1).strip()[:7]
            summary_m = re.search(r"<summary>(.*?)</summary>", entry_xml, re.DOTALL)
            if summary_m:
                entry["abstract"] = re.sub(r"\s+", " ", summary_m.group(1).strip())
            authors_m = re.findall(r"<name>(.*?)</name>", entry_xml)
            if authors_m:
                entry["authors"] = [a.strip() for a in authors_m][:3]
            if entry.get("title") and entry.get("url"):
                entries.append(entry)
        return entries
    except Exception as e:
        print(f"  WARNING: arXiv search error: {e}", flush=True)
        return []


def format_yaml_entry(entry, category, subcategory):
    title = entry["title"].replace('"', '\\"')
    authors = ", ".join(entry.get("authors", [])[:3])
    lines = [
        f'  - title: "{title}"',
        f'    date: "{entry.get("date", "")}"',
        f'    url: "{entry.get("url", "")}"',
        f"    category: {category}",
        f"    subcategory: {subcategory}",
        f"    authors: [{authors}]",
    ]
    if entry.get("abstract"):
        abstract = entry["abstract"][:200].replace('"', '\\"')
        lines.append(f'    abstract: "{abstract}..."')
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Discover graph research papers from arXiv"
    )
    parser.add_argument(
        "--months",
        type=int,
        default=3,
        help="Search papers from the last N months (default: 3)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without creating anything"
    )
    parser.add_argument(
        "--create-pr", action="store_true", help="Create a GitHub PR with new papers"
    )
    parser.add_argument(
        "--sleep", type=float, default=2.0, help="Seconds between queries"
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Max results per arXiv query (default: 100)",
    )
    parser.add_argument(
        "--from",
        dest="from_idx",
        type=int,
        default=0,
        help="Start at query index (0-based, inclusive)",
    )
    parser.add_argument(
        "--to",
        dest="to_idx",
        type=int,
        default=None,
        help="Stop at query index (0-based, inclusive)",
    )
    args = parser.parse_args()

    yaml_path = Path(__file__).resolve().parent.parent.parent / "papers.yaml"
    by_id, titles_lower = load_existing_papers(yaml_path)

    print(f"Loaded {len(by_id)} existing papers from papers.yaml", flush=True)
    print(
        f"Searching arXiv ({len(QUERIES)} queries) for papers from the last {args.months} month(s)...",
        flush=True,
    )

    all_new = []
    CHECKPOINT_EVERY = 10
    to_idx = args.to_idx if args.to_idx is not None else len(QUERIES) - 1
    for qi, qdef in enumerate(QUERIES[args.from_idx:to_idx + 1], start=args.from_idx):
        if len(qdef) == 4:
            query, category, hint, force_sub = qdef
        else:
            query, category, hint = qdef
            force_sub = None
        print(f"Query {qi + 1}/{len(QUERIES)} [{category}] {query[:70]}", flush=True)
        entries = search_arxiv(query, args.months, max_results=args.max_results)
        for entry in entries:
            arxiv_id_match = ARXIV_ID_PATTERN.search(entry.get("url", ""))
            arxiv_id = arxiv_id_match.group(1) if arxiv_id_match else None

            if arxiv_id and arxiv_id in by_id:
                continue

            title_lower = entry.get("title", "").lower().strip()
            if any(title_lower == t for t in titles_lower):
                continue

            if arxiv_id and any(e.get("url", "") == entry["url"] for e in all_new):
                continue

            entry["category"] = category
            entry["subcategory"] = force_sub or classify_subcategory(
                entry.get("title", ""), entry.get("abstract", "")
            )
            all_new.append(entry)
            by_id[arxiv_id] = entry
            titles_lower.append(title_lower)

        # Incremental checkpoint so partial runs are never lost
        if not args.dry_run and all_new and (qi + 1) % CHECKPOINT_EVERY == 0:
            append_papers(yaml_path, all_new)
            print(f"  [checkpoint] saved {len(all_new)} papers so far", flush=True)
            all_new = []
            by_id, titles_lower = load_existing_papers(yaml_path)

        time.sleep(args.sleep)

    print(
        f"\nFound {len(all_new)} new papers ({len(by_id)} already in list)", flush=True
    )

    if not all_new:
        print("No new papers to add.", flush=True)
        return

    print("\n--- New Papers (first 10) ---", flush=True)
    for entry in all_new[:10]:
        print(format_yaml_entry(entry, entry["category"], entry["subcategory"]), flush=True)
        print(flush=True)
    print(f"... and {max(0, len(all_new) - 10)} more", flush=True)

    if args.dry_run:
        print("\nDry run complete — no files modified", flush=True)
        return

    if args.create_pr:
        branch_name = f"add-new-papers-{datetime.now().strftime('%Y%m%d')}"
        print(f"\nCreating branch '{branch_name}' and PR...", flush=True)
        try:
            subprocess.run(
                ["git", "checkout", "-b", branch_name], check=True, cwd=yaml_path.parent
            )
            append_papers(yaml_path, all_new)
            subprocess.run(["git", "add", "papers.yaml"], check=True, cwd=yaml_path.parent)
            subprocess.run(
                ["git", "commit", "-m", f"Add {len(all_new)} new papers from arXiv discovery"],
                check=True,
                cwd=yaml_path.parent,
            )
            subprocess.run(
                ["git", "push", "origin", branch_name], check=True, cwd=yaml_path.parent
            )
            subprocess.run(
                [
                    "gh", "pr", "create",
                    "--title", f"Add {len(all_new)} new papers from arXiv discovery",
                    "--body", "Automatically discovered papers.\n\n**Please review taxonomy assignments.**",
                ],
                check=True,
                cwd=yaml_path.parent,
            )
            print("PR created successfully!", flush=True)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to create PR: {e}", flush=True)
            sys.exit(1)
    else:
        append_papers(yaml_path, all_new)
        print(f"\nAppended {len(all_new)} papers to papers.yaml", flush=True)
        print(
            "\nNext: run scripts/analysis/generate_analysis.py and scripts/generate_readme.py",
            flush=True,
        )


def append_papers(yaml_path, new_papers):
    """Append new papers to papers.yaml in stable format."""
    if yaml_path.exists():
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}
    papers = data.get("papers", [])
    for entry in new_papers:
        papers.append(
            {
                "title": entry.get("title", ""),
                "date": entry.get("date", ""),
                "url": entry.get("url", ""),
                "category": entry.get("category", ""),
                "subcategory": entry.get("subcategory", ""),
                "authors": entry.get("authors", []),
                "abstract": entry.get("abstract", ""),
            }
        )
    data["papers"] = papers
    with open(yaml_path, "w") as f:
        yaml.dump(
            data, f, default_flow_style=False, allow_unicode=True, sort_keys=False
        )


if __name__ == "__main__":
    main()
