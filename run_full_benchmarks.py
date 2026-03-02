#!/usr/bin/env python3
"""Run comprehensive benchmarks comparing all algorithms."""

import json
import math
import os
import signal
import sys
import time

sys.path.insert(0, ".")

from src.graphs.generator import sparse, grid, power_law, dijkstra_worst_case, road_network
from src.baselines.dijkstra_fibonacci import sssp as fib_sssp
from src.baselines.dijkstra_binary import sssp as bin_sssp
from src.sota.duan_stoc2025 import sssp as duan_sssp
from src.novel.dams_sssp import sssp as dams_sssp
from src.benchmark.harness import benchmark_single


class Timeout(Exception):
    pass

def _timeout_handler(signum, frame):
    raise Timeout()


def make_gen(gen_fn):
    def gen(n, seed):
        g = gen_fn(n, seed=seed)
        verts = g.vertices()
        n_actual = max(verts) + 1 if verts else 0
        return g.adj, n_actual
    return gen


GENERATORS = {
    "sparse": make_gen(sparse),
    "grid": make_gen(grid),
    "power_law": make_gen(power_law),
    "worst_case": make_gen(dijkstra_worst_case),
    "road_network": make_gen(road_network),
}

ALGORITHMS = {
    "dijkstra_fibonacci": fib_sssp,
    "dijkstra_binary": bin_sssp,
    "duan_stoc2025": duan_sssp,
    "dams_sssp": dams_sssp,
}

# Sizes: 1K, 5K, 10K, 50K, 100K
# Skip larger sizes for Python implementations (too slow)
SIZES = [1000, 5000, 10000, 50000, 100000]

results = []

for n in SIZES:
    for gname, gen_fn in GENERATORS.items():
        adj, n_actual = gen_fn(n, 42)
        m = sum(len(adj.get(v, [])) for v in range(n_actual))

        for aname, algo_fn in ALGORITHMS.items():
            # Skip very slow combos
            timeout_sec = 300
            if n > 50000 and aname in ('dijkstra_fibonacci', 'duan_stoc2025'):
                timeout_sec = 120
            if n > 10000 and gname == 'road_network':
                timeout_sec = 60  # road_network is dense

            print(f"  {aname:25s} | {gname:15s} | n={n_actual:>8d} m={m:>10d} ...",
                  end="", flush=True)

            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(timeout_sec)
            try:
                warmup = 2 if n <= 10000 else 1
                runs = 5 if n <= 10000 else 3
                r = benchmark_single(algo_fn, adj, 0, n_actual,
                                     warmup=warmup, runs=runs)
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

os.makedirs("results", exist_ok=True)
with open("results/full_benchmarks.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved {len(results)} results to results/full_benchmarks.json")
