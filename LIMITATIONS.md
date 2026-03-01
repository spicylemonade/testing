# Limitations, Failure Cases, and Future Research Directions

## 1. Scenarios Where BALT-H Does NOT Outperform Baselines

### 1.1 Complete Graphs (n ≤ 200)
On complete graphs, every vertex is directly connected to every other vertex with
uniform random weights. Dijkstra's algorithm terminates after examining O(V)
neighbors of the source, often finding the direct edge s→t immediately. BALT-H
adds preprocessing overhead (8 landmark + 8 hub Dijkstra runs on V-clique) but
cannot prune any vertices because landmark lower bounds are weak: all vertices are
roughly equidistant from landmarks. **Empirical result:** BALT-H is 0.3-0.8x
slower than Dijkstra P2P on complete graphs with n ≤ 200.

### 1.2 Very Small Graphs (n < 100)
For graphs with fewer than 100 nodes, preprocessing time dominates total cost.
BALT-H's preprocessing requires 16 Dijkstra runs (8 landmarks + 8 hubs), which
on a 50-node graph costs ~5ms — far exceeding the ~0.05ms cost of a single
Dijkstra P2P query. For single-query scenarios on small graphs, standard Dijkstra
is strictly faster. **Break-even**: BALT-H preprocessing amortizes over 100+
queries on graphs with n < 100.

### 1.3 Dense Erdős-Rényi Graphs (p > 0.1)
On dense ER graphs, the graph lacks structural hierarchy. Landmarks provide weak
lower bounds because all vertices have similar distances to landmarks (low variance
in the distance distribution). The hub identification also fails because degree
distribution is concentrated near the mean (np), so "hubs" are not meaningfully
different from other vertices. BALT-H reduces to approximately bidirectional
Dijkstra performance on these graphs, with the landmark computation overhead
making it 0.9-1.1x slower than bidirectional Dijkstra alone.

### 1.4 Pathological Hub Selection (Star Graphs)
On star graphs where a single center vertex has high degree but all shortest paths
between leaves go through the center anyway, hub precomputation is redundant —
Dijkstra would find the path in 2 steps regardless. The preprocessing overhead
provides no benefit in this degenerate case.

## 2. Theoretical Limitations

### 2.1 Worst-Case Complexity
BALT-H has the same worst-case time complexity as Dijkstra: O((V + E) log V).
The landmark pruning and hub upper bounds provide no guaranteed improvement —
they are heuristic speedups whose effectiveness depends on graph structure. This
contrasts with Contraction Hierarchies \cite{geisberger2008}, which provide
provably bounded query complexity (though at much higher preprocessing cost).

### 2.2 Preprocessing Space
BALT-H requires O((k_lm + k_hub) × V) space for distance tables. For a graph
with 1 million nodes and k=16 landmarks+hubs, this is ~128 million floating-point
values (~1 GB). This is comparable to ALT \cite{goldberg2005} but much larger
than Dijkstra (which needs O(V) space). Hub Labeling \cite{abraham2012} has
similar space requirements but achieves O(k) query time.

### 2.3 Non-Negative Weights Only
Like Dijkstra, BALT-H requires non-negative edge weights. The Dijkstra ordering
guarantee (monotonically non-decreasing extracted g-values) breaks with negative
weights. For graphs with negative weights, Bellman-Ford \cite{bellman1958} is
needed, and BALT-H's techniques do not apply.

### 2.4 Static Graphs Only
BALT-H's preprocessing assumes a static graph. If edges are added or removed,
all landmark and hub distances must be recomputed. This contrasts with
Customizable Route Planning \cite{delling2017}, which separates the graph
topology from edge weights, allowing efficient weight updates.

### 2.5 Pure Python Performance Ceiling
Our implementation is in pure Python, which limits absolute performance by
100-250x compared to C++ implementations. The relative speedup ratios
(BALT-H vs. Dijkstra) are meaningful, but absolute query times cannot compete
with production systems like OSRM or RoutingKit.

## 3. Comparison to Related Methods' Limitations

| Method | Preprocessing | Query | Dynamic Updates | Space | Our Advantage |
|--------|--------------|-------|-----------------|-------|---------------|
| Dijkstra \cite{dijkstra1959} | None | O((V+E)logV) | Trivial | O(V) | Faster query |
| ALT \cite{goldberg2005} | O(k·VlogV) | O((V+E)logV) | Recompute | O(kV) | Bidirectional + hubs |
| CH \cite{geisberger2008} | O(V·ElogV) | O(k·logk) | Full recompute | O(V+S) | Much lighter preprocessing |
| Hub Labeling \cite{abraham2012} | O(V²logV) | O(k) | Full recompute | O(kV) | Lighter preprocessing |
| CRP \cite{delling2017} | O(V·ElogV) | O(k·logk) | Metric update | O(V+S) | Simpler, no partitioning |

BALT-H's main advantage over CH and Hub Labeling is **lightweight preprocessing**
(seconds vs. minutes/hours). Its main disadvantage is **weaker query speedup**
(2-6x vs. 1000x+). This makes BALT-H suitable for scenarios where:
- Graphs change frequently (re-preprocessing is cheap)
- Preprocessing time budget is limited
- Moderate speedup (not microsecond queries) is sufficient
- Implementation simplicity is valued

## 4. Future Research Directions

### 4.1 Adaptive Landmark Selection During Query
Currently, active landmarks are selected once per query pair (s, t). A more
sophisticated approach would dynamically switch landmarks during the search as
the frontier moves, always using the landmarks most effective for the current
frontier position. This could provide stronger pruning without full landmark
evaluation.

### 4.2 Hierarchical Hub Decomposition
Instead of using flat high-degree vertex identification, construct a hierarchical
hub structure where vertices are ranked by their "importance" (centrality, betweenness)
across multiple levels. This would combine elements of Contraction Hierarchies
with our hub approach while maintaining lighter preprocessing.

### 4.3 Parallel Preprocessing
The 8 landmark and 8 hub Dijkstra runs are independent and can be parallelized
trivially. With 16 cores, preprocessing time would be reduced to a single Dijkstra
run. Additionally, GPU-parallel Dijkstra \cite{wang2021} could further accelerate
preprocessing.

### 4.4 Dynamic Graph Support
Extend BALT-H to support edge weight updates without full repreprocessing. When
a single edge weight changes, only landmarks and hubs whose shortest path trees
include that edge need updating. Lazy recomputation strategies from CRP
\cite{delling2017} could be adapted.

### 4.5 Learning-Based Landmark Selection
Replace the farthest-first heuristic with a learned landmark selection strategy
trained on query distributions. If certain source-target patterns are common
(e.g., suburban-to-downtown on road networks), landmarks can be placed to
maximize expected pruning for the actual query workload, following ideas from
neural algorithmic reasoning \cite{velickovic2021}.

### 4.6 Integration with Contraction Hierarchies
Use BALT-H as a "warm start" for CH preprocessing: the hub identification in
BALT-H could guide the vertex ordering in CH, potentially reducing CH preprocessing
time while maintaining its query performance.

### 4.7 Extension to Multi-Criteria Shortest Paths
Adapt BALT-H for multi-criteria optimization (e.g., minimize time and cost
simultaneously). Landmark bounds generalize to Pareto-optimal sets, and hub
shortcuts could prune dominated solutions early.
