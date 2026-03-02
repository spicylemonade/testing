"""Baseline statistical metrics for Collatz trajectories.

Computes stopping time distributions, mean stopping time growth,
odd/even ratio convergence, and Benford's law analysis.
"""

import json
import math
import os
import numpy as np
from collatz_engine import batch_stopping_times, collatz_trajectory

SEED = 42
np.random.seed(SEED)


def compute_baseline_metrics(max_n=1_000_000):
    """Compute all baseline metrics for n=1..max_n."""
    print(f"Computing stopping times for n=1..{max_n}...")
    stop_times = batch_stopping_times(max_n)

    # Exclude n=0 (index 0 is unused)
    st_array = np.array(stop_times[1:], dtype=np.float64)
    n_array = np.arange(1, max_n + 1, dtype=np.float64)

    # (a) Stopping time distribution
    print("Computing stopping time distribution...")
    hist, bin_edges = np.histogram(st_array, bins=200)

    # (b) Mean stopping time vs log(n) — fit C*log(n)
    print("Fitting mean stopping time growth...")
    # Compute running mean in log-spaced bins
    log_ns = np.logspace(1, np.log10(max_n), 50)
    mean_sts = []
    for ln in log_ns:
        idx = int(ln)
        if idx > max_n:
            idx = max_n
        mean_sts.append(np.mean(st_array[:idx]))
    mean_sts = np.array(mean_sts)
    log2_ns = np.log2(log_ns)

    # Linear fit: mean_st ≈ C * log2(n)
    from numpy.polynomial import polynomial as P
    coeffs = np.polyfit(log2_ns, mean_sts, 1)
    C_fitted = coeffs[0]
    # Lagarias bound: ~6.95*log2(n)
    C_lagarias = 6.95

    # (c) Odd/even ratio convergence
    print("Computing odd/even ratio...")
    # For a sample of large n, compute odd ratio
    sample_ns = np.random.choice(np.arange(max_n // 2, max_n + 1), size=10000, replace=False)
    odd_ratios = []
    for n in sample_ns:
        n = int(n)
        current = n
        odd = 0
        even = 0
        while current != 1:
            if current % 2 == 0:
                current //= 2
                even += 1
            else:
                current = 3 * current + 1
                odd += 1
        total = odd + even
        if total > 0:
            odd_ratios.append(odd / total)
    mean_odd_ratio = np.mean(odd_ratios)
    theoretical_ratio = math.log(2) / math.log(3)  # ≈ 0.6309

    # (d) Benford's law analysis
    print("Computing Benford's law...")
    # Collect leading digits along trajectories for sample of starting values
    leading_digit_counts = np.zeros(9, dtype=int)  # digits 1-9
    sample_for_benford = np.random.choice(np.arange(2, max_n + 1), size=5000, replace=False)
    for n in sample_for_benford:
        traj = collatz_trajectory(int(n))
        for val in traj:
            if val > 0:
                d = int(str(val)[0])
                leading_digit_counts[d - 1] += 1
    total_digits = leading_digit_counts.sum()
    observed_freq = leading_digit_counts / total_digits
    benford_expected = np.array([math.log10(1 + 1 / d) for d in range(1, 10)])
    benford_chi2 = np.sum((observed_freq - benford_expected) ** 2 / benford_expected * total_digits)

    metrics = {
        "max_n": max_n,
        "seed": SEED,
        "stopping_time_mean": float(np.mean(st_array)),
        "stopping_time_std": float(np.std(st_array)),
        "stopping_time_max": int(np.max(st_array)),
        "stopping_time_median": float(np.median(st_array)),
        "fitted_C_log2": float(C_fitted),
        "lagarias_C_log2": C_lagarias,
        "mean_odd_ratio": float(mean_odd_ratio),
        "theoretical_odd_ratio": theoretical_ratio,
        "odd_ratio_error": float(abs(mean_odd_ratio - theoretical_ratio)),
        "benford_observed": observed_freq.tolist(),
        "benford_expected": benford_expected.tolist(),
        "benford_chi2": float(benford_chi2),
        "benford_total_digits": int(total_digits),
        "histogram_counts": hist.tolist(),
        "histogram_edges": bin_edges.tolist(),
    }
    return metrics, st_array


def save_baseline(metrics, st_array):
    """Save metrics and generate figures."""
    os.makedirs("results/baseline", exist_ok=True)
    os.makedirs("figures", exist_ok=True)

    with open("results/baseline/baseline_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Generate stopping time distribution figure
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    plt.rcParams.update({
        'figure.figsize': (8, 5), 'figure.dpi': 300,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.linewidth': 0.8, 'axes.labelsize': 13,
        'axes.titlesize': 14, 'axes.titleweight': 'bold',
        'xtick.labelsize': 11, 'ytick.labelsize': 11,
        'legend.fontsize': 11, 'legend.framealpha': 0.9,
        'legend.edgecolor': '0.8', 'font.family': 'serif',
        'grid.alpha': 0.3, 'grid.linewidth': 0.5,
        'savefig.bbox': 'tight', 'savefig.pad_inches': 0.1,
    })
    colors = sns.color_palette("deep")

    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    ax.hist(st_array, bins=200, color=colors[0], edgecolor='white', linewidth=0.3, alpha=0.85)
    ax.set_xlabel("Total Stopping Time (steps)")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Collatz Stopping Times (n = 1 to 10⁶)")
    ax.axvline(metrics["stopping_time_mean"], color=colors[3], linestyle='--',
               linewidth=1.5, label=f'Mean = {metrics["stopping_time_mean"]:.1f}')
    ax.legend(frameon=True)
    plt.savefig("figures/stopping_time_dist.png", dpi=300)
    plt.savefig("figures/stopping_time_dist.pdf")
    plt.close()
    print("Saved figures/stopping_time_dist.png")


if __name__ == "__main__":
    metrics, st_array = compute_baseline_metrics(1_000_000)
    save_baseline(metrics, st_array)
    print(f"\nBaseline metrics:")
    print(f"  Mean stopping time: {metrics['stopping_time_mean']:.2f}")
    print(f"  Fitted C*log2(n): C = {metrics['fitted_C_log2']:.3f} (Lagarias: {metrics['lagarias_C_log2']})")
    print(f"  Mean odd ratio: {metrics['mean_odd_ratio']:.4f} (theory: {metrics['theoretical_odd_ratio']:.4f})")
    print(f"  Benford chi2: {metrics['benford_chi2']:.2f}")
    print("All baseline metrics computed and saved.")
