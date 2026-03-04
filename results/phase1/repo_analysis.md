# Repository Structure and Research Infrastructure Analysis

## Overview

This repository is organized as a research workspace for investigating the **univalent Bloch constant** $B_u$, with the goal of achieving tighter bounds than the current best known: $B_u > 0.5708858$ (Skinner 2009) and $B_u \le 1$ (trivial).

## Directory Structure

```
repo/
  .archivara/              # Core research infrastructure scripts
    concept_evolve.py      # Concept tree generation and exploration
    semantic_scholar.py    # Literature search and citation graph traversal
    opencode.json          # OpenCode agent configuration
    logs/                  # Runtime logs
  .opencode/               # OpenCode custom agents and tools
    agents/
      concept-tree-explorer.md   # Subagent for concept tree traversal
      literature-graph-miner.md  # Subagent for citation graph mining
    tools/
      concept_evolve.ts    # Tool wrapper for concept_evolve.py
      semantic_scholar.ts  # Tool wrapper for semantic_scholar.py
  results/                 # All research output artifacts
    phase1/                # Problem analysis & literature review
    phase2/                # Baseline implementation & metrics
    phase3/                # Core research & novel approaches
    phase4/                # Experiments & evaluation
    phase5/                # Analysis & documentation
    concept_evolve/        # Concept tree artifacts
    utils/                 # Shared utility modules
  figures/                 # Publication-quality figures (PNG + PDF)
  research_rubric.json     # Master rubric tracking all 26 items across 5 phases
  sources.bib              # BibTeX bibliography (to be created)
  TASK_researcher_attempt_1.md  # Task specification document
  README.md                # Repository readme
```

## Module Descriptions

### `.archivara/concept_evolve.py`
- **Purpose:** Cross-domain concept exploration via OpenCode sub-agents.
- **Commands:** `evolve`, `probe`, `reframe`, `walk`
- **Input:** Topic string (evolve), problem string (probe/reframe), seed+depth (walk)
- **Output:** JSON artifacts in `results/concept_evolve/`:
  - `concept_cards.json` — Array of concept card objects
  - `semantic_bridge.json` — Graph with nodes, edges, bridge_chains
  - `introspection.json` — Associations, blind spots, anomaly results
  - `steering_directions.json` — Array of steering direction objects
  - `tree/` — Individual concept folders with `concept.json`, `README.md`
  - `tree/index.json` — Concept index
  - `tree/adjacency.json` — Graph adjacency list
  - `tree/walk_paths.json` — DFS walk paths through concept graph
  - `evolve_results.json` — Summary statistics
- **Caching:** Results are cached for 7200s (2h) by topic hash
- **Sub-agent:** Launches `opencode run --agent build` with detailed prompts

### `.archivara/semantic_scholar.py`
- **Purpose:** Literature discovery via Semantic Scholar API
- **Commands:** `search`, `citations`, `references`, `recommend`, `graph`, `bibtex`
- **Input:** Query strings, paper IDs, limit parameters
- **Output:**
  - `search` → List of paper objects (paperId, title, authors, year, citationCount, abstract, DOI, URL)
  - `citations/references` → List of citing/referenced papers
  - `recommend` → Recommendations based on seed paper IDs
  - `graph` → Citation graph with nodes + edges, saveable to JSON
  - `bibtex` → BibTeX entry string for a paper ID
- **Rate limiting:** Exponential backoff (6 retries, 0.75 * 2^attempt seconds)

### `.opencode/agents/concept-tree-explorer.md`
- **Mode:** Subagent (read-only tools: webfetch, websearch, todoread, todowrite)
- **Purpose:** Traverse concept folders, identify missing links, propose next experiments

### `.opencode/agents/literature-graph-miner.md`
- **Mode:** Subagent (read-only tools: webfetch, websearch, todoread, todowrite)
- **Purpose:** Mine citation graphs for transferable ideas and supporting evidence

### `.opencode/tools/concept_evolve.ts` and `semantic_scholar.ts`
- **Purpose:** TypeScript tool wrappers that expose the Python scripts as OpenCode custom tools
- **Interface:** Available as `concept_evolve` and `semantic_scholar` tool calls within agent sessions

### `.archivara/opencode.json`
- **Purpose:** Master configuration for OpenCode
- **Model:** `anthropic/claude-opus-4-6`
- **Agents defined:** orchestrator, researcher, writer, reviewer, concept_worker
- **Tool permissions:** All tools enabled for researcher agent including concept_evolve and semantic_scholar

## Interconnections

1. **Rubric → All modules:** `research_rubric.json` drives the workflow; each item references specific output paths.
2. **concept_evolve.py → sub-agents:** Launches OpenCode build agents that use websearch, semantic_scholar, etc.
3. **semantic_scholar.py → sources.bib:** The `bibtex` command appends entries to the bibliography.
4. **results/utils/tracker.py → results/phase2/metrics.json:** (To be created) Centralized experiment tracking.
5. **Concept tree → Phase 3 work:** `results/concept_evolve/tree/` provides concept backlog for cross-domain exploration.

## Readiness Confirmation

- `results/` directory: EXISTS with all phase subdirectories created
- `figures/` directory: EXISTS with subdirectories for domain visualizations
- Python packages installed: mpmath, numpy, scipy, matplotlib, seaborn
- All infrastructure scripts verified: concept_evolve.py (628 lines), semantic_scholar.py (277 lines)
- OpenCode configuration verified with all required agents and tools

## Next Steps

1. Run concept_evolve `evolve` command (mandatory before completing item_001)
2. Begin deep mathematical formulation (item_002)
3. Conduct comprehensive literature search (item_003)
