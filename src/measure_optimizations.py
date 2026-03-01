"""Measure the independent effect of each BALT-H optimization.

Runs BALT-H with all combinations of optimizations enabled/disabled
across multiple graph types and sizes, reporting wall-clock time and
nodes expanded.
"""

import csv
import os
import random
import time
from typing import List, Tuple

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.graph import Graph
from src.novel_algorithm import BALTHPreprocessing, balth_query
from src.dijkstra import dijkstra_p2p


def generate_graphs(seed: int = 42) -> List[Tuple[str, Graph]]:
    """Generate a set of benchmark graphs."""
    graphs = []
    graphs.append(("grid_10x10", Graph.grid(10, 10, seed=seed)))
    graphs.append(("grid_20x20", Graph.grid(20, 20, seed=seed)))
    graphs.append(("grid_30x30", Graph.grid(30, 30, seed=seed)))
    graphs.append(("er_200_0.05", Graph.erdos_renyi(200, 0.05, seed=seed)))
    graphs.append(("er_500_0.03", Graph.erdos_renyi(500, 0.03, seed=seed)))
    graphs.append(("ba_200_3", Graph.barabasi_albert(200, m=3, seed=seed)))
    graphs.append(("ba_500_3", Graph.barabasi_albert(500, m=3, seed=seed)))
    return graphs


def measure_config(graph: Graph, prep: BALTHPreprocessing,
                   queries: List[Tuple[int, int]],
                   opt_active: bool, opt_settled: bool,
                   n_trials: int = 3) -> dict:
    """Measure average time and nodes expanded for a configuration."""
    total_time = 0.0
    total_expanded = 0
    total_queries = 0

    for _ in range(n_trials):
        for s, t in queries:
            t0 = time.perf_counter()
            d, exp = balth_query(graph, s, t, prep,
                                 opt_active_landmarks=opt_active,
                                 opt_settled_pruning=opt_settled)
            elapsed = time.perf_counter() - t0
            total_time += elapsed
            total_expanded += exp
            total_queries += 1

    return {
        "avg_time_ms": (total_time / total_queries) * 1000,
        "avg_expanded": total_expanded / total_queries,
    }


def main():
    rng = random.Random(42)
    graphs = generate_graphs(seed=42)

    configs = [
        ("none", False, False),
        ("active_landmarks", True, False),
        ("settled_pruning", False, True),
        ("both", True, True),
    ]

    os.makedirs("results", exist_ok=True)
    rows = []

    for gname, g in graphs:
        nodes = g.nodes()
        if len(nodes) < 2:
            continue

        # Generate 20 random queries
        queries = [(rng.choice(nodes), rng.choice(nodes)) for _ in range(20)]

        prep = BALTHPreprocessing(g, k_landmarks=8, k_hubs=8)

        # Also measure Dijkstra baseline for context
        t0 = time.perf_counter()
        dijk_expanded = 0
        for s, t in queries:
            d, exp = dijkstra_p2p(g, s, t)
            dijk_expanded += exp
        dijk_time = (time.perf_counter() - t0) / len(queries) * 1000
        dijk_expanded /= len(queries)

        rows.append({
            "graph": gname,
            "config": "dijkstra_baseline",
            "opt_active_landmarks": "N/A",
            "opt_settled_pruning": "N/A",
            "avg_time_ms": f"{dijk_time:.4f}",
            "avg_nodes_expanded": f"{dijk_expanded:.1f}",
        })

        for cname, opt_active, opt_settled in configs:
            result = measure_config(g, prep, queries, opt_active, opt_settled)
            rows.append({
                "graph": gname,
                "config": f"balth_{cname}",
                "opt_active_landmarks": str(opt_active),
                "opt_settled_pruning": str(opt_settled),
                "avg_time_ms": f"{result['avg_time_ms']:.4f}",
                "avg_nodes_expanded": f"{result['avg_expanded']:.1f}",
            })

    # Write CSV
    csv_path = "results/optimization_results.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "graph", "config", "opt_active_landmarks", "opt_settled_pruning",
            "avg_time_ms", "avg_nodes_expanded"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Results written to {csv_path}")
    print(f"\n{'Graph':<18} {'Config':<25} {'Time(ms)':<12} {'Expanded':<12}")
    print("-" * 70)
    for r in rows:
        print(f"{r['graph']:<18} {r['config']:<25} {r['avg_time_ms']:<12} {r['avg_nodes_expanded']:<12}")


if __name__ == "__main__":
    main()
