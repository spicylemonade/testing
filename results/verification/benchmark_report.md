# Benchmark Report

Date: 2026-03-13
Owner role: `benchmark_auditor`
Verification phase: `post_researcher`
Active hypothesis: `H1`
Bound-moving threshold: independently verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof
Rubric anchors:
- `item_006`
- `item_007`
- `item_008`
- `item_016`
- `item_017`
- `item_018`
- `item_019`
- `item_020`

Reviewed artifacts:
- `research_rubric.json`
- `results/research_context.md`
- `results/swarm/falsifier.md`
- `results/plans/phase2_baseline_sheet.md`
- `results/plans/phase3_route_sheet.md`
- `results/plans/phase4_evaluation_sheet.md`
- `results/plans/ramsey_research_program.md`
- `results/verification/h1_acceptance_contract.md`
- `results/verification/evaluation_rehearsal.md`
- `results/verification/verification_summary.md`
- `results/concept_evolve/probe_result.json`
- `results/concept_evolve/reframings.json`
- `results/concept_evolve/bridge_candidates.json`
- workspace artifact checks for `results/h1/*`, proof/certificate outputs, replay metadata, and benchmark manifests

## Audit Verdict

The benchmark packet is specification-complete enough to block obvious proxy claims, but the executed evidence is still benchmark-empty.
No publication-quality claim is supported today for lower-bound progress, upper-bound progress, `H1` structural intermediate evidence, or `H2`/`H3` certificate-path gains.
The current record supports only a constrained no-go or planning memo.

## Observed Evidence State

- `results/h1/` does not exist, so none of the planned `Rung 0` to `Rung 3` artifacts are present.
- No local `frontier_parent`, `extension_case`, or `failure_witness` corpus exists.
- No independent `44`-vertex witness verifier output exists.
- No machine-readable `45`-vertex residue, proof log, checker output, or replay ledger exists.
- No frozen benchmark manifest exists beyond policy text in the planning documents.
- The current generated outputs are ConceptEvolve probe/reframe/bridge packets and verification memos. Those sharpen validation plans, but they are not benchmark results.

## Findings

### 1. Missing executed baselines

- The prior-work matrix is specified, but no executed comparison table instantiates the required rows for Exoo 1989, Ge et al. 2022, Lehavi 2024, Aija'am 2010, McKay-Radziszowski 1992, Angeltveit-McKay 2018, Angeltveit-McKay 2024, or Gauthier 2025.
- No row currently records all of: `shared comparison object`, baseline artifact path, matched-compute tuple, result type, and replay path.
- No neutral-start lower-bound baseline exists.
- No non-Exoo seed-family baseline exists.
- No split-vertex/transverse-edge gluing baseline has been reproduced locally under the fixed compute tuple.
- No solved smaller certificate case has been reproduced, so future `H2` or `H3` gains would have no trusted ladder anchor.

Falsifiable requirement:

1. Before any headline comparison, create one frozen benchmark row per named comparator with `shared comparison object`, artifact path, compute tuple, result type, and replay path populated.
2. Reject any comparison row with a missing field rather than filling it post hoc.

### 2. Missing `H1` controls

- `Rung 0` has not been executed: no `results/h1/frontier_parents.jsonl`, `results/h1/extension_cases.jsonl`, or `results/h1/failure_witnesses.jsonl`.
- The decisive negative controls are absent: no `anti_exoo_holdout`, no family-balance audit, no witness-survival matrix, and no replay metadata.
- The repo still lacks the orbit-distinct `42 -> 43` extension enumerator and the independent witness verifier needed to validate any future atlas claim.
- The current ConceptEvolve outputs only state expected signals such as `>= 30 percent` top-core coverage, `>= 50 percent` held-out retention, and zero witness kills; none of those thresholds has been tested on actual artifacts.

Falsifiable requirement:

1. Materialize the three `Rung 0` files across at least 3 non-isomorphic parent families.
2. Freeze family labels before tuning and run leave-one-parent-out on the most non-Exoo-like family.
3. Demote `H1` immediately if held-out coverage is `< 50 percent` of training-side coverage, if one family supplies `> 50 percent` of recurring-core support, or if any known `42`- or `43`-vertex witness is deleted.

### 3. Missing ablations

- No per-filter on/off ablations exist, even though the route contract requires them before any scale-up.
- No canonicalization ablation exists to show that recurrence is not inflated by symmetry representatives or encoding noise.
- No provenance or seed-diversification ablation exists to test whether the same cores survive Exoo-like, asymmetric, and alternative parent families.
- No `H2` ablation separates decomposition choice from clause learning, symmetry reduction, or learned-kernel reuse.
- No `H3` ablation tests proof-carrying reuse on versus off under the same proof format and branch family.

Falsifiable requirement:

1. For every filter, core, kernel, or lemma object, run `on` versus `off` on the same rung set and matched-compute tuple.
2. For `H1`, compare raw witness clustering versus canonicalized cores and require at least `2x` core compression with unchanged witness coverage.
3. For each `H2` primitive, benchmark the same solver and proof logger with and without the new primitive. If verified residue size does not improve, or if proof bytes or checker runtime regress, kill that primitive.

### 4. Missing error analysis

- No run-level failure-code logs exist, so there is no evidence distribution for `overfit_seed`, `non_transfer`, `witness_killed`, `rare_core_tail`, `residue_only`, `uncheckable_proof`, `proof_bytes_regression`, or `checker_runtime_regression`.
- No uncovered-tail analysis exists for failures outside the dominant core set.
- No family-level contribution analysis exists to show whether support is broad or lineage-carried.
- No upper-bound regression analysis exists for proof size, checker runtime, or exactness failure.

Falsifiable requirement:

1. Every run must emit exactly one closed-taxonomy failure code.
2. Summarize failure counts by family, rung, and ablation condition before making any claim.
3. If the first atlas pass leaves a long uncovered tail with no dominant second cluster, record `rare_core_tail` and stop scaling instead of tuning around it.

### 5. Missing stress tests

- The planned fastest invalidators have not been run: `anti_exoo_holdout`, `witness_pressure`, and `rare_core_tail`.
- No smaller solved certificate case has been replayed outside the generating workflow.
- No cross-branch or cross-family replay exists for certificate-carrying reuse.
- No stale-baseline stress test exists to show that tuning privileges, warm starts, cached clauses, or symmetry priors stayed matched between baseline and candidate.

Falsifiable requirement:

1. Run the Phase 4 ladder in order and do not authorize expansion before `Rung 0` to `Rung 3` complete with artifacts.
2. Reproduce at least one smaller solved certificate case with input hash, artifact hash, checker version, and pass/fail result before any `n=45` upper-bound claim.
3. Keep `H3` as infrastructure unless replay on held-out branches reduces checked proof size or checker runtime.

## Publication-Quality Claim Status

- `improves bound`: unsupported. No verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof exists.
- `H1` structural intermediate result: unsupported. None of the required `results/h1/*` artifacts or numeric thresholds exists.
- `improves certificate path`: unsupported. No residue artifact, proof object, replay plan, or checker output exists.
- `H2` non-equivalence claim: unsupported. No solved-rung benchmark versus split-vertex/transverse-edge gluing exists.
- `H3` transfer claim: unsupported. No cross-branch replay artifact or checked proof-cost reduction exists.

## Minimal Next Benchmark Packet

1. `results/h1/frontier_parents.jsonl`, `results/h1/extension_cases.jsonl`, and `results/h1/failure_witnesses.jsonl`
2. `results/h1/obstruction_cores.jsonl` and `results/h1/atlas_summary.md`
3. `results/h1/transfer_records.jsonl` with explicit held-out coverage numbers
4. `results/h1/witness_safety_audit.md` with per-filter ablations and witness-survival rows
5. One frozen benchmark manifest covering every named prior-work row and the full matched-compute tuple
6. External replay artifacts: input hash, artifact hash, checker version, and pass/fail result

Until that packet exists, benchmark evidence is insufficient for publication-quality claims.
