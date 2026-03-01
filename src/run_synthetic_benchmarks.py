"""Run comprehensive synthetic benchmarks per experiment_plan.md.

Generates results/synthetic_results.csv with columns:
  algorithm, graph_type, num_nodes, num_edges, query_id,
  runtime_ms, nodes_expanded, peak_memory_kb
"""

import csv
import gc
import os
import random
import resource
import sys
import time
from statistics import median

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.graph import Graph
from src.dijkstra import dijkstra_p2p, dijkstra_bidirectional
from src.astar import astar_landmark
from src.novel_algorithm import BALTHPreprocessing, balth_query

SEED = 42
N_QUERIES = 10
N_REPS = 3


def generate_queries(graph, n_queries, seed):
    rng = random.Random(seed)
    nodes = graph.nodes()
    return [(rng.choice(nodes), rng.choice(nodes)) for _ in range(n_queries)]


def time_query(func, n_reps=N_REPS):
    """Run func n_reps times, return (median_time_ms, last_distance, last_expanded)."""
    times = []
    d, exp = None, None
    for _ in range(n_reps):
        gc.disable()
        t0 = time.perf_counter()
        d, exp = func()
        elapsed = time.perf_counter() - t0
        gc.enable()
        times.append(elapsed * 1000)
    return median(times), d, exp


def run_algorithms(graph, queries, prep=None, landmark_heur=None):
    """Run all algorithms on the given queries, return list of result dicts."""
    rows = []
    n_nodes = len(graph.nodes())
    n_edges = sum(1 for u in graph.nodes() for _ in graph.neighbors(u))
    if not graph.directed:
        n_edges //= 2

    for qi, (s, t) in enumerate(queries):
        # Dijkstra P2P
        ms, d, exp = time_query(lambda s=s, t=t: dijkstra_p2p(graph, s, t))
        rows.append({
            "algorithm": "dijkstra_p2p",
            "graph_type": "", "num_nodes": n_nodes, "num_edges": n_edges,
            "query_id": qi, "runtime_ms": f"{ms:.4f}",
            "nodes_expanded": exp, "distance": d,
        })

        # Bidirectional Dijkstra
        ms, d, exp = time_query(lambda s=s, t=t: dijkstra_bidirectional(graph, s, t))
        rows.append({
            "algorithm": "dijkstra_bidirectional",
            "graph_type": "", "num_nodes": n_nodes, "num_edges": n_edges,
            "query_id": qi, "runtime_ms": f"{ms:.4f}",
            "nodes_expanded": exp, "distance": d,
        })

        # A* Landmark
        if landmark_heur is not None:
            ms, d, exp = time_query(
                lambda s=s, t=t: astar_landmark(graph, s, t))
            rows.append({
                "algorithm": "astar_landmark",
                "graph_type": "", "num_nodes": n_nodes, "num_edges": n_edges,
                "query_id": qi, "runtime_ms": f"{ms:.4f}",
                "nodes_expanded": exp, "distance": d,
            })

        # BALT-H (all optimizations)
        if prep is not None:
            ms, d, exp = time_query(
                lambda s=s, t=t: balth_query(graph, s, t, prep))
            rows.append({
                "algorithm": "balth",
                "graph_type": "", "num_nodes": n_nodes, "num_edges": n_edges,
                "query_id": qi, "runtime_ms": f"{ms:.4f}",
                "nodes_expanded": exp, "distance": d,
            })

            # BALT-H (no optimizations)
            ms, d, exp = time_query(
                lambda s=s, t=t: balth_query(graph, s, t, prep,
                    opt_active_landmarks=False, opt_settled_pruning=False))
            rows.append({
                "algorithm": "balth_no_opt",
                "graph_type": "", "num_nodes": n_nodes, "num_edges": n_edges,
                "query_id": qi, "runtime_ms": f"{ms:.4f}",
                "nodes_expanded": exp, "distance": d,
            })

    return rows


def main():
    os.makedirs("results", exist_ok=True)

    configs = []

    # Grid graphs
    for side in [10, 20, 50, 100]:
        configs.append(("grid", side * side, lambda s=side: Graph.grid(s, s, seed=SEED)))

    # Erdős-Rényi at 5 density levels
    for n, p in [(100, 0.03), (100, 0.1), (500, 0.006), (500, 0.02), (500, 0.1),
                 (1000, 0.003), (1000, 0.01), (2500, 0.004), (5000, 0.002)]:
        label = f"er_{n}_{p}"
        configs.append((label, n, lambda n=n, p=p: Graph.erdos_renyi(n, p, seed=SEED)))

    # Barabási-Albert at 5 sizes
    for n in [100, 500, 1000, 2500, 5000]:
        configs.append((f"ba_{n}", n, lambda n=n: Graph.barabasi_albert(n, m=3, seed=SEED)))

    # Complete graphs
    for n in [50, 100, 200]:
        configs.append((f"complete_{n}", n, lambda n=n: Graph.complete(n, seed=SEED)))

    all_rows = []
    total_runs = 0

    for gtype, expected_n, gen_fn in configs:
        print(f"Benchmarking {gtype} (n~{expected_n})...", flush=True)
        g = gen_fn()
        nodes = g.nodes()
        if len(nodes) < 2:
            continue

        queries = generate_queries(g, N_QUERIES, seed=123)

        # Preprocess for BALT-H (skip for very small graphs)
        prep = BALTHPreprocessing(g, k_landmarks=min(8, len(nodes)),
                                  k_hubs=min(8, len(nodes)))

        rows = run_algorithms(g, queries, prep=prep, landmark_heur=True)
        for r in rows:
            r["graph_type"] = gtype
        all_rows.extend(rows)
        total_runs += len(rows)

    # Write CSV
    csv_path = "results/synthetic_results.csv"
    fieldnames = ["algorithm", "graph_type", "num_nodes", "num_edges",
                  "query_id", "runtime_ms", "nodes_expanded", "distance"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nWrote {total_runs} rows to {csv_path}")
    print(f"Unique configs: {len(configs)}")
    print(f"Total benchmark runs: {total_runs}")


if __name__ == "__main__":
    main()
