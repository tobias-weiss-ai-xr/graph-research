# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-04

### Added

#### Research Corpus
- Analysis of graph research papers across 20 graph disciplines
- 20x8 taxonomy (category × research aspect) with saturation tracking
- Complete statistics and gap analysis (`statistics.json`)
- JSON export of all papers (`papers.json`)
- Visualization suite (4 charts, D3 data)

#### Research Pipeline
- **arXiv discovery** (`scripts/fetch/fetch_new_papers.py`)
  - 160+ taxonomy-aware queries
  - Auto-classification into categories and subcategories
  - 429 rate-limit retry with backoff
  - Incremental checkpointing (partial runs are never lost)
  - GitHub PR creation mode for weekly CI discovery

- **Analysis** (`scripts/analysis/generate_analysis.py`)
  - Category/subcategory/cell/year statistics
  - 12-month emerging-theme detection
  - D3.js visualization data

- **Validation** (`scripts/validate_papers.py`) — strict taxonomy/URL/date checks
- **README generation** (`scripts/generate_readme.py`) — self-updating README
- **Visualizations** (`scripts/visualize_statistics.py`) — PNG charts

#### Article Planning Tools (graphwiz.ai)
- **Topic Planner** (`tools/topic_planner.py`)
  - Evidence-ranked article topics (density × velocity)
  - Per-category editorial templates
  - Writes `docs/topics/ARTICLE_TOPICS.md`

- **Trend Scanner** (`tools/trend_scanner.py`)
  - Keyword burst detection over the last N months
  - Fastest-growing taxonomy cells

- **Brief Generator** (`tools/brief_generator.py`)
  - Title candidates, outline, key papers, open questions

#### Documentation
- Taxonomy definition (`docs/research/taxonomy.md`)
- Trend report (`docs/research/graph_trends_2026.md`)
- Literature review (`docs/research/literature_review.md`)
- Article topic list (`docs/topics/ARTICLE_TOPICS.md`)
- Tool documentation (`tools/README.md`)
- Examples

#### CI/CD
- Validation workflow (validate papers + README freshness)
- Weekly arXiv discovery with auto-PR

---

## [0.1.0] - 2026-08-04

### Added
- Repository scaffold mirroring `learning-research` structure
- Initial 20-category graph taxonomy
- Fetch, analysis, validation and visualization scripts
- Article planning tools (topic planner, trend scanner, brief generator)
