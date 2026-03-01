"""Graph data structure for weighted directed graphs.

Adjacency list representation optimized for SSSP algorithms.
"""

from collections import defaultdict


class Graph:
    """Weighted directed graph using adjacency lists."""

    def __init__(self, n=0):
        self.n = n  # number of vertices (0-indexed: 0..n-1)
        self.adj = defaultdict(list)  # adj[u] = [(v, weight), ...]
        self._edge_count = 0

    @property
    def m(self):
        return self._edge_count

    def add_edge(self, u, v, w):
        """Add directed edge u -> v with weight w."""
        self.adj[u].append((v, w))
        self._edge_count += 1
        self.n = max(self.n, u + 1, v + 1)

    def neighbors(self, u):
        """Return list of (neighbor, weight) pairs for vertex u."""
        return self.adj[u]

    def vertices(self):
        """Return range of vertex IDs."""
        return range(self.n)

    def edges(self):
        """Yield all (u, v, w) triples."""
        for u in range(self.n):
            for v, w in self.adj[u]:
                yield u, v, w

    def __repr__(self):
        return f"Graph(n={self.n}, m={self.m})"
