# Repository Analysis

## Overview

This repository is organized as a research project investigating Single-Source Shortest Paths (SSSP) algorithms, with the goal of designing a novel algorithm that achieves asymptotically fewer operations than the current best known bound of O(m + n log n) on general weighted directed graphs.

## Repository Structure

```
.
├── .archivara/               # Research tooling (Semantic Scholar API, ConceptEvolve)
│   ├── semantic_scholar.py   # Academic paper discovery via Semantic Scholar API
│   ├── concept_evolve.py     # Cross-domain concept discovery sub-agent tool
│   └── logs/                 # Log files from tool runs
├── .git/                     # Git version control
├── .gitattributes            # Git LFS and attribute configuration
├── .gitignore                # Ignore patterns
├── README.md                 # Project readme
├── TASK_researcher_attempt_1.md  # Task specification for the researcher agent
├── research_rubric.json      # Research plan rubric tracking progress across 5 phases, 26 items
├── sources.bib               # BibTeX bibliography (maintained throughout research)
├── figures/                  # Output directory for publication-quality figures (PNG + PDF)
├── results/                  # Output directory for experimental data (JSON)
│   └── concept_evolve/       # ConceptEvolve outputs
├── src/                      # Source code (structured as software project)
│   ├── baselines/            # Baseline algorithm implementations (Dijkstra, Bellman-Ford)
│   ├── graphs/               # Graph generation and I/O
│   ├── benchmark/            # Benchmarking harness with proper methodology
│   ├── novel/                # Novel algorithm implementation
│   ├── sota/                 # State-of-the-art reference implementations (Duan et al. 2025)
│   └── datastructures/       # Specialized data structures (priority queues, etc.)
```

## Module Descriptions

### `.archivara/semantic_scholar.py`
**Purpose:** Academic paper discovery and citation management via the Semantic Scholar API.

**Commands:**
- `search "query" --limit N` — Keyword search for papers; returns titles, authors, years, citation counts, abstracts
- `citations <paperId> --limit N` — Find papers that cite a given paper (forward citation traversal)
- `references <paperId> --limit N` — Find papers referenced by a given paper (backward citation traversal)
- `recommend <paperId1> <paperId2> ...` — Cross-domain paper recommendations based on multiple seed papers
- `bibtex <paperId> >> sources.bib` — Generate and append a BibTeX entry for a paper

**Inter-module dependencies:** None (standalone tool). Outputs feed into `sources.bib` and inform `literature_review.md`.

**Usage for literature search:**
1. Search core topic to find foundational papers
2. Use `citations` and `references` for citation graph traversal
3. Use `recommend` with 2-3 key paper IDs to surface cross-domain connections
4. Append all discovered papers to `sources.bib` via `bibtex`

### `.archivara/concept_evolve.py`
**Purpose:** Cross-domain concept discovery using the Concept-Guided Evolutionary Discovery framework (2026). Spawns Claude sub-agents to generate structured concept connections.

**Commands:**
- `evolve "research topic"` — Full pipeline: concept externalization (8-12 concept cards), semantic bridge graph, proxy introspection, anomaly injection. Outputs to `results/concept_evolve/` (concept_cards.json, semantic_bridge.json, introspection.json)
- `probe "specific sub-problem"` — Deep introspection: forced bridging, anomaly injection, concrete steering directions. Outputs to `results/concept_evolve/probe_result.json`
- `reframe "problem statement"` — Restates problem in 5 different domain vocabularies. Outputs to `results/concept_evolve/reframings.json`

**Inter-module dependencies:** Requires `claude` CLI to be available in PATH (spawns sub-agents). Outputs to `results/concept_evolve/`.

**Usage for concept exploration:**
1. Run `evolve` at project start to generate initial concept landscape
2. Read concept cards for cross-domain mathematical formalizations
3. Use concept cards to guide Semantic Scholar searches in unexpected domains
4. Run `probe` when stuck or entering novel territory
5. Run `reframe` to see the problem through different domain lenses
6. Outputs are STEERING MECHANISMS — they guide search, not provide final answers

### `research_rubric.json`
**Purpose:** Central tracking document for the research plan. Contains 5 phases with 26 items total, each with description, acceptance criteria, and status tracking.

**Phases:**
1. Problem Analysis & Literature Review (items 001-006)
2. Baseline Implementation & Metrics (items 007-011)
3. Core Research & Novel Approaches (items 012-017)
4. Experiments & Evaluation (items 018-022)
5. Analysis & Documentation (items 023-026)

**Status tracking:** Each item has `status` (pending/in_progress/completed/failed), `notes`, and `error` fields. Summary section tracks aggregate counts.

### `sources.bib`
**Purpose:** BibTeX bibliography maintained throughout research. Every consulted paper, implementation, blog post, or documentation source must be recorded here.

### Project Source Code (`src/`)

**`src/baselines/`** — Reference implementations of known SSSP algorithms:
- Dijkstra with Fibonacci heap (the O(m + n log n) reference)
- Dijkstra with binary heap
- Bellman-Ford (correctness verification baseline)

**`src/graphs/`** — Graph generation and I/O:
- Random graph generators (Erdos-Renyi, sparse, dense, grid, power-law, road-network)
- DIMACS format I/O

**`src/benchmark/`** — Benchmarking harness:
- Wall-clock timing with warmup and statistical reporting
- Operation counting (comparisons, additions, heap ops)
- Memory tracking
- Output to JSON/CSV

**`src/sota/`** — State-of-the-art implementations:
- Duan et al. STOC 2025 algorithm (or faithful simplification)

**`src/novel/`** — Novel algorithm implementation (the core research contribution)

**`src/datastructures/`** — Specialized data structures:
- Priority queues, bucket structures, or other structures needed by the novel algorithm

## Key Dependencies and Data Flow

```
semantic_scholar.py ──→ sources.bib
                    ──→ literature_review.md
concept_evolve.py  ──→ results/concept_evolve/*.json
                    ──→ steering_notes.md, novel_directions.md

src/graphs/generator.py ──→ src/baselines/*.py
                        ──→ src/sota/*.py
                        ──→ src/novel/*.py

src/benchmark/harness.py ──→ results/*.json
                         ──→ figures/*.png
```

## Environment Notes

- Platform: Linux 4.4.0
- Python 3 available
- Git repository on branch `research-lab-1772408511`
- Main branch: `main`
- Fixed random seed: 42 for reproducibility
