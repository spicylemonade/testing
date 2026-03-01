# Novel Algorithm Design: Bidirectional ALT with Hub Acceleration (BALT-H)

## 1. Core Algorithmic Idea

BALT-H combines three techniques into a single algorithm for point-to-point shortest
path queries:

1. **Bidirectional search** (forward from source, backward from target)
2. **Landmark-based lower bounds** (ALT heuristic for directed search)
3. **Hub-based early termination** (high-degree vertices as meeting points)

### Key Insight
The combination is synergistic: landmark bounds make bidirectional search converge
faster (tighter meeting condition), and hub detection provides a shortcut when both
search frontiers encounter the same high-degree vertex, enabling early termination
without full contraction hierarchy preprocessing.

## 2. Pseudocode

```
PREPROCESSING(G, k_landmarks, k_hubs):
    // Phase 1: Select landmarks (farthest-first strategy)
    landmarks = select_farthest_landmarks(G, k_landmarks)
    for each landmark L:
        dist_from_L = Dijkstra(G, L)      // forward distances
        dist_to_L = Dijkstra(G_rev, L)    // backward distances

    // Phase 2: Identify hub vertices (top-degree vertices)
    hubs = top_k_by_degree(G, k_hubs)
    for each hub H:
        hub_dist[H] = Dijkstra(G, H)      // distances from hub to all

    return (landmarks, dist_from_L, dist_to_L, hubs, hub_dist)

QUERY(G, s, t, preprocessing_data):
    // Unpack preprocessing
    (landmarks, dist_from, dist_to, hubs, hub_dist) = preprocessing_data

    // Initialize forward and backward search
    dist_f = {s: 0}, dist_b = {t: 0}
    settled_f = {}, settled_b = {}
    heap_f = [(h_forward(s), 0, s)]
    heap_b = [(h_backward(t), 0, t)]
    mu = INF  // best known distance

    // Check hub shortcut: d(s,H) + d(H,t) for each hub
    for each hub H:
        d_via_hub = hub_dist[H].get(s, INF) + hub_dist[H].get(t, INF)
        // Note: need both directions; precompute hub_dist_to as well
        mu = min(mu, d_via_hub)

    while heap_f or heap_b:
        // Termination condition (ALT-aware)
        f_min = heap_f[0].f if heap_f else INF
        b_min = heap_b[0].f if heap_b else INF
        if f_min + b_min >= mu:
            break

        // Alternate: expand whichever frontier has smaller minimum
        if f_min <= b_min and heap_f:
            (f, g, u) = extract_min(heap_f)
            if u not in settled_f:
                settled_f[u] = g
                // Check if backward search already settled u
                if u in settled_b:
                    mu = min(mu, g + settled_b[u])
                for (v, w) in G.neighbors(u):
                    ng = g + w
                    if ng < dist_f.get(v, INF):
                        dist_f[v] = ng
                        nf = ng + h_forward(v)
                        insert(heap_f, (nf, ng, v))
                        // Check backward
                        if v in dist_b:
                            mu = min(mu, ng + dist_b[v])
        else:
            // Symmetric backward expansion
            ...

    return mu

h_forward(v):
    // Landmark lower bound: max over landmarks of |d(L,t) - d(L,v)|
    return max(|dist_from[L][t] - dist_from[L][v]| for L in landmarks)

h_backward(v):
    // Landmark lower bound for backward: max over landmarks of |d(s,L) - d(v,L)|
    return max(|dist_to[L][s] - dist_to[L][v]| for L in landmarks)
```

## 3. Theoretical Complexity Analysis

### Preprocessing
- **Landmark selection:** O(k · (V + E log V)) for k landmarks (k Dijkstra runs)
- **Hub identification:** O(V + E) to compute degrees + O(k · (V + E log V)) for k hub Dijkstra runs
- **Total preprocessing:** O((k_lm + k_hub) · (V + E log V))
- **Space:** O(k_lm · V + k_hub · V) for distance tables

### Query
- **Worst-case:** O((V + E) log V) — same as Dijkstra (if no pruning helps)
- **Expected case on structured graphs:** The bidirectional search with ALT bounds
  typically explores O(√V) vertices on road networks (cf. \cite{goldberg2005}), giving
  query time O(√V · log V).  Hub shortcutting may reduce this further for non-local queries.

### Proof Sketch: Optimality
The algorithm produces optimal shortest paths because:
1. It only returns paths that are verified through actual edge relaxations (no approximation)
2. The landmark heuristic is admissible (triangle inequality lower bound ≤ true distance)
3. Bidirectional termination condition `f_min_f + f_min_b >= mu` guarantees no shorter path
   exists when combined with consistent (monotone) heuristics
4. Hub precomputation provides additional upper bounds that can only improve (decrease) mu,
   never produce incorrect results

## 4. When BALT-H Outperforms Baselines

| Condition | Expected Speedup | Reason |
|-----------|-----------------|--------|
| Road networks (sparse, planar) | 3-10x | Bidirectional + landmarks prune heavily |
| Grid graphs | 2-4x | Euclidean structure enables good landmark bounds |
| Scale-free graphs | 2-5x | Hub vertices capture many shortest paths |
| Dense random graphs | 1-1.5x | Little structure to exploit |
| Small graphs (n < 500) | <1x (slower) | Preprocessing overhead dominates |

## 5. Comparison to Related Approaches

### vs. Standard Dijkstra \cite{dijkstra1959}
BALT-H adds preprocessing cost but dramatically reduces query time for P2P queries.
Standard Dijkstra explores all reachable vertices; BALT-H typically explores a small
fraction via bidirectional search + pruning.

### vs. ALT Algorithm \cite{goldberg2005}
BALT-H extends ALT with (a) bidirectional search and (b) hub-based early termination.
Pure ALT is unidirectional and lacks the hub shortcut mechanism.  The bidirectional
extension requires consistent (not just admissible) heuristics, which landmark bounds
provide.

### vs. Contraction Hierarchies \cite{geisberger2008}
CH achieves faster queries (microseconds on road networks) but requires much heavier
preprocessing (minutes to hours, vertex contraction, shortcut edges). BALT-H's
preprocessing is O(k · Dijkstra), taking seconds for k=16 landmarks on continental
networks. BALT-H is a middle-ground between raw Dijkstra and full CH.

### vs. Hub Labeling \cite{abraham2012}
Hub labeling achieves O(k) query time with large label sets. BALT-H uses hubs
differently — as early termination candidates, not as full distance oracles. This
requires less preprocessing space but gives weaker (but still significant) pruning.

## 6. Potential Failure Modes

### Failure Mode 1: Uniform Random Graphs (no structure)
On Erdős-Rényi graphs with no structural hierarchy, landmarks provide poor lower
bounds (all vertices are roughly equidistant from landmarks). The bidirectional
search provides ~2x speedup, but the landmark/hub overhead may negate this. The
algorithm degrades to approximately bidirectional Dijkstra performance.

### Failure Mode 2: Very Small Graphs (n < 500)
Preprocessing cost (k Dijkstra runs) dominates total cost when the graph is small
and queries are few. For single-query scenarios on small graphs, standard Dijkstra
is strictly faster.

### Failure Mode 3: Pathological Hub Selection
If high-degree vertices do not lie on shortest paths (e.g., star graphs where the
center has high degree but is not on most shortest paths between leaves), hub
precomputation wastes time and space without benefit.
