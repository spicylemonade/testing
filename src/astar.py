"""A* search with pluggable admissible heuristics.

Provides two admissible heuristics:
1. Euclidean distance (for graphs with coordinates)
2. Landmark-based lower bounds (ALT-style, triangle inequality)

Returns (distance, nodes_expanded) for point-to-point queries.
"""

from __future__ import annotations

import heapq
import math
from typing import Callable, Dict, List, Optional, Tuple

from src.graph import Graph
from src.dijkstra import dijkstra_standard

INF = float("inf")

# Type alias for heuristic function: h(node) -> lower_bound_to_target
HeuristicFn = Callable[[int], float]


def astar(graph: Graph, source: int, target: int,
          heuristic: HeuristicFn) -> Tuple[float, int]:
    """A* search with a user-supplied admissible heuristic.

    Args:
        graph: the input graph
        source: source vertex
        target: target vertex
        heuristic: function h(v) returning admissible lower bound on d(v, target)

    Returns:
        (shortest_distance, nodes_expanded)
    """
    if source == target:
        return 0.0, 0

    g_score: Dict[int, float] = {source: 0.0}
    settled = set()
    # heap entries: (f_score, g_score, vertex)
    heap = [(heuristic(source), 0.0, source)]
    nodes_expanded = 0

    while heap:
        f, g, u = heapq.heappop(heap)
        if u in settled:
            continue
        settled.add(u)
        nodes_expanded += 1

        if u == target:
            return g, nodes_expanded

        for v, w in graph.neighbors(u):
            ng = g + w
            if ng < g_score.get(v, INF):
                g_score[v] = ng
                f_new = ng + heuristic(v)
                heapq.heappush(heap, (f_new, ng, v))

    return INF, nodes_expanded


# ---- Heuristic 1: Euclidean distance ----

def euclidean_heuristic(graph: Graph, target: int) -> HeuristicFn:
    """Create Euclidean-distance heuristic for graphs with coords.

    Admissible when edge weights >= Euclidean distances (which holds
    for grid graphs with weights >= 1.0).
    """
    tx, ty = graph.coords.get(target, (0.0, 0.0))

    def h(v: int) -> float:
        if v not in graph.coords:
            return 0.0
        vx, vy = graph.coords[v]
        return math.sqrt((vx - tx) ** 2 + (vy - ty) ** 2)

    return h


# ---- Heuristic 2: Landmark-based (ALT) ----

class LandmarkHeuristic:
    """Landmark-based heuristic using triangle inequality.

    Precomputes distances from a set of landmark vertices to all others.
    For any landmark L: d(v, t) >= |d(L, t) - d(L, v)|
    The best lower bound across all landmarks is used.
    """

    def __init__(self, graph: Graph, landmarks: List[int]):
        self.landmark_dists: List[Dict[int, float]] = []
        for lm in landmarks:
            dist, _ = dijkstra_standard(graph, lm)
            self.landmark_dists.append(dist)

    def make_heuristic(self, target: int) -> HeuristicFn:
        """Create a heuristic function for a given target vertex."""
        target_dists = [ld.get(target, INF) for ld in self.landmark_dists]

        def h(v: int) -> float:
            best = 0.0
            for i, ld in enumerate(self.landmark_dists):
                dv = ld.get(v, INF)
                dt = target_dists[i]
                if dv < INF and dt < INF:
                    lb = abs(dt - dv)
                    if lb > best:
                        best = lb
            return best

        return h


def astar_euclidean(graph: Graph, source: int, target: int) -> Tuple[float, int]:
    """A* with Euclidean distance heuristic."""
    h = euclidean_heuristic(graph, target)
    return astar(graph, source, target, h)


def astar_landmark(graph: Graph, source: int, target: int,
                   landmarks: Optional[List[int]] = None,
                   precomputed: Optional[LandmarkHeuristic] = None) -> Tuple[float, int]:
    """A* with landmark-based (ALT) heuristic.

    If precomputed is provided, uses it. Otherwise, computes landmark
    distances on the fly using the given landmarks (or defaults to
    4 evenly-spaced vertex IDs).
    """
    if precomputed is None:
        if landmarks is None:
            nodes = graph.nodes()
            n = len(nodes)
            landmarks = [nodes[i * n // 4] for i in range(4)]
        precomputed = LandmarkHeuristic(graph, landmarks)

    h = precomputed.make_heuristic(target)
    return astar(graph, source, target, h)
