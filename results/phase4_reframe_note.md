# Phase 4 Reframe Note

This note records how `results/concept_evolve/reframings.json` is being used in the experiment phase.

## Immediate Keepers

- `zero_forcing_certificate_screen`
  - reason: it matches the monotone exact elimination structure most closely and helps interpret why a corridor candidate stalls.
- `structural_observability_screen`
  - reason: it gives a clean graph-pattern sanity check before blaming arithmetic labels for every failure.
- `matroid_circuit_elimination`
  - reason: it is a useful lens for understanding short versus long elimination chains once exact candidates appear.

## Deferred

- `index_coding_entropy_bounds`
- `expander_tanner_forcing`
- `toric_elimination_certificate`
- `electrical_flow_witness`
- `petri_net_invariant_filter`

These may help explain or generalize a later frontier, but they are too indirect for the current exact certificate search loop.

## Experiment Consequence

- The active H1 rows remain exact corridor searches with the corrected rational-span verifier.
- Reframe output is being used as a screening and interpretation guide, not as permission to widen the search family or claim a new mathematical formulation.
