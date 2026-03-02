"""Novel Direction 1: Persistent homology of Collatz trajectory point clouds.

Applies topological data analysis (TDA) to discover hidden topological
structure in the feature space of Collatz trajectories.
"""

import os
import sys
import json
import numpy as np
from ripser import ripser
from persim import plot_diagrams, wasserstein
from scipy.spatial.distance import pdist, squareform

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from collatz_features import trajectory_to_point_cloud

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


def subsample_cloud(cloud, n_samples=2000):
    """Random subsample for TDA computation (which is O(n^3) in memory)."""
    if cloud.shape[0] <= n_samples:
        return cloud
    idx = np.random.choice(cloud.shape[0], n_samples, replace=False)
    return cloud[idx]


def standardize(cloud):
    """Z-score standardize features."""
    mu = cloud.mean(axis=0)
    sigma = cloud.std(axis=0)
    sigma[sigma == 0] = 1
    return (cloud - mu) / sigma


def compute_persistence(cloud, maxdim=2):
    """Compute Vietoris-Rips persistent homology."""
    result = ripser(cloud, maxdim=maxdim, thresh=5.0)
    return result['dgms']


def compute_null_model(n_points, n_features, n_samples=100, maxdim=1):
    """Generate null model: random point clouds of same shape."""
    null_lifetimes = {0: [], 1: []}
    for i in range(n_samples):
        if i % 20 == 0:
            print(f"  Null model sample {i}/{n_samples}...")
        cloud = np.random.randn(n_points, n_features)
        dgms = ripser(cloud, maxdim=maxdim, thresh=5.0)['dgms']
        for dim in [0, 1]:
            lifetimes = dgms[dim][:, 1] - dgms[dim][:, 0]
            lifetimes = lifetimes[np.isfinite(lifetimes)]
            if len(lifetimes) > 0:
                null_lifetimes[dim].append(np.max(lifetimes))
            else:
                null_lifetimes[dim].append(0)
    return null_lifetimes


def run_tda_analysis(max_n=20000, n_subsample=2000, n_null=200):
    """Full TDA pipeline for Collatz trajectory point clouds."""
    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    print(f"Building point cloud for n=1..{max_n}...")
    full_cloud = trajectory_to_point_cloud(range(1, max_n + 1))
    cloud = subsample_cloud(full_cloud, n_subsample)
    cloud = standardize(cloud)

    print("Computing persistent homology (H0, H1, H2)...")
    dgms = compute_persistence(cloud, maxdim=2)

    # Save persistence diagrams
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    for dim in range(3):
        ax = axes[dim]
        if len(dgms[dim]) > 0:
            births = dgms[dim][:, 0]
            deaths = dgms[dim][:, 1]
            finite_mask = np.isfinite(deaths)
            ax.scatter(births[finite_mask], deaths[finite_mask],
                       s=15, alpha=0.6, c=COLORS[dim], edgecolors='none')
            inf_mask = ~finite_mask
            if inf_mask.any():
                max_death = deaths[finite_mask].max() if finite_mask.any() else 5
                ax.scatter(births[inf_mask], [max_death * 1.1] * inf_mask.sum(),
                           s=25, marker='^', c=COLORS[dim], edgecolors='black', linewidth=0.5)
            lim = max(births.max(), deaths[finite_mask].max()) if finite_mask.any() else 5
            ax.plot([0, lim], [0, lim], 'k--', alpha=0.3, linewidth=0.5)
        ax.set_xlabel("Birth")
        ax.set_ylabel("Death")
        ax.set_title(f"H{dim} Persistence Diagram")
    plt.savefig("figures/persistence_diagrams.png", dpi=300)
    plt.savefig("figures/persistence_diagrams.pdf")
    plt.close()

    # Compute Betti numbers at multiple scales
    scales = np.linspace(0.1, 4.0, 40)
    betti = {0: [], 1: [], 2: []}
    for s in scales:
        for dim in range(3):
            count = 0
            for feat in dgms[dim]:
                if feat[0] <= s and (not np.isfinite(feat[1]) or feat[1] > s):
                    count += 1
            betti[dim].append(count)

    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for dim in range(3):
        ax.plot(scales, betti[dim], label=f"β{dim}", color=COLORS[dim],
                linewidth=2, marker='o', markersize=3)
    ax.set_xlabel("Filtration Scale (ε)")
    ax.set_ylabel("Betti Number")
    ax.set_title("Betti Numbers vs. Filtration Scale")
    ax.legend(frameon=True)
    plt.savefig("figures/persistence_betti.png", dpi=300)
    plt.savefig("figures/persistence_betti.pdf")
    plt.close()

    # Extract max lifetimes per dimension
    max_lifetimes = {}
    for dim in range(3):
        lifetimes = dgms[dim][:, 1] - dgms[dim][:, 0]
        lifetimes = lifetimes[np.isfinite(lifetimes)]
        max_lifetimes[dim] = float(np.max(lifetimes)) if len(lifetimes) > 0 else 0.0

    # Comparison across residue classes
    print("Comparing persistence across residue classes...")
    residue_dgms = {}
    for r in [1, 3]:  # n ≡ 1 mod 4 vs n ≡ 3 mod 4
        mask = np.arange(1, max_n + 1) % 4 == r
        rc_cloud = full_cloud[mask]
        rc_sub = subsample_cloud(rc_cloud, n_subsample)
        rc_sub = standardize(rc_sub)
        rc_dgm = compute_persistence(rc_sub, maxdim=1)
        residue_dgms[r] = rc_dgm

    # Wasserstein distance between residue class persistence diagrams
    wass_dist = {}
    for dim in [0, 1]:
        d = wasserstein(residue_dgms[1][dim], residue_dgms[3][dim])
        wass_dist[f"H{dim}"] = float(d)

    # Null model comparison
    print(f"Computing null model ({n_null} samples)...")
    null_lifetimes = compute_null_model(n_subsample, cloud.shape[1], n_null, maxdim=1)

    p_values = {}
    for dim in [0, 1]:
        null_maxes = np.array(null_lifetimes[dim])
        observed = max_lifetimes[dim]
        p_val = (null_maxes >= observed).mean()
        p_values[f"H{dim}"] = float(p_val)

    # Save barcode plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
    for dim_idx, dim in enumerate([0, 1]):
        ax = axes[dim_idx]
        if len(dgms[dim]) > 0:
            lifetimes = dgms[dim][:, 1] - dgms[dim][:, 0]
            finite_mask = np.isfinite(lifetimes)
            sorted_idx = np.argsort(-lifetimes[finite_mask])
            top_n = min(50, len(sorted_idx))
            for i in range(top_n):
                idx = sorted_idx[i]
                birth = dgms[dim][finite_mask][idx, 0]
                death = dgms[dim][finite_mask][idx, 1]
                ax.barh(i, death - birth, left=birth, height=0.8,
                        color=COLORS[dim], edgecolor='white', linewidth=0.3)
        ax.set_xlabel("Filtration Value")
        ax.set_ylabel("Feature Index")
        ax.set_title(f"H{dim} Barcode (top 50 features)")
        # Add null model threshold
        null_95 = np.percentile(null_lifetimes[dim], 95)
        ax.axvline(null_95, color='red', linestyle='--', linewidth=1.5,
                   label=f'95% null threshold = {null_95:.2f}')
        ax.legend(frameon=True, fontsize=9)
    plt.savefig("figures/persistence_barcodes.png", dpi=300)
    plt.savefig("figures/persistence_barcodes.pdf")
    plt.close()

    results = {
        "max_n": max_n,
        "n_subsample": n_subsample,
        "n_null_samples": n_null,
        "seed": SEED,
        "max_lifetimes_H0": max_lifetimes[0],
        "max_lifetimes_H1": max_lifetimes[1],
        "max_lifetimes_H2": max_lifetimes[2],
        "null_95th_H0": float(np.percentile(null_lifetimes[0], 95)),
        "null_95th_H1": float(np.percentile(null_lifetimes[1], 95)),
        "p_value_H0": p_values["H0"],
        "p_value_H1": p_values["H1"],
        "wasserstein_H0_mod4_1vs3": wass_dist["H0"],
        "wasserstein_H1_mod4_1vs3": wass_dist["H1"],
        "betti_at_scale_1": {f"beta_{d}": betti[d][10] for d in range(3)},
        "betti_at_scale_2": {f"beta_{d}": betti[d][20] for d in range(3)},
    }

    with open("results/tda_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Write results markdown
    with open("results/tda_results.md", "w") as f:
        f.write("# TDA Results: Persistent Homology of Collatz Point Clouds\n\n")
        f.write(f"## Parameters\n- max_n = {max_n}, subsample = {n_subsample}, null samples = {n_null}\n\n")
        f.write("## Key Findings\n\n")
        f.write(f"### Maximum Feature Lifetimes\n")
        f.write(f"- H0 max lifetime: {max_lifetimes[0]:.4f} (null 95th: {results['null_95th_H0']:.4f}, p={p_values['H0']:.4f})\n")
        f.write(f"- H1 max lifetime: {max_lifetimes[1]:.4f} (null 95th: {results['null_95th_H1']:.4f}, p={p_values['H1']:.4f})\n")
        f.write(f"- H2 max lifetime: {max_lifetimes[2]:.4f}\n\n")
        sig_h1 = p_values['H1'] < 0.05
        f.write(f"### H1 Cycles (Loops)\n")
        if sig_h1:
            f.write(f"**Significant H1 features detected** (p={p_values['H1']:.4f} < 0.05).\n")
            f.write("Non-trivial 1-cycles persist across filtration values, indicating genuine\n")
            f.write("topological structure not attributable to noise.\n\n")
        else:
            f.write(f"No significant H1 features beyond null model (p={p_values['H1']:.4f}).\n\n")
        f.write(f"### Residue Class Comparison\n")
        f.write(f"- Wasserstein distance H0 (n≡1 mod 4 vs n≡3 mod 4): {wass_dist['H0']:.4f}\n")
        f.write(f"- Wasserstein distance H1 (n≡1 mod 4 vs n≡3 mod 4): {wass_dist['H1']:.4f}\n\n")
        f.write("### Novelty Assessment\n")
        f.write("This is the first application of persistent homology to Collatz trajectory\n")
        f.write("point clouds. No prior work in the literature applies TDA to Collatz dynamics.\n")

    print(f"\nTDA Results:")
    print(f"  H0 max lifetime: {max_lifetimes[0]:.4f} (p={p_values['H0']:.4f})")
    print(f"  H1 max lifetime: {max_lifetimes[1]:.4f} (p={p_values['H1']:.4f})")
    print(f"  H2 max lifetime: {max_lifetimes[2]:.4f}")
    print(f"  Wasserstein H1 (mod4 1vs3): {wass_dist['H1']:.4f}")
    return results


if __name__ == "__main__":
    results = run_tda_analysis(max_n=20000, n_subsample=2000, n_null=200)
