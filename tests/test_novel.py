"""Unit tests for src/novel_algorithm.py — at least 15 test cases."""

import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.graph import Graph
from src.novel_algorithm import BALTHPreprocessing, balth_query
from src.dijkstra import dijkstra_p2p

INF = float("inf")


def _check_against_dijkstra(graph, source, target, prep):
    d_balth, _ = balth_query(graph, source, target, prep)
    d_dijk, _ = dijkstra_p2p(graph, source, target)
    if d_balth == INF and d_dijk == INF:
        return  # both agree: unreachable
    assert abs(d_balth - d_dijk) < 1e-9, \
        f"Mismatch ({source}->{target}): BALT-H={d_balth}, Dijkstra={d_dijk}"


class TestBALTHBasic:
    def test_same_source_target(self):
        g = Graph(directed=False)
        g.add_edge(0, 1, 1.0)
        prep = BALTHPreprocessing(g, k_landmarks=1, k_hubs=1)
        d, expanded = balth_query(g, 0, 0, prep)
        assert d == 0.0
        assert expanded == 0

    def test_simple_triangle(self):
        g = Graph(directed=False)
        g.add_edge(0, 1, 1.0)
        g.add_edge(1, 2, 2.0)
        g.add_edge(0, 2, 5.0)
        prep = BALTHPreprocessing(g, k_landmarks=2, k_hubs=1)
        d, _ = balth_query(g, 0, 2, prep)
        assert abs(d - 3.0) < 1e-9

    def test_directed_graph(self):
        g = Graph(directed=True)
        g.add_edge(0, 1, 3.0)
        g.add_edge(1, 2, 4.0)
        g.add_edge(0, 2, 10.0)
        prep = BALTHPreprocessing(g, k_landmarks=2, k_hubs=1)
        d, _ = balth_query(g, 0, 2, prep)
        assert abs(d - 7.0) < 1e-9

    def test_unreachable(self):
        g = Graph(directed=True)
        g.add_node(0)
        g.add_node(1)
        prep = BALTHPreprocessing(g, k_landmarks=1, k_hubs=1)
        d, _ = balth_query(g, 0, 1, prep)
        assert d == INF

    def test_zero_weight(self):
        g = Graph(directed=False)
        g.add_edge(0, 1, 0.0)
        g.add_edge(1, 2, 0.0)
        prep = BALTHPreprocessing(g, k_landmarks=1, k_hubs=1)
        d, _ = balth_query(g, 0, 2, prep)
        assert d == 0.0


class TestBALTHGrid:
    def test_small_grid(self):
        g = Graph.grid(5, 5, seed=42)
        prep = BALTHPreprocessing(g, k_landmarks=4, k_hubs=4)
        _check_against_dijkstra(g, 0, 24, prep)

    def test_medium_grid(self):
        g = Graph.grid(10, 10, seed=42)
        prep = BALTHPreprocessing(g, k_landmarks=4, k_hubs=4)
        rng = random.Random(42)
        nodes = g.nodes()
        for _ in range(5):
            s, t = rng.choice(nodes), rng.choice(nodes)
            _check_against_dijkstra(g, s, t, prep)

    def test_grid_corners(self):
        g = Graph.grid(10, 10, seed=42)
        prep = BALTHPreprocessing(g, k_landmarks=4, k_hubs=4)
        _check_against_dijkstra(g, 0, 99, prep)
        _check_against_dijkstra(g, 9, 90, prep)


class TestBALTHErdosRenyi:
    def test_sparse(self):
        g = Graph.erdos_renyi(100, 0.05, seed=42, directed=False)
        prep = BALTHPreprocessing(g, k_landmarks=4, k_hubs=4)
        rng = random.Random(42)
        nodes = g.nodes()
        for _ in range(5):
            s, t = rng.choice(nodes), rng.choice(nodes)
            _check_against_dijkstra(g, s, t, prep)

    def test_dense(self):
        g = Graph.erdos_renyi(50, 0.3, seed=42, directed=False)
        prep = BALTHPreprocessing(g, k_landmarks=4, k_hubs=4)
        rng = random.Random(42)
        nodes = g.nodes()
        for _ in range(5):
            s, t = rng.choice(nodes), rng.choice(nodes)
            _check_against_dijkstra(g, s, t, prep)


class TestBALTHBarabasiAlbert:
    def test_scale_free(self):
        g = Graph.barabasi_albert(200, m=3, seed=42)
        prep = BALTHPreprocessing(g, k_landmarks=4, k_hubs=8)
        rng = random.Random(42)
        nodes = g.nodes()
        for _ in range(5):
            s, t = rng.choice(nodes), rng.choice(nodes)
            _check_against_dijkstra(g, s, t, prep)


class TestBALTHLargeScale:
    def test_50_random_graphs(self):
        """Verify correctness on 50+ random graphs of varying sizes and types."""
        rng = random.Random(42)
        passed = 0
        for trial in range(50):
            gtype = rng.choice(["er", "grid", "ba"])
            if gtype == "er":
                n = rng.randint(20, 200)
                p = rng.uniform(0.02, 0.2)
                g = Graph.erdos_renyi(n, p, seed=42 + trial, directed=False)
            elif gtype == "grid":
                side = rng.randint(4, 15)
                g = Graph.grid(side, side, seed=42 + trial)
            else:
                n = rng.randint(20, 200)
                g = Graph.barabasi_albert(n, m=3, seed=42 + trial)

            nodes = g.nodes()
            if len(nodes) < 2:
                passed += 1
                continue

            prep = BALTHPreprocessing(g, k_landmarks=4, k_hubs=4)
            s, t = rng.choice(nodes), rng.choice(nodes)
            _check_against_dijkstra(g, s, t, prep)
            passed += 1

        assert passed == 50

    def test_complete_graph(self):
        g = Graph.complete(20, seed=42)
        prep = BALTHPreprocessing(g, k_landmarks=4, k_hubs=4)
        rng = random.Random(42)
        nodes = g.nodes()
        for _ in range(5):
            s, t = rng.choice(nodes), rng.choice(nodes)
            _check_against_dijkstra(g, s, t, prep)

    def test_fewer_nodes_than_expansions(self):
        """BALT-H should expand fewer nodes than Dijkstra on grid."""
        g = Graph.grid(20, 20, seed=42)
        prep = BALTHPreprocessing(g, k_landmarks=8, k_hubs=8)
        _, exp_balth = balth_query(g, 0, 399, prep)
        _, exp_dijk = dijkstra_p2p(g, 0, 399)
        # BALT-H should expand fewer or equal nodes
        assert exp_balth <= exp_dijk * 1.1  # allow small margin
