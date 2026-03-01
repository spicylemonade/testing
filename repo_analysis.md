# Repository Analysis

## Overview

This repository is an Archivara-orchestrated research project investigating improvements to Single-Source Shortest Paths (SSSP) algorithms. The Archivara framework coordinates multiple agent phases (orchestrator → researcher → writer → reviewer) through a rubric-driven workflow defined in `research_rubric.json`.

## Repository Root Files

| File | Purpose |
|------|---------|
| `research_rubric.json` | Central state machine: defines 25 research items across 5 phases with status tracking. Agents read/update this to coordinate. |
| `README.md` | Project description (currently minimal). |
| `sources.bib` | BibTeX bibliography for all consulted papers and code references. |
| `.gitignore` | Excludes `.env`, secrets, `.claude/`, `.codex/`, `.archivara/`, `TASK_*.md`, agent logs. |
| `.gitattributes` | Git LFS / attribute configuration. |
| `TASK_researcher_attempt_1.md` | Task specification for the researcher agent (this run). |

## `.archivara/` Directory — Tooling Infrastructure

### `.archivara/semantic_scholar.py`

**Purpose:** CLI wrapper around the Semantic Scholar Academic Graph API for paper discovery and citation graph traversal.

**API / CLI Commands:**

| Command | Arguments | Description |
|---------|-----------|-------------|
| `search` | `<query> [--limit N]` | Full-text paper search. Returns paper ID, title, year, citation count, authors, abstract snippet. |
| `citations` | `<paperId> [--limit N]` | Lists papers that cite the given paper (forward citation graph). |
| `references` | `<paperId> [--limit N]` | Lists papers referenced by the given paper (backward citation graph). |
| `recommend` | `<paperId1> [<paperId2> ...]` | POST to recommendations API with positive paper IDs; returns cross-domain paper suggestions. |
| `bibtex` | `<paperId>` | Generates a BibTeX `@article` entry for the paper to stdout (pipe to `>> sources.bib`). |

**API Details:**
- Base URL: `https://api.semanticscholar.org/graph/v1`
- Fields requested: `title, authors, year, citationCount, abstract, externalIds, venue`
- Retry logic: 3 attempts with 1-second backoff
- User-Agent: `Archivara-Research/1.0`

**Data Flow:** CLI args → HTTP GET/POST to Semantic Scholar → JSON parsing → formatted stdout / BibTeX output.

### `.archivara/concept_evolve.py`

**Purpose:** Cross-domain concept discovery tool based on the Concept-Guided Evolutionary Discovery framework (2026). Spawns Claude Code CLI sub-agents to generate structured concept connections, semantic bridge graphs, and introspective analyses.

**API / CLI Commands:**

| Command | Arguments | Description |
|---------|-----------|-------------|
| `evolve` | `<topic>` | Full pipeline: concept externalization (8-12 concept cards), semantic bridge graph construction, concept probing, anomaly injection. Outputs to `results/concept_evolve/`. |
| `probe` | `<sub-problem>` | Deep introspection on a specific sub-problem: forced bridging between distant concepts, anomaly injection, concrete steering directions. Outputs `probe_result.json`. |
| `reframe` | `<problem>` | Restates the problem in 5 different domain vocabularies to unlock alternative solution strategies. Outputs `reframings.json`. |

**Output Files (in `results/concept_evolve/`):**

| File | Command | Content |
|------|---------|---------|
| `concept_cards.json` | `evolve` | Array of concept cards with symbolic_name, description, domains, mathematical_formalization, analogical_connections |
| `semantic_bridge.json` | `evolve` | Typed directed graph: nodes (concepts), edges (structural/functional/mathematical/metaphorical), bridge_chains |
| `introspection.json` | `evolve` | Associations, surprise ratings, dominant conceptual frames, anomaly injection results |
| `evolve_results.json` | `evolve` | Summary metadata: topic, timestamp, counts |
| `summary.txt` | `evolve` | Human-readable summary of all evolve outputs |
| `probe_result.json` | `probe` | Associations, forced_bridges, anomaly_results, steering_directions |
| `reframings.json` | `reframe` | Array of domain reframings with key_insight and suggested_technique |

**Sub-agent Mechanism:**
- Spawns `claude -p <prompt> --model opus --dangerously-skip-permissions --output-format text --allowedTools Bash,Read,Write,Glob,Grep,WebSearch,WebFetch`
- Default timeout: 600s for evolve, 300s for probe, 180s for reframe
- JSON extraction: tries markdown fence blocks, then regex for JSON objects/arrays
- Working directory: `.archivara/`

### `.archivara/logs/`

| File | Content |
|------|---------|
| `orchestrator.log` | Full execution log from the orchestrator agent that created the rubric |
| `researcher_attempt_1.log` | Log for the researcher agent's first attempt |

## Archivara Orchestration Framework

**Workflow:** The framework operates as a sequential agent pipeline:

1. **Orchestrator** (completed): Reads the task, generates `research_rubric.json` with 25 items across 5 phases, and hands off to the researcher.
2. **Researcher** (in progress — this agent): Executes all 25 rubric items in order, performing literature review, implementation, experimentation, and documentation.
3. **Writer** (pending): Takes researcher outputs and produces a polished paper/report.
4. **Reviewer** (pending): Reviews the paper and provides feedback.

**State Machine:** `research_rubric.json` serves as the shared state:
- `agent_status`: tracks which agent is active and its start/completion times
- `phases[].items[]`: each item has `status` (pending/in_progress/completed/failed), `notes`, `error`
- `summary`: aggregate counts of item statuses

**Data Flow:**
```
research_rubric.json (shared state)
        ↓
.archivara/semantic_scholar.py → sources.bib + literature data
.archivara/concept_evolve.py   → results/concept_evolve/*.json
        ↓
src/          → algorithm implementations
results/      → experimental data (JSON, CSV)
figures/      → publication-quality plots (PNG, PDF)
```

## Directory Structure (Target)

```
repo/
├── .archivara/           # Tooling (semantic_scholar, concept_evolve, logs)
├── src/
│   ├── baselines/        # Dijkstra+FibHeap, DMMSY implementations
│   ├── novel/            # Novel algorithm implementation
│   └── benchmarks/       # Graph generators, benchmark runner
├── results/              # Experimental data, proofs, analyses
│   └── concept_evolve/   # ConceptEvolve outputs
├── figures/              # Publication-quality plots
├── sources.bib           # Bibliography
├── research_rubric.json  # Orchestration state
└── survey.md             # Literature survey
```
