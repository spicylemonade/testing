"""Bellman-Ford SSSP algorithm."""


def sssp(adj, source, n):
    """Bellman-Ford single-source shortest paths.

    Runs n-1 relaxation rounds over every edge. Works with negative edge
    weights (unlike Dijkstra) but does not detect negative cycles.

    Args:
        adj: dict mapping vertex -> list of (neighbor, weight).
        source: source vertex.
        n: number of vertices.

    Returns:
        (distances, stats) where distances maps vertex -> shortest distance
        and stats is a dict with keys comparisons, additions, heap_ops.
    """
    INF = float("inf")
    dist = {v: INF for v in adj}
    dist[source] = 0

    stats = {"comparisons": 0, "additions": 0, "heap_ops": 0}

    # Build a flat edge list once for efficiency.
    edges = []
    for u in adj:
        for v, w in adj[u]:
            edges.append((u, v, w))

    # Relax all edges n-1 times.
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            stats["additions"] += 1
            new_dist = dist[u] + w
            stats["comparisons"] += 1
            if new_dist < dist[v]:
                dist[v] = new_dist
                changed = True
        # Early termination if no distance was updated this round.
        if not changed:
            break

    return dist, stats
