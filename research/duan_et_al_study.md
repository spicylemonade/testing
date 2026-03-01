# Deep Technical Study: Breaking the Sorting Barrier for Directed SSSP

## Duan, Mao, Mao, Shu, Yin — STOC 2025 (Best Paper Award)

**Full Title:** Breaking the Sorting Barrier for Directed Single-Source Shortest Paths
**Authors:** Ran Duan (Tsinghua), Jiayi Mao (Tsinghua), Xiao Mao (Stanford), Xinkai Shu (MPI Informatics), Longhui Yin (Tsinghua)
**Venue:** 57th ACM Symposium on Theory of Computing (STOC 2025), Prague
**arXiv:** 2504.17033

---

## 1. The Comparison-Addition Model

The comparison-addition model is the computational framework in which this result operates. It is defined as follows:

**Definition (Comparison-Addition Model).** An algorithm in the comparison-addition model may perform only two types of operations on edge weights and computed distances:
1. **Comparison:** Given two values a, b (which may be edge weights, computed distances, or sums of such), determine whether a < b, a = b, or a > b.
2. **Addition:** Given two values a, b, compute a + b.

Each comparison and each addition costs one unit of time. No other operations on edge weights are permitted — in particular, no hashing, no bitwise manipulation, no multiplication, and no rounding. This model captures the essential operations used by Dijkstra's algorithm and generalizes comparison-based sorting.

The comparison-addition model is strictly weaker than the word RAM model (which permits bitwise operations on integers and enables Thorup's O(m) undirected and O(m + n log log n) directed algorithms). It is the natural model for SSSP with real-valued weights, where integer tricks are inapplicable.

**Relation to prior work:**
- Fredman-Tarjan 1987 analyzed Fibonacci heap Dijkstra in this model, achieving O(m + n log n).
- Pettie-Ramachandran 2005 worked in this model for undirected graphs, achieving O(mα(m,n)).
- Thorup 1999/2004 require the word RAM model and integer weights.
- Haeupler et al. 2024 proved universal optimality of Dijkstra in the comparison model.

## 2. The Sorting Barrier

The "sorting barrier" refers to the O(m + n log n) complexity of Dijkstra's algorithm with Fibonacci heaps, and the widely held belief that this was optimal for SSSP in the comparison-addition model.

**Why the barrier seemed fundamental:**

Dijkstra's algorithm processes vertices in order of increasing distance from the source. On sparse graphs with m = O(n), this requires sorting n distance values, which requires Ω(n log n) comparisons in the comparison model. Since Dijkstra inherently produces a sorted ordering of vertices by distance, it performs at least n log n comparisons.

More formally, SSSP generalizes sorting: given n numbers a₁, ..., aₙ to sort, construct a path graph with edge weights a₁, a₂ - a₁, a₃ - a₂, ..., aₙ - aₙ₋₁. The SSSP distances are exactly the sorted prefix sums, and recovering the sorted order from distances is trivial. Therefore any SSSP algorithm that produces the ordered sequence of distances must use Ω(n log n) comparisons.

**The crucial observation (Haeupler et al. 2024):** Dijkstra's algorithm is optimal among algorithms that output vertices sorted by distance. However, the SSSP problem only asks for the distance values d(s,v) for each vertex v — it does NOT require that these values be produced in sorted order. This opens the door to algorithms that compute distances without fully sorting them.

**Why Dijkstra cannot break the barrier:** Dijkstra's correctness relies on processing vertices in distance order — each extract-min determines the next closest unfinalized vertex. This sequential dependence on the sorted order is inherent to the greedy approach. Any algorithm that processes vertices in a different order must find an alternative correctness argument.

## 3. Duan et al.'s Key Insight: Decoupling Distance Computation from Distance Ordering

The fundamental insight of Duan et al. 2025 is that shortest-path distances can be computed without determining the complete ordering of vertices by distance. Specifically, they decompose the SSSP problem into subproblems where:

1. Each subproblem involves vertices whose distances fall within a known interval [B'ᵢ, Bᵢ).
2. Within each subproblem, it suffices to compute distances without sorting them — the algorithm uses the structure of the shortest-path tree to propagate distances through "pivots" rather than through a global priority queue.

**Interval Pivots:** The algorithm partitions the vertex frontier into groups based on "interval pivots." A pivot is a vertex u whose shortest-path subtree T(u) contains at least k = ⌊log^{1/3} n⌋ vertices. The key observation is that after k relaxation steps from the current frontier, any vertex that hasn't been reached must have its shortest path passing through one of these pivots. This allows the algorithm to:
- Process vertices that are "close" (within k hops) directly via batch relaxation.
- Defer vertices that are "far" (more than k hops) to recursive subproblems organized around pivots.

This decomposition avoids the global sorting inherent in Dijkstra by replacing a single sorted processing order with a tree of localized processing steps.

## 4. Shortest-Path Tree Structure and Batch Relaxation

**Shortest-Path Tree Structure:** Let T be the shortest-path tree from source s. For a vertex u, define T(u) as the subtree rooted at u. The key structural property is: "the shortest path to v passes through u if and only if v is in the subtree T(u) rooted at u in the shortest-path tree."

The algorithm exploits this structure to identify which vertices depend on which frontier nodes without computing the distances in any particular order.

**Batch Relaxation (BMSSP Subroutine):** Instead of maintaining a single global priority queue and extracting minimums one at a time (as Dijkstra does), the BMSSP (Bounded-Many Single-Source Shortest Paths) subroutine processes edges in batches:

1. Edges are grouped by the distance interval of their source vertex.
2. All edges from vertices in the interval [B'ᵢ, Bᵢ) are relaxed simultaneously.
3. The BatchPrepend operation inserts multiple items into the data structure at once, amortizing the insertion cost.

The batch relaxation avoids the sequential dependence of Dijkstra: instead of extracting one minimum at a time (each requiring O(log n) comparisons), it processes groups of vertices whose distances are known to fall within an interval, reducing the number of comparison operations.

## 5. The Role of Auxiliary Data Structures

The algorithm uses a specialized block-based linked list data structure (Lemma 3.3 in the paper) that supports three operations:

1. **Insert(x):** Add a single element x to the data structure. Amortized cost: O(max{1, log(N/M)}) where N is the current size and M is the "pull batch size."

2. **BatchPrepend(L):** Insert a list L of elements, all of which are known to be smaller than any element currently in the data structure. Amortized cost: O(|L| · max{1, log(|L|/M)}).

3. **Pull(M):** Extract the M smallest elements from the data structure. Cost: O(M).

This data structure is crucial because:
- It allows batch insertions (avoiding the O(log n) per-element cost of Fibonacci heap decrease-key).
- The BatchPrepend operation exploits the fact that newly inserted elements have a known relationship to existing elements, reducing comparisons.
- The Pull operation extracts batches without maintaining a fully sorted order.

The data structure is maintained as two sequences: 𝒟₀ for batch prepends and 𝒟₁ for individual inserts, with blocks of O(N/M) size that enable efficient merging.

## 6. Why the Bound is O(m log^{2/3} n) Specifically

The O(m log^{2/3} n) bound arises from optimizing two competing parameters:

**Parameter k** (hop limit): The number of relaxation steps before checking for pivots. Set to k = ⌊log^{1/3} n⌋.

**Parameter t** (recursion parameter): Controls the subproblem size in the recursive decomposition. Set to t = ⌊log^{2/3} n⌋.

**Cost analysis:**

1. **FindPivots cost:** For each recursive call with vertex set Uₓ, finding pivots costs O(k · |Uₓ|). Across all recursion levels ((log n)/t levels) and all vertex sets, the total is:
   O(n · k · (log n)/t) = O(n · log^{1/3}(n) · log(n) / log^{2/3}(n)) = O(n · log^{2/3}(n))

2. **Edge relaxation cost:** Each edge relaxation costs O(log k + t) due to data structure operations. The total edge processing cost is:
   O(m · (log k + t)) = O(m · (log log^{1/3}(n) + log^{2/3}(n))) = O(m · log^{2/3}(n))

3. **Combined bound:** O(m · log^{2/3}(n) + n · log^{2/3}(n)) = O(m · log^{2/3}(n)) since m ≥ n - 1.

**Optimization principle:** The choice of k and t minimizes the maximum of the two cost terms. Setting k = log^{1/3} n balances the FindPivots cost (which grows with k) against the edge relaxation cost (which grows with t ≈ log(n)/k). The derivative condition ∂(k · t)/∂k = 0 subject to k · t ≈ log n yields the optimal split at k = log^{1/3} n, giving the exponent 2/3.

**Why 2/3 and not something else:** The exponent arises from a three-way tradeoff:
- The recursion depth is (log n)/t.
- The pivot-finding cost per level is O(k · n).
- The edge processing cost per edge is O(t).
- Minimizing max(nk · log(n)/t, mt) over k,t with the constraint k ≤ t yields k = log^{1/3}(n), t = log^{2/3}(n), and the total cost O(m log^{2/3} n).

## 7. The Gap Between Theory and Practice

The Duan et al. 2025 algorithm is a purely theoretical contribution with enormous constant factors that make it impractical for any conceivable real-world graph size.

**Why the crossover point is ~10^{67} vertices:**

The asymptotic advantage over Dijkstra is a factor of log^{1/3}(n). For this advantage to outweigh the constant-factor overhead, we need:

c₁ · m · log^{2/3}(n) < c₂ · (m + n · log n)

where c₁ >> c₂ due to the complexity of the recursive decomposition, batch data structures, and pivot finding. The constant c₁ includes:
- The overhead of maintaining the block-based linked list.
- The cost of FindPivots subroutine with its k-hop exploration.
- The recursive decomposition overhead with (log n)/t levels.
- Bookkeeping for managing multiple BMSSP instances.

Conservative estimates suggest c₁/c₂ ≈ 10^{20} or larger, which means the crossover occurs when log^{1/3}(n) ≈ 10^{20}, i.e., log(n) ≈ 10^{60}, giving n ≈ 2^{10^{60}} ≈ 10^{3·10^{59}}. Even the more optimistic estimates cited in the literature place the crossover at n ≈ 10^{67}.

**Comparison with practical SSSP:** For all practical purposes (graphs with billions of vertices or fewer), Dijkstra with a binary heap (not even Fibonacci heap) remains the fastest algorithm. The Duan et al. result is significant for what it proves about the computational complexity of SSSP, not for its practical utility.

**Experimental implementations:** GitHub implementations exist (danalec/DMMSY-SSSP in C, Rust, and Zig) but serve as pedagogical and verification tools, not practical alternatives to Dijkstra.

## 8. Summary of Key Technical Contributions

1. **Interval pivot decomposition:** A new technique for partitioning the SSSP problem into subproblems without requiring global sorting.
2. **Block-based linked list:** A data structure supporting efficient batch operations that avoids the per-element O(log n) cost of traditional priority queues.
3. **BMSSP subroutine:** A batch relaxation procedure that processes edges in groups, reducing comparison overhead.
4. **Optimal parameter balancing:** The careful choice of k = log^{1/3}(n) and t = log^{2/3}(n) achieves the optimal tradeoff between pivot-finding and edge-processing costs.
5. **Deterministic algorithm:** Unlike the prior undirected result (Duan et al. 2023), this directed algorithm is fully deterministic.

## 9. Implications for Our Research

The Duan et al. 2025 result establishes that:
1. Dijkstra's O(m + n log n) is NOT optimal for SSSP in the comparison-addition model.
2. The sorting barrier CAN be broken for directed graphs.
3. The current best bound is O(m log^{2/3} n), leaving a significant gap from O(m).

**Open directions we can explore:**
- Can the log^{2/3} factor be reduced further? The three-way tradeoff might not be tight.
- Can randomization help (the Duan et al. 2025 result is deterministic)?
- Can different decomposition strategies avoid the FindPivots overhead?
- Can we exploit graph structure (e.g., planarity, bounded treewidth) to improve the bound?
- Can the batch relaxation idea be generalized to achieve bounds closer to O(m · α(n)) or O(m · log* n)?
