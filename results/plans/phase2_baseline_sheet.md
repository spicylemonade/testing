# Phase 2 Baseline Sheet

Date: 2026-03-13
Scope: Phase 2 baseline implementation and metrics for `R(5,5)`

## 1. Executable Baseline Stack

| Planned activity | Existing utility or document | Immediate output | Logged blocker |
| --- | --- | --- | --- |
| Frontier and prior-work refresh | `.archivara/semantic_scholar.py`, `results/literature/literature_snapshot.json`, `results/literature/semantic_scholar_manifest.json`, `results/swarm/phase1_cleanup.md` | Fixed Ramsey corpus and citation path | No widening until the fixed corpus is exhausted |
| Concept branching | `.archivara/concept_evolve.py`, `results/concept_evolve/tree/`, `results/concept_evolve/walk_session.json` | Concept folders, walk paths, and route tags | Further branching blocked until `Rung 0` frontier reconstruction exists |
| Route governance | `results/swarm/hypotheses.json`, `results/swarm/director_brief.md`, `results/swarm/tool_plan.md`, `results/swarm/falsifier.md`, `results/plans/ramsey_research_program.md` | `H1/H2/H3` ordering and kill rules | None |
| Lower-bound baseline design | Exoo 1989, Ge et al. 2022, Lehavi 2024, `results/plans/ramsey_research_program.md` | Witness standards and search-effort normalization | No repo-local `frontier_parent` corpus or independent witness verifier |
| Upper-bound baseline design | McKay-Radziszowski 1992, Angeltveit-McKay 2018 and 2024, Gauthier 2025, `results/plans/ramsey_research_program.md` | Residue and certificate metrics | No repo-local residue reducer or proof checker |
| Novelty and overlap control | `results/literature/prior_art_gap.md`, `results/literature/prior_art_watchlist.md`, `results/swarm/phase1_cleanup.md` | Ramsey-specific overlap checks and lexical-noise exclusions | Keep watchlist noise out of baseline claims |
| Citation packaging | `sources.bib`, `results/literature/literature_snapshot.json` | Bibliography coverage for planned claims | Verification citations not yet materialized |

## 2. Indispensable Missing Tools To Log, Not Implement Ad Hoc

- No existing repo utility materializes the `frontier_parent`, `extension_case`, and `failure_witness` corpus required for `Rung 0`.
- No existing repo utility enumerates orbit-distinct `42 -> 43` extensions.
- No existing repo utility independently verifies a `44`-vertex witness.
- No existing repo utility checks a machine-readable `45`-vertex impossibility certificate.

## 3. Baseline Governance Pointer

- `results/plans/ramsey_research_program.md` remains the source of truth for route arbitration, metric definitions, exact ladder order, and claim grammar.
- This sheet exists to make the executable baseline stack auditable without reopening the full program document.
