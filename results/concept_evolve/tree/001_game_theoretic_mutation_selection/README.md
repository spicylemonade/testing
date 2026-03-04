# 001 — Game-Theoretic Mutation Selection

## Topic Context

Combinatorial protein stability optimization requires selecting amino acid substitutions at multiple positions simultaneously. The brute-force approach scales as O(20^k) for k positions, which is intractable for k > 5. Game theory provides a principled decomposition: treat each mutable position as a player choosing an amino acid, with the stability score as the shared payoff. Nash equilibria of this game represent mutation combinations where no single-position change improves the result — a natural local optimality criterion.

**GameOpt** (Bal et al., ICLR 2025) demonstrated this approach for combinatorial Bayesian optimization in protein design, achieving efficient exploration of 20^X configuration spaces. The key insight is that best-response dynamics — where each player sequentially optimizes their choice given others' current choices — converges rapidly when pairwise interactions (epistasis) are moderate, reducing O(20^k) to O(k × 20 × iterations).

## Key Connections

- **Epistasis as payoff coupling**: Strong epistasis between positions i and j means player i's optimal choice depends on j's choice — this IS the strategic interaction structure
- **Convergence guarantees**: For potential games (where a global potential function exists), best-response dynamics converges to a Nash equilibrium in finite time
- **Protein fitness landscapes often approximate potential games**: If ddG is approximately decomposable into pairwise terms, the game has a potential

## Implementation Backlog

1. [ ] Implement ESM-2 masked marginal scorer for single and multi-mutant evaluation
2. [ ] Implement best-response dynamics optimizer with configurable iteration limit
3. [ ] Add convergence detection (no player changes action for a full sweep)
4. [ ] Add randomized best-response order to avoid cycling
5. [ ] Implement correlated equilibrium computation via linear programming for small k
6. [ ] Benchmark on Mega-scale dataset proteins
7. [ ] Compare with greedy accumulation and beam search baselines
8. [ ] Profile GPU utilization and optimize batching of scorer calls
9. [ ] Add support for position constraints (excluded/required positions)
10. [ ] Integrate with cascading funnel scoring pipeline
