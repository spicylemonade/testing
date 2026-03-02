#!/usr/bin/env python3
"""Run benchmarks on realistic graph instances (item_021).

Generates:
  1. Road-network-like graph: 2D geometric random graph with >= 100K vertices
  2. Social-network-like graph: power-law graph with >= 100K vertices

Produces results/realistic_benchmarks.json
"""

import json
import math
import os
import signal
import sys
import time

sys.path.insert(0, ".")

from src.baselines.dijkstra_fibonacci import sssp as fib_sssp
from src.baselines.dijkstra_binary import sssp as bin_sssp
from src.sota.duan_stoc2025 import sssp as duan_sssp
from src.novel.dams_sssp import sssp as dams_sssp
from src.benchmark.harness import benchmark_single


class Timeout(Exception):
    pass

def _timeout_handler(signum, frame):
    raise Timeout()


ALGORITHMS = {
    "dijkstra_fibonacci": fib_sssp,
    "dijkstra_binary": bin_sssp,
    "duan_stoc2025": duan_sssp,
    "dams_sssp": dams_sssp,
}


def generate_road_network_like(n, seed=42):
    """Generate a road-network-like 2D geometric graph."""
    import random
    random.seed(seed)

    points = [(random.random(), random.random()) for _ in range(n)]
    grid_size = max(1, int(math.sqrt(n) / 4))
    cells = {}
    for i, (x, y) in enumerate(points):
        cx = min(int(x * grid_size), grid_size - 1)
        cy = min(int(y * grid_size), grid_size - 1)
        cells.setdefault((cx, cy), []).append(i)

    adj = {}
    k_neighbors = 4
    radius = 3.0 / math.sqrt(n)

    for i, (x, y) in enumerate(points):
        cx = min(int(x * grid_size), grid_size - 1)
        cy = min(int(y * grid_size), grid_size - 1)
        neighbors = []
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                ncx, ncy = cx + dx, cy + dy
                if (ncx, ncy) not in cells:
                    continue
                for j in cells[(ncx, ncy)]:
                    if j == i:
                        continue
                    dist = math.sqrt((points[i][0] - points[j][0])**2 +
                                     (points[i][1] - points[j][1])**2)
                    if dist <= radius:
                        neighbors.append((j, dist))
        neighbors.sort(key=lambda x: x[1])
        for j, w in neighbors[:k_neighbors]:
            adj.setdefault(i, []).append((j, w))
            adj.setdefault(j, []).append((i, w))

    return adj, n


def generate_social_network_like(n, seed=42):
    """Generate a social-network-like power-law graph using fast BA model."""
    import random
    random.seed(seed)

    m_attach = 5
    adj = {}

    # Initialize with small complete graph
    for i in range(m_attach + 1):
        for j in range(i + 1, m_attach + 1):
            w = random.uniform(0.1, 1.0)
            adj.setdefault(i, []).append((j, w))
            adj.setdefault(j, []).append((i, w))

    # Use a flat array for fast preferential attachment
    stubs = []
    for i in range(m_attach + 1):
        stubs.extend([i] * m_attach)

    for v in range(m_attach + 1, n):
        targets = set()
        attempts = 0
        while len(targets) < min(m_attach, v) and attempts < m_attach * 10:
            u = stubs[random.randint(0, len(stubs) - 1)]
            targets.add(u)
            attempts += 1

        for u in targets:
            w = random.uniform(0.1, 1.0)
            adj.setdefault(v, []).append((u, w))
            adj.setdefault(u, []).append((v, w))
            stubs.append(u)
            stubs.append(v)

    return adj, n


def save_results(results):
    with open("results/realistic_benchmarks.json", "w") as f:
        json.dump(results, f, indent=2)


def main():
    os.makedirs("results", exist_ok=True)
    results = []

    configs = [
        ("road_network_100K", generate_road_network_like, 100000),
        ("road_network_200K", generate_road_network_like, 200000),
        ("social_network_100K", generate_social_network_like, 100000),
        ("social_network_200K", generate_social_network_like, 200000),
    ]

    for gname, gen_fn, n_target in configs:
        print(f"\nGenerating {gname} (n={n_target})...")
        t0 = time.time()
        adj, n_actual = gen_fn(n_target, seed=42)
        gen_time = time.time() - t0
        m = sum(len(adj.get(v, [])) for v in range(n_actual))
        print(f"  Generated: n={n_actual}, m={m}, gen_time={gen_time:.1f}s")

        source = 0
        for v in range(n_actual):
            if adj.get(v):
                source = v
                break

        for aname, algo_fn in ALGORITHMS.items():
            timeout_sec = 180

            print(f"  {aname:25s} | {gname:25s} | n={n_actual:>8d} m={m:>10d} ...",
                  end="", flush=True)

            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(timeout_sec)
            try:
                r = benchmark_single(algo_fn, adj, source, n_actual,
                                     warmup=1, runs=3)
                results.append({
                    "algorithm": aname, "graph_type": gname,
                    "n": n_actual, "m": m,
                    "mean_time": r["mean"], "median_time": r["median"],
                    "std_time": r["std"], "min_time": r["min"], "max_time": r["max"],
                    "comparisons": r["stats"]["comparisons"],
                    "additions": r["stats"]["additions"],
                    "heap_ops": r["stats"]["heap_ops"],
                    "peak_memory_kb": r["peak_memory_kb"],
                })
                signal.alarm(0)
                print(f"  {r['median']:.4f}s  comp={r['stats']['comparisons']}")
            except Timeout:
                signal.alarm(0)
                print("  TIMEOUT")
                results.append({
                    "algorithm": aname, "graph_type": gname,
                    "n": n_actual, "m": m, "error": "timeout",
                })
            except Exception as e:
                signal.alarm(0)
                print(f"  ERROR: {e}")
                results.append({
                    "algorithm": aname, "graph_type": gname,
                    "n": n_actual, "m": m, "error": str(e),
                })

        # Save incrementally after each graph type
        save_results(results)
        print(f"  [Saved {len(results)} results so far]")

    print(f"\nFinal: Saved {len(results)} results to results/realistic_benchmarks.json")


if __name__ == "__main__":
    main()
