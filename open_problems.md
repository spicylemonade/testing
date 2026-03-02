# Open Problems and Improvement Directions for SSSP

## Problem 1: The Practical Constant-Factor Gap

**Problem statement:** The Duan et al. STOC 2025 algorithm achieves O(m log^{2/3} n), which is asymptotically better than O(m + n log n) for sparse graphs. However, experimental analysis [castro2025] shows that Dijkstra's algorithm remains 3–4× faster in practice on all tested graph sizes (up to 10M vertices). The estimated crossover point is n > 10^{67}.

**Why current approaches don't solve it:** The recursive BMSSP decomposition introduces substantial overhead in constant factors: each level of recursion requires creating new subproblems, managing partial-order priority queues, and performing bookkeeping for interval boundaries. The O(m log^{2/3} n) bound hides constants estimated at ~7× Dijkstra's constant.

**Potential angle of attack:** Design a **hybrid algorithm** that uses Dijkstra for small subproblems (below a threshold n₀) and the recursive decomposition only for larger instances. Additionally, optimize the constant factor by:
- Reducing the overhead of POPQ operations via cache-friendly bucket layouts
- Using SIMD/vectorized batch operations for interval processing
- Implementing a simplified recursion that collapses shallow levels

This is primarily an engineering challenge, but could yield a provably faster algorithm in practice for graphs above a reduced crossover threshold.

## Problem 2: Closing the Randomized vs. Deterministic Gap

**Problem statement:** For undirected graphs, the randomized bound is O(m√(log n · log log n)) [duan2023] while the deterministic bound is O(m log^{2/3} n) [duan2025]. For directed graphs, the 2026 result achieves O(m√log n) deterministically. Is there a deterministic algorithm for undirected SSSP running in O(m√log n) or better — specifically, one that eliminates the log log n factor in the randomized bound?

**Why current approaches don't solve it:** The randomized algorithm benefits from random pivot selection, which avoids adversarial pivot positions. The deterministic pivot selection in Duan et al. 2025 uses a more conservative approach that introduces the log^{2/3} n factor. The 2026 improvement refines this but introduces a √(mn log n log log n) additive term for very sparse graphs.

**Potential angle of attack:** Derandomize the pivot selection using pseudorandom generators with limited independence. Specifically, O(log log n)-wise independence might suffice for the sampling step, enabling a deterministic construction. Alternatively, use the "method of conditional expectations" to deterministically find near-optimal pivots in O(m) time per level.

## Problem 3: The Undirected vs. Directed Gap for Very Sparse Graphs

**Problem statement:** For extremely sparse graphs (m = O(n)), the best known directed bound is O(n√(log n log log n)) [duan2026] while the undirected bound could potentially be O(n√log n) or even o(n√log n). Is there a fundamental reason why directed SSSP should be harder than undirected on sparse graphs?

**Why current approaches don't solve it:** The directed case cannot use MST-based decompositions (MSTs are not meaningful for directed graphs). The recursive decomposition works in both cases but the tighter analysis for undirected graphs exploits edge symmetry. For directed graphs, the boundary between "near" and "far" vertices can be more complex.

**Potential angle of attack:** Identify structural properties of directed graphs that enable cheaper processing. For instance, if the graph has bounded DAG-width or entanglement (directed analogues of treewidth), specialized algorithms could achieve near-linear time. Alternatively, develop a preprocessing step that identifies and contracts strongly-connected components, reducing the effective graph size.

## Problem 4: Adaptive Algorithms Based on Graph Structure (ConceptEvolve-Inspired)

**Problem statement:** Current SSSP algorithms use worst-case bounds that don't exploit specific structural properties of the input graph. Can we design an algorithm that is adaptive to the "difficulty" of the input — running in near-linear time on "easy" graphs (road networks, grids, bounded-treewidth graphs) and gracefully degrading to O(m log^{2/3} n) on the hardest instances?

**Cross-domain insight (from ConceptEvolve — Information-Theoretic Distance Compression):** The entropy of the distance distribution H(D) measures how "spread out" the shortest-path distances are. For road networks, H(D) is low (distances cluster around a few values due to the geometric structure). An algorithm that adapts to H(D) could achieve O(m + n · H(D)) time, which is near-linear for low-entropy graphs.

**Why current approaches don't solve it:** Haeupler et al. [haeupler2024] showed Dijkstra is universally optimal among ordering-based algorithms, but their notion of optimality is for worst-case weights on a fixed graph. There is no analogous result for algorithms that adapt to the distance distribution.

**Potential angle of attack:** Design a priority queue whose extract-min cost depends on the local "entropy" of distances in the queue, not the total queue size. Combine with the Duan et al. recursive decomposition: use cheap Dijkstra when the distance distribution in a subproblem is low-entropy, and switch to BMSSP when it's high-entropy.

## Problem 5: Batch-Parallel SSSP with Sub-logarithmic Depth (ConceptEvolve-Inspired)

**Problem statement:** Can SSSP be solved in parallel with O(polylog n) depth and O(m + n) total work? Current parallel algorithms (Δ-stepping [meyersanders2003]) achieve good practical performance but have O(n) depth in the worst case. The theoretical parallel SSSP algorithms are work-inefficient.

**Cross-domain insight (from ConceptEvolve — Thermodynamic Relaxation Analogy):** In physics, many-body systems reach equilibrium via parallel relaxation: all particles simultaneously move toward lower energy. SSSP can be viewed as a relaxation process where all vertices simultaneously update their distances. The challenge is ensuring convergence without sequential bottlenecks.

**Why current approaches don't solve it:** The sequential bottleneck in SSSP is the longest shortest path (in terms of number of edges). Graphs with diameter D require at least D rounds of any relaxation-based algorithm. For general graphs, D can be Ω(n).

**Potential angle of attack:** Use the recursive decomposition of Duan et al. to reduce parallel depth. Each BMSSP subproblem has bounded distance range, which limits the parallel depth within each subproblem. If the recursion itself can be parallelized (processing independent subproblems concurrently), the total depth becomes O(recursion_depth × max_subproblem_depth).

## Problem 6: SSSP in the Comparison-Only Model

**Problem statement:** The comparison-addition model allows both comparisons and additions on edge weights. What if we restrict to comparisons only? This is relevant for ordinal data where edge "weights" are only comparable, not addable. Can SSSP be solved in o(mn) time with only comparisons?

**Why current approaches don't solve it:** All known efficient SSSP algorithms (Dijkstra, Duan et al.) fundamentally use addition to compute path lengths. Without addition, the algorithm cannot compute d(s,v) = d(s,u) + w(u,v). The best comparison-only algorithms are essentially Bellman-Ford variants with O(mn) time.

**Potential angle of attack:** For the special case where all edge weights are from a bounded set {w₁, ..., wₖ}, SSSP reduces to a multi-criteria shortest path problem. With k weight types, paths can be represented as k-dimensional vectors, and comparisons between paths become lexicographic. This connects to multi-objective optimization, where efficient algorithms exist for small k.

## Summary

| # | Problem | Current Gap | Approach | Feasibility |
|---|---|---|---|---|
| 1 | Practical constant factors | 3-4× slower than Dijkstra | Hybrid + engineering | High |
| 2 | Randomized vs. deterministic | log log n factor gap | Derandomization | Medium |
| 3 | Directed vs. undirected sparse | Additive √(mn log n log log n) | Structural exploitation | Medium |
| 4 | Adaptive algorithms | No instance-adaptive sub-Dijkstra | Entropy-based PQ | Medium-High |
| 5 | Parallel SSSP | No work-efficient polylog depth | Recursive parallelism | Low-Medium |
| 6 | Comparison-only model | O(mn) vs O(m + n log n) | Multi-criteria reduction | Low |
