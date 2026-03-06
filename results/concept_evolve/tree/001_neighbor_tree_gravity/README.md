# neighbor_tree_gravity

## Context
Combine exact near-field gravity from molecular-dynamics-style neighbor lists with Barnes-Hut or fast-multipole far fields. The result is a minimal simulator that keeps close passes crisp without paying O(N^2) everywhere.

## Domains
- astrophysics
- molecular_dynamics
- numerical_analysis

## Mathematical Formalization
a_i = sum_{j in N_i(r_n)} G m_j r_ji / (||r_ji||^2 + eps_i^2)^(3/2) + M_theta(Far(i)); choose r_n, theta so that ||delta a_i|| < eta

## Closest Prior Art
- REBOUND: An open-source multi-purpose N-body code for collisional dynamics (`5240c4a18da2b6dcae3fbfa633c01bee1670d0a0`)
- A hierarchical O(N log N) force-calculation algorithm (`fce7fd98928ab9bf3e4e919e108c48fc1040f569`)
- A fast algorithm for particle simulations (`688384fc5e643445e835435e96b9dfcfb6598d36`)

## Novelty
The novelty is the interface boundary: the simulator is organized around an explicit near/far split that matches interactive workloads, rather than around a monolithic research code or a single global approximation.

## Differentiation
Barnes-Hut and FMM accelerate all interactions, while molecular-dynamics neighbor lists usually assume short-range cutoffs. This concept fuses them for gravity by keeping local exactness without pretending the force law is actually truncated.

## Experiment Seed
Benchmark 2-body, Plummer-sphere, and ring scenes at N in {16, 128, 1024}; compare wall-clock time, force error, and orbit drift against direct summation and pure Barnes-Hut.

## Implementation Backlog
1. Implement a dense direct-sum reference kernel.
2. Build the cell hash and rolling neighbor list.
3. Add a Barnes-Hut far-field path with an error budget.
4. Introduce an auto-fallback threshold and profiling hooks.
5. Benchmark against analytic 2-body and dense-reference scenes.

## Planned Paths
- `results/concept_evolve/tree/001_neighbor_tree_gravity/concept.json`
- `results/concept_evolve/tree/001_neighbor_tree_gravity/README.md`
- `results/concept_evolve/tree/001_neighbor_tree_gravity/literature.json`
- `prototypes/minigrav/force/neighbor_tree.py`
- `prototypes/minigrav/benchmarks/neighbor_tree_accuracy.py`
