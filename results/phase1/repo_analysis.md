# Repository Structure Analysis

## Overview

This repository is a structured research workspace for discovering, implementing, and formally verifying a novel branchless binary GCD algorithm. It uses an agent pipeline with specialized tooling for literature review, concept exploration, and iterative experimentation.

## Agent Pipeline

```
orchestrator -> researcher -> writer -> reviewer
```

| Agent | Role | Status |
|-------|------|--------|
| **orchestrator** | Planning-only rubric author. Creates `research_rubric.json`. Cannot use concept_evolve. | completed |
| **researcher** | Execution-heavy research worker. Has access to concept_evolve and semantic_scholar tools. | in_progress |
| **writer** | Paper writing and synthesis. Has semantic_scholar but no concept_evolve. | pending |
| **reviewer** | Peer review and quality control. Has semantic_scholar but no concept_evolve. | pending |
| **concept_worker** | ConceptEvolve sub-worker (no recursive concept tool). Has all other tools. | available |

Configuration: `.archivara/opencode.json`

## Core Modules

### `.archivara/concept_evolve.py` (829 lines)
- **Purpose**: Cross-domain concept tree generation and traversal
- **Commands**: `evolve`, `probe`, `reframe`, `walk`
- **Execution paths**: (1) OpenCode sub-agent via `opencode run`, (2) Direct LLM API fallback (Anthropic/OpenAI)
- **Output**: `results/concept_evolve/` with `tree/`, `concept_cards.json`, `semantic_bridge.json`, `steering_directions.json`, `walk_paths.json`
- **Features**: File-based locking, caching with configurable TTL (2h default), automatic Semantic Scholar literature enrichment per concept

### `.archivara/semantic_scholar.py` (277 lines)
- **Purpose**: Literature graph traversal via Semantic Scholar API
- **Commands**: `search`, `citations`, `references`, `recommend`, `graph`, `bibtex`
- **Features**: Exponential backoff (6 retries), BibTeX export, citation graph construction
- **API**: Uses `https://api.semanticscholar.org/graph/v1`

### `.opencode/tools/concept_evolve.ts`
- Tool wrapper exposing concept_evolve.py to OpenCode agents

### `.opencode/tools/semantic_scholar.ts`
- Tool wrapper exposing semantic_scholar.py to OpenCode agents

## Subagents (`.opencode/agents/`)

### `concept-tree-explorer.md`
- **Mode**: subagent (read-only: no write/edit)
- **Tools**: webfetch, websearch, todoread, todowrite
- **Purpose**: Traverse concept folders, identify missing links, propose next experiments

### `literature-graph-miner.md`
- **Mode**: subagent (read-only: no write/edit)
- **Tools**: webfetch, websearch, todoread, todowrite
- **Purpose**: Mine citation graphs for transferable ideas and supporting evidence

## Output Directory Structure

```
results/
  phase1/          # Literature review, concept bridges, bottleneck analysis
  phase2/          # Baseline benchmarks, profiling reports
  phase3/          # Novel approach documentation
  phase4/          # Full experiments, statistical analysis
  phase5/          # Correctness proofs, research report, negative results
  concept_evolve/  # ConceptEvolve artifacts
    tree/          # Materialized concept folders with concept.json, README.md, literature.json
    evolve_results.json
    concept_cards.json
    semantic_bridge.json
    steering_directions.json
    walk_paths.json
figures/           # Publication-quality PNG (300 DPI) + PDF/SVG
src/
  baselines/       # C/C++ baseline GCD implementations
  baselines_rust/  # Rust baseline GCD implementations
  bench/           # Micro-benchmark harness
  novel/           # Novel algorithm implementations
```

## Key Configuration Files

| File | Purpose |
|------|---------|
| `research_rubric.json` | Master rubric with 29 items across 5 phases, tracks status |
| `sources.bib` | BibTeX references (to be created) |
| `.archivara/opencode.json` | Agent configuration, model selection, permissions |

## Research Rubric Summary

- **29 total items** across 5 phases
- **Phase 1** (6 items): Problem Analysis & Literature Review
- **Phase 2** (5 items): Baseline Implementation & Metrics
- **Phase 3** (7 items): Core Research & Novel Approaches
- **Phase 4** (6 items): Experiments & Evaluation
- **Phase 5** (5 items): Analysis & Documentation

## How Components Connect

1. **Orchestrator** creates the rubric → **Researcher** executes items in order
2. **ConceptEvolve** generates concept trees → researcher materializes them into `results/concept_evolve/tree/` → each concept becomes a module with its own `concept.json`, `README.md`, `literature.json`
3. **Semantic Scholar** provides literature backing → papers flow into `sources.bib` and concept `literature.json` files
4. **Literature-graph-miner** subagent traverses citation chains → feeds transferable ideas back to researcher
5. **Concept-tree-explorer** subagent identifies gaps → informs what experiments to run next
6. Source code in `src/` implements algorithms → benchmarks produce CSV in `results/` → figures generated in `figures/`
