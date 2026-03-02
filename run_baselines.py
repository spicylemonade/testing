#!/usr/bin/env python3
"""Run baseline benchmarks across graph sizes and types."""

import json
import math
import os
import signal
import sys
import time

sys.path.insert(0, ".")

from src.graphs.generator import (
    sparse, dense, grid, power_law, dijkstra_worst_case, road_network,
)
from src.baselines.dijkstra_fibonacci import sssp as fib_sssp
from src.baselines.dijkstra_binary import sssp as bin_sssp
from src.baselines.bellman_ford import sssp as bf_sssp
from src.benchmark.harness import benchmark_single


class Timeout(Exception):
    pass


def _timeout_handler(signum, frame):
    raise Timeout()


def make_gen(gen_fn):
    """Wrap a graph generator to return (adj, n)."""
    def gen(n, seed):
        g = gen_fn(n, seed=seed)
        verts = g.vertices()
        n_actual = max(verts) + 1 if verts else 0
        return g.adj, n_actual
    return gen


GENERATORS = {
    "sparse": make_gen(sparse),
    "dense": make_gen(dense),
    "grid": make_gen(grid),
    "power_law": make_gen(power_law),
    "worst_case": make_gen(dijkstra_worst_case),
}

ALGORITHMS = {
    "dijkstra_fibonacci": fib_sssp,
    "dijkstra_binary": bin_sssp,
}

# Sizes to test (Bellman-Ford only on smaller sizes)
SIZES = [1000, 10000, 100000]
BF_SIZES = [1000, 10000]

results = []

# Bellman-Ford on small sizes
for n in BF_SIZES:
    for gname, gen_fn in GENERATORS.items():
        if gname == "dense" and n > 5000:
            continue
        adj, n_actual = gen_fn(n, 42)
        m = sum(len(adj.get(v, [])) for v in range(n_actual))
        print(f"  bellman_ford          | {gname:15s} | n={n_actual:>8d} m={m:>10d} ...", end="", flush=True)
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(120)
        try:
            r = benchmark_single(bf_sssp, adj, 0, n_actual, warmup=1, runs=3)
            results.append({
                "algorithm": "bellman_ford", "graph_type": gname,
                "n": n_actual, "m": m,
                "mean_time": r["mean"], "median_time": r["median"],
                "std_time": r["std"], "min_time": r["min"], "max_time": r["max"],
                "comparisons": r["stats"]["comparisons"],
                "additions": r["stats"]["additions"],
                "heap_ops": r["stats"]["heap_ops"],
                "peak_memory_kb": r["peak_memory_kb"],
            })
            signal.alarm(0)
            print(f"  {r['median']:.4f}s")
        except Timeout:
            signal.alarm(0)
            print("  TIMEOUT")
            results.append({
                "algorithm": "bellman_ford", "graph_type": gname,
                "n": n_actual, "m": m, "error": "timeout",
            })
        except Exception as e:
            signal.alarm(0)
            print(f"  ERROR: {e}")

# Main algorithms on all sizes
for n in SIZES:
    for gname, gen_fn in GENERATORS.items():
        if gname == "dense" and n > 10000:
            continue  # Dense n^2 graphs too large above 10K
        adj, n_actual = gen_fn(n, 42)
        m = sum(len(adj.get(v, [])) for v in range(n_actual))
        for aname, algo_fn in ALGORITHMS.items():
            print(f"  {aname:25s} | {gname:15s} | n={n_actual:>8d} m={m:>10d} ...", end="", flush=True)
            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(300)
            try:
                r = benchmark_single(algo_fn, adj, 0, n_actual, warmup=2, runs=5)
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
                print(f"  {r['median']:.4f}s")
            except Timeout:
                signal.alarm(0)
                print("  TIMEOUT")
            except Exception as e:
                signal.alarm(0)
                print(f"  ERROR: {e}")

# Save results
os.makedirs("results", exist_ok=True)
with open("results/baseline_benchmarks.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved {len(results)} results to results/baseline_benchmarks.json")
