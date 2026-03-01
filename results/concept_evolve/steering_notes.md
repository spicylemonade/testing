# ConceptEvolve Steering Notes

## Steering Direction 1: Density-Adaptive Hybrid Algorithm with Recursive Interval Decomposition

**Concept sources:** Recursive Subproblem Decomposition, Sampling-Based Pivot Selection, Information-Theoretic Distance Compression

**Direction:** Design a hybrid algorithm that adapts its strategy based on graph density regime:
- For sparse graphs (m = O(n)): use a simplified Duan et al.-style recursive decomposition with pivot sampling, targeting O(m * f(n)) where f(n) = o(log n)
- For dense graphs (m = Theta(n^2)): use distance-bucketing inspired by information-theoretic compression, exploiting that dense graphs have more structured distance distributions
- The key novelty: an **adaptive interval width** that is tuned based on the empirical distance distribution, not a fixed parameter

**Informs rubric items:** item_012 (SOTA implementation), item_014 (novel algorithm design), item_015 (novel implementation), item_016 (data structures)

## Steering Direction 2: Batch-Relaxation with Amortized Potential Analysis

**Concept sources:** Lazy Evaluation and Deferred Computation, Amortized Potential Function Design, Thermodynamic Relaxation Analogy

**Direction:** Instead of relaxing edges one-at-a-time via priority queue extract-min, batch edge relaxations into groups of size B = Theta(sqrt(m/n)). Within each batch, use radix-sort or bucket-sort (O(B) time for bounded-range distances) instead of comparison-based PQ operations. The potential function tracks the total "excess distance" across all vertices.

**Key insight:** The sorting barrier applies to comparison-based algorithms. Bucketing/radix approaches bypass comparisons by using the arithmetic structure of distances. Even for real weights, discretizing to O(log n) bits of precision and using word-level bucket operations can shave the log n factor.

**Informs rubric items:** item_014 (novel algorithm design), item_016 (data structures), item_017 (correctness proof)

## Steering Direction 3: Partial-Order Priority Queue with Epsilon-Scaling (Primary Focus)

**Concept sources:** Topological Sorting Bypass via Partial Orders, Auction algorithm epsilon-scaling insight, Persistent homology analogy

**Direction:** Implement a multi-scale SSSP algorithm inspired by epsilon-scaling from auction/network flow algorithms:
1. Start with coarse distance approximation (large epsilon)
2. Use approximate distances as Johnson-style potentials to reduce edge weights
3. Refine distances at each scale, halving epsilon
4. At each scale, the reduced graph has small weight range, enabling faster processing

This is essentially the approach that Duan et al. 2026 uses to achieve O(m sqrt(log n)), but we can potentially:
- Improve the constant factors by better scale-transition logic
- Achieve better practical performance by adapting the number of scales to the actual weight distribution
- Provide a cleaner, more modular implementation that is easier to benchmark

**Why prioritized first:** This direction is the most concrete and directly implementable. It builds on the proven Duan et al. framework while offering clear avenues for improvement. The epsilon-scaling perspective from auction algorithms provides a clean framework for understanding and potentially improving the multi-scale approach. It also directly targets the stated goal: o(m + n log n) operations, with O(m sqrt(log n)) as the concrete target.

**Informs rubric items:** item_012, item_013, item_014, item_015, item_016, item_017, item_022 (ablation on number of scales)
