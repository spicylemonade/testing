"""Novel Direction 4: Information-theoretic analysis of Collatz trajectories.

Computes mutual information between binary structure of n and trajectory
parity to test the stochastic independence assumption.
"""

import os
import sys
import json
import numpy as np
from collections import defaultdict

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


def get_k_bit_window(n, k, offset=0):
    """Extract k-bit window from binary representation of n starting at bit offset."""
    return (n >> offset) & ((1 << k) - 1)


def compute_mutual_information_vs_step(max_n, k_values, max_step=200):
    """Compute I(X_k; Y_t) where X_k = k-bit window of binary(n), Y_t = parity at step t."""
    results = {}

    for k in k_values:
        print(f"  Computing MI for k={k}...")
        mi_values = np.zeros(max_step)
        valid_counts = np.zeros(max_step, dtype=int)

        # Collect joint distribution for each step t
        for t in range(max_step):
            # Joint counts: (x_k_value, y_t_value) -> count
            joint = defaultdict(int)
            x_marginal = defaultdict(int)
            y_marginal = defaultdict(int)
            n_valid = 0

            for n in range(1, max_n + 1):
                ps = collatz_parity_sequence(n)
                if t >= len(ps):
                    continue
                x = get_k_bit_window(n, k)
                y = int(ps[t])
                joint[(x, y)] += 1
                x_marginal[x] += 1
                y_marginal[y] += 1
                n_valid += 1

            valid_counts[t] = n_valid
            if n_valid < 100:
                mi_values[t] = np.nan
                continue

            # Compute MI
            mi = 0.0
            for (x, y), count in joint.items():
                p_xy = count / n_valid
                p_x = x_marginal[x] / n_valid
                p_y = y_marginal[y] / n_valid
                if p_xy > 0 and p_x > 0 and p_y > 0:
                    mi += p_xy * np.log2(p_xy / (p_x * p_y))
            mi_values[t] = mi

        results[k] = {
            "mi_values": mi_values.tolist(),
            "valid_counts": valid_counts.tolist(),
        }

    return results


def compute_conditional_entropy(max_n, max_step=200):
    """Compute H(parity_step_t | binary_bits_of_n) as function of t."""
    k = 8  # Use 8-bit window
    h_cond = np.zeros(max_step)

    for t in range(max_step):
        # For each x value, compute H(Y|X=x) then average
        x_counts = defaultdict(lambda: [0, 0])
        total = 0
        for n in range(1, max_n + 1):
            ps = collatz_parity_sequence(n)
            if t >= len(ps):
                continue
            x = get_k_bit_window(n, k)
            y = int(ps[t])
            x_counts[x][y] += 1
            total += 1

        if total < 100:
            h_cond[t] = np.nan
            continue

        h = 0.0
        for x, counts in x_counts.items():
            nx = sum(counts)
            px = nx / total
            for c in counts:
                if c > 0:
                    py_given_x = c / nx
                    h -= px * py_given_x * np.log2(py_given_x)
        h_cond[t] = h

    return h_cond


def compute_shuffled_null(max_n, k, max_step=200, n_shuffles=50):
    """Null model: shuffle parity sequences independently to destroy correlations."""
    null_mi = np.zeros((n_shuffles, max_step))

    # Collect all parity sequences first
    all_parities = []
    for n in range(1, max_n + 1):
        ps = collatz_parity_sequence(n)
        all_parities.append(ps)

    for s in range(n_shuffles):
        if s % 10 == 0:
            print(f"  Null shuffle {s}/{n_shuffles}...")
        # For each step t, shuffle the parity values across all n
        perm = np.random.permutation(max_n)
        for t in range(max_step):
            joint = defaultdict(int)
            x_marginal = defaultdict(int)
            y_marginal = defaultdict(int)
            n_valid = 0
            for i in range(max_n):
                n = i + 1
                ps = all_parities[perm[i]]
                if t >= len(ps):
                    continue
                x = get_k_bit_window(n, k)
                y = int(ps[t])
                joint[(x, y)] += 1
                x_marginal[x] += 1
                y_marginal[y] += 1
                n_valid += 1

            if n_valid < 100:
                null_mi[s, t] = np.nan
                continue
            mi = 0.0
            for (x, y), count in joint.items():
                p_xy = count / n_valid
                p_x = x_marginal[x] / n_valid
                p_y = y_marginal[y] / n_valid
                if p_xy > 0 and p_x > 0 and p_y > 0:
                    mi += p_xy * np.log2(p_xy / (p_x * p_y))
            null_mi[s, t] = mi

    return null_mi


def run_info_theory_analysis(max_n=50000, max_step=150):
    """Full information-theoretic analysis."""
    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    k_values = [4, 6, 8]

    print(f"Computing mutual information for n=1..{max_n}...")
    mi_results = compute_mutual_information_vs_step(max_n, k_values, max_step)

    print("Computing null model (shuffled)...")
    null_mi = compute_shuffled_null(max_n, k=6, max_step=max_step, n_shuffles=30)

    # Plot MI vs step for different k values
    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
    for i, k in enumerate(k_values):
        mi = np.array(mi_results[k]["mi_values"][:max_step])
        valid = np.array(mi_results[k]["valid_counts"][:max_step])
        mask = valid > 100
        steps = np.arange(max_step)[mask]
        mi_clean = mi[mask]
        ax.plot(steps, mi_clean, label=f"k = {k}", color=COLORS[i],
                linewidth=1.5, marker='o', markersize=2, alpha=0.8)

    # Null model band
    null_mean = np.nanmean(null_mi, axis=0)
    null_std = np.nanstd(null_mi, axis=0)
    ax.fill_between(range(max_step), null_mean - 2 * null_std, null_mean + 2 * null_std,
                    alpha=0.2, color='gray', label="Null model (±2σ)")
    ax.plot(range(max_step), null_mean, color='gray', linestyle='--', linewidth=1)

    ax.set_xlabel("Trajectory Step t")
    ax.set_ylabel("Mutual Information I(X_k; Y_t) (bits)")
    ax.set_title("Mutual Information Between Binary Structure and Parity Sequence")
    ax.legend(frameon=True, loc='upper right')
    ax.set_xlim(0, max_step)
    ax.set_ylim(bottom=0)
    plt.savefig("figures/mutual_information_decay.png", dpi=300)
    plt.savefig("figures/mutual_information_decay.pdf")
    plt.close()

    # Determine if MI plateaus
    # Check last 30% of steps for each k
    tail_start = int(max_step * 0.7)
    plateau_results = {}
    for k in k_values:
        mi = np.array(mi_results[k]["mi_values"])
        valid = np.array(mi_results[k]["valid_counts"])
        tail_mask = (np.arange(max_step) >= tail_start) & (valid > 100)
        if tail_mask.sum() > 5:
            tail_mi = mi[tail_mask]
            tail_mean = float(np.nanmean(tail_mi))
            tail_std = float(np.nanstd(tail_mi))
            null_tail = null_mean[tail_mask]
            null_tail_mean = float(np.nanmean(null_tail))
            # Is MI significantly above null?
            excess = tail_mean - null_tail_mean
            plateau_results[k] = {
                "tail_mean_mi": tail_mean,
                "tail_std_mi": tail_std,
                "null_tail_mean": null_tail_mean,
                "excess_mi": float(excess),
                "significant": bool(excess > 3 * tail_std) if tail_std > 0 else False,
            }
        else:
            plateau_results[k] = {"tail_mean_mi": 0, "significant": False}

    # Initial MI values (step 0-5 average)
    initial_mi = {}
    for k in k_values:
        mi = np.array(mi_results[k]["mi_values"][:6])
        initial_mi[k] = float(np.nanmean(mi))

    results = {
        "max_n": max_n,
        "max_step": max_step,
        "k_values": k_values,
        "seed": SEED,
        "initial_mi": initial_mi,
        "plateau_analysis": plateau_results,
        "mi_curves": {str(k): mi_results[k]["mi_values"][:max_step] for k in k_values},
        "null_mean": null_mean.tolist(),
        "null_std": null_std.tolist(),
    }

    with open("results/info_theory_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Write markdown report
    with open("results/info_theory_results.md", "w") as f:
        f.write("# Information-Theoretic Analysis: Mutual Information in Collatz Trajectories\n\n")
        f.write(f"## Parameters\n- N = {max_n}, max_step = {max_step}, k = {k_values}\n\n")
        f.write("## Key Findings\n\n")
        f.write("### Mutual Information Decay\n\n")
        for k in k_values:
            p = plateau_results.get(k, {})
            f.write(f"- **k={k}**: Initial MI = {initial_mi[k]:.4f} bits, ")
            f.write(f"tail MI = {p.get('tail_mean_mi', 0):.4f} ± {p.get('tail_std_mi', 0):.4f}, ")
            f.write(f"excess over null = {p.get('excess_mi', 0):.4f}, ")
            f.write(f"significant = {p.get('significant', False)}\n")
        f.write("\n### Interpretation\n\n")
        any_sig = any(plateau_results.get(k, {}).get('significant', False) for k in k_values)
        if any_sig:
            f.write("**Mutual information does NOT fully decay to zero.** The parity sequence\n")
            f.write("retains measurable information about the initial binary structure even at\n")
            f.write("late trajectory steps. This provides computational evidence against the\n")
            f.write("stochastic independence assumption (Kontorovich-Lagarias 2009).\n\n")
            f.write("This finding, if confirmed at larger scales, would be a significant\n")
            f.write("new constraint on Collatz dynamics.\n")
        else:
            f.write("Mutual information decays to the null model level, consistent with the\n")
            f.write("stochastic independence assumption. However, the RATE of decay and its\n")
            f.write("dependence on k is itself informative about the mixing properties of\n")
            f.write("the Collatz map.\n")

    print("\nInfo Theory Results:")
    for k in k_values:
        p = plateau_results.get(k, {})
        print(f"  k={k}: initial MI={initial_mi[k]:.4f}, tail={p.get('tail_mean_mi', 0):.4f}, "
              f"sig={p.get('significant', False)}")
    return results


if __name__ == "__main__":
    results = run_info_theory_analysis(max_n=50000, max_step=150)
