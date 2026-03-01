# Key Algorithmic Techniques for Sub-Dijkstra SSSP

This document analyzes the major algorithmic techniques across the SSSP literature that enable bounds better than Dijkstra's O(m + n log n).

---

## 1. Low-Diameter Decomposition (LDD)

### Formal Definition

Given a directed graph G = (V, E, w) and a parameter β > 0, a (β, d)-low-diameter decomposition partitions V into clusters C₁, C₂, ..., Cₖ such that:
1. **Low diameter:** For each cluster Cᵢ, the shortest-path diameter within the subgraph induced by Cᵢ is at most d.
2. **Few inter-cluster edges:** The expected number of edges (u,v) with u ∈ Cᵢ, v ∈ Cⱼ (i ≠ j) is at most β · m.

The tradeoff is parametric: smaller diameter d requires more inter-cluster edges (larger β), and vice versa.

### Usage in SSSP Literature

- **Bernstein-Nanongkai-Wulff-Nilsen 2022:** LDD is the core structural tool. The graph is decomposed into low-diameter clusters. Within each cluster, shortest paths can be computed efficiently because the diameter is bounded. Inter-cluster edges are handled by recursive calls. The decomposition has d = O(log²(n)/β), giving a total of O(log² n) recursive levels.
- **Bringmann-Cassis-Fischer 2023:** Improved the LDD parameters, reducing the decomposition to d = O(log(n)/β), which decreased the polylogarithmic overhead from log⁸ to log².

### Computational Cost

Computing an LDD typically costs O(m) time using BFS/DFS-based ball growing. The key cost parameter is the number of inter-cluster edges, which determines how much work is done in recursive calls.

**Complexity formula:** With (β, O(log(n)/β))-LDD and O(1/β) recursion levels, total cost is:
T(m, n) = O(m) + O(β · m) · T(m', n') ≈ O(m · polylog(n))

### Potential for Combination

LDD is primarily useful for negative-weight SSSP. For non-negative weights, Dijkstra already runs within each cluster efficiently. However, LDD could potentially be combined with batch relaxation to partition the graph into regions processed independently, reducing the global coordination overhead.

---

## 2. Price Functions / Potentials (Johnson Reweighting)

### Formal Definition

A price function (or potential function) is a mapping π: V → ℝ such that for every edge (u,v) with weight w(u,v):

w_π(u,v) = w(u,v) + π(u) - π(v) ≥ 0

If π satisfies this condition, the reweighted graph has non-negative edge weights, and shortest paths in the reweighted graph correspond to shortest paths in the original graph (with distances adjusted by d_π(s,t) = d(s,t) - π(s) + π(t)).

### Usage in SSSP Literature

- **Johnson 1977:** Introduced the technique for all-pairs shortest paths. Compute SSSP with Bellman-Ford to obtain distances d(s,·), then use π(v) = d(s,v) as potentials.
- **Bernstein-Nanongkai-Wulff-Nilsen 2022:** Use price functions locally within LDD clusters to eliminate negative weights. The innovation is maintaining approximate price functions that are "good enough" to make most edges non-negative.
- **Goldberg 2001:** Used price functions in the context of shortest path algorithms with reduced worst-case behavior.

### Computational Cost

Computing a valid price function requires solving SSSP with negative weights (bootstrapping problem). BNW 2022 solve this recursively: use LDD to decompose, compute prices within clusters, then adjust and recurse.

**Complexity formula:** Price function computation dominates the BNW algorithm's cost: O(m · log^O(1)(n) · log W).

### Potential for Combination

Price functions can transform any negative-weight SSSP into a non-negative-weight SSSP, making them composable with any non-negative SSSP algorithm. Combining efficient price function computation with Duan et al.'s sub-Dijkstra algorithm could yield improved negative-weight SSSP.

---

## 3. Hop-Limited Shortest Paths

### Formal Definition

The h-hop-limited shortest path from s to v, denoted d_h(s,v), is the minimum weight of any s-to-v path using at most h edges:

d_h(s,v) = min{w(P) : P is an s-v path with |P| ≤ h}

The standard shortest path distance is d(s,v) = d_n(s,v) = d_{n-1}(s,v).

### Usage in SSSP Literature

- **Bernstein-Nanongkai-Wulff-Nilsen 2022:** Hop-limited paths are central to the scaling framework. They compute d_h(s,v) for geometrically increasing h values and use these to build increasingly accurate price functions.
- **Duan et al. 2025:** The k-hop exploration in FindPivots computes paths of at most k hops from the frontier, where k = log^{1/3}(n). Vertices reachable within k hops are processed immediately; the rest are deferred.

### Computational Cost

Computing h-hop-limited shortest paths from a single source costs O(hm) using h rounds of Bellman-Ford-style relaxation, or O(m + nh) using BFS-like exploration on the hop-limited problem.

**Complexity formula:** In Duan et al., k-hop exploration costs O(k · |frontier|) per recursive call, totaling O(n · k · log(n)/t) = O(n · log^{2/3}(n)) across all levels.

### Potential for Combination

Hop-limited paths provide a natural "radius of exploration" parameter that can be tuned independently of the sorting/ordering problem. Combining hop-limited paths with different decomposition strategies could yield alternative tradeoffs.

---

## 4. Scaling (Weight Rounding and Successive Refinement)

### Formal Definition

Scaling gradually refines the precision of edge weights. Given integer weights in [0, W], the algorithm processes weights bit by bit from most significant to least significant. At scale i:
- Weights are rounded to i-bit precision: w_i(e) = ⌊w(e) / 2^{b-i}⌋
- The solution at scale i provides an approximate price function for scale i+1
- Each scale requires solving a "residual" SSSP problem with small weights (0 or 1 after reweighting)

### Usage in SSSP Literature

- **Gabow-Tarjan (classical):** Used scaling for minimum spanning tree and assignment problems.
- **Bernstein-Nanongkai-Wulff-Nilsen 2022:** Scaling across O(log W) weight bits, with hop-limited SSSP at each scale. Each scale introduces errors of magnitude O(1), which are corrected by the next scale.
- **Bringmann-Cassis-Fischer 2023:** Improved the scaling framework to reduce the number of effective scales.
- **Goldberg 1995:** Scaling for shortest paths in networks with integer costs.

### Computational Cost

Scaling introduces a multiplicative factor of O(log W) (for integer weights with maximum W) or O(log(nW)) in the total running time.

**Complexity formula:** BNW 2022 total cost: T(m,n) = O(log W) · O(m · polylog(n)) = O(m · polylog(n) · log W).

### Potential for Combination

Scaling is specific to integer weights and does not apply in the comparison-addition model. However, it could be combined with novel techniques for integer-weight SSSP to achieve bounds better than Thorup's O(m + n log log n).

---

## 5. Beyond-Worst-Case Heaps

### Formal Definition

A beyond-worst-case heap is a priority queue that provides performance guarantees parameterized by the actual input sequence, not just the worst case. Specifically, the Haeupler et al. 2024 heap has the **working-set property:**

The cost of extracting the minimum element x is O(log k) where k is the number of elements inserted into the heap AFTER x was inserted, rather than O(log n) where n is the total number of elements.

### Usage in SSSP Literature

- **Haeupler-Hladík-Rozhoň-Tarjan-Tětek 2024:** Designed a heap where extract-min costs O(log k) instead of O(log n). When combined with Dijkstra's algorithm, this gives a universally optimal SSSP algorithm: for any graph G, the running time is O(m + Σᵥ log kᵥ) where kᵥ is a graph-dependent parameter, and this is optimal for G.
- **Standard Fibonacci heaps:** Worst-case O(log n) extract-min, O(1) decrease-key. The Fibonacci heap does NOT have the working-set property.

### Computational Cost

**Complexity formula:**
- Fibonacci heap Dijkstra: O(m + n log n) worst case
- Beyond-worst-case heap Dijkstra: O(m + Σᵥ log kᵥ) where kᵥ ≤ n, so worst case is still O(m + n log n) but best case is O(m + n)

### Potential for Combination

Beyond-worst-case heaps provide instance-optimal Dijkstra but do not break the worst-case O(m + n log n) bound. They could be combined with batch relaxation: use the beyond-worst-case heap for vertices that must be processed individually, and batch relaxation for groups of vertices, achieving sub-O(m + n log n) worst case while retaining instance-optimality on easy inputs.

---

## 6. Batch Relaxation and Interval Pivots

### Formal Definition

**Batch relaxation:** Instead of relaxing edges one vertex at a time (as in Dijkstra), process a batch of vertices simultaneously. Given a set S of vertices with distances in a known interval [a, b), relax all outgoing edges from S in one batch operation.

**Interval pivots:** Partition the vertex set into groups based on shortest-path tree structure. A vertex u is a pivot if its subtree in the SPT contains at least k vertices. Vertices within k hops of the frontier are processed by batch relaxation; vertices beyond k hops are deferred to subproblems organized around pivots.

### Usage in SSSP Literature

- **Duan et al. 2025:** Batch relaxation via the BMSSP subroutine, combined with interval pivots, is the core technique achieving O(m log^{2/3} n). The BatchPrepend data structure operation amortizes the cost of inserting multiple elements.
- **Duan et al. 2023 (undirected):** Used a randomized variant of batch relaxation for undirected graphs, achieving O(m√(log n · log log n)).

### Computational Cost

**Complexity formula:** Batch relaxation with parameter k (hop limit) and t (recursion depth):
- Per edge: O(t) for data structure operations
- Per vertex: O(k) for pivot finding
- Total: O(mt + nk · log(n)/t)
- Optimized: k = log^{1/3}(n), t = log^{2/3}(n), giving O(m log^{2/3}(n))

### Potential for Combination

Batch relaxation is the most promising technique for our novel algorithm. Key observations:
1. The batch size k = log^{1/3}(n) in Duan et al. may not be optimal — different graph structures could benefit from adaptive batch sizes.
2. Combining batch relaxation with beyond-worst-case heaps could reduce the per-vertex overhead.
3. Using structural properties of the graph (e.g., separators, low treewidth) could enable larger batch sizes.

---

## 7. Multi-Level Bucketing

### Formal Definition

Multi-level bucketing organizes vertices into buckets based on distance ranges, with multiple levels of granularity. Level i has buckets of width Δᵢ, and vertices are promoted to finer-grained buckets as their distances are refined.

### Usage in SSSP Literature

- **Thorup 1999:** Uses a component hierarchy (derived from MST) as a multi-level bucketing scheme for undirected graphs with integer weights. The MST provides a natural hierarchy of distance scales.
- **Thorup 2004:** Uses multi-level bucketing with word-RAM operations for directed integer-weight SSSP.
- **Dial 1969:** Single-level bucketing (bucket sort) for SSSP with small integer weights, giving O(m + C) time.

### Computational Cost

**Complexity formula:** Thorup 1999: O(m) for undirected integer weights. Thorup 2004: O(m + n log log n) for directed integer weights. Dial: O(m + C) where C is max weight.

### Potential for Combination

Multi-level bucketing is most effective with integer weights (word RAM model). In the comparison-addition model, bucketing cannot be done exactly without comparisons. However, approximate bucketing — where vertices are placed in buckets based on known distance bounds — could reduce the number of comparisons needed.

---

## Summary: Technique Comparison Table

| Technique | Model | Weight Type | Key Cost | Used By | Combinability |
|-----------|-------|-------------|----------|---------|---------------|
| LDD | Any | Negative | O(m · polylog) | BNW 2022, BCF 2023 | High (with any SSSP) |
| Price Functions | Any | Negative→Non-neg | O(m · polylog) | Johnson 1977, BNW 2022 | High (preprocessing) |
| Hop-Limited Paths | Any | Any | O(hm) | BNW 2022, Duan 2025 | High (tunable parameter) |
| Scaling | Word RAM | Integer | O(log W factor) | BNW 2022, BCF 2023 | Integer-only |
| BWC Heaps | Comparison | Non-negative | O(Σ log kᵥ) | Haeupler 2024 | High (drop-in for Dijkstra) |
| Batch Relaxation | Comp-Add | Non-negative | O(m log^{2/3} n) | Duan 2025 | Core technique for our work |
| Multi-Level Buckets | Word RAM | Integer | O(m + n log log n) | Thorup 1999/2004 | Integer-only |
