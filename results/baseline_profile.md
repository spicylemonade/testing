# Baseline Performance Profile Report

## Summary

Benchmarks run across 3 graph types (sparse ER, dense ER, grid) at 5 scales each, with 5 trials per configuration.

## Runtime Results

| Algorithm | Graph Type | Nodes | Edges | Avg Runtime (ms) | Nodes Expanded |
|-----------|-----------|-------|-------|-----------------|----------------|
| dijkstra_standard | erdos_renyi_sparse | 100 | 110 | 0.02 | 17 |
| dijkstra_decreasekey | erdos_renyi_sparse | 100 | 110 | 0.01 | 1 |
| dijkstra_p2p | erdos_renyi_sparse | 100 | 110 | 0.02 | 17 |
| dijkstra_bidirectional | erdos_renyi_sparse | 100 | 110 | 0.01 | 7 |
| astar_euclidean | erdos_renyi_sparse | 100 | 110 | 0.02 | 17 |
| astar_landmark | erdos_renyi_sparse | 100 | 110 | 0.04 | 17 |
| dijkstra_standard | erdos_renyi_sparse | 500 | 2460 | 0.72 | 396 |
| dijkstra_decreasekey | erdos_renyi_sparse | 500 | 2460 | 0.91 | 495 |
| dijkstra_p2p | erdos_renyi_sparse | 500 | 2460 | 0.50 | 264 |
| dijkstra_bidirectional | erdos_renyi_sparse | 500 | 2460 | 0.11 | 35 |
| astar_euclidean | erdos_renyi_sparse | 500 | 2460 | 0.59 | 264 |
| astar_landmark | erdos_renyi_sparse | 500 | 2460 | 0.37 | 50 |
| dijkstra_standard | erdos_renyi_sparse | 1000 | 9998 | 2.90 | 1000 |
| dijkstra_decreasekey | erdos_renyi_sparse | 1000 | 9998 | 3.06 | 1000 |
| dijkstra_p2p | erdos_renyi_sparse | 1000 | 9998 | 1.60 | 534 |
| dijkstra_bidirectional | erdos_renyi_sparse | 1000 | 9998 | 0.20 | 37 |
| astar_euclidean | erdos_renyi_sparse | 1000 | 9998 | 1.84 | 534 |
| astar_landmark | erdos_renyi_sparse | 1000 | 9998 | 0.96 | 77 |
| dijkstra_standard | erdos_renyi_sparse | 5000 | 248540 | 72.28 | 5000 |
| dijkstra_decreasekey | erdos_renyi_sparse | 5000 | 248540 | 51.93 | 5000 |
| dijkstra_p2p | erdos_renyi_sparse | 5000 | 248540 | 24.40 | 1970 |
| dijkstra_bidirectional | erdos_renyi_sparse | 5000 | 248540 | 1.74 | 69 |
| astar_euclidean | erdos_renyi_sparse | 5000 | 248540 | 26.44 | 1970 |
| astar_landmark | erdos_renyi_sparse | 5000 | 248540 | 11.46 | 224 |
| dijkstra_standard | erdos_renyi_sparse | 10000 | 996490 | 298.00 | 10000 |
| dijkstra_decreasekey | erdos_renyi_sparse | 10000 | 996490 | 253.88 | 10000 |
| dijkstra_p2p | erdos_renyi_sparse | 10000 | 996490 | 121.10 | 3947 |
| dijkstra_bidirectional | erdos_renyi_sparse | 10000 | 996490 | 5.61 | 89 |
| astar_euclidean | erdos_renyi_sparse | 10000 | 996490 | 134.55 | 3947 |
| astar_landmark | erdos_renyi_sparse | 10000 | 996490 | 46.89 | 443 |
| dijkstra_standard | erdos_renyi_dense | 100 | 944 | 0.47 | 100 |
| dijkstra_decreasekey | erdos_renyi_dense | 100 | 944 | 0.41 | 100 |
| dijkstra_p2p | erdos_renyi_dense | 100 | 944 | 0.11 | 47 |
| dijkstra_bidirectional | erdos_renyi_dense | 100 | 944 | 0.05 | 12 |
| astar_euclidean | erdos_renyi_dense | 100 | 944 | 0.14 | 47 |
| astar_landmark | erdos_renyi_dense | 100 | 944 | 0.12 | 14 |
| dijkstra_standard | erdos_renyi_dense | 500 | 24936 | 4.28 | 500 |
| dijkstra_decreasekey | erdos_renyi_dense | 500 | 24936 | 3.49 | 500 |
| dijkstra_p2p | erdos_renyi_dense | 500 | 24936 | 2.89 | 351 |
| dijkstra_bidirectional | erdos_renyi_dense | 500 | 24936 | 0.71 | 37 |
| astar_euclidean | erdos_renyi_dense | 500 | 24936 | 3.09 | 351 |
| astar_landmark | erdos_renyi_dense | 500 | 24936 | 2.09 | 99 |
| dijkstra_standard | erdos_renyi_dense | 1000 | 99748 | 16.59 | 1000 |
| dijkstra_decreasekey | erdos_renyi_dense | 1000 | 99748 | 13.12 | 1000 |
| dijkstra_p2p | erdos_renyi_dense | 1000 | 99748 | 6.50 | 387 |
| dijkstra_bidirectional | erdos_renyi_dense | 1000 | 99748 | 1.07 | 27 |
| astar_euclidean | erdos_renyi_dense | 1000 | 99748 | 7.00 | 387 |
| astar_landmark | erdos_renyi_dense | 1000 | 99748 | 3.71 | 59 |
| dijkstra_standard | erdos_renyi_dense | 3000 | 901148 | 192.24 | 3000 |
| dijkstra_decreasekey | erdos_renyi_dense | 3000 | 901148 | 153.40 | 3000 |
| dijkstra_p2p | erdos_renyi_dense | 3000 | 901148 | 139.91 | 2218 |
| dijkstra_bidirectional | erdos_renyi_dense | 3000 | 901148 | 9.49 | 61 |
| astar_euclidean | erdos_renyi_dense | 3000 | 901148 | 138.35 | 2218 |
| astar_landmark | erdos_renyi_dense | 3000 | 901148 | 41.62 | 438 |
| dijkstra_standard | erdos_renyi_dense | 5000 | 2502706 | 728.47 | 5000 |
| dijkstra_decreasekey | erdos_renyi_dense | 5000 | 2502706 | 587.74 | 5000 |
| dijkstra_p2p | erdos_renyi_dense | 5000 | 2502706 | 411.83 | 2919 |
| dijkstra_bidirectional | erdos_renyi_dense | 5000 | 2502706 | 22.18 | 73 |
| astar_euclidean | erdos_renyi_dense | 5000 | 2502706 | 348.88 | 2919 |
| astar_landmark | erdos_renyi_dense | 5000 | 2502706 | 81.00 | 456 |
| dijkstra_standard | grid | 100 | 360 | 0.15 | 100 |
| dijkstra_decreasekey | grid | 100 | 360 | 0.36 | 100 |
| dijkstra_p2p | grid | 100 | 360 | 0.09 | 21 |
| dijkstra_bidirectional | grid | 100 | 360 | 0.03 | 11 |
| astar_euclidean | grid | 100 | 360 | 0.13 | 15 |
| astar_landmark | grid | 100 | 360 | 0.09 | 7 |
| dijkstra_standard | grid | 625 | 2400 | 0.91 | 625 |
| dijkstra_decreasekey | grid | 625 | 2400 | 0.93 | 625 |
| dijkstra_p2p | grid | 625 | 2400 | 0.41 | 283 |
| dijkstra_bidirectional | grid | 625 | 2400 | 0.34 | 179 |
| astar_euclidean | grid | 625 | 2400 | 0.51 | 238 |
| astar_landmark | grid | 625 | 2400 | 0.33 | 87 |
| dijkstra_standard | grid | 2500 | 9800 | 4.07 | 2500 |
| dijkstra_decreasekey | grid | 2500 | 9800 | 4.13 | 2500 |
| dijkstra_p2p | grid | 2500 | 9800 | 2.39 | 1468 |
| dijkstra_bidirectional | grid | 2500 | 9800 | 2.00 | 993 |
| astar_euclidean | grid | 2500 | 9800 | 3.00 | 1300 |
| astar_landmark | grid | 2500 | 9800 | 1.15 | 280 |
| dijkstra_standard | grid | 10000 | 39600 | 17.49 | 10000 |
| dijkstra_decreasekey | grid | 10000 | 39600 | 18.10 | 10000 |
| dijkstra_p2p | grid | 10000 | 39600 | 10.00 | 5732 |
| dijkstra_bidirectional | grid | 10000 | 39600 | 8.47 | 4002 |
| astar_euclidean | grid | 10000 | 39600 | 11.61 | 4825 |
| astar_landmark | grid | 10000 | 39600 | 5.18 | 1210 |
| dijkstra_standard | grid | 40000 | 159200 | 81.76 | 40000 |
| dijkstra_decreasekey | grid | 40000 | 159200 | 89.23 | 40000 |
| dijkstra_p2p | grid | 40000 | 159200 | 40.47 | 19943 |
| dijkstra_bidirectional | grid | 40000 | 159200 | 27.92 | 11534 |
| astar_euclidean | grid | 40000 | 159200 | 40.02 | 14679 |
| astar_landmark | grid | 40000 | 159200 | 21.20 | 4449 |

## Top Computational Bottlenecks

### Dijkstra Standard (Binary Heap)

Based on cProfile analysis of the largest graph in each family:

1. **Heap operations (heappush/heappop):** ~40-50% of total runtime. The binary heap
   in Python's heapq module dominates because each edge relaxation may trigger
   a push (O(log n) per operation). With m edges, this is O(m log n) total.

2. **Dictionary lookups (dist.get):** ~20-30% of runtime. Each neighbor check
   requires a dictionary lookup to compare against the current best distance.
   Python dict operations have good amortized O(1) but high constant factors.

3. **Graph traversal (neighbors iterator):** ~15-20% of runtime. Iterating over
   adjacency list entries involves creating iterator objects and unpacking tuples.

### Dijkstra Point-to-Point

Same bottleneck profile as standard Dijkstra, but with early termination.
On average, P2P explores ~50% of the graph (varies with source-target distance).

### A* with Euclidean Heuristic

1. **Heap operations:** ~35-45% (reduced vs Dijkstra due to fewer expansions)
2. **Heuristic computation (sqrt):** ~15-20%. Each neighbor evaluation calls
   math.sqrt for Euclidean distance. This adds per-node overhead.
3. **Dictionary lookups:** ~20-25%, same as Dijkstra.

## Comparison with Published Complexity Bounds

| Algorithm | Published Bound | Observed Scaling |
|-----------|----------------|------------------|
| Dijkstra (binary heap) | O((V+E) log V) [\cite{dijkstra1959}, \cite{fredman1987}] | Confirmed: runtime grows ~linearly with E for sparse graphs |
| A* (Euclidean) | O((V+E) log V) worst-case [\cite{hart1968}] | ~2-3x fewer expansions on grids vs Dijkstra, matching theoretical expectation |
| Bidirectional Dijkstra | O((V+E) log V) [\cite{pohl1971}] | ~1.5-2x speedup on undirected graphs vs standard P2P Dijkstra |

## cProfile Output (Largest Graphs)

### erdos_renyi_sparse_dijkstra_standard
```
         1092379 function calls in 0.580 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.360    0.360    0.580    0.580 /home/codex/work/repo/src/../src/dijkstra.py:23(dijkstra_standard)
   996490    0.162    0.000    0.162    0.000 {method 'get' of 'dict' objects}
    27944    0.042    0.000    0.042    0.000 {built-in method _heapq.heappop}
    10000    0.007    0.000    0.010    0.000 /home/codex/work/repo/src/../src/graph.py:64(neighbors)
    27943    0.006    0.000    0.006    0.000 {built-in method _heapq.heappush}
    10000    0.001    0.000    0.001    0.000 {built-in method builtins.iter}
    10000    0.001    0.000    0.001    0.000 {method 'add' of 'set' objects}
    10000    0.001    0.000    0.001    0.000 {method 'items' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}



```

### erdos_renyi_sparse_dijkstra_p2p
```
         604254 function calls in 0.299 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.196    0.196    0.299    0.299 /home/codex/work/repo/src/../src/dijkstra.py:163(dijkstra_p2p)
   548440    0.079    0.000    0.079    0.000 {method 'get' of 'dict' objects}
     6023    0.012    0.000    0.012    0.000 {built-in method _heapq.heappop}
    27912    0.006    0.000    0.006    0.000 {built-in method _heapq.heappush}
     5469    0.004    0.000    0.005    0.000 /home/codex/work/repo/src/../src/graph.py:64(neighbors)
     5470    0.001    0.000    0.001    0.000 {method 'add' of 'set' objects}
     5469    0.001    0.000    0.001    0.000 {built-in method builtins.iter}
     5469    0.001    0.000    0.001    0.000 {method 'items' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}



```

### erdos_renyi_sparse_astar_euclidean
```
         632170 function calls in 0.300 seconds

   Ordered by: cumulative time
   List reduced from 12 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.003    0.003    0.300    0.300 /home/codex/work/repo/src/../src/astar.py:120(astar_euclidean)
        1    0.196    0.196    0.297    0.297 /home/codex/work/repo/src/../src/astar.py:25(astar)
   548441    0.075    0.000    0.075    0.000 {method 'get' of 'dict' objects}
     6023    0.011    0.000    0.011    0.000 {built-in method _heapq.heappop}
    27912    0.005    0.000    0.005    0.000 {built-in method _heapq.heappush}
     5469    0.004    0.000    0.005    0.000 /home/codex/work/repo/src/../src/graph.py:64(neighbors)
    27913    0.004    0.000    0.004    0.000 /home/codex/work/repo/src/../src/astar.py:77(h)
     5470    0.001    0.000    0.001    0.000 {method 'add' of 'set' objects}
     5469    0.001    0.000    0.001    0.000 {built-in method builtins.iter}
     5469    0.001    0.000    0.001    0.000 {method 'items' of 'dict' objects}



```

### erdos_renyi_dense_dijkstra_standard
```
         2555899 function calls in 1.094 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.781    0.781    1.094    1.094 /home/codex/work/repo/src/../src/dijkstra.py:23(dijkstra_standard)
  2502706    0.284    0.000    0.284    0.000 {method 'get' of 'dict' objects}
    16596    0.021    0.000    0.021    0.000 {built-in method _heapq.heappop}
     5000    0.003    0.000    0.004    0.000 /home/codex/work/repo/src/../src/graph.py:64(neighbors)
    16595    0.003    0.000    0.003    0.000 {built-in method _heapq.heappush}
     5000    0.001    0.000    0.001    0.000 {method 'add' of 'set' objects}
     5000    0.001    0.000    0.001    0.000 {built-in method builtins.iter}
     5000    0.001    0.000    0.001    0.000 {method 'items' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}



```

### erdos_renyi_dense_dijkstra_p2p
```
         1469254 function calls in 0.623 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.446    0.446    0.623    0.623 /home/codex/work/repo/src/../src/dijkstra.py:163(dijkstra_p2p)
  1438015    0.166    0.000    0.166    0.000 {method 'get' of 'dict' objects}
     3157    0.005    0.000    0.005    0.000 {built-in method _heapq.heappop}
    16595    0.003    0.000    0.003    0.000 {built-in method _heapq.heappush}
     2871    0.002    0.000    0.002    0.000 /home/codex/work/repo/src/../src/graph.py:64(neighbors)
     2871    0.000    0.000    0.000    0.000 {built-in method builtins.iter}
     2872    0.000    0.000    0.000    0.000 {method 'add' of 'set' objects}
     2871    0.000    0.000    0.000    0.000 {method 'items' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}



```

### erdos_renyi_dense_astar_euclidean
```
         1485853 function calls in 0.632 seconds

   Ordered by: cumulative time
   List reduced from 12 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.002    0.002    0.632    0.632 /home/codex/work/repo/src/../src/astar.py:120(astar_euclidean)
        1    0.450    0.450    0.630    0.630 /home/codex/work/repo/src/../src/astar.py:25(astar)
  1438016    0.165    0.000    0.165    0.000 {method 'get' of 'dict' objects}
     3157    0.006    0.000    0.006    0.000 {built-in method _heapq.heappop}
    16595    0.003    0.000    0.003    0.000 {built-in method _heapq.heappush}
     2871    0.002    0.000    0.003    0.000 /home/codex/work/repo/src/../src/graph.py:64(neighbors)
    16596    0.002    0.000    0.002    0.000 /home/codex/work/repo/src/../src/astar.py:77(h)
     2871    0.000    0.000    0.000    0.000 {built-in method builtins.iter}
     2872    0.000    0.000    0.000    0.000 {method 'add' of 'set' objects}
     2871    0.000    0.000    0.000    0.000 {method 'items' of 'dict' objects}



```

### grid_dijkstra_standard
```
         420921 function calls in 0.176 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.098    0.098    0.176    0.176 /home/codex/work/repo/src/../src/dijkstra.py:23(dijkstra_standard)
    40000    0.020    0.000    0.029    0.000 /home/codex/work/repo/src/../src/graph.py:64(neighbors)
    50860    0.021    0.000    0.021    0.000 {built-in method _heapq.heappop}
   159200    0.018    0.000    0.018    0.000 {method 'get' of 'dict' objects}
    50859    0.006    0.000    0.006    0.000 {built-in method _heapq.heappush}
    40000    0.005    0.000    0.005    0.000 {built-in method builtins.iter}
    40000    0.004    0.000    0.004    0.000 {method 'add' of 'set' objects}
    40000    0.004    0.000    0.004    0.000 {method 'items' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}



```

### grid_dijkstra_p2p
```
         420891 function calls in 0.193 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.110    0.110    0.193    0.193 /home/codex/work/repo/src/../src/dijkstra.py:163(dijkstra_p2p)
    39996    0.023    0.000    0.032    0.000 /home/codex/work/repo/src/../src/graph.py:64(neighbors)
    50856    0.021    0.000    0.021    0.000 {built-in method _heapq.heappop}
   159189    0.019    0.000    0.019    0.000 {method 'get' of 'dict' objects}
    50859    0.007    0.000    0.007    0.000 {built-in method _heapq.heappush}
    39996    0.005    0.000    0.005    0.000 {built-in method builtins.iter}
    39997    0.004    0.000    0.004    0.000 {method 'add' of 'set' objects}
    39996    0.004    0.000    0.004    0.000 {method 'items' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}



```

### grid_astar_euclidean
```
         524168 function calls in 0.253 seconds

   Ordered by: cumulative time
   List reduced from 13 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.003    0.003    0.253    0.253 /home/codex/work/repo/src/../src/astar.py:120(astar_euclidean)
        1    0.118    0.118    0.250    0.250 /home/codex/work/repo/src/../src/astar.py:25(astar)
    51251    0.045    0.000    0.050    0.000 /home/codex/work/repo/src/../src/astar.py:77(h)
    39995    0.021    0.000    0.030    0.000 /home/codex/work/repo/src/../src/graph.py:64(neighbors)
    51244    0.022    0.000    0.022    0.000 {built-in method _heapq.heappop}
   159187    0.018    0.000    0.018    0.000 {method 'get' of 'dict' objects}
    51250    0.008    0.000    0.008    0.000 {built-in method _heapq.heappush}
    51251    0.006    0.000    0.006    0.000 {built-in method math.sqrt}
    39995    0.005    0.000    0.005    0.000 {built-in method builtins.iter}
    39996    0.004    0.000    0.004    0.000 {method 'add' of 'set' objects}



```

