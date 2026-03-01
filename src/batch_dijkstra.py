"""Simplified sorting-barrier-breaking SSSP reference implementation.

Uses a modified Dial's algorithm / bucket-based SSSP. The key idea from
the sorting barrier literature is that SSSP can be solved with fewer
comparisons by avoiding full vertex sorting.

This reference uses small bucket widths to reduce within-bucket errors.
Correctness is ensured by processing each bucket completely (including
re-insertions) before advancing.

SIMPLIFICATION vs. Duan et al. 2025:
  - Uses simple bucket decomposition instead of interval pivots
  - Smaller bucket width sqrt(max_weight) for accuracy
  - No recursive subproblem decomposition or hop-limited exploration
"""

from collections import deque, defaultdict
import math
from src.graph import Graph
from src.op_counter import OpCounter

INF = float('inf')


def batch_dijkstra(graph, source, counter=None):
    """Bucket-based SSSP with reduced comparisons.

    Uses small bucket widths. Within each bucket, FIFO processing avoids
    priority-queue comparisons. Multiple passes per bucket ensure correctness.

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

    # Find min edge weight for bucket width
    min_weight = INF
    max_weight = 0
    for u in range(n):
        for v, w in graph.neighbors(u):
            if w < min_weight and w > 0:
                min_weight = w
            if w > max_weight:
                max_weight = w

    if min_weight == INF:
        min_weight = 1

    # Use min_weight as bucket width — guarantees correctness
    # because any edge weight >= delta, so relaxing a vertex in bucket i
    # can only reach bucket >= i. Within a bucket, all distances are
    # within [i*delta, (i+1)*delta), so they can be processed in any order.
    delta = min_weight if min_weight > 0 else max(1e-10, max_weight)

    buckets = defaultdict(deque)
    buckets[0].append(source)

    current_bucket = 0
    nodes_expanded = 0
    max_bucket_used = 0
    finalized = [False] * n

    while current_bucket <= max_bucket_used + 1:
        while buckets[current_bucket]:
            u = buckets[current_bucket].popleft()

            if finalized[u]:
                continue

            if dist[u] == INF:
                continue

            u_bucket = int(dist[u] / delta)
            if u_bucket > current_bucket:
                buckets[u_bucket].append(u)
                if u_bucket > max_bucket_used:
                    max_bucket_used = u_bucket
                continue

            finalized[u] = True
            nodes_expanded += 1
            counter.record_extract_min()

            for v, w in graph.neighbors(u):
                new_dist = counter.add(dist[u], w)
                if counter.less_than(new_dist, dist[v]):
                    dist[v] = new_dist
                    if not finalized[v]:
                        v_bucket = int(new_dist / delta)
                        buckets[v_bucket].append(v)
                        counter.record_insert()
                        if v_bucket > max_bucket_used:
                            max_bucket_used = v_bucket

        current_bucket += 1

    return dist, counter, nodes_expanded
