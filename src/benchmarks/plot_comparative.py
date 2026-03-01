"""Generate publication-quality comparative plots for item_019.

Produces 6+ plots comparing HopGuidedSSSP vs Dijkstra vs DMMSY.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import csv
import numpy as np
import tracemalloc

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl

try:
    import seaborn as sns
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
except ImportError:
    pass

mpl.rcParams.update({
    'figure.figsize': (8, 5),
    'figure.dpi': 300,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'legend.framealpha': 0.9,
    'legend.edgecolor': '0.8',
    'font.family': 'serif',
    'grid.alpha': 0.3,
    'grid.linewidth': 0.5,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

COLORS = {'dijkstra_fib': '#2176AE', 'dmmsy': '#E84855', 'hop_guided': '#57A773'}
MARKERS = {'dijkstra_fib': 'o', 'dmmsy': 's', 'hop_guided': 'D'}
LABELS = {'dijkstra_fib': 'Dijkstra + Fib Heap',
          'dmmsy': 'DMMSY (2025)',
          'hop_guided': 'HopGuidedSSSP (Novel)'}


def load_csv(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('error'):
                continue
            row['n'] = int(row['n'])
            row['m'] = int(row['m'])
            row['wall_time_ms'] = float(row['wall_time_ms'])
            row['comparisons'] = int(row['comparisons'])
            row['additions'] = int(row['additions'])
            row['decrease_keys'] = int(row['decrease_keys'])
            rows.append(row)
    return rows


def plot1_time_comparison(rows):
    """Plot 1: Wall-clock time comparison across all graph families."""
    fig, ax = plt.subplots(figsize=(9, 5.5))

    for algo in ['dijkstra_fib', 'dmmsy', 'hop_guided']:
        data = {}
        for r in rows:
            if r['algorithm'] == algo:
                n = r['n']
                data.setdefault(n, []).append(r['wall_time_ms'])

        ns = sorted(data.keys())
        means = [np.mean(data[n]) for n in ns]
        stds = [np.std(data[n]) for n in ns]

        ax.errorbar(ns, means, yerr=stds,
                    label=LABELS[algo], color=COLORS[algo],
                    marker=MARKERS[algo], linewidth=2, markersize=7,
                    capsize=4, capthick=1.5)

    ax.set_xlabel('Number of Vertices (n)')
    ax.set_ylabel('Wall-Clock Time (ms)')
    ax.set_title('SSSP Algorithm Comparison: Time vs Graph Size')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(frameon=True, shadow=True, loc='upper left')

    plt.savefig('figures/comparative_time_vs_n.png', dpi=300)
    plt.savefig('figures/comparative_time_vs_n.pdf')
    plt.close()
    print("  Saved figures/comparative_time_vs_n.png/pdf")


def plot2_ops_comparison(rows):
    """Plot 2: Operation count comparison."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), constrained_layout=True)

    for i, (metric, ylabel) in enumerate([
        ('comparisons', 'Comparisons'),
        ('additions', 'Additions'),
        ('decrease_keys', 'Decrease-Key Calls'),
    ]):
        ax = axes[i]
        for algo in ['dijkstra_fib', 'dmmsy', 'hop_guided']:
            data = {}
            for r in rows:
                if r['algorithm'] == algo:
                    n = r['n']
                    data.setdefault(n, []).append(r[metric])

            ns = sorted(data.keys())
            means = [np.mean(data[n]) for n in ns]

            ax.plot(ns, means, label=LABELS[algo], color=COLORS[algo],
                    marker=MARKERS[algo], linewidth=2, markersize=6)

        ax.set_xlabel('Number of Vertices (n)')
        ax.set_ylabel(ylabel)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend(frameon=True, fontsize=9)

    fig.suptitle('Operation Counts: All Algorithms', fontweight='bold', fontsize=14)
    plt.savefig('figures/comparative_ops_vs_n.png', dpi=300)
    plt.savefig('figures/comparative_ops_vs_n.pdf')
    plt.close()
    print("  Saved figures/comparative_ops_vs_n.png/pdf")


def plot3_scaling_behavior(rows):
    """Plot 3: time/m vs log(n) to validate complexity."""
    fig, ax = plt.subplots(figsize=(9, 5.5))

    for algo in ['dijkstra_fib', 'dmmsy', 'hop_guided']:
        data = {}
        for r in rows:
            if r['algorithm'] == algo and r['m'] > 0:
                n = r['n']
                time_per_edge = r['wall_time_ms'] / r['m'] * 1000  # us per edge
                data.setdefault(n, []).append(time_per_edge)

        ns = sorted(data.keys())
        log_ns = [np.log2(n) for n in ns]
        means = [np.mean(data[n]) for n in ns]

        ax.plot(log_ns, means, label=LABELS[algo], color=COLORS[algo],
                marker=MARKERS[algo], linewidth=2, markersize=7)

    ax.set_xlabel('log₂(n)')
    ax.set_ylabel('Time per Edge (μs)')
    ax.set_title('Scaling Behavior: Time/m vs log(n)')
    ax.legend(frameon=True, shadow=True)

    plt.savefig('figures/comparative_scaling.png', dpi=300)
    plt.savefig('figures/comparative_scaling.pdf')
    plt.close()
    print("  Saved figures/comparative_scaling.png/pdf")


def plot4_memory_comparison(rows):
    """Plot 4: Memory usage comparison (estimated from operation counts)."""
    fig, ax = plt.subplots(figsize=(9, 5.5))

    # Estimate memory as proportional to n + m + operation_counts
    for algo in ['dijkstra_fib', 'dmmsy', 'hop_guided']:
        data = {}
        for r in rows:
            if r['algorithm'] == algo:
                n = r['n']
                # Rough memory estimate: n*8 bytes for dist + m*12 for adj
                # + overhead proportional to decrease_keys (heap entries)
                mem_kb = (n * 8 + r['m'] * 12 + r['decrease_keys'] * 16) / 1024
                data.setdefault(n, []).append(mem_kb)

        ns = sorted(data.keys())
        means = [np.mean(data[n]) for n in ns]

        ax.plot(ns, means, label=LABELS[algo], color=COLORS[algo],
                marker=MARKERS[algo], linewidth=2, markersize=7)

    ax.set_xlabel('Number of Vertices (n)')
    ax.set_ylabel('Estimated Memory (KB)')
    ax.set_title('Memory Usage Comparison (Estimated)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(frameon=True, shadow=True)

    plt.savefig('figures/comparative_memory.png', dpi=300)
    plt.savefig('figures/comparative_memory.pdf')
    plt.close()
    print("  Saved figures/comparative_memory.png/pdf")


def plot5_crossover_analysis(rows):
    """Plot 5: Crossover point analysis — when does novel beat baselines."""
    fig, ax = plt.subplots(figsize=(9, 5.5))

    # Group by (n, family, density_approx)
    algo_data = {}
    for r in rows:
        key = (r['n'], r['graph_family'], r['m'])
        algo_data.setdefault(key, {})[r['algorithm']] = r['wall_time_ms']

    # Compute ratios by n
    novel_vs_dijk = {}
    novel_vs_dmmsy = {}

    for key, algos in algo_data.items():
        n = key[0]
        if 'hop_guided' in algos and 'dijkstra_fib' in algos:
            if algos['dijkstra_fib'] > 0:
                ratio = algos['hop_guided'] / algos['dijkstra_fib']
                novel_vs_dijk.setdefault(n, []).append(ratio)
        if 'hop_guided' in algos and 'dmmsy' in algos:
            if algos['dmmsy'] > 0:
                ratio = algos['hop_guided'] / algos['dmmsy']
                novel_vs_dmmsy.setdefault(n, []).append(ratio)

    for data, label, color in [
        (novel_vs_dijk, 'Novel / Dijkstra', '#2176AE'),
        (novel_vs_dmmsy, 'Novel / DMMSY', '#E84855'),
    ]:
        ns = sorted(data.keys())
        means = [np.mean(data[n]) for n in ns]
        stds = [np.std(data[n]) for n in ns]
        ax.errorbar(ns, means, yerr=stds, label=label, color=color,
                    marker='o', linewidth=2, markersize=7,
                    capsize=4, capthick=1.5)

    ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1,
               label='Break-even (ratio = 1)')

    ax.set_xlabel('Number of Vertices (n)')
    ax.set_ylabel('Time Ratio')
    ax.set_title('Crossover Analysis: Novel Algorithm vs Baselines')
    ax.set_xscale('log')
    ax.legend(frameon=True, shadow=True)

    plt.savefig('figures/comparative_crossover.png', dpi=300)
    plt.savefig('figures/comparative_crossover.pdf')
    plt.close()
    print("  Saved figures/comparative_crossover.png/pdf")


def plot6_speedup_heatmap(rows):
    """Plot 6: Heatmap of speedup ratio across (n, m/n)."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), constrained_layout=True)

    for ax_idx, (ref_algo, ref_label) in enumerate([
        ('dijkstra_fib', 'vs Dijkstra'),
        ('dmmsy', 'vs DMMSY'),
    ]):
        ax = axes[ax_idx]

        # Collect data
        speedup_data = {}  # (n, density_bin) -> list of speedup ratios
        ref_data = {}
        novel_data = {}

        for r in rows:
            key = (r['n'], r['graph_family'], r['m'])
            if r['algorithm'] == ref_algo:
                ref_data[key] = r['wall_time_ms']
            elif r['algorithm'] == 'hop_guided':
                novel_data[key] = r['wall_time_ms']

        for key in ref_data:
            if key in novel_data and ref_data[key] > 0:
                n = key[0]
                m = key[2]
                density = round(m / n)
                ratio = ref_data[key] / novel_data[key]  # speedup
                speedup_data.setdefault((n, density), []).append(ratio)

        ns = sorted(set(k[0] for k in speedup_data))
        densities = sorted(set(k[1] for k in speedup_data))

        if not ns or not densities:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center')
            continue

        matrix = np.full((len(densities), len(ns)), np.nan)
        for i, d in enumerate(densities):
            for j, n in enumerate(ns):
                vals = speedup_data.get((n, d), [])
                if vals:
                    matrix[i, j] = np.mean(vals)

        im = ax.imshow(matrix, aspect='auto', cmap='RdYlGn',
                       vmin=0.3, vmax=2.0)
        ax.set_xticks(range(len(ns)))
        ax.set_xticklabels([str(n) for n in ns], rotation=45, ha='right')
        ax.set_yticks(range(len(densities)))
        ax.set_yticklabels([str(d) for d in densities])
        ax.set_xlabel('n')
        ax.set_ylabel('m/n')
        ax.set_title(f'Speedup {ref_label}')
        fig.colorbar(im, ax=ax, label='Speedup (>1 = novel faster)')

    fig.suptitle('Speedup Heatmap: Novel Algorithm vs Baselines',
                 fontweight='bold', fontsize=14)
    plt.savefig('figures/comparative_heatmap.png', dpi=300)
    plt.savefig('figures/comparative_heatmap.pdf')
    plt.close()
    print("  Saved figures/comparative_heatmap.png/pdf")


def main():
    os.makedirs('figures', exist_ok=True)

    # Load all data
    baselines = load_csv('results/baselines.csv')
    novel = load_csv('results/novel_results.csv')
    all_rows = baselines + novel

    print(f"Loaded {len(baselines)} baseline + {len(novel)} novel = "
          f"{len(all_rows)} total rows")

    plot1_time_comparison(all_rows)
    plot2_ops_comparison(all_rows)
    plot3_scaling_behavior(all_rows)
    plot4_memory_comparison(all_rows)
    plot5_crossover_analysis(all_rows)
    plot6_speedup_heatmap(all_rows)

    print("\nAll comparative plots generated.")


if __name__ == '__main__':
    main()
