# Evaluation Memo

## Theorem-backed conclusions

- For selectors with eventually periodic gaps - concretely, the arithmetic-progression and finite-union rows frozen in the panel - the H1 memo supplies the proof-backed claim that irrational slopes are excluded while rationals survive.
- This theorem-backed lane covers the AP/FUAP portion of the full panel and its matched irrational controls without invoking any sparse-selector evidence.

## Empirical observations

- The refreshed full panel in `results/experiments/full_panel_results.json` executes 145 cases with 20 justified waivers and records 32 exact-certified cases.
- 28 of those exact-certified cases are rational AP/FUAP baselines; the remaining 4 are the isolated `quadratic_convergent_even` identities for `phi - 1`, `phi`, `sqrt(2)`, and `1 + sqrt(2)`.
- The revision ablation in `results/experiments/claim_sensitive_ablation.json` now extends all 15 `uncertified_exact_holdout` rows to holdout length `320` and adds a fit-length ablation over `8/12/16/24`.
- All 4 certified quadratic identities remain stable through `320`; the strongest nonquadratic anomaly, `salem_quartic / ost_suffix_001`, breaks by `80`, and all 3 plastic prefix fits break by `40`.
- The remaining long-holdout leaks are confined to rational-trivial sparse selectors and the Fibonacci/Pell/Ostrowski selectors on `phi`, `phi - 1`, `sqrt(2)`, and `1 + sqrt(2)`.
- The beta-endpoint suffix-`10` construction stays negative on every executed irrational slope in the current implementation.

## Empirical-only boundary

- No family-level claim is made about quadratics, periodic continued fractions, or zero intercept.
- Any sharper sparse-lane statement would still need intercept controls, continued-fraction-prefix-matched nonquadratic controls, and infinite certificates for the surviving leaks.

## Failure-case studies

### 1. Plastic constant on `ap_2_0`
- Artifact: `results/experiments/full_panel_summary.csv`
- Outcome: `selector_shadow_failure`
- Reading: the first training window admits a low-order candidate, but exact holdout and modular replay reject it immediately.

### 2. Plastic constant on `union_mod3_01`
- Artifact: `results/experiments/claim_sensitive_ablation.json`
- Outcome: `prefix_fit` at length `20`, `selector_shadow_failure` by length `40`
- Reading: a positive-density selector can still create a convincing short-window mirage, but the longer follow-up destroys it.

### 3. Salem quartic root on `ost_suffix_001`
- Artifact: `results/experiments/claim_sensitive_ablation.json`
- Outcome: `sparse_subsequence_leak` through `40`, `selector_shadow_failure` by `80`
- Reading: the strongest nonquadratic sparse anomaly is a finite-window survivor rather than a durable counterexample.

## Ablations

### Selector-family restriction
- Artifact: `results/experiments/ablation_summary.json`
- Result: with all families enabled there are 32 exact recurrence cases; restricting to AP/FUAP leaves 28 exact cases, all rational; restricting to the sparse families leaves 4 exact cases, all `quadratic_convergent_even`.
- Interpretation: the theorem-backed lane is entirely rational, and the irrational story is confined to isolated sparse constructions.

### Modulus-panel restriction
- Artifact: `results/experiments/ablation_summary.json`
- Result: reducing the modular panel from `{2,3,5,7,11,25}` to `{2,3,5}` changes 0 of 49 candidate-case classifications.
- Interpretation: the larger modulus panel is currently a robustness layer rather than a verdict-changing ingredient.

### Order-cap and fit-length restriction
- Artifact: `results/experiments/claim_sensitive_ablation.json`
- Result: increasing the search ceiling from `d <= 4` to `d <= 6` and `d <= 8` adds no new exact-certified case but creates many extra short-window fits; shrinking `fit_length` from `12` to `8` creates 87 extra false candidates, while expanding it to `16` or `24` only removes weak shadow failures.
- Interpretation: exact certificates and explicit holdouts are more informative than aggressive fitting on short prefixes.

### Exhaustive long-holdout follow-up
- Artifact: `results/experiments/claim_sensitive_ablation.json`
- Result: all 15 `uncertified_exact_holdout` rows now run through `320`; 11 remain as long exact leaks, 3 plastic mirages fail by `40`, and `salem_quartic / ost_suffix_001` fails by `80`.
- Interpretation: the revision removes the strongest nonquadratic anomaly but still leaves a genuinely empirical sparse lane on the four quadratic slopes.
