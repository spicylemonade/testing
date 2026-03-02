# Repository Structure & Tooling Analysis

**Date**: 2026-03-02  
**Item**: item_001  
**Author**: Researcher Agent

## Overview

This repository is an AI research sandbox on branch `research-lab-1772441812`, designed to
implement a minimal N-body gravity simulation through an automated multi-agent workflow.
The orchestrator agent has already produced a 28-item research rubric across 5 phases.

## Build Prerequisites

| Prerequisite | Purpose | Version |
|---|---|---|
| **Python 3** | Core simulation code, ConceptEvolve, Semantic Scholar CLI | 3.10+ |
| **Bun** | JavaScript/TypeScript runtime for OpenCode tool wrappers | Latest |
| **OpenCode CLI** | Agent orchestration, sub-agent spawning | Latest |
| **Git** | Version control, LFS for large data files | 2.x+ |

No third-party Python packages are required by the existing tooling (all stdlib).
The simulation implementation will require `numpy`, `matplotlib`, and `scipy` (to be installed).

## Module Inventory

### `.archivara/concept_evolve.py` (604 lines)

**Purpose**: Cross-domain concept tree explorer. Generates, probes, reframes, and walks
research concept trees by delegating reasoning to OpenCode sub-agents.

**Key Functions**:
- `evolve(topic)` — Generates 14+ concept cards with semantic bridges, introspection data, and steering directions
- `probe(problem)` — Deep concept probe for specific bottlenecks
- `reframe(problem)` — Reframes a problem across 8+ distinct domains
- `walk(seed, depth)` — Traverses previously-generated concept walk paths
- `_run_sub_agent(prompt, name, timeout)` — Spawns `opencode` CLI in non-interactive JSON mode
- `_semantic_search(query, limit)` — Delegates to `semantic_scholar.py`
- `_materialize_concept_folders(topic, cards, bridge)` — Creates per-concept folders under `results/concept_evolve/tree/`

**Dependencies**: Python stdlib only (`argparse`, `fcntl`, `json`, `os`, `re`, `subprocess`, `sys`, `time`, `pathlib`)

**Connections**:
- Calls `semantic_scholar.py` via subprocess
- Invoked by `.opencode/tools/concept_evolve.ts`
- Writes to `results/concept_evolve/`

### `.archivara/semantic_scholar.py` (277 lines)

**Purpose**: CLI tool for querying the Semantic Scholar API. Supports paper search,
citation/reference traversal, recommendations, citation graph construction, and BibTeX export.

**Key Functions**:
- `search(query, limit)` — Keyword paper search
- `citations(paper_id, limit)` — Get citing papers
- `references(paper_id, limit)` — Get referenced papers
- `recommend(paper_ids, limit)` — Get recommendations from seed papers
- `citation_graph(seed_query, roots, fanout)` — Builds citation graph with BFS
- `bibtex_entry(paper_id)` — Formats paper metadata as BibTeX

**Dependencies**: Python stdlib only (`urllib.request`, `urllib.parse`, `json`, `argparse`, `time`)

**Connections**:
- Called by `concept_evolve.py` for literature lookups
- Invoked by `.opencode/tools/semantic_scholar.ts`
- Queries `https://api.semanticscholar.org/graph/v1`

### `.archivara/opencode.json` (88 lines)

**Purpose**: Configures the OpenCode agent framework for this workspace.

**Key Settings**:
- Model: `anthropic/claude-opus-4-6`
- Default agent: `build`
- Provider: Anthropic (API key from env vars)

### `.opencode/tools/concept_evolve.ts` (32 lines)

**Purpose**: OpenCode tool wrapper for `concept_evolve.py`. Accepts command
(evolve/probe/reframe/walk), topic, seed, and depth parameters. Spawns Python via `execFileSync`.

### `.opencode/tools/semantic_scholar.ts` (38 lines)

**Purpose**: OpenCode tool wrapper for `semantic_scholar.py`. Accepts command
(search/citations/references/recommend/graph/bibtex), query, and limit parameters.

### `.opencode/agents/literature-graph-miner.md`

**Purpose**: Subagent definition for mining citation graphs. Read-only mode.
Tools: webfetch, websearch, todoread, todowrite.
Instruction: "Prioritize citation chains that connect distant domains."

### `.opencode/agents/concept-tree-explorer.md`

**Purpose**: Subagent definition for exploring concept trees. Read-only mode.
Tools: webfetch, websearch, todoread, todowrite.
Instruction: "Focus on traversing concept folders, identifying missing links."

## Agent Roles

| Role | Status | Tools | Purpose |
|---|---|---|---|
| **orchestrator** | completed | No concept_evolve | Planning-only rubric author |
| **researcher** | in_progress | concept_evolve + semantic_scholar | Execution-heavy research worker |
| **writer** | pending | semantic_scholar only | Paper writing and synthesis |
| **reviewer** | pending | semantic_scholar only | Peer review and quality control |
| **concept_worker** | — | semantic_scholar, websearch, webfetch, bash, read, write, edit | ConceptEvolve sub-worker (no concept_evolve to prevent recursion) |

## Inter-Module Connection Map

```
research_rubric.json (plan, 28 items)
        |
.archivara/opencode.json (agent config)
        |
        +---> orchestrator (completed) --wrote--> research_rubric.json
        +---> researcher (in_progress) --reads--> research_rubric.json
        +---> writer (pending)
        +---> reviewer (pending)
        |
.opencode/tools/
        +---> concept_evolve.ts --calls--> .archivara/concept_evolve.py
        |                                        |
        |                                        +--calls--> semantic_scholar.py
        |                                        +--calls--> opencode CLI (sub-agents)
        |                                        +--writes-> results/concept_evolve/
        |
        +---> semantic_scholar.ts --calls--> .archivara/semantic_scholar.py
                                                     +--calls--> Semantic Scholar API

.opencode/agents/
        +---> literature-graph-miner.md (subagent)
        +---> concept-tree-explorer.md  (subagent)
```

## Output Directories

| Directory | Purpose | Current State |
|---|---|---|
| `results/` | All JSON/CSV data, reports, concept trees | Empty (subdirs created) |
| `results/analysis/` | Problem analysis documents | This document |
| `results/baseline/` | Baseline experiment results | Empty |
| `results/experiments/` | Advanced experiment results | Empty |
| `results/concept_evolve/` | Concept tree artifacts | Empty (populated by evolve) |
| `figures/` | PNG (300 DPI) + PDF publication-grade plots | Empty |
| `src/` | Simulation source modules | To be created |
| `tests/` | Unit test files | To be created |

## Git Configuration

- **LFS**: Tracking archives (`.tar`, `.gz`, `.zip`), scientific data (`.npz`, `.npy`, `.h5`, `.hdf5`, `.parquet`, `.csv`, `.feather`, `.dat`), serialized (`.pickle`, `.pkl`), 3D mesh (`.obj`, `.stl`, `.ply`)
- **Ignored**: `.env*`, `*.key`, `*.pem`, `opencode.json`, `.opencode/`, `.archivara/`, `TASK_*.md`, agent logs
