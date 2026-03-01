"""Generate publication-quality figures from benchmark results.

Produces 5+ figures in figures/ as both PNG and PDF:
1. Runtime comparison bar chart across graph types
2. Scalability log-log plot with fitted complexity curves
3. Nodes-expanded comparison
4. Speedup heatmap across graph type and size
5. Preprocessing time analysis
"""

import csv
import math
import os
import sys
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Colorblind-friendly palette (Wong 2011)
COLORS = {
    "dijkstra_p2p": "#0072B2",         # blue
    "dijkstra_bidirectional": "#56B4E9", # sky blue
    "astar_landmark": "#009E73",         # green
    "balth": "#D55E00",                  # vermillion
    "balth_no_opt": "#CC79A7",           # pink
}

LABELS = {
    "dijkstra_p2p": "Dijkstra P2P",
    "dijkstra_bidirectional": "Bidir. Dijkstra",
    "astar_landmark": "A* Landmark",
    "balth": "BALT-H",
    "balth_no_opt": "BALT-H (no opt)",
}


def load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def save_fig(fig, name):
    """Save figure as both PNG and PDF."""
    fig.savefig(f"figures/{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(f"figures/{name}.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved figures/{name}.png and .pdf")


def fig1_runtime_comparison():
    """Bar chart: average runtime by algorithm across major graph types."""
    data = load_csv("results/synthetic_results.csv")

    # Group selected graph types
    selected = {
        "grid": [r for r in data if r["graph_type"].startswith("grid") and int(r["num_nodes"]) >= 2500],
        "er_sparse": [r for r in data if "er_" in r["graph_type"] and int(r["num_nodes"]) >= 500
                      and float(r["graph_type"].split("_")[-1]) <= 0.01],
        "ba": [r for r in data if r["graph_type"].startswith("ba_") and int(r["num_nodes"]) >= 500],
    }

    algs = ["dijkstra_p2p", "dijkstra_bidirectional", "astar_landmark", "balth"]
    graph_labels = ["Grid (2500+)", "ER Sparse (500+)", "BA Scale-Free (500+)"]

    means = {a: [] for a in algs}
    for gkey in ["grid", "er_sparse", "ba"]:
        for alg in algs:
            vals = [float(r["runtime_ms"]) for r in selected[gkey] if r["algorithm"] == alg]
            means[alg].append(sum(vals) / len(vals) if vals else 0)

    x = np.arange(len(graph_labels))
    width = 0.2
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, alg in enumerate(algs):
        bars = ax.bar(x + i * width, means[alg], width,
                      label=LABELS[alg], color=COLORS[alg])

    ax.set_ylabel("Average Query Time (ms)", fontsize=12)
    ax.set_title("Runtime Comparison Across Graph Types", fontsize=14)
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(graph_labels, fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    save_fig(fig, "fig1_runtime_comparison")


def fig2_scalability():
    """Log-log scalability plot with fitted lines."""
    data = load_csv("results/scalability_results.csv")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for ax, family, title in zip(axes, ["grid", "ba"],
                                  ["Grid Graphs", "Barabási-Albert Graphs"]):
        fdata = [r for r in data if r["graph_family"] == family]

        for alg in ["dijkstra_p2p", "dijkstra_bidirectional", "balth"]:
            by_n = defaultdict(list)
            for r in fdata:
                if r["algorithm"] == alg:
                    by_n[int(r["num_nodes"])].append(float(r["runtime_ms"]))

            ns = sorted(by_n.keys())
            ts = [sum(by_n[n]) / len(by_n[n]) for n in ns]

            # Filter zeros
            valid = [(n, t) for n, t in zip(ns, ts) if t > 0 and n > 0]
            if not valid:
                continue
            ns, ts = zip(*valid)

            ax.loglog(ns, ts, "o-", color=COLORS[alg], label=LABELS[alg],
                     markersize=5, linewidth=2)

            # Fit line
            if len(ns) >= 3:
                log_n = [math.log(n) for n in ns]
                log_t = [math.log(t) for t in ts]
                n_pts = len(log_n)
                mean_ln = sum(log_n) / n_pts
                mean_lt = sum(log_t) / n_pts
                num = sum((log_n[i] - mean_ln) * (log_t[i] - mean_lt) for i in range(n_pts))
                den = sum((log_n[i] - mean_ln) ** 2 for i in range(n_pts))
                if den > 0:
                    exp = num / den
                    intercept = mean_lt - exp * mean_ln
                    fit_ns = np.logspace(math.log10(min(ns)), math.log10(max(ns)), 50)
                    fit_ts = [math.exp(intercept + exp * math.log(n)) for n in fit_ns]
                    ax.loglog(fit_ns, fit_ts, "--", color=COLORS[alg], alpha=0.5,
                             linewidth=1)
                    ax.annotate(f"O(n^{exp:.2f})", xy=(ns[-1], ts[-1]),
                               fontsize=8, color=COLORS[alg])

        ax.set_xlabel("Number of Nodes", fontsize=12)
        ax.set_ylabel("Query Time (ms)", fontsize=12)
        ax.set_title(f"Scalability: {title}", fontsize=13)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, which="both")

    fig.suptitle("Scalability Analysis (Log-Log Scale)", fontsize=15, y=1.02)
    fig.tight_layout()
    save_fig(fig, "fig2_scalability")


def fig3_nodes_expanded():
    """Bar chart: average nodes expanded by algorithm."""
    data = load_csv("results/synthetic_results.csv")

    # Use larger graphs for meaningful comparison
    selected = [r for r in data if int(r["num_nodes"]) >= 1000]

    algs = ["dijkstra_p2p", "dijkstra_bidirectional", "astar_landmark", "balth"]

    by_alg = defaultdict(list)
    for r in selected:
        if r["algorithm"] in algs:
            by_alg[r["algorithm"]].append(int(r["nodes_expanded"]))

    fig, ax = plt.subplots(figsize=(8, 5))
    means = [sum(by_alg[a]) / len(by_alg[a]) if by_alg[a] else 0 for a in algs]
    bars = ax.bar([LABELS[a] for a in algs], means,
                  color=[COLORS[a] for a in algs])

    ax.set_ylabel("Average Nodes Expanded", fontsize=12)
    ax.set_title("Search Efficiency: Nodes Expanded (n ≥ 1000)", fontsize=14)
    ax.grid(axis="y", alpha=0.3)

    # Add value labels
    for bar, val in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                f"{val:.0f}", ha="center", fontsize=10)

    save_fig(fig, "fig3_nodes_expanded")


def fig4_speedup_heatmap():
    """Heatmap: speedup of BALT-H vs Dijkstra P2P across graph type and size."""
    data = load_csv("results/synthetic_results.csv")

    # Compute speedup per (graph_type, query_id)
    by_gq = defaultdict(dict)
    for r in data:
        by_gq[(r["graph_type"], r["query_id"])][r["algorithm"]] = float(r["runtime_ms"])

    # Aggregate by graph_type
    speedups = defaultdict(list)
    for (gtype, qi), algs in by_gq.items():
        if "balth" in algs and "dijkstra_p2p" in algs and algs["balth"] > 0:
            speedups[gtype].append(algs["dijkstra_p2p"] / algs["balth"])

    # Organize into grid
    gtypes = sorted(speedups.keys())
    avg_speedups = [sum(speedups[g]) / len(speedups[g]) for g in gtypes]

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.barh(range(len(gtypes)), avg_speedups, color="#D55E00", alpha=0.8)
    ax.set_yticks(range(len(gtypes)))
    ax.set_yticklabels(gtypes, fontsize=9)
    ax.set_xlabel("Speedup (BALT-H vs Dijkstra P2P)", fontsize=12)
    ax.set_title("Speedup by Graph Configuration", fontsize=14)
    ax.axvline(x=1.0, color="black", linestyle="--", linewidth=1, alpha=0.5)
    ax.grid(axis="x", alpha=0.3)

    # Add value labels
    for bar, val in zip(bars, avg_speedups):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                f"{val:.2f}x", va="center", fontsize=9)

    fig.tight_layout()
    save_fig(fig, "fig4_speedup_heatmap")


def fig5_preprocessing_time():
    """Bar chart: preprocessing time vs total query time for different scales."""
    data = load_csv("results/scalability_results.csv")

    # Get BALT-H prep and query times per scale
    ba_data = [r for r in data if r["graph_family"] == "ba" and r["algorithm"] == "balth"]

    by_size = defaultdict(lambda: {"prep": 0, "query": []})
    for r in ba_data:
        n = int(r["num_nodes"])
        by_size[n]["prep"] = float(r["prep_time_ms"])
        by_size[n]["query"].append(float(r["runtime_ms"]))

    sizes = sorted(by_size.keys())
    prep_times = [by_size[n]["prep"] for n in sizes]
    avg_query = [sum(by_size[n]["query"]) / len(by_size[n]["query"]) for n in sizes]
    total_10q = [by_size[n]["prep"] + 10 * avg for n, avg in zip(sizes, avg_query)]

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(sizes))
    width = 0.35

    ax.bar(x - width / 2, prep_times, width, label="Preprocessing", color="#0072B2")
    ax.bar(x + width / 2, [10 * q for q in avg_query], width,
           label="10 Queries", color="#D55E00")

    ax.set_xlabel("Number of Nodes", fontsize=12)
    ax.set_ylabel("Time (ms)", fontsize=12)
    ax.set_title("BALT-H: Preprocessing vs Query Time (BA Graphs)", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in sizes], rotation=45, fontsize=9)
    ax.legend(fontsize=10)
    ax.set_yscale("log")
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    save_fig(fig, "fig5_preprocessing_time")


def fig6_realworld_comparison():
    """Grouped bar chart for real-world proxy datasets."""
    data = load_csv("results/realworld_results.csv")

    datasets = sorted(set(r["dataset"] for r in data))
    algs = ["dijkstra_p2p", "dijkstra_bidirectional", "astar_landmark", "balth"]

    fig, axes = plt.subplots(1, len(datasets), figsize=(14, 5), sharey=False)
    if len(datasets) == 1:
        axes = [axes]

    for ax, ds in zip(axes, datasets):
        means = []
        for alg in algs:
            vals = [float(r["runtime_ms"]) for r in data
                    if r["dataset"] == ds and r["algorithm"] == alg]
            means.append(sum(vals) / len(vals) if vals else 0)

        bars = ax.bar([LABELS[a] for a in algs], means,
                      color=[COLORS[a] for a in algs])
        ax.set_title(ds, fontsize=12)
        ax.set_ylabel("Avg Query Time (ms)", fontsize=10)
        ax.tick_params(axis="x", rotation=30, labelsize=9)
        ax.grid(axis="y", alpha=0.3)

    fig.suptitle("Real-World Proxy Dataset Performance", fontsize=14)
    fig.tight_layout()
    save_fig(fig, "fig6_realworld_comparison")


def main():
    os.makedirs("figures", exist_ok=True)

    print("Generating figures...")
    fig1_runtime_comparison()
    fig2_scalability()
    fig3_nodes_expanded()
    fig4_speedup_heatmap()
    fig5_preprocessing_time()
    fig6_realworld_comparison()
    print("Done! 6 figures generated.")


if __name__ == "__main__":
    main()
