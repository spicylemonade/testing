# Evaluation Rehearsal

Date: 2026-03-13
Rubric item: `item_020`
Delegation roles:
- `monitor`
- `benchmark_auditor`
- `citation_auditor`
- `integrator`

## Recommended Precompute Check Order

1. Lock the route and claim class first using `results/plans/phase3_route_sheet.md` and `results/verification/verification_summary.md`.
2. Freeze the Phase 4 ladder, matched-compute tuple, win rule, failure taxonomy, and replay path using `results/plans/phase4_evaluation_sheet.md` and `results/verification/benchmark_report.md`.
3. Repair and freeze the citation packet, especially the Lehavi row and the `shared comparison object` column, using `results/verification/citation_audit.md` and the Phase 4 comparison matrix.
4. Recheck novelty before spending compute, with special attention to the `anti_exoo_holdout` risk in `results/verification/novelty_report.md`.
5. Confirm prerequisite tooling status: local `frontier_parent` corpus, orbit-distinct `42 -> 43` enumerator, independent `44`-vertex witness verifier, and `45`-vertex certificate checker.
6. Only then execute the ladder itself in dependency order: `Rung 0` reconstruction, `Rung 1` atlas plus `rare_core_tail`, `Rung 2` held-out transfer plus `anti_exoo_holdout`, and `Rung 3` witness-safety plus per-filter ablations.

## Sequencing Risks Surfaced Before Compute

1. Starting from `verification_summary.md` alone can create false confidence because it is derivative and compresses unresolved benchmark, citation, and novelty blockers.
2. Starting compute before the matched-compute tuple, win rule, and failure taxonomy are frozen triggers the stale-baseline failure mode.
3. Starting `Rung 0` before citation cleanup bakes weak provenance, especially around Lehavi 2024, into the `frontier_parent` packet.
4. Starting atlas or transfer compute before the novelty gate risks sinking effort into an Exoo-memorizing failure catalog that collapses under `anti_exoo_holdout`.
5. Starting filter use before witness-survival and ablation checks risks unsound pruning that kills known `42`- and `43`-vertex witnesses.
6. Starting any heavier compute before the missing corpus/enumerator/verifier/checker tooling exists produces artifacts that cannot rise above `intermediate evidence` or `residue_only`.
7. Starting benchmarking before the `shared comparison object` column is fixed allows proxy or apples-to-oranges wins to masquerade as progress.

## Current Rehearsal Verdict

- `No-go` on any bound-improvement claim.
- `Go` only for `H1` `Rung 0` and the bounded Phase 4 ladder as intermediate structural work.
