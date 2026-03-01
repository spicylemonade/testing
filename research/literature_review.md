# Literature Review: Single-Source Shortest Paths Algorithms

## 1. Classical Foundations

### 1.1 Dijkstra's Algorithm (1959)
**Authors:** Edsger W. Dijkstra
**Venue:** Numerische Mathematik, 1959
**Key Result:** O(n²) algorithm for SSSP with non-negative edge weights on graphs with n vertices.

Dijkstra's algorithm is the foundational algorithm for SSSP with non-negative weights. It maintains a set of vertices with finalized distances and greedily extracts the minimum-distance unfinalized vertex at each step. The original implementation uses O(n²) time due to linear scans for minimum extraction. The correctness relies on the invariant that when a vertex is extracted, its distance is finalized — this holds because all edge weights are non-negative.

### 1.2 Bellman-Ford Algorithm (1958)
**Authors:** Richard Bellman (1958), Lester Ford Jr., Edward Moore
**Venue:** Quarterly of Applied Mathematics
**Key Result:** O(nm) algorithm for SSSP with arbitrary (including negative) edge weights.

The Bellman-Ford algorithm handles negative weights by performing n-1 rounds of edge relaxation. It can also detect negative-weight cycles. While asymptotically slower than Dijkstra for non-negative weights, it remained the standard for general weights until recent breakthroughs.

## 2. The Fibonacci Heap Revolution

### 2.1 Fredman-Tarjan 1987: Fibonacci Heaps
**Authors:** Michael L. Fredman, Robert E. Tarjan
**Venue:** Journal of the ACM, 1987
**Key Result:** O(m + n log n) SSSP for non-negative weights using Fibonacci heaps.

The Fibonacci heap data structure supports:
- **Insert:** O(1) amortized
- **Find-min:** O(1)
- **Extract-min:** O(log n) amortized
- **Decrease-key:** O(1) amortized

When used with Dijkstra's algorithm, this yields O(m + n log n) total time: O(m) for decrease-key operations across all edges, and O(n log n) for extract-min operations across all vertices. This bound was optimal in the comparison-based model for nearly 40 years.

**Significance:** This result established the benchmark that all subsequent SSSP algorithms are compared against. For dense graphs (m = Θ(n²)), the bound is O(n²), matching the trivial lower bound. For sparse graphs (m = O(n)), the bound is O(n log n).

## 3. Linear-Time and Near-Linear SSSP for Special Cases

### 3.1 Thorup 1999: Linear-Time Undirected SSSP
**Authors:** Mikkel Thorup
**Venue:** JACM, 1999
**Key Result:** O(m) SSSP for undirected graphs with non-negative integer weights in the word RAM model.

Thorup achieved linear-time SSSP for undirected graphs by exploiting:
1. The word RAM model's ability to manipulate integers in constant time
2. A component hierarchy based on the minimum spanning tree
3. Visiting vertices in a specific order determined by the MST structure

This was the first result showing that SSSP can be solved faster than sorting on undirected graphs. The algorithm is inherently for undirected graphs because it relies on MST structure.

### 3.2 Thorup 2003/2004: Directed Integer-Weight SSSP
**Authors:** Mikkel Thorup
**Venue:** STOC 2003 / JCSS 2004
**Key Result:** O(m + n log log n) SSSP for directed graphs with non-negative integer weights, and O(m + n log log C) where C is the maximum edge weight.

Thorup designed integer priority queues with O(1) decrease-key and O(log log n) extract-min time. Combined with Dijkstra's algorithm, this gives O(m + n log log n) for integer weights. This exploits the word RAM model's ability to perform bitwise operations, giving faster priority queue operations when keys are integers.

### 3.3 Pettie-Ramachandran 2005: Comparison-Based Undirected SSSP
**Authors:** Seth Pettie, Vijaya Ramachandran
**Venue:** SIAM Journal on Computing, 2005
**Key Result:** O(m · α(m,n) + n) SSSP for undirected graphs with non-negative real weights in the comparison-addition model, where α is the inverse Ackermann function.

This result showed that undirected SSSP with real weights can be solved in nearly linear time in the comparison-addition model, using the hierarchy-based approach from their optimal MST algorithm. The bound is tantalizingly close to O(m) but the inverse Ackermann factor, while practically constant, represents a theoretical gap.

### 3.4 Hagerup 2000: Word RAM SSSP
**Authors:** Torben Hagerup
**Venue:** ICALP 2000
**Key Result:** Improved SSSP bounds on the word RAM for various weight ranges.

Hagerup developed improved priority queue implementations for the word RAM model, giving faster SSSP for graphs with bounded integer weights. This work bridges the gap between comparison-based and word RAM models.

## 4. Negative-Weight Breakthroughs (2022-2023)

### 4.1 Bernstein-Nanongkai-Wulff-Nilsen 2022: Near-Linear Negative-Weight SSSP
**Authors:** Aaron Bernstein, Danupon Nanongkai, Christian Wulff-Nilsen
**Venue:** FOCS 2022
**Key Result:** Randomized O(m log⁸(n) log W) algorithm for SSSP with negative integer weights (W = max absolute weight).

This was a major breakthrough, reducing negative-weight SSSP from the long-standing O(mn) Bellman-Ford bound to near-linear time. The key techniques include:
1. **Low-diameter decomposition** of the graph
2. **Price functions** (Johnson-style potentials) to eliminate negative weights locally
3. **Hop-limited shortest paths** computed via scaling
4. Recursive decomposition of the problem

**Significance:** This resolved a decades-old open problem about whether near-linear SSSP with negative weights is possible, albeit with large polylogarithmic factors.

### 4.2 Bringmann-Cassis-Fischer 2023: Faster Negative-Weight SSSP
**Authors:** Karl Bringmann, Alejandro Cassis, Nick Fischer
**Venue:** FOCS 2023
**Key Result:** Improved the BNW bound to O(m log²(n) log(nW)), significantly reducing the polylogarithmic overhead.

This follow-up refined the BNW approach with improved scaling techniques and tighter analysis of the low-diameter decomposition, bringing the complexity much closer to the near-linear ideal.

### 4.3 Chen-Kyng-Liu-Peng-Gutenberg-Sachdeva 2022: Almost-Linear Min-Cost Flow
**Authors:** Li Chen, Rasmus Kyng, Yang P. Liu, Richard Peng, Maximilian Probst Gutenberg, Sushant Sachdeva
**Venue:** FOCS 2022 (Best Paper Award)
**Key Result:** m^{1+o(1)} algorithm for maximum flow and minimum-cost flow.

While not directly an SSSP algorithm, this breakthrough is deeply connected because:
1. SSSP reduces to min-cost flow
2. The interior point method techniques developed here influenced subsequent SSSP work
3. The result showed that many fundamental graph optimization problems admit almost-linear time algorithms

## 5. The Sorting Barrier and Beyond-Worst-Case Analysis

### 5.1 Haeupler-Hladík-Rozhoň-Tarjan-Tětek 2024: Universal Optimality of Dijkstra
**Authors:** Bernhard Haeupler, Richard Hladík, Václav Rozhoň, Robert E. Tarjan, Jakub Tětek
**Venue:** FOCS 2024 (Best Paper Award)
**Key Result:** Dijkstra's algorithm is universally optimal when combined with a beyond-worst-case heap.

This paper proves that if an SSSP algorithm is required to output vertices in order of their distances from the source (i.e., to "sort by distance"), then Dijkstra's algorithm with their new heap data structure is universally optimal — meaning it is simultaneously near-optimal on every graph topology, not just in the worst case.

**Key Insight — The Sorting Barrier:** If SSSP requires sorting vertices by distance, then Ω(n log n) comparisons are necessary on sparse graphs (since SSSP generalizes sorting). Dijkstra inherently performs this sorting. The paper shows that breaking O(m + n log n) for SSSP requires an algorithm that does NOT sort vertices by distance — it must compute distances without determining their complete order.

This paper directly motivated the Duan et al. 2025 work by clarifying exactly what barrier must be overcome.

### 5.2 Duan-Mao-Shu-Yin 2023: Undirected Sorting Barrier Broken
**Authors:** Ran Duan, Jiayi Mao, Xinkai Shu, Longhui Yin
**Venue:** FOCS 2023
**Key Result:** Randomized O(m√(log n · log log n)) SSSP for undirected graphs with real non-negative weights.

This was the first result to break the O(n log n) sorting barrier for undirected SSSP, using a randomized approach that avoids sorting all vertices. The key idea was to use the structure of shortest-path trees and batch relaxation to process groups of vertices without fully ordering them.

### 5.3 Duan-Mao-Mao-Shu-Yin 2025: Directed Sorting Barrier Broken
**Authors:** Ran Duan, Jiayi Mao, Xiao Mao, Xinkai Shu, Longhui Yin
**Venue:** STOC 2025 (Best Paper Award)
**Key Result:** Deterministic O(m log^{2/3} n) SSSP for directed graphs with real non-negative edge weights in the comparison-addition model.

This is the current state-of-the-art result and the primary point of comparison for our research. Key aspects:

1. **Model:** Comparison-addition model (operations are comparisons and additions on real-valued edge weights and distances)
2. **Deterministic:** Unlike the undirected precursor, this algorithm is deterministic
3. **Key Insight:** Decouple distance computation from distance ordering using "interval pivots" and recursive subproblem decomposition
4. **Practical caveat:** The theoretical crossover point where this beats Dijkstra is estimated at n ≈ 10^{67}, making it purely a theoretical contribution

## 6. Additional Related Work

### 6.1 Johnson 1977: All-Pairs via Potentials
**Authors:** Donald B. Johnson
**Venue:** JACM, 1977
**Key Result:** O(nm + n² log n) all-pairs shortest paths using potential functions to reweight edges.

Johnson's algorithm introduced the technique of using potential functions (vertex prices) to transform negative-weight instances into non-negative ones. This technique is fundamental to the BNW 2022 approach.

### 6.2 Meyer 2001: Average-Case Linear SSSP
**Authors:** Ulrich Meyer
**Venue:** SODA 2001
**Key Result:** O(m) expected time SSSP for directed graphs with random edge weights.

This result shows that for random inputs, SSSP can be solved in linear time, motivating the study of beyond-worst-case complexity.

### 6.3 Cassis-Fischer-Haeupler 2025: Experimental Study
**Authors:** Alejandro Cassis, Nick Fischer, Bernhard Haeupler
**Venue:** SEA 2025
**Key Result:** Experimental evaluation of recent theoretical SSSP algorithms.

This experimental study compares the practical performance of recent theoretical SSSP algorithms against classical implementations, providing crucial empirical data on constant factors and crossover points.

## 7. Summary of Complexity Landscape

| Algorithm | Year | Weights | Directed? | Model | Complexity |
|-----------|------|---------|-----------|-------|-----------|
| Dijkstra + Fibonacci heap | 1987 | Non-negative | Yes | Comparison | O(m + n log n) |
| Thorup | 1999 | Non-neg integer | No | Word RAM | O(m) |
| Thorup | 2004 | Non-neg integer | Yes | Word RAM | O(m + n log log n) |
| Pettie-Ramachandran | 2005 | Non-negative | No | Comparison-addition | O(mα(m,n) + n) |
| BNW | 2022 | Integer (negative) | Yes | Word RAM | O(m log⁸(n) log W) |
| Chen et al. | 2022 | Integer | Yes | Word RAM | m^{1+o(1)} (min-cost flow) |
| Bringmann-Cassis-Fischer | 2023 | Integer (negative) | Yes | Word RAM | O(m log²(n) log(nW)) |
| Duan-Mao-Shu-Yin | 2023 | Non-negative | No | Comparison-addition | O(m√(log n log log n)) |
| Haeupler et al. | 2024 | Non-negative | Yes | Comparison | Universally optimal Dijkstra |
| **Duan et al.** | **2025** | **Non-negative** | **Yes** | **Comparison-addition** | **O(m log^{2/3} n)** |

## 8. Key Open Questions for Our Research

1. Can the log^{2/3} n factor in Duan et al. be further reduced?
2. Is O(m) achievable for directed SSSP in the comparison-addition model?
3. Can the techniques be made practical (reducing the constant factors)?
4. What is the relationship between comparison-addition complexity and word RAM complexity for SSSP?
5. Can randomization help for directed SSSP (Duan et al. 2025 is deterministic)?

## References

All citations reference entries in `sources.bib`.
