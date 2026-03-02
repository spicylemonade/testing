"""Dijkstra's SSSP algorithm using a binary heap (Python heapq) with lazy deletion."""

import heapq


def sssp(adj, source, n):
    """Dijkstra's algorithm with a binary min-heap (heapq) and lazy deletion.

    Since heapq does not support decrease_key, stale entries are left in the
    heap and skipped when popped (lazy deletion pattern).

    Args:
        adj: dict mapping vertex -> list of (neighbor, weight).
        source: source vertex.
        n: number of vertices (unused beyond documentation).

    Returns:
        (distances, stats) where distances maps vertex -> shortest distance
        and stats is a dict with keys comparisons, additions, heap_ops.
    """
    INF = float("inf")
    dist = {v: INF for v in adj}
    dist[source] = 0

    stats = {"comparisons": 0, "additions": 0, "heap_ops": 0}

    # Min-heap of (distance, vertex)
    heap = [(0, source)]
    stats["heap_ops"] += 1  # initial push

    visited = set()

    while heap:
        d_u, u = heapq.heappop(heap)
        stats["heap_ops"] += 1

        # Lazy deletion: skip if we already found a shorter path
        stats["comparisons"] += 1
        if d_u > dist[u]:
            continue

        if u in visited:
            continue
        visited.add(u)

        for v, w in adj.get(u, []):
            stats["additions"] += 1
            new_dist = d_u + w
            stats["comparisons"] += 1
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))
                stats["heap_ops"] += 1

    return dist, stats
