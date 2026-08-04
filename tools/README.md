# Graph Research Tools — API Reference

Tools that turn the research corpus into graphwiz.ai article plans.

| Tool | Purpose |
|------|---------|
| `topic_planner.py` | Evidence-ranked article topics (density × velocity) |
| `trend_scanner.py` | Emerging trend detection (keyword bursts, growing cells) |
| `brief_generator.py` | Full article briefs (title, outline, key papers) |

All tools read `papers.yaml` at the repository root. Run them from anywhere —
they resolve paths relative to the repo.

---

## 1. Topic Planner (`topic_planner.py`)

Ranks article topics by corpus density × 12-month research velocity and writes
`docs/topics/ARTICLE_TOPICS.md`.

```bash
python3 tools/topic_planner.py                # top 10 topics
python3 tools/topic_planner.py --top 20
python3 tools/topic_planner.py --category graphrag
python3 tools/topic_planner.py --json         # machine-readable output
```

**How ranking works:**
- **Density:** number of papers in the category
- **Velocity:** share of category papers published in the last 12 months
- **Focus:** most frequent research keyword in recent category papers
- **Angle:** editorial priority per category (e.g. GraphRAG → deployment costs)

**Customisation:** edit `TOPIC_TEMPLATES`, `ANGLE_BANK`, `PRIORITY_ANGLE` in the
script to shape the editorial voice.

---

## 2. Trend Scanner (`trend_scanner.py`)

Detects research trends via keyword-burst analysis: a keyword is a *burst* if
its share of recent papers exceeds its share of the whole corpus.

```bash
python3 tools/trend_scanner.py --months 6
python3 tools/trend_scanner.py --months 12 --json
```

**Output:**
- 🔥 Top keyword bursts (recent share vs corpus share)
- 📈 Fastest-growing taxonomy cells (share of papers in look-back window)

**Customisation:** extend `TREND_KEYWORDS` in the script with domain terms.

---

## 3. Brief Generator (`brief_generator.py`)

Builds a write-ready brief for a topic by matching corpus papers
(keyword overlap + phrase bonus + recency).

```bash
python3 tools/brief_generator.py "GraphRAG at scale" --papers 5
python3 tools/brief_generator.py "temporal knowledge graphs" --json
```

**Output:** title candidates, angle, 7-section outline, key papers
(title/date/url/category), open questions.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `papers.yaml not found` | Run from repo root or `cd ~/git/graph-research` |
| Empty results | Corpus not fetched yet — run `scripts/fetch/fetch_new_papers.py` |
| Wrong categories in output | Taxonomy assignments are auto-tagged; refine in `papers.yaml` |

## Configuration

All tools are zero-config — the only dependency is `pyyaml`:

```bash
pip install -r requirements.txt
```
