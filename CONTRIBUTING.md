# Contributing to graph-research

Thanks for helping build the evidence base for graphwiz.ai!

## Ways to Contribute

### 1. Add Papers

1. Fork the repository.
2. Edit `papers.yaml` — append entries in this format:

```yaml
- title: "A great graph paper"
  date: "2026-07"
  url: https://arxiv.org/abs/2607.12345
  category: knowledge-graphs
  subcategory: method
  authors: []
  abstract: "Short abstract..."
```

3. Open a PR. Use the `paper_submission` issue template for guidance.

### Taxonomy Reference

**Categories (20):** `knowledge-graphs`, `graphrag`, `graph-databases`,
`graph-query-languages`, `graph-algorithms`, `graph-neural-networks`,
`graph-theory`, `network-science`, `graph-embeddings`, `graph-construction`,
`semantic-web`, `ontology`, `graph-analytics`, `community-detection`,
`graph-visualization`, `graph-machine-learning`, `temporal-graphs`,
`distributed-graphs`, `graph-security`, `graph-applications`

**Subcategories (8):** `theory`, `mechanism`, `method`, `application`,
`development`, `systems`, `evaluation`, `review`

### 2. Improve Tools / Scripts

- Scripts and tools are Python 3.10+ with type hints and logging.
- Run `python3 scripts/validate_papers.py` and the relevant tool before opening a PR.
- Keep the fetch script's query list taxonomy-aware — each query carries a
  `(query, category, subcategory-hint)` tuple.

### 3. Improve Documentation

- `docs/research/` — research docs (taxonomy, trends, literature review)
- `docs/topics/` — generated article topics (regenerate via topic planner)
- `tools/README.md` — tool API reference

## Development Workflow

```bash
pip install -r requirements.txt

# fetch new papers (rate-limit safe)
python3 scripts/fetch/fetch_new_papers.py --months 3 --sleep 3

# validate + analyze + visualize + regenerate README
python3 scripts/validate_papers.py
python3 scripts/analysis/generate_analysis.py
python3 scripts/visualize_statistics.py
python3 scripts/generate_readme.py

# regenerate article topics
python3 tools/topic_planner.py --top 10
```

## Pull Request Checklist

- [ ] `papers.yaml` passes `scripts/validate_papers.py`
- [ ] README is regenerated (`scripts/generate_readme.py`) if statistics changed
- [ ] New tools/scripts have `--help` and type hints
- [ ] CHANGELOG.md updated

## Code of Conduct

Be respectful, evidence-first, and kind. This is a research corpus — claims
should be traceable to papers.

## License

Tools: MIT. Corpus and generated research documents: proprietary (see LICENSE).
