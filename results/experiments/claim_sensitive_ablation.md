# Claim-Sensitive Ablation Memo

## Order-cap ablation
- Raising the search ceiling from `d <= 4` to `d <= 6` or `d <= 8` on the same 20-value panel does **not** create any new exact-certified case.
- `d <= 6` flips 84 classifications relative to `d <= 4`, almost entirely by converting `no_candidate` rows into `prefix_fit`, `sparse_subsequence_leak`, or `selector_shadow_failure` under higher-order overfitting.
- `d <= 8` flips 89 classifications relative to `d <= 4` with the same pattern, so higher order alone is not evidence of new exact structure.

## Holdout-length ablation
- The four certified quadratic-convergent cases (`phi`, `phi-1`, `sqrt(2)`, `1+sqrt(2)`) retain the same order-2 recurrence through lengths `40`, `80`, and `160`.
- The unresolved quadratic `fib_indices` and `pell_indices` cases also keep their 20-sample exact holdout recurrences through length `160`, which strengthens them empirically but does not upgrade them to theorem status.
- All three plastic positive-density prefix fits fail by length `40`, confirming that the earlier 20-sample positives were finite-window mirages.

## Selector-template variants around `quadratic_convergent_even`
- Nearby quadratic templates (`odd`, `even_shift1`, `every_third`) still show long exact holdouts for the four quadratic slopes, but they remain uncertified and therefore stay in the sparse empirical lane.
- Matched nonquadratic controls (`plastic`, `e`) stay in `selector_shadow_failure` across the baseline 20-sample variant panel.

## Takeaway
- The ablations narrow the safe story: exact theorem language belongs to the periodic-gap rational lane and the four certified quadratic-convergent identities; higher-order search on short windows mostly manufactures additional false positives rather than new exact cases.
