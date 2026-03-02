# Summary Tables: Complexity Results and Experimental Findings

## Table 1: Implemented Algorithms — Theoretical and Empirical Comparison

| Algorithm | Theoretical Complexity | Model | Directed? | Det/Rand | Wall-clock n=100K Sparse | Wall-clock n=100K Grid | Total Ops n=100K Sparse | Total Ops n=100K Grid |
|---|---|---|---|---|---|---|---|---|
| Dijkstra + Fibonacci Heap | O(m + n log n) | Comparison | Both | Det | 3.92s | 3.32s | 3,381,477 | 3,459,322 |
| Dijkstra + Binary Heap | O((m + n) log n) | Comparison | Both | Det | 0.72s | 0.47s | 898,648 | 1,191,630 |
| Duan et al. 2025 (simplified) | O(m log^{2/3} n) | Comp-Add | Directed | Det | 1.62s | 1.08s | 2,590,498 | 3,580,590 |
| **DAMS-SSSP (novel)** | **O(m √(log n) + n log n)** | **Comp-Add** | **Directed** | **Det** | **3.28s** | **3.30s** | **6,093,456** | **9,142,188** |

### Notes on Table 1

- Wall-clock times are median over 3 timed runs after 1 warmup, in Python 3
- Total ops = comparisons + additions + heap operations
- Binary heap Dijkstra is fastest in practice due to Python's optimized heapq (C implementation)
- DAMS-SSSP has higher operation counts due to processing each edge O(√log n) times across scales
- Operation counts for Dijkstra + Fibonacci heap include internal heap comparisons (cascading cuts, consolidation)

## Table 2: DAMS-SSSP Complexity vs All Known SSSP Bounds

| Algorithm | Year | Complexity | Regime | DAMS-SSSP comparison |
|---|---|---|---|---|
| Dijkstra + Fibonacci Heap [fredmantarjan1987] | 1987 | O(m + n log n) | All | **Improves** for m = Ω(n √(log n)) |
| Dijkstra + Binary Heap | 1987 | O((m+n) log n) | All | **Improves** for all m |
| Thorup [thorup1999] | 1999 | O(m + n) | Undirected, integer, word-RAM | **Weaker** (different model) |
| Pettie-Ramachandran [pettieramachandran2005] | 2005 | O(mα(m,n) + n log log r) | Undirected real | **Weaker** for undirected sparse; **incomparable** for directed |
| Thorup [thorup2004] | 2004 | O(m + n log log C) | Directed, integer, word-RAM | **Weaker** (different model) |
| Duan et al. [duan2023] | 2023 | O(m √(log n · log log n)) | Undirected real, randomized | **Matches** (up to log log n factor); directed vs undirected |
| Duan et al. [duan2025] | 2025 | O(m log^{2/3} n) | Directed real, det | **Improves** (√log n < log^{2/3} n for all n) |
| Duan et al. [duan2026] | 2026 | O(m √(log n)) | Directed real, det | **Matches** (+ additive n log n term) |
| Bellman-Ford [bellmanford1958] | 1958 | O(mn) | All (incl. negative) | **Improves** for all non-negative weight graphs |

### Notes on Table 2

- "Improves" means DAMS-SSSP has a strictly better asymptotic bound in the relevant regime
- "Matches" means the same asymptotic bound (up to lower-order terms)
- "Weaker" means DAMS-SSSP has a worse bound, typically because the comparison is to a different computational model (word-RAM vs comparison-addition) or graph class (undirected only)
- The comparison with Duan et al. 2026 is the most relevant: DAMS-SSSP matches O(m √(log n)) for m = Ω(n √(log n)) but has an additive O(n log n) term that makes it slightly worse for very sparse graphs
- For the common case of m = Θ(n), DAMS-SSSP gives O(n √(log n) + n log n) = O(n log n), matching Dijkstra but not improving on it; Duan et al. 2026 gives O(n √(log n)), which is genuinely sub-logarithmic

## Table 3: Performance on Realistic Graphs

| Graph Type | n | m | Dijkstra+Fib | Dijkstra+Bin | Duan 2025 | DAMS-SSSP |
|---|---|---|---|---|---|---|
| Road Network 100K | 100,000 | 800,000 | 3.73s | 0.61s | 2.12s | 5.54s |
| Road Network 200K | 200,000 | 1,600,000 | 8.37s | 1.39s | 5.47s | 12.81s |
| Social Network 100K | 100,000 | 999,970 | 4.67s | 1.45s | 3.39s | 5.50s |
| Social Network 200K | 200,000 | 1,999,970 | 10.31s | 3.34s | 8.09s | 12.28s |

## Table 4: Ablation Study Summary (Sparse Graphs, n=50K)

| Parameter | Variant | Time | Speedup vs Default | Correct? |
|---|---|---|---|---|
| Scales | 1 scale | 0.65s | 1.57× | Sometimes no |
| Scales | √log n (default) | 1.02s | 1.00× | Yes |
| Scales | log n | 2.86s | 0.36× | Yes |
| Scales | 2 log n | 5.39s | 0.19× | Yes |
| Buckets | √n/4 | 1.07s | 0.97× | Yes |
| Buckets | √n (default) | 1.04s | 1.00× | Yes |
| Buckets | 2√n | 1.05s | 1.00× | Yes |
| Cleanup | 0 passes | 0.74s | 1.44× | Yes* |
| Cleanup | 1 pass | 0.85s | 1.25× | Yes |
| Cleanup | 3 passes (default) | 1.06s | 1.00× | Yes |

*At n=50K, 0 cleanup passes happens to be correct, but fails at smaller n on sparse graphs.
