# Module Map

Date: 2026-03-13
Task: Improve the Ramsey number `R(5,5)` bound
Primary route: `H1` orbit-stable extension-obstruction atlas

## Workspace Role Split

- `README.md`
  Minimal placeholder only. It does not describe the research pipeline, so all operational meaning comes from the task files and generated artifacts instead.

- `TASK_orchestrator.md`
  Absent from the current workspace, but recoverable from `.archivara/logs/orchestrator.log` (`item_12`). Its role was to create `research_rubric.json` with five phases, force concept-tree exploration, require literature/citation maintenance, and require one multi-agent delegation round per phase.

- `TASK_researcher_attempt_1.md`
  Active researcher brief. It upgrades the rubric from planning into execution, requires reading the saved context first, mandates the `concept_evolve.py` sequence, and requires Semantic Scholar helper usage, citation maintenance, and rubric status discipline.

- `research_rubric.json`
  The run controller. It defines the 25-item execution contract, current agent ownership, and the status/notes/error fields that must be maintained item by item.

## Core Utilities

- `.archivara/semantic_scholar.py`
  Repo-local literature crawler. It searches Semantic Scholar, traverses references/citations/recommendations, exports BibTeX, caches responses in `.archivara/cache/semantic_scholar/`, and records canonical query memory in `results/literature/semantic_scholar_manifest.json`.

- `.archivara/concept_evolve.py`
  Structured concept-tree generator. It launches Codex child agents for `evolve`, `probe`, `reframe`, `iterate`, and `walk`; reads saved research/literature/swarm/verification context; and writes concept artifacts under `results/concept_evolve/` plus per-concept folders under `results/concept_evolve/tree/`.
  The local script required a runtime repair on 2026-03-13: `evolve()` was calling `_run_sub_agent()` without the required `command`, `fingerprint`, `topic`, and `watched_paths` arguments. The helper now follows the same fingerprinted execution path as `probe`, `reframe`, and `iterate`.

## Literature Layer

- `results/literature/literature_snapshot.json`
  Initial literature memory. It currently preserves a noisy lexical seed and must be extended with a Ramsey-specific review rather than replaced.

- `results/literature/prior_art_watchlist.md`
  Novelty guardrail file. It is mostly lexical-query noise, but it keeps the mandatory differentiation questions visible and must be answered explicitly in `prior_art_gap.md`.

- `results/literature/prior_art_gap.md`
  The active overlap ledger. It already kills plain GA/metaheuristic lower-bound work, plain LP/flag/SDP upper-bound work, and plain SAT/static decomposition work as standalone novelty claims.

- `results/literature/semantic_scholar_manifest.json`
  Canonical memory of what has already been searched. This is the file that prevents repeated broad searches and should drive seed expansion via references/citations/recommendations.

- `results/literature/gap_frontier.md`
  Gap-first reading list extracted from the noisy snapshot. It is useful mainly as a reminder to prefer open-problem and limitation signals over popularity-ranked lexical hits.

- `results/literature/gap_probe_1.json`
  Most useful saved Ramsey-specific query result so far. It surfaces the key `R(5,5)` sources that the initial broad snapshot missed or buried.

## Swarm Outputs

- `results/swarm/director_brief.md`
  Route selection memo. It selects `H1` as champion, `H2` as backup, and `H3` as reserve, and states the rationale and immediate handoff constraints.

- `results/swarm/hypotheses.json`
  Machine-readable hypothesis registry. It stores novelty claims, closest prior art, easiest falsifiers, and budget envelopes for `H1`, `H2`, and `H3`.

- `results/swarm/tool_plan.md`
  Governance layer. It sets strict bound-moving thresholds, bans broad exploratory compute during synthesis-only mode, and constrains what counts as valid progress for each role.

- `results/swarm/falsifier.md`
  Adversarial review of failure modes. It defines the fastest invalidators and the anti-proxy rules that later baseline and experiment specs must honor.

- `results/swarm/gap_map.md`
  Useful substitute for the missing `hypothesis_bridge.md` and `hypothesis_negative_space.md`. It records the negative-space opportunities that motivated `H1`.

## Generated / Missing Artifact Zones

- `results/concept_evolve/*`
  This directory was missing at the start of the run and is now populated in the helper schema after a manual recovery from child-agent churn. The current top-level files include `concept_cards.json`, `semantic_bridge.json`, `introspection.json`, `steering_directions.json`, `evolve_results.json`, `concept_delta.md`, `summary.txt`, and `walk_session.json`, plus 11 concept folders and graph files under `results/concept_evolve/tree/`.

- `results/verification/*`
  Present as an empty directory at run start. Later phases require at least `novelty_report.md`, `citation_audit.md`, `benchmark_report.md`, and `verification_summary.md`, and `concept_evolve.py` reads these files during `probe`, `reframe`, and especially `iterate`.

## Concrete Cross-File Dependencies

1. `.archivara/semantic_scholar.py` writes query memory into `results/literature/semantic_scholar_manifest.json`, and both the researcher brief and `concept_evolve.py` explicitly tell later searches to reuse that manifest instead of restarting from scratch.

2. `.archivara/concept_evolve.py` reads `results/research_context.md`, `results/literature/prior_art_watchlist.md`, `results/literature/prior_art_gap.md`, `results/literature/semantic_scholar_manifest.json`, `results/swarm/director_brief.md`, `results/swarm/hypotheses.json`, `results/swarm/tool_plan.md`, and `results/swarm/falsifier.md` before generating new concept artifacts.

3. `results/swarm/director_brief.md`, `results/swarm/hypotheses.json`, and `results/swarm/tool_plan.md` all converge on the same operational rule: keep `H1` active unless transfer or witness-safety tests fail, and do not open `H2`/`H3` early.

4. `research_rubric.json` item `item_009` depends on `concept_evolve.py evolve` and `walk` producing `results/concept_evolve/tree/` folders, so the ConceptEvolve outputs are not optional side artifacts; they are rubric-critical dependencies.

5. `results/literature/prior_art_gap.md` and `results/swarm/falsifier.md` jointly constrain acceptable novelty claims for every later baseline and experiment spec. A plan that ignores either file will drift back into banned "same search, better engine" territory.

6. `results/verification/verification_summary.md` is a required read target for `concept_evolve.py probe` and `reframe`, while `iterate` additionally reads `novelty_report.md`, `benchmark_report.md`, and `citation_audit.md`. That means verification artifacts are upstream inputs to later concept evolution, not just end-of-project paperwork.

7. `TASK_orchestrator.md` (recovered from log) is upstream of `research_rubric.json`, and `TASK_researcher_attempt_1.md` is upstream of how that rubric must now be executed. The task files are therefore part of the effective dependency graph even when one of them is absent from the workspace.

8. `results/literature/gap_probe_1.json`, `results/swarm/gap_map.md`, and `results/swarm/director_brief.md` all point to the same structural gap: the missing reusable object is not another search engine but a transferable obstruction atlas for failed `42 -> 43` extensions.

## Immediate Consequence

The repo is not missing a solver implementation; it is missing cleaned literature memory, explicit baseline rules, concept-tree outputs, and verification packaging around the already selected `H1` route. The rest of the rubric should therefore be executed as artifact production and route-hardening first, not as ad hoc search code.
