"""Graph generators for SSSP benchmarking.

Six families covering diverse structural properties:
1. Adversarial Dijkstra inputs (maximize Fibonacci heap advantage)
2. Sparse Erdos-Renyi G(n, c/n)
3. Dense random graphs m = Theta(n^2)
4. Layered DAGs with controlled diameter
5. Grid/lattice graphs
6. Planted shortest-path tree graphs
"""

import random
import math
from src.graph import Graph


def gen_adversarial_dijkstra(n, seed=42):
    """Adversarial input that maximizes decrease-key operations.

    Constructs a graph where nearly every edge triggers a decrease-key
    in Dijkstra's algorithm, demonstrating the Fibonacci heap advantage
    over binary heaps.

    Strategy: Create a "spiral" where vertex i is initially reached via a
    long path, then a shortcut edge from vertex 0 provides a shorter path,
    triggering decrease-key for many vertices.
    """
    rng = random.Random(seed)
    g = Graph(n)

    # Backbone: chain 0 -> 1 -> 2 -> ... -> n-1 with decreasing weights
    for i in range(n - 1):
        g.add_edge(i, i + 1, n - i + rng.uniform(0, 1))

    # Shortcut edges from early vertices to later ones with shorter distances
    # This forces many decrease-key operations
    for i in range(min(n, 20)):
        for j in range(i + 2, n, max(1, n // 50)):
            g.add_edge(i, j, (j - i) * 0.5 + rng.uniform(0, 0.1))

    return g, "adversarial"


def gen_sparse_erdos_renyi(n, c=3.0, seed=42):
    """Sparse Erdos-Renyi G(n, c/n) near connectivity threshold.

    Expected edges: c*n (sparse). Uses direct edge sampling for efficiency.
    """
    rng = random.Random(seed)
    g = Graph(n)

    # Ensure connectivity: add spanning tree first
    perm = list(range(n))
    rng.shuffle(perm)
    for i in range(n - 1):
        w = rng.uniform(1, 100)
        g.add_edge(perm[i], perm[i + 1], w)

    # Sample approximately c*n additional random edges
    num_extra = int(c * n)
    for _ in range(num_extra):
        u = rng.randint(0, n - 1)
        v = rng.randint(0, n - 1)
        if u != v:
            g.add_edge(u, v, rng.uniform(1, 100))

    return g, "sparse_er"


def gen_dense_random(n, seed=42):
    """Dense random graph with m = Theta(n^2).

    For n <= 3000, each edge exists with probability 0.5.
    For larger n, sample n^2/2 random edges for efficiency.
    """
    rng = random.Random(seed)
    g = Graph(n)

    if n <= 3000:
        for u in range(n):
            for v in range(n):
                if u != v and rng.random() < 0.5:
                    g.add_edge(u, v, rng.uniform(1, 100))
    else:
        # Sample approximately n^2/2 edges
        num_edges = n * n // 2
        for _ in range(num_edges):
            u = rng.randint(0, n - 1)
            v = rng.randint(0, n - 1)
            if u != v:
                g.add_edge(u, v, rng.uniform(1, 100))

    return g, "dense"


def gen_layered_dag(n, num_layers=None, seed=42):
    """Layered DAG with controlled diameter.

    Vertices are partitioned into layers. Edges only go from layer i to
    layer i+1 (and within layers), creating a DAG with diameter = num_layers.
    """
    rng = random.Random(seed)
    if num_layers is None:
        num_layers = max(3, int(math.sqrt(n)))

    g = Graph(n)
    layer_size = max(1, n // num_layers)

    def layer_of(v):
        return min(v // layer_size, num_layers - 1)

    # Edges from each layer to the next
    for u in range(n):
        lu = layer_of(u)
        # Forward edges to next layer
        next_layer_start = (lu + 1) * layer_size
        next_layer_end = min((lu + 2) * layer_size, n)
        if next_layer_start < n:
            # Connect to 2-5 random vertices in next layer
            targets = list(range(next_layer_start, min(next_layer_end, n)))
            for v in rng.sample(targets, min(len(targets), rng.randint(2, 5))):
                g.add_edge(u, v, rng.uniform(1, 50))

    return g, "layered_dag"


def gen_grid(n, seed=42):
    """2D grid/lattice graph.

    Creates a sqrt(n) x sqrt(n) grid with directed edges in all 4 directions.
    """
    rng = random.Random(seed)
    side = int(math.ceil(math.sqrt(n)))
    actual_n = side * side
    g = Graph(actual_n)

    for r in range(side):
        for c in range(side):
            u = r * side + c
            # Right
            if c + 1 < side:
                v = r * side + (c + 1)
                g.add_edge(u, v, rng.uniform(1, 10))
                g.add_edge(v, u, rng.uniform(1, 10))
            # Down
            if r + 1 < side:
                v = (r + 1) * side + c
                g.add_edge(u, v, rng.uniform(1, 10))
                g.add_edge(v, u, rng.uniform(1, 10))

    return g, "grid"


def gen_planted_spt(n, seed=42):
    """Graph with planted shortest-path tree structure.

    First creates a random spanning tree (the planted SPT), then adds
    random edges that do NOT create shorter paths. This tests whether
    algorithms can efficiently discover the planted tree.
    """
    rng = random.Random(seed)
    g = Graph(n)

    # Build random spanning tree from vertex 0
    dist = [0.0] * n
    parent = [-1] * n
    order = list(range(1, n))
    rng.shuffle(order)

    for v in order:
        # Attach v to a random existing vertex
        u = rng.randint(0, v - 1) if v > 0 else 0
        w = rng.uniform(1, 10)
        g.add_edge(u, v, w)
        dist[v] = dist[u] + w
        parent[v] = u

    # Add non-tree edges that don't create shorter paths
    num_extra = n * 2
    for _ in range(num_extra):
        u = rng.randint(0, n - 1)
        v = rng.randint(0, n - 1)
        if u != v:
            # Weight must be >= dist[v] - dist[u] to not create shorter path
            min_w = max(0.01, dist[v] - dist[u] + rng.uniform(0.01, 5))
            g.add_edge(u, v, min_w)

    return g, "planted_spt"


# Registry of all generators
GENERATORS = {
    "adversarial": gen_adversarial_dijkstra,
    "sparse_er": gen_sparse_erdos_renyi,
    "dense": gen_dense_random,
    "layered_dag": gen_layered_dag,
    "grid": gen_grid,
    "planted_spt": gen_planted_spt,
}


def generate_all(n, seed=42):
    """Generate one graph from each family."""
    results = {}
    for name, gen_fn in GENERATORS.items():
        g, gtype = gen_fn(n, seed=seed)
        results[name] = g
    return results
