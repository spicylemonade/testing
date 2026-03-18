# Verification Summary

Review phase: `review_round_1`

## Decision

Current work should: `REVISE`

The surviving contribution is narrow but real: a seeded falsification attempt on the published `64`-modular order-`668` frontier seed, under matched same-representation controls, with no `exact_hit` and no improvement over the seed objective `13/2880/512`.

The current package should not be accepted in its present framing as a new CA repair method, an order-`668` frontier advance, or a publication-grade benchmark. Choose `DEEPEN` only if the team wants to preserve stronger mechanism, robustness, or competitiveness claims after the rewrite below.

## Must-Fix Issues

- Reframe `H1` as a negative-result / falsification scaffold. Remove or narrow claims of material CA-method novelty, frontier advance, or broad competitiveness.
- Keep exactness statements explicitly negative: no exact witness, no proof artifact, and no improvement over the published seed objective `13/2880/512`.
- Repair the literature-positioning section at `research_paper.tex:115-127`. Add clause-level citations or label the comparison language as author synthesis instead of direct source support.
- Rewrite or re-cite interpretation-heavy passages at `research_paper.tex:123`, `research_paper.tex:624`, `research_paper.tex:650-655`, `research_paper.tex:686-698`, and `research_paper.tex:702`. The current wording overstates support for novelty narrowing, runtime causality, structural diagnosis, representation advice, and AI-pipeline generalization.
- Replace derivative and circular evidence chains. Use direct artifacts as first-line support instead of the verification memos wherever possible.
- Promote direct artifacts near every load-bearing quantitative claim: `results/frontier/order_668_64m/seed_manifest.json`, `results/frontier/order_668_64m/source_excerpt.txt`, `results/experiments/order_668_64m/summary.json`, `results/experiments/controls/summary.json`, `results/analysis/frontier_locality_scan.json`, `results/branches/H1_frontier_sensitivity_probe.json`, `results/verification/benchmark_gate.md`, `hadamard_ca/harness.py`, and `hadamard_ca/h1_ca.py`.
- Correct cited bibliography metadata before final assembly. At minimum fix `tsompanas2017`, `mariot2019_mols`, and `artacho2013`, and keep unvalidated watchlist entries out of the manuscript.
- Limit benchmark language to what the saved pack actually proves: one canonical seed, one RNG seed, `evaluation_budget = 80`, requested `restart_count = 3` with unequal executed restart coverage, and a narrow same-representation roster. Do not claim restart robustness, seed robustness, mechanism diagnosis, full auditability, or literature-level competitiveness.
- Keep `H2` blocked until a family-leakage audit artifact exists. If it collapses into Goethals-Seidel / Williamson / Turyn / cocyclic / block-circulant search, relabel it as optimizer-over-known-family or reject it.
- Keep `H3` reserve-only until direct CA-design overlap has been explicitly cleared in the literature framing.

## Optional Improvements

- Run matched CA-mechanism ablations on the same controls and frontier seed: full H1 vs zero-coupling, zero-refractory, scorer-only, and fallback-disabled variants.
- Add a harder control ladder with multi-flip, higher-support, and longer-length q/s controls closer to the frontier defect geometry; add random-walk and recoverability/oracle anchors on the tiny solved controls.
- Replicate the frontier batch across multiple RNG seeds, equal executed restart coverage or fixed per-restart budgets, budget sweeps, restart-perturbation sweeps, and nearby q/s perturbations of the canonical seed.
- Add actuator-basis and multi-packet activation ablations before claiming locality failure or representation-level failure.
- Repair artifact auditability with per-restart terminal summaries, explicit `output_semantics`, stronger trace semantics, and code/config/seed digests sufficient for third-party reconstruction.
- Add profiling and failure-clustering analysis only if the paper needs a causal runtime or mechanism story; otherwise keep those points labeled as interpretation.

## Recommended Next Step

Revise the manuscript and verification framing now.

If the goal is a narrow negative-result package, stop after the rewrite.

If the goal is to preserve broader method or benchmark claims, deepen only the specific missing evidence tracks above, starting with `H1` CA-off ablations, restart-robust replication, and `H2` family-leakage clearance.
