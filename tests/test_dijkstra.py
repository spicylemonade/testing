"""Tests for Dijkstra's algorithm with Fibonacci heap and binary heap."""

import math
import pytest
from src.graph import Graph
from src.dijkstra import dijkstra_fibonacci, dijkstra_binary
from src.op_counter import OpCounter

INF = float('inf')


def make_simple_graph():
    """Simple 5-node directed graph."""
    g = Graph(5)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 3, 5)
    g.add_edge(1, 2, 1)
    g.add_edge(1, 3, 2)
    g.add_edge(2, 4, 4)
    g.add_edge(3, 1, 3)
    g.add_edge(3, 2, 9)
    g.add_edge(3, 4, 2)
    g.add_edge(4, 0, 7)
    g.add_edge(4, 2, 6)
    return g


def make_linear_graph(n):
    """Linear chain: 0 -> 1 -> 2 -> ... -> n-1."""
    g = Graph(n)
    for i in range(n - 1):
        g.add_edge(i, i + 1, 1.0)
    return g


def make_complete_graph(n):
    """Complete directed graph with random-ish weights."""
    import random
    rng = random.Random(42)
    g = Graph(n)
    for i in range(n):
        for j in range(n):
            if i != j:
                g.add_edge(i, j, rng.uniform(1, 100))
    return g


class TestDijkstraFibonacci:
    def test_simple_graph(self):
        g = make_simple_graph()
        dist, counter, expanded = dijkstra_fibonacci(g, 0)
        assert dist[0] == 0
        assert dist[1] == 8  # 0->3->1
        assert dist[2] == 9  # 0->3->1->2
        assert dist[3] == 5  # 0->3
        assert dist[4] == 7  # 0->3->4

    def test_single_vertex(self):
        g = Graph(1)
        dist, counter, expanded = dijkstra_fibonacci(g, 0)
        assert dist[0] == 0

    def test_disconnected(self):
        g = Graph(3)
        g.add_edge(0, 1, 5)
        dist, counter, expanded = dijkstra_fibonacci(g, 0)
        assert dist[0] == 0
        assert dist[1] == 5
        assert dist[2] == INF

    def test_linear_graph(self):
        g = make_linear_graph(10)
        dist, counter, expanded = dijkstra_fibonacci(g, 0)
        for i in range(10):
            assert abs(dist[i] - i) < 1e-9

    def test_zero_weight_edges(self):
        g = Graph(3)
        g.add_edge(0, 1, 0)
        g.add_edge(1, 2, 0)
        dist, counter, expanded = dijkstra_fibonacci(g, 0)
        assert dist[0] == 0
        assert dist[1] == 0
        assert dist[2] == 0

    def test_parallel_edges(self):
        g = Graph(2)
        g.add_edge(0, 1, 10)
        g.add_edge(0, 1, 5)
        g.add_edge(0, 1, 7)
        dist, counter, expanded = dijkstra_fibonacci(g, 0)
        assert dist[1] == 5

    def test_counter_tracks_ops(self):
        g = make_simple_graph()
        dist, counter, expanded = dijkstra_fibonacci(g, 0)
        assert counter.comparisons > 0
        assert counter.additions > 0
        assert counter.extract_mins > 0
        assert counter.total_ops > 0

    def test_complete_graph(self):
        g = make_complete_graph(20)
        dist_fib, _, _ = dijkstra_fibonacci(g, 0)
        dist_bin, _, _ = dijkstra_binary(g, 0)
        for i in range(20):
            assert abs(dist_fib[i] - dist_bin[i]) < 1e-9

    def test_large_linear(self):
        g = make_linear_graph(1000)
        dist, counter, expanded = dijkstra_fibonacci(g, 0)
        assert abs(dist[999] - 999) < 1e-9
        assert expanded == 1000


class TestDijkstraBinary:
    def test_simple_graph(self):
        g = make_simple_graph()
        dist, counter, expanded = dijkstra_binary(g, 0)
        assert dist[0] == 0
        assert dist[1] == 8
        assert dist[2] == 9
        assert dist[3] == 5
        assert dist[4] == 7

    def test_single_vertex(self):
        g = Graph(1)
        dist, counter, expanded = dijkstra_binary(g, 0)
        assert dist[0] == 0

    def test_disconnected(self):
        g = Graph(3)
        g.add_edge(0, 1, 5)
        dist, counter, expanded = dijkstra_binary(g, 0)
        assert dist[0] == 0
        assert dist[1] == 5
        assert dist[2] == INF


class TestFibVsBinaryAgreement:
    """Verify both implementations produce identical results."""

    def test_agreement_simple(self):
        g = make_simple_graph()
        d1, _, _ = dijkstra_fibonacci(g, 0)
        d2, _, _ = dijkstra_binary(g, 0)
        for i in range(g.n):
            assert abs(d1[i] - d2[i]) < 1e-9

    def test_agreement_linear(self):
        g = make_linear_graph(100)
        d1, _, _ = dijkstra_fibonacci(g, 0)
        d2, _, _ = dijkstra_binary(g, 0)
        for i in range(g.n):
            assert abs(d1[i] - d2[i]) < 1e-9

    def test_agreement_complete(self):
        g = make_complete_graph(50)
        d1, _, _ = dijkstra_fibonacci(g, 0)
        d2, _, _ = dijkstra_binary(g, 0)
        for i in range(g.n):
            assert abs(d1[i] - d2[i]) < 1e-9
