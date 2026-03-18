# Concept Delta

## Suggestion

The strongest ConceptEvolve signals after the mandatory `evolve` and `probe` runs were:

- `coupled_peeling_with_exact_templates`
- `sat_plus_egraph_symbolic_backbone`
- `observer_guided_macrocell_search`

The common suggestion was to keep the search local and automaton-shaped, but force every local update to stay attached to exact witness legality rather than to free-form spatial dynamics.

The later mandatory `reframe` pass added `11` broader domain views, with the most useful ones being:

- proof-labeling schemes
- group-testing / peeling
- Petri-net coverability
- network coding

The later mandatory `iterate` pass then converted those ideas into bridge decisions:

- promote `proof_carrying_exact_decoder_bridge`
- promote `spatially_coupled_peeling_ladders`
- promote `sat_egraph_symbolic_backbone`
- retire `anisotropic_current_screening`
- retire `odometer_rotor_transport_bridge`
- retire `observer_guided_macrocell_search`

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
- `results/concept_evolve/reframings.json`
  - confirmed that the best experiment-phase analogies still emphasize local certificates, sparse seeds, peeling, and monotone closure
  - did not justify opening a new non-CA or modular-first lane
- `results/concept_evolve/bridge_candidates.json`
  - promoted three exact-decoder-compatible bridges and retired the most proxy-heavy ones
- `results/concept_evolve/concept_delta.json`
  - collapsed the final focus to verifier recovery, tiny exact gadget seeds, SAT legality pruning, and e-graph span caching

## Result

- The ConceptEvolve output did not justify opening a neural-CA or modular curriculum lane.
- It did strengthen the case for a proof-carrying, stage-indexed CA whose state decodes directly to `(X,G,R,T)`.
- The verifier blocker still dominates execution risk, so the delta is architectural and falsification-oriented rather than experimental.
- The completed `reframe` output widened the analogy set without moving the active lane: it sharpened vocabulary around proof-carrying local certificates but did not produce a better empirical target than the current H1 design.
- The later `reframe` pass broadened the analogy set into proof-labeling schemes, group-testing peeling, Petri-net coverability, network coding, Datalog saturation, sheaf consistency, and synchronizing automata.
- Those reframings reinforced the local-certificate / singleton-isolation interpretation of the task, but they did not justify changing the champion lane or relaxing the exact-verifier gate.
- The final `iterate` pass narrowed the actionable bridge set to three promoted ideas and explicitly retired the transport-proxy and observer-heavy bridges.

## Novelty Delta

- Before ConceptEvolve integration, the lane risked collapsing into generic CA search over a serialized witness.
- After integration, the active lane is narrower and more defensible:
  - direct product-grid witness representation
  - proof-carrying symbolic state
  - exact decoder contract
  - no-repair rejection policy
- After the `reframe` pass, the novelty story is also better bounded:
  - reframed domains are treated as hypothesis generators, not as substitute prior-art clearance
  - the strongest transferable idea is local proof-labeling / peeling, not generic learned morphology
- After the `iterate` pass, the novelty story is also operationally narrower:
  - exact-decoder-compatible bridges stay alive
  - proxy-dynamics bridges are retired rather than left ambiguously “interesting”
- This does not create mathematical novelty by itself. It only reduces methodological overlap with generic automated-discovery systems and bounded-slope CA heuristics.
