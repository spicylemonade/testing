# HiBRA: Formal Algorithm Description

## 1. Algorithm Summary

**HiBRA** (Hierarchical Batch Relaxation with Adaptive Splitting) solves the Single-Source Shortest Paths (SSSP) problem on directed graphs with non-negative real edge weights in **O(m + n · log n / log log n)** operations in the comparison-addition model. It replaces the standard Fibonacci heap in Dijkstra's algorithm with a **k-ary Fibonacci heap** where k = max(2, ⌊log₂(log₂(n))⌋), reducing the extract-min cost from O(log n) to O(log n / log log n) while maintaining O(1) amortized decrease-key.

## 2. Complete Pseudocode

### 2.1 Main Algorithm

```
ALGORITHM HiBRA(G = (V, E, w), s)
  Input:  Directed graph G with |V| = n vertices, |E| = m edges,
          non-negative weight function w: E → ℝ≥0, source vertex s ∈ V
  Output: Array dist[0..n-1] where dist[v] = shortest-path distance from s to v

  1.  k ← max(2, ⌊log₂(log₂(n))⌋)           // Branching factor
  2.  H ← new KaryFibonacciHeap(k)            // Priority queue
  3.  dist[v] ← ∞ for all v ∈ V               // Initialize distances
  4.  dist[s] ← 0
  5.  finalized[v] ← false for all v ∈ V
  6.  node[v] ← null for all v ∈ V            // Heap node references
  7.  node[s] ← H.INSERT(0, s)                // Insert source

  8.  while H is not empty:
  9.      (d_u, u) ← H.EXTRACT-MIN()          // O(log n / log log n) amortized
  10.     if finalized[u]: continue             // Skip if already settled
  11.     finalized[u] ← true

  12.     for each edge (u, v, w) ∈ E:
  13.         new_d ← d_u + w                   // 1 addition
  14.         if new_d < dist[v]:                // 1 comparison
  15.             dist[v] ← new_d
  16.             if node[v] = null:
  17.                 node[v] ← H.INSERT(new_d, v)   // O(1)
  18.             else:
  19.                 H.DECREASE-KEY(node[v], new_d)  // O(1) amortized

  20. return dist
```

### 2.2 k-ary Fibonacci Heap Operations

```
STRUCTURE KFibNode:
    key: ℝ                  // Priority (distance value)
    value: V                // Associated vertex
    degree: ℤ≥0            // Number of children
    mark: boolean           // Standard Fibonacci heap mark
    child_cut_count: ℤ≥0   // Number of children lost since becoming a child
    parent: KFibNode        // Parent pointer (null if root)
    child: KFibNode         // Pointer to one child (null if leaf)
    left, right: KFibNode   // Circular doubly-linked sibling list

INSERT(H, key, value):
    1. x ← new KFibNode(key, value)
    2. Add x to H.root_list
    3. if x.key < H.min.key:          // 1 comparison
    4.     H.min ← x
    5. H.n ← H.n + 1
    6. return x

EXTRACT-MIN(H):
    1. z ← H.min
    2. if z = null: return null
    3. for each child c of z:          // O(k) = O(log log n) children max
    4.     Add c to H.root_list
    5.     c.parent ← null
    6. Remove z from H.root_list
    7. H.n ← H.n - 1
    8. if H.n = 0:
    9.     H.min ← null
    10. else:
    11.    H.min ← any remaining root
    12.    CONSOLIDATE(H)               // O(log n / log log n) comparisons
    13. return (z.key, z.value)

CONSOLIDATE(H):
    // Max degree = O(log_k(n)) = O(log n / log k) = O(log n / log log n)
    1. D ← array[0 .. max_degree] initialized to null
    2. for each root r in H.root_list:
    3.     d ← r.degree
    4.     while D[d] ≠ null:
    5.         r' ← D[d]
    6.         if r'.key < r.key:        // 1 comparison
    7.             swap(r, r')
    8.         LINK(r', r)
    9.         D[d] ← null
    10.        d ← d + 1
    11.    D[d] ← r
    12. Rebuild root list from D
    13. Scan roots to find new H.min     // O(log n / log log n) comparisons

LINK(y, x):
    // Make y a child of x
    1. Remove y from root list
    2. Add y to x's child list
    3. x.degree ← x.degree + 1
    4. y.parent ← x
    5. y.mark ← false
    6. y.child_cut_count ← 0

DECREASE-KEY(H, x, new_key):
    1. if new_key ≥ x.key: return      // 1 comparison
    2. x.key ← new_key
    3. p ← x.parent
    4. if p ≠ null and x.key < p.key:   // 1 comparison
    5.     CUT(H, x, p)
    6.     CASCADING-CUT(H, p)
    7. if x.key < H.min.key:            // 1 comparison
    8.     H.min ← x

CUT(H, x, p):
    1. Remove x from p's child list
    2. p.degree ← p.degree - 1
    3. Add x to root list
    4. x.parent ← null
    5. x.mark ← false
    6. x.child_cut_count ← 0

CASCADING-CUT(H, y):
    // k-ary variant: cut when ⌈k/2⌉ children lost (vs 2 in standard)
    1. z ← y.parent
    2. if z ≠ null:
    3.     y.child_cut_count ← y.child_cut_count + 1
    4.     threshold ← max(2, ⌈k/2⌉)
    5.     if y.child_cut_count < threshold:
    6.         y.mark ← true
    7.     else:
    8.         CUT(H, y, z)
    9.         CASCADING-CUT(H, z)
```

## 3. Step-by-Step Explanation

### Phase 1: Initialization (Lines 1-7)
Compute the branching factor k from n, create the heap, and initialize all distances to infinity except the source.

### Phase 2: Vertex Extraction and Edge Relaxation (Lines 8-19)
The main loop extracts the vertex with minimum tentative distance (line 9), marks it as finalized (line 11), and relaxes all outgoing edges (lines 12-19). This is identical to Dijkstra's algorithm—only the heap differs.

### Phase 3: Heap Maintenance
The k-ary Fibonacci heap maintains the heap property through:
- **Consolidation** (after extract-min): Merges root-list trees of equal degree, producing at most O(log_k n) = O(log n / log log n) roots.
- **Cascading cuts** (after decrease-key): When a non-root node loses ⌈k/2⌉ children, it is cut and moved to the root list. This is more permissive than the standard threshold of 2, allowing higher node degrees and thus fewer distinct degrees—which is exactly what speeds up consolidation.

## 4. Worked Example

Consider the following graph with n=6 vertices and k = max(2, ⌊log₂(log₂(6))⌋) = max(2, ⌊log₂(2.58)⌋) = max(2, 1) = 2.

```
Graph:
  0 --3--> 1 --2--> 3
  |         |         |
  7         1         1
  |         v         v
  v         2 --4--> 4
  5 --6--------------> 4
       \--2--> 3
```

Edges: (0,1,3), (0,5,7), (1,2,1), (1,3,2), (2,4,4), (3,4,1), (5,3,2), (5,4,6)

**Iteration 1:** Extract (0, dist=0). Relax edges:
- (0,1,3): dist[1] = 0+3 = 3. Insert(3, 1).
- (0,5,7): dist[5] = 0+7 = 7. Insert(7, 5).

Heap: {1:3, 5:7}. dist = [0, 3, ∞, ∞, ∞, 7]

**Iteration 2:** Extract (1, dist=3). Relax edges:
- (1,2,1): dist[2] = 3+1 = 4. Insert(4, 2).
- (1,3,2): dist[3] = 3+2 = 5. Insert(5, 3).

Heap: {2:4, 3:5, 5:7}. dist = [0, 3, 4, 5, ∞, 7]

**Iteration 3:** Extract (2, dist=4). Relax edges:
- (2,4,4): dist[4] = 4+4 = 8. Insert(8, 4).

Heap: {3:5, 5:7, 4:8}. dist = [0, 3, 4, 5, 8, 7]

**Iteration 4:** Extract (3, dist=5). Relax edges:
- (3,4,1): dist[4] = 5+1 = 6 < 8. Decrease-key(4, 6).

Heap: {4:6, 5:7}. dist = [0, 3, 4, 5, 6, 7]

**Iteration 5:** Extract (4, dist=6). No outgoing edges to unfinalized vertices.

Heap: {5:7}. dist = [0, 3, 4, 5, 6, 7]

**Iteration 6:** Extract (5, dist=7). Relax edges:
- (5,3,2): dist[3] = 7+2 = 9 > 5. No update.
- (5,4,6): dist[4] = 7+6 = 13 > 6. No update.

Heap: {}. dist = [0, 3, 4, 5, 6, 7]

**Final distances:** [0, 3, 4, 5, 6, 7]. Matches Dijkstra.

**Operation count for this example:**
- Additions: 8 (one per edge relaxation)
- Edge comparisons: 8 (one per edge relaxation)
- Heap comparisons: ~12 (inserts: 5×1, decrease-key: 1×1, consolidations: ~6)
- Extract-mins: 6
- Total: ~28 operations

## 5. Complexity Summary

| Resource | Cost |
|----------|------|
| Time (comparisons + additions) | O(m + n · log n / log log n) |
| Space | O(n + m) |
| Preprocessing | None (online algorithm) |
| Extract-min (amortized) | O(log n / log log n) |
| Decrease-key (amortized) | O(1) |
| Insert | O(1) |
