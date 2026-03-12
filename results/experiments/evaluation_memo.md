# Evaluation Memo

## Theorem-backed conclusions

- For arithmetic progressions and finite unions of arithmetic progressions, the H1 memo supplies the proof-backed claim that irrational slopes are excluded while rationals survive.
- This theorem-backed lane covers all primary rational slopes and all irrational positive-density controls in the frozen panel.

## Empirical observations

- The full panel in `results/experiments/full_panel_results.json` executes 145 cases with 20 justified waivers and finds 10 exact recurrence cases.
- All irrational exact cases come from the single zero-density construction `quadratic_convergent_even`, and they occur only for `phi`, `sqrt(2)`, and `1 + sqrt(2)`.
- The beta-endpoint suffix-`10` construction is negative on every executed irrational slope in the current concrete implementation.

## Conjectural inferences

- The clean survivor mechanism looks periodic-continued-fraction / quadratic rather than broadly Pisot.
- A stronger irrational classification would need structural certificates for the quadratic survivors or a new higher-degree endpoint mechanism; the current evidence does not justify either as theorem language.

## Failure-case studies

### 1. Plastic constant on `ap_2_0`
- Artifact: `results/experiments/full_panel_summary.csv`
- Outcome: `selector_shadow_failure`
- Reading: the first training window admits a low-order recurrence candidate, but exact holdout and modular replay reject it.

### 2. Plastic constant on `union_mod3_01`
- Artifact: `results/experiments/full_panel_summary.csv`
- Outcome: `prefix_fit`
- Reading: a positive-density selector can still generate a long exact-looking fit, but without a structural certificate it stays downgraded.

### 3. Beta-endpoint suffix `10` on higher-degree and control slopes
- Artifact: `results/concept_evolve/tree/009_pisot_beta_endpoint_sampler/results.json`
- Outcome: `no_candidate` for `plastic`, `sqrt(2)`, the Salem quartic root, and `e`
- Reading: the most obvious executable endpoint-cylinder mechanism does not explain the higher-degree lane.

## Ablations

### Selector-family restriction
- Artifact: `results/experiments/ablation_summary.json`
- Result: with all families enabled there are 10 exact recurrence cases; restricting to positive-density families leaves 7 exact cases, all rational; restricting to zero-density families leaves 3 exact cases, all quadratic-convergent.
- Interpretation: the irrational story is entirely carried by the sparse selector lane.

### Modulus-panel restriction
- Artifact: `results/experiments/ablation_summary.json`
- Result: reducing the modular panel from `{2,3,5,7,11,25}` to `{2,3,5}` changes 0 of 49 candidate-case classifications.
- Interpretation: the larger modulus panel is currently a robustness layer rather than a verdict-changing ingredient, which is itself a useful stability result.
