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

## 3. Lower-Bound Baseline Metrics And Witness Standards

Lower-bound work counts as bound progress only if it yields an independently verified `44`-vertex witness.

Required metrics:

1. Witness recovery from neutral starts, not only Exoo-like seeds or hand-picked warm starts.
2. Family diversity beyond Exoo-like seeds, tracked by non-isomorphic parent families that contribute candidate improvements.
3. Witness-safety under filters: every pruning or screening rule must be tested against all known `42`- and `43`-vertex witnesses before it is trusted.
4. Equalized search effort, including edge flips, neighborhood evaluations, SAT or LP calls, and wall-clock budget.
5. Failure-mode logging with explicit reasons such as overfit seeds, transfer collapse, unsound pruning, or stalled defect reduction.
6. Held-out transfer score for any learned obstruction object, so proxy defect gains do not masquerade as structural progress.

Witness standards:

- Any candidate `44`-vertex witness must be recoverable from a seed-neutral run or from multiple distinct parent families.
- The stored artifact must include provenance, canonical labeling metadata, and the exact checker used for independent validation.
- If the candidate cannot be independently revalidated outside the generating workflow, it is intermediate evidence only.

## 4. Upper-Bound Baseline Metrics And Certificate Standards

Upper-bound work counts as bound progress only if it yields a machine-checkable `45`-vertex impossibility proof.
A residue with a clear certificate path counts only as certificate-path progress or intermediate evidence.

Required metrics:

1. Verified residue size after decomposition and pruning.
2. Proof bytes or certificate size for every impossibility claim.
3. Checker runtime on the emitted proof or residue certificate.
4. Exactness or rationalization status of each impossibility step.
5. Matched-baseline runtime against the split-vertex and transverse-edge gluing line.
6. Transferability of any learned kernel, obstruction, or lemma object across decomposition families.

Certificate standards:

- Smaller residues without a certificate path count as intermediate evidence, not an upper-bound improvement.
- Solver speed alone does not count unless the emitted residue or proof object is also improved under matched conditions.
- A `clear certificate path` is valid only if the artifact includes a machine-readable residue, residue hash, remaining-open-case count, target proof format, checker name and version, and an exact replay plan.
- Every accepted upper-bound artifact must record the checker, proof format, and whether rational reconstruction or exact replay is still pending.
- Every accepted upper-bound artifact must be replayed outside the generating workflow, with input hash, artifact hash, checker version, and pass/fail result recorded.
- Every upper-bound primitive must reproduce at least one solved smaller certificate case before it is trusted on `R(5,5)` upper-bound claims.

## 5. Matched-Compute And No-Cheat Protocol

Every benchmark row must log a fixed matched-compute tuple:

- solver binary and version
- proof format
- preprocessing passes
- thread count
- hardware class
- timeout policy
- branch-order policy
- random-seed policy
- warm-start and cached-clause policy

No-cheat rules:

- Warm starts, oracle seeds, cached clauses, proof reuse, and hand-picked symmetry priors are allowed only if enabled for both baseline and candidate under the same rules.
- Every learned pruning object, kernel, lemma, or certificate-reuse object must have an on/off ablation on the same rung set under the same compute tuple.
- Benchmark manifests must be frozen before tuning; later additions belong to a new versioned stratum rather than the headline table.
- Every run must emit one failure code from a closed taxonomy such as `overfit_seed`, `witness_killed`, `non_transfer`, `residue_only`, `uncheckable_proof`, `exactness_failure`, `proof_bytes_regression`, or `checker_runtime_regression`.

Upper-bound win rule:

- Compare methods in the order `bound status > certificate class > verified residue size > proof bytes > checker runtime`.
- No headline claim is allowed if a higher-priority metric regresses.

## 6. ConceptEvolve First-Pass Contract

First concept exploration step after Phase 1:

- `.archivara/concept_evolve.py evolve "Improve the Ramsey number R(5,5) bound"` has already been executed and its recovery artifacts were materialized under `results/concept_evolve/`.
- `.archivara/concept_evolve.py walk --depth 4` has already been executed and saved `results/concept_evolve/walk_session.json`.

Current first-pass state:

- `results/concept_evolve/tree/` contains 11 concept folders, which clears the acceptance floor of 10.
- `results/concept_evolve/tree/index.json` maps every folder to `H1`, `H2`, or `H3`.
- Each folder contains `concept.json`, `README.md`, and `literature.json`.
- Each `concept.json` records a concrete `experiment_seed`.
- Each `concept.json` or `literature.json` records the closest prior-art packet for that concept.

Route coverage in the current tree:

- `H1`: 6 folders
- `H2`: 3 folders
- `H3`: 2 folders

No-drift rule:

- No further concept branching or promotion happens until `Rung 0` frontier reconstruction is defined.
- Later `probe`, `reframe`, and `iterate` actions must update existing folders instead of creating `_v2` clutter.

## 7. Baseline Governance Pointer

- `results/plans/ramsey_research_program.md` remains the source of truth for route arbitration, metric definitions, exact ladder order, and claim grammar.
- This sheet exists to make the executable baseline stack auditable without reopening the full program document.
