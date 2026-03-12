# Final Claim Memo

## Locked setting

- Domain: `r > 0`.
- Subsequence meaning: ordered values `b_k = floor(n_k r)` with `n_0 < n_1 < ...` from the frozen selector families.
- Recurrence meaning: homogeneous constant-coefficient recurrence over `Z`.

## Strongest theorem-backed claim

**Theorem-backed statement.**
For the selector classes whose gap sequence is eventually periodic - in particular, arithmetic progressions and finite unions of arithmetic progressions - the extracted value sequence `floor(n_k r)` satisfies a homogeneous constant-coefficient recurrence over `Z` if and only if `r` is rational.

- Rational baseline: if `r = p/q`, any arithmetic progression with step divisible by `q` yields an arithmetic value sequence, hence an order-2 recurrence.
- Irrational exclusion: the H1 memo shows that the corresponding difference sequences are bounded mechanical codings of irrational rotation, while bounded integer recurrences would force eventual periodicity.

Artifact support: `results/core/h1_modular_shadow_memo.md`, `results/definition_lock.md`, `results/experiments/full_panel_results.json`.
Sources: `bell2005`, `derksen2005`, `schaeffer2024`, `durand2000`.

## Strongest experiment-backed claim

**Experiment-backed statement.**
Within the frozen zero-density selector panel, the exact-certified irrational recurrence cases are the quadratic periodic-continued-fraction examples `phi - 1`, `phi`, `sqrt(2)`, and `1 + sqrt(2)` on the selector `quadratic_convergent_even`.

- `phi - 1` and `phi` support `x_k - 3 x_{k+1} + x_{k+2} = 0`.
- `sqrt(2)` and `1 + sqrt(2)` support `x_k - 6 x_{k+1} + x_{k+2} = 0`.
- Additional zero-density quadratic cases on `fib_indices` and `pell_indices` survive exact holdout through 160 samples in `results/experiments/claim_sensitive_ablation.json`, but they still lack structural certificates and therefore remain empirical only.
- No higher-degree Pisot, Salem, or transcendental slope survives the same order-`<=4` convergent construction or the concrete suffix-`10` beta-endpoint construction.

Artifact support: `results/concept_evolve/tree/005_convergent_hankel_detector/results.json`, `results/core/h2_pisot_backup.md`, `results/concept_evolve/tree/009_pisot_beta_endpoint_sampler/results.json`, `results/experiments/full_panel_results.json`, `results/experiments/claim_sensitive_ablation.json`.
Sources: `schaeffer2024`, `byszewski2023`, `allouche2018`, `maskov2006`.

## Conjectural refinement

The current evidence supports the conjecture that the sparse survivor mechanism is periodic-continued-fraction / quadratic rather than broadly Pisot. That conjecture is **not** claimed as a theorem here.

## Scope warning

No claim is made for arbitrary subsequences, for symbolic linear recurrence, or for unordered Beatty-set embeddings. Every positive statement above stays inside the locked arithmetic problem and the frozen selector families.
