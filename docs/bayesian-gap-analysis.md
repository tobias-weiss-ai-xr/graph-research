# Bayesian Gap Analysis of the Graph-Research Corpus

Corpus: 26,496 papers · model: hierarchical empirical-Bayes Gamma prior (a=1.35, b=1.37) on cell rate ratios · gap := P(rho < 0.5)

## Method

For every taxonomy cell (category x subcategory) we compare the observed paper count n with the count expected under an independence baseline e = category_total * corpus_wide_subcategory_share. The rate ratio rho = lambda/e gets an empirical-Bayes Gamma prior fitted across all 200 cells; the posterior is Gamma(a+n, b+e). This shrinks small cells toward the corpus structure, so a single paper in a small category no longer masquerades as a trend, and a thin cell in a huge category is recognised as a true anomaly. Category growth is a Poisson rate-ratio posterior (Gamma(0.5, 0.5) prior, 20k Monte-Carlo draws); saturation uses a Beta-Binomial posterior. All code: `scripts/analysis/bayesian_gap_analysis.py`.

## Headline results

- **Taxonomy saturation** 177/200 -> posterior mean 88.1%, 95% CI [83.3%, 92.2%]
- **20 cells** have >= 95% posterior probability of being true gaps (rho < 0.5)

## Top 15 true gaps (highest P(gap))

| Cell | n | Expected | Post. rho | 95% CI | P(gap) |
| --- | --: | --: | --: | --- | ---: |
| graph-applications/method | 141 | 422.9 | 0.34 | 0.28-0.39 | 1.000 |
| graph-construction/theory | 30 | 164.2 | 0.19 | 0.13-0.26 | 1.000 |
| graph-theory/application | 86 | 343.5 | 0.25 | 0.2-0.31 | 1.000 |
| graph-theory/evaluation | 11 | 102.4 | 0.12 | 0.06-0.19 | 1.000 |
| graph-algorithms/evaluation | 26 | 91.4 | 0.29 | 0.19-0.41 | 0.999 |
| knowledge-graphs/theory | 132 | 342.6 | 0.39 | 0.32-0.46 | 0.999 |
| graph-theory/mechanism | 40 | 126.4 | 0.32 | 0.23-0.43 | 0.999 |
| graph-applications/survey | 0 | 13.8 | 0.09 | 0.01-0.29 | 0.999 |
| network-science/survey | 0 | 13.8 | 0.09 | 0.01-0.29 | 0.999 |
| distributed-graphs/evaluation | 14 | 55.9 | 0.27 | 0.15-0.42 | 0.998 |
| temporal-graphs/survey | 0 | 9.9 | 0.12 | 0.01-0.39 | 0.992 |
| graph-security/evaluation | 48 | 134.2 | 0.36 | 0.27-0.47 | 0.992 |
| graph-theory/survey | 1 | 13.7 | 0.16 | 0.02-0.41 | 0.992 |
| graph-machine-learning/survey | 0 | 9.3 | 0.13 | 0.01-0.41 | 0.990 |
| graph-construction/survey | 0 | 8.3 | 0.14 | 0.01-0.45 | 0.984 |

## Top 10 hot cells (P(rho > 2) — strongest over-representation)

| Cell | n | Expected | Post. rho | 95% CI | P(hot) |
| --- | --: | --: | --: | --- | ---: |
| community-detection/survey | 50 | 12.2 | 3.8 | 2.83-4.9 | 1.000 |
| graph-theory/theory | 646 | 270.2 | 2.38 | 2.2-2.57 | 1.000 |
| ontology/survey | 46 | 12.9 | 3.32 | 2.45-4.34 | 0.999 |
| graph-construction/evaluation | 158 | 62.3 | 2.5 | 2.13-2.91 | 0.997 |
| graph-query-languages/evaluation | 94 | 38.2 | 2.41 | 1.95-2.92 | 0.958 |
| graph-visualization/survey | 18 | 5.9 | 2.66 | 1.61-3.97 | 0.868 |
| graph-machine-learning/evaluation | 153 | 70.1 | 2.16 | 1.83-2.51 | 0.819 |
| graph-applications/application | 709 | 346.4 | 2.04 | 1.9-2.2 | 0.709 |
| graph-databases/development | 36 | 17.1 | 2.02 | 1.42-2.71 | 0.499 |
| graph-construction/development | 37 | 19.0 | 1.88 | 1.33-2.52 | 0.328 |

## Category growth with uncertainty

| Category | Last 12m | Prior 12m | Post. ratio | 95% CI | P(growing) |
| --- | --: | --: | --: | --- | ---: |
| Graph Query Languages | 290 | 114 | 2.56 | 2.06-3 | 1.000 |
| Graphrag | 829 | 445 | 1.87 | 1.66-2 | 1.000 |
| Graph Analytics | 314 | 170 | 1.86 | 1.54-2 | 1.000 |
| Ontology | 593 | 362 | 1.64 | 1.44-2 | 1.000 |
| Graph Databases | 344 | 210 | 1.65 | 1.38-2 | 1.000 |
| Graph Neural Networks | 929 | 623 | 1.49 | 1.34-2 | 1.000 |
| Graph Algorithms | 450 | 324 | 1.39 | 1.21-2 | 1.000 |
| Knowledge Graphs | 634 | 492 | 1.29 | 1.15-1 | 1.000 |
| Graph Construction | 245 | 197 | 1.25 | 1.03-2 | 0.989 |
| Network Science | 371 | 331 | 1.12 | 0.97-1 | 0.934 |
| Graph Visualization | 225 | 221 | 1.02 | 0.84-1 | 0.577 |
| Graph Applications | 400 | 374 | 1.07 | 0.93-1 | 0.824 |
| Graph Embeddings | 319 | 309 | 1.04 | 0.88-1 | 0.659 |
| Graph Security | 584 | 670 | 0.87 | 0.78-1 | 0.008 |
| Graph Theory | 356 | 400 | 0.89 | 0.77-1 | 0.055 |
| Semantic Web | 215 | 273 | 0.79 | 0.66-1 | 0.004 |
| Graph Machine Learning | 199 | 286 | 0.7 | 0.58-1 | 0.000 |
| Distributed Graphs | 166 | 259 | 0.64 | 0.53-1 | 0.000 |
| Community Detection | 239 | 413 | 0.58 | 0.49-1 | 0.000 |
| Temporal Graphs | 198 | 374 | 0.53 | 0.45-1 | 0.000 |

## GQL case study

| Cell | n | Expected | Post. rho | 95% CI | P(gap) |
| --- | --: | --: | --: | --- | ---: |
| experiment | 0 | 0.2 | 0.86 | 0.05-2.79 | 0.392 |
| survey | 0 | 5.1 | 0.21 | 0.01-0.68 | 0.927 |
| development | 16 | 11.7 | 1.33 | 0.78-2.02 | 0.000 |
| review | 15 | 15.0 | 1.0 | 0.58-1.54 | 0.008 |
| evaluation | 94 | 38.2 | 2.41 | 1.95-2.92 | 0.000 |
| mechanism | 33 | 47.1 | 0.71 | 0.49-0.96 | 0.031 |
| systems | 80 | 81.5 | 0.98 | 0.78-1.21 | 0.000 |
| theory | 78 | 100.7 | 0.78 | 0.62-0.96 | 0.000 |
| application | 96 | 128.1 | 0.75 | 0.61-0.91 | 0.000 |
| method | 172 | 156.4 | 1.1 | 0.94-1.27 | 0.000 |

## Reading the results — the naive narrative, revised

**The GQL 'review gap' is not an anomaly.** Naively, 15 review papers against 584 total looks like the category's sharpest white space. Under shrinkage, the expected count for a GQL review cell is 15.0 — the observed 15 sit exactly on the corpus pattern (posterior rho = 1.0, 95% CI 0.58-1.54, P(gap) = 0.0076). Thin review cells are a *global* property of young fields, not a GQL anomaly; none of the GQL cells ranks in the global top-15 gaps (count: 0).

**What GQL actually looks like:** a benchmarked field. Its evaluation cell is one of the most over-represented in the corpus (n=94 vs expected 38.2, rho = 2.41, P(hot) = 0.9582), its method cell is slightly above expectation (rho 1.10), and its only notable deficit is the survey cell (0/5.1, P(gap) = 0.9272) — the definitive practitioner survey genuinely does not exist yet, but that is the survey desert of a young field speaking, not a GQL-specific pathology.

**Where the corpus really under-delivers** (posterior P(rho < 0.5) >= 0.95, expected >= 3): applications/method (141/422.9), graph-construction/theory (30/164.2), graph-theory/application (86/343.5), graph-theory/evaluation (11/102.4), knowledge-graphs/theory (132/342.6), graph-algorithms/evaluation (26/91.4), graph-theory/mechanism (40/126.4), graph-security/evaluation (48/134.2), distributed-graphs/evaluation (14/55.9) — plus five *empty* survey cells (graph-applications, network-science, temporal-graphs, graph-machine-learning, graph-construction). These are the cells where new work moves the whole corpus, because the deficit is measured relative to each category's own size and the corpus-wide subcategory structure.

**Growth is Bayesian-robust:** the GQL acceleration is real with posterior probability ~1.000 (rate ratio 2.56, 95% CI 2.06-3.0); GraphRAG (1.87) and Graph Analytics (1.86) follow. Temporal Graphs (0.53) and Community Detection (0.58) are in significant decline (P(growing) = 0.000).
