# Repository Control-Plane Map

## Scope

This repository is a research control plane for the bounded-difference question on the greedy array `T`, not yet a mature experiment package.

At the start of the researcher run:
- `.archivara/semantic_scholar.py` existed as the literature-memory and graph-traversal helper.
- `.archivara/concept_evolve.py` existed as the structured concept-tree orchestrator.
- `results/literature/` existed with seed searches, a literature snapshot, and novelty guardrails.
- `results/swarm/` existed with hypothesis selection, falsifier notes, and tool-budget guidance.
- `results/verification/` existed as an empty artifact family placeholder.
- `results/concept_evolve/tree/` did not exist yet.
- no baseline generator, benchmark harness, or reusable experiment package existed yet.

## Major Modules And Artifact Families

### `research_rubric.json`

The run controller. It defines the five research phases, the item-by-item acceptance criteria, and the required output artifacts. The researcher should treat it as the authoritative execution ledger.

### `.archivara/semantic_scholar.py`

The literature ingestion and memory layer.

Responsibilities:
- execute targeted Semantic Scholar search, citation, reference, recommendation, and graph queries;
- cache responses locally;
- update `results/literature/semantic_scholar_manifest.json` so repeated searches can be avoided;
- emit structured JSON and BibTeX for downstream artifacts.

Inputs:
- command-line query terms or paper IDs;
- existing manifest state and local cache.

Outputs:
- saved JSON under `results/literature/`;
- manifest updates in `results/literature/semantic_scholar_manifest.json`;
- BibTeX text for `sources.bib`.

### `.archivara/concept_evolve.py`

The concept-exploration orchestrator. It launches Codex child agents for `evolve`, `probe`, `reframe`, and `iterate`, tracks watched artifacts, and records run state under `results/concept_evolve/.state/`.

Inputs:
- the current research prompt;
- saved context from `results/research_context.md`, `results/literature/*`, `results/swarm/*`, and later `results/verification/*`.

Outputs:
- concept artifacts under `results/concept_evolve/`;
- a concept tree under `results/concept_evolve/tree/`;
- run-state diagnostics under `results/concept_evolve/.state/` and `.debug/`.

Operational note:
- the helper shipped with a broken `evolve()` call signature and was patched in this run before the mandatory concept-evolve step could execute.

### `results/literature/`

The literature and provenance memory.

Current contents:
- `literature_snapshot.json`: current literature inventory;
- `semantic_scholar_manifest.json`: canonical query history and known-paper memory;
- `prior_art_watchlist.md`: closest surfaced overlaps, even when noisy;
- `prior_art_gap.md`: differentiation ledger to maintain as research proceeds;
- `gap_frontier.md` and related JSON: gap-first search stubs;
- query result dumps such as `seed_search.json`, `gap_probe_*.json`, and `literature_graph.json`.

Role in the pipeline:
- feeds provenance, overlap checks, and citation targets into problem framing and novelty control;
- should be extended in place rather than restarted from scratch.

### `results/swarm/`

The strategy layer produced before the researcher handoff.

Current contents:
- `director_brief.md`: chooses `H1_frontier_witness_certificate` as champion and `H2_prime_support_fixed_point` as backup;
- `hypotheses.json`: structured claim ladder and falsifiers;
- `tool_plan.md`: budget, routing, and stop conditions;
- `falsifier.md`: adversarial acceptance bar and failure modes;
- `gap_map.md`, `hypothesis_bridge.md`, `hypothesis_negative_space.md`: additional exploratory notes.

Role in the pipeline:
- constrains what counts as valid progress;
- defines which computations are worth doing and which novelty illusions to avoid.

### `results/verification/`

The verification sink for post-implementation audits.

Expected outputs later in the run:
- `citation_audit.md`;
- `benchmark_report.md`;
- `novelty_report.md`;
- `verification_summary.md`.

Current state:
- directory exists but no finished verification artifacts were present before this researcher run.

### `results/concept_evolve/`

The concept-iteration workspace.

Current state at handoff:
- `.state/` and `.debug/` were created during the mandatory researcher run;
- `tree/` was missing initially and is supposed to be initialized by the concept-evolve workflow plus later concept-branch maintenance.

Role in the pipeline:
- stores concept cards, bridges, reframings, probes, iteration deltas, and branch-level notes that connect literature, implementation, and verification.

## Data Flow

1. `research_rubric.json` defines the required artifacts and acceptance criteria.
2. `results/swarm/` supplies the active hypothesis ladder, failure modes, and stop conditions.
3. `results/literature/` supplies provenance memory and prior-art differentiation targets.
4. `.archivara/concept_evolve.py` reads those artifacts and writes exploratory concept outputs under `results/concept_evolve/`.
5. The missing baseline generator and benchmark harness must then be created by the researcher so the hypotheses can be tested on a reproducible corpus.
6. Those experiments will feed `results/verification/` and update the novelty ledger in `results/literature/prior_art_gap.md`.
7. The refreshed results then flow back into `results/research_context.md` and the concept tree for final synthesis.

## Gaps That Matter Before Core Research

- There is no checked-in implementation of the recurrence.
- There is no witness-log schema or benchmark harness.
- There is no existing reproducible path from the swarm notes to a machine-readable record-gap corpus.
- There was no initialized concept tree before the current run.

Those absences are not bookkeeping details; they are the main blockers between the swarm strategy and any defensible boundedness claim.
