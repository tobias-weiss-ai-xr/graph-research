# Graph Research — Documentation Index

## Research

| Document | Purpose |
|----------|---------|
| [`research/taxonomy.md`](research/taxonomy.md) | The 20×8 taxonomy definition |
| [`research/literature_review.md`](research/literature_review.md) | Synthesis of the corpus |
| [`research/graph_trends_2026.md`](research/graph_trends_2026.md) | Trend analysis for article planning |
| [`research/gql_investigation.md`](research/gql_investigation.md) | Deep-dive on the GQL standard & graph query languages |

## Topics (Generated)

| Document | Purpose |
|----------|---------|
| [`topics/ARTICLE_TOPICS.md`](topics/ARTICLE_TOPICS.md) | Evidence-ranked article topics for graphwiz.ai |

## Data Files

| File | Description |
|------|-------------|
| `../papers.yaml` | Source of truth (paper metadata) |
| `../papers.json` | JSON export of all papers |
| `../statistics.json` | Machine-readable statistics |

## Regenerating

```bash
python3 scripts/analysis/generate_analysis.py   # statistics.json + papers.json
python3 scripts/visualize_statistics.py          # PNG charts
python3 tools/trend_scanner.py --months 6        # trend report
python3 tools/topic_planner.py --top 10          # ARTICLE_TOPICS.md
python3 scripts/generate_readme.py               # README.md
```
