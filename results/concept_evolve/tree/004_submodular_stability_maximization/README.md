# 004 — Submodular Stability Maximization

## Topic Context

Submodular functions — set functions with the diminishing returns property — appear throughout combinatorial optimization and have a rich theoretical foundation of approximation guarantees. The classic result (Nemhauser, Wolsey, Fisher 1978) states that greedy maximization of a monotone submodular function subject to a cardinality constraint achieves at least (1-1/e) ≈ 63% of the optimal value, and this bound is tight.

The key question for protein stability is: **is the multi-mutant stability improvement function approximately submodular?** Intuitively, if each added mutation contributes less to stability as the protein is already stabilized (diminishing returns from filling the stability "gaps"), then submodularity holds. This is plausible for stabilizing core packing mutations but may fail for surface mutations that act through long-range electrostatic networks.

Even approximate submodularity (bounded curvature) yields approximation guarantees: for curvature c, greedy achieves (1 - c/e) approximation (Sviridenko, Vondrák, Ward 2017).

## Key Connections

- **Lazy greedy evaluation** accelerates the algorithm by caching marginal gains and skipping evaluations that cannot improve the best candidate
- **Connection to beam search**: Greedy is beam search with width 1; increasing beam width trades guaranteed approximation for better empirical performance

## Implementation Backlog

1. [ ] Implement monotone submodular greedy with cardinality constraint
2. [ ] Implement lazy (accelerated) greedy evaluation
3. [ ] Build submodularity testing utility: sample random (S, T, v) triples and check diminishing returns
4. [ ] Compute curvature parameter from sampled evaluations
5. [ ] Compare greedy solution quality to beam search (width 10, 50, 100)
6. [ ] Test on proteins where submodularity clearly holds vs. clearly fails
7. [ ] Implement randomized variant (SAMPLEGREEDY from Feldman et al. 2017)
8. [ ] Benchmark on Mega-scale proteins with known multi-mutant data
