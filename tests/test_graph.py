"""Unit tests for src/graph.py — at least 10 test cases."""

import io
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.graph import Graph


class TestGraphBasics:
    def test_add_node(self):
        g = Graph()
        g.add_node(0)
        g.add_node(1)
        assert g.num_nodes == 2
        assert g.num_edges == 0

    def test_add_edge_directed(self):
        g = Graph(directed=True)
        g.add_edge(0, 1, 5.0)
        assert g.has_edge(0, 1)
        assert not g.has_edge(1, 0)
        assert g.weight(0, 1) == 5.0
        assert g.num_edges == 1

    def test_add_edge_undirected(self):
        g = Graph(directed=False)
        g.add_edge(0, 1, 3.0)
        assert g.has_edge(0, 1)
        assert g.has_edge(1, 0)
        assert g.weight(1, 0) == 3.0
        # Undirected edges counted in both directions
        assert g.num_edges == 2

    def test_neighbors(self):
        g = Graph(directed=True)
        g.add_edge(0, 1, 2.0)
        g.add_edge(0, 2, 3.0)
        g.add_edge(1, 2, 1.0)
        nbrs = dict(g.neighbors(0))
        assert nbrs == {1: 2.0, 2: 3.0}

    def test_degree(self):
        g = Graph(directed=False)
        g.add_edge(0, 1, 1.0)
        g.add_edge(0, 2, 1.0)
        g.add_edge(0, 3, 1.0)
        assert g.degree(0) == 3
        assert g.degree(1) == 1

    def test_nodes_list(self):
        g = Graph()
        g.add_node(5)
        g.add_node(10)
        g.add_edge(5, 10, 1.0)
        assert set(g.nodes()) == {5, 10}


class TestGraphIO:
    def test_edge_list_roundtrip(self):
        g = Graph(directed=True)
        g.add_edge(0, 1, 2.5)
        g.add_edge(1, 2, 3.7)

        buf = io.StringIO()
        g.to_edge_list(buf)
        buf.seek(0)

        g2 = Graph.from_edge_list(buf, directed=True)
        assert g2.has_edge(0, 1)
        assert g2.has_edge(1, 2)
        assert abs(g2.weight(0, 1) - 2.5) < 1e-9
        assert abs(g2.weight(1, 2) - 3.7) < 1e-9

    def test_dimacs_roundtrip(self):
        g = Graph(directed=True)
        g.add_edge(1, 2, 10)
        g.add_edge(2, 3, 20)

        buf = io.StringIO()
        g.to_dimacs(buf)
        buf.seek(0)

        g2 = Graph.from_dimacs(buf)
        assert g2.has_edge(1, 2)
        assert g2.has_edge(2, 3)
        assert g2.weight(1, 2) == 10.0


class TestGraphGenerators:
    def test_erdos_renyi_size(self):
        g = Graph.erdos_renyi(100, 0.1, seed=42)
        assert g.num_nodes == 100
        # With p=0.1 and 100 nodes, expect ~495 undirected edges
        assert g.num_edges > 100  # very likely

    def test_erdos_renyi_reproducibility(self):
        g1 = Graph.erdos_renyi(50, 0.2, seed=42)
        g2 = Graph.erdos_renyi(50, 0.2, seed=42)
        assert g1.num_edges == g2.num_edges

    def test_grid_structure(self):
        g = Graph.grid(3, 4, seed=42)
        assert g.num_nodes == 12
        # 3x4 grid: 3*3 horizontal + 2*4 vertical = 9+8=17 undirected edges
        # Each undirected edge counted as 2 directed edges
        assert g.num_edges == 17 * 2

    def test_grid_coords(self):
        g = Graph.grid(5, 5, seed=42)
        assert 0 in g.coords
        assert g.coords[0] == (0.0, 0.0)
        assert g.coords[24] == (4.0, 4.0)

    def test_barabasi_albert_size(self):
        g = Graph.barabasi_albert(100, m=3, seed=42)
        assert g.num_nodes == 100
        assert g.num_edges > 0

    def test_complete_graph(self):
        g = Graph.complete(5, seed=42)
        assert g.num_nodes == 5
        # K_5: 10 undirected edges = 20 directed edges
        assert g.num_edges == 20

    def test_negative_weights(self):
        """Verify graph supports negative edge weights."""
        g = Graph(directed=True)
        g.add_edge(0, 1, -5.0)
        assert g.weight(0, 1) == -5.0
