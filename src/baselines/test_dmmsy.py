"""Correctness tests for DMMSY algorithm on 5 graph families.

Compares against Bellman-Ford reference.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.baselines.dmmsy import dmmsy_sssp
from src.baselines.test_dijkstra import bellman_ford_reference
from src.benchmarks.graph_gen import (
    erdos_renyi, sparse_random, grid_lattice, adversarial_dijkstra
)
import random


def check_correctness(adj, n, source=0, label=""):
    result = dmmsy_sssp(adj, source, n)
    ref_dist = bellman_ford_reference(adj, source, n)
    for v in range(n):
        d_dmmsy = result.dist[v]
        d_ref = ref_dist[v]
        if d_ref == float('inf'):
            assert d_dmmsy == float('inf'), \
                f"{label}: v={v}: DMMSY={d_dmmsy}, BF=inf"
        else:
            assert abs(d_dmmsy - d_ref) < 1e-9, \
                f"{label}: v={v}: DMMSY={d_dmmsy}, BF={d_ref}"
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


if __name__ == '__main__':
    print("Running DMMSY correctness tests...")
    test_complete()
    test_sparse()
    test_grid()
    test_uniform()
    test_adversarial()
    print("All tests PASSED")
