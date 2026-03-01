# Bottleneck Analysis and Improvement Opportunities

## 1. Dominant Operations in Baseline Algorithms

Based on our cProfile analysis of Dijkstra and A* across sparse, dense, and grid graphs
(see results/baseline_profile.md), the following operations dominate runtime:

### 1.1 Heap Operations (40-50% of runtime)
**heapq.heappush and heapq.heappop** consume the largest fraction of total runtime.
In standard Dijkstra with binary heap, each edge relaxation potentially pushes a new
entry, leading to O(m) pushes and O(n) pops, each costing O(log n).  Total heap work:
O(m log n).

**Key observation:** On sparse graphs (m = O(n)), heap operations are O(n log n),
which is near-optimal.  On dense graphs (m = O(n²)), heap operations become
O(n² log n), which is worse than the O(n²) achievable with array-based Dijkstra.

### 1.2 Dictionary Lookups (20-30% of runtime)
Each neighbor check requires `dist.get(v, INF)` to compare against the current best
distance. Python dict operations have O(1) amortized cost but high constant factors
due to hashing overhead and cache misses for large dictionaries.

### 1.3 Graph Traversal / Iterator Overhead (15-20% of runtime)
Iterating `graph.neighbors(u)` creates a Python iterator over dict items.  The
overhead of Python's iteration protocol (creating iterator objects, calling `__next__`,
unpacking tuples) is significant compared to native C/C++ implementations.

## 2. Specific Improvement Opportunities

### Opportunity 1: Bidirectional Search with Landmark Pruning (ALT-Bidirectional)
**Theoretical justification:** Bidirectional search reduces search space by ~50%
\cite{pohl1971}. Landmark-based heuristics provide tight lower bounds \cite{goldberg2005}.
Combining them should yield superadditive pruning because the landmark bounds tighten
the meeting condition in bidirectional search.

**Estimated speedup:** 3-5x on structured graphs (grids, road networks) vs standard Dijkstra.

**From literature:** This is the ALT (A*, Landmarks, Triangle inequality) approach
from \cite{goldberg2005}, extended to bidirectional search.  \cite{geisberger2008}
showed that bidirectional CH queries are extremely fast; our approach uses cheaper
preprocessing than full CH while capturing similar bidirectional benefits.

### Opportunity 2: Adaptive Priority Queue (Bucket Queue + Heap Hybrid)
**Theoretical justification:** Dial's bucket queue \cite{dial1969} achieves O(V + E + C)
for integer weights with max weight C.  When C is small (common in road networks where
weights are travel times in seconds), this avoids log-factor overhead entirely.

**Our proposal:** Adaptively select between bucket queue and binary heap based on the
weight distribution observed during preprocessing.  For graphs with bounded integer
weights, use bucket queue; for unbounded/real weights, fall back to binary heap.

**Estimated speedup:** 2-3x on graphs with small integer weights.  No improvement on
real-valued weights.

### Opportunity 3: Hub-Based Pruning with Lightweight Preprocessing
**Theoretical justification:** Hub labeling \cite{abraham2012} achieves near-constant
query time but requires expensive preprocessing.  We propose a lightweight version:
identify the top-k highest-degree vertices as "hub" candidates during a single O(V+E)
pass.  During search, when both forward and backward searches have reached hub vertices,
check if any hub lies on the shortest path.

**From literature:** \cite{bast2007} showed that transit nodes (a form of hubs) enable
O(1) queries for non-local queries.  Our approach uses far simpler hub identification
but may still capture significant pruning on scale-free and road network graphs.

**Estimated speedup:** 2-4x on scale-free graphs; less effective on uniform-degree graphs.

## 3. Comparison with Literature Techniques

| Opportunity | Related Technique | Advantage | Disadvantage |
|-------------|-------------------|-----------|--------------|
| ALT-Bidirectional | ALT \cite{goldberg2005} | Combines two pruning mechanisms | Requires landmark precomputation |
| Adaptive PQ | Dial's algorithm \cite{dial1969} | O(V+E+C) for integer weights | Only helps with bounded weights |
| Hub pruning | Hub labeling \cite{abraham2012} | Lightweight O(V+E) preprocessing | Less effective than full HL |
| (baseline) CH \cite{geisberger2008} | Full preprocessing | Heavy preprocessing cost |
| (baseline) CRP \cite{delling2011} | Metric-independent partitioning | Requires graph partitioning |

## 4. Concrete Hypothesis

**Hypothesis:** A hybrid algorithm combining (1) bidirectional search, (2) landmark-based
lower bounds (ALT heuristic), and (3) adaptive hub detection will achieve ≥2x speedup
over standard Dijkstra across diverse graph types, with only O(kV + kE) preprocessing
cost (where k is the number of landmarks, typically 4-16).

The key novelty is the combination: bidirectional ALT search with hub-based early
termination. When the forward and backward search frontiers both encounter a high-degree
hub vertex that was precomputed as a "bridge" node, we can check the hub path and
potentially terminate early without the full CH preprocessing machinery.

This combines insights from:
- \cite{pohl1971} (bidirectional search reduces search space)
- \cite{goldberg2005} (landmark bounds tighten search)
- \cite{abraham2012} (hub vertices enable fast queries)
- \cite{bast2007} (transit nodes for non-local queries)
- \cite{geisberger2008} (hierarchical structure in road networks)
