# Repo Map

## Key Modules And Artifact Roots

- `.archivara/semantic_scholar.py`
  - Local Semantic Scholar client for `search`, `citations`, `references`, `recommend`, `graph`, and `bibtex`.
  - Caches raw API responses under `.archivara/cache/semantic_scholar/`.
  - Treats `results/literature/semantic_scholar_manifest.json` as the canonical memory of prior queries and seen paper IDs.
- `.archivara/concept_evolve.py`
  - Child-agent orchestrator for `evolve`, `probe`, `reframe`, `iterate`, and concept-tree materialization.
  - Reads saved context from `results/research_context.md`, `results/literature/*`, and `results/swarm/*`.
  - Writes `results/concept_evolve/*` plus `results/concept_evolve/tree/*`.
- `results/literature/`
  - Stores the persistent literature snapshot, watchlist, gap notes, Semantic Scholar manifest, and graph/query artifacts.
  - This is the input memory for novelty checks and the later `sources.bib` build.
- `results/swarm/`
  - Stores branch-selection artifacts: `director_brief.md`, `hypotheses.json`, `tool_plan.md`, `falsifier.md`, and supporting bridge/gap notes.
  - These files are the current source of truth for branch order, novelty scope, and kill criteria.
- `results/verification/`
  - Intended sink for benchmark, novelty, citation, runtime, and summary audits.
  - The directory exists, but this run started with no verification files under it.

## Current Data Flow

1. `results/research_context.md` and `results/research_context.json` summarize the run state, tracked-paper counts, and verification availability.
2. `.archivara/semantic_scholar.py` expands the literature state and appends query provenance into `results/literature/semantic_scholar_manifest.json`.
3. `results/literature/*` feeds the swarm selection layer in `results/swarm/*`, which currently selects `H1_defect_syndrome_ca_64m` as champion.
4. `research_rubric.json` turns the saved context plus swarm guidance into the itemized execution plan for this researcher pass.
5. `.archivara/concept_evolve.py` consumes the same context, then later verification outputs, to grow `results/concept_evolve/tree/*` and recurrent idea state.
6. `results/verification/*` is meant to close the loop back into `results/research_context.*`, `results/literature/prior_art_gap.md`, and the final writeup artifacts.

## Current Gaps And Repair Notes

- `research_rubric.json` has no deep repo history yet.
  - `git log -- research_rubric.json` currently shows only the rubric-creation commit `52c422e`.
- `results/verification/` was empty at the start of this run.
- At the start of this pass, `.archivara/concept_evolve.py` had a real call-signature mismatch:
  - `_run_sub_agent()` required `command`, `fingerprint`, `topic`, and `watched_paths`.
  - `evolve()` called `_run_sub_agent()` without those arguments.
  - I repaired that local helper mismatch before launching the mandatory `concept_evolve.py evolve ...` run.
- There is still no tracked solver or experiment package in the repo root.
  - The repo started as orchestration plus saved notes, not as an implemented Hadamard search codebase.

## Why This Matters For Hadamard 668

- Literature and swarm artifacts already narrow the contribution claim to a seed-matched CA repair method rather than a general Hadamard-construction claim.
- The concept-evolve helper is mandatory in the rubric, so its local repair was required just to execute Phase 1 honestly.
- Because `results/verification/` was empty, later claims must be backed by new benchmark, runtime, novelty, and citation artifacts produced in this run rather than by inherited evidence.
