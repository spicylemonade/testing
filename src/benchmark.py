"""Benchmark harness for SSSP algorithms.

Runs algorithms across graph families and sizes, collecting operation counts
and wall-clock times into CSV files.
"""

import csv
import time
import statistics
from src.graph_generators import GENERATORS
from src.dijkstra import dijkstra_fibonacci, dijkstra_binary
from src.op_counter import OpCounter, CSV_COLUMNS, write_csv_header, append_csv_row


def benchmark_single(algorithm_fn, algorithm_name, graph, graph_type, n, m,
                     trial, source=0):
    """Run a single benchmark and return a result dict."""
    counter = OpCounter()
    start = time.perf_counter()
    dist, counter, nodes_expanded = algorithm_fn(graph, source, counter=counter)
    elapsed_ms = (time.perf_counter() - start) * 1000

    return {
        "algorithm": algorithm_name,
        "graph_type": graph_type,
        "n": n,
        "m": m,
        "trial": trial,
        "total_ops": counter.total_ops,
        "comparisons": counter.comparisons,
        "additions": counter.additions,
        "heap_ops": counter.heap_ops,
        "heap_inserts": counter.heap_inserts,
        "extract_mins": counter.extract_mins,
        "decrease_keys": counter.decrease_keys,
        "wall_time_ms": round(elapsed_ms, 3),
        "nodes_expanded": nodes_expanded,
    }


def run_profile(output_path="results/dijkstra_baseline.csv",
                sizes=None, num_trials=3, graph_families=None,
                algorithms=None):
    """Run full profiling benchmark.

    Args:
        output_path: CSV file path for results.
        sizes: List of n values.
        num_trials: Trials per configuration.
        graph_families: List of generator names (default: all).
        algorithms: Dict of name -> function (default: Dijkstra variants).
    """
    if sizes is None:
        sizes = [1000, 10000]
    if graph_families is None:
        graph_families = list(GENERATORS.keys())
    if algorithms is None:
        algorithms = {
            "dijkstra_fib": dijkstra_fibonacci,
            "dijkstra_bin": dijkstra_binary,
        }

    write_csv_header(output_path)

    for n in sizes:
        for gtype in graph_families:
            gen_fn = GENERATORS[gtype]
            for trial in range(num_trials):
                seed = 42 + trial
                graph, _ = gen_fn(n, seed=seed)
                m = graph.m

                for algo_name, algo_fn in algorithms.items():
                    try:
                        result = benchmark_single(
                            algo_fn, algo_name, graph, gtype,
                            n, m, trial, source=0
                        )
                        append_csv_row(output_path, result)
                        print(f"  {algo_name}/{gtype} n={n} trial={trial}: "
                              f"ops={result['total_ops']}, "
                              f"time={result['wall_time_ms']:.1f}ms")
                    except Exception as e:
                        print(f"  ERROR {algo_name}/{gtype} n={n}: {e}")

    print(f"\nResults written to {output_path}")


if __name__ == "__main__":
    run_profile()
