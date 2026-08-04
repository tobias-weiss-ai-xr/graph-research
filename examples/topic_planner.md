# Topic Planner — Example Workflow

This guide walks through turning the corpus into a graphwiz.ai article.

## 1. See what's hot

```bash
python3 tools/trend_scanner.py --months 12
```

Example output (illustrative):

```
🔥 TOP KEYWORD BURSTS
GraphRAG        12 recent / 30 total  burst=8.2   ################
graph foundation  9 recent / 15 total  burst=6.4   #############
temporal         15 recent / 45 total  burst=4.1   ########
```

## 2. Get ranked topics

```bash
python3 tools/topic_planner.py --top 10
```

Writes `docs/topics/ARTICLE_TOPICS.md` with 10 evidence-ranked topics.

## 3. Build a brief

```bash
python3 tools/brief_generator.py "GraphRAG at scale" --papers 5
```

Output:

```
📝 ARTICLE BRIEF: GraphRAG at scale
   Category: Graph Applications
   Angle: Evidence-based guide to graphrag at scale — synthesize the 5 most
          relevant papers into practical guidance for graphwiz.ai readers.

Title candidates:
  - Graphrag at Scale: What the Research Says
  - Graphrag at Scale in Production: Lessons from the Literature
  ...

Key papers:
  [2026-02] LazyGraphRAG: ...           https://arxiv.org/abs/...
  [2025-11] GraphRAG cost models ...    https://arxiv.org/abs/...
```

## 4. Write & publish

Follow the `graphwiz-reporter` pipeline in the
[next-graphwiz-ai](https://github.com/tobias-weiss-ai-xr/next-graphwiz-ai)
repo: research → write (800–1500 words, British English, GFM) → save to
`content/graphs/{slug}.md` → validate → commit → push.

## 5. Keep the corpus fresh

Weekly CI runs `fetch_new_papers.py --months 1 --create-pr` and opens a PR
with new papers. Review the taxonomy assignments, merge, and the topic list
regenerates automatically.
