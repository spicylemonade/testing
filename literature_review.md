# Literature Review: Shortest Path Algorithms

## Part I: Classical Algorithms (1956–1990)

### 1. Dijkstra's Algorithm (1959)
**Reference:** \cite{dijkstra1959}

Dijkstra's algorithm solves the single-source shortest path (SSSP) problem for graphs
with non-negative edge weights. It maintains a set of vertices whose shortest distance
from the source is known and repeatedly extracts the minimum-distance unvisited vertex.

- **Time complexity:** O(V² ) with array, O((V+E) log V) with binary heap, O(V log V + E) with Fibonacci heap
- **Space complexity:** O(V)
- **Limitations:** Requires non-negative edge weights
- **Key insight:** Greedy selection of the minimum-distance vertex is optimal because edge weights are non-negative

### 2. Bellman-Ford Algorithm (1958)
**Reference:** \cite{bellman1958}, \cite{ford1956}

Bellman-Ford solves SSSP with general (possibly negative) edge weights. It iteratively
relaxes all edges V-1 times. Can detect negative-weight cycles.

- **Time complexity:** O(VE)
- **Space complexity:** O(V)
- **Limitations:** Much slower than Dijkstra for non-negative weights
- **Key insight:** After k iterations, shortest paths using at most k edges are correct

### 3. Floyd-Warshall Algorithm (1962)
**Reference:** \cite{floyd1962}, \cite{warshall1962}

Floyd-Warshall solves the all-pairs shortest path (APSP) problem using dynamic programming.
For each intermediate vertex k, it checks whether going through k improves known paths.

- **Time complexity:** O(V³)
- **Space complexity:** O(V²)
- **Limitations:** Cubic complexity, impractical for large graphs
- **Key insight:** Optimal substructure of shortest paths through intermediate vertices

### 4. A* Search (1968)
**Reference:** \cite{hart1968}

A* is a best-first search algorithm that uses a heuristic function h(v) estimating
the distance from v to the target. With an admissible (non-overestimating) heuristic,
A* finds optimal paths while expanding fewer nodes than Dijkstra.

- **Time complexity:** O((V+E) log V) worst-case (same as Dijkstra), but practically much faster with good heuristics
- **Space complexity:** O(V) for open/closed lists
- **Limitations:** Requires an admissible heuristic; heuristic quality determines speedup
- **Key insight:** f(v) = g(v) + h(v) combines actual cost with estimated remaining cost

### 5. Bidirectional Search (1971)
**Reference:** \cite{pohl1971}

Bidirectional search runs two simultaneous searches: forward from source and backward
from target. The searches meet in the middle, reducing the search space roughly by half.

- **Time complexity:** O((V+E) log V) worst-case, ~O(V^{d/2}) practical for d-dimensional grids
- **Space complexity:** O(V)
- **Limitations:** Requires knowing the target; termination condition is subtle
- **Key insight:** Two small search spheres cover less volume than one large sphere

### 6. Fibonacci Heaps (1987)
**Reference:** \cite{fredman1987}

Fredman and Tarjan introduced Fibonacci heaps, a priority queue with O(1) amortized
insert/decrease-key and O(log n) extract-min. When used with Dijkstra's algorithm,
this yields the asymptotically optimal O(V log V + E) bound.

- **Time complexity for Dijkstra:** O(V log V + E)
- **Space complexity:** O(V)
- **Limitations:** High constant factors; binary heaps often faster in practice for sparse graphs
- **Key insight:** Lazy merging and cascading cuts enable amortized O(1) decrease-key

### 7. Dial's Algorithm / Bucket Queue (1969)
**Reference:** \cite{dial1969}

Dial's algorithm uses a bucket queue (array of buckets indexed by distance) for graphs
with integer weights. This avoids the logarithmic overhead of comparison-based heaps.

- **Time complexity:** O(V + E + C) where C is the maximum edge weight
- **Space complexity:** O(V + C)
- **Limitations:** Only for non-negative integer weights; space depends on weight range
- **Key insight:** When weight range is small, bucketing beats comparison-based sorting

### 8. Johnson's Algorithm (1977)
**Reference:** \cite{johnson1977}

Johnson's algorithm solves APSP efficiently for sparse graphs by reweighting edges
(using Bellman-Ford) to eliminate negative weights, then running Dijkstra from each vertex.

- **Time complexity:** O(V² log V + VE) with Fibonacci heaps
- **Space complexity:** O(V + E)
- **Limitations:** Requires Bellman-Ford preprocessing
- **Key insight:** Reweighting preserves shortest path structure while eliminating negative edges

## Complexity Summary Table

| Algorithm | Problem | Time | Space | Weight Req. |
|-----------|---------|------|-------|-------------|
| Dijkstra (binary heap) | SSSP | O((V+E) log V) | O(V) | Non-negative |
| Dijkstra (Fibonacci heap) | SSSP | O(V log V + E) | O(V) | Non-negative |
| Bellman-Ford | SSSP | O(VE) | O(V) | Any |
| Floyd-Warshall | APSP | O(V³) | O(V²) | Any |
| A* | P2P | O((V+E) log V) | O(V) | Non-negative + heuristic |
| Bidirectional Dijkstra | P2P | O((V+E) log V) | O(V) | Non-negative |
| Dial's (bucket queue) | SSSP | O(V+E+C) | O(V+C) | Non-neg integer |
| Johnson | APSP | O(V² log V + VE) | O(V+E) | Any |

## Cross-Domain Connections

### Connection to Information Theory
The shortest path problem has deep connections to coding theory and information-theoretic
bounds. The Viterbi algorithm for decoding convolutional codes is essentially a shortest
path algorithm on a trellis graph. This suggests that techniques from coding theory
(belief propagation, iterative decoding) might inspire new shortest path approaches.

### Connection to Computational Geometry
For geometric graphs (road networks, mesh graphs), Euclidean distance provides natural
admissible heuristics for A*. More sophisticated approaches use Voronoi diagrams or
well-separated pair decompositions to precompute distance oracles, bridging shortest
path algorithms with computational geometry data structures.
