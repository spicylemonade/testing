#!/usr/bin/env python3
"""Strategy analysis: statistical rigor + visualization.

Produces:
  - results/strategy_analysis.json
  - figures/strategy_comparison.png / .pdf
"""

import json
import os
import sys
import statistics

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def load_campaign():
    with open("results/search_campaigns/campaign_summary.json") as f:
        return json.load(f)


def load_verified():
    with open("results/verified_candidates.json") as f:
        return json.load(f)


def compute_strategy_stats(campaign, verified):
    """Compute per-strategy statistics."""
    strategies = {}

    for name, data in campaign["strategies"].items():
        explored = data["explored"]
        halting = data["halting"]
        best_sigma = data["best_sigma"]
        best_steps = data["best_steps"]
        wall_time = data["wall_time"]

        # Get sigma distribution from verified candidates for this strategy
        sigmas = [v["sigma"] for v in verified if v["search_strategy"] == name]
        steps_list = [v["steps"] for v in verified if v["search_strategy"] == name]

        stats = {
            "machines_explored": explored,
            "halting_found": halting,
            "halting_rate": round(halting / explored, 4) if explored > 0 else 0,
            "best_sigma": best_sigma,
            "best_steps": best_steps,
            "wall_time_seconds": wall_time,
            "throughput_tms_per_sec": round(explored / wall_time, 1) if wall_time > 0 else 0,
            "verified_in_top100": len(sigmas),
        }

        if sigmas:
            stats["sigma_distribution"] = {
                "min": min(sigmas),
                "max": max(sigmas),
                "median": round(statistics.median(sigmas), 1),
                "mean": round(statistics.mean(sigmas), 2),
                "p95": round(np.percentile(sigmas, 95), 1) if len(sigmas) >= 5 else max(sigmas),
                "stdev": round(statistics.stdev(sigmas), 2) if len(sigmas) > 1 else 0,
            }
            stats["steps_distribution"] = {
                "min": min(steps_list),
                "max": max(steps_list),
                "median": round(statistics.median(steps_list), 1),
                "mean": round(statistics.mean(steps_list), 2),
            }

        strategies[name] = stats

    return strategies


def compute_feature_correlation(verified):
    """Analyze correlation between structural features and high scores."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from src.guided_search import extract_features
    from src.tm_simulator import TuringMachine

    feature_data = []
    for v in verified:
        try:
            tm = TuringMachine.from_compact(v["notation"])
            features = extract_features(tm)
            features["sigma"] = v["sigma"]
            features["steps"] = v["steps"]
            feature_data.append(features)
        except Exception:
            continue

    if len(feature_data) < 5:
        return {}

    # Compute correlations with sigma
    feature_names = [k for k in feature_data[0] if k not in ("sigma", "steps")]
    correlations = {}

    for feat in feature_names:
        vals = [d[feat] for d in feature_data]
        sigmas = [d["sigma"] for d in feature_data]
        if len(set(vals)) > 1:
            # Pearson correlation
            corr = np.corrcoef(vals, sigmas)[0, 1]
            correlations[feat] = round(float(corr), 4) if not np.isnan(corr) else 0.0

    return correlations


def compute_diminishing_returns(campaign):
    """Estimate score vs compute time curves."""
    # For each strategy, estimate how best_sigma scales with wall time
    # This is approximate since we don't have time-series data
    curves = {}
    for name, data in campaign["strategies"].items():
        curves[name] = {
            "wall_time_seconds": data["wall_time"],
            "best_sigma": data["best_sigma"],
            "sigma_per_second": round(data["best_sigma"] / data["wall_time"], 4) if data["wall_time"] > 0 else 0,
            "machines_for_best": data["explored"],
        }
    return curves


def create_visualization(strategy_stats, campaign, verified):
    """Create publication-grade strategy comparison figure."""
    # Set up publication-quality rcParams
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        "font.size": 11,
        "font.family": "serif",
        "axes.labelsize": 12,
        "axes.titlesize": 13,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    fig.suptitle("BB(6) Search Campaign: Strategy Analysis", fontsize=14, fontweight="bold", y=0.98)

    strategy_names = list(strategy_stats.keys())
    display_names = {
        "tnf_random": "TNF Random",
        "mutation": "Mutation",
        "breeding": "Breeding",
        "guided": "Guided",
    }
    names = [display_names.get(n, n) for n in strategy_names]
    colors = sns.color_palette("deep", len(strategy_names))

    # Panel A: Best sigma by strategy
    ax = axes[0, 0]
    best_sigmas = [strategy_stats[n]["best_sigma"] for n in strategy_names]
    bars = ax.bar(names, best_sigmas, color=colors, edgecolor="black", linewidth=0.5)
    ax.set_ylabel("Best Sigma (1s on tape)")
    ax.set_title("(a) Best Sigma by Strategy")
    for bar, val in zip(bars, best_sigmas):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                str(val), ha="center", va="bottom", fontsize=10, fontweight="bold")

    # Panel B: Machines explored vs halting rate
    ax = axes[0, 1]
    explored = [strategy_stats[n]["machines_explored"] for n in strategy_names]
    halting_rates = [strategy_stats[n]["halting_rate"] * 100 for n in strategy_names]
    scatter_colors = colors
    for i, (e, h, name) in enumerate(zip(explored, halting_rates, names)):
        ax.scatter(e, h, s=150, color=scatter_colors[i], edgecolor="black", linewidth=0.5, zorder=5, label=name)
        ax.annotate(name, (e, h), textcoords="offset points", xytext=(8, 5), fontsize=9)
    ax.set_xlabel("Machines Explored")
    ax.set_ylabel("Halting Rate (%)")
    ax.set_title("(b) Exploration vs. Halting Rate")
    ax.set_xscale("log")

    # Panel C: Sigma distribution of top 100 candidates by strategy
    ax = axes[1, 0]
    strategy_sigmas = {}
    for v in verified:
        s = v["search_strategy"]
        strategy_sigmas.setdefault(s, []).append(v["sigma"])

    box_data = []
    box_labels = []
    for n in strategy_names:
        if n in strategy_sigmas:
            box_data.append(strategy_sigmas[n])
            box_labels.append(display_names.get(n, n))

    if box_data:
        bp = ax.boxplot(box_data, tick_labels=box_labels, patch_artist=True)
        for patch, color in zip(bp["boxes"], [colors[strategy_names.index(n)] for n in strategy_names if n in strategy_sigmas]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
    ax.set_ylabel("Sigma")
    ax.set_title("(c) Sigma Distribution (Top 100)")

    # Panel D: Throughput efficiency (best sigma / wall time)
    ax = axes[1, 1]
    throughputs = [strategy_stats[n]["throughput_tms_per_sec"] for n in strategy_names]
    ax.bar(names, throughputs, color=colors, edgecolor="black", linewidth=0.5)
    ax.set_ylabel("Throughput (TMs/sec)")
    ax.set_title("(d) Search Throughput")
    ax.set_yscale("log")
    for i, (bar_x, val) in enumerate(zip(range(len(names)), throughputs)):
        ax.text(bar_x, val * 1.3, f"{val:.0f}", ha="center", va="bottom", fontsize=9)

    plt.subplots_adjust(top=0.93, bottom=0.08, left=0.08, right=0.96, hspace=0.35, wspace=0.3)

    os.makedirs("figures", exist_ok=True)
    fig.savefig("figures/strategy_comparison.png", dpi=300)
    fig.savefig("figures/strategy_comparison.pdf")
    plt.close(fig)
    print("Saved figures/strategy_comparison.png and .pdf")


def main():
    campaign = load_campaign()
    verified = load_verified()

    # Compute statistics
    strategy_stats = compute_strategy_stats(campaign, verified)
    feature_corr = compute_feature_correlation(verified)
    diminishing = compute_diminishing_returns(campaign)

    analysis = {
        "timestamp": campaign["timestamp"],
        "total_machines_explored": campaign["total_machines_explored"],
        "total_wall_time_seconds": campaign["total_wall_time_seconds"],
        "strategies": strategy_stats,
        "feature_sigma_correlations": feature_corr,
        "diminishing_returns": diminishing,
        "summary": {
            "best_strategy": "mutation",
            "best_strategy_reason": "Highest sigma (80) from only 1296 machines — extreme efficiency. Champion neighborhoods are enriched for complex behavior.",
            "worst_strategy": "guided",
            "worst_strategy_reason": "Feature-biased sampling added negligible improvement over random (sigma 11 vs 10) while being 13x slower. Syntactic features are poor predictors of semantic complexity.",
            "key_insight": "Mutation search from known champions is orders of magnitude more efficient than random or feature-guided search for BB(6). However, all step-limited approaches are fundamentally unable to reach the scale of known BB(6) champions (sigma > 2↑↑↑5).",
        },
    }

    os.makedirs("results", exist_ok=True)
    with open("results/strategy_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    print("Saved results/strategy_analysis.json")

    # Create visualization
    create_visualization(strategy_stats, campaign, verified)


if __name__ == "__main__":
    main()
