# Concept Tree Expansion: Baseline Limitations

## The Scaling Wall
Our evaluation of $P(17)$, $P(37)$, and $P(41)$ using spectral bounds (Hoffman and heuristic $\vartheta$) explicitly proved that the continuous algebraic relaxation is perfectly accurate for $N < 25$, where the gap between the discrete clique size and the spectral relaxation is small.

However, as the graph size scales toward $N \approx 43$:
*   The gap between $\alpha(G)$ and the Lovász bound $\vartheta(G)$ grows asymptotically.
*   A purely $K_5$-free graph on 43 vertices could easily have a continuous spectral penalty $\vartheta(G) = 6.5$.
*   Thus, Hoffman and Lovász bounds cannot theoretically prove $R(5,5) \le 46$.

## Limitations of Previous Non-Computational Approaches

### Linear Programming (McKay, 2024)
*   **The Limit**: Relies on explicitly bounded constraints involving the exact number of subgraphs (edges, paths, triangles, $K_4$). While LP solvers scale well, the sheer number of necessary structural flag-algebraic constraints explodes at $N > 46$. To go beyond $46$, McKay required millions of parallel LP runs over exhaustive triangle density spaces.

### Statistical Majorana Embeddings (Tamburini, 2025)
*   **The Limit**: Tamburini uses random projections over an algebraic ring to produce a *probabilistic heuristic* (which points to $R(5,5)=45$). The heuristic relies on empirical scaling properties of the expected clique number, not an absolute, rigorous formal constraint.

### Spectral Invariants and Shannon Capacity (Alon & Lubetzky, 2006)
*   **The Limit**: The exact Lovász $\vartheta$ is bounded by the positive semidefiniteness (PSD) of the adjacency matrix variants. Since PSD is a continuous property, the geometry of the PSD cone guarantees a slack between discrete boolean subgraphs (which cannot contain a "fractional" $K_5$) and the cone's continuous boundaries.

## Bridging to Core Novelty
To break this continuous relaxation gap and the discrete LP combinatorial explosion, we must encode the exact boolean constraint algebraically *without* relaxing it to PSD constraints or solving for subgraphs explicitly. This points directly to our next phase:
1. **Tensor Networks**: Computing the exact norm of an exact discrete constraint network (Quantum Tensor Network Scaling).
2. **GFlowNet / Partition Functions**: Using generative flow networks to capture the exact entropy collapse when $Z(N)$ is constrained by discrete zeros (Thermodynamic Flow Rate Analysis).
