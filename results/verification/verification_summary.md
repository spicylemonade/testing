# Verification Summary

Date: 2026-03-13
Owner role: `integrator`
Verification phase: `post_researcher`
Active hypothesis: `H1` = `Cross-family canonical obstruction atlas for failed 42 -> 43 extensions in R(5,5)`
Bound-moving threshold: independently verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof

## Reviewed Specialist Reports

- `results/verification/novelty_report.md`
- `results/verification/citation_audit.md`
- `results/verification/benchmark_report.md`

## Recommendation

Decision: `DEEPEN`

Rationale: the packet is acceptable only as a constrained no-go/planning memo. It is not acceptable as an achieved `H1` result, a bound-improvement claim, or a stronger `H2`/`H3` comparison memo because the benchmark layer is still empty and the core `H1` transfer evidence does not exist yet.

## Safe Current Scope

- `Go` only for a constrained memo stating that `H1` remains the only plausible novelty route, that no bound movement has been shown, and that the next step is evidence generation.
- `No-go` on any claim of an independently supported `44`-vertex witness, a machine-checkable `45`-vertex impossibility proof, an achieved `H1` structural intermediate result, an `H2` non-equivalence win, or an `H3` proof-transfer gain.

## Must-Fix Issues

- Materialize the missing `H1` evidence layer before making stronger claims: `results/h1/frontier_parents.jsonl`, `results/h1/extension_cases.jsonl`, `results/h1/failure_witnesses.jsonl`, `results/h1/obstruction_cores.jsonl`, `results/h1/transfer_records.jsonl`, `results/h1/atlas_summary.md`, and `results/h1/witness_safety_audit.md`.
- Add the gating validation tools and controls for `H1`: an orbit-distinct `42 -> 43` extension enumerator, an independent `44`-vertex witness verifier, `anti_exoo_holdout`, family-balance auditing across at least 3 non-isomorphic parent families, leave-one-parent-out evaluation, and zero known-witness deletions.
- Freeze and execute benchmark rows for every named comparator with a shared comparison object, artifact path, matched compute tuple, result type, and replay path. Do not allow partially populated benchmark rows.
- Reproduce at least one smaller solved certificate case with input hash, artifact hash, checker version, and pass/fail result before making any `H2`, `H3`, or `n=45` certificate-path claim.
- Run the required ablations and stress tests before treating any signal as real: per-filter `on/off`, canonicalized cores versus raw witness clustering, family/provenance diversification, `H2` and `H3` primitive `on/off`, `anti_exoo_holdout`, `witness_pressure`, and `rare_core_tail`.
- Emit run-level failure codes and summaries by family, rung, and ablation condition so the packet can distinguish `non_transfer`, `witness_killed`, `rare_core_tail`, `proof_bytes_regression`, and related failure modes from real progress.

## Optional Improvements

- Writer-side citation/context repairs were applied after the original audit: the `gauthier2025` row now points to the verified AITP strategy abstract, H3 comparison language now cites `narvez2024`, `heule2018schur`, and `li2025ramseycert`, and `results/research_context.md` no longer labels lexical false positives as closest prior art.
- Keep novelty language narrow: frame `H1` as a prospective transfer-safe obstruction atlas, not as one-vertex-extension relabeling, Exoo-line structural analysis, optimizer tuning, solver shopping, or proof-packaging infrastructure.
- Restrict novelty and comparison arguments to the curated Ramsey-specific corpus; do not let lexical watchlist or snapshot noise carry argumentative weight.
- Keep `aijaam2010` as overlap-only and enrich its metadata if retained. Keep `mckay1992` and `noga2022` background-only unless stronger anchors are found.
- After the blocking evidence exists, add stronger diagnostics: target `>= 2x` canonical core compression with unchanged witness coverage, explicit uncovered-tail analysis, and proof-bytes/checker-runtime regression tracking for `H2` and `H3`.

## Bottom Line

The current packet is useful as a disciplined stop signal: no bound improvement, no achieved `H1` result, and no publication-grade benchmark case have been demonstrated. The next action is to deepen the evidence packet, not to strengthen claims.
