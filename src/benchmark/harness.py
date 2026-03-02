"""Benchmarking harness for SSSP algorithms.

Provides wall-clock timing with warmup, statistical reporting, operation
counting, and peak memory tracking. Outputs results as JSON.
"""

import gc
import json
import os
import resource
import statistics
import time


def _peak_rss_kb():
    """Return peak RSS in kilobytes."""
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def benchmark_single(algo_fn, adj, source, n, *, warmup=2, runs=5):
    """Benchmark a single algorithm on a single graph.

    Parameters
    ----------
    algo_fn : callable
        Function with signature sssp(adj, source, n) -> (dist, stats).
    adj : dict
        Adjacency list.
    source : int
        Source vertex.
    n : int
        Number of vertices.
    warmup : int
        Number of warmup runs (discarded).
    runs : int
        Number of timed runs.

    Returns
    -------
    dict with keys: times, mean, median, std, min, max, stats (from last run),
    peak_memory_kb, distances (from last run).
    """
    # Warmup
    for _ in range(warmup):
        algo_fn(adj, source, n)

    times = []
    last_dist = None
    last_stats = None
    mem_before = _peak_rss_kb()

    for _ in range(runs):
        gc.disable()
        t0 = time.perf_counter()
        dist, stats = algo_fn(adj, source, n)
        t1 = time.perf_counter()
        gc.enable()
        times.append(t1 - t0)
        last_dist = dist
        last_stats = stats

    mem_after = _peak_rss_kb()

    return {
        "times": times,
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "std": statistics.stdev(times) if len(times) > 1 else 0.0,
        "min": min(times),
        "max": max(times),
        "stats": last_stats,
        "peak_memory_kb": mem_after - mem_before if mem_after > mem_before else 0,
        "distances": last_dist,
    }


def benchmark_matrix(algorithms, graph_generators, sizes, *,
                     warmup=2, runs=5, output_path=None):
    """Run benchmarks across a matrix of algorithms × graph types × sizes.

    Parameters
    ----------
    algorithms : dict
        Mapping name -> sssp function.
    graph_generators : dict
        Mapping name -> function(n, seed) returning (adj, n_actual).
    sizes : list of int
        Graph sizes to test.
    warmup, runs : int
        Benchmark parameters.
    output_path : str or None
        If given, write JSON results to this file.

    Returns
    -------
    list of result dicts.
    """
    results = []
    for n in sizes:
        for gname, gen_fn in graph_generators.items():
            adj, n_actual = gen_fn(n, 42)
            m = sum(len(adj.get(v, [])) for v in range(n_actual))
            for aname, algo_fn in algorithms.items():
                print(f"  {aname:25s} | {gname:15s} | n={n_actual:>8d} m={m:>10d} ...",
                      end="", flush=True)
                try:
                    r = benchmark_single(algo_fn, adj, 0, n_actual,
                                         warmup=warmup, runs=runs)
                    entry = {
                        "algorithm": aname,
                        "graph_type": gname,
                        "n": n_actual,
                        "m": m,
                        "mean_time": r["mean"],
                        "median_time": r["median"],
                        "std_time": r["std"],
                        "min_time": r["min"],
                        "max_time": r["max"],
                        "comparisons": r["stats"].get("comparisons", 0),
                        "additions": r["stats"].get("additions", 0),
                        "heap_ops": r["stats"].get("heap_ops", 0),
                        "peak_memory_kb": r["peak_memory_kb"],
                    }
                    results.append(entry)
                    print(f"  {r['median']:.4f}s")
                except Exception as e:
                    print(f"  ERROR: {e}")
                    results.append({
                        "algorithm": aname, "graph_type": gname,
                        "n": n_actual, "m": m, "error": str(e),
                    })

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")

    return results
