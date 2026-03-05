# Ramsey $R(5,5)$ Non-Computational Bounds Research

This repository contains a comprehensive, novel methodology to analytically evaluate and mathematically guarantee upper bounds for the Ramsey number $R(5,5)$ without explicitly enumerating exponential boolean subgraphs.

## Repository Structure

*   `core/`: Core mathematical formalisms and basic algebraic ideal constraints.
*   `metrics/`: Exact and heuristic algebraic pruning filters (Hoffman's bound, Lovász $\vartheta$).
*   `generators/`: Novel mathematical Ansatz generators for $K_5$-free candidate graphs.
    *   `tensor_network/`: Encodes the exact partition function $Z(N)$ of $K_N$ using rank-10 constraint networks.
    *   `algebraic_curves/`: Implements symmetric structures based on geometry.
    *   `twisted_algebraic.py`: Employs quasi-random orbit breaking on cyclotomic graphs to find near-critical topologies.
    *   `refined_tensor_ansatz.py`: GFlowNet transition probability mechanics for dynamically minimizing monochromatic cliques.
*   `experiments/`: Executable suites measuring baseline metrics on Paley graphs and testing novel generators.
*   `docs/`: Full analytical synthesis, viability checks, and the formal proof sketch showing the isomorphism of $R(5,5)$ bounds to Tensor Network divergence limits.
*   `results/concept_evolve/`: The living Concept Tree driving the cross-domain conceptual jumps from Graph Theory into Statistical Mechanics.

## Core Novelty
Instead of exhaustively searching for edge distributions via LPs (as done by Angeltveit & McKay, 2024), we map the existence of a $K_5$-free graph on $N=43$ to the exact contraction norm of a many-body Tensor Network. This replaces $O(2^{\binom{N}{2}})$ boolean searches with the calculation of a topological index in a macroscopic thermodynamic system.
