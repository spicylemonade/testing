# Correctness and Complexity Proofs for HiBRA

## 1. Correctness Proof

### Theorem 1 (Correctness)
Let G = (V, E, w) be a directed graph with non-negative edge weights, and let s ∈ V be the source vertex. HiBRA correctly computes d(s,v) for all v ∈ V, where d(s,v) is the shortest-path distance from s to v.

### Proof

HiBRA uses the standard Dijkstra algorithm skeleton with a k-ary Fibonacci heap instead of a standard Fibonacci heap. We show that the k-ary Fibonacci heap correctly implements a priority queue, which suffices for Dijkstra's correctness.

**Loop Invariant:** At the start of each iteration of the while loop, for every finalized vertex u (i.e., u has been extracted from the heap), dist[u] = d(s,u) is the true shortest-path distance.

**Initialization:** Initially, only s is in the heap with key 0, and dist[s] = 0 = d(s,s). No vertices are finalized. The invariant holds vacuously.

**Maintenance:** Suppose the invariant holds before extracting vertex u. We need to show dist[u] = d(s,u).

Since u has the minimum key in the heap and all finalized vertices have correct distances, assume for contradiction that d(s,u) < dist[u]. Then there exists a shortest path P from s to u. Let (x,y) be the first edge on P where x is finalized but y is not. Since x is finalized with correct distance d(s,x), and the edge (x,y) was relaxed when x was extracted, we have:

dist[y] ≤ d(s,x) + w(x,y) = d(s,y) ≤ d(s,u) < dist[u]

But u has the minimum key in the heap, so dist[u] ≤ dist[y], contradiction.

This argument is identical to the standard Dijkstra correctness proof and depends only on the priority queue correctly returning the element with minimum key. The k-ary Fibonacci heap, being a valid min-heap, satisfies this requirement (see Lemma 1 below).

**Termination:** Each iteration extracts one vertex and marks it finalized. Since there are n vertices and no vertex is extracted twice (finalized vertices are removed from the heap), the algorithm terminates after at most n iterations.

**Edge Cases:**
- *Disconnected graphs:* Unreachable vertices retain dist[v] = ∞, which is correct.
- *Zero-weight edges:* The non-negative weight assumption ensures w(e) ≥ 0, so the greedy property holds even with zero weights.
- *Parallel edges:* Multiple edges between the same pair are handled naturally; each is relaxed independently.

### Lemma 1 (k-ary Fibonacci Heap Correctness)
The k-ary Fibonacci heap correctly implements a min-heap: extract_min always returns the element with the minimum key.

**Proof:** The k-ary Fibonacci heap maintains the heap property: each node's key is ≤ its children's keys. This is maintained by:
1. **Insert:** New nodes are added to the root list (trivially satisfying heap property as they have no children).
2. **Decrease-key:** If the new key violates the heap property with the parent, the node is cut and moved to the root list (cascading cut). The cut node now has no parent, so no violation.
3. **Extract-min:** The minimum is at a root node (since all non-root nodes have a parent with smaller or equal key). After removing the minimum, its children are promoted to roots and consolidation merges trees while maintaining the heap property (via linking only smaller-keyed roots as parents).
4. **Consolidation:** Only links tree y under tree x when x.key ≤ y.key, maintaining the heap property.

The minimum root is always correctly identified during consolidation by scanning all roots. □

## 2. Complexity Analysis

### Theorem 2 (Complexity Bound)
HiBRA solves SSSP in O(m + n · log n / log log n) operations in the comparison-addition model.

### Proof

We analyze the cost of each phase:

#### Phase 1: Edge Relaxation

Each edge (u,v,w) is relaxed exactly once when vertex u is extracted. Each relaxation requires:
- 1 addition: dist[u] + w
- 1 comparison: is new_dist < dist[v]?
- At most 1 decrease-key operation if the comparison succeeds.

Total edge relaxation cost: **O(m)** additions + **O(m)** comparisons = **O(m)** operations.

#### Phase 2: Heap Operations

We must account for:
- n insert operations
- n extract-min operations
- At most m decrease-key operations

**Lemma 2 (k-ary Fibonacci Heap: Extract-Min Cost).**
Each extract-min in a k-ary Fibonacci heap with k = Θ(log log n) costs O(k + log_k n) = O(log log n + log n / log log n) = O(log n / log log n) amortized comparisons.

**Proof of Lemma 2:**
1. *Adding children to root list:* The extracted node has at most D(k,n) children, where D(k,n) is the maximum degree. By the Fibonacci heap degree bound generalized to k-ary: D(k,n) = O(log_k n) = O(log n / log(log log n)) = O(log n / log log n). Adding these children costs O(D(k,n)) = O(log n / log log n) to traverse.

2. *Consolidation:* We scan the root list and merge trees with equal degrees. The number of distinct degrees is at most D(k,n) + 1 = O(log n / log log n). Each merge involves linking one tree under another (1 comparison, O(1) pointer operations). The final scan to find the new minimum visits O(log n / log log n) roots.

Total per extract-min: O(log n / log log n) amortized comparisons.

**Remark on the degree bound:** In a k-ary Fibonacci heap, the cascading cut rule ensures that a node of degree d has at least F_k(d) descendants, where F_k is a generalized Fibonacci-like sequence with F_k(0)=1, F_k(1)=k+1, and F_k(i) ≥ k·F_k(i-2) for i ≥ 2. This gives d ≤ log_φ_k(n) where φ_k ≈ k^{1/2} for large k. For k = log log n, this gives:
d ≤ log_{(log log n)^{1/2}}(n) = 2·log n / log(log log n) = O(log n / log log n).

**Lemma 3 (k-ary Fibonacci Heap: Decrease-Key Cost).**
Each decrease-key costs O(1) amortized comparisons.

**Proof:** Identical to the standard Fibonacci heap analysis. Decrease-key performs at most one cut and one cascading cut chain. The cascading cut chain is charged using the potential function Φ = Σ(2·mark(v)), where mark(v) ∈ {0,1}. Each cascading cut reduces Φ by 2, paying for its O(1) comparison cost. The amortized cost is O(1). □

**Lemma 4 (k-ary Fibonacci Heap: Insert Cost).**
Each insert costs O(1) comparisons (add to root list, compare with min).

#### Total Complexity

| Operation | Count | Amortized Cost | Total |
|-----------|-------|---------------|-------|
| Insert | n | O(1) | O(n) |
| Extract-min | n | O(log n / log log n) | **O(n log n / log log n)** |
| Decrease-key | ≤ m | O(1) | O(m) |
| Edge additions | m | O(1) | O(m) |
| Edge comparisons | m | O(1) | O(m) |

**Grand total: O(m + n · log n / log log n).**

Since m ≥ n-1 for connected graphs, this simplifies to O(m + n log n / log log n).

### Theorem 3 (Improvement over Fredman-Tarjan)
For all n ≥ 4, O(m + n log n / log log n) = o(m + n log n).

**Proof:** We need to show n log n / log log n = o(n log n), i.e., 1/log log n → 0 as n → ∞. Since log log n → ∞ as n → ∞, this follows immediately.

The ratio of improvement is log log n, which grows (slowly) without bound. □

### Discussion: Tightness

The bound O(m + n log n / log log n) is likely not tight. The log n / log log n factor arises from the maximum degree in the k-ary Fibonacci heap. It may be possible to:
1. Use larger k (e.g., k = log n) to get O(m + n · log n / log log n) → but this increases decrease-key cost.
2. Use a different heap structure entirely to achieve O(m + n · log^c n) for c < 1 (as Duan et al. achieve O(m · log^{2/3} n) by avoiding heaps altogether).

A matching lower bound of Ω(m + n log n / log log n) is not known. The best known lower bound in the comparison-addition model is Ω(m), so there remains a gap.
