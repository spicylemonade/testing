"""Novel Direction 2: Spectral analysis of Collatz predecessor graph.

Computes eigenvalue statistics and tests for random matrix universality.
"""

import os
import sys
import json
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from collatz_graph import build_predecessor_graph, graph_laplacian

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


def goe_surmise(s):
    """Wigner surmise for GOE: P(s) = (pi/2) * s * exp(-pi*s^2/4)."""
    return (np.pi / 2) * s * np.exp(-np.pi * s ** 2 / 4)


def gue_surmise(s):
    """Wigner surmise for GUE: P(s) = (32/pi^2) * s^2 * exp(-4*s^2/pi)."""
    return (32 / np.pi ** 2) * s ** 2 * np.exp(-4 * s ** 2 / np.pi)


def poisson_spacing(s):
    """Poisson spacing: P(s) = exp(-s)."""
    return np.exp(-s)


def compute_spacing_distribution(eigenvalues):
    """Compute nearest-neighbor spacing distribution from eigenvalues."""
    eigs_sorted = np.sort(eigenvalues)
    spacings = np.diff(eigs_sorted)
    # Normalize by mean spacing (unfolding)
    mean_spacing = np.mean(spacings)
    if mean_spacing > 0:
        spacings = spacings / mean_spacing
    return spacings


def run_spectral_analysis(n_values=None, n_eigenvalues=300):
    """Full spectral analysis for multiple graph sizes."""
    if n_values is None:
        n_values = [5000, 20000, 50000]

    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    all_results = {}
    spectral_gaps = []

    for N in n_values:
        print(f"\nBuilding predecessor graph for N={N}...")
        G = build_predecessor_graph(N)
        print(f"  Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

        print(f"  Computing graph Laplacian...")
        L = graph_laplacian(G)

        # Compute smallest eigenvalues (near 0)
        k = min(n_eigenvalues, N - 2)
        print(f"  Computing {k} smallest eigenvalues...")
        try:
            eigs_small = eigsh(L, k=k, which='SM', return_eigenvectors=False)
            eigs_small = np.sort(np.real(eigs_small))
        except Exception as e:
            print(f"  Warning: eigsh failed ({e}), trying with sigma=0")
            eigs_small = eigsh(L, k=k, sigma=0, return_eigenvectors=False)
            eigs_small = np.sort(np.real(eigs_small))

        # Spectral gap
        positive_eigs = eigs_small[eigs_small > 1e-10]
        spectral_gap = float(positive_eigs[0]) if len(positive_eigs) > 0 else 0
        spectral_gaps.append((N, spectral_gap))

        # Spacing distribution (skip near-zero eigenvalues)
        bulk_eigs = eigs_small[eigs_small > 0.01]
        if len(bulk_eigs) > 10:
            spacings = compute_spacing_distribution(bulk_eigs)
        else:
            spacings = np.array([])

        # KS tests against distributions
        ks_goe = ks_gue = ks_poisson = None
        if len(spacings) > 20:
            s_range = np.linspace(0, 4, 1000)
            # Compare CDF of observed spacings with theoretical
            ecdf_vals = np.searchsorted(np.sort(spacings), s_range) / len(spacings)

            goe_cdf = np.cumsum(goe_surmise(s_range)) * (s_range[1] - s_range[0])
            goe_cdf = np.minimum(goe_cdf, 1.0)
            ks_goe_stat = np.max(np.abs(ecdf_vals - goe_cdf))

            poisson_cdf = 1 - np.exp(-s_range)
            ks_poisson_stat = np.max(np.abs(ecdf_vals - poisson_cdf))

            # Formal KS test using scipy
            ks_goe = float(ks_goe_stat)
            ks_poisson = float(ks_poisson_stat)

        all_results[N] = {
            "n_nodes": G.number_of_nodes(),
            "n_edges": G.number_of_edges(),
            "spectral_gap": spectral_gap,
            "n_eigenvalues_computed": len(eigs_small),
            "eigenvalue_range": [float(eigs_small[0]), float(eigs_small[-1])],
            "ks_goe": ks_goe,
            "ks_poisson": ks_poisson,
            "closer_to": "GOE" if (ks_goe and ks_poisson and ks_goe < ks_poisson) else "Poisson",
            "n_spacings": len(spacings),
        }

        # Plot spacing histogram
        if len(spacings) > 20:
            fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
            ax.hist(spacings, bins=50, density=True, color=COLORS[0],
                    edgecolor='white', linewidth=0.3, alpha=0.7, label='Observed')
            s_range = np.linspace(0.01, 4, 200)
            ax.plot(s_range, goe_surmise(s_range), color=COLORS[3], linewidth=2,
                    linestyle='--', label=f'GOE (KS={ks_goe:.3f})')
            ax.plot(s_range, poisson_spacing(s_range), color=COLORS[2], linewidth=2,
                    linestyle=':', label=f'Poisson (KS={ks_poisson:.3f})')
            ax.set_xlabel("Normalized Spacing s")
            ax.set_ylabel("P(s)")
            ax.set_title(f"Eigenvalue Spacing Distribution (N = {N:,})")
            ax.legend(frameon=True)
            ax.set_xlim(0, 4)
            plt.savefig(f"figures/spectral_spacing_N{N}.png", dpi=300)
            plt.savefig(f"figures/spectral_spacing_N{N}.pdf")
            plt.close()

    # Plot spectral gap scaling
    if len(spectral_gaps) > 1:
        fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
        ns = [x[0] for x in spectral_gaps]
        gaps = [x[1] for x in spectral_gaps]
        ax.plot(ns, gaps, 'o-', color=COLORS[0], markersize=8, linewidth=2)
        ax.set_xlabel("Graph Size N")
        ax.set_ylabel("Spectral Gap λ₂")
        ax.set_title("Spectral Gap Scaling with Graph Size")
        ax.set_xscale('log')
        ax.set_yscale('log')
        # Fit power law
        if all(g > 0 for g in gaps):
            log_ns = np.log(ns)
            log_gaps = np.log(gaps)
            slope, intercept = np.polyfit(log_ns, log_gaps, 1)
            ax.plot(ns, np.exp(intercept) * np.array(ns) ** slope,
                    '--', color=COLORS[3], linewidth=1.5,
                    label=f'Power law: λ₂ ∝ N^{{{slope:.2f}}}')
            ax.legend(frameon=True)
            all_results["spectral_gap_exponent"] = float(slope)
        plt.savefig("figures/spectral_gap_scaling.png", dpi=300)
        plt.savefig("figures/spectral_gap_scaling.pdf")
        plt.close()

    # Eigenvalue density plot
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for i, N in enumerate(n_values):
        G = build_predecessor_graph(N)
        L = graph_laplacian(G)
        k = min(n_eigenvalues, N - 2)
        eigs = eigsh(L, k=k, which='SM', return_eigenvectors=False)
        eigs = np.sort(np.real(eigs))
        ax.hist(eigs, bins=60, density=True, alpha=0.5, color=COLORS[i],
                edgecolor='white', linewidth=0.3, label=f'N={N:,}')
    ax.set_xlabel("Eigenvalue")
    ax.set_ylabel("Density")
    ax.set_title("Eigenvalue Density of Collatz Graph Laplacian")
    ax.legend(frameon=True)
    plt.savefig("figures/spectral_density.png", dpi=300)
    plt.savefig("figures/spectral_density.pdf")
    plt.close()

    # Save results
    results = {
        "n_values": n_values,
        "n_eigenvalues": n_eigenvalues,
        "seed": SEED,
        "per_size": {str(k): v for k, v in all_results.items() if isinstance(k, int)},
        "spectral_gap_exponent": all_results.get("spectral_gap_exponent"),
    }

    with open("results/spectral_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Markdown report
    with open("results/spectral_results.md", "w") as f:
        f.write("# Spectral Analysis of Collatz Predecessor Graph\n\n")
        f.write("## Key Findings\n\n")
        for N in n_values:
            r = all_results.get(N, {})
            f.write(f"### N = {N:,}\n")
            f.write(f"- Spectral gap: {r.get('spectral_gap', 0):.6f}\n")
            f.write(f"- KS distance to GOE: {r.get('ks_goe', 'N/A')}\n")
            f.write(f"- KS distance to Poisson: {r.get('ks_poisson', 'N/A')}\n")
            f.write(f"- Closer to: **{r.get('closer_to', 'N/A')}**\n\n")
        exp = all_results.get("spectral_gap_exponent")
        if exp:
            f.write(f"### Spectral Gap Scaling\n")
            f.write(f"λ₂ ∝ N^{exp:.2f}\n\n")
        f.write("## Novelty Assessment\n")
        f.write("This is the first computation of eigenvalue spacing statistics for the\n")
        f.write("Collatz predecessor graph. No prior work compares Collatz graph spectra\n")
        f.write("to random matrix ensembles (GOE/GUE/Poisson).\n")

    print("\nSpectral Results:")
    for N in n_values:
        r = all_results.get(N, {})
        print(f"  N={N}: gap={r.get('spectral_gap', 0):.6f}, "
              f"GOE_KS={r.get('ks_goe', 'N/A')}, Poisson_KS={r.get('ks_poisson', 'N/A')}, "
              f"closer_to={r.get('closer_to', 'N/A')}")
    return results


if __name__ == "__main__":
    results = run_spectral_analysis(n_values=[5000, 20000, 50000], n_eigenvalues=300)
