"""Benchmarking infrastructure for shortest path algorithms.

Measures wall-clock time, nodes expanded, peak memory, and path optimality.
Outputs results as CSV files in results/ directory.
"""

from __future__ import annotations

import csv
import json
import math
import os
import random
import resource
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

from src.graph import Graph
from src.dijkstra import (
    dijkstra_standard,
    dijkstra_decreasekey,
    dijkstra_bidirectional,
    dijkstra_p2p,
)
from src.astar import astar_euclidean, astar_landmark, LandmarkHeuristic

INF = float("inf")


def _peak_memory_mb() -> float:
    """Get peak resident memory in MB (Linux)."""
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_maxrss / 1024.0  # ru_maxrss is in KB on Linux


def generate_graph(graph_type: str, n: int, params: dict, seed: int = 42) -> Graph:
    """Generate a graph based on type name and size."""
    if graph_type == "erdos_renyi":
        p = params.get("p", 0.01)
        directed = params.get("directed", False)
        return Graph.erdos_renyi(n, p, seed=seed, directed=directed)
    elif graph_type == "grid":
        side = int(math.sqrt(n))
        return Graph.grid(side, side, seed=seed)
    elif graph_type == "barabasi_albert":
        m = params.get("m", 3)
        return Graph.barabasi_albert(n, m=m, seed=seed)
    elif graph_type == "complete":
        return Graph.complete(n, seed=seed)
    else:
        raise ValueError(f"Unknown graph type: {graph_type}")


def benchmark_sssp(graph: Graph, source: int,
                   algorithm: str) -> Dict[str, Any]:
    """Run a single SSSP benchmark and return metrics."""
    mem_before = _peak_memory_mb()
    t0 = time.perf_counter()

    if algorithm == "dijkstra_standard":
        dist, expanded = dijkstra_standard(graph, source)
    elif algorithm == "dijkstra_decreasekey":
        dist, expanded = dijkstra_decreasekey(graph, source)
    else:
        raise ValueError(f"Unknown SSSP algorithm: {algorithm}")

    elapsed = time.perf_counter() - t0
    mem_after = _peak_memory_mb()

    return {
        "runtime_ms": elapsed * 1000,
        "nodes_expanded": expanded,
        "peak_memory_mb": mem_after,
        "reachable_nodes": len(dist),
    }


def benchmark_p2p(graph: Graph, source: int, target: int,
                  algorithm: str, true_dist: float,
                  lm_heuristic: Optional[LandmarkHeuristic] = None
                  ) -> Dict[str, Any]:
    """Run a single point-to-point benchmark and return metrics."""
    mem_before = _peak_memory_mb()
    t0 = time.perf_counter()

    if algorithm == "dijkstra_p2p":
        dist, expanded = dijkstra_p2p(graph, source, target)
    elif algorithm == "dijkstra_bidirectional":
        dist, expanded = dijkstra_bidirectional(graph, source, target)
    elif algorithm == "astar_euclidean":
        dist, expanded = astar_euclidean(graph, source, target)
    elif algorithm == "astar_landmark":
        dist, expanded = astar_landmark(graph, source, target,
                                         precomputed=lm_heuristic)
    else:
        raise ValueError(f"Unknown P2P algorithm: {algorithm}")

    elapsed = time.perf_counter() - t0
    mem_after = _peak_memory_mb()

    optimality = dist / true_dist if true_dist > 0 and true_dist < INF else 1.0

    return {
        "runtime_ms": elapsed * 1000,
        "nodes_expanded": expanded,
        "peak_memory_mb": mem_after,
        "distance": dist,
        "optimality_ratio": optimality,
    }


def run_benchmarks(config_path: str = "benchmark_config.json",
                   output_path: str = "results/baseline_results.csv") -> None:
    """Run full benchmark suite from config file."""
    with open(config_path) as f:
        config = json.load(f)

    os.makedirs("results", exist_ok=True)
    seed = config.get("seed", 42)
    trials = config.get("trials_per_config", 10)

    rows = []
    sssp_algos = ["dijkstra_standard", "dijkstra_decreasekey"]
    p2p_algos = ["dijkstra_p2p", "dijkstra_bidirectional",
                 "astar_euclidean", "astar_landmark"]

    for gt in config["graph_types"]:
        for n in gt["sizes"]:
            print(f"  Generating {gt['name']} n={n}...")
            graph = generate_graph(gt["generator"], n, gt["params"], seed=seed)
            rng = random.Random(seed)
            nodes = graph.nodes()
            if not nodes:
                continue

            # Precompute landmark heuristic once per graph
            lm_nodes = [nodes[i * len(nodes) // 4] for i in range(4)]
            lm_heuristic = None

            # Run SSSP benchmarks
            for algo in sssp_algos:
                runtimes = []
                expansions = []
                for t in range(trials):
                    src = rng.choice(nodes)
                    result = benchmark_sssp(graph, src, algo)
                    runtimes.append(result["runtime_ms"])
                    expansions.append(result["nodes_expanded"])

                import statistics
                rows.append({
                    "algorithm": algo,
                    "graph_type": gt["name"],
                    "num_nodes": graph.num_nodes,
                    "num_edges": graph.num_edges,
                    "avg_runtime_ms": round(statistics.mean(runtimes), 4),
                    "std_runtime_ms": round(statistics.stdev(runtimes) if len(runtimes) > 1 else 0, 4),
                    "avg_nodes_expanded": round(statistics.mean(expansions), 1),
                    "peak_memory_mb": round(_peak_memory_mb(), 1),
                })

            # Generate source-target pairs for P2P
            pairs = []
            for t in range(trials):
                s, tgt = rng.choice(nodes), rng.choice(nodes)
                d_true, _ = dijkstra_p2p(graph, s, tgt)
                pairs.append((s, tgt, d_true))

            # Precompute landmark heuristic
            if any(a in config.get("algorithms", []) for a in ["astar_landmark"]):
                lm_heuristic = LandmarkHeuristic(graph, lm_nodes)

            for algo in p2p_algos:
                runtimes = []
                expansions = []
                for s, tgt, d_true in pairs:
                    result = benchmark_p2p(graph, s, tgt, algo, d_true,
                                           lm_heuristic=lm_heuristic)
                    runtimes.append(result["runtime_ms"])
                    expansions.append(result["nodes_expanded"])

                import statistics
                rows.append({
                    "algorithm": algo,
                    "graph_type": gt["name"],
                    "num_nodes": graph.num_nodes,
                    "num_edges": graph.num_edges,
                    "avg_runtime_ms": round(statistics.mean(runtimes), 4),
                    "std_runtime_ms": round(statistics.stdev(runtimes) if len(runtimes) > 1 else 0, 4),
                    "avg_nodes_expanded": round(statistics.mean(expansions), 1),
                    "peak_memory_mb": round(_peak_memory_mb(), 1),
                })

    # Write CSV
    if rows:
        fieldnames = list(rows[0].keys())
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Results written to {output_path} ({len(rows)} rows)")


if __name__ == "__main__":
    run_benchmarks()
