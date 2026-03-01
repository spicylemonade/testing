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

## Part II: Modern and State-of-the-Art Techniques (2005–2026)

### 9. ALT Algorithm — Landmarks + Triangle Inequality (2005)
**Reference:** \cite{goldberg2005}

The ALT algorithm (A*, Landmarks, Triangle inequality) precomputes shortest path
distances from all vertices to a small set of landmark vertices. During queries, these
distances provide tight lower bounds via the triangle inequality, dramatically
improving A* search efficiency.

- **Preprocessing:** O(k · (V + E log V)) for k landmarks (k Dijkstra runs)
- **Query:** O((V+E) log V) worst-case, but 10-20x faster than plain Dijkstra in practice
- **Space:** O(kV) for landmark distances
- **Key insight:** Triangle inequality on graph distances gives admissible heuristics

### 10. Contraction Hierarchies (2008)
**Reference:** \cite{geisberger2008}

Contraction Hierarchies (CH) preprocess a graph by iteratively contracting vertices
in order of "importance," adding shortcut edges to preserve shortest paths. Queries
use bidirectional Dijkstra on the augmented graph, only relaxing edges toward
more important vertices.

- **Preprocessing:** O(V log V) to O(V² ) depending on graph structure
- **Query:** O(k log k) where k is the search space size (typically O(√V) for road networks)
- **Space:** O(V + E + shortcuts)
- **Key insight:** Hierarchical vertex ordering enables pruning most of the search space

### 11. Hub Labeling (2012)
**Reference:** \cite{abraham2012}

Hub labeling assigns each vertex a set of "hub" vertices with precomputed distances.
A query d(s,t) is answered by finding the hub that minimizes dist(s,h) + dist(h,t).
Hierarchical hub labelings achieve the fastest known query times for road networks.

- **Preprocessing:** O(V · E) approximately
- **Query:** O(k) where k is the label size (typically O(√V · log V))
- **Space:** O(V · k)
- **Key insight:** For road networks with small highway dimension, label sizes are polylogarithmic

### 12. Transit Node Routing (2007)
**Reference:** \cite{bast2007}

Transit node routing identifies a small set of "transit nodes" (important junctions)
and precomputes all pairwise distances between them. For non-local queries, the
answer is found by looking up distances to/from the nearest transit nodes.

- **Preprocessing:** Heavy (hours for continental networks)
- **Query:** O(1) for non-local queries (table lookup)
- **Space:** O(T² + VT) where T is the number of transit nodes
- **Key insight:** For distant queries, paths go through a small set of important nodes

### 13. Customizable Route Planning (2011, 2017)
**Reference:** \cite{delling2011}, \cite{delling2017}

CRP separates preprocessing into metric-independent (graph partitioning) and
metric-dependent (customization) phases. This allows real-time updates when
the cost function changes (e.g., traffic conditions), with customization taking
less than a second for continental road networks. Used in Bing Maps.

- **Preprocessing:** Minutes (partitioning), <1 second (customization)
- **Query:** Milliseconds
- **Key insight:** Natural cuts in road networks enable robust partitioning

### 14. GPU-Parallel Shortest Paths (2015, 2021)
**Reference:** \cite{ortega2015}, \cite{wang2021}

GPU-based approaches exploit massive parallelism for shortest path computation.
Delta-stepping provides a tunable trade-off between Dijkstra's work efficiency
and Bellman-Ford's parallelism. The ADDS algorithm (Wang et al. 2021) achieves
34x speedup over serial Dijkstra.

- **Speedups:** 2-34x depending on graph type and algorithm
- **Challenge:** Dijkstra's sequential nature (priority queue) limits GPU parallelism
- **Key insight:** Coarse-grained bucketing enables parallel edge relaxation

### 15. Neural Algorithmic Reasoning (2021, 2022)
**Reference:** \cite{velickovic2021}, \cite{abboud2022}, \cite{li2020}

Neural algorithmic reasoning trains GNNs to execute classical algorithms.
Shortest-path GNNs learn to approximate Bellman-Ford-like message passing.
Distance encoding uses shortest-path features to improve GNN expressiveness.

- **Approach:** Train GNNs to mimic algorithmic steps
- **Advantage:** Can generalize across graph sizes; enables soft/differentiable pathfinding
- **Limitation:** Approximate; no optimality guarantees; training overhead
- **Key insight:** Graph attention over shortest-path neighborhoods enables long-range communication

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
