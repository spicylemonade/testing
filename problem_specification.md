# Problem Specification: Single-Source Shortest Paths (SSSP)

## 1. Formal Definition of SSSP on Weighted Directed Graphs

**Input:** A weighted directed graph G = (V, E, w) where:
- V is a finite set of vertices with |V| = n
- E ⊆ V × V is a set of directed edges with |E| = m
- w : E → ℝ≥0 is a weight function assigning a non-negative real weight to each edge
- s ∈ V is a designated source vertex

**Output:** For each vertex v ∈ V, the shortest-path distance d(s, v) defined as:

d(s, v) = min { w(p) : p is a directed path from s to v in G }

where for a path p = (s = v₀, v₁, ..., vₖ = v):

w(p) = Σᵢ₌₀^{k-1} w(vᵢ, vᵢ₊₁)

If no directed path from s to v exists, d(s, v) = +∞.

**Remark on non-negative weights:** We restrict to w(e) ≥ 0 for all e ∈ E. This is the setting where Dijkstra's algorithm applies and where the sorting barrier is relevant. The negative-weight case is a related but distinct problem addressed by Bernstein et al. [bernstein2022] and Bringmann et al. [bringmann2023].

## 2. The Comparison-Addition Model

The **comparison-addition model** is the computational model used by all recent SSSP breakthroughs [duan2023, duan2025, duan2026, haeupler2024]. It is the natural model for real-weighted inputs.

### Definition

In the comparison-addition model, an algorithm operates on real-valued inputs (edge weights) through two primitive operations, each costing unit time:

1. **Comparison:** Given two values a, b ∈ ℝ, determine whether a < b, a = b, or a > b.
2. **Addition/Subtraction:** Given two values a, b ∈ ℝ, compute a + b or a - b.

All other computation (pointer manipulation, array indexing, control flow) is free. The complexity of an algorithm is measured by the total number of comparison and addition operations performed.

### Why This Model?

- **Generality:** The model makes no assumptions about the representation of edge weights. Weights can be irrational, transcendental, or symbolic — they just need to support comparison and addition.
- **Lower bounds:** Stronger lower bounds can be proven in this model than in the word-RAM model. Sorting n elements requires Ω(n log n) comparisons in this model.
- **Fair comparison:** All algorithms in the Duan et al. series [duan2023, duan2025, duan2026] and the Haeupler et al. result [haeupler2024] are analyzed in this model, making results directly comparable.

### Limitations

- The model does NOT allow hashing, bitwise operations, multiplication, or division on edge weights.
- It does NOT capture word-level parallelism available on real machines.
- Integer-specific speedups (Thorup's linear-time algorithm [thorup1999]) are NOT possible in this model.

## 3. The Word-RAM Model

The **word-RAM model** is the standard model for algorithm analysis on modern hardware.

### Definition

The word-RAM model operates on a random-access memory with the following characteristics:

- Memory consists of words of w bits each, where w ≥ log₂ n (the word size is at least large enough to address n memory locations).
- Each memory word can hold an integer in the range [0, 2^w - 1].
- Standard operations on words take O(1) time: arithmetic (+, -, ×, ÷), bitwise (AND, OR, XOR, NOT, shifts), comparison (<, =, >), and memory access (load, store).
- Edge weights are assumed to be integers bounded by C (where C fits in a constant number of words), or real numbers representable in O(1) words.

### SSSP Results in the Word-RAM Model

The word-RAM model allows stronger results due to bit-level parallelism:
- **Thorup (1999) [thorup1999]:** O(m + n) for undirected graphs with positive integer weights.
- **Thorup (2004) [thorup2004]:** O(m + n log log min{n, C}) for directed graphs with non-negative integer weights bounded by C.

These results do NOT transfer to the comparison-addition model because they exploit word-level operations (e.g., finding the most significant bit in O(1) time).

## 4. Table of All Known Complexity Bounds

### Non-Negative Weights (the setting of our research)

| Algorithm | Year | Complexity | Model | Dir/Undir | Det/Rand | Notes |
|---|---|---|---|---|---|---|
| Dijkstra + array PQ | 1959 | O(n²) | Comparison | Both | Det | Original |
| Dijkstra + binary heap | 1959/1975 | O((m+n) log n) | Comparison | Both | Det | Johnson 1975 |
| Dijkstra + Fibonacci heap | 1987 | O(m + n log n) | Comparison | Both | Det | Fredman-Tarjan |
| Dijkstra + relaxed heap | 1988 | O(m + n log n) | Comparison | Both | Det | Driscoll et al. |
| Thorup | 1999 | O(m + n) | Word-RAM | Undirected | Det | Integer weights |
| Thorup | 2004 | O(m + n log log C) | Word-RAM | Directed | Det | Integer weights ≤ C |
| Pettie-Ramachandran | 2005 | O(mα + min{n log n, n log log r}) | Comp-Add | Undirected | Det | r = weight ratio |
| Haeupler et al. | 2024 | Universally optimal (ordering) | Comparison | Both | Det | Beyond-worst-case heap |
| Duan-Mao-Shu-Yin | 2023 | O(m√(log n · log log n)) | Comp-Add | Undirected | Rand | First to break barrier |
| Duan-Mao-Mao-Shu-Yin | 2025 | O(m log^{2/3} n) | Comp-Add | Directed | Det | First directed sub-barrier |
| Duan-Mao-Shu-Yin | 2026 | O(m√log n + √(mn log n log log n)) | Comp-Add | Directed | Det | Current best |

### Negative Weights (for reference)

| Algorithm | Year | Complexity | Model | Notes |
|---|---|---|---|---|
| Bellman-Ford | 1958 | O(mn) | General | Handles negative cycles |
| Goldberg-Radzik | 1993 | O(mn) worst-case | General | Practically faster |
| Bernstein-Nanongkai-Wulff-Nilsen | 2022 | O(m log⁸n log W) | Rand | Near-linear, neg weights |
| Bringmann-Cassis-Fischer | 2023 | O(m log²n log(nW) log log n) | Rand | Improved neg weights |

### Lower Bounds

| Bound | Year | Model | Scope |
|---|---|---|---|
| Ω(m + n) | Trivial | All | Must read input |
| Ω(n log n) | Info-theoretic | Comparison | For sorting / vertex ordering |
| Ω(m + min{n log n, n log log r}) | Pettie-Ramachandran | Comp-Add | Hierarchy-based algorithms only |

## 5. Target: An Algorithm with o(m + n log n) on Directed Graphs with Non-Negative Real Weights

### Precise Statement

**Target:** Design and implement an algorithm A for SSSP with the following properties:

1. **Correctness:** For any directed graph G = (V, E, w) with non-negative real edge weights and source s, A outputs exact shortest-path distances d(s, v) for all v ∈ V.

2. **Asymptotic improvement:** The worst-case time complexity of A in the comparison-addition model is o(m + n log n). Specifically, we target one of:
   - O(m log^{2/3} n) — matching Duan et al. STOC 2025 [duan2025]
   - O(m √log n) — matching Duan et al. 2026 [duan2026]
   - A novel bound that improves on the above in specific density regimes

3. **Model:** The algorithm operates in the comparison-addition model. It may also be analyzed in the word-RAM model for practical performance.

4. **Novelty:** The algorithm introduces at least one genuinely new technique or provides a cleaner/simpler formulation of existing techniques that enables better practical performance or new theoretical insights.

### What "o(m + n log n)" Means

The small-o notation o(f(n)) means the algorithm's complexity is asymptotically strictly less than f(n):

lim_{n→∞} T(n) / (m + n log n) = 0

For the sparse case m = Θ(n), this means T(n) = o(n log n). The recent breakthroughs achieve:
- O(n log^{2/3} n) = o(n log n) ✓  [duan2025]
- O(n √(log n log log n)) = o(n log n) ✓  [duan2026]

For the dense case m = Θ(n²), the existing bound O(m + n log n) = O(n²) is already dominated by the m term. The recent results give O(n² log^{2/3} n), which is actually WORSE than O(n²). Thus the improvement is specifically for sparse to moderately dense graphs.

### Precise Density Threshold

Let m = n^{1+ε} for some ε > 0. Then:
- Dijkstra + FibHeap: O(n^{1+ε} + n log n) = O(n^{1+ε}) for ε > 0
- Duan et al. 2025: O(n^{1+ε} log^{2/3} n) — this is worse than Dijkstra for all ε > 0!

The improvement is only in the n log n term, which matters only when m = O(n log n / log^{2/3} n). For denser graphs, Dijkstra + FibHeap remains optimal.

More precisely, the crossover occurs at:
m + n log n = m log^{2/3} n
⟹ n log n = m(log^{2/3} n - 1) ≈ m log^{2/3} n
⟹ m ≈ n log^{1/3} n

So for m ≤ O(n log^{1/3} n), the Duan et al. 2025 algorithm is faster. For denser graphs, Dijkstra is better. Our algorithm should be aware of this density threshold.

### Computational Model Distinctions

| Feature | Comparison-Addition | Word-RAM |
|---|---|---|
| Primitive operations | compare, add, subtract | +, -, ×, ÷, bitwise, shifts |
| Weight representation | Abstract real numbers | Bounded integers or floats |
| Sorting lower bound | Ω(n log n) | O(n) possible (radix sort) |
| SSSP lower bound | Ω(m + n) | Ω(m + n) |
| Best SSSP (directed, non-neg) | O(m √log n) [duan2026] | O(m + n log log C) [thorup2004] |
| Our results apply in? | Yes (primary model) | Yes (for practical benchmarks) |
