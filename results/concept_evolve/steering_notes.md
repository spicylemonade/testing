# Steering Notes: Chvátal–Sankoff Constant Research

## 3 Concrete Steering Directions

### Direction 1: Scaled-up Lueker/Heineman Computation (PRIORITIZED)
**Summary:** Push the feasible-triplet lower bound framework to larger state spaces using symmetry exploitation (bit-flip, string-swap), vectorized operations, and sparse linear algebra. Target ℓ=10–12 to potentially exceed the current best lower bound of 0.792665992.

**Rubric items informed:** item_009, item_012, item_017, item_019, item_022

**Why prioritized:** This direction has the highest probability of producing a concrete, rigorous improvement. The Heineman et al. [H2024] result at h=15 with specialized hardware yielded 0.792665992. Our approach uses a different parametrization (Lueker's feasible-triplet framework rather than Heineman's direct DP), which may have different convergence properties. By exploiting symmetries and modern numerical linear algebra (scipy.sparse, numpy vectorization), we can potentially reach parameter regimes that yield bounds competitive with or exceeding Heineman et al. This is a computationally intensive but mathematically well-understood path with clear acceptance criteria.

### Direction 2: Information-Theoretic / Deletion Channel Upper Bound
**Summary:** Establish a formal connection between γ₂ and the binary deletion channel capacity C_del(1/2). Recent bounds (Cheraghchi 2020: C_del(1/2) ≤ 0.4943) may translate to an upper bound on γ₂ tighter than Lueker's 0.826280. The key insight from the concept tree is that the LCS of random strings is intimately related to the information capacity of a deletion channel.

**Rubric items informed:** item_013, item_014, item_016, item_018

**Why this direction:** The 0.826280 upper bound has stood since 2009. Any improvement would be a significant contribution. The information-theoretic approach is qualitatively different from Lueker's LP/automata framework and may bypass its structural limitations. Even a partial result (e.g., a conjectural bound with numerical evidence) would be valuable.

### Direction 3: Last-Passage Percolation Bridge and Monte Carlo Estimation
**Summary:** Exploit the connection between LCS and Bernoulli last-passage percolation (LPP). The Bernoulli model has exact constant 2(√2−1) ≈ 0.8284. Quantifying the correlation penalty between the Bernoulli model and the true LCS model provides an upper bound γ₂ ≤ 0.8284 − δ. Simultaneously, high-precision Monte Carlo with finite-size scaling narrows the empirical estimate of γ₂.

**Rubric items informed:** item_007, item_010, item_015, item_018, item_019

**Why this direction:** This connects to the rich literature on integrable probability and KPZ universality. Even if the rigorous coupling bound doesn't improve on 0.826280, the numerical evidence and scaling analysis provide essential context for evaluating all other approaches.

## Priority Ranking

1. **Direction 1 (Lueker/Heineman computation)** — Highest confidence in producing rigorous results
2. **Direction 2 (Information-theoretic upper bound)** — Highest potential novelty and impact
3. **Direction 3 (LPP bridge + Monte Carlo)** — Essential baseline and complementary evidence

## Concept Tree Walk Paths of Note

From `walk_paths.json`, the most informative paths:
- `information_bottleneck_lcs → replica_free_energy → tensor_network_contraction → markov_chain_automaton_refinement` (connects information theory to practical computation)
- `last_passage_percolation_bridge → hammersley_process_coupling → stochastic_particle_duality` (connects integrable probability to particle systems)
- `sdp_relaxation_alignment → tropical_lcs_geometry → convex_relaxation_hierarchy` (connects optimization hierarchy to algebraic structure)
