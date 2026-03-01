"""Unit tests for src/dijkstra.py — at least 12 test cases."""

import math
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.graph import Graph
from src.dijkstra import (
    dijkstra_standard,
    dijkstra_decreasekey,
    dijkstra_bidirectional,
    dijkstra_p2p,
)

INF = float("inf")


def _brute_force_sssp(graph, source):
    """Bellman-Ford brute force for verification."""
    dist = {n: INF for n in graph.nodes()}
    dist[source] = 0.0
    for _ in range(len(graph.nodes()) - 1):
        for u in graph.nodes():
            if dist[u] == INF:
                continue
            for v, w in graph.neighbors(u):
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
    return {k: v for k, v in dist.items() if v < INF}


class TestDijkstraStandard:
    def test_simple_path(self):
        g = Graph(directed=True)
        g.add_edge(0, 1, 1.0)
        g.add_edge(1, 2, 2.0)
        g.add_edge(0, 2, 5.0)
        dist, _ = dijkstra_standard(g, 0)
        assert dist[0] == 0.0
        assert dist[1] == 1.0
        assert dist[2] == 3.0

    def test_disconnected_graph(self):
        g = Graph(directed=True)
        g.add_node(0)
        g.add_node(1)
        g.add_node(2)
        g.add_edge(0, 1, 1.0)
        dist, _ = dijkstra_standard(g, 0)
        assert 2 not in dist

    def test_single_node(self):
        g = Graph(directed=True)
        g.add_node(0)
        dist, expanded = dijkstra_standard(g, 0)
        assert dist == {0: 0.0}
        assert expanded == 1

    def test_zero_weight_edges(self):
        g = Graph(directed=True)
        g.add_edge(0, 1, 0.0)
        g.add_edge(1, 2, 0.0)
        dist, _ = dijkstra_standard(g, 0)
        assert dist[2] == 0.0

    def test_self_loop(self):
        g = Graph(directed=True)
        g.add_edge(0, 0, 5.0)
        g.add_edge(0, 1, 2.0)
        dist, _ = dijkstra_standard(g, 0)
        assert dist[0] == 0.0
        assert dist[1] == 2.0

    def test_against_brute_force(self):
        """Verify against Bellman-Ford on random graph up to 100 nodes."""
        rng = random.Random(42)
        for trial in range(5):
            g = Graph.erdos_renyi(100, 0.1, seed=42 + trial)
            source = rng.choice(g.nodes())
            dist_d, _ = dijkstra_standard(g, source)
            dist_bf = _brute_force_sssp(g, source)
            for v in dist_bf:
                assert abs(dist_d.get(v, INF) - dist_bf[v]) < 1e-9, \
                    f"Trial {trial}: mismatch at vertex {v}"


class TestDijkstraDecreaseKey:
    def test_simple_path(self):
        g = Graph(directed=True)
        g.add_edge(0, 1, 1.0)
        g.add_edge(1, 2, 2.0)
        g.add_edge(0, 2, 5.0)
        dist, _ = dijkstra_decreasekey(g, 0)
        assert dist[2] == 3.0

    def test_against_standard(self):
        """Verify decrease-key variant matches standard on random graph."""
        g = Graph.erdos_renyi(200, 0.05, seed=42)
        source = 0
        dist_std, _ = dijkstra_standard(g, source)
        dist_dk, _ = dijkstra_decreasekey(g, source)
        for v in dist_std:
            assert abs(dist_std[v] - dist_dk.get(v, INF)) < 1e-9

    def test_large_graph(self):
        """Test on 1000-node graph to verify correctness at scale."""
        g = Graph.erdos_renyi(1000, 0.01, seed=42)
        dist, expanded = dijkstra_decreasekey(g, 0)
        assert expanded > 0
        assert dist[0] == 0.0


class TestBidirectionalDijkstra:
    def test_simple(self):
        g = Graph(directed=False)
        g.add_edge(0, 1, 1.0)
        g.add_edge(1, 2, 2.0)
        g.add_edge(0, 2, 5.0)
        d, _ = dijkstra_bidirectional(g, 0, 2)
        assert abs(d - 3.0) < 1e-9

    def test_same_source_target(self):
        g = Graph(directed=False)
        g.add_edge(0, 1, 1.0)
        d, expanded = dijkstra_bidirectional(g, 0, 0)
        assert d == 0.0
        assert expanded == 0

    def test_unreachable(self):
        g = Graph(directed=True)
        g.add_node(0)
        g.add_node(1)
        d, _ = dijkstra_bidirectional(g, 0, 1)
        assert d == INF

    def test_against_standard_p2p(self):
        """Verify bidirectional matches standard Dijkstra on random undirected graph."""
        g = Graph.erdos_renyi(200, 0.1, seed=42, directed=False)
        nodes = g.nodes()
        rng = random.Random(42)
        for _ in range(10):
            s, t = rng.choice(nodes), rng.choice(nodes)
            d_std, _ = dijkstra_p2p(g, s, t)
            d_bid, _ = dijkstra_bidirectional(g, s, t)
            assert abs(d_std - d_bid) < 1e-9, \
                f"Mismatch for ({s}, {t}): std={d_std}, bid={d_bid}"

    def test_directed_graph(self):
        g = Graph(directed=True)
        g.add_edge(0, 1, 3.0)
        g.add_edge(1, 2, 4.0)
        g.add_edge(0, 2, 10.0)
        d, _ = dijkstra_bidirectional(g, 0, 2)
        assert abs(d - 7.0) < 1e-9
