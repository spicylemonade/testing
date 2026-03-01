"""Comprehensive tests for HiBRA (novel algorithm).

Tests correctness against Dijkstra on diverse graph instances.
20+ test cases covering all graph families, edge cases, and stress tests.
"""

import random
import math
import pytest
from src.graph import Graph
from src.novel_algorithm import hibra
from src.dijkstra import dijkstra_binary, dijkstra_fibonacci
from src.graph_generators import (
    gen_adversarial_dijkstra, gen_sparse_erdos_renyi, gen_dense_random,
    gen_layered_dag, gen_grid, gen_planted_spt
)

INF = float('inf')
TOL = 1e-9


def assert_distances_match(d1, d2, n):
    """Assert two distance arrays match within tolerance."""
    for i in range(n):
        if d1[i] == INF and d2[i] == INF:
            continue
        assert abs(d1[i] - d2[i]) < TOL, f"Mismatch at vertex {i}: {d1[i]} vs {d2[i]}"


# === Test 1-6: All six graph families ===

class TestGraphFamilies:
    """Test correctness on all 6 graph families from item_009."""

    def test_adversarial(self):
        g, _ = gen_adversarial_dijkstra(500, seed=42)
        d1, _, _ = dijkstra_binary(g, 0)
        d2, _, _ = hibra(g, 0)
        assert_distances_match(d1, d2, g.n)

    def test_sparse_erdos_renyi(self):
        g, _ = gen_sparse_erdos_renyi(500, seed=42)
        d1, _, _ = dijkstra_binary(g, 0)
        d2, _, _ = hibra(g, 0)
        assert_distances_match(d1, d2, g.n)

    def test_dense_random(self):
        g, _ = gen_dense_random(200, seed=42)
        d1, _, _ = dijkstra_binary(g, 0)
        d2, _, _ = hibra(g, 0)
        assert_distances_match(d1, d2, g.n)

    def test_layered_dag(self):
        g, _ = gen_layered_dag(500, seed=42)
        d1, _, _ = dijkstra_binary(g, 0)
        d2, _, _ = hibra(g, 0)
        assert_distances_match(d1, d2, g.n)

    def test_grid(self):
        g, _ = gen_grid(500, seed=42)
        d1, _, _ = dijkstra_binary(g, 0)
        d2, _, _ = hibra(g, 0)
        assert_distances_match(d1, d2, g.n)

    def test_planted_spt(self):
        g, _ = gen_planted_spt(500, seed=42)
        d1, _, _ = dijkstra_binary(g, 0)
        d2, _, _ = hibra(g, 0)
        assert_distances_match(d1, d2, g.n)


# === Tests 7-10: Small exhaustive tests (n <= 8) ===

class TestSmallGraphs:
    """Exhaustive tests on small graphs."""

    def test_single_vertex(self):
        g = Graph(1)
        d, _, _ = hibra(g, 0)
        assert d[0] == 0

    def test_two_vertices(self):
        g = Graph(2)
        g.add_edge(0, 1, 5.0)
        d, _, _ = hibra(g, 0)
        assert d[0] == 0
        assert d[1] == 5.0

    def test_triangle(self):
        g = Graph(3)
        g.add_edge(0, 1, 1.0)
        g.add_edge(1, 2, 2.0)
        g.add_edge(0, 2, 4.0)
        d, _, _ = hibra(g, 0)
        assert d[0] == 0
        assert d[1] == 1.0
        assert d[2] == 3.0  # 0->1->2

    def test_all_small_graphs(self):
        """Test on random small graphs with n=3..8."""
        rng = random.Random(42)
        for n in range(3, 9):
            for _ in range(20):
                g = Graph(n)
                # Add random edges
                num_edges = rng.randint(n - 1, n * (n - 1) // 2)
                for _ in range(num_edges):
                    u = rng.randint(0, n - 1)
                    v = rng.randint(0, n - 1)
                    if u != v:
                        g.add_edge(u, v, rng.uniform(0.1, 100))
                d1, _, _ = dijkstra_binary(g, 0)
                d2, _, _ = hibra(g, 0)
                assert_distances_match(d1, d2, n)


# === Tests 11-13: Medium random tests (n=100-1000, 100+ instances) ===

class TestMediumRandom:
    """Medium random tests: 100+ instances at n=100-1000."""

    def test_random_medium_sparse(self):
        for seed in range(100):
            g, _ = gen_sparse_erdos_renyi(200, seed=seed)
            d1, _, _ = dijkstra_binary(g, 0)
            d2, _, _ = hibra(g, 0)
            assert_distances_match(d1, d2, g.n)

    def test_random_medium_dense(self):
        for seed in range(20):
            g, _ = gen_dense_random(100, seed=seed)
            d1, _, _ = dijkstra_binary(g, 0)
            d2, _, _ = hibra(g, 0)
            assert_distances_match(d1, d2, g.n)

    def test_random_medium_grid(self):
        for seed in range(50):
            g, _ = gen_grid(200, seed=seed)
            d1, _, _ = dijkstra_binary(g, 0)
            d2, _, _ = hibra(g, 0)
            assert_distances_match(d1, d2, g.n)


# === Tests 14-16: Large stress tests (n=10^4-10^5) ===

class TestLargeStress:
    """Large stress tests: n=10000-100000."""

    def test_large_sparse(self):
        for seed in range(5):
            g, _ = gen_sparse_erdos_renyi(10000, seed=seed)
            d1, _, _ = dijkstra_binary(g, 0)
            d2, _, _ = hibra(g, 0)
            assert_distances_match(d1, d2, g.n)

    def test_large_adversarial(self):
        for seed in range(5):
            g, _ = gen_adversarial_dijkstra(10000, seed=seed)
            d1, _, _ = dijkstra_binary(g, 0)
            d2, _, _ = hibra(g, 0)
            assert_distances_match(d1, d2, g.n)

    def test_large_planted(self):
        for seed in range(3):
            g, _ = gen_planted_spt(50000, seed=seed)
            d1, _, _ = dijkstra_binary(g, 0)
            d2, _, _ = hibra(g, 0)
            assert_distances_match(d1, d2, g.n)


# === Tests 17-21: Edge cases ===

class TestEdgeCases:
    """Edge case tests."""

    def test_empty_graph(self):
        g = Graph(0)
        d, _, _ = hibra(g, 0)
        assert d == []

    def test_disconnected_graph(self):
        g = Graph(5)
        g.add_edge(0, 1, 1.0)
        g.add_edge(1, 2, 2.0)
        # vertices 3, 4 unreachable
        d, _, _ = hibra(g, 0)
        assert d[0] == 0
        assert d[1] == 1.0
        assert d[2] == 3.0
        assert d[3] == INF
        assert d[4] == INF

    def test_single_edge(self):
        g = Graph(2)
        g.add_edge(0, 1, 42.0)
        d, _, _ = hibra(g, 0)
        assert d[0] == 0
        assert d[1] == 42.0

    def test_complete_graph(self):
        rng = random.Random(42)
        n = 50
        g = Graph(n)
        for i in range(n):
            for j in range(n):
                if i != j:
                    g.add_edge(i, j, rng.uniform(1, 100))
        d1, _, _ = dijkstra_binary(g, 0)
        d2, _, _ = hibra(g, 0)
        assert_distances_match(d1, d2, n)

    def test_zero_weight_edges(self):
        g = Graph(4)
        g.add_edge(0, 1, 0)
        g.add_edge(1, 2, 0)
        g.add_edge(0, 3, 1)
        g.add_edge(3, 2, 0)
        d, _, _ = hibra(g, 0)
        assert d[0] == 0
        assert d[1] == 0
        assert d[2] == 0
        assert d[3] == 1


# === Test 22: Operation counting ===

class TestOperationCounting:
    """Verify operation counter tracks ops correctly."""

    def test_counter_populated(self):
        g, _ = gen_sparse_erdos_renyi(100, seed=42)
        d, counter, expanded = hibra(g, 0)
        assert counter.comparisons > 0
        assert counter.additions > 0
        assert counter.extract_mins > 0
        assert counter.total_ops > 0
        assert expanded > 0
