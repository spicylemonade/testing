"""Generate publication-quality plots for baseline comparison (item_010)."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import csv
import numpy as np

# Professional figure setup
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

COLORS = {'dijkstra_fib': '#2176AE', 'dmmsy': '#E84855', 'novel': '#57A773'}
MARKERS = {'dijkstra_fib': 'o', 'dmmsy': 's', 'novel': 'D'}
LABELS = {'dijkstra_fib': 'Dijkstra + Fib Heap', 'dmmsy': 'DMMSY (2025)', 'novel': 'Novel Algorithm'}


def load_csv(path):
    rows = []
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


def plot_time_vs_n(rows, output_prefix='figures/baseline_time_vs_n'):
    """Plot 1: Wall-clock time vs n for each algorithm, averaged over families."""
    fig, ax = plt.subplots(figsize=(8, 5))

    for algo in ['dijkstra_fib', 'dmmsy']:
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
    ax.set_title('SSSP Algorithm Scaling: Time vs Graph Size')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(frameon=True, shadow=True, loc='upper left')

    plt.savefig(f'{output_prefix}.png', dpi=300)
    plt.savefig(f'{output_prefix}.pdf')
    plt.close()
    print(f"  Saved {output_prefix}.png/pdf")


def plot_ops_vs_n(rows, output_prefix='figures/baseline_ops_vs_n'):
    """Plot 2: Operation counts vs n."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), constrained_layout=True)

    for i, (metric, ylabel) in enumerate([
        ('comparisons', 'Comparisons'),
        ('additions', 'Additions'),
        ('decrease_keys', 'Decrease-Key Calls'),
    ]):
        ax = axes[i]
        for algo in ['dijkstra_fib', 'dmmsy']:
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

    fig.suptitle('Operation Counts vs Graph Size', fontweight='bold', fontsize=14)
    plt.savefig(f'{output_prefix}.png', dpi=300)
    plt.savefig(f'{output_prefix}.pdf')
    plt.close()
    print(f"  Saved {output_prefix}.png/pdf")


def plot_time_vs_density(rows, output_prefix='figures/baseline_time_vs_density'):
    """Plot 3: Time vs m/n density ratio."""
    fig, ax = plt.subplots(figsize=(8, 5))

    for algo in ['dijkstra_fib', 'dmmsy']:
        data = {}
        for r in rows:
            if r['algorithm'] == algo and r['n'] >= 1000:
                density = r['m'] / r['n']
                data.setdefault(round(density, 1), []).append(r['wall_time_ms'])

        densities = sorted(data.keys())
        means = [np.mean(data[d]) for d in densities]
        stds = [np.std(data[d]) for d in densities]

        ax.errorbar(densities, means, yerr=stds,
                    label=LABELS[algo], color=COLORS[algo],
                    marker=MARKERS[algo], linewidth=2, markersize=7,
                    capsize=4, capthick=1.5)

    ax.set_xlabel('Edge Density (m/n)')
    ax.set_ylabel('Wall-Clock Time (ms)')
    ax.set_title('SSSP Scaling: Time vs Edge Density')
    ax.legend(frameon=True, shadow=True)

    plt.savefig(f'{output_prefix}.png', dpi=300)
    plt.savefig(f'{output_prefix}.pdf')
    plt.close()
    print(f"  Saved {output_prefix}.png/pdf")


def plot_crossover(rows, output_prefix='figures/baseline_crossover'):
    """Plot 4: Crossover analysis - DMMSY time / Dijkstra time ratio."""
    fig, ax = plt.subplots(figsize=(8, 5))

    # Group by (n, family)
    dijk_data = {}
    dmmsy_data = {}

    for r in rows:
        key = (r['n'], r['graph_family'])
        if r['algorithm'] == 'dijkstra_fib':
            dijk_data[key] = r['wall_time_ms']
        elif r['algorithm'] == 'dmmsy':
            dmmsy_data[key] = r['wall_time_ms']

    # Plot ratio by n
    ratio_by_n = {}
    for key in dijk_data:
        if key in dmmsy_data and dijk_data[key] > 0:
            n = key[0]
            ratio = dmmsy_data[key] / dijk_data[key]
            ratio_by_n.setdefault(n, []).append(ratio)

    ns = sorted(ratio_by_n.keys())
    means = [np.mean(ratio_by_n[n]) for n in ns]
    stds = [np.std(ratio_by_n[n]) for n in ns]

    ax.errorbar(ns, means, yerr=stds, color='#2176AE', marker='o',
                linewidth=2, markersize=7, capsize=4, capthick=1.5,
                label='DMMSY / Dijkstra ratio')
    ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1,
               label='Break-even (ratio = 1)')

    ax.set_xlabel('Number of Vertices (n)')
    ax.set_ylabel('Time Ratio (DMMSY / Dijkstra)')
    ax.set_title('Crossover Analysis: When Does DMMSY Beat Dijkstra?')
    ax.set_xscale('log')
    ax.legend(frameon=True, shadow=True)

    plt.savefig(f'{output_prefix}.png', dpi=300)
    plt.savefig(f'{output_prefix}.pdf')
    plt.close()
    print(f"  Saved {output_prefix}.png/pdf")


def main():
    os.makedirs('figures', exist_ok=True)
    rows = load_csv('results/baselines.csv')
    print(f"Loaded {len(rows)} rows from results/baselines.csv")

    plot_time_vs_n(rows)
    plot_ops_vs_n(rows)
    plot_time_vs_density(rows)
    plot_crossover(rows)

    print("\nAll baseline plots generated.")


if __name__ == '__main__':
    main()
