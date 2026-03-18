# Verification Summary

## Decision

Recommended status: `REVISE`

The current pack can support one narrow contribution: a seeded CA falsification attempt on the published `64`-modular order-`668` frontier seed, under matched same-representation controls, with no exact hit and no improvement over the seed objective `13/2880/512`. It should not be accepted in its current framing as a new CA repair method, an order-`668` frontier advance, or a literature-level benchmark.

Do not choose `DEEPEN` by default. Additional experiments matter only if the team wants to preserve broader mechanism, novelty, or competitiveness claims after the revisions below.

## Must-Fix Issues

- Rewrite `H1` as a negative-result / falsification scaffold. Remove or narrow language claiming material CA-method novelty, frontier advance, or broad competitiveness.
- Keep exactness statements explicitly negative: no exact witness, no proof artifact, and no improvement over the published seed objective.
- Replace derivative and circular evidence chains. Stop using `results/verification/citation_audit.md`, `results/verification/benchmark_report.md`, and `results/verification/novelty_report.md` as primary support where direct artifacts exist.
- Promote direct artifacts to first-line evidence: `results/frontier/order_668_64m/seed_manifest.json`, `results/frontier/order_668_64m/source_excerpt.txt`, `results/experiments/order_668_64m/summary.json`, `results/experiments/controls/summary.json`, `results/experiments/order_668_64m/configs/*.json`, and `hadamard_ca/harness.py`.
- Mark the following as interpretation unless new evidence is added: the narrow novelty framing beyond the negative result, any literature-competitiveness claim, the `pivot to H2` mechanism story, and the causal explanation for H1 runtime cost.
- Keep `H2` blocked until a family-leakage audit artifact exists. If it collapses into Goethals-Seidel / Williamson / Turyn / cocyclic / block-circulant style search, relabel it as optimizer-over-known-family or reject it.
- Keep `H3` reserve-only until CA/design overlap sources are added to the bibliography/watchlist and explicitly cleared.
- Limit benchmark language to what the saved pack actually shows: internal branch elimination on one canonical seed, one RNG seed, one budget, and a narrow same-representation roster. Remove wording that implies restart robustness, seed robustness, mechanism diagnosis, full auditability, or publication-grade comparison.

## Optional Improvements

- Run matched CA-mechanism ablations on the same controls and frontier seed: full H1 vs zero-coupling, zero-refractory, scorer-only, and fallback-disabled variants.
- Build a harder control ladder with multi-flip and frontier-style synthetic controls closer to `seed_length = 167` and higher initial support; add random-walk and oracle anchors on the tiny solved controls.
- Replicate the frontier batch across multiple RNG seeds, q-flip and s-flip perturbation seeds, and equalized restart coverage or fixed per-restart budgets.
- Add per-restart terminal summaries, explicit `output_semantics`, defect-location summaries, and code/config/seed digests strong enough for a third party to reproduce all saved experiments.
- Add profiling if the writeup wants a causal runtime story; otherwise keep only the measured runtime numbers.
- Fix risky bibliography metadata (`tsompanas2017`, `suksmono2024`) and keep `ghaleb2019`, `ghaemi2022`, and `leeuwen2000` as watchlist-only.
- If broader background or comparison language remains, strengthen it with direct Hadamard and modular-Hadamard anchors such as `eliahou2005`, `eliahou2001`, `bright2018`, `suksmono2022` or corrected `suksmono2024`, and `cati2024`.

## Next Action

Revise the writeup and verification framing now. After that, either:

- stop with a narrow negative-result package
- deepen only the specific claim tracks that still matter, starting with `H2` family-leakage clearance and H1 CA-off ablations
