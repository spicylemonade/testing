"""BALT-H: Bidirectional ALT with Hub Acceleration.

Novel point-to-point shortest path algorithm combining:
1. Bidirectional Dijkstra search
2. Landmark-based lower bounds (ALT heuristic)
3. Hub-based early termination via high-degree vertices

Interface matches baseline implementations:
  preprocess(graph, k_landmarks, k_hubs) -> BALTHPreprocessing
  balth_query(graph, source, target, preprocessing) -> (distance, nodes_expanded)
"""

from __future__ import annotations

import heapq
import math
from typing import Dict, List, Optional, Tuple

from src.graph import Graph
from src.dijkstra import dijkstra_standard

INF = float("inf")


class BALTHPreprocessing:
    """Stores precomputed data for BALT-H queries.

    Attributes:
        landmark_dist_from: dist_from[i][v] = d(landmark_i, v)
        landmark_dist_to: dist_to[i][v] = d(v, landmark_i)
        landmarks: list of landmark vertex IDs
        hub_ids: list of hub vertex IDs
        hub_dist_from: hub_dist_from[i][v] = d(hub_i, v)
    """

    def __init__(self, graph: Graph, k_landmarks: int = 8, k_hubs: int = 8):
        self.landmarks: List[int] = []
        self.landmark_dist_from: List[Dict[int, float]] = []
        self.landmark_dist_to: List[Dict[int, float]] = []
        self.hub_ids: List[int] = []
        self.hub_dist_from: List[Dict[int, float]] = []

        nodes = graph.nodes()
        if not nodes:
            return

        # Phase 1: Select landmarks using farthest-first heuristic
        # This gives well-spread landmarks for better lower bounds.
        self.landmarks = self._select_landmarks(graph, nodes, k_landmarks)

        # Compute distances from/to each landmark
        for lm in self.landmarks:
            dist_from, _ = dijkstra_standard(graph, lm)
            self.landmark_dist_from.append(dist_from)
            # For undirected graphs, dist_to = dist_from
            if graph.directed:
                # Build reverse graph and run Dijkstra
                dist_to = self._reverse_dijkstra(graph, lm)
                self.landmark_dist_to.append(dist_to)
            else:
                self.landmark_dist_to.append(dist_from)

        # Phase 2: Identify hub vertices (highest-degree nodes)
        degree_list = [(graph.degree(v), v) for v in nodes]
        degree_list.sort(reverse=True)
        self.hub_ids = [v for _, v in degree_list[:k_hubs]]

        # Compute distances from each hub
        for hub in self.hub_ids:
            dist, _ = dijkstra_standard(graph, hub)
            self.hub_dist_from.append(dist)

    def _select_landmarks(self, graph: Graph, nodes: List[int],
                          k: int) -> List[int]:
        """Select landmarks using farthest-first strategy."""
        if len(nodes) <= k:
            return list(nodes)

        landmarks = [nodes[0]]  # start with first node
        dist_to_closest = {}
        # Initialize with distances from first landmark
        d, _ = dijkstra_standard(graph, nodes[0])
        for v in nodes:
            dist_to_closest[v] = d.get(v, INF)

        for _ in range(k - 1):
            # Pick the vertex farthest from all current landmarks
            farthest = max(nodes, key=lambda v: dist_to_closest.get(v, 0))
            landmarks.append(farthest)
            d, _ = dijkstra_standard(graph, farthest)
            for v in nodes:
                dist_to_closest[v] = min(dist_to_closest[v], d.get(v, INF))

        return landmarks

    def _reverse_dijkstra(self, graph: Graph, target: int) -> Dict[int, float]:
        """Dijkstra on reverse graph to get d(v, target) for all v."""
        # Build reverse adjacency
        rev = {}
        for u in graph.nodes():
            for v, w in graph.neighbors(u):
                if v not in rev:
                    rev[v] = {}
                rev[v][u] = w

        # Run Dijkstra from target on reverse graph
        dist = {target: 0.0}
        settled = set()
        heap = [(0.0, target)]
        while heap:
            d, u = heapq.heappop(heap)
            if u in settled:
                continue
            settled.add(u)
            for v, w in rev.get(u, {}).items():
                nd = d + w
                if nd < dist.get(v, INF):
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))
        return dist

    def lower_bound_forward(self, v: int, target: int) -> float:
        """Compute landmark lower bound for d(v, target): forward direction."""
        best = 0.0
        for i in range(len(self.landmarks)):
            d_lm_v = self.landmark_dist_from[i].get(v, INF)
            d_lm_t = self.landmark_dist_from[i].get(target, INF)
            d_v_lm = self.landmark_dist_to[i].get(v, INF)
            d_t_lm = self.landmark_dist_to[i].get(target, INF)
            if d_lm_v < INF and d_lm_t < INF:
                best = max(best, d_lm_t - d_lm_v)
            if d_v_lm < INF and d_t_lm < INF:
                best = max(best, d_v_lm - d_t_lm)
        return max(best, 0.0)

    def lower_bound_backward(self, v: int, source: int) -> float:
        """Compute landmark lower bound for d(source, v): backward direction."""
        best = 0.0
        for i in range(len(self.landmarks)):
            d_lm_s = self.landmark_dist_from[i].get(source, INF)
            d_lm_v = self.landmark_dist_from[i].get(v, INF)
            d_s_lm = self.landmark_dist_to[i].get(source, INF)
            d_v_lm = self.landmark_dist_to[i].get(v, INF)
            if d_lm_s < INF and d_lm_v < INF:
                best = max(best, d_lm_s - d_lm_v)
            if d_s_lm < INF and d_v_lm < INF:
                best = max(best, d_s_lm - d_v_lm)
        return max(best, 0.0)

    def hub_upper_bound(self, source: int, target: int) -> float:
        """Compute upper bound via hub vertices: min over hubs of d(h,s)+d(h,t).

        For undirected graphs, d(h,v) = d(v,h), so d(s,h)+d(h,t) can be
        computed from hub_dist_from.
        """
        mu = INF
        for i, hub in enumerate(self.hub_ids):
            d_h_s = self.hub_dist_from[i].get(source, INF)
            d_h_t = self.hub_dist_from[i].get(target, INF)
            if d_h_s < INF and d_h_t < INF:
                # For undirected: d(s,h) = d(h,s)
                mu = min(mu, d_h_s + d_h_t)
        return mu


def balth_query(graph: Graph, source: int, target: int,
                prep: BALTHPreprocessing) -> Tuple[float, int]:
    """BALT-H point-to-point shortest path query.

    Uses bidirectional Dijkstra (g-value ordered heaps) for correctness,
    with landmark lower bounds for pruning individual nodes, and hub
    upper bounds for early mu initialization.

    Returns (distance, nodes_expanded).
    """
    if source == target:
        return 0.0, 0

    # Initialize best known distance with hub upper bound
    mu = prep.hub_upper_bound(source, target)

    # Build reverse adjacency for directed graphs
    if graph.directed:
        rev_adj: Optional[Dict[int, Dict[int, float]]] = {}
        for u in graph.nodes():
            for v, w in graph.neighbors(u):
                if v not in rev_adj:
                    rev_adj[v] = {}
                rev_adj[v][u] = w
    else:
        rev_adj = None

    # Forward search: heap ordered by g-value (standard Dijkstra)
    dist_f: Dict[int, float] = {source: 0.0}
    settled_f: Dict[int, float] = {}
    heap_f = [(0.0, source)]  # (g_value, vertex)

    # Backward search: heap ordered by g-value
    dist_b: Dict[int, float] = {target: 0.0}
    settled_b: Dict[int, float] = {}
    heap_b = [(0.0, target)]

    nodes_expanded = 0

    def _rev_neighbors(u):
        if rev_adj is not None:
            return rev_adj.get(u, {}).items()
        return graph.neighbors(u)

    while heap_f or heap_b:
        # Termination: minimum g-values from both frontiers sum >= mu
        # This is correct because Dijkstra g-values are monotonically non-decreasing
        g_min_f = heap_f[0][0] if heap_f else INF
        g_min_b = heap_b[0][0] if heap_b else INF

        if g_min_f + g_min_b >= mu:
            break

        # Expand whichever frontier has smaller g-value
        if heap_f and (not heap_b or g_min_f <= g_min_b):
            g, u = heapq.heappop(heap_f)
            if u in settled_f:
                continue
            settled_f[u] = g
            nodes_expanded += 1

            # Check meeting with backward frontier
            if u in dist_b:
                mu = min(mu, g + dist_b[u])

            # Landmark pruning: if g + h_forward(u) >= mu, skip expansion
            lb = prep.lower_bound_forward(u, target)
            if g + lb >= mu:
                continue

            for v, w in graph.neighbors(u):
                ng = g + w
                if ng < dist_f.get(v, INF):
                    dist_f[v] = ng
                    heapq.heappush(heap_f, (ng, v))
                    # Check backward for meeting update
                    if v in dist_b:
                        mu = min(mu, ng + dist_b[v])
        else:
            g, u = heapq.heappop(heap_b)
            if u in settled_b:
                continue
            settled_b[u] = g
            nodes_expanded += 1

            # Check meeting with forward frontier
            if u in dist_f:
                mu = min(mu, g + dist_f[u])

            # Landmark pruning: if g + h_backward(u) >= mu, skip expansion
            lb = prep.lower_bound_backward(u, source)
            if g + lb >= mu:
                continue

            for v, w in _rev_neighbors(u):
                ng = g + w
                if ng < dist_b.get(v, INF):
                    dist_b[v] = ng
                    heapq.heappush(heap_b, (ng, v))
                    # Check forward for meeting update
                    if v in dist_f:
                        mu = min(mu, ng + dist_f[v])

    return mu, nodes_expanded


def balth_query_no_preprocessing(graph: Graph, source: int, target: int,
                                  k_landmarks: int = 4,
                                  k_hubs: int = 4) -> Tuple[float, int]:
    """Convenience wrapper that preprocesses and queries in one call."""
    prep = BALTHPreprocessing(graph, k_landmarks=k_landmarks, k_hubs=k_hubs)
    return balth_query(graph, source, target, prep)
