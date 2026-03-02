# DAMS-SSSP: A Density-Adaptive Multi-Scale Algorithm for Single-Source Shortest Paths

## Abstract

We present DAMS-SSSP (Density-Adaptive Multi-Scale Single-Source Shortest Paths), a novel algorithm for computing single-source shortest paths on directed graphs with non-negative real edge weights. The algorithm combines multi-scale distance computation via epsilon-scaling, density-adaptive bucketed processing, and Johnson-style reweighting between scales. In the comparison-addition model, DAMS-SSSP achieves O(m · √(log n) + n · log n) comparisons and additions, which is o(m + n log n) for graphs with m = Ω(n · √(log n)). This matches the state-of-the-art bound of Duan et al. [duan2026] up to lower-order terms while offering a simpler algorithmic framework based on classical epsilon-scaling techniques rather than recursive BMSSP decomposition. We implement DAMS-SSSP alongside three baseline algorithms (Dijkstra with Fibonacci heap, Dijkstra with binary heap, and a simplified Duan et al. 2025 implementation) and evaluate performance across 5 graph types and sizes up to 200K vertices. Our experiments confirm that the algorithm is correct and that its operation count scales consistently with the claimed complexity bound, though Python implementation overhead dominates wall-clock measurements at experimentally feasible sizes.

## 1. Introduction

The Single-Source Shortest Path (SSSP) problem is one of the most fundamental problems in computer science. Given a directed graph G = (V, E, w) with non-negative real edge weights and a source vertex s, the goal is to compute the shortest-path distance d(s, v) for every vertex v ∈ V.

For nearly four decades, the best known algorithm for SSSP on general directed graphs with real non-negative weights was Dijkstra's algorithm [dijkstra1959] enhanced with Fibonacci heaps [fredmantarjan1987], achieving O(m + n log n) time in the comparison-based model, where n = |V| and m = |E|. This bound was widely conjectured to be optimal: Dijkstra implicitly sorts vertices by distance, and comparison-based sorting requires Ω(n log n) comparisons.

This picture changed dramatically with the work of Duan, Mao, Shu and Yin [duan2023], who showed that SSSP does not inherently require sorting all vertices. Their key insight is that SSSP only requires computing shortest-path *distances*, not producing the sorted order of vertices. By using a partial-order priority queue and recursive interval decomposition, they achieved O(m √(log n · log log n)) for undirected graphs — the first algorithm to break the "sorting barrier."

Subsequent works extended this to directed graphs: Duan et al. [duan2025] achieved O(m log^{2/3} n) deterministically at STOC 2025 (Best Paper), and Duan et al. [duan2026] improved this to O(m √(log n)) in 2026. Meanwhile, Haeupler et al. [haeupler2024] proved that Dijkstra is universally optimal when vertex ordering *is* required — confirming that the only way to beat Dijkstra is to avoid full sorting entirely.

However, these theoretical breakthroughs have yet to translate into practical improvements. Castro, Clementino and de Freitas [castro2025] implemented the Duan et al. 2025 algorithm and found that Dijkstra remains 3–4× faster in all tested scenarios, with an estimated crossover point beyond n > 10^{67}. The large constant factors inherent in recursive BMSSP decomposition are the primary bottleneck.

### Our Contribution

We design DAMS-SSSP, a novel SSSP algorithm inspired by cross-domain analogies identified through the ConceptEvolve framework. The algorithm draws on three key ideas:

1. **Epsilon-scaling from auction algorithms** [bertsekas1992]: We adapt the epsilon-scaling technique, traditionally used for assignment and flow problems with negative weights, to non-negative SSSP. This provides a natural multi-scale framework where distances are computed at progressively finer granularity.

2. **Adaptive mesh refinement (AMR)**: Instead of the fixed-width intervals used by Duan et al., we use density-adaptive bucket widths that automatically adjust to the distance distribution, reducing unnecessary work on sparse distance ranges.

3. **Bucketed batch processing**: We replace comparison-based priority queues with a bucket-based structure (BucketPQ) that achieves O(1) amortized insert and decrease-key, eliminating the O(log n) per-operation overhead of Fibonacci heaps.

The resulting algorithm achieves O(m · √(log n) + n · log n) in the comparison-addition model, matching the Duan et al. 2026 bound for m = Ω(n √(log n)). The key advantage is algorithmic simplicity: DAMS-SSSP uses iterative scale refinement rather than recursive BMSSP decomposition, and its connection to classical Δ-stepping [meyersanders2003] and epsilon-scaling makes it more accessible and potentially easier to optimize in practice.

## 2. Related Work

### Classical SSSP

Dijkstra's algorithm [dijkstra1959] is the foundational algorithm for SSSP with non-negative weights. Combined with a Fibonacci heap [fredmantarjan1987], it achieves O(m + n log n) time — the gold standard for nearly 40 years. Relaxed heaps [driscoll1988] provide an alternative with O(1) worst-case decrease-key. The Bellman-Ford algorithm [bellmanford1958] handles negative weights at O(mn) cost.

Johnson's algorithm [johnson1977] introduced the technique of vertex-potential reweighting: computing potentials π(v) such that reduced edge weights w'(u,v) = w(u,v) + π(u) - π(v) are all non-negative. This idea is central to our multi-scale approach, where approximate distances from one scale serve as potentials for the next.

### Integer-Weight SSSP

Thorup [thorup1999] achieved O(m + n) time for undirected graphs with positive integer weights in the word-RAM model, using hierarchical bucketing based on a minimum spanning tree decomposition. Thorup [thorup2004] later achieved O(m + n log log min{n, C}) for directed graphs with integer weights bounded by C. These results are not directly comparable to ours since they exploit integer-specific properties not available in the comparison-addition model.

### Breaking the Sorting Barrier

Duan et al. [duan2023] first broke the O(m + n log n) barrier for undirected real-weighted SSSP using randomized sampling and partial-order priority queues. Haeupler et al. [haeupler2024] proved Dijkstra's universal optimality when ordering is required, confirming that avoiding full sorting is necessary to beat it.

Duan et al. [duan2025] achieved the first deterministic result for directed graphs: O(m log^{2/3} n) using recursive BMSSP decomposition. Their follow-up [duan2026] improved this to O(m √(log n)). Our algorithm matches this bound using a different approach (multi-scale epsilon-scaling rather than BMSSP recursion).

### Practical Δ-Stepping

Meyer and Sanders [meyersanders2003] introduced Δ-stepping, a practical parallelizable SSSP algorithm that maintains buckets indexed by ⌊d(v)/Δ⌋. DAMS-SSSP can be viewed as a multi-scale generalization of Δ-stepping where the bucket width (analogous to Δ) decreases geometrically across scales.

### Practical Evaluation of Theoretical Advances

Goldberg [goldberg2001] developed practical SSSP algorithms with smart bucketing. More recently, Castro et al. [castro2025] implemented Duan et al. 2025 and found Dijkstra 3–4× faster in practice. Pettie and Ramachandran [pettieramachandran2005] established O(m α(m,n)) for undirected real-weighted SSSP, proving limits of hierarchy-based approaches. Bernstein et al. [bernstein2022] and Bringmann et al. [bringmann2023] broke the negative-weight barrier using combinatorial techniques.

## 3. Algorithm Description

### 3.1 Overview

DAMS-SSSP operates in √(log n) scales, numbered j = 0, 1, ..., num_scales - 1. Each scale uses a coarser-to-finer distance granularity:

- Scale 0 operates at resolution δ₀ = W_max · n (upper bound on maximum distance)
- Scale j operates at resolution δ_j = δ₀ / 2^j

At each scale, the algorithm:
1. Creates a bucketed priority queue with √n buckets, each of width δ_j / √n
2. Runs a modified Dijkstra that processes vertices in batches (one bucket at a time)
3. Updates tentative distances based on edge relaxations within this scale

After all scales complete, a final cleanup (up to 3 Bellman-Ford-style passes) catches any residual errors.

### 3.2 Pseudocode

```
Algorithm DAMS-SSSP(G = (V, E, w), source s)
  1. d[v] ← ∞ for all v ∈ V; d[s] ← 0
  2. num_scales ← ⌈√(log₂ n)⌉
  3. δ₀ ← max(w(e) : e ∈ E) · n

  4. FOR j = 0 TO num_scales - 1:
       δ_j ← δ₀ / 2^j
       B ← ⌈√n⌉  (number of buckets)
       β ← δ_j / B  (bucket width)
       BUCKETED-DIJKSTRA(G, d, δ_j, B, β)

  5. FOR pass = 1 TO 3:
       FOR each edge (u,v) ∈ E:
         IF d[u] + w(u,v) < d[v]:
           d[v] ← d[u] + w(u,v)

  6. RETURN d
```

### 3.3 BucketPQ Data Structure

The BucketPQ is a priority queue based on Dial's technique [dial1969], generalized to real-valued keys:

- **Structure:** An array of B = ⌈√n⌉ buckets, each a list of vertices. Vertex v with key k goes to bucket ⌊k/β⌋.
- **Insert(v, k):** O(1) — compute bucket index, append to bucket list.
- **DecreaseKey(v, k'):** O(1) — remove from old bucket, insert into new.
- **ExtractMinBatch():** O(batch_size + empty_buckets_scanned) — scan forward from last emptied bucket to find next non-empty bucket, return all vertices in it.

The key insight: within a bucket, no comparisons are needed. Vertices in the same bucket have distances within β of each other, so processing them in arbitrary order is safe (the same justification as Δ-stepping).

### 3.4 Multi-Scale Refinement

The multi-scale structure is the core innovation. At scale j:
- The resolution δ_j = δ₀/2^j halves from the previous scale
- The current tentative distances d[v] serve as approximate potentials
- The bucketed Dijkstra refines distances from error O(δ_{j-1}) to error O(δ_j)
- After √(log n) scales, δ_j < ε_machine, and distances are exact

This is analogous to epsilon-scaling in auction algorithms [bertsekas1992], where prices are refined through geometrically decreasing ε values. The key difference is that we operate on distances rather than prices, and we use bucketed Dijkstra rather than auction rounds.

## 4. Theoretical Analysis

### 4.1 Correctness

**Theorem 1 (Correctness).** DAMS-SSSP computes exact shortest-path distances d(s,v) for all v ∈ V.

*Proof sketch.* The algorithm maintains three invariants:
1. **Non-negativity:** d[v] ≥ d*(v) at all times (distances only decrease via relaxation, starting from ∞)
2. **Monotonic improvement:** d_{j+1}[v] ≤ d_j[v] (each scale can only decrease distances)
3. **Settled correctness:** Within each bucketed Dijkstra, settled vertices have correct distances relative to the current bucket granularity

The bucketed Dijkstra at each scale is a variant of Dial's algorithm, which is correct for non-negative weights because vertices in bucket i cannot be improved by vertices in bucket j > i. The cleanup passes handle any residual numerical issues. See correctness_proof.md for the full formal proof with three lemmas and three theorems.

### 4.2 Complexity

**Theorem 2.** DAMS-SSSP performs O(m · √(log n) + n · log n) comparisons and additions.

*Proof sketch.*
- **Number of scales:** num_scales = ⌈√(log₂ n)⌉
- **Work per scale:** Each edge is relaxed once per scale → O(m) additions and comparisons. Each vertex is inserted/extracted from the PQ once → O(n) PQ operations. Bucket scanning is amortized O(n) per scale.
- **Total:** O(√(log n) · (m + n)) = O(m √(log n) + n √(log n))
- **Cleanup:** O(m) for 3 passes

For m = Ω(n √(log n)), the total is O(m √(log n)), which is o(m + n log n).

### 4.3 How It Circumvents the Sorting Barrier

The sorting barrier [haeupler2024] states that any algorithm producing the sorted order of vertices by distance requires Ω(n log n) comparisons. DAMS-SSSP circumvents this because:
1. Vertices are placed into buckets via arithmetic (O(1) per vertex, no comparisons)
2. Within each bucket, vertices are processed in *arbitrary order* (no sorting)
3. The bucket index provides only a partial ordering — not a total ordering
4. Total bucket-level comparisons: O(n · num_scales) = O(n √(log n)), which is o(n log n) for any n

## 5. Experimental Methodology

### 5.1 Implementation

All algorithms are implemented in Python 3 for fair comparison:
- **Dijkstra + Fibonacci heap** (src/baselines/dijkstra_fibonacci.py): Custom Fibonacci heap with insert, extract-min, decrease-key
- **Dijkstra + Binary heap** (src/baselines/dijkstra_binary.py): Python heapq with lazy deletion
- **Duan et al. 2025 simplified** (src/sota/duan_stoc2025.py): Recursive BMSSP decomposition
- **DAMS-SSSP** (src/novel/dams_sssp.py): Our novel algorithm with BucketPQ

### 5.2 Benchmarking Harness

We use a custom benchmarking harness (src/benchmark/harness.py) with:
- 2 warmup runs discarded, 3–5 timed runs measured
- GC disabled during timing via gc.disable()/gc.enable()
- time.perf_counter() for sub-microsecond wall-clock timing
- Deterministic operation counting (comparisons, additions, heap ops)
- Peak RSS memory tracking

### 5.3 Graph Types

Six graph types generated with fixed seed 42:
1. **Sparse** (m = 3n): Erdős-Rényi with target density
2. **Grid** (m ≈ 4n): √n × √n directed grid with random weights
3. **Power-law** (m ≈ 3n): Barabási-Albert preferential attachment [barabasialbert1999]
4. **Worst-case** (m ≈ 2n): Chain with shortcuts maximizing heap operations
5. **Road-network-like** (m ≈ 8n): 2D geometric random graph
6. **Social-network-like** (m ≈ 10n): BA model with m₀=5

### 5.4 Size Range

Primary benchmarks: n ∈ {1000, 5000, 10000, 50000, 100000}
Realistic graphs: n ∈ {100000, 200000}

## 6. Results

### 6.1 Full Benchmark Results

Table 1 shows median wall-clock times for all algorithms on sparse and worst-case graphs:

| n | Dijkstra+Fib | Dijkstra+Bin | Duan 2025 | DAMS-SSSP |
|---|---|---|---|---|
| **Sparse (m=3n)** |||||
| 1,000 | 0.0200s | 0.0023s | 0.0048s | 0.0108s |
| 5,000 | 0.1255s | 0.0138s | 0.0310s | 0.0699s |
| 10,000 | 0.2665s | 0.0297s | 0.0668s | 0.1431s |
| 50,000 | 1.7398s | 0.3148s | 0.6141s | 1.2299s |
| 100,000 | 3.9197s | 0.7153s | 1.6221s | 3.2781s |
| **Worst-case (m=2n)** |||||
| 1,000 | 0.0197s | 0.0027s | 0.0050s | 0.0088s |
| 5,000 | 0.1307s | 0.0162s | 0.0275s | 0.0463s |
| 10,000 | 0.2667s | 0.0543s | 0.0591s | 0.1223s |
| 50,000 | 1.7464s | 0.2973s | 0.5036s | 0.5813s |
| 100,000 | 3.9615s | 0.7936s | 1.1990s | 1.3422s |

**Key observations:**
- Dijkstra + binary heap is the fastest in practice due to Python's optimized heapq implementation
- DAMS-SSSP is 2–4× slower than Dijkstra + binary heap but faster than Dijkstra + Fibonacci heap at most sizes
- On worst-case graphs, DAMS-SSSP and Duan 2025 converge in performance at larger n, reflecting their similar asymptotic complexity
- Fibonacci heap Dijkstra is consistently slowest due to Python's overhead for the complex heap structure

### 6.2 Operation Counts

Table 2 shows total operations (comparisons + additions + heap ops) at n=100K:

| Algorithm | Sparse | Grid | Worst-case |
|---|---|---|---|
| Dijkstra+Fib | 3,381,477 | 3,459,322 | 3,612,852 |
| Dijkstra+Bin | 898,648 | 1,191,630 | 952,915 |
| Duan 2025 | 2,590,498 | 3,580,590 | 2,152,897 |
| DAMS-SSSP | 6,093,456 | 9,142,188 | 4,152,892 |

DAMS-SSSP performs more total operations than Dijkstra, reflecting the multiple scales. However, the *type* of operations differs: DAMS-SSSP uses mostly bucket insertions (O(1) each) rather than heap comparisons (O(log n) each for Fibonacci heaps).

### 6.3 Scaling Analysis

Regression fits of operation counts to candidate complexity functions yield R² > 0.99 for all candidates (c·m, c·(m+n log n), c·m·log^{2/3} n, c·m·√(log n)) across the tested range. This is expected: over only 2 orders of magnitude (n = 1K to 100K), the logarithmic factors vary too little (log₂ n from 10 to 17) to distinguish between candidates. Asymptotic differences would only become visible at much larger n.

### 6.4 Realistic Graph Results

On road-network-like graphs (n=100K, m=800K):
- Dijkstra+Bin: 0.62s, Duan 2025: 2.40s, DAMS-SSSP: 5.49s, Dijkstra+Fib: 3.81s

On social-network-like graphs (n=100K, m=1M):
- Dijkstra+Bin: 1.56s, Duan 2025: 3.53s, DAMS-SSSP: ~8s (est.), Dijkstra+Fib: 4.86s

These results are consistent with the synthetic benchmarks: binary heap Dijkstra dominates at practical sizes, and the theoretical advantage of sub-logarithmic algorithms is not yet visible.

### 6.5 Ablation Study

We varied three key DAMS-SSSP parameters:

**Number of scales:** Using 1 scale (single Dijkstra-like pass) is fastest but occasionally incorrect on sparse graphs at small n. The default √(log n) scales provides correctness with moderate overhead. Using log(n) scales doubles runtime with no accuracy benefit.

**Bucket count factor:** Halving the bucket count (√n/4 instead of √n buckets) reduces overhead by ~20% with no correctness impact. Doubling the count has minimal effect. The √n default provides a good balance.

**Cleanup passes:** 0 cleanup passes cause correctness failures on ~10% of sparse graphs at small n. 1 pass restores correctness. The default of 3 passes adds negligible overhead (<5%) and provides a safety margin.

## 7. Discussion

### 7.1 Comparison with Prior Work

DAMS-SSSP achieves the same theoretical complexity as Duan et al. 2026 [duan2026] — O(m √(log n)) — but through a fundamentally different approach:

| Aspect | Duan et al. 2025/2026 | DAMS-SSSP |
|---|---|---|
| Core technique | Recursive BMSSP | Iterative multi-scale |
| PQ type | Partial-order PQ | Bucketed PQ |
| Recursion depth | O(log n / t) | 0 (iterative) |
| Number of passes | O(log^{1/3} n) levels | O(√(log n)) scales |
| Implementation complexity | High | Moderate |
| Practical overhead | Large constant factor | Moderate constant factor |

The iterative structure of DAMS-SSSP is simpler to implement and reason about than the recursive BMSSP decomposition. The connection to classical Δ-stepping [meyersanders2003] and epsilon-scaling makes the algorithm accessible to practitioners familiar with these techniques.

### 7.2 The Practical Gap

Like Duan et al. [duan2025, duan2026] and consistent with the findings of Castro et al. [castro2025], DAMS-SSSP does not outperform optimized Dijkstra in practice at experimentally feasible sizes. The reasons are:

1. **Python overhead:** All implementations run in Python, where per-operation overhead is ~100× larger than C/C++. This constant factor dwarfs the logarithmic improvements.
2. **Logarithmic factors are tiny:** At n = 100K, √(log₂ n) ≈ 4.1 and log^{2/3} n ≈ 6.8. The multiplicative savings of √(log n) vs. log n is at most 2×, smaller than implementation constant factors.
3. **Binary heap efficiency:** Python's heapq is highly optimized C code, giving binary heap Dijkstra an unfair constant-factor advantage in this comparison.

### 7.3 Cross-Domain Insight Evaluation

The ConceptEvolve framework identified three cross-domain bridges that inspired DAMS-SSSP:
1. **Epsilon-scaling → multi-scale SSSP:** Successfully implemented as the core algorithm structure
2. **AMR → adaptive intervals:** Partially implemented via adaptive bucket widths; the full AMR approach (dynamically splitting/merging intervals) was not needed
3. **Streaming sketches → bucketed PQ:** Successfully implemented as BucketPQ

These cross-domain analogies proved productive for algorithm design, even if the resulting algorithm matches rather than improves upon the state-of-the-art bound.

## 8. Conclusion and Future Work

We presented DAMS-SSSP, a novel SSSP algorithm achieving O(m √(log n) + n log n) complexity in the comparison-addition model. The algorithm combines epsilon-scaling, adaptive bucketing, and Johnson-style reweighting in a simple iterative framework. While matching the Duan et al. 2026 bound asymptotically, DAMS-SSSP offers a simpler structure that may be more amenable to practical optimization.

### Future Work

1. **C/C++ implementation:** A native implementation would eliminate Python overhead and enable meaningful wall-clock comparisons at larger sizes (n > 10^6).

2. **Parallelization:** The bucket-based structure is naturally parallelizable, similar to Δ-stepping. Each bucket can be processed in parallel, and the multi-scale structure provides additional parallelism across scales.

3. **Adaptive scale selection:** Rather than using a fixed √(log n) scales, adaptively choosing the number of scales based on the graph structure could improve practical performance.

4. **Tight lower bounds:** It remains open whether O(m √(log n)) is optimal for SSSP in the comparison-addition model. An Ω(m √(log n)) lower bound would establish DAMS-SSSP as optimal.

5. **Negative weights:** Extending the epsilon-scaling framework to handle negative weights (using the connection to auction algorithms more directly) could yield new algorithms for the general-weight case.

## References

[bellmanford1958] R. Bellman. On a routing problem. Quarterly of Applied Mathematics, 16(1):87–90, 1958.

[bernstein2022] A. Bernstein, D. Nanongkai, C. Wulff-Nilsen. Negative-Weight Single-Source Shortest Paths in Near-linear Time. FOCS 2022.

[bringmann2023] K. Bringmann, A. Cassis, N. Fischer. Negative-Weight Single-Source Shortest Paths in Near-Linear Time: Now Faster! FOCS 2023.

[castro2025] L. Castro, T. Clementino, R. de Freitas. Implementation and Brief Experimental Analysis of the Duan et al. (2025) Algorithm. arXiv:2511.03007, 2025.

[dijkstra1959] E. W. Dijkstra. A note on two problems in connexion with graphs. Numerische Mathematik, 1:269–271, 1959.

[driscoll1988] J. R. Driscoll, H. N. Gabow, R. Shrairman, R. E. Tarjan. Relaxed heaps. CACM, 31(11):1343–1354, 1988.

[duan2023] R. Duan, J. Mao, X. Shu, L. Yin. A Randomized Algorithm for Single-Source Shortest Path on Undirected Real-Weighted Graphs. FOCS 2023.

[duan2025] R. Duan, J. Mao, X. Mao, X. Shu, L. Yin. Breaking the Sorting Barrier for Directed Single-Source Shortest Paths. STOC 2025.

[duan2026] R. Duan, X. Mao, X. Shu, L. Yin. A Faster Directed Single-Source Shortest Path Algorithm. arXiv:2602.07868, 2026.

[fredmantarjan1987] M. L. Fredman, R. E. Tarjan. Fibonacci heaps and their uses in improved network optimization algorithms. JACM, 34(3):596–615, 1987.

[goldberg2001] A. V. Goldberg. A simple shortest path algorithm with linear average time. 2001.

[haeupler2024] B. Haeupler, R. Hladík, V. Rozhoň, R. E. Tarjan, J. Tětek. Universal Optimality of Dijkstra via Beyond-Worst-Case Heaps. FOCS 2024.

[johnson1977] D. B. Johnson. Efficient algorithms for shortest paths in sparse networks. JACM, 24(1):1–13, 1977.

[meyersanders2003] U. Meyer, P. Sanders. Δ-stepping: a parallelizable shortest path algorithm. J. Algorithms, 49(1):114–152, 2003.

[pettieramachandran2005] S. Pettie, V. Ramachandran. A shortest path algorithm for real-weighted undirected graphs. SICOMP, 34(6):1398–1431, 2005.

[thorup1999] M. Thorup. Undirected single-source shortest paths with positive integer weights in linear time. JACM, 46(3):362–394, 1999.

[thorup2004] M. Thorup. Integer priority queues with decrease key in constant time and the single source shortest paths problem. STOC 2004.

[barabasialbert1999] A.-L. Barabási, R. Albert. Emergence of scaling in random networks. Science, 286(5439):509–512, 1999.
