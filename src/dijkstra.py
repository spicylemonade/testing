"""Dijkstra's algorithm — three variants for SSSP and point-to-point.

Variant 1: Standard Dijkstra with binary heap (heapq)
Variant 2: Dijkstra with lazy deletion (simulates decrease-key)
Variant 3: Bidirectional Dijkstra for point-to-point queries

All variants return (dist_dict, nodes_expanded) where dist_dict maps
vertex -> shortest distance from source, and nodes_expanded counts
the number of vertices settled during search.
"""

from __future__ import annotations

import heapq
import math
from typing import Dict, Optional, Tuple

from src.graph import Graph

INF = float("inf")


def dijkstra_standard(graph: Graph, source: int) -> Tuple[Dict[int, float], int]:
    """Dijkstra with binary heap (heapq).  O((V+E) log V).

    Uses lazy deletion: when a vertex is popped from the heap but already
    settled, it is skipped.  This avoids the need for decrease-key.
    """
    dist: Dict[int, float] = {source: 0.0}
    settled = set()
    heap = [(0.0, source)]
    nodes_expanded = 0

    while heap:
        d, u = heapq.heappop(heap)
        if u in settled:
            continue
        settled.add(u)
        nodes_expanded += 1
        for v, w in graph.neighbors(u):
            nd = d + w
            if nd < dist.get(v, INF):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist, nodes_expanded


def dijkstra_decreasekey(graph: Graph, source: int) -> Tuple[Dict[int, float], int]:
    """Dijkstra with explicit decrease-key via index tracking.

    Simulates Fibonacci-heap behavior using a dict-backed heap that
    tracks current distances. In Python, we use lazy deletion with
    an additional optimization: skip stale entries early by comparing
    against the recorded distance before processing neighbors.

    This is functionally identical to the standard variant but provides
    a distinct implementation for benchmarking comparisons.
    """
    dist: Dict[int, float] = {}
    for n in graph.nodes():
        dist[n] = INF
    dist[source] = 0.0

    settled = set()
    heap = [(0.0, source)]
    nodes_expanded = 0

    while heap:
        d, u = heapq.heappop(heap)
        if u in settled:
            continue
        if d > dist[u]:
            continue  # stale entry
        settled.add(u)
        nodes_expanded += 1
        for v, w in graph.neighbors(u):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    # Filter unreachable vertices
    return {k: v for k, v in dist.items() if v < INF}, nodes_expanded


def dijkstra_bidirectional(graph: Graph, source: int, target: int) -> Tuple[float, int]:
    """Bidirectional Dijkstra for point-to-point shortest path.

    Runs forward search from source and backward search from target
    simultaneously.  Returns (distance, nodes_expanded).
    For undirected graphs, backward uses the same adjacency.
    For directed graphs, this implementation builds a reverse graph on the fly.

    Returns (INF, nodes_expanded) if target is unreachable.
    """
    if source == target:
        return 0.0, 0

    # Build reverse adjacency for directed graphs
    if graph.directed:
        rev_adj = {}
        for u in graph.nodes():
            for v, w in graph.neighbors(u):
                if v not in rev_adj:
                    rev_adj[v] = {}
                rev_adj[v][u] = w
    else:
        rev_adj = None  # use same adjacency

    dist_f: Dict[int, float] = {source: 0.0}
    dist_b: Dict[int, float] = {target: 0.0}
    settled_f = set()
    settled_b = set()
    heap_f = [(0.0, source)]
    heap_b = [(0.0, target)]
    nodes_expanded = 0
    mu = INF  # best known s-t distance

    def _rev_neighbors(u):
        if rev_adj is not None:
            return rev_adj.get(u, {}).items()
        else:
            return graph.neighbors(u)

    while heap_f or heap_b:
        # Termination: both frontiers exceed best known distance
        df_min = heap_f[0][0] if heap_f else INF
        db_min = heap_b[0][0] if heap_b else INF
        if df_min + db_min >= mu:
            break

        # Expand forward
        if heap_f and df_min <= db_min:
            d, u = heapq.heappop(heap_f)
            if u not in settled_f:
                settled_f.add(u)
                nodes_expanded += 1
                for v, w in graph.neighbors(u):
                    nd = d + w
                    if nd < dist_f.get(v, INF):
                        dist_f[v] = nd
                        heapq.heappush(heap_f, (nd, v))
                        if v in dist_b:
                            mu = min(mu, nd + dist_b[v])
        # Expand backward
        elif heap_b:
            d, u = heapq.heappop(heap_b)
            if u not in settled_b:
                settled_b.add(u)
                nodes_expanded += 1
                for v, w in _rev_neighbors(u):
                    nd = d + w
                    if nd < dist_b.get(v, INF):
                        dist_b[v] = nd
                        heapq.heappush(heap_b, (nd, v))
                        if v in dist_f:
                            mu = min(mu, nd + dist_f[v])

    return mu, nodes_expanded


def dijkstra_p2p(graph: Graph, source: int, target: int) -> Tuple[float, int]:
    """Standard Dijkstra with early termination for point-to-point."""
    if source == target:
        return 0.0, 0
    dist: Dict[int, float] = {source: 0.0}
    settled = set()
    heap = [(0.0, source)]
    nodes_expanded = 0

    while heap:
        d, u = heapq.heappop(heap)
        if u in settled:
            continue
        settled.add(u)
        nodes_expanded += 1
        if u == target:
            return d, nodes_expanded
        for v, w in graph.neighbors(u):
            nd = d + w
            if nd < dist.get(v, INF):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return INF, nodes_expanded
