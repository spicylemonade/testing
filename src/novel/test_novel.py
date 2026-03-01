"""Correctness tests for the HopGuidedSSSP novel algorithm.

Tests on all 5 graph families + edge cases, compared against Bellman-Ford.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.novel.sssp import hop_guided_sssp
from src.baselines.test_dijkstra import bellman_ford_reference
from src.benchmarks.graph_gen import (
    erdos_renyi, sparse_random, grid_lattice, adversarial_dijkstra
)
import random


def check_correctness(adj, n, source=0, label=""):
    result = hop_guided_sssp(adj, source, n)
    ref_dist = bellman_ford_reference(adj, source, n)
    for v in range(n):
        d_novel = result.dist[v]
        d_ref = ref_dist[v]
        if d_ref == float('inf'):
            assert d_novel == float('inf'), \
                f"{label}: v={v}: novel={d_novel}, BF=inf"
        else:
            assert abs(d_novel - d_ref) < 1e-9, \
                f"{label}: v={v}: novel={d_novel}, BF={d_ref}"
    return result


def test_complete():
    rng = random.Random(42)
    n = 50
    adj = {i: [] for i in range(n)}
    for u in range(n):
        for v in range(n):
            if u != v:
                adj[u].append((v, rng.uniform(0.1, 10.0)))
    res = check_correctness(adj, n, label="complete")
    print(f"  complete(n={n}): OK | comps={res.comparisons} adds={res.additions} dk={res.decrease_keys}")


def test_sparse():
    adj, n, m = sparse_random(200, m=400, seed=42)
    res = check_correctness(adj, n, label="sparse")
    print(f"  sparse(n={n}, m={m}): OK | comps={res.comparisons} adds={res.additions} dk={res.decrease_keys}")


def test_grid():
    adj, n, m = grid_lattice(100, seed=42)
    res = check_correctness(adj, n, label="grid")
    print(f"  grid(n={n}, m={m}): OK | comps={res.comparisons} adds={res.additions} dk={res.decrease_keys}")


def test_uniform():
    rng = random.Random(42)
    n = 100
    adj = {i: [] for i in range(n)}
    for i in range(n - 1):
        adj[i].append((i + 1, 1.0))
    for _ in range(200):
        u = rng.randint(0, n - 1)
        v = rng.randint(0, n - 1)
        if u != v:
            adj[u].append((v, 1.0))
    res = check_correctness(adj, n, label="uniform")
    print(f"  uniform(n={n}): OK | comps={res.comparisons} adds={res.additions} dk={res.decrease_keys}")


def test_adversarial():
    adj, n, m = adversarial_dijkstra(200, m=1000, seed=42)
    res = check_correctness(adj, n, label="adversarial")
    print(f"  adversarial(n={n}, m={m}): OK | comps={res.comparisons} adds={res.additions} dk={res.decrease_keys}")


def test_edge_cases():
    # Single vertex
    adj = {0: []}
    res = hop_guided_sssp(adj, 0, n=1)
    assert res.dist == [0.0]

    # Disconnected
    adj = {0: [(1, 1.0)], 1: [], 2: []}
    res = hop_guided_sssp(adj, 0, n=3)
    assert res.dist[0] == 0.0
    assert res.dist[1] == 1.0
    assert res.dist[2] == float('inf')

    # Self-loops
    adj = {0: [(0, 5.0), (1, 2.0)], 1: [(1, 3.0)]}
    res = hop_guided_sssp(adj, 0, n=2)
    assert res.dist == [0.0, 2.0]

    # Zero-weight edges
    adj = {0: [(1, 0.0), (2, 1.0)], 1: [(2, 0.0)], 2: []}
    res = hop_guided_sssp(adj, 0, n=3)
    assert res.dist == [0.0, 0.0, 0.0]

    print("  edge_cases: OK")


def test_larger():
    """Test on larger graphs for robustness."""
    for size in [500, 1000]:
        adj, n, m = sparse_random(size, m=2*size, seed=42)
        res = check_correctness(adj, n, label=f"sparse_{size}")
        print(f"  sparse(n={n}, m={m}): OK")

        adj, n, m = adversarial_dijkstra(size, m=3*size, seed=42)
        res = check_correctness(adj, n, label=f"adversarial_{size}")
        print(f"  adversarial(n={n}, m={m}): OK")


if __name__ == '__main__':
    print("Running HopGuidedSSSP correctness tests...")
    test_complete()
    test_sparse()
    test_grid()
    test_uniform()
    test_adversarial()
    test_edge_cases()
    test_larger()
    print("All novel algorithm tests PASSED")
