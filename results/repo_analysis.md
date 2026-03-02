# Repository Structure and Tooling Analysis

## Overview

This repository implements a computational research project investigating the **Perfect Cuboid Problem** (also known as the perfect box or Euler brick with integer space diagonal). The goal is to find a rectangular box where all edges, all face diagonals, and the space diagonal are integers — or to contribute computational evidence regarding the problem's status.

## File Structure

### Root-Level Files

| File | Purpose |
|------|---------|
| `research_rubric.json` | Central research tracking document. Contains 27 items across 5 phases, each with status tracking (pending/in_progress/completed/failed), acceptance criteria, and notes. Used by the orchestrator-researcher-writer-reviewer agent pipeline. |
| `sources.bib` | BibTeX bibliography file for all academic references used in the project. |
| `README.md` | Project readme (minimal placeholder). |
| `TASK_researcher_attempt_1.md` | Full task specification for the researcher agent, including all instructions, constraints, and workflow requirements. |
| `.gitignore` | Git ignore rules. |
| `.gitattributes` | Git attributes configuration. |

### `.archivara/` — Research Tooling

#### `.archivara/semantic_scholar.py`
**Purpose:** Python CLI tool for querying the Semantic Scholar API for academic paper discovery.

**API/Commands:**
- `search "query" [--limit N]` — Search for papers by keyword, returns titles, authors, years, citation counts, abstracts, and paper IDs.
- `citations <paperId> [--limit N]` — Get papers that cite a given paper (forward citation traversal).
- `references <paperId> [--limit N]` — Get papers referenced by a given paper (backward citation traversal).
- `recommend <paperId1> [<paperId2> ...]` — Get cross-domain paper recommendations based on seed papers.
- `bibtex <paperId>` — Generate BibTeX entry for a paper (pipe to `>> sources.bib`).

**Dependencies:** Python stdlib only (`urllib`, `json`, `sys`, `time`).

**Data Flow:** Queries Semantic Scholar Graph API v1 (`https://api.semanticscholar.org/graph/v1`). Returns structured paper metadata. The `bibtex` command outputs formatted BibTeX to stdout for appending to `sources.bib`.

#### `.archivara/concept_evolve.py`
**Purpose:** Cross-domain concept discovery tool that spawns Claude sub-agents for concept externalization, semantic bridge construction, and proxy introspection.

**API/Commands:**
- `evolve "topic"` — Full pipeline: generates concept cards (8-12), builds semantic bridge graph, performs introspection and anomaly injection. Outputs to `results/concept_evolve/`.
- `probe "sub-problem"` — Deep introspection on a specific sub-problem with forced bridging, anomaly injection, and concrete steering directions. Outputs `probe_result.json`.
- `reframe "problem"` — Restates the problem in 5 different domain vocabularies with suggested techniques. Outputs `reframings.json`.

**Dependencies:** Python stdlib + `claude` CLI (spawns sub-agents via `subprocess.run`).

**Data Flow:**
1. Constructs detailed prompts for Claude sub-agents
2. Spawns `claude -p <prompt>` subprocess with specific model and tool permissions
3. Parses JSON output from sub-agent (handles markdown fence extraction)
4. Writes structured JSON files to `results/concept_evolve/`

**Output Files:**
- `results/concept_evolve/concept_cards.json` — Cross-domain concept cards with mathematical formalizations
- `results/concept_evolve/semantic_bridge.json` — Typed directed graph of analogical relationships
- `results/concept_evolve/introspection.json` — Self-reflective associations and anomaly injection results
- `results/concept_evolve/evolve_results.json` — Summary metadata
- `results/concept_evolve/summary.txt` — Human-readable summary
- `results/concept_evolve/probe_result.json` — Deep probe output
- `results/concept_evolve/reframings.json` — Domain reframings

#### `.archivara/logs/`
- `orchestrator.log` — Log from the orchestrator agent that created the research rubric.
- `researcher_attempt_1.log` — Log from a previous researcher agent attempt.

### `src/` — Source Code (to be created)
Will contain the computational modules:
- `euler_brick.py` — Parametric Euler brick generators
- `modular_filter.py` — Multi-stage modular sieve
- `space_diagonal.py` — Perfect square tests and near-miss tracking
- `baseline_search.py` — Brute-force search implementation
- `metrics.py` — Search metrics framework
- `config.py` — Run configuration for reproducibility
- `triple_decomposition.py` — Pythagorean triple pair search
- `elliptic_families.py` — Elliptic curve parametric families
- `constraint_solver.py` — CSP/SAT encoding
- `quadratic_sieve.py` — Quadratic residue sieving
- `combined_search.py` — Integration of all methods
- `near_miss_analysis.py` — Statistical analysis of near-misses

### `results/` — Research Outputs
Directory for experimental data, analysis documents, and JSON result files.

### `figures/` — Visualizations
Directory for publication-quality figures (PNG and PDF).

## Data Flow Architecture

```
research_rubric.json (orchestration)
       │
       ▼
.archivara/semantic_scholar.py ──► sources.bib
       │                              │
       ▼                              ▼
.archivara/concept_evolve.py ──► results/concept_evolve/*.json
       │
       ▼
src/ modules (euler_brick → modular_filter → space_diagonal → search)
       │
       ├──► results/*.json, results/*.csv, results/*.md
       └──► figures/*.png, figures/*.pdf
```

## Interconnections

1. **Rubric → All Work**: `research_rubric.json` drives the order and tracking of all research items.
2. **Semantic Scholar → sources.bib**: Paper discovery feeds the bibliography.
3. **Concept Evolve → Research Steering**: Cross-domain concepts inform algorithmic design choices in `src/`.
4. **src/ modules → results/**: All computational experiments produce structured output.
5. **results/ → figures/**: Analysis scripts read results data and produce visualizations.
6. **sources.bib ← All documents**: Every `results/*.md` document cites entries from the bibliography.

## Agent Pipeline

The project uses a multi-agent pipeline:
1. **Orchestrator** (completed) — Created the research rubric
2. **Researcher** (current) — Executes all 27 rubric items, writes code, runs experiments
3. **Writer** (pending) — Will produce the final research report
4. **Reviewer** (pending) — Will review and validate all outputs
