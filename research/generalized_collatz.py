"""Novel Direction 7: Phase transitions in the generalized Collatz family an+b."""

import os
import sys
import json
import math
import numpy as np
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

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


def generalized_collatz_test(n, a, b, max_iter=500000, max_val=10**15):
    """Test if n converges under T(n)=n/2 (even), T(n)=a*n+b (odd).

    Returns (converged, steps_or_cycle_length).
    """
    seen = set()
    current = n
    for step in range(max_iter):
        if current in seen:
            return True, step  # Found a cycle
        if current <= 0:
            return True, step
        seen.add(current)
        if current % 2 == 0:
            current = current // 2
        else:
            current = a * current + b
        if current > max_val:
            return False, step  # Diverged
    return False, max_iter  # Didn't converge in time


def run_phase_diagram(test_n=5000, max_iter=100000):
    """Compute phase diagram for generalized Collatz maps."""
    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    a_values = list(range(1, 22, 2))  # 1, 3, 5, ..., 21
    b_values = list(range(1, 22, 2))  # 1, 3, 5, ..., 21

    print(f"Computing phase diagram for a={a_values}, b={b_values}, test_n={test_n}...")

    convergence_fractions = np.zeros((len(a_values), len(b_values)))
    mean_escape_times = np.zeros((len(a_values), len(b_values)))

    for i, a in enumerate(a_values):
        for j, b in enumerate(b_values):
            n_converge = 0
            escape_times = []
            sample_ns = np.random.choice(range(1, test_n + 1), size=min(test_n, 2000), replace=False)
            for n in sample_ns:
                converged, steps = generalized_collatz_test(int(n), a, b, max_iter=max_iter)
                if converged:
                    n_converge += 1
                else:
                    escape_times.append(steps)

            frac = n_converge / len(sample_ns)
            convergence_fractions[i, j] = frac
            mean_escape_times[i, j] = np.mean(escape_times) if escape_times else max_iter

            if (i * len(b_values) + j) % 10 == 0:
                print(f"  a={a}, b={b}: convergence fraction = {frac:.3f}")

    # Phase diagram plot
    fig, ax = plt.subplots(figsize=(9, 7), constrained_layout=True)
    im = ax.imshow(convergence_fractions, cmap='RdYlGn', aspect='equal', origin='lower',
                   vmin=0, vmax=1, interpolation='nearest')
    ax.set_xticks(range(len(b_values)))
    ax.set_xticklabels(b_values)
    ax.set_yticks(range(len(a_values)))
    ax.set_yticklabels(a_values)
    ax.set_xlabel("b (odd additive parameter)")
    ax.set_ylabel("a (odd multiplicative parameter)")
    ax.set_title("Phase Diagram: Convergence Fraction of Generalized Collatz Maps T(n)=an+b")

    # Annotate cells
    for i in range(len(a_values)):
        for j in range(len(b_values)):
            val = convergence_fractions[i, j]
            color = 'white' if val < 0.5 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center', fontsize=7, color=color)

    cbar = plt.colorbar(im, ax=ax, label='Convergence Fraction')
    plt.savefig("figures/phase_diagram.png", dpi=300)
    plt.savefig("figures/phase_diagram.pdf")
    plt.close()

    # Identify critical boundary
    # For each b, find the a value where convergence transitions
    critical_pairs = []
    for j, b in enumerate(b_values):
        for i in range(len(a_values) - 1):
            f1 = convergence_fractions[i, j]
            f2 = convergence_fractions[i + 1, j]
            if f1 > 0.5 and f2 < 0.5:
                critical_pairs.append((a_values[i], a_values[i + 1], b))

    # Near-critical escape time analysis
    print("\nAnalyzing near-critical regions...")
    critical_analysis = []
    # Focus on the boundary region around a=3 (known convergent) to a=5 (divergent)
    for b in [1, 3, 5]:
        escape_times_by_a = {}
        fine_a_values = [3, 5, 7, 9, 11]
        for a in fine_a_values:
            times = []
            for n in range(1, min(test_n, 5000) + 1):
                converged, steps = generalized_collatz_test(n, a, b, max_iter=max_iter)
                if not converged:
                    times.append(steps)
            mean_et = np.mean(times) if times else 0
            escape_times_by_a[a] = mean_et
            critical_analysis.append({"a": a, "b": b, "mean_escape_time": float(mean_et),
                                       "n_divergent": len(times)})

    # Box-counting dimension of boundary (simplified)
    # Use the convergence fraction matrix to estimate boundary complexity
    # The boundary consists of cells where 0.1 < fraction < 0.9
    boundary_cells = np.sum((convergence_fractions > 0.1) & (convergence_fractions < 0.9))
    total_cells = convergence_fractions.size
    boundary_fraction = boundary_cells / total_cells

    # Escape time plot
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    im2 = ax.imshow(np.log10(mean_escape_times + 1), cmap='inferno', aspect='equal',
                     origin='lower', interpolation='nearest')
    ax.set_xticks(range(len(b_values)))
    ax.set_xticklabels(b_values)
    ax.set_yticks(range(len(a_values)))
    ax.set_yticklabels(a_values)
    ax.set_xlabel("b")
    ax.set_ylabel("a")
    ax.set_title("Mean Escape Time (log₁₀ scale)")
    plt.colorbar(im2, ax=ax, label='log₁₀(Mean Escape Time)')
    plt.savefig("figures/escape_time_map.png", dpi=300)
    plt.savefig("figures/escape_time_map.pdf")
    plt.close()

    results = {
        "test_n": test_n,
        "max_iter": max_iter,
        "seed": SEED,
        "a_values": a_values,
        "b_values": b_values,
        "convergence_fractions": convergence_fractions.tolist(),
        "critical_pairs": critical_pairs,
        "boundary_fraction": float(boundary_fraction),
        "boundary_cells": int(boundary_cells),
        "critical_analysis": critical_analysis,
        "known_a3b1_converges": float(convergence_fractions[1, 0]),
        "known_a5b1_diverges": float(convergence_fractions[2, 0]),
    }

    with open("results/phase_transition.json", "w") as f:
        json.dump(results, f, indent=2)

    with open("results/phase_transition.md", "w") as f:
        f.write("# Phase Transitions in Generalized Collatz Family\n\n")
        f.write(f"## Parameters\n- test_n = {test_n}, max_iter = {max_iter}\n")
        f.write(f"- a ∈ {a_values}, b ∈ {b_values}\n\n")
        f.write("## Phase Diagram\n\n")
        f.write(f"- a=3, b=1 convergence: {results['known_a3b1_converges']:.3f} (expected ~1.0)\n")
        f.write(f"- a=5, b=1 convergence: {results['known_a5b1_diverges']:.3f} (expected ~0.0)\n\n")
        f.write("## Critical Boundary\n\n")
        f.write(f"- Boundary cells (0.1 < frac < 0.9): {boundary_cells} / {total_cells}\n")
        f.write(f"- Boundary fraction: {boundary_fraction:.3f}\n\n")
        f.write("## Critical Transitions\n")
        for cp in critical_pairs:
            f.write(f"- b={cp[2]}: transition between a={cp[0]} (convergent) and a={cp[1]} (divergent)\n")
        f.write("\n## Escape Time Analysis Near Boundary\n\n")
        for ca in critical_analysis:
            f.write(f"- a={ca['a']}, b={ca['b']}: mean escape = {ca['mean_escape_time']:.0f}, ")
            f.write(f"n_divergent = {ca['n_divergent']}\n")

    print("\nPhase Diagram Results:")
    print(f"  a=3,b=1 convergence: {results['known_a3b1_converges']:.3f}")
    print(f"  a=5,b=1 convergence: {results['known_a5b1_diverges']:.3f}")
    print(f"  Boundary cells: {boundary_cells}/{total_cells}")
    return results


if __name__ == "__main__":
    results = run_phase_diagram(test_n=5000, max_iter=100000)
