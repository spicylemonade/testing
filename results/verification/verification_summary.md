# Verification Summary

Date: 2026-03-13
Owner role: `integrator`
Verification phase: `review_round_1`
Active hypothesis: `H1` = `Cross-family canonical obstruction atlas for failed 42 -> 43 extensions in R(5,5)`
Bound-moving threshold: independently verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof

## Reviewed Specialist Reports

- `results/verification/novelty_report.md`
- `results/verification/citation_audit.md`
- `results/verification/benchmark_report.md`

## Recommendation

Decision: `DEEPEN`

Rationale:

- Citation issues are targeted and repairable, but the novelty and benchmark reviews both conclude that the packet still lacks the executed `H1` evidence needed for any stronger scientific claim.
- The current work is safe only as an `infrastructure-only` plus `negative result` / route-specification memo. It is not ready to claim a new bound, an achieved `H1` structural result, an `H2` non-equivalence win, or an `H3` proof-transfer gain.
- `REVISE` would understate the gap, because the main blockers are missing artifacts, controls, ablations, and replayable benchmark evidence rather than wording alone.

## Safe Current Scope

- Accept only the narrow claim that `H1` remains the only plausible live route, while no bound movement or executed structural intermediate result has been demonstrated.
- Keep all present claims framed as governance, route selection, and no-go evidence.
- Do not attach novelty credit beyond that scope until the required `H1` artifact and benchmark packet exists.

## Must-Fix Issues

### Evidence and novelty gates

- Materialize the missing `results/h1/` packet: `frontier_parents.jsonl`, `extension_cases.jsonl`, `failure_witnesses.jsonl`, `obstruction_cores.jsonl`, `transfer_records.jsonl`, `atlas_summary.md`, and `witness_safety_audit.md`.
- Build the missing execution infrastructure: an orbit-distinct `42 -> 43` extension enumerator, an independent `44`-vertex witness verifier, and a replayable `45`-vertex certificate-checking path.
- Demonstrate all four `H1` distinctness tests together before upgrading the manuscript: recurrence across at least 3 non-isomorphic parent families, substantial leave-one-parent-out transfer including the decisive `anti_exoo_holdout`, zero known-witness deletions, and at least one core family reused identically for lower-bound pruning and an upper-bound lemma candidate.
- Keep all bound-moving novelty language blocked unless there is an independently verified `44`-vertex witness or a machine-checkable `45`-vertex impossibility proof.

### Benchmark execution and controls

- Freeze a versioned benchmark manifest with mandatory columns for comparator, shared comparison object, artifact path, matched-compute tuple, result class, and replay path. Reject incomplete rows.
- Execute at least one reproduced lower-bound baseline and one smaller solved upper-bound certificate case under that manifest before making empirical comparison claims.
- Run the Phase 4 ladder in order: `Rung 0`; `Rung 1` with `rare_core_tail`; `Rung 2` with `anti_exoo_holdout`; `Rung 3` with per-filter ablations.
- Add the missing ablations and stress tests: raw-witness versus canonical-core, filter `off` versus `on`, provenance/family diversification, `witness_pressure`, and any reopened `H2`/`H3` primitive toggles under otherwise identical conditions.
- Require run-level failure codes and summaries by family, rung, and ablation condition so the packet can distinguish transfer failure, witness kills, tail behavior, and proof-path regressions from real progress.

### Citation and traceability repairs

- Fix the broken `gauthier2025` bibliography URL and keep that source explicitly limited to overlap / strategy support.
- Repair the stale exact-measurement row `Known papers tracked = 106` and reconcile corpus counts with one auditable source of truth.
- Add consistent current-frontier support where the prose makes present-tense status claims, especially by citing `radziszowski2024ds1` with its DOI and exact revision/date.
- Narrow or properly source the broad comparison paragraph that currently leans too heavily on `aijaam2010`.
- Replace weak source metadata that is still being relied on directly, especially the `narvez2024` Semantic Scholar mirror.

## Optional Improvements

- Strengthen bibliography metadata for `exoo1989`, `mckay1992`, and `angeltveit2018`, and add a stable release or commit anchor for `lehavirepo`.
- Clean residual false-positive prior-art rows from context files so later synthesis steps do not reintroduce traceability noise.
- If `H2` or `H3` is reopened later, claim novelty only if the primitive itself changes the proof object and wins under matched conditions.
- Track stronger post-blocker diagnostics once execution exists, including `>= 2x` canonical-core compression with unchanged witness coverage, uncovered-tail summaries, and proof-bytes / checker-runtime regressions.
- Avoid novelty inflation from OVE relabeling, Exoo-line digestion, solver shopping, governance-theorem language, or proof-packaging alone.

## Bottom Line

The current packet should not be accepted as a stronger Ramsey contribution. It should be deepened: first by repairing the targeted citation-traceability issues, and more importantly by producing the missing `H1` corpus, controls, ablations, replay artifacts, and benchmark rows that would make the novelty claim real rather than prospective.
