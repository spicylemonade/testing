# Repository Structure Analysis

## Overview

This repository implements an **automated multi-agent research system** built on the OpenCode platform. The current research project is "Improving the Lower Bound of BB(6): Searching for Long-Running 6-State Turing Machines." The system uses a pipeline of AI agents (orchestrator → researcher → writer → reviewer) coordinated through a shared `research_rubric.json`, with a novel "ConceptEvolve" subsystem that spawns sub-agents for cross-domain ideation.

## 1. `.archivara/` Scripts and Their Purposes

### `concept_evolve.py` (628 lines)
The ConceptEvolve engine — a concept-tree exploration system that spawns OpenCode sub-agents to research, ideate, and write structured artifacts to disk. Python serves as the orchestration layer only; it constructs rich natural-language prompts, shells out to `opencode run --agent build --model anthropic/claude-opus-4-6` as a subprocess, and post-processes the filesystem artifacts the sub-agent leaves behind.

**Four CLI commands:**
- **`evolve <topic>`**: The main command. Spawns a sub-agent (up to 2 attempts, 900s timeout each) with a 6-step prompt instructing it to: (1) research via websearch/semantic_scholar, (2) generate 10+ concept cards, (3) build a semantic bridge graph, (4) introspect for blind spots, (5) produce steering directions, (6) write all files. Post-processes results into concept folders, adjacency graphs, and DFS walk paths. Uses a 2-hour TTL cache and file locking to prevent duplicate runs.
- **`probe <problem>`**: Deep-dive on a specific bottleneck. Produces `probe_result.json` with associations, forced bridges, anomaly results, and steering directions.
- **`reframe <problem>`**: Reframes a problem across 8+ distinct domains, producing `reframings.json` with domain-specific techniques and mappings back to the original problem.
- **`walk [--seed X] [--depth N]`**: Purely local (no sub-agent). Navigates pre-computed walk paths from the concept tree.

### `semantic_scholar.py` (277 lines)
A standalone CLI utility for querying the Semantic Scholar academic API. Provides robust literature graph traversal with exponential-backoff retry logic (6 attempts) and BibTeX export. Supports six commands: `search`, `citations`, `references`, `recommend`, `graph`, and `bibtex`. All commands support `--json` output and `--save <path>` for persistence.

### `opencode.json` (88 lines)
The OpenCode platform configuration file defining the model (`anthropic/claude-opus-4-6`), provider settings, global permissions (edit, webfetch, websearch, bash, etc.), and all agent roles. Defines five agents with differentiated tool access — notably, the `concept_worker` agent disables `concept_evolve` to prevent recursive spawning while granting full research capabilities.

### `logs/`
Contains JSONL-formatted execution traces of agent sessions:
- `orchestrator.log`: Records the orchestrator choosing BB(6) as the research problem and writing the 25-item rubric.
- `researcher_attempt_1.log`: Beginning of the researcher agent's execution, showing initial repo exploration and task planning.

## 2. `.opencode/` Agent Definitions and Tool Wrappers

### Agent Definitions (`agents/`)

| Agent File | Mode | Description | Key Tools |
|-----------|------|-------------|-----------|
| `concept-tree-explorer.md` | subagent | Explore concept trees, identify high-value paths | webfetch, websearch (read-only, no write/edit) |
| `literature-graph-miner.md` | subagent | Mine citation graphs for transferable ideas | webfetch, websearch (read-only, no write/edit) |

Both subagents are read-only — they cannot modify files, only observe and report. They are spawned by the researcher agent at specific rubric items (e.g., item_014 for concept-tree-explorer, item_011 for literature-graph-miner).

### Tool Wrappers (`tools/`)

| Wrapper | Language | Wraps | Timeout | Key Features |
|---------|----------|-------|---------|--------------|
| `concept_evolve.ts` (33 lines) | TypeScript | `concept_evolve.py` | 1,200,000ms (20 min) | Routes evolve/probe/reframe/walk commands, 10MB buffer |
| `semantic_scholar.ts` (38 lines) | TypeScript | `semantic_scholar.py` | Default | Auto-appends `--json`, handles `recommend` multi-ID splitting |

Both use `@opencode-ai/plugin` (v1.2.15) for the `tool` function and `tool.schema` interface.

## 3. Multi-Agent Pipeline

```
ORCHESTRATOR (planning-only, concept_evolve disabled)
    │  Writes research_rubric.json (25 items, 5 phases)
    │  Status: completed
    ▼
RESEARCHER (execution-heavy, full tool access)
    │  Works through rubric items phase by phase
    │  Has concept_evolve + semantic_scholar tools
    │  Spawns subagents: concept-tree-explorer, literature-graph-miner
    │  Status: in_progress
    ▼
WRITER (synthesis, concept_evolve disabled)
    │  Reads completed research artifacts
    │  Produces research report, Twitter thread, documentation
    │  Status: pending
    ▼
REVIEWER (quality control, concept_evolve disabled)
    │  Reviews all artifacts against acceptance criteria
    │  Checks claims, verifies results
    │  Status: pending
```

**Coordination mechanism:** `research_rubric.json` serves as a shared state contract. Fields include `current_agent`, `agent_status` lifecycle tracking, and per-item `status` (pending → in_progress → completed/failed). The `updated_at` timestamp is refreshed on every change.

## 4. ConceptEvolve System Architecture

```
Agent (researcher) → concept_evolve.ts (TypeScript wrapper)
    → concept_evolve.py (Python orchestrator)
        → subprocess: opencode run --agent build (concept_worker role)
            → Sub-agent uses: websearch, webfetch, semantic_scholar, bash, write, edit
            → Writes: JSON + Markdown artifacts to results/concept_evolve/
        ← Python post-processes: concept folders, adjacency graphs, walk paths
```

**Key design principles:**
1. **Sub-agents do the real work** — Python only checks file existence and exit codes
2. **Anti-recursion guard** — `concept_worker` agent has `concept_evolve: false`
3. **Cache and locking** — 2-hour TTL cache + `fcntl.flock` prevents duplicate runs
4. **Tolerant JSON parsing** — Handles markdown fences, surrounding text, bracket-matching
5. **Debug logging** — All sub-agent I/O saved to `.debug/` for post-mortem analysis

**Output structure after `evolve`:**
```
results/concept_evolve/
    concept_cards.json          # Array of 10+ cross-domain concept cards
    semantic_bridge.json        # Graph: nodes + edges + bridge_chains
    introspection.json          # associations, blind_spots, anomaly_results
    steering_directions.json    # Array of steering direction objects
    evolve_results.json         # Summary metadata
    tree/
        index.json              # Concept index
        adjacency.json          # Graph adjacency list
        walk_paths.json         # Pre-computed DFS paths
        001_concept_slug/       # Per-concept folders
            concept.json
            README.md
            literature.json
```

## 5. Research Rubric Structure

The rubric (`research_rubric.json`) defines 25 items across 5 phases:

| Phase | Name | Items | Key Deliverables |
|-------|------|-------|-----------------|
| Phase 1 | Problem Analysis & Literature Review | 6 (001-006) | Repo analysis, SOTA survey, 10+ papers, tools catalog, ConceptEvolve, champions |
| Phase 2 | Baseline Implementation & Metrics | 5 (007-011) | TM simulator, accelerated simulator, TNF enumerator, deciders, reproduce record |
| Phase 3 | Core Research & Novel Approaches | 5 (012-016) | Guided search, mutation search, cross-domain experiments, TM breeding, parallel infra |
| Phase 4 | Experiments & Evaluation | 5 (017-021) | Search campaigns, verification, comparison, standalone verify.py, strategy analysis |
| Phase 5 | Analysis & Documentation | 4 (022-025) | Research report, Twitter thread, visualizations, concept synthesis |

Each phase includes at least one subagent delegation item for cross-checking or concept exploration.

## 6. Key Insight: Problem Reassessment

The rubric was written when BB(6) was believed to be ~10^36,534. However, as of June 2025, the record stands at **2↑↑↑5** (pentation level), discovered by mxdys. This is so vastly larger than any computable number that:
- Simple Python simulation cannot verify it (would take longer than the age of the universe)
- Verification requires algebraic proof of the TM's behavior, not step-by-step simulation
- "Beating the record" via random search is effectively impossible

This fundamentally changes the project approach: rather than trying to beat the current record, we should focus on understanding the search landscape, reproducing known results with acceleration, and potentially finding interesting new machines in subspaces that haven't been thoroughly explored.
