"""Run benchmarks on real-world-proxy graph datasets.

Since DIMACS/SNAP downloads are not available in this environment, we generate
realistic proxy graphs that mimic real-world network properties:

1. Road network proxy: Large grid graphs with random weight perturbation
   (mimics planar, low-degree road networks like DIMACS NY/BAY)
2. Social network proxy: Barabási-Albert with parameters matching SNAP datasets
   (power-law degree distribution, small-world properties)

Each dataset gets 100 random source-target queries per the experiment plan.
Results saved to results/realworld_results.csv.
"""

import csv
import gc
import os
import random
import sys
import time
from statistics import median

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.graph import Graph
from src.dijkstra import dijkstra_p2p, dijkstra_bidirectional
from src.astar import astar_landmark
from src.novel_algorithm import BALTHPreprocessing, balth_query

SEED = 42
N_QUERIES = 100
N_REPS = 3


def generate_road_network_proxy(n_side=100, seed=42):
    """Generate a grid graph with random weight perturbation (road network proxy).

    Mimics DIMACS NY (264K nodes) at smaller scale. Grid structure gives planarity
    and low average degree (~4), characteristic of road networks.
    """
    g = Graph.grid(n_side, n_side, seed=seed)
    return g, f"road_proxy_{n_side}x{n_side}"


def generate_social_network_proxy(n=5000, m=5, seed=42):
    """Generate a BA graph (social network proxy).

    Mimics SNAP social network datasets (power-law degree, small diameter).
    m=5 gives average degree ~10, similar to Facebook ego-net statistics.
    """
    g = Graph.barabasi_albert(n, m=m, seed=seed)
    return g, f"social_proxy_{n}"


def generate_queries(graph, n_queries, seed):
    rng = random.Random(seed)
    nodes = graph.nodes()
    return [(rng.choice(nodes), rng.choice(nodes)) for _ in range(n_queries)]


def time_query(func, n_reps=N_REPS):
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


def benchmark_dataset(graph, dataset_name, queries):
    """Run all algorithms on the given dataset."""
    n_nodes = len(graph.nodes())
    n_edges = sum(1 for u in graph.nodes() for _ in graph.neighbors(u))
    if not graph.directed:
        n_edges //= 2

    print(f"  Preprocessing BALT-H...", flush=True)
    t0 = time.perf_counter()
    prep = BALTHPreprocessing(graph, k_landmarks=8, k_hubs=8)
    prep_time = (time.perf_counter() - t0) * 1000
    print(f"  Preprocessing done in {prep_time:.1f}ms", flush=True)

    rows = []
    for qi, (s, t) in enumerate(queries):
        if qi % 20 == 0:
            print(f"  Query {qi}/{len(queries)}...", flush=True)

        # Dijkstra P2P
        ms, d, exp = time_query(lambda s=s, t=t: dijkstra_p2p(graph, s, t))
        rows.append({
            "algorithm": "dijkstra_p2p", "dataset": dataset_name,
            "num_nodes": n_nodes, "num_edges": n_edges,
            "query_id": qi, "runtime_ms": f"{ms:.4f}",
            "nodes_expanded": exp, "distance": d,
        })

        # Bidirectional Dijkstra
        ms, d, exp = time_query(lambda s=s, t=t: dijkstra_bidirectional(graph, s, t))
        rows.append({
            "algorithm": "dijkstra_bidirectional", "dataset": dataset_name,
            "num_nodes": n_nodes, "num_edges": n_edges,
            "query_id": qi, "runtime_ms": f"{ms:.4f}",
            "nodes_expanded": exp, "distance": d,
        })

        # A* Landmark
        ms, d, exp = time_query(lambda s=s, t=t: astar_landmark(graph, s, t))
        rows.append({
            "algorithm": "astar_landmark", "dataset": dataset_name,
            "num_nodes": n_nodes, "num_edges": n_edges,
            "query_id": qi, "runtime_ms": f"{ms:.4f}",
            "nodes_expanded": exp, "distance": d,
        })

        # BALT-H
        ms, d, exp = time_query(lambda s=s, t=t: balth_query(graph, s, t, prep))
        rows.append({
            "algorithm": "balth", "dataset": dataset_name,
            "num_nodes": n_nodes, "num_edges": n_edges,
            "query_id": qi, "runtime_ms": f"{ms:.4f}",
            "nodes_expanded": exp, "distance": d,
        })

    return rows


def main():
    os.makedirs("results", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    all_rows = []

    # Dataset 1: Road network proxy
    print("Dataset 1: Road network proxy (100x100 grid)", flush=True)
    g1, name1 = generate_road_network_proxy(n_side=100, seed=SEED)
    queries1 = generate_queries(g1, N_QUERIES, seed=123)
    rows1 = benchmark_dataset(g1, name1, queries1)
    all_rows.extend(rows1)

    # Dataset 2: Social network proxy
    print("\nDataset 2: Social network proxy (5000 nodes, BA m=5)", flush=True)
    g2, name2 = generate_social_network_proxy(n=5000, m=5, seed=SEED)
    queries2 = generate_queries(g2, N_QUERIES, seed=123)
    rows2 = benchmark_dataset(g2, name2, queries2)
    all_rows.extend(rows2)

    # Write CSV
    csv_path = "results/realworld_results.csv"
    fieldnames = ["algorithm", "dataset", "num_nodes", "num_edges",
                  "query_id", "runtime_ms", "nodes_expanded", "distance"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nWrote {len(all_rows)} rows to {csv_path}")

    # Write data/README.md
    readme = """# Real-World Proxy Datasets

## Overview
Since DIMACS and SNAP datasets cannot be downloaded in the current environment,
we generate proxy graphs with matching structural properties.

## Dataset 1: Road Network Proxy
- **Generator:** `Graph.grid(100, 100, seed=42)` with random weight perturbation
- **Properties:** 10,000 nodes, ~19,800 edges, planar, avg degree ~4
- **Mimics:** DIMACS NY road network (264K nodes, 733K edges)
- **Key structural match:** Planarity, low degree, spatial locality

## Dataset 2: Social Network Proxy
- **Generator:** `Graph.barabasi_albert(5000, m=5, seed=42)`
- **Properties:** 5,000 nodes, ~24,985 edges, power-law degree distribution
- **Mimics:** SNAP Facebook ego-net (4K nodes) and similar social networks
- **Key structural match:** Power-law degree, small-world, high-degree hubs

## Reproduction
To download actual DIMACS/SNAP datasets for full evaluation:
1. DIMACS: http://www.diag.uniroma1.it/challenge9/download.shtml
   - Download NY.gr.gz, extract, use `Graph.from_dimacs("NY.gr")`
2. SNAP: https://snap.stanford.edu/data/
   - Download edge list, use `Graph.from_edgelist("dataset.txt")`
"""
    with open("data/README.md", "w") as f:
        f.write(readme)

    print("Wrote data/README.md")


if __name__ == "__main__":
    main()
