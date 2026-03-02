"""Graph generators for SSSP benchmarking.

Directed-graph generators (Erdos-Renyi, sparse, dense, grid, power-law,
worst-case Dijkstra, road-network-like) plus DIMACS I/O and bidirectional
conversion.  All generators are seeded for reproducibility.
"""
from __future__ import annotations
import math, random
from typing import Dict, List, Tuple, Optional, TextIO, Union

Edge = Tuple[int, float]
AdjList = Dict[int, List[Edge]]


class Graph:
    """Directed weighted graph stored as adjacency lists."""
    def __init__(self, n: int = 0) -> None:
        self.n = n
        self.adj: AdjList = {v: [] for v in range(n)}

    def add_edge(self, u: int, v: int, w: float) -> None:
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append((v, w))

    def edge_count(self) -> int:
        return sum(len(nb) for nb in self.adj.values())

    def vertices(self) -> List[int]:
        return sorted(self.adj)


# -- helpers -----------------------------------------------------------------
def _rng(seed: int) -> random.Random:
    return random.Random(seed)

def _rw(r: random.Random, wr: Tuple[float, float]) -> float:
    return r.uniform(*wr)

def _empty(n: int) -> Graph:
    return Graph(n)


# -- generators --------------------------------------------------------------
def erdos_renyi(n: int, *, p: float = 0.1, m: Optional[int] = None,
                seed: int = 42, weight_range: Tuple[float, float] = (1.0, 100.0)) -> Graph:
    """Erdos-Renyi directed graph G(n, p).  *m* is accepted but ignored."""
    r, g = _rng(seed), _empty(n)
    for u in range(n):
        for v in range(n):
            if u != v and r.random() < p:
                g.add_edge(u, v, _rw(r, weight_range))
    return g

def sparse(n: int, *, m: Optional[int] = None, seed: int = 42,
           weight_range: Tuple[float, float] = (1.0, 100.0)) -> Graph:
    """Sparse directed graph with *m* = O(n) edges (default 3n)."""
    m = m or 3 * n
    r, g = _rng(seed), _empty(n)
    edges: set[Tuple[int, int]] = set()
    while len(edges) < m:
        u, v = r.randrange(n), r.randrange(n)
        if u != v and (u, v) not in edges:
            edges.add((u, v))
            g.add_edge(u, v, _rw(r, weight_range))
    return g

def dense(n: int, *, m: Optional[int] = None, seed: int = 42,
          weight_range: Tuple[float, float] = (1.0, 100.0)) -> Graph:
    """Dense directed graph with *m* = Theta(n^2) edges (default n^2/2)."""
    m = m or max(n, n * n // 2)
    r, g = _rng(seed), _empty(n)
    edges: set[Tuple[int, int]] = set()
    while len(edges) < min(m, n * (n - 1)):
        u, v = r.randrange(n), r.randrange(n)
        if u != v and (u, v) not in edges:
            edges.add((u, v))
            g.add_edge(u, v, _rw(r, weight_range))
    return g

def grid(n: int, *, m: Optional[int] = None, seed: int = 42,
         weight_range: Tuple[float, float] = (1.0, 100.0)) -> Graph:
    """Directed sqrt(n) x sqrt(n) grid with 4-directional edges."""
    side = max(1, int(math.isqrt(n)))
    actual_n = side * side
    r, g = _rng(seed), _empty(actual_n)
    for row in range(side):
        for col in range(side):
            u = row * side + col
            for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                nr, nc = row + dr, col + dc
                if 0 <= nr < side and 0 <= nc < side:
                    g.add_edge(u, nr * side + nc, _rw(r, weight_range))
    return g

def power_law(n: int, *, m: Optional[int] = None, seed: int = 42,
              weight_range: Tuple[float, float] = (1.0, 100.0)) -> Graph:
    """Barabasi-Albert style directed scale-free graph (default k=3)."""
    k = max(1, (m // n) if m else 3)
    r, g = _rng(seed), _empty(n)
    targets: List[int] = list(range(min(k, n)))
    for u in range(k, n):
        chosen: set[int] = set()
        while len(chosen) < min(k, u):
            v = targets[r.randrange(len(targets))]
            if v != u:
                chosen.add(v)
        for v in chosen:
            g.add_edge(u, v, _rw(r, weight_range))
            targets.append(v)
        targets.append(u)
    return g

def dijkstra_worst_case(n: int, *, m: Optional[int] = None, seed: int = 42,
                        weight_range: Tuple[float, float] = (1.0, 100.0)) -> Graph:
    """Worst-case for Dijkstra: chain + heavy shortcuts force Theta(n log n) ops.

    Chain 0->1->...->n-1 with small weights, plus shortcuts 0->v with large
    weights so relaxations via the chain trigger decrease-key for every node.
    """
    r, g = _rng(seed), _empty(n)
    for i in range(n - 1):
        g.add_edge(i, i + 1, _rw(r, (1.0, 2.0)))
    for v in range(2, n):
        g.add_edge(0, v, _rw(r, (weight_range[1], weight_range[1] * 2)))
    return g

def road_network(n: int, *, m: Optional[int] = None, seed: int = 42,
                 weight_range: Tuple[float, float] = (1.0, 100.0)) -> Graph:
    """2-D geometric random graph: edges between nearby random points."""
    r, g = _rng(seed), _empty(n)
    radius = min(1.0, 2.0 * math.sqrt(math.log(max(n, 2)) / max(n, 1)))
    pts = [(r.random(), r.random()) for _ in range(n)]
    lo, hi = weight_range
    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            d = math.hypot(pts[u][0] - pts[v][0], pts[u][1] - pts[v][1])
            if d <= radius:
                g.add_edge(u, v, round(lo + (hi - lo) * d / radius, 6))
    return g


# -- bidirectional conversion ------------------------------------------------
def make_bidirectional(g: Graph) -> Graph:
    """Return a new graph with every edge duplicated in both directions."""
    bg = Graph(g.n)
    seen: set[Tuple[int, int]] = set()
    for u, nbrs in g.adj.items():
        for v, w in nbrs:
            if (u, v) not in seen:
                bg.add_edge(u, v, w)
                seen.add((u, v))
            if (v, u) not in seen:
                bg.add_edge(v, u, w)
                seen.add((v, u))
    return bg


# -- DIMACS I/O --------------------------------------------------------------
def write_dimacs(g: Graph, out: Union[str, TextIO]) -> None:
    """Write *g* in DIMACS shortest-path format (1-indexed vertices)."""
    lines = [f"p sp {g.n} {g.edge_count()}"]
    for u in g.vertices():
        for v, w in g.adj[u]:
            lines.append(f"a {u+1} {v+1} {w:.6f}")
    text = "\n".join(lines) + "\n"
    if isinstance(out, str):
        with open(out, "w") as f:
            f.write(text)
    else:
        out.write(text)

def read_dimacs(src: Union[str, TextIO]) -> Graph:
    """Read a DIMACS shortest-path file and return a Graph (0-indexed)."""
    def _parse(lines):
        g: Optional[Graph] = None
        for line in lines:
            p = line.split()
            if not p or p[0] == "c":
                continue
            if p[0] == "p":
                g = Graph(int(p[2]))
            elif p[0] == "a" and g is not None:
                g.add_edge(int(p[1]) - 1, int(p[2]) - 1, float(p[3]))
        if g is None:
            raise ValueError("No problem line found in DIMACS input")
        return g
    if isinstance(src, str):
        with open(src) as f:
            return _parse(f)
    return _parse(src)
