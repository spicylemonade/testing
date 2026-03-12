# Full Panel Memo

## Scope

`results/experiments/full_panel_results.json` executes the frozen phase-4 panel with:
- the primary slopes from `results/baseline/panel_spec.json`,
- the low-slope controls `1/2` and `phi - 1`,
- the H2 follow-up slope `1 + sqrt(2)` required to complete the three-Pisot backup lane,
- all approved selector families,
- exact recurrence search limited to `d <= 4`,
- modular shadows on `2,3,5,7,11,25`.

## Aggregate counts

- Executed cases: 145
- Waived cases: 20
- Exact recurrence cases: 32 after the writer-stage certificate refresh in `results/experiments/metrics_full_panel.json`

## Main observations

1. Eventually-periodic-gap theorem lane behaves as expected.
   - Rational slopes now carry exact certificates across the full AP/FUAP lane, not only on denominator-compatible arithmetic progressions.
   - Irrational slopes in those same AP/FUAP rows collapse to `no_candidate`, `prefix_fit`, or `selector_shadow_failure`.

2. Sparse exact certificates stay narrow.
   - `phi - 1`, `phi`, `sqrt(2)`, and `1 + sqrt(2)` have exact certificates on `quadratic_convergent_even`.
   - `results/experiments/claim_sensitive_ablation.json` shows that these order-2 recurrences persist through holdout lengths `40`, `80`, `160`, and `320`.
   - No broader family statement is made from those four examples alone.

3. Higher-degree and control lanes stay negative at certificate level.
   - `plastic` has no order-`<=4` recurrence on `quadratic_convergent_even` and no exact survivor on `beta_endpoint_suffix_10`.
   - Salem and transcendental controls also fail at the certificate level; the revision follow-up further shows that `salem_quartic / ost_suffix_001` breaks by holdout length `80`.

4. Waivers are definition-driven, not convenience-driven.
   - Rational slopes waive Ostrowski and convergent-even selectors because those constructions require irrational continued-fraction structure.
   - Rational slopes waive `beta_endpoint_suffix_10` because that construction is only meaningful for irrational numeration bases.

5. The revision follow-up closes the stale-summary gap.
   - `results/experiments/claim_sensitive_ablation.json` now extends all 15 `uncertified_exact_holdout` rows to `320` and adds a fit-length ablation over `8/12/16/24`.
   - `results/experiments/falsifier_controls.md` and `results/experiments/evaluation_memo.md` are synchronized to the refreshed 28 rational exact cases, 4 irrational exact certificates, 12 sparse leaks at the 20-term screen, and the strengthened long-holdout results.

## Writer-stage follow-up

- `results/experiments/metrics_full_panel.json` publishes per-case `holdout_exact_20`, `exact_certificate_present`, `risk_tags`, and the nondegenerate exact-hit split.
- `results/experiments/claim_sensitive_ablation.md` records the order-cap, fit-length, holdout-length, and selector-variant ablations requested by verification.
