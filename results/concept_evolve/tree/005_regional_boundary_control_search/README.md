# regional_boundary_control_search

## Topic context
Translate the micro-level CA design problem into a SAT-style regional controllability problem. Boundary conditions, local rule tables, and exact extraction constraints are solved together so that only microdynamics capable of targeting a prescribed solved region survive.

Primary domains: cellular_automata_control, sat_smt, additive_combinatorics.

Mathematical sketch:
Introduce Boolean variables for local cell states z_{v,t}, rule-table entries \rho, and regional targets y_v. Constrain z_{v,t+1}=\rho(N(v,t)), require y_v=1 on a target shell or subrectangle, and add compilation clauses guaranteeing that the induced activation history yields legal relations in \mathbb{Z}^{2|V|}. Optimize lexicographically for feasibility, then low extracted score.

Closest prior art:
- Regional Controllability of Cellular Automata as a SAT Problem (arXiv:2504.03691)
- Differentiable Logic Cellular Automata: From Game of Life to Pattern Generation (arXiv:2506.04912)
- Graph grammar induction (DOI:10.1016/bs.adcom.2019.07.003)

Novelty claim:
The novelty is the joint satisfiability layer: local CA reachability is not enough, so the search is constrained by exact arithmetic certificate compilation from the outset.

Differentiation:
This is not ordinary CA controllability because the target is not a raw configuration. The target is a configuration whose history can be certified as a legal forcing proof under integer-support restrictions.

## Implementation backlog
- Build a minimal exact extractor for this concept before any broad search.
- Benchmark against raw arithmetic features and a no-CA baseline on the same small instances.
- Track description length, seed count, and exact score together to avoid proxy overfitting.
- Record an explicit falsifier for the concept after the first pilot sweep.
