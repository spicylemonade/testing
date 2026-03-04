# 002 — Epistasis-Aware Sparse Search

## Topic Context

Epistasis — the non-additive interaction between mutations — is the fundamental reason why combinatorial optimization is needed rather than simply stacking the best single mutations. However, empirical studies consistently show that epistasis is **sparse**: most mutation pairs interact additively, and significant epistatic interactions are concentrated among structurally proximal residues.

Ranganathan et al. (Nature Communications 2019) showed that in a comprehensive study of all 2^13 mutants linking two fluorescent protein variants, high-order epistasis exists but is "extraordinarily sparse," enabling accurate phenotype prediction from limited measurements. Tokuriki (Nature Communications 2023) found pervasive but structurally localized epistasis in enzyme evolution.

This sparsity is the key to breaking the combinatorial explosion: if 8 mutable positions decompose into 3 independent clusters of sizes {3, 3, 2}, the search space drops from 19^8 ≈ 17 billion to 19^3 + 19^3 + 19^2 ≈ 14,000 — a million-fold reduction.

## Key Connections

- **Compressed sensing analogy**: Just as sparse signals in high-dimensional spaces can be reconstructed from a small number of measurements, sparse epistatic landscapes can be characterized from a small number of double-mutant measurements
- **Graph decomposition**: The interaction graph's connected components define independent subproblems, directly analogous to graph coloring decomposition in constraint satisfaction

## Implementation Backlog

1. [ ] Implement pairwise epistasis calculator: e_{ij} = ddG(i,j) - ddG(i) - ddG(j)
2. [ ] Build interaction graph construction with configurable threshold
3. [ ] Implement connected component decomposition
4. [ ] Add within-component exhaustive search (for small components) and beam search (for large)
5. [ ] Implement cross-component combination of solutions
6. [ ] Validate sparsity assumption on Mega-scale double mutant data
7. [ ] Benchmark search efficiency vs full combinatorial search
8. [ ] Add GNN-predicted epistasis as alternative to computed epistasis
9. [ ] Handle the case of a single large connected component (fallback to beam search)
10. [ ] Profile computational cost of pairwise evaluation phase
