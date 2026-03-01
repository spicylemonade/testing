"""Unit tests for src/astar.py — at least 8 test cases."""

import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.graph import Graph
from src.astar import (
    astar,
    astar_euclidean,
    astar_landmark,
    euclidean_heuristic,
    LandmarkHeuristic,
)
from src.dijkstra import dijkstra_p2p

INF = float("inf")


class TestAStarEuclidean:
    def test_grid_simple(self):
        g = Graph.grid(5, 5, seed=42)
        d, expanded = astar_euclidean(g, 0, 24)
        d_ref, _ = dijkstra_p2p(g, 0, 24)
        assert abs(d - d_ref) < 1e-9

    def test_grid_same_node(self):
        g = Graph.grid(3, 3, seed=42)
        d, expanded = astar_euclidean(g, 0, 0)
        assert d == 0.0
        assert expanded == 0

    def test_grid_fewer_expansions_than_dijkstra(self):
        """A* with Euclidean heuristic should expand fewer nodes than Dijkstra."""
        g = Graph.grid(20, 20, seed=42)
        d_astar, exp_astar = astar_euclidean(g, 0, 399)
        d_dijk, exp_dijk = dijkstra_p2p(g, 0, 399)
        assert abs(d_astar - d_dijk) < 1e-9
        assert exp_astar <= exp_dijk

    def test_grid_various_targets(self):
        """Verify against Dijkstra on multiple random source-target pairs."""
        g = Graph.grid(10, 10, seed=42)
        rng = random.Random(42)
        nodes = g.nodes()
        for _ in range(5):
            s, t = rng.choice(nodes), rng.choice(nodes)
            d_astar, _ = astar_euclidean(g, s, t)
            d_dijk, _ = dijkstra_p2p(g, s, t)
            assert abs(d_astar - d_dijk) < 1e-9


class TestAStarLandmark:
    def test_simple_graph(self):
        g = Graph(directed=False)
        g.add_edge(0, 1, 1.0)
        g.add_edge(1, 2, 2.0)
        g.add_edge(0, 2, 5.0)
        d, _ = astar_landmark(g, 0, 2, landmarks=[0, 2])
        assert abs(d - 3.0) < 1e-9

    def test_against_dijkstra_erdos_renyi(self):
        """Verify on Erdős-Rényi graph."""
        g = Graph.erdos_renyi(100, 0.1, seed=42, directed=False)
        nodes = g.nodes()
        landmarks = [nodes[i * len(nodes) // 4] for i in range(4)]
        lm = LandmarkHeuristic(g, landmarks)

        rng = random.Random(42)
        for _ in range(10):
            s, t = rng.choice(nodes), rng.choice(nodes)
            d_astar, _ = astar_landmark(g, s, t, precomputed=lm)
            d_dijk, _ = dijkstra_p2p(g, s, t)
            assert abs(d_astar - d_dijk) < 1e-9

    def test_unreachable(self):
        g = Graph(directed=True)
        g.add_node(0)
        g.add_node(1)
        d, _ = astar_landmark(g, 0, 1, landmarks=[0])
        assert d == INF

    def test_grid_with_landmarks(self):
        """Verify on grid graph with corner landmarks."""
        g = Graph.grid(10, 10, seed=42)
        landmarks = [0, 9, 90, 99]  # four corners
        lm = LandmarkHeuristic(g, landmarks)
        rng = random.Random(42)
        nodes = g.nodes()
        for _ in range(5):
            s, t = rng.choice(nodes), rng.choice(nodes)
            d_astar, _ = astar_landmark(g, s, t, precomputed=lm)
            d_dijk, _ = dijkstra_p2p(g, s, t)
            assert abs(d_astar - d_dijk) < 1e-9
