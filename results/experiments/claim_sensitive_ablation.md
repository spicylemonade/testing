# Claim-Sensitive Ablation Memo

## Order-cap ablation
- Raising the search ceiling from `d <= 4` to `d <= 6` or `d <= 8` on the same 20-value panel does **not** create any new exact-certified case.
- `d <= 6` flips 84 classifications relative to `d <= 4`, almost entirely by converting `no_candidate` rows into `prefix_fit`, `sparse_subsequence_leak`, or `selector_shadow_failure` under higher-order overfitting.
- `d <= 8` flips 89 classifications relative to `d <= 4` with the same pattern, so higher order alone is not evidence of new exact structure.

## Fit-length ablation
- The baseline `fit_length = 12` reproduces the published `32 exact / 12 sparse leaks / 3 prefix fits / 7 shadow failures / 91 no-candidate` split.
- Shrinking the fit window to `8` keeps the exact-hit and sparse-leak counts unchanged but creates 87 extra false candidates, almost all ending as `selector_shadow_failure` rather than exact recurrences.
- Enlarging the fit window to `16` or `24` adds no new exact cases and instead removes 2 and 7 weak shadow-failure candidates by collapsing them back to `no_candidate`.

## Holdout-length ablation
- All 4 certified quadratic-convergent cases retain the same order-2 recurrence through holdout length `320`.
- Exhaustive follow-up on all 15 `uncertified_exact_holdout` rows leaves 11 still holding through `320`; these survivors are either rational-trivial sparse selectors or the Fibonacci/Pell/Ostrowski leaks on `phi`, `phi-1`, `sqrt(2)`, and `1+sqrt(2)`, so they remain empirical only.
- The strongest nonquadratic anomaly `salem_quartic / ost_suffix_001` keeps the same order-4 fit through `40` terms but fails at holdout length `80`, so it no longer survives the strengthened follow-up.
- All three plastic positive-density prefix fits fail by length `40`, leaving no nonquadratic irrational long-holdout survivor outside the 6 quadratic sparse leaks.

## Selector-template variants around `quadratic_convergent_even`
- Nearby quadratic templates (`odd`, `even_shift1`, `every_third`) still show long exact holdouts for the four quadratic slopes, but they remain uncertified and therefore stay in the sparse empirical lane.
- Matched nonquadratic controls (`plastic`, `e`) stay in `selector_shadow_failure` across the baseline 20-sample variant panel.

## Takeaway
- The revision ablations narrow the safe story further: exact theorem language belongs to the periodic-gap rational lane, while the four certified quadratic-convergent identities remain isolated exact examples and every broader sparse claim stays empirical.
