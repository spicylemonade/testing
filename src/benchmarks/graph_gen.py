"""Graph generation framework for SSSP benchmarking.

Generates directed weighted graphs for 8 families:
  1. Erdos-Renyi G(n,p)
  2. Sparse random (m = O(n))
  3. Dense random (m = Theta(n^2))
  4. Grid/lattice
  5. Planar graphs (grid-based with random weights)
  6. High-diameter (path + random shortcuts)
  7. Expander-like (random regular)
  8. Adversarial (worst-case for Dijkstra decrease-key chains)

All generators return adj: dict[int, list[tuple[int, float]]] and
guarantee the graph is connected from vertex 0 (source).
"""

import random
import math


def _ensure_connected(adj, n, rng, max_weight=10.0):
    """Add edges along a random permutation to ensure connectivity from 0."""
    perm = list(range(n))
    rng.shuffle(perm)
    # Ensure vertex 0 is first
    idx0 = perm.index(0)
    perm[0], perm[idx0] = perm[idx0], perm[0]
    added = 0
    for i in range(n - 1):
        u, v = perm[i], perm[i + 1]
        w = rng.uniform(0.1, max_weight)
        if u not in adj:
            adj[u] = []
        adj[u].append((v, w))
        added += 1
    return added


def erdos_renyi(n, m=None, seed=42, max_weight=10.0):
    """Erdos-Renyi G(n,p) directed graph with m target edges."""
    rng = random.Random(seed)
    if m is None:
        m = 5 * n
    adj = {i: [] for i in range(n)}
    p = min(1.0, m / max(1, n * (n - 1)))
    edge_count = 0
    for u in range(n):
        for v in range(n):
            if u != v and rng.random() < p:
                w = rng.uniform(0.1, max_weight)
                adj[u].append((v, w))
                edge_count += 1
    edge_count += _ensure_connected(adj, n, rng, max_weight)
    return adj, n, edge_count


def sparse_random(n, m=None, seed=42, max_weight=10.0):
    """Sparse random directed graph with m = O(n) edges."""
    rng = random.Random(seed)
    if m is None:
        m = 2 * n
    adj = {i: [] for i in range(n)}
    edge_count = _ensure_connected(adj, n, rng, max_weight)
    while edge_count < m:
        u = rng.randint(0, n - 1)
        v = rng.randint(0, n - 1)
        if u != v:
            w = rng.uniform(0.1, max_weight)
            adj[u].append((v, w))
            edge_count += 1
    return adj, n, edge_count


def dense_random(n, m=None, seed=42, max_weight=10.0):
    """Dense random directed graph with m = Theta(n^2) edges."""
    rng = random.Random(seed)
    if m is None:
        m = n * n // 2
    adj = {i: [] for i in range(n)}
    edge_count = _ensure_connected(adj, n, rng, max_weight)
    while edge_count < m:
        u = rng.randint(0, n - 1)
        v = rng.randint(0, n - 1)
        if u != v:
            w = rng.uniform(0.1, max_weight)
            adj[u].append((v, w))
            edge_count += 1
    return adj, n, edge_count


def grid_lattice(n, m=None, seed=42, max_weight=10.0):
    """Grid/lattice graph. n is approximate; actual n = rows*cols."""
    rng = random.Random(seed)
    rows = max(2, int(math.sqrt(n)))
    cols = max(2, n // rows)
    actual_n = rows * cols
    adj = {i: [] for i in range(actual_n)}
    edge_count = 0

    def idx(r, c):
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            u = idx(r, c)
            # Right neighbor
            if c + 1 < cols:
                w = rng.uniform(0.1, max_weight)
                adj[u].append((idx(r, c + 1), w))
                edge_count += 1
            # Down neighbor
            if r + 1 < rows:
                w = rng.uniform(0.1, max_weight)
                adj[u].append((idx(r + 1, c), w))
                edge_count += 1
            # Left (directed both ways)
            if c > 0:
                w = rng.uniform(0.1, max_weight)
                adj[u].append((idx(r, c - 1), w))
                edge_count += 1
            # Up
            if r > 0:
                w = rng.uniform(0.1, max_weight)
                adj[u].append((idx(r - 1, c), w))
                edge_count += 1

    return adj, actual_n, edge_count


def planar_graph(n, m=None, seed=42, max_weight=10.0):
    """Planar graph based on Delaunay-like triangulation of grid."""
    rng = random.Random(seed)
    rows = max(2, int(math.sqrt(n)))
    cols = max(2, n // rows)
    actual_n = rows * cols
    adj = {i: [] for i in range(actual_n)}
    edge_count = 0

    def idx(r, c):
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            u = idx(r, c)
            neighbors = []
            if c + 1 < cols:
                neighbors.append(idx(r, c + 1))
            if r + 1 < rows:
                neighbors.append(idx(r + 1, c))
            if r + 1 < rows and c + 1 < cols:
                neighbors.append(idx(r + 1, c + 1))
            for v in neighbors:
                w = rng.uniform(0.1, max_weight)
                adj[u].append((v, w))
                adj[v].append((u, rng.uniform(0.1, max_weight)))
                edge_count += 2

    return adj, actual_n, edge_count


def high_diameter(n, m=None, seed=42, max_weight=10.0):
    """High-diameter graph: path + sparse random shortcuts."""
    rng = random.Random(seed)
    if m is None:
        m = 2 * n
    adj = {i: [] for i in range(n)}
    edge_count = 0

    # Build a directed path 0 -> 1 -> ... -> n-1
    for i in range(n - 1):
        w = rng.uniform(0.1, max_weight)
        adj[i].append((i + 1, w))
        edge_count += 1

    # Add sparse random shortcuts
    shortcut_count = max(0, m - (n - 1))
    for _ in range(shortcut_count):
        u = rng.randint(0, n - 1)
        v = rng.randint(0, n - 1)
        if u != v:
            w = rng.uniform(0.1, max_weight)
            adj[u].append((v, w))
            edge_count += 1

    return adj, n, edge_count


def expander_like(n, m=None, seed=42, max_weight=10.0, degree=10):
    """Expander-like graph: random regular with given degree."""
    rng = random.Random(seed)
    if m is None:
        m = degree * n
    adj = {i: [] for i in range(n)}
    edge_count = _ensure_connected(adj, n, rng, max_weight)

    target = m - edge_count
    per_vertex = max(1, target // n)
    for u in range(n):
        for _ in range(per_vertex):
            v = rng.randint(0, n - 1)
            if u != v:
                w = rng.uniform(0.1, max_weight)
                adj[u].append((v, w))
                edge_count += 1

    return adj, n, edge_count


def adversarial_dijkstra(n, m=None, seed=42, max_weight=10.0):
    """Adversarial graph for Dijkstra: long decrease-key chains.

    Constructs a graph where many decrease-key operations are triggered
    by having multiple paths to the same vertex with decreasing weights.
    """
    rng = random.Random(seed)
    if m is None:
        m = 5 * n
    adj = {i: [] for i in range(n)}
    edge_count = 0

    # Forward path with large weights
    for i in range(n - 1):
        adj[i].append((i + 1, max_weight * (n - i)))
        edge_count += 1

    # Backward "shortcut" edges that trigger cascading decrease-keys
    # Edge from i to j (j > i) with progressively smaller weights
    # discovered in reverse order
    for layer in range(min(n // 2, int(math.sqrt(m)))):
        for i in range(0, n - 1, max(1, n // (layer + 2))):
            j = min(n - 1, i + rng.randint(1, max(1, n // 4)))
            if i != j and edge_count < m:
                # Weight that beats current best path through forward edges
                w = rng.uniform(0.1, max_weight * 0.5)
                adj[i].append((j, w))
                edge_count += 1

    # Fill remaining edges randomly
    while edge_count < m:
        u = rng.randint(0, n - 1)
        v = rng.randint(0, n - 1)
        if u != v:
            w = rng.uniform(0.1, max_weight)
            adj[u].append((v, w))
            edge_count += 1

    return adj, n, edge_count


# Registry of all generators
GENERATORS = {
    'erdos_renyi': erdos_renyi,
    'sparse_random': sparse_random,
    'dense_random': dense_random,
    'grid_lattice': grid_lattice,
    'planar': planar_graph,
    'high_diameter': high_diameter,
    'expander': expander_like,
    'adversarial': adversarial_dijkstra,
}


def generate(family, n, m=None, seed=42, max_weight=10.0):
    """Generate a graph from the given family."""
    gen = GENERATORS[family]
    return gen(n, m=m, seed=seed, max_weight=max_weight)


if __name__ == '__main__':
    for name, gen in GENERATORS.items():
        adj, actual_n, actual_m = gen(100, seed=42)
        print(f"{name:20s}: n={actual_n:5d}, m={actual_m:5d}")
