"""Correctness tests for Dijkstra + Fibonacci heap on 5 graph families.

Tests against a simple Bellman-Ford reference implementation.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.baselines.dijkstra_fib import dijkstra_fibonacci
from src.benchmarks.graph_gen import (
    erdos_renyi, sparse_random, grid_lattice, adversarial_dijkstra
)
import random

def bellman_ford_reference(adj, source, n):
    """Simple Bellman-Ford for correctness reference."""
    INF = float('inf')
    dist = [INF] * n
    dist[source] = 0.0
    for _ in range(n - 1):
        updated = False
        for u in range(n):
            if dist[u] == INF:
                continue
            for v, w in adj.get(u, []):
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
        if not updated:
            break
    return dist


def check_correctness(adj, n, source=0, label=""):
    """Compare Dijkstra-Fib against Bellman-Ford reference."""
    result = dijkstra_fibonacci(adj, source, n)
    ref_dist = bellman_ford_reference(adj, source, n)

    for v in range(n):
        d_dijk = result.dist[v]
        d_ref = ref_dist[v]
        if d_ref == float('inf'):
            assert d_dijk == float('inf'), \
                f"{label}: vertex {v}: Dijkstra={d_dijk}, BF=inf"
        else:
            assert abs(d_dijk - d_ref) < 1e-9, \
                f"{label}: vertex {v}: Dijkstra={d_dijk}, BF={d_ref}"
    return result


def test_complete_graph():
    """Test 1: Complete graph."""
    rng = random.Random(42)
    n = 50
    adj = {i: [] for i in range(n)}
    for u in range(n):
        for v in range(n):
            if u != v:
                adj[u].append((v, rng.uniform(0.1, 10.0)))
    res = check_correctness(adj, n, label="complete")
    print(f"  complete(n={n}): OK | comps={res.comparisons} adds={res.additions} dk={res.decrease_keys}")


def test_sparse_random():
    """Test 2: Sparse random graph."""
    adj, n, m = sparse_random(200, m=400, seed=42)
    res = check_correctness(adj, n, label="sparse_random")
    print(f"  sparse_random(n={n}, m={m}): OK | comps={res.comparisons} adds={res.additions} dk={res.decrease_keys}")


def test_grid_lattice():
    """Test 3: Grid/lattice graph."""
    adj, n, m = grid_lattice(100, seed=42)
    res = check_correctness(adj, n, label="grid_lattice")
    print(f"  grid_lattice(n={n}, m={m}): OK | comps={res.comparisons} adds={res.additions} dk={res.decrease_keys}")


def test_uniform_weights():
    """Test 4: Graph with uniform weights."""
    rng = random.Random(42)
    n = 100
    adj = {i: [] for i in range(n)}
    # All edges weight 1.0
    for i in range(n - 1):
        adj[i].append((i + 1, 1.0))
    for _ in range(200):
        u = rng.randint(0, n - 1)
        v = rng.randint(0, n - 1)
        if u != v:
            adj[u].append((v, 1.0))
    res = check_correctness(adj, n, label="uniform_weight")
    print(f"  uniform_weight(n={n}): OK | comps={res.comparisons} adds={res.additions} dk={res.decrease_keys}")


def test_adversarial():
    """Test 5: Worst-case Fibonacci heap graph."""
    adj, n, m = adversarial_dijkstra(200, m=1000, seed=42)
    res = check_correctness(adj, n, label="adversarial")
    print(f"  adversarial(n={n}, m={m}): OK | comps={res.comparisons} adds={res.additions} dk={res.decrease_keys}")


def test_edge_cases():
    """Test edge cases: single vertex, disconnected, self-loops, zero weights."""
    # Single vertex
    adj = {0: []}
    res = dijkstra_fibonacci(adj, 0, n=1)
    assert res.dist == [0.0]

    # Disconnected
    adj = {0: [(1, 1.0)], 1: [], 2: []}
    res = dijkstra_fibonacci(adj, 0, n=3)
    assert res.dist[0] == 0.0
    assert res.dist[1] == 1.0
    assert res.dist[2] == float('inf')

    # Self-loops (should be ignored)
    adj = {0: [(0, 5.0), (1, 2.0)], 1: [(1, 3.0)]}
    res = dijkstra_fibonacci(adj, 0, n=2)
    assert res.dist == [0.0, 2.0]

    # Zero-weight edges
    adj = {0: [(1, 0.0), (2, 1.0)], 1: [(2, 0.0)], 2: []}
    res = dijkstra_fibonacci(adj, 0, n=3)
    assert res.dist == [0.0, 0.0, 0.0]

    print("  edge_cases: OK")


if __name__ == '__main__':
    print("Running Dijkstra-Fibonacci correctness tests...")
    test_complete_graph()
    test_sparse_random()
    test_grid_lattice()
    test_uniform_weights()
    test_adversarial()
    test_edge_cases()
    print("All tests PASSED")
