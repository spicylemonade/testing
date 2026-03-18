# Anisotropic Current Screening

Treat each nonzero vector in X as a particle species in a number-conserving cellular automaton. Instead of decoding every trajectory, rank trajectories by how strongly they suppress the forbidden (1,-1) channel relative to legal slope channels, then exact-decode only the best candidates.

## Context
State lattice s_t : \Lambda -> \{0\} \cup (X \setminus \{(0,0)\}). For each species x define a directional current J_x(T) = \sum_{t<T}\sum_{u\in\Lambda} \langle d_x, \mathrm{step}_t(u)\rangle. Decode a trajectory to a witness W and rank by \Psi(W) = S(W) + \lambda \max\{0, J_{(1,-1)} - \beta \min_{x\in X\setminus\{0\}} J_x\}.

## Implementation Backlog
- Prototype the bridge: Enumerate small radius-1 conservative CA on tori, assign one species per candidate slope, evolve sparse seeds, extract periodic worldlines and collision graphs, and decode only the top-ranked trajectories into candidate nonzero f_i entries and seed R/T data.
- Run the seed test: Use X={(0,0),(1,0),(0,1),(1,1),(2,1)} on 4x4 and 5x5 tori. Compare current-ranked decoding against random decoding and species-label shuffles at the same trajectory budget.
- Add label-shuffle, geometry-shuffle, and density-matched controls before trusting any signal.
- Keep the direction only if exact verifier outcomes improve, not just proxy metrics.

## Closest Prior Art
- On the arithmetic Kakeya conjecture of Katz and Tao (10.1007/s10998-018-0270-z)
- Additive conserved quantities in discrete-time lattice dynamical systems (10.1016/0167-2789(91)90150-8)
- Cellular automaton rules conserving the number of active sites (10.1088/0305-4470/31/28/014)

## Novelty Delta
The new ingredient is a score-aware directional-current statistic tied directly to arithmetic witness decoding, rather than generic conservation-law analysis or bounded-slope heuristics.

## Why It Is Distinct
This is not a reimplementation of number-conserving CA classification because the automaton is only a ranking prior, and it is not a restatement of arithmetic Kakeya because the output is an explicit local dynamical compiler into witnesses.
