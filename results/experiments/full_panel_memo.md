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

1. Positive-density theorem lane behaves as expected.
   - Rational slopes now carry exact certificates across the full AP/FUAP lane, not only on denominator-compatible arithmetic progressions.
   - Irrational slopes in the positive-density families collapse to `no_candidate`, `prefix_fit`, or `selector_shadow_failure`.

2. Quadratic survivor lane is real.
   - `phi - 1`, `phi`, `sqrt(2)`, and `1 + sqrt(2)` now have exact certificates on `quadratic_convergent_even`.
   - `results/experiments/claim_sensitive_ablation.json` shows that these order-2 recurrences persist through holdout lengths `40`, `80`, and `160`.
   - This is the evidence base behind the H2 memo's conclusion that the surviving mechanism is quadratic/periodic-CF rather than broadly Pisot.

3. Higher-degree backup lane stays negative in the frozen constructions.
   - `plastic` has no order-`<=4` recurrence on `quadratic_convergent_even` and no exact survivor on `beta_endpoint_suffix_10`.
   - Salem and transcendental controls also fail.

4. Waivers are definition-driven, not convenience-driven.
   - Rational slopes waive Ostrowski and convergent-even selectors because those constructions require irrational continued-fraction structure.
   - Rational slopes waive `beta_endpoint_suffix_10` because that construction is only meaningful for irrational numeration bases.

5. The beta-endpoint fairness repair stays negative.
   - After extending `beta_endpoint_suffix_10` to the matched irrational controls, every executed endpoint case remains `no_candidate`, including `phi`, `1 + sqrt(2)`, `plastic`, `sqrt(2)`, the Salem quartic root, `e`, and `phi - 1`.

## Writer-stage follow-up

- `results/experiments/metrics_full_panel.json` now publishes per-case `holdout_exact_20`, `exact_certificate_present`, `risk_tags`, and the nondegenerate exact-hit split.
- `results/experiments/claim_sensitive_ablation.md` records the order-cap, holdout-length, and selector-variant ablations requested by verification.
