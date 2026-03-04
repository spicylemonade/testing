# 012 — Quantum-Inspired Annealing

## Topic Context

Quadratic Unconstrained Binary Optimization (QUBO) is the native problem formulation for quantum annealers (D-Wave) and many quantum-inspired classical algorithms. The protein multi-site optimization problem maps naturally to QUBO: each binary variable represents whether a specific amino acid is placed at a specific position, with one-hot constraints ensuring exactly one amino acid per position.

Mohseni et al. (2024, arXiv) demonstrated that a quantum-inspired reformulation of protein design outperforms conventional sequence optimization **even when run on classical machines**. The key insight is that the QUBO encoding forces explicit representation of pairwise interactions, which classical optimizers can exploit through specialized decomposition techniques (e.g., Burer-Monteiro relaxation, belief propagation).

For thermostability optimization, the QUBO Hamiltonian has a clear physical interpretation: h terms are single-mutation free energy changes, J terms are pairwise epistatic couplings, and the ground state is the most stabilizing mutation combination. Simulated annealing with parallel tempering is a well-understood solver for this class of problems.

## Key Connections

- **Ising model analogy**: The QUBO is literally an Ising model — decades of statistical physics techniques apply
- **Sparse J matrix**: If epistasis is sparse (Concept 002), the Ising model has few frustrated interactions and annealing converges faster

## Implementation Backlog

1. [ ] Implement QUBO formulation from positions, amino acids, and scores
2. [ ] Add one-hot constraints via penalty terms
3. [ ] Implement simulated annealing solver
4. [ ] Implement parallel tempering with replica exchange
5. [ ] Integrate D-Wave neal sampler (pip install dwave-neal)
6. [ ] Set h terms from ESM-2 single-mutant scores
7. [ ] Set J terms from double-mutant epistasis or GNN prediction
8. [ ] Benchmark against beam search and MCTS
9. [ ] Measure solution diversity (number of distinct near-ground-state solutions)
10. [ ] Profile annealing convergence: sweeps vs energy for different graph sparsities
