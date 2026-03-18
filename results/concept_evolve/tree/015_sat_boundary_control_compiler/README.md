# sat_boundary_control_compiler
Compile finite-time forcing into SAT or MaxSAT, viewing the initial singleton seeds and already-forced vertices as boundary controls for a cellular automaton. The solver searches jointly over edge labels, seeds, and infection schedules while minimizing m(G)+|R| under exact logical constraints.
## Domains
satisfiability, control_theory, cellular_automata, additive_combinatorics
## Mathematical Sketch
Introduce Boolean variables for edge labels, seed placements, time-layered infection events inf(e,t), and bounded coefficient choices for local derivations. Constrain inf(e,t+1) to hold iff inf(e,t) already holds or some allowed local certificate produces a(1,-1) at e using support inside T_t union {e}; minimize sum(edge_used) + sum(seed_used).
## Why This Bridge Might Matter
This would be the first exact SAT compilation of arithmetic Kakeya constructible certificates as steerable CA trajectories.
## Implementation Backlog
- Build: solver/sat_encoding.py
- Build: solver/symmetry_breaking.py
- Test: Attempt exact synthesis on 2-layer and 3-layer product grids with small X, then benchmark whether MaxSAT can rediscover known near-bound motifs or prove small instances impossible.
- Check: It is not generic graph generation and not generic CA controllability: the Boolean model must encode integer-labelled edge differences, anti-diagonal detection, and the score objective from the verifier.
## Closest Prior Art
- Regional Controllability of Cellular Automata as a SAT Problem (arXiv:2504.03691)
- SAT-Based Generation of Planar Graphs (DOI:10.4230/LIPIcs.SAT.2023.14)
- Generalized Arithmetic Kakeya (arXiv:2411.13395)
