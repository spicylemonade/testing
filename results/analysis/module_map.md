# Module Map

Generated for rubric `item_001`.

## Repo-Level Wiring

| Module | Purpose | Inputs | Outputs / Generated Artifacts | Dependencies |
| --- | --- | --- | --- | --- |
| `.archivara/concept_evolve.py` | Structured concept exploration orchestrator that launches Codex child agents for `evolve`, `probe`, `reframe`, `iterate`, and `walk`. | CLI command, task/topic string, `OPENAI_API_KEY`, `CODEX_HOME`, existing context files under `results/research_context.md`, `results/literature/`, `results/swarm/`, and later `results/verification/`. | `results/concept_evolve/evolve_results.json`, `probe_result.json`, `reframings.json`, `bridge_candidates.json`, `recurrent_state.json`, `concept_delta.json`, `walk_session.json`, plus `results/concept_evolve/tree/index.json`, `adjacency.json`, `walk_paths.json`, concept subfolders, `.debug/`, `.state/`. | External `codex` CLI, local repo context, prior-art artifacts, verification artifacts, filesystem locking, Python stdlib. |
| `.archivara/semantic_scholar.py` | Literature search / citation graph / BibTeX helper for Semantic Scholar. | CLI subcommand, query or `paperId`, optional API key (`S2_API_KEY` / `SEMANTIC_SCHOLAR_API_KEY`), cache + manifest paths. | Query payloads printed or saved by caller, cache files under `.archivara/cache/semantic_scholar/`, updated `results/literature/semantic_scholar_manifest.json`, BibTeX text for `sources.bib`. | Semantic Scholar Graph API, local cache, manifest state, Python stdlib networking. |
| `results/literature/` | Canonical literature memory for the run: watchlist, novelty guardrails, search manifest, snapshot, gap probes, graph exports. | Seed queries, Semantic Scholar results, web/manual curation, researcher notes. | `literature_snapshot.json`, `semantic_scholar_manifest.json`, `prior_art_watchlist.md`, `prior_art_gap.md`, `gap_frontier.*`, seed/gap query dumps. | `.archivara/semantic_scholar.py`, researcher curation, web evidence, later verification packets. |
| `results/swarm/` | Multi-agent hypothesis planning and governance outputs from the orchestrator stage. | Prior literature context, novelty guardrails, child-agent synthesis. | `director_brief.md`, `hypotheses.json`, `tool_plan.md`, `falsifier.md`, plus bridge / negative-space memos. | `results/literature/*`, orchestrator agent, later researcher branch selection. |
| `results/verification/` | Specialist audit packet for novelty, citations, benchmarks, and final verification. Currently absent at run start. | Executed branch artifacts, experiment logs, bibliography, baseline sheets, prior-art gap records. | `novelty_report.md`, `citation_audit.md`, `benchmark_report.md`, `verification_summary.md`. | Researcher experiment outputs, `sources.bib`, `results/literature/*`, `results/swarm/*`, and `concept_evolve.py iterate`. |

## `.archivara/concept_evolve.py`

### Commands

| Command | Immediate Inputs | Expected Artifacts |
| --- | --- | --- |
| `evolve` | topic string; repo context files in `results/research_context.md`, `results/literature/prior_art_watchlist.md`, `results/literature/novelty_guard.json`, `results/literature/semantic_scholar_manifest.json` | `concept_cards.json`, `semantic_bridge.json`, `introspection.json`, `steering_directions.json`, `tree/index.json`, `tree/adjacency.json`, `tree/walk_paths.json`, concept folders with `concept.json`, `README.md`, `literature.json` |
| `probe` | bottleneck string; same persistent context | `probe_result.json` |
| `reframe` | problem string; prior context plus `probe_result.json` when present | `reframings.json` |
| `iterate` | problem string; prior concept artifacts and verification outputs when present | `bridge_candidates.json`, `concept_delta.json`, `recurrent_state.json` |
| `walk` | optional seed + depth | `walk_session.json` derived from `tree/walk_paths.json` and `tree/index.json` |

### Internal Wiring

- Child-run orchestration lives in `_run_sub_agent()`.
- Context fingerprinting lives in `_build_operation_fingerprint()` and `_operation_context_paths()`.
- Artifact freshness and caching are managed by `_load_cached_*()` helpers plus `.state/` JSON files.
- Post-processing from `semantic_bridge.json` into `tree/adjacency.json` and `tree/walk_paths.json` is handled locally by `_adjacency_from_bridge()` and `_walk_paths()`.
- `results/verification/verification_summary.md`, `novelty_report.md`, `benchmark_report.md`, and `citation_audit.md` are optional inputs for `probe`, `reframe`, and especially `iterate`, which means Phase 5 verification feeds back into concept evolution.

## `.archivara/semantic_scholar.py`

### Commands

| Command | Inputs | Outputs |
| --- | --- | --- |
| `search` | free-text query, `--limit`, `--skip-known`, optional `--save` | list of paper records |
| `citations` | `paperId`, `--limit`, `--skip-known`, optional `--save` | citing-paper list |
| `references` | `paperId`, `--limit`, `--skip-known`, optional `--save` | cited-paper list |
| `recommend` | one or more `paperId`s, `--limit`, `--skip-known`, optional `--save` | recommendation list |
| `graph` | free-text query, `--roots`, `--fanout`, `--skip-known`, optional `--save` | graph JSON with nodes, edges, recommendations |
| `bibtex` | `paperId` | BibTeX entry text |

### Persistent State

- Cache path defaults to `.archivara/cache/semantic_scholar/`.
- Manifest path defaults to `results/literature/semantic_scholar_manifest.json`.
- Every command appends query stats and seen paper IDs into the manifest through `_record_manifest()`.
- `--skip-known` is implemented against manifest paper IDs, so the manifest is the run's literature memory and must not be reset mid-project.

## `results/literature/`

### Current Roles

- `prior_art_watchlist.md`: nearest neighboring literature, even when some hits are noisy.
- `prior_art_gap.md`: manual differentiation / pivot ledger that should turn the watchlist into evidence-backed pass/fail calls.
- `novelty_guard.json`: watchlist metadata and guardrails for avoiding novelty collapse.
- `semantic_scholar_manifest.json`: canonical log of what has already been searched.
- `literature_snapshot.json`: synthesized literature picture; currently seeded from poor broad-query hits and needs focused repair.
- `gap_frontier.*`, `seed_search.json`, `gap_probe_*.json`, `literature_graph.json`: saved search byproducts.

### Upstream / Downstream Dependencies

- Upstream: `.archivara/semantic_scholar.py`, web evidence, researcher curation.
- Downstream: `results/swarm/*`, `sources.bib`, baseline justification, novelty audit, citation audit, final writeup.

## `results/swarm/`

### Current Roles

- `director_brief.md`: selects `H1` as champion, `H2` as backup, and makes "cellar automata" default to a `cellular automata` interpretation unless evidence proves otherwise.
- `hypotheses.json`: machine-readable descriptions of `H1`, `H2`, and `H3`, including novelty claims, evidence plans, and kill rules.
- `tool_plan.md`: operational governance and benchmark rules.
- `falsifier.md`: explicit failure modes, benchmark traps, and closest prior-art pressure.

### Dependencies

- Upstream: `results/literature/*` and orchestrator child-agent outputs.
- Downstream: researcher branch choice, benchmark design, Phase 3 selection memo, verification audits.

## `results/verification/`

### Planned Roles

- `novelty_report.md`: does the active branch stay materially distinct from the watchlist and exact Hadamard baselines?
- `citation_audit.md`: do load-bearing claims have exact supporting sources with no padding?
- `benchmark_report.md`: are baselines representation- and seed-matched?
- `verification_summary.md`: final pass/fail gate aggregating the specialist audits.

### Dependencies

- Upstream: experiment matrices, baseline sheets, literature snapshot, prior-art gap file, and `sources.bib`.
- Downstream: final branch memo, reproducibility packet, `concept_evolve.py iterate`.

## Gaps Exposed By The Map

- `concept_evolve.py` had a stale `evolve -> _run_sub_agent()` call signature and required a local fix before the mandated exploration run could execute.
- `results/verification/` does not exist yet, but multiple modules already treat it as a required later-stage input.
- `results/literature/literature_snapshot.json` is structurally present but semantically weak because the seed query was too noisy; Phase 1 needs a focused rebuild, not a reset.
