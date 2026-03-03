# Repository Module Map

This map covers all requested non-vendor modules and artifact roots.

## Python orchestration modules (`.archivara/*.py`)

| Module | Purpose | Inputs | Outputs | Connection |
| --- | --- | --- | --- | --- |
| `.archivara/concept_evolve.py` | Builds concept backlog via `evolve/probe/reframe/walk`; materializes concept folders. | Topic/problem text; optional seed/depth; Semantic Scholar helper. | `results/concept_evolve/*.json`, `results/concept_evolve/tree/*`, `summary.txt`. | `TASK_researcher_attempt_1.md` -> `.archivara/concept_evolve.py` -> `results/concept_evolve/tree/index.json` |
| `.archivara/semantic_scholar.py` | Queries papers/citations/references/recommendations and exports BibTeX. | Query text or paper IDs. | JSON payloads and BibTeX text for `sources.bib`. | `results/literature/search_log.md` -> `.archivara/semantic_scholar.py` -> `sources.bib` |

## Tool wrappers (`.opencode/tools/*.ts`)

| Module | Purpose | Inputs | Outputs | Connection |
| --- | --- | --- | --- | --- |
| `.opencode/tools/concept_evolve.ts` | Exposes ConceptEvolve Python CLI as OpenCode tool wrapper. | Tool args: command/topic/seed/depth. | Process output from Python script. | `OpenCode tool call` -> `.opencode/tools/concept_evolve.ts` -> `.archivara/concept_evolve.py` |
| `.opencode/tools/semantic_scholar.ts` | Exposes Semantic Scholar Python CLI as OpenCode tool wrapper. | Tool args: command/query/limit. | JSON-formatted search/citation results. | `OpenCode tool call` -> `.opencode/tools/semantic_scholar.ts` -> `.archivara/semantic_scholar.py` |

## Subagent definitions (`.opencode/agents/*.md`)

| Module | Purpose | Inputs | Outputs | Connection |
| --- | --- | --- | --- | --- |
| `.opencode/agents/literature-graph-miner.md` | Configures citation-graph mining behavior for subagent work. | Literature prompts and web tools. | Citation chains and actionable leads. | `results/literature/*` -> `literature-graph-miner` -> `results/literature/subagent_phase1/synthesis.md` |
| `.opencode/agents/concept-tree-explorer.md` | Configures concept-tree traversal and backlog prioritization behavior. | Concept tree folders and prompts. | Candidate next experiments and missing links. | `results/concept_evolve/tree/*` -> `concept-tree-explorer` -> `results/concept_evolve/tree/retrospective.md` |

## Root documentation and control files

| Module | Purpose | Inputs | Outputs | Connection |
| --- | --- | --- | --- | --- |
| `README.md` | Minimal project entry point (currently placeholder). | Reader context. | Project overview. | `README.md` -> planned `results/final/reproducibility.md` |
| `TASK_researcher_attempt_1.md` | Execution protocol for ordered rubric-driven research workflow. | User task and constraints. | Operating instructions for agent execution. | `TASK_researcher_attempt_1.md` -> `research_rubric.json` |
| `research_rubric.json` | Canonical 5-phase, 25-item tracker with acceptance criteria. | Progress state updates and notes. | Frontend-visible status and summary counters. | `research_rubric.json` -> all `results/*` deliverables |
| `.archivara/opencode.json` | Tool and agent permission/config contract for this workspace. | Provider env vars and tool policy. | Enabled command surface for orchestrator/researcher/writer/reviewer. | `.archivara/opencode.json` -> `.opencode/tools/*.ts` and `.opencode/agents/*.md` |

## Artifact roots

| Module | Purpose | Inputs | Outputs | Connection |
| --- | --- | --- | --- | --- |
| `results/` | Stores structured research artifacts for all rubric phases. | Script outputs, metric files, markdown analyses. | Phase-specific JSON/CSV/MD assets. | `simulation + analysis scripts` -> `results/` -> `results/final/findings.md` |
| `figures/` | Stores publication-grade visual outputs (PNG/PDF). | Metrics and experiment aggregates. | `*.png` and `*.pdf` figures at 300 DPI. | `results/experiments/*` -> `figures/*` -> `results/final/findings.md` |
