# 012 — Quantum Annealing Analog

## Concept

Quadratic Unconstrained Binary Optimization (QUBO) formulates optimization over binary variables as maximizing x^T Q x, where Q encodes both linear preferences (diagonal) and pairwise interactions (off-diagonal). This is mathematically equivalent to finding the ground state of an Ising spin glass — exactly the problem quantum annealers like D-Wave are designed to solve.

The quantum annealing analog reformulates Collatz delay maximization as a QUBO problem. Each bit x_i of the integer n becomes a binary decision variable. The delay function is approximated as a quadratic form: delay(n) ≈ sum_i a_i x_i + sum_{i<j} b_{ij} x_i x_j. The interaction matrix Q, fitted from training data, reveals which bit positions cooperate or compete in producing long trajectories.

Even without a quantum computer, this formulation is valuable: the Q matrix exposes the quadratic structure of the delay landscape, and classical solvers (simulated annealing, tabu search, branch-and-bound) can exploit this structure far more efficiently than brute-force enumeration.

## Cross-Domain Connections

- **D-Wave quantum annealing**: D-Wave processors natively solve QUBO problems by physically implementing quantum tunneling through energy barriers. If the quadratic approximation is accurate, delay maximization could be mapped directly onto quantum hardware.
- **Ising model in statistical physics**: The Ising model describes interacting spins on a lattice. The QUBO formulation of Collatz delays reveals an analogous interaction structure among bits, where "ferromagnetic" couplings (b_{ij} > 0) indicate bit pairs that jointly increase delay.
- **Hopfield networks**: Hopfield networks store patterns as energy minima of a quadratic energy function over binary neurons. The QUBO delay model is a Hopfield network whose energy landscape encodes delay information — high-delay numbers are low-energy attractors.
- **MAX-CUT and combinatorial optimization**: Many classic combinatorial problems (MAX-CUT, graph coloring, satisfiability) have natural QUBO formulations. The delay maximization QUBO connects Collatz theory to the rich toolkit of combinatorial optimization.

## Implementation Backlog

1. **Training data preparation** — Compute delays for all B=30 bit integers (or a large sample). Construct feature matrix with all linear and quadratic terms x_i and x_i * x_j.
2. **LASSO-regularized quadratic fit** — Fit delay(n) ≈ x^T Q x using LASSO regression to induce sparsity in Q, revealing the most important bit interactions. Evaluate R^2 on held-out data.
3. **Exact QUBO solution for small B** — For B ≤ 20, solve the QUBO exactly via exhaustive search or branch-and-bound. Compare the QUBO-optimal solution to the true delay champion at that bit length.
4. **Simulated annealing for large B** — For B = 30–64, use simulated annealing on the QUBO objective. Compare SA-found optima to known delay records.
5. **Interaction structure analysis** — Visualize the Q matrix as a heatmap. Identify clusters of strongly interacting bits. Test whether the interaction pattern is consistent across different bit lengths (universality) or changes qualitatively (phase transitions).
