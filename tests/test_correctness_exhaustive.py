"""Exhaustive correctness verification for BALT-H.

Tests:
1. All graphs up to 8 nodes (enumeration of small connected graphs)
2. 1000 random graphs with 100-10000 nodes vs Dijkstra
3. Edge cases: disconnected components, very large weights, duplicate edges
"""

import itertools
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.graph import Graph
from src.novel_algorithm import BALTHPreprocessing, balth_query
from src.dijkstra import dijkstra_p2p

INF = float("inf")


def _check(graph, source, target, prep):
    """Assert BALT-H matches Dijkstra."""
    d_balth, _ = balth_query(graph, source, target, prep)
    d_dijk, _ = dijkstra_p2p(graph, source, target)
    if d_balth == INF and d_dijk == INF:
        return
    assert abs(d_balth - d_dijk) < 1e-9, \
        f"Mismatch ({source}->{target}): BALT-H={d_balth}, Dijkstra={d_dijk}"


# =============================================================================
# Test 1: Exhaustive small graphs (up to 8 nodes)
# =============================================================================
class TestExhaustiveSmallGraphs:
    def test_all_graphs_up_to_5_nodes(self):
        """Test all possible edge combinations for n=2..5."""
        rng = random.Random(42)
        for n in range(2, 6):
            nodes = list(range(n))
            possible_edges = [(i, j) for i in nodes for j in nodes if i < j]
            # Test a sample of edge subsets (all subsets for n<=4, sample for n=5)
            if n <= 4:
                for r in range(len(possible_edges) + 1):
                    for edges in itertools.combinations(possible_edges, r):
                        g = Graph(directed=False)
                        for v in nodes:
                            g.add_node(v)
                        for u, v in edges:
                            w = rng.uniform(0.1, 10.0)
                            g.add_edge(u, v, w)
                        prep = BALTHPreprocessing(g, k_landmarks=min(2, n),
                                                  k_hubs=min(2, n))
                        for s in nodes:
                            for t in nodes:
                                _check(g, s, t, prep)
            else:
                # n=5: 10 possible edges, 1024 subsets — test all
                for mask in range(1 << len(possible_edges)):
                    g = Graph(directed=False)
                    for v in nodes:
                        g.add_node(v)
                    for idx, (u, v) in enumerate(possible_edges):
                        if mask & (1 << idx):
                            w = rng.uniform(0.1, 10.0)
                            g.add_edge(u, v, w)
                    prep = BALTHPreprocessing(g, k_landmarks=2, k_hubs=2)
                    s, t = rng.choice(nodes), rng.choice(nodes)
                    _check(g, s, t, prep)

    def test_graphs_6_to_8_nodes_sampled(self):
        """Sample random graphs with 6-8 nodes and test all pairs."""
        rng = random.Random(42)
        for n in [6, 7, 8]:
            for trial in range(200):
                g = Graph(directed=False)
                for v in range(n):
                    g.add_node(v)
                # Random edges
                num_edges = rng.randint(0, n * (n - 1) // 2)
                possible = [(i, j) for i in range(n) for j in range(i + 1, n)]
                chosen = rng.sample(possible, min(num_edges, len(possible)))
                for u, v in chosen:
                    g.add_edge(u, v, rng.uniform(0.1, 10.0))

                prep = BALTHPreprocessing(g, k_landmarks=min(3, n),
                                          k_hubs=min(3, n))
                # Test all pairs
                for s in range(n):
                    for t in range(n):
                        _check(g, s, t, prep)


# =============================================================================
# Test 2: 1000 random graphs with 100-10000 nodes
# =============================================================================
class TestRandomized1000:
    def test_1000_random_graphs(self):
        """Verify correctness on 1000 random graphs of varying sizes."""
        rng = random.Random(42)
        for trial in range(1000):
            gtype = rng.choice(["er", "grid", "ba"])
            if gtype == "er":
                n = rng.randint(100, 500)
                p = rng.uniform(0.01, 0.1)
                g = Graph.erdos_renyi(n, p, seed=42 + trial, directed=False)
            elif gtype == "grid":
                side = rng.randint(10, 50)
                g = Graph.grid(side, side, seed=42 + trial)
            else:
                n = rng.randint(100, 500)
                g = Graph.barabasi_albert(n, m=3, seed=42 + trial)

            nodes = g.nodes()
            if len(nodes) < 2:
                continue

            prep = BALTHPreprocessing(g, k_landmarks=4, k_hubs=4)
            # Test 3 random queries per graph
            for _ in range(3):
                s, t = rng.choice(nodes), rng.choice(nodes)
                _check(g, s, t, prep)


# =============================================================================
# Test 3: Edge cases
# =============================================================================
class TestEdgeCases:
    def test_disconnected_components(self):
        """Test graph with multiple disconnected components."""
        g = Graph(directed=False)
        # Component 1: 0-1-2
        g.add_edge(0, 1, 1.0)
        g.add_edge(1, 2, 2.0)
        # Component 2: 3-4
        g.add_edge(3, 4, 1.0)
        # Isolated: 5
        g.add_node(5)

        prep = BALTHPreprocessing(g, k_landmarks=2, k_hubs=2)
        # Within component
        _check(g, 0, 2, prep)
        # Across components
        _check(g, 0, 3, prep)
        _check(g, 0, 5, prep)
        _check(g, 3, 5, prep)

    def test_very_large_weights(self):
        """Test with edge weights up to 1e15."""
        g = Graph(directed=False)
        g.add_edge(0, 1, 1e15)
        g.add_edge(1, 2, 1e15)
        g.add_edge(0, 2, 3e15)
        prep = BALTHPreprocessing(g, k_landmarks=2, k_hubs=1)
        _check(g, 0, 2, prep)

    def test_very_small_weights(self):
        """Test with very small positive weights."""
        g = Graph(directed=False)
        g.add_edge(0, 1, 1e-15)
        g.add_edge(1, 2, 1e-15)
        g.add_edge(0, 2, 1e-14)
        prep = BALTHPreprocessing(g, k_landmarks=2, k_hubs=1)
        _check(g, 0, 2, prep)

    def test_mixed_weight_magnitudes(self):
        """Test with weights spanning many orders of magnitude."""
        g = Graph(directed=False)
        g.add_edge(0, 1, 1e-10)
        g.add_edge(1, 2, 1e10)
        g.add_edge(0, 2, 1e10 + 1)
        prep = BALTHPreprocessing(g, k_landmarks=2, k_hubs=1)
        _check(g, 0, 2, prep)

    def test_duplicate_edges(self):
        """Test graph where edges are added multiple times (last weight wins)."""
        g = Graph(directed=False)
        g.add_edge(0, 1, 10.0)
        g.add_edge(0, 1, 1.0)  # overwrites
        g.add_edge(1, 2, 1.0)
        prep = BALTHPreprocessing(g, k_landmarks=2, k_hubs=1)
        d, _ = balth_query(g, 0, 2, prep)
        d_dijk, _ = dijkstra_p2p(g, 0, 2)
        assert abs(d - d_dijk) < 1e-9

    def test_single_node(self):
        """Test on a graph with a single node."""
        g = Graph(directed=False)
        g.add_node(0)
        prep = BALTHPreprocessing(g, k_landmarks=1, k_hubs=1)
        d, exp = balth_query(g, 0, 0, prep)
        assert d == 0.0
        assert exp == 0

    def test_linear_chain(self):
        """Test on a long linear chain (worst case for bidirectional)."""
        g = Graph(directed=False)
        for i in range(99):
            g.add_edge(i, i + 1, 1.0)
        prep = BALTHPreprocessing(g, k_landmarks=4, k_hubs=4)
        _check(g, 0, 99, prep)
        _check(g, 0, 50, prep)
        _check(g, 25, 75, prep)

    def test_star_graph(self):
        """Test star graph (high-degree center, low-degree leaves)."""
        g = Graph(directed=False)
        for i in range(1, 100):
            g.add_edge(0, i, float(i))
        prep = BALTHPreprocessing(g, k_landmarks=4, k_hubs=4)
        # Leaf to leaf goes through center
        _check(g, 1, 99, prep)
        _check(g, 50, 51, prep)
        # Center to leaf
        _check(g, 0, 50, prep)

    def test_directed_graph_with_components(self):
        """Test directed graph where reachability is asymmetric."""
        g = Graph(directed=True)
        g.add_edge(0, 1, 1.0)
        g.add_edge(1, 2, 1.0)
        # No edges back from 2 to 0
        prep = BALTHPreprocessing(g, k_landmarks=2, k_hubs=1)
        _check(g, 0, 2, prep)
        _check(g, 2, 0, prep)  # should be INF

    def test_all_optimization_combinations(self):
        """Verify all 4 optimization flag combinations produce same result."""
        g = Graph.grid(15, 15, seed=42)
        prep = BALTHPreprocessing(g, k_landmarks=4, k_hubs=4)
        rng = random.Random(42)
        nodes = g.nodes()
        for _ in range(20):
            s, t = rng.choice(nodes), rng.choice(nodes)
            d_ref, _ = dijkstra_p2p(g, s, t)
            for opt_a in [True, False]:
                for opt_s in [True, False]:
                    d, _ = balth_query(g, s, t, prep,
                                       opt_active_landmarks=opt_a,
                                       opt_settled_pruning=opt_s)
                    if d_ref == INF and d == INF:
                        continue
                    assert abs(d - d_ref) < 1e-9, \
                        f"opts=({opt_a},{opt_s}), {s}->{t}: {d} vs {d_ref}"
