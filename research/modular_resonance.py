"""Novel Direction 5: Modular resonance scanner for Collatz stopping times.

Systematically discovers hidden periodicity in stopping_time(n) mod m.
"""

import os
import sys
import json
import math
import numpy as np
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from collatz_engine import batch_stopping_times

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


def is_power_of_2(n):
    return n > 0 and (n & (n - 1)) == 0


def is_smooth_23(n):
    """Check if n = 2^a * 3^b for some a, b >= 0."""
    while n % 2 == 0:
        n //= 2
    while n % 3 == 0:
        n //= 3
    return n == 1


def run_modular_resonance(max_n=500000, max_mod=500):
    """Systematic scan of stopping times mod m."""
    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    print(f"Computing stopping times for n=1..{max_n}...")
    st = batch_stopping_times(max_n)
    st_array = np.array(st[1:], dtype=np.int64)  # st_array[0] = stopping_time(1)

    print(f"Scanning moduli m=2..{max_mod}...")
    resonance_data = []

    for m in range(2, max_mod + 1):
        # Compute distribution of stopping_time mod m
        residues = st_array % m
        observed = np.bincount(residues, minlength=m)
        expected = max_n / m

        # Chi-squared test
        chi2 = np.sum((observed - expected) ** 2 / expected)
        dof = m - 1
        p_value = 1 - stats.chi2.cdf(chi2, dof)

        # Effect size (Cramér's V)
        cramers_v = math.sqrt(chi2 / (max_n * (m - 1))) if m > 1 else 0

        # Classify modulus
        is_pow2 = is_power_of_2(m)
        is_23smooth = is_smooth_23(m)
        coprime_to_6 = math.gcd(m, 6) == 1
        is_prime = all(m % i != 0 for i in range(2, int(math.sqrt(m)) + 1)) and m > 1

        resonance_data.append({
            "modulus": m,
            "chi2": float(chi2),
            "dof": dof,
            "p_value": float(p_value),
            "cramers_v": float(cramers_v),
            "is_power_of_2": is_pow2,
            "is_23smooth": is_23smooth,
            "coprime_to_6": coprime_to_6,
            "is_prime": is_prime,
            "observed_max_deviation": float(np.max(np.abs(observed - expected)) / expected),
        })

    # Sort by effect size
    resonance_data.sort(key=lambda x: -x["cramers_v"])

    # Identify top resonances
    bonferroni_threshold = 1e-10 / max_mod
    significant = [d for d in resonance_data if d["p_value"] < bonferroni_threshold]
    novel_resonances = [d for d in significant if d["coprime_to_6"] and not d["is_23smooth"]]

    print(f"\nTotal significant moduli (p < {bonferroni_threshold:.1e}): {len(significant)}")
    print(f"Novel resonances (coprime to 6): {len(novel_resonances)}")

    # Plot top 20 resonant moduli
    top_20 = resonance_data[:20]
    for i, d in enumerate(top_20[:8]):  # Save figures for top 8
        m = d["modulus"]
        residues = st_array % m
        observed = np.bincount(residues, minlength=m)

        fig, ax = plt.subplots(figsize=(max(8, m * 0.15), 5), constrained_layout=True)
        bars = ax.bar(range(m), observed, color=COLORS[0], edgecolor='white', linewidth=0.3)
        ax.axhline(max_n / m, color=COLORS[3], linestyle='--', linewidth=1.5,
                    label=f'Expected (uniform) = {max_n/m:.0f}')
        ax.set_xlabel(f"Stopping Time mod {m}")
        ax.set_ylabel("Count")
        tag = ""
        if d["is_power_of_2"]:
            tag = " [power of 2]"
        elif d["is_23smooth"]:
            tag = " [{2,3}-smooth]"
        elif d["coprime_to_6"]:
            tag = " [coprime to 6 — NOVEL]"
        ax.set_title(f"Stopping Time Distribution mod {m}{tag} (V={d['cramers_v']:.3f})")
        ax.legend(frameon=True)
        plt.savefig(f"figures/resonance_mod_{m}.png", dpi=300)
        plt.close()

    # Overview plot: Cramér's V vs modulus
    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
    mods = [d["modulus"] for d in resonance_data]
    vs = [d["cramers_v"] for d in resonance_data]
    colors_scatter = []
    for d in resonance_data:
        if d["is_power_of_2"]:
            colors_scatter.append(COLORS[3])
        elif d["is_23smooth"]:
            colors_scatter.append(COLORS[1])
        elif d["coprime_to_6"] and d["p_value"] < bonferroni_threshold:
            colors_scatter.append(COLORS[2])
        else:
            colors_scatter.append(COLORS[0])

    # Sort by modulus for plotting
    sorted_data = sorted(resonance_data, key=lambda x: x["modulus"])
    ax.scatter([d["modulus"] for d in sorted_data],
               [d["cramers_v"] for d in sorted_data],
               c=[COLORS[3] if d["is_power_of_2"] else
                  COLORS[1] if d["is_23smooth"] else
                  COLORS[2] if (d["coprime_to_6"] and d["p_value"] < bonferroni_threshold) else
                  COLORS[0] for d in sorted_data],
               s=20, alpha=0.7, edgecolors='none')
    ax.set_xlabel("Modulus m")
    ax.set_ylabel("Cramér's V (effect size)")
    ax.set_title("Modular Resonance Scan: Non-uniformity of Stopping Times mod m")
    # Custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS[3], label='Power of 2'),
        Patch(facecolor=COLORS[1], label='{2,3}-smooth'),
        Patch(facecolor=COLORS[2], label='Coprime to 6 (novel)'),
        Patch(facecolor=COLORS[0], label='Other'),
    ]
    ax.legend(handles=legend_elements, frameon=True, loc='upper right')
    plt.savefig("figures/resonance_overview.png", dpi=300)
    plt.savefig("figures/resonance_overview.pdf")
    plt.close()

    # Save results
    results = {
        "max_n": max_n,
        "max_mod": max_mod,
        "seed": SEED,
        "n_significant": len(significant),
        "n_novel_coprime6": len(novel_resonances),
        "bonferroni_threshold": bonferroni_threshold,
        "top_20_resonances": top_20,
        "novel_resonances": novel_resonances[:20],
        "all_resonances": sorted(resonance_data, key=lambda x: x["modulus"]),
    }

    with open("results/resonance_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Markdown report
    with open("results/resonance_results.md", "w") as f:
        f.write("# Modular Resonance Scan: Stopping Times mod m\n\n")
        f.write(f"## Parameters\n- N = {max_n}, moduli m = 2..{max_mod}\n")
        f.write(f"- Bonferroni threshold: p < {bonferroni_threshold:.1e}\n\n")
        f.write(f"## Summary\n")
        f.write(f"- Total significant moduli: {len(significant)}\n")
        f.write(f"- Novel resonances (coprime to 6): {len(novel_resonances)}\n\n")
        f.write("## Top 20 Resonances (by Cramér's V)\n\n")
        f.write("| Rank | Modulus | Cramér's V | p-value | Type |\n")
        f.write("|------|---------|------------|---------|------|\n")
        for i, d in enumerate(top_20):
            t = "pow2" if d["is_power_of_2"] else "{2,3}-smooth" if d["is_23smooth"] else "coprime6" if d["coprime_to_6"] else "other"
            f.write(f"| {i+1} | {d['modulus']} | {d['cramers_v']:.4f} | {d['p_value']:.2e} | {t} |\n")
        f.write("\n## Novel Resonances (coprime to 6)\n\n")
        if novel_resonances:
            for d in novel_resonances[:10]:
                f.write(f"- **mod {d['modulus']}** (prime={d['is_prime']}): V={d['cramers_v']:.4f}, p={d['p_value']:.2e}\n")
            f.write("\n**These resonances are not explained by powers of 2 or 3 and represent\n")
            f.write("potentially novel arithmetic constraints on Collatz stopping times.**\n")
        else:
            f.write("No novel resonances found at primes coprime to 6.\n")
            f.write("All significant non-uniformity is explained by powers of 2 and 3.\n")

    return results


if __name__ == "__main__":
    results = run_modular_resonance(max_n=500000, max_mod=500)
