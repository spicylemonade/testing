# Concept Delta

## Suggestion

The strongest ConceptEvolve signals after the mandatory `evolve` and `probe` runs were:

- `coupled_peeling_with_exact_templates`
- `sat_plus_egraph_symbolic_backbone`
- `observer_guided_macrocell_search`

The common suggestion was to keep the search local and automaton-shaped, but force every local update to stay attached to exact witness legality rather than to free-form spatial dynamics.

## Implementation

The run incorporated those suggestions in the following concrete artifacts:

- `results/core/h1_design.md`
  - adopted the stage-indexed fiber layout and fixed exact decoder interface
  - enforced the no-repair rule so the decoder cannot hide search failures
- `results/swarm/phase_3_h1_review.md`
  - kept `H1` active only behind exact-verifier, label-shuffle, and out-of-distribution gates
- `results/concept_evolve/tree/phase_3_core/`
  - kept the direct proof-front branch active
  - held a factorized variant in reserve
  - killed neural-CA and modular-shadow branches that diluted exact witness semantics

## Result

- The ConceptEvolve output did not justify opening a neural-CA or modular curriculum lane.
- It did strengthen the case for a proof-carrying, stage-indexed CA whose state decodes directly to `(X,G,R,T)`.
- The verifier blocker still dominates execution risk, so the delta is architectural and falsification-oriented rather than experimental.

## Novelty Delta

- Before ConceptEvolve integration, the lane risked collapsing into generic CA search over a serialized witness.
- After integration, the active lane is narrower and more defensible:
  - direct product-grid witness representation
  - proof-carrying symbolic state
  - exact decoder contract
  - no-repair rejection policy
- This does not create mathematical novelty by itself. It only reduces methodological overlap with generic automated-discovery systems and bounded-slope CA heuristics.
