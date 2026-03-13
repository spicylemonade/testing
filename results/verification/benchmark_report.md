# Benchmark Report

Date: 2026-03-13
Owner role: `benchmark_auditor`
Verification phase: `review_round_1`
Active hypothesis: `H1`
Bound-moving threshold: independently verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof

Reviewed artifacts:
- `research_rubric.json`
- `results/research_context.md`
- `results/swarm/falsifier.md`
- `results/plans/phase2_baseline_sheet.md`
- `results/plans/phase3_route_sheet.md`
- `results/plans/phase4_evaluation_sheet.md`
- `results/verification/verification_summary.md`
- `results/verification/h1_acceptance_contract.md`
- `results/verification/evaluation_rehearsal.md`
- `results/verification/final_review.md`
- `results/concept_evolve/probe_result.json`
- `results/concept_evolve/recurrent_state.json`
- `research_paper.tex`
- local artifact checks for `results/h1/*`, benchmark manifests, proof or certificate outputs, and replay metadata

## Review-Round Verdict

Benchmark evidence is still execution-empty for publication-quality empirical claims.
The safe manuscript scope remains infrastructure-only plus negative-result or no-go framing.
No executed baseline, control, ablation, error-analysis, or stress-test packet currently supports `improves bound`, `improves certificate path`, or an achieved `H1` structural intermediate result.

## Current Evidence State

- `results/h1/` is absent, so the planned `frontier_parent`, `extension_case`, `failure_witness`, `obstruction_core`, `transfer_record`, `atlas_summary`, and `witness_safety_audit` artifacts are all missing.
- The manuscript's own measurement table records `0/7` planned `H1` evidence artifacts present, `0/4` ladder rungs completed, `0/8` named benchmark rows instantiated, and `0/2` bound-moving artifacts present.
- The executed outputs that do exist are route-selection and governance artifacts: ConceptEvolve `evolve`, `walk`, and `iterate` outputs, the Phase 3 route stress test, the evaluation rehearsal, and the verification packet.
- `research_paper.tex` states explicitly that no bound-search experiment was executed for the manuscript.

## Missing Executed Baselines

- No instantiated comparison row exists for Exoo 1989, Ge et al. 2022, Lehavi 2024, Aija'am 2010, McKay-Radziszowski 1992, Angeltveit-McKay 2018, Angeltveit-McKay 2024, or Gauthier 2025.
- No row currently contains the full matched-compute tuple, shared comparison object, artifact path, result class, and replay path.
- No neutral-start recovery baseline exists for lower-bound work.
- No non-Exoo or deliberately asymmetric seed-family baseline exists.
- No local reproduction of the split-vertex or transverse-edge-gluing upper-bound baseline exists.
- No smaller solved certificate case has been replayed locally.

Publication blocker:

- Without at least one executed row per named comparator, any benchmark claim is stale-baseline or apples-to-oranges by construction.

Falsifiable recommendation:

1. Freeze a versioned benchmark manifest with mandatory columns: comparator, shared comparison object, artifact path, matched-compute tuple, result class, and replay path.
2. Reject any row with a blank column instead of backfilling it after tuning.
3. Reproduce at least one lower-bound baseline and one smaller solved upper-bound certificate case under that manifest before comparing new methods.

## Missing Controls

- `Rung 0` has not been executed, so there is no local frontier corpus reconstructed from the Exoo, Ge, and Lehavi line.
- Because the corpus is absent, the decisive `anti_exoo_holdout`, family-balance audit, and witness-oracle safety checks cannot yet be run.
- The repo still lacks the orbit-distinct `42 -> 43` extension enumerator, an independent `44`-vertex witness verifier, and a `45`-vertex certificate checker.
- No current artifact demonstrates coverage across at least 3 non-isomorphic parent families.

Publication blocker:

- `H1` cannot be evaluated as a structural object until the route has a real corpus and safety oracle instead of only a planned schema.

Falsifiable recommendation:

1. Materialize `results/h1/frontier_parents.jsonl`, `results/h1/extension_cases.jsonl`, and `results/h1/failure_witnesses.jsonl` for at least 3 non-isomorphic parent families.
2. Freeze family labels before tuning.
3. Run leave-one-parent-out on the most non-Exoo-like family and demote `H1` immediately if held-out retention is `< 50 percent`, if any family contributes `> 50 percent` of accepted support, or if any stored `42`- or `43`-vertex witness is deleted.

## Missing Ablations

- No per-filter `on` versus `off` ablations exist for core-derived pruning rules.
- No raw-witness-versus-canonical-core ablation exists to show that recurrence survives canonicalization instead of being created by it.
- No provenance or seed-diversification ablation exists to distinguish Exoo-line memorization from cross-family structure.
- No `H2` ablation separates decomposition choice from clause learning, symmetry reduction, or learned-kernel reuse.
- No `H3` ablation tests certificate-carrying reuse `on` versus `off` under the same proof format and branch family.

Publication blocker:

- Without these ablations, any claimed gain can still be attributed to representation changes, seed privilege, or solver engineering rather than a Ramsey structural object.

Falsifiable recommendation:

1. For `H1`, run raw versus canonical and filter `off` versus `on` on the same rung set and compute tuple.
2. Require at least `2x` core compression with unchanged witness coverage before claiming canonicalization helps.
3. If `H2` or `H3` is reopened, benchmark each primitive against the exact same solver, proof logger, and decomposition with only the target primitive toggled.

## Missing Error Analysis

- The failure-code taxonomy is defined, but no executed run emits closed failure codes.
- No summary exists by family, rung, and ablation condition.
- No uncovered-tail analysis exists for failures outside the dominant core set.
- No upper-bound regression report exists for proof bytes, checker runtime, exactness failure, or replay failure.

Publication blocker:

- Without run-level failure accounting, the packet cannot distinguish a reusable pattern from overfit, non-transfer, or unsound pruning.

Falsifiable recommendation:

1. Every executed run must emit exactly one failure code from the fixed taxonomy.
2. Summarize counts by family, rung, and ablation condition before any claim is upgraded.
3. If the first atlas pass leaves a long uncovered tail with no dominant second cluster, record `rare_core_tail` and stop scaling instead of tuning around it.

## Missing Stress Tests

- The decisive invalidators `anti_exoo_holdout`, `witness_pressure`, and `rare_core_tail` are defined but unrun.
- No stale-baseline stress test has verified that warm starts, cached clauses, symmetry priors, and tuning privileges were matched.
- No external replay has reproduced a witness or proof artifact outside the generating workflow.
- No smaller solved case has been used as a certificate-ladder anchor.

Publication blocker:

- The current packet has no executed adversarial checks that could falsify the route under the project's own stop rules.

Falsifiable recommendation:

1. Execute the Phase 4 ladder in order: `Rung 0`, then `Rung 1` plus `rare_core_tail`, then `Rung 2` plus `anti_exoo_holdout`, then `Rung 3` plus per-filter ablations.
2. Block any `H2`, `H3`, or upper-bound certificate-path claim until at least one smaller solved case is replayed with input hash, artifact hash, checker version, and pass or fail result.
3. Treat missing replay metadata as immediate demotion to `intermediate evidence` or `residue_only`.

## Publication-Quality Claim Status

- `improves bound`: unsupported. No verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof exists.
- `H1` structural intermediate result: unsupported. The full `results/h1/*` control packet is absent, so the 3-family, `>= 30 percent` coverage, `>= 50 percent` held-out retention, and zero-witness-kill gates are untested.
- `improves certificate path`: unsupported. No machine-readable residue, proof log, checker output, or replay ledger exists.
- `H2` non-equivalence claim: unsupported. No matched-baseline reproduction versus the split-vertex or transverse-edge-gluing line exists.
- `H3` transfer claim: unsupported. No proof-format-stable, cross-branch reuse result exists.

## Minimal Benchmark Packet Before Any Stronger Claim

1. A versioned benchmark manifest with one executed row per named comparator.
2. `results/h1/frontier_parents.jsonl`, `results/h1/extension_cases.jsonl`, and `results/h1/failure_witnesses.jsonl` spanning at least 3 non-isomorphic families.
3. `results/h1/obstruction_cores.jsonl` and `results/h1/atlas_summary.md` with explicit coverage numbers.
4. `results/h1/transfer_records.jsonl` with held-out retention on the decisive anti-Exoo family.
5. `results/h1/witness_safety_audit.md` with per-filter `on` versus `off` ablations and zero witness kills.
6. External replay artifacts for at least one smaller solved certificate case and any future bound-moving artifact.

Until that packet exists, the evidence is insufficient for publication-quality empirical claims.
The current paper is benchmark-safe only as a constrained no-go or route-specification memo.
