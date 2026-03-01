"""Scalability analysis: runtime vs graph size across multiple orders of magnitude.

Covers graph sizes from ~10 to ~40000 nodes (limited by pure Python performance).
Fits log-log curves to determine empirical complexity exponents.
Produces results/scalability_results.csv.
"""

import csv
import gc
import math
import os
import random
import sys
import time
from statistics import median

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.graph import Graph
from src.dijkstra import dijkstra_p2p, dijkstra_bidirectional
from src.novel_algorithm import BALTHPreprocessing, balth_query

SEED = 42
N_QUERIES = 10
N_REPS = 3


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


def log_fit(xs, ys):
    """Simple log-log linear fit: log(y) = a * log(x) + b. Returns exponent a."""
    if len(xs) < 2:
        return 0, 0
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys if y > 0]
    if len(ly) < 2:
        return 0, 0
    n = min(len(lx), len(ly))
    lx, ly = lx[:n], ly[:n]
    mean_lx = sum(lx) / n
    mean_ly = sum(ly) / n
    num = sum((lx[i] - mean_lx) * (ly[i] - mean_ly) for i in range(n))
    den = sum((lx[i] - mean_lx) ** 2 for i in range(n))
    if den == 0:
        return 0, mean_ly
    a = num / den
    b = mean_ly - a * mean_lx
    return a, b


def main():
    os.makedirs("results", exist_ok=True)

    # Grid scalability: 3x3 to 200x200
    grid_sides = [3, 5, 10, 20, 30, 50, 70, 100, 150, 200]

    # BA scalability: 10 to 40000
    ba_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000, 20000, 40000]

    all_rows = []

    for graph_family, sizes, gen_fn in [
        ("grid", grid_sides, lambda s: Graph.grid(s, s, seed=SEED)),
        ("ba", ba_sizes, lambda n: Graph.barabasi_albert(n, m=3, seed=SEED)),
    ]:
        print(f"\nScalability: {graph_family}", flush=True)
        for size in sizes:
            if graph_family == "grid":
                label = f"{size}x{size}"
                n_expected = size * size
            else:
                label = str(size)
                n_expected = size

            print(f"  {graph_family} {label} (n~{n_expected})...", flush=True)

            g = gen_fn(size)
            nodes = g.nodes()
            n_nodes = len(nodes)
            n_edges = sum(1 for u in nodes for _ in g.neighbors(u))
            if not g.directed:
                n_edges //= 2

            if n_nodes < 2:
                continue

            rng = random.Random(123)
            queries = [(rng.choice(nodes), rng.choice(nodes)) for _ in range(N_QUERIES)]

            # Skip A*/BALT-H preprocessing for very large graphs if too slow
            do_balth = n_nodes <= 40000

            if do_balth:
                t0 = time.perf_counter()
                prep = BALTHPreprocessing(g, k_landmarks=min(8, n_nodes),
                                          k_hubs=min(8, n_nodes))
                prep_ms = (time.perf_counter() - t0) * 1000
            else:
                prep = None
                prep_ms = 0

            for qi, (s, t) in enumerate(queries):
                # Dijkstra P2P
                ms, d, exp = time_query(lambda s=s, t=t: dijkstra_p2p(g, s, t))
                all_rows.append({
                    "graph_family": graph_family, "size_label": label,
                    "num_nodes": n_nodes, "num_edges": n_edges,
                    "algorithm": "dijkstra_p2p", "query_id": qi,
                    "runtime_ms": f"{ms:.4f}", "nodes_expanded": exp,
                    "prep_time_ms": "0",
                })

                # Bidirectional Dijkstra
                ms, d, exp = time_query(lambda s=s, t=t: dijkstra_bidirectional(g, s, t))
                all_rows.append({
                    "graph_family": graph_family, "size_label": label,
                    "num_nodes": n_nodes, "num_edges": n_edges,
                    "algorithm": "dijkstra_bidirectional", "query_id": qi,
                    "runtime_ms": f"{ms:.4f}", "nodes_expanded": exp,
                    "prep_time_ms": "0",
                })

                # BALT-H
                if do_balth and prep:
                    ms, d, exp = time_query(lambda s=s, t=t: balth_query(g, s, t, prep))
                    all_rows.append({
                        "graph_family": graph_family, "size_label": label,
                        "num_nodes": n_nodes, "num_edges": n_edges,
                        "algorithm": "balth", "query_id": qi,
                        "runtime_ms": f"{ms:.4f}", "nodes_expanded": exp,
                        "prep_time_ms": f"{prep_ms:.4f}",
                    })

    # Write CSV
    csv_path = "results/scalability_results.csv"
    fieldnames = ["graph_family", "size_label", "num_nodes", "num_edges",
                  "algorithm", "query_id", "runtime_ms", "nodes_expanded",
                  "prep_time_ms"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nWrote {len(all_rows)} rows to {csv_path}")

    # Compute empirical complexity exponents
    print("\nEmpirical complexity exponents (log-log fit):")
    from collections import defaultdict
    by_alg_family = defaultdict(lambda: defaultdict(list))
    for r in all_rows:
        key = (r["algorithm"], r["graph_family"])
        by_alg_family[key]["n"].append(int(r["num_nodes"]))
        by_alg_family[key]["t"].append(float(r["runtime_ms"]))

    for (alg, fam), data in sorted(by_alg_family.items()):
        # Average runtime per size
        by_n = defaultdict(list)
        for n, t in zip(data["n"], data["t"]):
            by_n[n].append(t)
        ns = sorted(by_n.keys())
        ts = [sum(by_n[n]) / len(by_n[n]) for n in ns]
        ts = [t for t in ts if t > 0]
        ns = ns[:len(ts)]
        if len(ns) >= 3:
            exp, _ = log_fit(ns, ts)
            print(f"  {alg:30s} on {fam:6s}: exponent = {exp:.2f}")


if __name__ == "__main__":
    main()
