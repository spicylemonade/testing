# Concept Delta

## Promoted bridges
- `005_convergent_hankel_detector -> 004_skolem_automatic_intersection_filter`
  - Reason: the exact low-rank front-end now produces clean survivor/failure certificates that can be fed into the modular-shadow rejection layer.
- `009_pisot_beta_endpoint_sampler -> 005_convergent_hankel_detector`
  - Reason: the H2 backup now needs the convergent/Hankel machinery as its exact screening front-end.
- `004_skolem_automatic_intersection_filter -> 010_beatty_model_complete_obstruction`
  - Reason: the champion obstruction story now flows from modular shadows into definability scarcity.

## Retired bridges
- `001_ostrowski_synchronized_subsequence_search`
  - Retirement reason: too close to the quadratic-Ostrowski decidability lane for a first theorem claim.
- `002_presburger_recurrence_oracle`
  - Retirement reason: useful infrastructure, but too derivative as a theorem direction before the arithmetic survivor set is stabilized.
- `006_annihilating_filter_quantization`, `007_substitution_return_word_compiler`, `011_rigidity_time_selector`
  - Retirement reason: high novelty potential, but lower signal-to-time ratio than the H1/H2 path under the locked budget.

## Implemented techniques so far

### 1. Convergent Hankel detector
1. CE suggestion: sample `floor(q_j r)` on convergents, recover exact annihilating polynomials from Hankel blocks, then validate them on holdout.
2. What was implemented: `results/concept_evolve/tree/005_convergent_hankel_detector/experiment.py` plus `special_numbers/recurrence.py` and `special_numbers/slopes.py`.
3. Result: `phi` and `1 + sqrt(2)` survive with exact order-2 recurrences; plastic, Salem, and `e` only generate finite-window low-rank mirages that fail on holdout.
4. Novel contribution: this turns convergent sampling into an exact survivor/falsifier front-end for Beatty subsequences rather than a heuristic signal-processing analogy.

### 2. Pisot beta endpoint sampler
1. CE suggestion: generate `G_n`, compute greedy beta expansions for small Pisot units, enumerate endpoint-constrained indices, and test the sampled Beatty values with exact Hankel and companion-matrix checks.
2. What was implemented: `results/concept_evolve/tree/009_pisot_beta_endpoint_sampler/experiment.py` together with `special_numbers/beta_numeration.py`.
3. Result: the concrete suffix-`10` endpoint proxy produced no exact low-order recurrence for `phi`, `1 + sqrt(2)`, `plastic`, or the matched controls `sqrt(2)`, Salem, and `e`.
4. Novel contribution: this negative result narrows the higher-degree exception search by ruling out the most obvious executable beta-endpoint cylinder before more elaborate Rauzy-face refinements are attempted.

## Next experiments
- Implement the exact beta-endpoint sampler for the plastic constant and matched controls.
- Convert the H1 modular-shadow layer into a concept-specific experiment for folder `004_skolem_automatic_intersection_filter`.
- Upgrade quadratic survivors from exact holdout success to full structural certificates tied to their periodic continued fractions.
