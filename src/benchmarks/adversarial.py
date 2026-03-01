"""Adversarial graph families that stress-test HopGuidedSSSP.

Three adversarial constructions targeting the algorithm's weak points:
1. Flat hop structure: all vertices at the same hop-distance
2. Deep chain with cross-edges: maximizes recursion depth and correction rounds
3. Layered bipartite: maximizes inter-block edge fraction
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import random


def flat_hop(n, m=None, seed=42, max_weight=10.0):
    """All non-source vertices at hop-distance 1 from source.

    This forces the geometric partition into a single block
    (all vertices share the same hop-layer), defeating the
    hop-guided decomposition and falling back to Dijkstra.

    The source has edges to all other vertices (star graph),
    plus m - (n-1) random edges among non-source vertices.
    """
    rng = random.Random(seed)
    if m is None:
        m = 3 * n

    adj = {i: [] for i in range(n)}

    # Source connects to all others (star)
    for v in range(1, n):
        adj[0].append((v, rng.uniform(0.1, max_weight)))

    edge_count = n - 1
    # Random edges among non-source vertices
    attempts = 0
    while edge_count < m and attempts < m * 5:
        u = rng.randint(1, n - 1)
        v = rng.randint(1, n - 1)
        if u != v:
            adj[u].append((v, rng.uniform(0.1, max_weight)))
            edge_count += 1
        attempts += 1

    return adj, n, edge_count


def deep_chain(n, m=None, seed=42, max_weight=10.0):
    """Long chain with cross-edges: maximizes hop-diameter.

    Vertices 0 -> 1 -> 2 -> ... -> n-1 form a chain (hop-diameter = n-1).
    Additional random cross-edges create shortcuts that require
    many inter-block correction rounds.
    """
    rng = random.Random(seed)
    if m is None:
        m = 3 * n

    adj = {i: [] for i in range(n)}

    # Main chain
    for i in range(n - 1):
        adj[i].append((i + 1, rng.uniform(0.1, max_weight)))
    edge_count = n - 1

    # Cross-edges: random backward and forward edges
    attempts = 0
    while edge_count < m and attempts < m * 5:
        u = rng.randint(0, n - 1)
        v = rng.randint(0, n - 1)
        if u != v:
            # Use small weights to create actual shortcuts
            adj[u].append((v, rng.uniform(0.01, 0.5)))
            edge_count += 1
        attempts += 1

    return adj, n, edge_count


def layered_bipartite(n, m=None, seed=42, max_weight=10.0):
    """Layered graph maximizing inter-block edges.

    Creates layers of vertices where most edges cross between
    adjacent layers. This maximizes the fraction of inter-block
    edges in the hop-guided partition, stressing the correction step.

    Layer structure: source -> L1 -> L2 -> ... -> L_k
    where k = sqrt(n). Each layer has sqrt(n) vertices.
    Edges: dense between adjacent layers, sparse within layers.
    """
    rng = random.Random(seed)
    if m is None:
        m = 3 * n

    k = max(2, int(n ** 0.5))
    layer_size = max(1, (n - 1) // k)

    adj = {i: [] for i in range(n)}
    edge_count = 0

    # Assign vertices to layers
    layers = []
    vid = 1
    for i in range(k):
        layer = []
        for _ in range(layer_size):
            if vid < n:
                layer.append(vid)
                vid += 1
        if layer:
            layers.append(layer)

    # Remaining vertices go to last layer
    while vid < n:
        if layers:
            layers[-1].append(vid)
        vid += 1

    # Source to first layer
    if layers:
        for v in layers[0]:
            adj[0].append((v, rng.uniform(0.1, max_weight)))
            edge_count += 1

    # Dense inter-layer edges (adjacent layers)
    for i in range(len(layers) - 1):
        for u in layers[i]:
            # Connect to ~3 random vertices in next layer
            targets = rng.sample(layers[i + 1],
                                min(3, len(layers[i + 1])))
            for v in targets:
                adj[u].append((v, rng.uniform(0.1, max_weight)))
                edge_count += 1

    # Fill remaining edges: mostly cross-layer
    attempts = 0
    while edge_count < m and attempts < m * 5:
        li = rng.randint(0, len(layers) - 1)
        lj = rng.randint(0, len(layers) - 1)
        if li != lj and layers[li] and layers[lj]:
            u = rng.choice(layers[li])
            v = rng.choice(layers[lj])
            adj[u].append((v, rng.uniform(0.1, max_weight)))
            edge_count += 1
        attempts += 1

    return adj, n, edge_count


ADVERSARIAL_GENERATORS = {
    'flat_hop': flat_hop,
    'deep_chain': deep_chain,
    'layered_bipartite': layered_bipartite,
}


if __name__ == '__main__':
    # Quick test
    for name, gen in ADVERSARIAL_GENERATORS.items():
        adj, n, m = gen(100, m=300, seed=42)
        print(f"{name}: n={n}, m={m}, "
              f"vertices_with_edges={sum(1 for v in adj if adj[v])}")
