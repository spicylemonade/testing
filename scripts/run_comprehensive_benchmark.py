"""Comprehensive benchmark: all algorithms, all graph families, multiple sizes.

Item 019: 500+ benchmark runs comparing HiBRA, Dijkstra (binary), Dijkstra (Fibonacci),
and batch Dijkstra across all 6 graph families at sizes n in {1000, 3000, 10000, 30000, 100000}.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph_generators import GENERATORS
from src.dijkstra import dijkstra_fibonacci, dijkstra_binary
from src.novel_algorithm import hibra
from src.batch_dijkstra import batch_dijkstra
from src.benchmark import benchmark_single
from src.op_counter import write_csv_header, append_csv_row

OUTPUT = "results/comprehensive_benchmark.csv"

# Configuration
SIZES = [1000, 3000, 10000, 30000, 100000]
NUM_TRIALS = 3
GRAPH_FAMILIES = list(GENERATORS.keys())

# Algorithms — Fibonacci heap excluded for large n (too slow in pure Python)
ALGORITHMS_ALL = {
    "hibra": hibra,
    "dijkstra_bin": dijkstra_binary,
    "dijkstra_fib": dijkstra_fibonacci,
    "batch_dijkstra": batch_dijkstra,
}

ALGORITHMS_NO_FIB = {
    "hibra": hibra,
    "dijkstra_bin": dijkstra_binary,
    "batch_dijkstra": batch_dijkstra,
}

# Dense graphs are O(n^2) edges — skip very large sizes
DENSE_MAX_N = 3000


def main():
    write_csv_header(OUTPUT)
    total_runs = 0
    start_time = time.time()

    for n in SIZES:
        for gtype in GRAPH_FAMILIES:
            # Skip large dense graphs
            if gtype == "dense_random" and n > DENSE_MAX_N:
                continue

            gen_fn = GENERATORS[gtype]

            # Choose algorithm set based on n
            if n <= 10000:
                algos = ALGORITHMS_ALL
            else:
                algos = ALGORITHMS_NO_FIB

            for trial in range(NUM_TRIALS):
                seed = 42 + trial
                try:
                    graph, _ = gen_fn(n, seed=seed)
                except Exception as e:
                    print(f"  SKIP {gtype} n={n}: generator error: {e}")
                    continue
                m = graph.m

                for algo_name, algo_fn in algos.items():
                    try:
                        result = benchmark_single(
                            algo_fn, algo_name, graph, gtype,
                            n, m, trial, source=0
                        )
                        append_csv_row(OUTPUT, result)
                        total_runs += 1
                        elapsed = time.time() - start_time
                        print(f"  [{total_runs:4d}] {algo_name:15s}/{gtype:20s} "
                              f"n={n:6d} m={m:8d} trial={trial} "
                              f"ops={result['total_ops']:12d} "
                              f"time={result['wall_time_ms']:8.1f}ms "
                              f"[{elapsed:.0f}s elapsed]")
                    except Exception as e:
                        print(f"  ERROR {algo_name}/{gtype} n={n}: {e}")

    elapsed = time.time() - start_time
    print(f"\n=== COMPLETE: {total_runs} runs in {elapsed:.1f}s ===")
    print(f"Results: {OUTPUT}")


if __name__ == "__main__":
    main()
