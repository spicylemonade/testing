"""Core graph data structures for shortest path research.

Provides an adjacency-list graph with O(1) neighbor lookup,
weighted edges, I/O in edge-list and DIMACS formats, and
random graph generators (Erdős-Rényi, grid, Barabási-Albert).
"""

from __future__ import annotations

import math
import random
from collections import defaultdict
from typing import Dict, Iterator, List, Optional, TextIO, Tuple


class Graph:
    """Weighted directed graph using adjacency-list representation.

    Each vertex is an integer.  Edges store float weights.
    Undirected graphs are represented as symmetric directed graphs.
    """

    def __init__(self, directed: bool = True):
        self.directed = directed
        # adj[u] is a dict mapping neighbor v -> weight
        self._adj: Dict[int, Dict[int, float]] = defaultdict(dict)
        self._num_edges = 0
        # Optional coordinate data for spatial graphs
        self.coords: Dict[int, Tuple[float, float]] = {}

    # ---- Basic operations ----

    @property
    def num_nodes(self) -> int:
        return len(self._adj)

    @property
    def num_edges(self) -> int:
        return self._num_edges

    def nodes(self) -> List[int]:
        return list(self._adj.keys())

    def add_node(self, u: int) -> None:
        if u not in self._adj:
            self._adj[u] = {}

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        if v not in self._adj[u]:
            self._num_edges += 1
        self._adj[u][v] = weight
        self.add_node(v)  # ensure v exists
        if not self.directed:
            if u not in self._adj[v]:
                self._num_edges += 1
            self._adj[v][u] = weight

    def has_edge(self, u: int, v: int) -> bool:
        return v in self._adj.get(u, {})

    def weight(self, u: int, v: int) -> float:
        return self._adj[u][v]

    def neighbors(self, u: int) -> Iterator[Tuple[int, float]]:
        """Yield (neighbor, weight) pairs for vertex u.  O(1) per item."""
        return iter(self._adj[u].items())

    def degree(self, u: int) -> int:
        return len(self._adj[u])

    # ---- I/O: edge list format ----

    def to_edge_list(self, fp: TextIO) -> None:
        """Write graph in edge-list format: one 'u v weight' per line."""
        fp.write(f"# nodes={self.num_nodes} edges={self.num_edges} directed={self.directed}\n")
        seen = set()
        for u in sorted(self._adj):
            for v, w in sorted(self._adj[u].items()):
                if not self.directed:
                    key = (min(u, v), max(u, v))
                    if key in seen:
                        continue
                    seen.add(key)
                fp.write(f"{u} {v} {w}\n")

    @classmethod
    def from_edge_list(cls, fp: TextIO, directed: bool = True) -> "Graph":
        """Read graph from edge-list format."""
        g = cls(directed=directed)
        for line in fp:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("%"):
                continue
            parts = line.split()
            u, v = int(parts[0]), int(parts[1])
            w = float(parts[2]) if len(parts) > 2 else 1.0
            g.add_edge(u, v, w)
        return g

    # ---- I/O: DIMACS format ----

    def to_dimacs(self, fp: TextIO) -> None:
        """Write graph in DIMACS shortest-path format."""
        n = self.num_nodes
        m = self.num_edges
        fp.write(f"p sp {n} {m}\n")
        for u in sorted(self._adj):
            for v, w in sorted(self._adj[u].items()):
                fp.write(f"a {u} {v} {int(w)}\n")

    @classmethod
    def from_dimacs(cls, fp: TextIO) -> "Graph":
        """Read graph from DIMACS shortest-path format."""
        g = cls(directed=True)
        for line in fp:
            line = line.strip()
            if not line:
                continue
            if line.startswith("c"):
                continue
            if line.startswith("p"):
                continue  # we infer n,m from edges
            if line.startswith("a"):
                parts = line.split()
                u, v, w = int(parts[1]), int(parts[2]), float(parts[3])
                g.add_edge(u, v, w)
        return g

    # ---- Random graph generators ----

    @staticmethod
    def erdos_renyi(n: int, p: float, seed: int = 42,
                    directed: bool = False,
                    weight_range: Tuple[float, float] = (1.0, 10.0)) -> "Graph":
        """Generate Erdős-Rényi random graph G(n, p)."""
        rng = random.Random(seed)
        g = Graph(directed=directed)
        for i in range(n):
            g.add_node(i)
        wlo, whi = weight_range
        for i in range(n):
            start = 0 if directed else i + 1
            for j in range(start, n):
                if i == j:
                    continue
                if rng.random() < p:
                    w = rng.uniform(wlo, whi)
                    g.add_edge(i, j, round(w, 2))
        return g

    @staticmethod
    def grid(rows: int, cols: int, seed: int = 42,
             weight_range: Tuple[float, float] = (1.0, 10.0)) -> "Graph":
        """Generate a 2D grid graph with random weights."""
        rng = random.Random(seed)
        g = Graph(directed=False)
        wlo, whi = weight_range

        def node_id(r: int, c: int) -> int:
            return r * cols + c

        for r in range(rows):
            for c in range(cols):
                nid = node_id(r, c)
                g.add_node(nid)
                g.coords[nid] = (float(r), float(c))
                if c + 1 < cols:
                    g.add_edge(nid, node_id(r, c + 1), round(rng.uniform(wlo, whi), 2))
                if r + 1 < rows:
                    g.add_edge(nid, node_id(r + 1, c), round(rng.uniform(wlo, whi), 2))
        return g

    @staticmethod
    def barabasi_albert(n: int, m: int = 3, seed: int = 42,
                        weight_range: Tuple[float, float] = (1.0, 10.0)) -> "Graph":
        """Generate Barabási-Albert preferential attachment graph.

        Args:
            n: number of nodes
            m: number of edges to attach from new node to existing nodes
        """
        rng = random.Random(seed)
        g = Graph(directed=False)
        wlo, whi = weight_range

        # Start with a complete graph on m nodes
        for i in range(m):
            g.add_node(i)
            for j in range(i):
                g.add_edge(i, j, round(rng.uniform(wlo, whi), 2))

        # Degree-weighted target list for preferential attachment
        targets = []
        for i in range(m):
            targets.extend([i] * (m - 1))

        for new_node in range(m, n):
            chosen = set()
            attempts = 0
            while len(chosen) < m and attempts < m * 10:
                t = rng.choice(targets)
                chosen.add(t)
                attempts += 1
            for t in chosen:
                w = round(rng.uniform(wlo, whi), 2)
                g.add_edge(new_node, t, w)
                targets.append(new_node)
                targets.append(t)

        return g

    @staticmethod
    def complete(n: int, seed: int = 42,
                 weight_range: Tuple[float, float] = (1.0, 10.0)) -> "Graph":
        """Generate complete graph K_n with random weights."""
        rng = random.Random(seed)
        g = Graph(directed=False)
        wlo, whi = weight_range
        for i in range(n):
            g.add_node(i)
        for i in range(n):
            for j in range(i + 1, n):
                g.add_edge(i, j, round(rng.uniform(wlo, whi), 2))
        return g
