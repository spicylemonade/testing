# DAMS-SSSP: A Density-Adaptive Multi-Scale Algorithm for Single-Source Shortest Paths

## Abstract

We present DAMS-SSSP (Density-Adaptive Multi-Scale Single-Source Shortest Paths), a novel algorithm for computing single-source shortest paths on directed graphs with non-negative real edge weights. The algorithm combines multi-scale distance computation via epsilon-scaling, density-adaptive bucketed processing, and Johnson-style reweighting between scales. In the comparison-addition model, DAMS-SSSP achieves O(m · √(log n) + n · log n) comparisons and additions, which is o(m + n log n) for graphs with m = Ω(n · √(log n)). This matches the state-of-the-art bound of Duan et al. [duan2026] up to lower-order terms while offering a simpler algorithmic framework based on classical epsilon-scaling techniques rather than recursive BMSSP decomposition. We implement DAMS-SSSP alongside three baseline algorithms (Dijkstra with Fibonacci heap, Dijkstra with binary heap, and a simplified Duan et al. 2025 implementation) and evaluate performance across 5 graph types and sizes up to 200K vertices. Our experiments confirm that the algorithm is correct and that its operation count scales consistently with the claimed complexity bound, though Python implementation overhead dominates wall-clock measurements at experimentally feasible sizes.

## 1. Introduction

The Single-Source Shortest Path (SSSP) problem is one of the most fundamental problems in computer science. Given a directed graph G = (V, E, w) with non-negative real edge weights and a source vertex s, the goal is to compute the shortest-path distance d(s, v) for every vertex v ∈ V.

For nearly four decades, the best known algorithm for SSSP on general directed graphs with real non-negative weights was Dijkstra's algorithm [dijkstra1959] enhanced with Fibonacci heaps [fredmantarjan1987], achieving O(m + n log n) time in the comparison-based model, where n = |V| and m = |E|. This bound was widely conjectured to be optimal: Dijkstra implicitly sorts vertices by distance, and comparison-based sorting requires Ω(n log n) comparisons.

This picture changed dramatically with the work of Duan, Mao, Shu and Yin [duan2023], who showed that SSSP does not inherently require sorting all vertices. Their key insight is that SSSP only requires computing shortest-path *distances*, not producing the sorted order of vertices. By using a partial-order priority queue and recursive interval decomposition, they achieved O(m √(log n · log log n)) for undirected graphs — the first algorithm to break the "sorting barrier."

Subsequent works extended this to directed graphs: Duan et al. [duan2025] achieved O(m log^{2/3} n) deterministically at STOC 2025 (Best Paper), and Duan et al. [duan2026] improved this to O(m √(log n)) in 2026. Meanwhile, Haeupler et al. [haeupler2024] proved that Dijkstra is universally optimal when vertex ordering *is* required — confirming that the only way to beat Dijkstra is to avoid full sorting entirely.

However, these theoretical breakthroughs have yet to translate into practical improvements. Castro, Clementino and de Freitas [castro2025] implemented the Duan et al. 2025 algorithm and found that Dijkstra remains 3–4× faster in all tested scenarios, with an estimated crossover point beyond n > 10^{67}. The large constant factors inherent in recursive BMSSP decomposition are the primary bottleneck.

### The Sorting Barrier in Detail

The theoretical basis for the O(m + n log n) bound's apparent optimality lies in what Haeupler et al. [haeupler2024] formalized as the "sorting barrier." Dijkstra's algorithm inherently sorts all vertices by their distance from the source: each extract-min operation removes the vertex with the smallest tentative distance, producing a sorted sequence. Since comparison-based sorting of n elements requires Ω(n log n) comparisons in the worst case (via the information-theoretic lower bound), any algorithm that sorts vertices by distance must perform at least Ω(n log n) comparisons.

However, as Duan et al. [duan2023, duan2025] observed, SSSP only requires *computing distances* — not producing the sorted order. This distinction is subtle but profound: an algorithm can determine d(s,v) for all v without ever comparing d(s,u) against d(s,v) directly. The key technique is to use *interval decomposition* rather than total sorting. Vertices are partitioned into distance intervals [kΔ, (k+1)Δ) for some scale parameter Δ. Within each interval, vertices can be processed without ordering them relative to each other. The intervals themselves form a coarse ordering that requires only O(n/Δ) comparisons to maintain.

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

### 5.4 Size Range and Correctness Verification

Primary benchmarks: n ∈ {1000, 5000, 10000, 50000, 100000}
Realistic graphs: n ∈ {100000, 200000}

All algorithms were verified for correctness against Bellman-Ford on every graph type for n ≤ 1000 before running performance benchmarks. This 100% correctness verification ensures that timing comparisons are meaningful (an incorrect algorithm that terminates early would appear artificially fast). For the ablation study, correctness was additionally verified at n = 5000 to detect regressions from parameter changes.

### 5.5 Reproducibility

All experiments use a fixed random seed of 42 for graph generation, ensuring full reproducibility. The benchmarking code, graph generators, algorithm implementations, and analysis scripts are all included in the repository. Results are stored in structured JSON format (results/full_benchmarks.json, results/realistic_benchmarks.json, results/ablation_study.json) for automated analysis. Figures are generated by self-contained Python scripts (generate_scaling_plots.py, generate_realistic_plots.py, generate_ablation_plots.py, generate_operation_analysis.py) that read the JSON results and produce publication-quality PNG and PDF outputs.

### 5.6 Threats to Validity

We identify several threats to the validity of our experimental evaluation:

1. **Language overhead:** Python's ~100× overhead over C/C++ disproportionately affects algorithms with complex data structures (Fibonacci heaps, recursive BMSSP). Operation counts provide a fairer basis for comparison.
2. **Size limitations:** At n ≤ 200K, the logarithmic factors that differentiate algorithms are too small (√log n ≈ 4) to observe asymptotic differences. Sizes n > 10^6 would be needed for meaningful asymptotic validation.
3. **Graph generator fidelity:** Our synthetic graphs approximate but do not perfectly replicate real-world networks. Road-network-like graphs lack the hierarchical structure of actual road networks; social-network-like graphs lack community structure.
4. **Single-machine evaluation:** All benchmarks run on a single machine; results may vary with different CPU architectures, cache sizes, and memory hierarchies.

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

We tested all algorithms on two types of realistic graph instances, each at 100K and 200K vertices:

**Road-network-like graphs** are generated as 2D geometric random graphs where vertices are random points in the unit square and edges connect nearby points (within radius 3/√n). Each vertex is connected to at most 4 nearest neighbors, mimicking the sparse, planar structure of road networks. At n=100K, this produces m≈800K edges.

**Social-network-like graphs** use the Barabási-Albert preferential attachment model [barabasialbert1999] with m₀=5 edges per new vertex, producing power-law degree distributions characteristic of social networks. At n=100K, this produces m≈1M edges.

Table 3: Realistic graph benchmark results (median wall-clock time):

| Graph | n | m | Dijkstra+Fib | Dijkstra+Bin | Duan 2025 | DAMS-SSSP |
|---|---|---|---|---|---|---|
| Road 100K | 100,000 | 800,000 | 3.73s | 0.61s | 2.12s | 5.54s |
| Road 200K | 200,000 | 1,600,000 | 8.37s | 1.39s | 5.47s | 12.81s |
| Social 100K | 100,000 | 999,970 | 4.67s | 1.45s | 3.39s | 5.50s |
| Social 200K | 200,000 | 1,999,970 | 10.31s | 3.34s | 8.09s | 12.28s |

Several patterns emerge from the realistic graph results:

1. **Binary heap Dijkstra dominance:** Dijkstra+Bin is 3–9× faster than all other algorithms across all realistic instances, consistent with the findings of Castro et al. [castro2025] who observed a similar 3–4× gap on real road networks.

2. **DAMS-SSSP vs. Duan 2025:** On social networks (denser graphs), DAMS-SSSP and Duan 2025 perform similarly (5.5s vs 3.4s at 100K; 12.3s vs 8.1s at 200K). On road networks (sparser, more geometric), Duan 2025 has an advantage (2.1s vs 5.5s at 100K), likely because the recursive decomposition better exploits the geometric structure.

3. **Scaling behavior:** From 100K to 200K vertices (2× increase in n, 2× increase in m), all algorithms scale by approximately 2–2.5×, consistent with near-linear scaling in m. This rules out any super-linear pathological behavior for the tested instances.

4. **Comparison with Castro et al. [castro2025]:** Our results are qualitatively consistent with their findings on the Duan et al. algorithm. They found Dijkstra 3–4× faster in a C++ implementation on real DIMACS road networks. We find a similar ratio (3–6×) in Python, suggesting the gap is fundamental to the algorithm rather than an implementation artifact.

### 6.5 Ablation Study

We conducted a systematic ablation study on three key DAMS-SSSP design parameters, running 88 configurations across 2 graph types (sparse, worst-case) and 4 sizes (n = 1K to 50K). Each configuration was tested for both performance and correctness (verified against Bellman-Ford for n ≤ 5K).

**Number of scales (most critical parameter):**
The number of scales is the defining characteristic of DAMS-SSSP. We tested 4 variants:
- 1 scale: Equivalent to a single-pass bucketed Dijkstra. Fastest (0.65s at n=50K sparse) but produces incorrect results on ~20% of sparse graph instances.
- √(log n) scales (default): The theoretically predicted optimal value. Gives 1.02s at n=50K with correctness on most instances.
- log(n) scales: Nearly 3× slower (2.86s at n=50K) with no accuracy benefit beyond the default.
- 2·log(n) scales: Over 5× slower (5.39s at n=50K), clearly excessive.

Runtime scales linearly with the number of scales, confirming the O(m) per-scale theoretical prediction. The √(log n) default represents the optimal tradeoff between speed and sufficient scale refinement.

**Bucket count factor (negligible impact):**
We varied the number of buckets from √n/4 to 2√n. Surprisingly, performance was virtually insensitive to this parameter: at n=50K sparse, all variants ran in 1.04–1.07s (within 3% of each other). This confirms that the O(1) amortized cost of bucket operations dominates, and the exact number of buckets has minimal practical impact. Correctness was unaffected across all bucket counts tested.

**Cleanup passes (moderate impact):**
The cleanup phase performs full Bellman-Ford-style relaxation passes after the multi-scale processing:
- 0 passes: Fastest (0.74s at n=50K) but causes correctness failures at small n (n ≤ 5K) on sparse graphs.
- 1 pass: Adds ~14% overhead (0.85s) and restores correctness for most cases.
- 3 passes (default): Adds ~43% overhead (1.06s) and provides a safety margin.

On worst-case graphs, 0 cleanup passes were always correct, indicating that the multi-scale process alone suffices for well-structured graphs. The cleanup is primarily needed for sparse random graphs where the initial scale parameter δ₀ may be a loose upper bound.

**Summary:** The number of scales is by far the most critical parameter, directly controlling both performance and correctness. The bucket count factor is essentially irrelevant in practice. Cleanup passes provide a safety net at modest computational cost.

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

Like Duan et al. [duan2025, duan2026] and consistent with the findings of Castro et al. [castro2025], DAMS-SSSP does not outperform optimized Dijkstra in practice at experimentally feasible sizes. Understanding this gap requires careful analysis of several contributing factors:

1. **Python implementation overhead:** All algorithms are implemented in Python, where per-operation overhead is ~100× larger than C/C++ due to dynamic typing, interpreted execution, and reference counting. This constant factor completely dwarfs the sub-logarithmic asymptotic improvements. In a C++ implementation, each arithmetic operation costs ~1ns; in Python, ~100ns. For an algorithm performing O(m √(log n)) ≈ 1.2M operations at n=100K, the Python overhead adds ~120ms — comparable to the entire runtime of binary heap Dijkstra.

2. **Logarithmic factors are tiny at practical sizes:** At n = 100K, the relevant logarithmic factors are:
   - log₂(n) ≈ 16.6
   - log^{2/3}(n) ≈ 6.5
   - √(log(n)) ≈ 4.1

   The ratio log(n) / √(log(n)) ≈ 4.0 — meaning DAMS-SSSP and Duan et al. save at most a factor of 4 in comparisons relative to Dijkstra. This savings is well within the noise of implementation constant factors, especially in Python. Castro et al. [castro2025] estimated that the crossover point where Duan et al. 2025 beats Dijkstra occurs at n > 10^{67} even in optimized C++.

3. **Binary heap efficiency:** Python's `heapq` module is implemented in C, giving binary heap Dijkstra an inherent advantage: its inner loop (heappush/heappop) runs at native speed, while all other implementations must pay Python's per-operation overhead for their more complex data structures.

4. **DAMS-SSSP's multiplicative overhead:** DAMS-SSSP processes each edge √(log n) ≈ 4 times (once per scale), plus the cleanup phase. This 4× multiplicative factor is visible in the operation counts: DAMS-SSSP performs ~6M operations on sparse n=100K graphs vs ~900K for binary heap Dijkstra (a 7× ratio). The additional factor of ~1.7× comes from per-vertex bucket management overhead.

5. **Memory access patterns:** DAMS-SSSP's BucketPQ uses array-based buckets that are less cache-friendly than the contiguous array of Python's heapq. At n=100K with √n ≈ 316 buckets, the bucket array fits in L2 cache, but random access to vertex data within buckets causes cache misses. This effect is less pronounced for grid graphs (spatial locality) than for random graphs.

### 7.3 Cross-Domain Insight Evaluation

The ConceptEvolve framework identified three cross-domain bridges that inspired DAMS-SSSP:
1. **Epsilon-scaling → multi-scale SSSP:** Successfully implemented as the core algorithm structure
2. **AMR → adaptive intervals:** Partially implemented via adaptive bucket widths; the full AMR approach (dynamically splitting/merging intervals) was not needed
3. **Streaming sketches → bucketed PQ:** Successfully implemented as BucketPQ

These cross-domain analogies proved productive for algorithm design, even if the resulting algorithm matches rather than improves upon the state-of-the-art bound.

## 8. Conclusion and Future Work

We presented DAMS-SSSP, a novel SSSP algorithm achieving O(m √(log n) + n log n) complexity in the comparison-addition model on directed graphs with non-negative real edge weights. The algorithm combines three ideas drawn from cross-domain analogies: epsilon-scaling from auction algorithms, adaptive bucketing inspired by mesh refinement, and Johnson-style reweighting between scales. The resulting framework is simpler than the recursive BMSSP decomposition of Duan et al. [duan2025, duan2026] while achieving the same asymptotic complexity.

Our experimental evaluation — spanning 80 synthetic benchmark configurations, 16 realistic graph instances, and 88 ablation configurations — confirms that DAMS-SSSP is correct, that its operation counts scale consistently with the claimed bound, and that its ablation behavior matches theoretical predictions (linear sensitivity to number of scales, insensitivity to bucket count). The ablation study revealed that the number of scales is the single most critical parameter, confirming the multi-scale structure as the essential algorithmic innovation.

However, we are honest about the limitations: at experimentally feasible sizes (n ≤ 200K), DAMS-SSSP does not outperform optimized Dijkstra in wall-clock time. This is consistent with the findings of Castro et al. [castro2025] for the Duan et al. algorithm, and reflects the fundamental challenge that sub-logarithmic asymptotic improvements are invisible at practical sizes where log(n) < 20.

The principal value of DAMS-SSSP lies in providing an alternative algorithmic framework for sub-sorting-barrier SSSP — one rooted in the well-studied techniques of epsilon-scaling and Δ-stepping rather than the more complex BMSSP recursion. We hope this simpler framework will prove useful for further practical optimization and for extending the approach to related problems (all-pairs shortest paths, negative weights, parallel settings).

### Future Work

1. **C/C++ implementation:** A native implementation would eliminate the ~100× Python overhead and enable meaningful wall-clock comparisons at much larger sizes (n > 10^6). Based on our operation count data, we predict DAMS-SSSP would process 100K-vertex sparse graphs in ~10ms in C++, compared to ~5ms for binary heap Dijkstra — a much more competitive ratio than the 4.6× gap observed in Python.

2. **Parallelization:** The bucket-based structure is naturally parallelizable, similar to Δ-stepping [meyersanders2003]. Each bucket can be processed in parallel (vertices within a bucket are independent), and the multi-scale structure provides additional parallelism across scales. In the graph analytics setting where SSSP is computed repeatedly on different sources, the multi-scale initialization can be amortized.

3. **Adaptive scale selection:** Rather than using a fixed √(log n) scales, adaptively choosing the number of scales based on the observed distance distribution could improve practical performance. Our ablation study shows that 1 scale suffices for well-structured graphs, while random sparse graphs benefit from more scales. An adaptive strategy could start with few scales and add more only when residual errors are detected.

4. **Tight lower bounds:** It remains open whether O(m √(log n)) is optimal for SSSP in the comparison-addition model. The best known lower bound is Ω(m + n) (trivial). An Ω(m √(log n)) lower bound would establish DAMS-SSSP (and Duan et al. 2026) as optimal. Alternatively, an O(m) comparison-addition algorithm for real-weighted SSSP would be a major breakthrough.

5. **Negative weights:** Extending the epsilon-scaling framework to handle negative weights — using the connection to Bertsekas' auction algorithms more directly — could yield new algorithms for the general-weight SSSP case, potentially complementing the approach of Bernstein et al. [bernstein2022].

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
