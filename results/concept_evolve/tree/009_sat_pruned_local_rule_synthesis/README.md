# Sat Pruned Local Rule Synthesis

Encode periodic CA trajectories, local witness-decoding constraints, and symmetry or integrality requirements as a SAT family that enumerates only admissible local rules. This shrinks the CA search space into a proof-carrying rule-synthesis problem before any stochastic search or learning begins.

## Context
Boolean variables describe local rule-table entries, orbit bits on a periodic torus, and decoded nonzero incidences in f_i,R,T. Constraints enforce locality, optional conservation or reversibility, and exact decoder legality. Solve \exists F,\Omega\; \mathrm{SAT}(F,\Omega,\sigma) where \sigma bounds score and orbit period.

## Implementation Backlog
- Prototype the bridge: Start with tiny radii and short periods, add symmetry breaking for rotations and species relabeling, enumerate minimal feasible rules with SAT, and lift those rules into larger exact searches or learned initializations.
- Run the seed test: Target period-4 or period-6 torus orbits with 2-3 species and compare SAT-enumerated rules against random rule sampling on exact-valid output rate.
- Add label-shuffle, geometry-shuffle, and density-matched controls before trusting any signal.
- Keep the direction only if exact verifier outcomes improve, not just proxy metrics.

## Closest Prior Art
- SAT-Based Analysis of Cellular Automata (10.1007/978-3-540-30479-1_77)
- egg: Fast and extensible equality saturation (10.1145/3434304)
- AlphaEvolve: A coding agent for scientific and algorithmic discovery (arXiv:2506.13131)

## Novelty Delta
SAT is used here to synthesize only those CA rules whose spacetime diagrams decode to exact arithmetic witnesses, not merely to analyze a fixed automaton.

## Why It Is Distinct
Unlike generic agentic search, the constraints bake in the six-line witness semantics and exact score accounting from the outset.
