# Director Brief

## Decision

Champion: `H1_defect_syndrome_ca_64m`.

This is the best novelty-to-falsifiability tradeoff in the current swarm output. It is anchored to the actual order-`668` frontier object, keeps the CA claim narrow enough to defend, and has the cleanest kill test: from the same seed and the same coordinate system, a real CA repair dynamic must beat matched greedy/tabu/simulated-annealing repair on exact-feasibility outcomes, not just on prettier defect traces.

Backup: `H2_lag_space_ca_167`.

This is the best hedge if the defect-transport locality assumption fails on the modular seed. It preserves some genuine representation-level novelty, but only if it avoids collapsing back into `Williamson`, `Turyn`, cocyclic, or other already-structured sequence families. The drop rule is simple: if success requires re-entering a known family, relabel it as optimizer-over-known-family and stop treating it as a new direction.

Hold / reserve: `H3_spacetime_row_emission_ca`.

This is the most radical and compressive idea, but it is the weakest fit to the present `668 = 4 x 167` frontier and the most exposed to prior CA-construction overlap. It should not consume the first execution budget.

## Framing Constraints

- Treat `cellar automata` as `cellular automata`; no separate method family is evidenced in the repo.
- Do not claim CA is new for Hadamard matrices in general. The defensible novelty claim is narrower: CA is not established here as an exact-search repair dynamic for the open real order-`668` case, especially when seeded from the new `64`-modular frontier object.
- Do not claim progress on Hadamard `668` unless exact orthogonality is reached up to standard equivalence. Better defect counts or modular residuals are not a solution.

## Blocker And Handoff

Current blocker: the repo snapshot cites the `64`-modular order-`668` frontier result, but it does not include the actual seed matrix, generating quadruple, or a canonical benchmark harness around that object.

Exact next experiment for the researcher:

1. Acquire the cited `64`-modular order-`668` seed or its generating quadruple and canonicalize it under standard symmetries.
2. Build one compressed defect representation for `H1` and one seed-matched non-CA control in the same coordinates.
3. Run only the first kill test: CA versus greedy, tabu, and simulated annealing from identical seeds under identical evaluation budgets, with exact-hit rate as the gate metric.
4. Stop immediately if the defect support plateaus, diffuses, or loses any advantage once the baselines are seed-matched.

If `H1` fails because the locality assumption is false rather than because of weak implementation, move to `H2` with the family-leakage audit turned on from the first run.
