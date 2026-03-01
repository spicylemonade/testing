# ConceptEvolve Steering Notes

## Three Concrete Steering Directions

### Direction 1: Hierarchical Frontier Decomposition with Spectral Potentials
**Concept Bridge:** HierarchicalCoarsening → SpectralDistanceEstimation → PotentialFunctionGuidance

**Key Idea:** Use spectral graph theory to compute initial distance estimates (potentials) at multiple resolution levels. The spectral embedding gives approximate distances that serve as potentials for Dijkstra-like exploration. With good potentials, most edges become "tight" (zero reduced cost) and don't need processing. The hierarchy allows coarse-level potentials to be computed once and refined locally.

**Informed Rubric Items:** item_011 (concept exploration), item_012 (novel algorithm design), item_013 (core data structure — the hierarchical potential oracle), item_016 (complexity analysis)

### Direction 2: Adaptive Batch Processing with Entropy-Based Budgeting
**Concept Bridge:** RecursiveFrontierPartitioning → BatchedLazyPropagation → EntropyBudgetedExploration

**Key Idea:** Instead of processing vertices one-at-a-time, process them in batches whose size adapts to the local graph structure. Batches in "easy" regions (low distance-entropy, meaning distances are well-separated and predictable) are large and processed cheaply. Batches in "hard" regions are small and get more careful treatment. This adaptive approach spends fewer total comparisons than uniform batching.

**Informed Rubric Items:** item_012 (novel algorithm design), item_013 (core data structure — adaptive batch priority queue), item_014 (implementation), item_016 (complexity analysis)

### Direction 3: Recursive Frontier Reduction with Improved Partition Balance
**Concept Bridge:** RecursiveFrontierPartitioning → TopologicalFiltration → LocalitySensitiveRelaxation

**Key Idea:** Improve on the Duan-Mao frontier-reduction framework by using a weight-based filtration to define more balanced partitions. The filtration ensures each partition level has bounded diameter, enabling locality-sensitive relaxation within partitions. The key improvement over Duan et al.: instead of splitting frontiers by distance rank (which requires partial sorting), split by graph-structural properties (connected components in threshold subgraphs), which can be computed in O(m) time.

**Informed Rubric Items:** item_011, item_012 (novel algorithm design — direct improvement on Duan et al.), item_014 (implementation), item_015 (correctness proof), item_017 (negative weight extension via LDD synergy)

## Prioritized Direction

**Priority: Direction 3 (Recursive Frontier Reduction with Improved Partition Balance)**

**Rationale:** This direction is the most directly actionable because it builds on the existing state-of-the-art (Duan et al.'s frontier-reduction framework) rather than starting from scratch. The improvement is concrete and analyzable: replacing the distance-rank-based partition with a structural partition saves a sub-logarithmic factor. The approach has the clearest path to a provable improvement over O(m√(log n)), and the implementation can be verified against the Duan et al. baseline. Additionally, the structural partitioning technique connects to LDDs, which opens a natural path to the negative-weight extension (item_017).

Direction 1 (spectral potentials) is theoretically appealing but requires computing eigenvectors, which is O(m · polylog n) in the best case and may not lead to a clean comparison-addition model result. Direction 2 (entropy budgeting) is novel but harder to analyze formally.
