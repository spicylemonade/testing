"""Novel Direction 3: Transfer matrix products and Lyapunov exponent distribution.

Encodes Collatz steps as 2x2 matrices and analyzes the distribution
of finite-time Lyapunov exponents.
"""

import os
import sys
import json
import numpy as np
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from collatz_engine import collatz_parity_sequence

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
mpl.rcParams.update({
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

SEED = 42
np.random.seed(SEED)
COLORS = sns.color_palette("deep")

# Transfer matrices
M_EVEN = np.array([[0.5, 0], [0, 1]], dtype=np.float64)
M_ODD = np.array([[3.0, 1.0], [0, 1]], dtype=np.float64)


def compute_lyapunov(n):
    """Compute finite-time Lyapunov exponent for starting value n."""
    ps = collatz_parity_sequence(n)
    T = len(ps)
    if T == 0:
        return 0.0, 0

    # Compute product using QR decomposition for numerical stability
    # Instead of full matrix product (overflow risk), accumulate log of norms
    log_norm_sum = 0.0
    R = np.eye(2)
    for i, c in enumerate(ps):
        M = M_ODD if c == '1' else M_EVEN
        R = M @ R
        # Periodically normalize to prevent overflow
        if (i + 1) % 50 == 0 or i == T - 1:
            norm = np.linalg.norm(R)
            if norm > 0:
                log_norm_sum += np.log(norm)
                R = R / norm

    lam = log_norm_sum / T
    return lam, T


def two_adic_valuation(n):
    """Compute v_2(n)."""
    if n == 0:
        return -1
    v = 0
    while n % 2 == 0:
        v += 1
        n //= 2
    return v


def popcount(n):
    """Count number of 1-bits in binary representation."""
    return bin(n).count('1')


def run_lyapunov_analysis(max_n=100000):
    """Full Lyapunov exponent analysis."""
    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    print(f"Computing Lyapunov exponents for n=1..{max_n}...")
    lambdas = np.zeros(max_n)
    stopping_times = np.zeros(max_n, dtype=int)
    v2_vals = np.zeros(max_n, dtype=int)
    popcount_vals = np.zeros(max_n, dtype=int)

    for n in range(1, max_n + 1):
        if n % 20000 == 0:
            print(f"  n = {n}...")
        lam, T = compute_lyapunov(n)
        lambdas[n - 1] = lam
        stopping_times[n - 1] = T
        v2_vals[n - 1] = two_adic_valuation(n)
        popcount_vals[n - 1] = popcount(n)

    # Exclude n=1 (trivial)
    lam_valid = lambdas[1:]  # n=2..max_n
    st_valid = stopping_times[1:]
    v2_valid = v2_vals[1:]
    pop_valid = popcount_vals[1:]

    # Basic statistics
    mean_lam = float(np.mean(lam_valid))
    std_lam = float(np.std(lam_valid))
    theoretical_lam = np.log(3 / 2) / 2  # ≈ 0.2027

    print(f"\nMean Lyapunov: {mean_lam:.6f} (theoretical: {theoretical_lam:.6f})")
    print(f"Std Lyapunov: {std_lam:.6f}")

    # Distribution fitting
    # Test: Normal
    ks_normal = stats.kstest(lam_valid, 'norm', args=(mean_lam, std_lam))

    # Plot distribution
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    ax.hist(lam_valid, bins=150, density=True, color=COLORS[0],
            edgecolor='white', linewidth=0.3, alpha=0.8, label='Observed')
    x = np.linspace(lam_valid.min(), lam_valid.max(), 300)
    ax.plot(x, stats.norm.pdf(x, mean_lam, std_lam), color=COLORS[3],
            linewidth=2, linestyle='--', label=f'Normal fit (μ={mean_lam:.4f}, σ={std_lam:.4f})')
    ax.axvline(theoretical_lam, color=COLORS[2], linewidth=2, linestyle=':',
               label=f'Theoretical log(3/2)/2 = {theoretical_lam:.4f}')
    ax.set_xlabel("Finite-Time Lyapunov Exponent λ(n)")
    ax.set_ylabel("Density")
    ax.set_title(f"Distribution of Lyapunov Exponents (N = {max_n:,})")
    ax.legend(frameon=True)
    plt.savefig("figures/lyapunov_distribution.png", dpi=300)
    plt.savefig("figures/lyapunov_distribution.pdf")
    plt.close()

    # Correlation with features
    corr_v2 = float(np.corrcoef(lam_valid, v2_valid)[0, 1])
    corr_pop = float(np.corrcoef(lam_valid, pop_valid)[0, 1])
    corr_st = float(np.corrcoef(lam_valid, st_valid)[0, 1])

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    for ax, (feat, name, corr) in zip(axes, [
        (v2_valid, "2-adic valuation v₂(n)", corr_v2),
        (pop_valid, "Bit count (popcount)", corr_pop),
        (st_valid, "Stopping time T(n)", corr_st),
    ]):
        # Subsample for visualization
        idx = np.random.choice(len(lam_valid), min(5000, len(lam_valid)), replace=False)
        ax.scatter(feat[idx], lam_valid[idx], s=3, alpha=0.3, color=COLORS[0], edgecolors='none')
        ax.set_xlabel(name)
        ax.set_ylabel("λ(n)")
        ax.set_title(f"ρ = {corr:.4f}")
    plt.suptitle("Lyapunov Exponent Correlations", fontweight='bold', fontsize=14)
    plt.savefig("figures/lyapunov_correlations.png", dpi=300)
    plt.savefig("figures/lyapunov_correlations.pdf")
    plt.close()

    # Identify outliers
    z_scores = (lam_valid - mean_lam) / std_lam
    outlier_high = np.where(z_scores > 4)[0] + 2  # +2 because we skipped n=1
    outlier_low = np.where(z_scores < -4)[0] + 2

    results = {
        "max_n": max_n,
        "seed": SEED,
        "mean_lyapunov": mean_lam,
        "std_lyapunov": std_lam,
        "theoretical_lyapunov": theoretical_lam,
        "deviation_from_theory": float(abs(mean_lam - theoretical_lam)),
        "ks_normal_statistic": float(ks_normal.statistic),
        "ks_normal_pvalue": float(ks_normal.pvalue),
        "correlation_v2": corr_v2,
        "correlation_popcount": corr_pop,
        "correlation_stopping_time": corr_st,
        "n_outliers_high": len(outlier_high),
        "n_outliers_low": len(outlier_low),
        "top_outliers_high": outlier_high[:10].tolist() if len(outlier_high) > 0 else [],
        "top_outliers_low": outlier_low[:10].tolist() if len(outlier_low) > 0 else [],
    }

    with open("results/lyapunov_results.json", "w") as f:
        json.dump(results, f, indent=2)

    with open("results/lyapunov_results.md", "w") as f:
        f.write("# Transfer Matrix Lyapunov Exponent Analysis\n\n")
        f.write(f"## Parameters\n- N = {max_n}\n\n")
        f.write("## Key Findings\n\n")
        f.write(f"- Mean Lyapunov exponent: **{mean_lam:.6f}** (theoretical: {theoretical_lam:.6f})\n")
        f.write(f"- Standard deviation: {std_lam:.6f}\n")
        f.write(f"- KS test vs Normal: stat={ks_normal.statistic:.4f}, p={ks_normal.pvalue:.2e}\n")
        f.write(f"- Correlation with 2-adic valuation: {corr_v2:.4f}\n")
        f.write(f"- Correlation with popcount: {corr_pop:.4f}\n")
        f.write(f"- Number of high outliers (z>4): {len(outlier_high)}\n\n")
        normal_ok = ks_normal.pvalue > 0.05
        f.write("## Interpretation\n\n")
        if not normal_ok:
            f.write("The Lyapunov exponent distribution **deviates significantly from Normal**.\n")
            f.write("This non-Gaussianity indicates the transfer matrix products are NOT\n")
            f.write("well-described by a simple random matrix model.\n")
        else:
            f.write("The distribution is consistent with Normal, supporting the random\n")
            f.write("multiplicative process model.\n")

    return results


if __name__ == "__main__":
    results = run_lyapunov_analysis(max_n=100000)
