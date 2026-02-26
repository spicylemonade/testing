"""Generate scaling plot: BF vs BH interaction count and timing."""

import json
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    with open("results/benchmark_comparison.json") as f:
        data = json.load(f)

    benchmarks = data["force_evaluation_benchmark"]
    Ns = [b["N"] for b in benchmarks]
    bf_ints = [b["bf_interactions"] for b in benchmarks]
    bh_ints = [b["bh_interactions"] for b in benchmarks]
    bf_times = [b["bf_time_s"] for b in benchmarks]
    bh_times = [b["bh_time_s"] for b in benchmarks]

    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: interaction counts
    ax1.loglog(Ns, bf_ints, "o-", color="#e74c3c", label=r"Brute-force $O(N^2)$", linewidth=2, markersize=8)
    ax1.loglog(Ns, bh_ints, "s-", color="#3498db", label=r"Barnes-Hut $O(N\log N)$", linewidth=2, markersize=8)
    # Reference lines
    N_ref = np.array(Ns)
    ax1.loglog(N_ref, 0.5 * N_ref**2, "--", color="#e74c3c", alpha=0.3, label=r"$\propto N^2$")
    ax1.loglog(N_ref, 30 * N_ref * np.log2(N_ref), "--", color="#3498db", alpha=0.3, label=r"$\propto N\log N$")
    ax1.set_xlabel("Number of particles $N$")
    ax1.set_ylabel("Total interactions")
    ax1.set_title("Interaction Count Scaling")
    ax1.legend(fontsize=9)

    # Right: wall-clock time
    ax2.loglog(Ns, bf_times, "o-", color="#e74c3c", label="Brute-force (vectorized)", linewidth=2, markersize=8)
    ax2.loglog(Ns, bh_times, "s-", color="#3498db", label="Barnes-Hut (Python tree)", linewidth=2, markersize=8)
    ax2.set_xlabel("Number of particles $N$")
    ax2.set_ylabel("Wall-clock time (s)")
    ax2.set_title("Single Force Evaluation Timing")
    ax2.legend(fontsize=9)

    fig.suptitle("Barnes-Hut vs Brute-Force Scaling (θ = 0.5)", fontsize=14, y=1.02)
    fig.tight_layout()
    fig.savefig("figures/scaling_comparison.png", dpi=150, bbox_inches="tight")
    fig.savefig("figures/scaling_comparison.pdf", bbox_inches="tight")
    plt.close(fig)
    print("Saved figures/scaling_comparison.png and .pdf")


if __name__ == "__main__":
    main()
