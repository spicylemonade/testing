"""Novel Direction 6: Forbidden and anomalously rare subwords in Collatz parity sequences."""

import os
import sys
import json
import math
import numpy as np
from collections import Counter, defaultdict
from itertools import product as iproduct

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

# Theoretical probability of odd step
P_ODD = math.log(2) / (math.log(2) + math.log(3))  # ≈ 0.387


def expected_kgram_freq(pattern, total_positions):
    """Expected frequency of a k-gram under iid Bernoulli(P_ODD) model."""
    k = len(pattern)
    n_ones = pattern.count('1')
    n_zeros = k - n_ones
    prob = (P_ODD ** n_ones) * ((1 - P_ODD) ** n_zeros)
    return prob * total_positions


def collect_parity_sequences(max_n):
    """Collect all parity sequences."""
    sequences = []
    for n in range(1, max_n + 1):
        ps = collatz_parity_sequence(n)
        sequences.append(ps)
    return sequences


def count_kgrams(sequences, k):
    """Count all k-grams across all parity sequences."""
    counts = Counter()
    total_positions = 0
    for ps in sequences:
        for i in range(len(ps) - k + 1):
            counts[ps[i:i + k]] += 1
            total_positions += 1
    return counts, total_positions


def run_forbidden_patterns(max_n=200000, max_k=12):
    """Full forbidden pattern analysis."""
    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    print(f"Collecting parity sequences for n=1..{max_n}...")
    sequences = collect_parity_sequences(max_n)

    results = {"max_n": max_n, "max_k": max_k, "seed": SEED}
    all_forbidden = {}
    all_rare = {}

    for k in range(4, max_k + 1):
        print(f"\nAnalyzing {k}-grams...")
        counts, total_pos = count_kgrams(sequences, k)
        n_possible = 2 ** k

        # All possible k-grams
        all_patterns = [''.join(bits) for bits in iproduct('01', repeat=k)]

        forbidden = []
        rare = []
        pattern_data = []

        for pat in all_patterns:
            obs = counts.get(pat, 0)
            exp = expected_kgram_freq(pat, total_pos)
            ratio = obs / exp if exp > 0 else 0

            if obs == 0:
                forbidden.append(pat)
            elif ratio < 0.01:
                rare.append((pat, obs, exp, ratio))

            pattern_data.append({
                "pattern": pat,
                "observed": obs,
                "expected": float(exp),
                "ratio": float(ratio),
            })

        # Check structural constraint: consecutive odd steps impossible?
        # After an odd step (1), 3n+1 is even, so next step MUST be even (0)
        # Therefore "11" is forbidden! Two consecutive 1s cannot appear.
        has_consecutive_ones = [p for p in forbidden if '11' in p]

        all_forbidden[k] = forbidden
        all_rare[k] = [(p, o, float(e), float(r)) for p, o, e, r in rare]

        print(f"  k={k}: {len(forbidden)} forbidden, {len(rare)} rare (<1% expected)")
        print(f"  Total positions: {total_pos}, possible patterns: {n_possible}")

        results[f"k_{k}"] = {
            "n_forbidden": len(forbidden),
            "n_rare": len(rare),
            "total_positions": total_pos,
            "forbidden_patterns": forbidden,
            "rare_patterns": [(p, o, e, r) for p, o, e, r in rare[:20]],
        }

    # The key structural constraint: "11" is forbidden
    # Because odd → 3n+1 → always even → next step is division by 2
    # So parity bit after a 1 must be 0
    # This means ALL patterns containing "11" are forbidden
    print("\n=== STRUCTURAL ANALYSIS ===")
    print("Key constraint: '11' (consecutive odd steps) is FORBIDDEN")
    print("because 3n+1 always produces an even number.")

    # Count non-trivial forbidden patterns (not explained by "11" constraint)
    nontrivial_forbidden = {}
    for k, patterns in all_forbidden.items():
        trivial = [p for p in patterns if '11' in p]
        nontrivial = [p for p in patterns if '11' not in p]
        nontrivial_forbidden[k] = nontrivial
        results[f"k_{k}"]["trivial_forbidden"] = len(trivial)
        results[f"k_{k}"]["nontrivial_forbidden"] = len(nontrivial)
        results[f"k_{k}"]["nontrivial_forbidden_patterns"] = nontrivial
        if nontrivial:
            print(f"  k={k}: {len(nontrivial)} NON-TRIVIAL forbidden patterns: {nontrivial[:5]}")

    # Test with generalized maps (5n+1, 7n+1)
    print("\nTesting generalized maps...")
    gen_results = {}
    for a in [5, 7]:
        gen_sequences = []
        for n in range(1, min(max_n, 50000) + 1):
            current = n
            ps = []
            steps = 0
            while current != 1 and steps < 10000:
                if current % 2 == 0:
                    ps.append('0')
                    current //= 2
                else:
                    ps.append('1')
                    current = a * current + 1
                steps += 1
                if current > 10 ** 15:
                    break
            gen_sequences.append(''.join(ps))

        gen_forbidden_6 = []
        gen_counts, gen_total = count_kgrams(gen_sequences, 6)
        for pat in [''.join(bits) for bits in iproduct('01', repeat=6)]:
            if gen_counts.get(pat, 0) == 0:
                gen_forbidden_6.append(pat)
        gen_results[a] = {
            "n_forbidden_6grams": len(gen_forbidden_6),
            "forbidden_with_11": len([p for p in gen_forbidden_6 if '11' in p]),
        }
        # For a=5, 5n+1 is even when n is odd, so "11" should still be forbidden
        print(f"  {a}n+1: {len(gen_forbidden_6)} forbidden 6-grams")

    results["generalized_maps"] = gen_results

    # Visualization: ratio of observed/expected for k=8
    k_plot = 8
    counts_8, total_8 = count_kgrams(sequences, k_plot)
    all_pats_8 = sorted([''.join(bits) for bits in iproduct('01', repeat=k_plot)])
    ratios_8 = []
    for pat in all_pats_8:
        obs = counts_8.get(pat, 0)
        exp = expected_kgram_freq(pat, total_8)
        ratios_8.append(obs / exp if exp > 0 else 0)

    # Only show patterns without "11" (admissible patterns)
    admissible = [(p, r) for p, r in zip(all_pats_8, ratios_8) if '11' not in p]
    fig, ax = plt.subplots(figsize=(14, 5), constrained_layout=True)
    pats_a = [p for p, _ in admissible]
    rats_a = [r for _, r in admissible]
    bar_colors = [COLORS[2] if r < 0.01 else COLORS[0] for r in rats_a]
    ax.bar(range(len(pats_a)), rats_a, color=bar_colors, edgecolor='white', linewidth=0.3)
    ax.axhline(1.0, color=COLORS[3], linestyle='--', linewidth=1.5, label='Expected (uniform Bernoulli)')
    ax.set_xlabel(f"{k_plot}-gram Pattern (admissible only, no consecutive 1s)")
    ax.set_ylabel("Observed / Expected Ratio")
    ax.set_title(f"Frequency Ratios of Admissible {k_plot}-grams in Parity Sequences")
    ax.set_xticks(range(0, len(pats_a), max(1, len(pats_a) // 20)))
    ax.set_xticklabels([pats_a[i] for i in range(0, len(pats_a), max(1, len(pats_a) // 20))],
                        rotation=90, fontsize=7)
    ax.legend(frameon=True)
    plt.savefig("figures/forbidden_patterns_ratios.png", dpi=300)
    plt.savefig("figures/forbidden_patterns_ratios.pdf")
    plt.close()

    # Summary plot: number of forbidden patterns vs k
    ks = list(range(4, max_k + 1))
    n_forbidden_total = [results[f"k_{k}"]["n_forbidden"] for k in ks]
    n_trivial = [results[f"k_{k}"]["trivial_forbidden"] for k in ks]
    n_nontrivial = [results[f"k_{k}"]["nontrivial_forbidden"] for k in ks]

    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    x = np.arange(len(ks))
    width = 0.35
    ax.bar(x - width / 2, n_trivial, width, color=COLORS[0], label='Trivial (contain "11")',
           edgecolor='white')
    ax.bar(x + width / 2, n_nontrivial, width, color=COLORS[2], label='Non-trivial',
           edgecolor='white')
    ax.set_xlabel("k-gram Length")
    ax.set_ylabel("Number of Forbidden Patterns")
    ax.set_title("Forbidden Patterns in Collatz Parity Sequences")
    ax.set_xticks(x)
    ax.set_xticklabels(ks)
    ax.legend(frameon=True)
    for i, (t, nt) in enumerate(zip(n_trivial, n_nontrivial)):
        ax.annotate(f'{t}', (i - width / 2, t), ha='center', va='bottom', fontsize=8)
        if nt > 0:
            ax.annotate(f'{nt}', (i + width / 2, nt), ha='center', va='bottom', fontsize=8, color=COLORS[2])
    plt.savefig("figures/forbidden_patterns_count.png", dpi=300)
    plt.savefig("figures/forbidden_patterns_count.pdf")
    plt.close()

    with open("results/forbidden_patterns.json", "w") as f:
        json.dump(results, f, indent=2)

    # Markdown report
    with open("results/forbidden_patterns.md", "w") as f:
        f.write("# Forbidden Patterns in Collatz Parity Sequences\n\n")
        f.write(f"## Parameters\n- N = {max_n}, k = 4..{max_k}\n\n")
        f.write("## Key Structural Constraint\n\n")
        f.write("The pattern '11' (consecutive odd steps) is **provably forbidden** because\n")
        f.write("3n+1 always produces an even number when n is odd. This means the next\n")
        f.write("Collatz step after an odd step is always a division by 2 (even step).\n\n")
        f.write("## Forbidden Pattern Counts\n\n")
        f.write("| k | Total Forbidden | Trivial (contain '11') | Non-trivial |\n")
        f.write("|---|----------------|----------------------|-------------|\n")
        for k in ks:
            d = results[f"k_{k}"]
            f.write(f"| {k} | {d['n_forbidden']} | {d['trivial_forbidden']} | {d['nontrivial_forbidden']} |\n")
        f.write("\n## Non-trivial Forbidden Patterns\n\n")
        any_nontrivial = False
        for k in ks:
            ntp = nontrivial_forbidden.get(k, [])
            if ntp:
                any_nontrivial = True
                f.write(f"- k={k}: {ntp[:10]}\n")
        if not any_nontrivial:
            f.write("**No non-trivial forbidden patterns found** for k ≤ {max_k}.\n")
            f.write("All forbidden patterns are explained by the '11' constraint.\n")
        f.write("\n## Generalized Maps\n\n")
        for a, gd in gen_results.items():
            f.write(f"- {a}n+1: {gd['n_forbidden_6grams']} forbidden 6-grams ")
            f.write(f"({gd['forbidden_with_11']} contain '11')\n")

    return results


if __name__ == "__main__":
    results = run_forbidden_patterns(max_n=200000, max_k=12)
