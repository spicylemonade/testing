# Final Claim Memo

## Locked setting

- Domain: `r > 0`.
- Subsequence meaning: ordered values `b_k = floor(n_k r)` with `n_0 < n_1 < ...` from the frozen selector families.
- Recurrence meaning: homogeneous constant-coefficient recurrence over `Z`.

## Strongest theorem-backed claim

**Theorem-backed statement.**
For the frozen selectors whose gap sequence is eventually periodic - in particular, arithmetic progressions and finite unions of arithmetic progressions - the extracted value sequence `floor(n_k r)` satisfies a homogeneous constant-coefficient recurrence over `Z` if and only if `r` is rational.

- Rational baseline: if `r = p/q`, any arithmetic progression with step divisible by `q` yields an arithmetic value sequence, hence an order-2 recurrence.
- Irrational exclusion: the H1 memo shows that the corresponding difference sequences are bounded mechanical codings of irrational rotation, while bounded integer recurrences would force eventual periodicity.

Artifact support: `results/core/h1_modular_shadow_memo.md`, `results/definition_lock.md`, `results/experiments/full_panel_results.json`.
Sources: `bell2005`, `derksen2005`, `schaeffer2024`, `durand2000`.

## Strongest experiment-backed claim

**Experiment-backed statement.**
Within the frozen sparse-selector panel, the only exact-certified irrational recurrence cases are the four isolated `quadratic_convergent_even` identities for `phi - 1`, `phi`, `sqrt(2)`, and `1 + sqrt(2)`.

- `phi - 1` and `phi` support `x_k - 3 x_{k+1} + x_{k+2} = 0`.
- `sqrt(2)` and `1 + sqrt(2)` support `x_k - 6 x_{k+1} + x_{k+2} = 0`.
- The revision follow-up now pushes all 15 `uncertified_exact_holdout` rows to holdout length `320`: the strongest nonquadratic anomaly `salem_quartic / ost_suffix_001` fails by `80`, while the remaining long exact leaks are confined to rational-trivial sparse selectors and the Fibonacci/Pell/Ostrowski selectors on the same four quadratic slopes.
- No family-level statement is made about quadratics, periodic continued fractions, or zero intercept.

Artifact support: `results/concept_evolve/tree/005_convergent_hankel_detector/results.json`, `results/core/h2_pisot_backup.md`, `results/concept_evolve/tree/009_pisot_beta_endpoint_sampler/results.json`, `results/experiments/full_panel_results.json`, `results/experiments/claim_sensitive_ablation.json`.
Sources: `schaeffer2024`, `byszewski2023`, `allouche2018`, `maskov2006`.

## Open empirical lane

The surviving sparse leaks on `phi`, `phi - 1`, `sqrt(2)`, and `1 + sqrt(2)` remain empirical only. They have long exact holdouts but no infinite certificate in the current package.

- Missing controls before any sharper boundary claim: intercept baselines `floor(n r + beta)`, continued-fraction-prefix-matched nonquadratic controls, and structural certificates for the surviving leaks.
- The failed higher-degree Pisot lane is kept only as a falsifier outcome, not as evidence for a quadratic-only or periodic-CF-only theorem.

## Scope warning

No claim is made for arbitrary subsequences, for sparse selectors in general, for symbolic linear recurrence, or for unordered Beatty-set embeddings. Every positive statement above stays inside the locked arithmetic problem and the frozen selector families.
