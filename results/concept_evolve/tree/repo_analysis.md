# Repository Analysis: Minimal Gravity Simulator

**Date:** 2026-03-03  
**Agent:** researcher  
**Rubric Item:** item_001  

## 1. Project Overview

This repository is an AI-agent-orchestrated research platform built on the Archivara + OpenCode framework. The project goal is to design, implement, and evaluate a minimal N-body gravity simulator with multiple integration methods, tree-based force approximation, adaptive timestepping, collision detection, and publication-grade visualization. The project is tracked via a 25-item research rubric spanning 5 phases: problem analysis, baseline implementation, core research, experiments, and documentation.

## 2. Module Inventory

### 2.1 `.archivara/` — Platform Runtime Scripts and Configuration

This module contains the core Python tooling and agent configuration that powers the research automation.

**Files:**

- **`opencode.json`** (88 lines): Master agent configuration file. Defines the LLM model (`anthropic/claude-opus-4-6`), default agent role (`build`), Anthropic provider settings, and global tool permissions. Specifies per-agent tool access matrices for five agent roles: orchestrator, researcher, writer, reviewer, and concept_worker. The researcher agent has access to `concept_evolve` and `semantic_scholar` tools; the concept_worker has all tools except `concept_evolve` (to prevent recursive spawning).

- **`concept_evolve.py`** (628 lines): The ConceptEvolve engine — the central concept-tree exploration system. Supports four CLI commands:
  - `evolve <topic>`: Generates 10+ cross-domain concept cards, a semantic bridge graph, introspection analysis, and steering directions. Writes results to `results/concept_evolve/`.
  - `probe <problem>`: Deep-probes a specific bottleneck for solutions from adjacent fields.
  - `reframe <problem>`: Reframes a problem across 8+ distinct domains to discover novel approaches.
  - `walk [--seed X] [--depth N]`: Traverses the accumulated concept tree and filters high-value paths.
  
  The engine spawns OpenCode sub-agents (concept_worker role), includes 2-hour TTL caching, file locking for concurrent access, JSON tolerance (handles markdown fence-wrapped JSON), and debug logging to `results/concept_evolve/.debug/`.

- **`semantic_scholar.py`** (277 lines): Semantic Scholar API client for academic paper search and citation graph traversal. Uses the Semantic Scholar Graph API v1 with exponential backoff retry (6 attempts). Supports six commands: `search`, `citations`, `references`, `recommend`, `graph` (builds citation graphs with configurable roots and fanout), and `bibtex` (generates BibTeX entries for `sources.bib`).

- **`logs/`**: Agent execution logs in JSONL format.
  - `orchestrator.log` (31 lines): Records the orchestrator agent session that created the research rubric.
  - `researcher_attempt_1.log` (12 lines): Partial log from the researcher agent's initial (interrupted) attempt.

### 2.2 `.opencode/` — OpenCode Plugin System (Tooling Runtime)

This module provides the Node.js/TypeScript plugin infrastructure that wraps Python tools as OpenCode-compatible tools and defines sub-agent roles.

**Files:**

- **`package.json`**: Single dependency on `@opencode-ai/plugin` v1.2.15.
- **`bun.lock`**: Lockfile for the Bun JavaScript runtime pinning exact dependency versions.
- **`node_modules/`**: Installed packages including `@opencode-ai/sdk`, `@opencode-ai/plugin`, and `zod` (schema validation).

**Tool Wrappers:**

- **`tools/concept_evolve.ts`** (33 lines): TypeScript wrapper that exposes `.archivara/concept_evolve.py` as an OpenCode tool. Accepts parameters: `command` (evolve/probe/reframe/walk), optional `topic`, optional `seed`, optional `depth`. Executes via `execFileSync` with a 20-minute timeout.

- **`tools/semantic_scholar.ts`** (38 lines): TypeScript wrapper for `.archivara/semantic_scholar.py`. Accepts: `command` (search/citations/references/recommend/graph/bibtex), optional `query`, optional `limit`. Automatically appends `--json` flag for non-bibtex commands.

**Sub-Agent Definitions:**

- **`agents/literature-graph-miner.md`** (12 lines): Read-only sub-agent with websearch, webfetch, and todo tools. Purpose: mine citation graphs for transferable ideas and supporting evidence, prioritizing citation chains that connect distant domains.

- **`agents/concept-tree-explorer.md`** (12 lines): Read-only sub-agent with websearch, webfetch, and todo tools. Purpose: traverse concept folders, identify missing conceptual links, and propose next experiments based on the concept tree.

### 2.3 `figures/` — Visualization Output Directory

Currently empty. Designated output location for publication-grade figures in both PNG (300 DPI) and PDF formats. Expected figures by project completion include: `baseline_scaling.png`, `integrator_comparison.png`, `scaling_comparison.png`, `solar_system_orbits.png`, `collapse_sequence.png`, and `theta_tradeoff.png` (minimum 5 figures required).

### 2.4 `results/` — Research Results Output Directory

Currently empty (with subdirectories created). Will contain all experimental data, analysis documents, and concept exploration artifacts. Expected subdirectories: `baseline/`, `verlet/`, `leapfrog/`, `barneshut/`, `adaptive/`, `collisions/`, `experiments/`, and `concept_evolve/tree/`. Key deliverables include `findings.md` (>2000 words) and `final_checklist.md`.

### 2.5 `src/` — Source Code (To Be Created)

Not yet present. Will contain the core simulation code: `gravity_sim.py` (main simulator with multiple integrators), `visualize.py` (2D visualization), and `barneshut.py` (Barnes-Hut tree algorithm).

### 2.6 `tests/` — Test Suite (To Be Created)

Not yet present. Will contain `test_physics.py` with at least 5 unit tests covering Keplerian orbits, momentum conservation, energy computation, force symmetry, and single-body edge cases.

### 2.7 `scenarios/` — Physical Scenario Configurations (To Be Created)

Not yet present. Will contain JSON scenario files such as `solar_system.json` with real mass ratios and orbital parameters.

### 2.8 Root-Level Files

- **`research_rubric.json`** (276 lines): Master research plan and progress tracker. Defines 25 items across 5 phases with acceptance criteria, status tracking, and summary counts. Read and updated by all agents.
- **`README.md`**: Currently a placeholder (`# testing`). Will be expanded to >500 words with project overview, installation instructions, usage examples, and key findings.
- **`TASK_researcher_attempt_1.md`**: Researcher agent instructions/prompt (112 lines).
- **`.gitignore`**: Excludes sensitive files, agent configs, and logs from version control.
- **`.gitattributes`**: Configures Git LFS tracking for large binary and data files (CSV, HDF5, NPY, etc.).

## 3. Inter-Module Dependency Graph

```
research_rubric.json (master plan)
    |
    v
.archivara/opencode.json (agent config)
    |
    +---> Agent Roles: orchestrator, researcher, writer, reviewer, concept_worker
    |         |
    |         +---> Tool Access:
    |                  .opencode/tools/concept_evolve.ts --> .archivara/concept_evolve.py
    |                  .opencode/tools/semantic_scholar.ts --> .archivara/semantic_scholar.py
    |
    +---> Sub-Agents:
              .opencode/agents/literature-graph-miner.md (read-only, websearch)
              .opencode/agents/concept-tree-explorer.md (read-only, websearch)

.archivara/concept_evolve.py
    |
    +---> Outputs: results/concept_evolve/ (concept cards, semantic bridges, steering directions)
    +---> Outputs: results/concept_evolve/tree/ (concept folders, index, adjacency graph, walk paths)
    +---> Spawns: OpenCode sub-agents (concept_worker role)

.archivara/semantic_scholar.py
    |
    +---> External API: api.semanticscholar.org/graph/v1
    +---> Outputs: results/literature_graph.json, sources.bib
```

## 4. Agent Capabilities

| Agent Role | Primary Purpose | Key Tools | Write Access |
|---|---|---|---|
| **orchestrator** | Creates research plan, manages rubric | bash, write, edit, webfetch, websearch | Yes |
| **researcher** | Executes research items, implements code | All tools + concept_evolve + semantic_scholar | Yes |
| **writer** | Synthesizes findings into documents | bash, write, edit, webfetch + semantic_scholar | Yes |
| **reviewer** | Quality checks deliverables | bash, write, edit, webfetch + semantic_scholar | Yes |
| **concept_worker** | Spawned by concept_evolve for cross-domain research | All tools except concept_evolve | Yes |

## 5. Current State Assessment

- **Infrastructure:** Fully operational. All agent configs, tool wrappers, sub-agent definitions, and Python tooling are in place.
- **Research Progress:** Zero items completed. The orchestrator has finished (rubric created). The researcher agent is actively executing.
- **Missing Artifacts:** No source code (`src/`), tests (`tests/`), scenarios (`scenarios/`), bibliography (`sources.bib`), or results data. All must be created during rubric execution.
- **Dependencies:** Python 3 is available. Additional packages (numpy, matplotlib, seaborn, scipy) will need to be installed for simulation and visualization.
- **Risk Assessment:** The primary risk is the computational scope of 25 rubric items. Barnes-Hut implementation (item_013) and adaptive timestepping (item_015) are the most technically complex items. The concept_evolve engine's sub-agent spawning adds execution time overhead.

## 6. Recommended Execution Strategy

1. Install scientific Python stack (numpy, matplotlib, seaborn, scipy) early.
2. Complete literature reviews (items 002-003) in parallel where possible.
3. Build the core simulator incrementally, testing each integrator before moving to the next.
4. Use concept_evolve strategically — at project kickoff (mandatory) and when blocked on optimization strategies.
5. Maintain continuous rubric updates and atomic git commits for traceability.
