# Problem Definition: Faster Shortest Path Algorithms

## 1. Problem Variants in Scope

### Primary Focus: Single-Source Shortest Path (SSSP)
Given a weighted graph G = (V, E, w) and a source vertex s, compute the shortest
path distance d(s, v) for all vertices v ∈ V. This is the core problem addressed
by Dijkstra's algorithm (non-negative weights) and Bellman-Ford (general weights).

### Secondary Focus: Point-to-Point Shortest Path (P2P)
Given a source s and target t, compute d(s, t) and the actual path. This variant
allows early termination and goal-directed search (e.g., A*, bidirectional search),
which are critical for practical applications like route planning.

### Tertiary (Exploratory): Static Preprocessing for Faster Queries
Preprocessing-based approaches (contraction hierarchies, hub labeling, transit nodes)
that invest O(f(n)) preprocessing time to answer subsequent queries in o(n + m) time.
These are important for understanding the space of possible speedups.

### Out of Scope
- **All-Pairs Shortest Path (APSP)**: O(n³) baseline; different algorithmic landscape.
- **Dynamic shortest paths**: Edge insertions/deletions during queries.
- **Negative-weight cycles**: Detection is a separate problem (Bellman-Ford detects but
  does not solve).
- **Distributed/parallel shortest path**: MapReduce, GPU — interesting but changes the
  computational model fundamentally.

## 2. Graph Types Considered

| Property | Variants | Notes |
|----------|----------|-------|
| **Direction** | Directed and undirected | Undirected = symmetric directed |
| **Weights** | Non-negative real (primary), general real (secondary) | Negative weights require Bellman-Ford |
| **Density** | Sparse (m = O(n)), medium (m = O(n log n)), dense (m = O(n²)) | Most real-world graphs are sparse |
| **Structure** | Random (Erdős-Rényi), grid/lattice, scale-free (Barabási-Albert), road networks, social networks | Different structures expose different algorithmic bottlenecks |
| **Dynamics** | Static only | Graph does not change during computation |
| **Size range** | 10 to 10⁷ nodes | Spanning toy examples to practical scale |

### Graph Families for Benchmarking
1. **Erdős-Rényi G(n, p)**: Random graphs at varying densities
2. **Grid graphs**: Regular 2D lattices (model spatial/mesh problems)
3. **Barabási-Albert**: Power-law degree distribution (model social/web networks)
4. **Complete graphs K_n**: Worst-case density scenarios
5. **Road networks**: Real-world sparse planar graphs (DIMACS challenge)
6. **Social networks**: Real-world heavy-tailed degree distributions (SNAP)

## 3. Target Computational Complexity Improvements

### Current State of the Art
| Algorithm | Time Complexity | Space | Notes |
|-----------|----------------|-------|-------|
| Dijkstra (binary heap) | O((n + m) log n) | O(n) | Standard baseline |
| Dijkstra (Fibonacci heap) | O(n log n + m) | O(n) | Optimal for dense graphs |
| Bellman-Ford | O(nm) | O(n) | Handles negative weights |
| A* (with good heuristic) | O((n + m) log n) worst-case | O(n) | Practical speedup, same worst-case |
| Bidirectional Dijkstra | O((n + m) log n) worst-case | O(n) | ~2x practical speedup |
| Contraction Hierarchies | O(n log n) preprocess, O(k log k) query | O(n + m) | k = nodes in search space |

### Target Improvements
Our research targets **practical speedup** rather than worst-case complexity improvements
(which are bounded by Ω(n + m) for SSSP). Specifically:

1. **2-5x practical speedup** over standard Dijkstra on sparse graphs by reducing
   the number of nodes expanded through adaptive search strategies.
2. **Reduced heap operations** by combining ideas from bidirectional search,
   landmark-based pruning, and hierarchical decomposition.
3. **Better cache locality** through graph reordering and bucket-based priority queues
   that reduce cache misses on large graphs.

### Theoretical Target
- Worst-case: O((n + m) log n) — no worse than Dijkstra
- Best-case on structured graphs: O(n + m) or O(n√(log n) + m) amortized
- Practical: ≥ 2x fewer node expansions than Dijkstra on road/social networks

## 4. Research Questions

### RQ1: Adaptive Priority Queue Selection
**Can an algorithm that dynamically switches between priority queue strategies
(bucket queues for small weight ranges, binary heaps for general cases) achieve
consistent speedup across diverse graph types?**

Motivation: Different priority queue implementations dominate on different graph
types. Bucket queues (Dial's algorithm) are O(n + m + C) where C is the max weight,
excellent for integer/small weights. Fibonacci heaps have better amortized bounds
for dense graphs. No single structure is universally best.

### RQ2: Bidirectional Search with Landmark Pruning
**Does combining bidirectional Dijkstra with landmark-based lower bounds (ALT
algorithm) yield superadditive speedup compared to either technique alone?**

Motivation: Bidirectional search reduces the search space by ~half. Landmark
pruning (A*-like bounds from precomputed landmark distances) prunes unpromising
directions. The combination may prune more aggressively than the sum of individual
effects due to tighter bounds from both directions.

### RQ3: Graph-Structure-Aware Preprocessing
**Can lightweight graph analysis (degree distribution, connected component structure,
vertex ordering) performed in O(n + m) time enable significant query speedup
without the heavy preprocessing of contraction hierarchies?**

Motivation: Full contraction hierarchies require expensive preprocessing. We
hypothesize that simple structural features (high-degree hub vertices, natural
graph partitions) can be detected cheaply and exploited for faster search.

### RQ4: Hybrid Algorithm Selection
**Can a meta-algorithm that selects the best shortest path strategy based on
graph properties (density, diameter estimate, degree distribution) outperform
any single algorithm across all graph types?**

Motivation: No single algorithm dominates all graph types. A classifier that
identifies graph structure and dispatches to the best strategy could achieve
robust speedup across diverse inputs.
