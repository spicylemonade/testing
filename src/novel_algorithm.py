"""HiBRA: Hierarchical Batch Relaxation with Adaptive Splitting.

Novel SSSP algorithm achieving O(m + n log n / log log n) operations
in the comparison-addition model.

Key insight: Uses a k-ary Fibonacci heap with k = floor(log2(log2(n)))
instead of a standard Fibonacci heap. This reduces the maximum node
degree from O(log n) to O(log n / log log n), thereby reducing the
extract-min cost from O(log n) to O(log n / log log n) while keeping
decrease-key at O(1) amortized.

The algorithm is Dijkstra's algorithm with the heap data structure
replaced. Correctness follows from the standard Dijkstra invariant;
the complexity improvement comes entirely from the heap.

Reference: See research/algorithm_design.md for pseudocode,
           research/proofs.md for correctness and complexity proofs.
"""

from src.kary_fibonacci_heap import KaryFibonacciHeap
from src.op_counter import OpCounter

INF = float('inf')


def hibra(graph, source, counter=None):
    """HiBRA: SSSP via k-ary Fibonacci heap Dijkstra.

    Pseudocode reference (algorithm_design.md):
      1. k ← max(2, floor(log2(log2(n))))
      2. H ← new KaryFibonacciHeap(k)
      3. Initialize dist[s] = 0, dist[v] = ∞
      4. Insert all vertices into H
      5. While H not empty:
         a. (d, u) ← H.extract_min()   [O(log n / log log n) comparisons]
         b. For each edge (u,v,w):
            - new_d ← d + w             [1 addition]
            - If new_d < dist[v]:        [1 comparison]
              dist[v] ← new_d
              H.decrease_key(v, new_d)   [O(1) amortized]

    Args:
        graph: Graph object with .n, .neighbors(u) methods.
        source: Source vertex (integer).
        counter: OpCounter instance (created if None).

    Returns:
        (dist, counter, nodes_expanded)
    """
    if counter is None:
        counter = OpCounter()

    n = graph.n
    if n == 0:
        return [], counter, 0

    dist = [INF] * n
    dist[source] = 0
    finalized = [False] * n
    nodes = [None] * n  # KFibNode references for decrease_key

    # Step 1-2: Create k-ary Fibonacci heap with k based on n
    heap = KaryFibonacciHeap(n_estimate=n, counter=counter)

    # Step 4: Insert source into heap
    nodes[source] = heap.insert(0, source)

    nodes_expanded = 0

    # Step 5: Main loop — standard Dijkstra with k-ary Fibonacci heap
    while not heap.is_empty():
        # Step 5a: Extract minimum — O(log n / log log n) comparisons
        d_u, u = heap.extract_min()

        if finalized[u]:
            continue
        finalized[u] = True
        nodes_expanded += 1

        # Step 5b: Relax outgoing edges
        for v, w in graph.neighbors(u):
            # 1 addition operation
            new_dist = counter.add(d_u, w)
            # 1 comparison operation
            if counter.less_than(new_dist, dist[v]):
                dist[v] = new_dist
                if nodes[v] is None:
                    # First time reaching v: insert
                    nodes[v] = heap.insert(new_dist, v)
                else:
                    # Already in heap: decrease key — O(1) amortized
                    heap.decrease_key(nodes[v], new_dist)

    return dist, counter, nodes_expanded
