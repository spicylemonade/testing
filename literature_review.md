# Literature Review: Single-Source Shortest Paths (SSSP)

## 1. Classical Foundations

### Dijkstra's Algorithm (1959) [dijkstra1959]
**Key contribution:** The original greedy algorithm for SSSP on graphs with non-negative edge weights. Processes vertices in order of increasing distance from the source, using a priority queue to determine the next vertex to settle.

**Model:** Comparison-based; applicable to all non-negative real-weighted graphs, both directed and undirected.

**Complexity:** O(n²) with an array-based priority queue. The runtime is dominated by priority queue operations: n extract-min and m decrease-key operations.

**Technique:** Greedy relaxation with a total ordering of vertices by distance. This total ordering requirement is the fundamental bottleneck that later works identify as the "sorting barrier."

### Bellman-Ford Algorithm (1958) [bellmanford1958]
**Key contribution:** SSSP algorithm that handles negative edge weights (unlike Dijkstra). Detects negative-weight cycles.

**Model:** General; works on any weighted directed graph.

**Complexity:** O(mn) — performs n-1 rounds of relaxing all m edges.

**Technique:** Iterative relaxation. Each round propagates shortest path information one hop further. Correctness follows from the fact that shortest paths have at most n-1 edges.

### Johnson's Algorithm (1977) [johnson1977]
**Key contribution:** All-pairs shortest paths using Bellman-Ford to compute vertex potentials, then Dijkstra with reweighted edges.

**Model:** General directed graphs with arbitrary weights.

**Complexity:** O(mn + n² log n) using Fibonacci heaps for Dijkstra.

**Technique:** The reduced cost function d_π(u,v) = w(u,v) + π(u) - π(v) transforms all edge weights to non-negative, enabling Dijkstra. This potential-based reweighting idea reappears in modern SSSP algorithms.

## 2. The Fibonacci Heap Era

### Fredman & Tarjan (1987) [fredmantarjan1987]
**Key contribution:** Invented the Fibonacci heap, a priority queue with O(1) amortized decrease-key and O(log n) amortized extract-min. Applied to Dijkstra's algorithm, this yields O(m + n log n) SSSP.

**Model:** Comparison-based; directed and undirected graphs with non-negative real weights.

**Complexity:** O(m + n log n) — the dominant bound for nearly 40 years.

**Technique:** Lazy heap with cascading cuts. The key insight: decrease-key need not restructure the entire heap. By allowing temporary violations of heap order (and cutting subtrees lazily), amortized O(1) decrease-key is achieved.

**Significance:** This bound remained the best known for general directed graphs with real non-negative weights until 2025.

### Driscoll, Gabow, Shrairman & Tarjan (1988) [driscoll1988]
**Key contribution:** Relaxed heaps — an alternative to Fibonacci heaps achieving the same amortized bounds but with O(1) worst-case decrease-key and O(log n) worst-case extract-min.

**Model:** Same as Fibonacci heaps.

**Complexity:** Same amortized bounds as Fibonacci heaps; better worst-case guarantees.

**Technique:** Allows heap-order violations in a controlled manner. Also enables processor-efficient parallel Dijkstra.

## 3. Integer and Word-RAM Improvements

### Thorup (1999) [thorup1999]
**Key contribution:** Linear-time SSSP for undirected graphs with positive integer weights in the word-RAM model.

**Model:** Word-RAM with integer weights; undirected graphs only.

**Complexity:** O(m + n) — optimal.

**Technique:** Hierarchical bucketing structure that avoids the sorting bottleneck. Builds on a minimum spanning tree decomposition: the MST defines a hierarchy of "components" at different weight scales, and shortest paths respect this hierarchy in undirected graphs. Uses atomic heaps (defined only for astronomically large n) and the RAM model's ability to manipulate word-sized integers in O(1) time.

**Limitations:** Only for undirected graphs (directed case requires different techniques). Only for integer weights. The use of atomic heaps makes the algorithm impractical.

### Thorup (2004) [thorup2004]
**Key contribution:** Integer priority queues with O(1) decrease-key on word-RAM, yielding faster SSSP for directed graphs with integer weights.

**Model:** Word-RAM; directed graphs with non-negative integer weights bounded by C.

**Complexity:** O(m + n log log min{n, C}).

**Technique:** Multi-level bucketing exploiting the word-RAM model's ability to perform bit-level operations in constant time.

## 4. The Comparison-Addition Model: Hierarchy-Based Approaches

### Pettie & Ramachandran (2005) [pettieramachandran2005]
**Key contribution:** Best known bound for undirected real-weighted SSSP before the Duan et al. breakthrough.

**Model:** Comparison-addition model; undirected graphs only.

**Complexity:** O(m α(m,n) + min{n log n, n log log r}) where α is the inverse-Ackermann function and r is the ratio of maximum to minimum edge weight.

**Technique:** Hierarchy-based approach extending Thorup's ideas to real weights. Constructs a "shortest path hierarchy" that decomposes the graph into components at different scales. Also proves a lower bound of Ω(m + min{n log n, n log log r}) for hierarchy-based algorithms, suggesting that fundamentally new ideas are needed to go further.

**Significance:** Established that hierarchy-based approaches have inherent limitations for undirected SSSP.

## 5. Negative-Weight Breakthroughs

### Bernstein, Nanongkai & Wulff-Nilsen (2022) [bernstein2022]
**Key contribution:** Near-linear time SSSP with negative edge weights — resolving a decades-old open problem.

**Model:** Randomized; directed graphs with integer weights (possibly negative).

**Complexity:** O(m log⁸(n) log W) where W bounds the absolute edge weight magnitudes.

**Technique:** Simple graph decomposition using low-diameter decompositions (LDD) combined with elementary combinatorial tools. Unlike prior approaches based on continuous optimization, this is purely combinatorial. Recursively decomposes the graph into components of bounded diameter, computes shortest paths within components, and stitches results together.

**Significance:** Best Paper at FOCS 2022. First combinatorial algorithm to break the classic Õ(m√n log W) bound (Gabow-Tarjan 1989).

### Bringmann, Cassis & Fischer (2023) [bringmann2023]
**Key contribution:** Improved negative-weight SSSP to O(m log²(n) log(nW) log log n) — nearly six log-factors better than Bernstein et al.

**Model:** Same as Bernstein et al.

**Complexity:** O(m log²(n) log(nW) log log n).

**Technique:** Combines efficient priority queue replacement with a negative-cycle detection algorithm reminiscent of noisy binary search (analyzed via drift analysis), plus improved Low-Diameter Decomposition construction.

## 6. Breaking the Sorting Barrier (2023–2026)

### Duan, Mao, Shu & Yin — FOCS 2023 [duan2023]
**Key contribution:** First algorithm to break the O(m + n log n) bound for real-weighted SSSP (on undirected graphs).

**Model:** Randomized; comparison-addition model; undirected graphs with non-negative real weights.

**Complexity:** O(m √(log n · log log n)).

**Technique:** The key insight is that the sorting barrier applies only when one needs the complete ordering of vertices by distance. SSSP only requires distances, not the sorted order. Their approach:
1. Sample a random subset R of vertices (each included with probability ~√(log n / n)).
2. Compute exact SSSP on the subgraph induced by R.
3. Use R-distances as "pivots" to partition remaining vertices into distance intervals.
4. Within each interval, use a simplified subroutine (no full sorting needed).
This "partial ordering" insight is the conceptual breakthrough that enables all subsequent results.

**Significance:** First result to beat Dijkstra+Fibonacci for sparse graphs on any graph class.

### Haeupler, Hladík, Rozhoň, Tarjan & Tětek — FOCS 2024 [haeupler2024]
**Key contribution:** Proved that Dijkstra's algorithm is universally optimal when vertex ordering IS required.

**Model:** Comparison-based; directed and undirected graphs.

**Complexity:** Instance-optimal: for any graph G, Dijkstra with their "beyond-worst-case" heap runs in O(n + m + cost of optimal algorithm for G).

**Technique:** Designed a new heap with a "working-set" property: extracting the minimum costs O(log k) where k is the number of elements inserted after it (not the total heap size). This means Dijkstra automatically adapts to easy instances.

**Significance:** Best Paper at FOCS 2024. Establishes that Dijkstra IS optimal when you must sort vertices — the only way to beat it is to avoid sorting entirely (as Duan et al. do).

### Duan, Mao, Mao, Shu & Yin — STOC 2025 [duan2025]
**Key contribution:** First deterministic algorithm to break the sorting barrier for directed SSSP.

**Model:** Deterministic; comparison-addition model; directed graphs with non-negative real weights.

**Complexity:** O(m log^{2/3} n).

**Technique:** Three key innovations:
1. **Recursive interval decomposition:** Partition vertices into distance intervals [L, L+Δ). Within each interval, vertices can be processed without full sorting.
2. **Partial-order priority queue:** A modified priority queue that maintains only a partial order on vertices, avoiding the Ω(n log n) sorting lower bound.
3. **BMSSP subroutine (Bounded Multiple-Source Shortest Path):** A subroutine that efficiently handles the recursive decomposition, processing multiple sources within a bounded distance range.
The algorithm recursively decomposes SSSP into smaller BMSSP instances using carefully chosen "pivot" distances.

**Significance:** Best Paper at STOC 2025. The first result showing Dijkstra is suboptimal even for directed graphs. Resolves a 40-year-old open question.

### Duan, Mao, Shu & Yin — 2026 [duan2026]
**Key contribution:** Improved the directed SSSP bound further, matching the undirected result.

**Model:** Deterministic; comparison-addition model; directed graphs with non-negative real weights.

**Complexity:** O(m√(log n) + √(mn log n log log n)), which is O(m√(log n)) for m ≥ n log log n and O(n√(log n log log n)) for sparse m = O(n).

**Technique:** Refined recursive decomposition with improved interval pivot selection and tighter analysis of the BMSSP subroutine. Achieves the same asymptotic bound for directed graphs as the earlier randomized bound for undirected graphs.

**Significance:** State-of-the-art as of 2026. Shows that the directed/undirected gap for SSSP can be closed.

## 7. Practical Algorithms and Experimental Analysis

### Meyer & Sanders — Δ-Stepping (1998/2003) [meyersanders2003]
**Key contribution:** A parallelizable SSSP algorithm that generalizes both Dijkstra and Bellman-Ford via a bucket-width parameter Δ.

**Model:** Practical/parallel; works on both RAM and distributed-memory machines.

**Complexity:** O(n + m + d·L) average case for random weights, where d is max degree and L is max shortest path weight. On random graphs: O(log³n / log log n) parallel time with linear work.

**Technique:** Maintains a bucket array indexed by ⌊d(v)/Δ⌋. Light edges (weight ≤ Δ) relaxed within a phase; heavy edges relaxed after settling. The Δ parameter trades off between Dijkstra-style (Δ→0) and Bellman-Ford-style (Δ→∞) behavior.

**Significance:** Reference implementation of Graph 500 benchmark. Highly practical for parallel shortest paths.

### Goldberg (2001) [goldberg2001]
**Key contribution:** Practical SSSP algorithms with O(V) average-case time for point-to-point shortest paths.

**Model:** Practical; various heuristic improvements.

**Technique:** Smart bucket structures, multi-level buckets, and A*-based heuristics for practical speedups.

### Castro, Clementino & de Freitas (2025) [castro2025]
**Key contribution:** First rigorous experimental analysis of the Duan et al. 2025 algorithm.

**Model:** Experimental; C++ implementation tested on sparse random graphs, grids, and US road networks up to 10M vertices.

**Key findings:**
- Dijkstra remains 3–4× faster than Duan et al. in all tested scenarios
- Estimated crossover point: n > 10^{67} for worst-case implementation
- Large constant factors are the main practical bottleneck
- The expected-time variant offers some practical improvement over worst-case

**Significance:** Establishes that theoretical breakthroughs in SSSP have not yet translated to practical improvements. The constant-factor gap is enormous.

## 8. Cross-Domain Connections

### Barabási-Albert Model (1999) [barabasialbert1999]
**Relevance:** Power-law/scale-free graph generation model. Many real-world networks follow power-law degree distributions, which affects SSSP performance. Algorithms that exploit structural properties (low treewidth, bounded highway dimension) can outperform worst-case bounds on these graphs.

### Goldberg-Radzik Algorithm (1993) [goldbergradzik1993]
**Relevance:** Practical negative-weight SSSP algorithm. Outperforms Bellman-Ford by processing vertices in topological order of SCCs. Recently shown to be competitive with even the theoretically faster Bringmann et al. algorithm on practical instances.

## Summary Table of Key Results

| Paper | Year | Directed? | Weights | Model | Complexity | Det/Rand |
|---|---|---|---|---|---|---|
| Dijkstra + FibHeap [fredmantarjan1987] | 1987 | Both | Non-neg real | Comparison | O(m + n log n) | Det |
| Thorup [thorup1999] | 1999 | Undirected | Pos integer | Word-RAM | O(m + n) | Det |
| Pettie-Ramachandran [pettieramachandran2005] | 2005 | Undirected | Non-neg real | Comp-Add | O(mα + min{n log n, n log log r}) | Det |
| Bernstein et al. [bernstein2022] | 2022 | Directed | Neg integer | — | O(m log⁸n log W) | Rand |
| Bringmann et al. [bringmann2023] | 2023 | Directed | Neg integer | — | O(m log²n log(nW) log log n) | Rand |
| Duan et al. [duan2023] | 2023 | Undirected | Non-neg real | Comp-Add | O(m√(log n log log n)) | Rand |
| Haeupler et al. [haeupler2024] | 2024 | Both | Non-neg real | Comparison | Universally optimal | Det |
| Duan et al. [duan2025] | 2025 | Directed | Non-neg real | Comp-Add | O(m log^{2/3} n) | Det |
| Duan et al. [duan2026] | 2026 | Directed | Non-neg real | Comp-Add | O(m√log n) | Det |
