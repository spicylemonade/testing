# Steering Notes

## Direction 1 - Convergent Hankel witnesses, then exact rejection or promotion
- Concept card to implement: `convergent_hankel_detector`.
- Exact implementation hook: compute convergent blocks, build exact Hankel matrices, run Prony or matrix-pencil reconstruction, and symbolically validate any annihilating polynomial on longer blocks.
- Bridge chains to turn into experiments:
  - `convergent_hankel_detector -> annihilating_filter_quantization -> rigidity_time_selector -> rauzy_window_recurrence_lift`
  - `pisot_beta_endpoint_sampler -> convergent_hankel_detector -> ostrowski_synchronized_subsequence_search`
- Rubric items informed: `item_006`, `item_007`, `item_008`, `item_011`, `item_016`, `item_020`.

## Direction 2 - Pisot endpoint stress test beyond the quadratic lane
- Concept card to implement: `pisot_beta_endpoint_sampler`.
- Exact implementation hook: generate `G_n`, compute greedy beta expansions for named Pisot units, enumerate endpoint-constrained indices, and test the sampled Beatty values with exact Hankel and companion-matrix checks.
- Bridge chains to turn into experiments:
  - `substitution_return_word_compiler -> ostrowski_synchronized_subsequence_search -> rauzy_window_recurrence_lift -> pisot_beta_endpoint_sampler`
  - `pisot_beta_endpoint_sampler -> convergent_hankel_detector -> ostrowski_synchronized_subsequence_search`
- Rubric items informed: `item_006`, `item_012`, `item_013`, `item_016`, `item_020`.

## Direction 3 - Modular-shadow obstruction pipeline for generic survivors
- Concept card to implement: `skolem_automatic_intersection_filter`.
- Exact implementation hook: start from fixed LRS families, derive modular and p-adic necessary conditions on Beatty membership, and discard candidate selectors whose admissible sets collapse under progression-shadow checks.
- Bridge chains to turn into experiments:
  - `skolem_automatic_intersection_filter -> beatty_model_complete_obstruction -> generalized_polynomial_intersection_obstruction`
  - `ostrowski_synchronized_subsequence_search -> presburger_recurrence_oracle -> beatty_model_complete_obstruction -> generalized_polynomial_intersection_obstruction`
- Rubric items informed: `item_008`, `item_011`, `item_014`, `item_015`, `item_018`, `item_019`.

## Immediate commitment
- Mandatory exact card implementations for novelty evidence: `convergent_hankel_detector` and `pisot_beta_endpoint_sampler`.
- Supporting bridge experiment emphasis: use the low-rank detector as the front-end and the modular-shadow filter as the back-end so that prefix mirages are promoted or killed by cross-modulus evidence rather than by finite-prefix intuition.
