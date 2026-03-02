#!/usr/bin/env python3
"""Generate scaling analysis plots for all benchmark results (item_019)."""

import json
import math
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Publication-quality settings
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'legend.fontsize': 9,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'lines.linewidth': 1.8,
    'lines.markersize': 6,
})

ALGO_STYLES = {
    'dijkstra_fibonacci': {'color': '#1f77b4', 'marker': 'o', 'label': 'Dijkstra + Fibonacci Heap'},
    'dijkstra_binary':    {'color': '#2ca02c', 'marker': 's', 'label': 'Dijkstra + Binary Heap'},
    'duan_stoc2025':      {'color': '#ff7f0e', 'marker': '^', 'label': 'Duan et al. 2025 (simplified)'},
    'dams_sssp':          {'color': '#d62728', 'marker': 'D', 'label': 'DAMS-SSSP (novel)'},
}

def load_data():
    with open('results/full_benchmarks.json') as f:
        return json.load(f)

def filter_data(data, graph_type=None, algorithm=None):
    out = data
    if graph_type:
        out = [r for r in out if r['graph_type'] == graph_type]
    if algorithm:
        out = [r for r in out if r['algorithm'] == algorithm]
    return [r for r in out if 'error' not in r]

def get_series(data, graph_type, algorithm):
    """Extract (n, median_time, std_time) series for a given algo+graph."""
    rows = filter_data(data, graph_type=graph_type, algorithm=algorithm)
    rows.sort(key=lambda r: r['n'])
    ns = [r['n'] for r in rows]
    medians = [r['median_time'] for r in rows]
    stds = [r['std_time'] for r in rows]
    return ns, medians, stds

def get_ops_series(data, graph_type, algorithm):
    """Extract (n, m, total_ops) series."""
    rows = filter_data(data, graph_type=graph_type, algorithm=algorithm)
    rows.sort(key=lambda r: r['n'])
    ns = [r['n'] for r in rows]
    ms = [r['m'] for r in rows]
    total_ops = [r['comparisons'] + r['additions'] + r['heap_ops'] for r in rows]
    return ns, ms, total_ops


def plot_scaling_time(data, graph_type, title_suffix, filename):
    """Plot wall-clock time vs n for all algorithms on a given graph type."""
    fig, ax = plt.subplots(figsize=(8, 5.5))

    for algo, style in ALGO_STYLES.items():
        ns, medians, stds = get_series(data, graph_type, algo)
        if not ns:
            continue
        # Skip degenerate data (power_law with 0 ops)
        if max(medians) < 1e-6:
            continue
        ax.errorbar(ns, medians, yerr=stds, label=style['label'],
                     color=style['color'], marker=style['marker'],
                     capsize=3, capthick=1)

    ax.set_xlabel('Number of Vertices (n)')
    ax.set_ylabel('Median Wall-Clock Time (seconds)')
    ax.set_title(f'Scaling: Wall-Clock Time vs n ({title_suffix})')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(loc='upper left')
    ax.grid(True, which='both', alpha=0.3)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    fig.tight_layout()
    fig.savefig(f'figures/{filename}.png')
    fig.savefig(f'figures/{filename}.pdf')
    plt.close(fig)
    print(f"  Saved figures/{filename}.png/.pdf")


def plot_scaling_ops(data, graph_type, title_suffix, filename):
    """Plot operation counts vs n with theoretical complexity curves overlaid."""
    fig, ax = plt.subplots(figsize=(8, 5.5))

    # Plot empirical data
    for algo, style in ALGO_STYLES.items():
        ns, ms, ops = get_ops_series(data, graph_type, algo)
        if not ns or max(ops) < 10:
            continue
        ax.plot(ns, ops, label=style['label'],
                color=style['color'], marker=style['marker'])

    # Theoretical curves — fitted to the data
    # Use the sparse or grid m values
    rows = filter_data(data, graph_type=graph_type, algorithm='dijkstra_binary')
    rows.sort(key=lambda r: r['n'])
    if rows:
        ns_th = np.array([r['n'] for r in rows], dtype=float)
        ms_th = np.array([r['m'] for r in rows], dtype=float)

        # O(m + n log n)
        th_mnlogn = ms_th + ns_th * np.log2(ns_th)
        # O(m * log^{2/3} n)
        th_mlog23 = ms_th * np.power(np.log2(ns_th), 2.0/3.0)
        # O(m * sqrt(log n))
        th_msqrtlog = ms_th * np.sqrt(np.log2(ns_th))

        # Fit scaling constants using the largest n point from dijkstra_binary
        bin_ns, bin_ms, bin_ops = get_ops_series(data, graph_type, 'dijkstra_binary')
        if bin_ops and max(bin_ops) > 10:
            c_mnlogn = bin_ops[-1] / th_mnlogn[-1]
            ax.plot(ns_th, c_mnlogn * th_mnlogn, '--', color='gray',
                    alpha=0.6, label=r'$O(m + n \log n)$ fit')

        duan_ns, duan_ms, duan_ops = get_ops_series(data, graph_type, 'duan_stoc2025')
        if duan_ops and max(duan_ops) > 10:
            c_mlog23 = duan_ops[-1] / th_mlog23[-1]
            ax.plot(ns_th, c_mlog23 * th_mlog23, '--', color='#ff7f0e',
                    alpha=0.4, label=r'$O(m \log^{2/3} n)$ fit')

        dams_ns, dams_ms, dams_ops = get_ops_series(data, graph_type, 'dams_sssp')
        if dams_ops and max(dams_ops) > 10:
            c_msqrtlog = dams_ops[-1] / th_msqrtlog[-1]
            ax.plot(ns_th, c_msqrtlog * th_msqrtlog, '--', color='#d62728',
                    alpha=0.4, label=r'$O(m \sqrt{\log n})$ fit')

    ax.set_xlabel('Number of Vertices (n)')
    ax.set_ylabel('Total Operations (comparisons + additions + heap ops)')
    ax.set_title(f'Operation Counts vs n ({title_suffix})')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(loc='upper left', fontsize=8)
    ax.grid(True, which='both', alpha=0.3)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    fig.tight_layout()
    fig.savefig(f'figures/{filename}.png')
    fig.savefig(f'figures/{filename}.pdf')
    plt.close(fig)
    print(f"  Saved figures/{filename}.png/.pdf")


def plot_crossover_analysis(data):
    """Plot ratio of novel algorithm time to Dijkstra(binary) time vs n."""
    fig, ax = plt.subplots(figsize=(8, 5.5))

    for gtype, gstyle in [('sparse', '-'), ('grid', '--'), ('worst_case', ':')]:
        ns_dams, med_dams, _ = get_series(data, gtype, 'dams_sssp')
        ns_bin, med_bin, _ = get_series(data, gtype, 'dijkstra_binary')
        ns_duan, med_duan, _ = get_series(data, gtype, 'duan_stoc2025')

        if not ns_dams or not ns_bin:
            continue

        # Filter to sizes present in both
        common_n = sorted(set(ns_dams) & set(ns_bin))
        dams_map = dict(zip(ns_dams, med_dams))
        bin_map = dict(zip(ns_bin, med_bin))
        duan_map = dict(zip(ns_duan, med_duan))

        ratios_dams = [dams_map[n] / bin_map[n] for n in common_n if bin_map[n] > 0]
        ratios_duan = [duan_map.get(n, 0) / bin_map[n] for n in common_n if bin_map[n] > 0 and n in duan_map]

        ax.plot(common_n[:len(ratios_dams)], ratios_dams,
                linestyle=gstyle, color='#d62728', marker='D',
                label=f'DAMS / Binary ({gtype})')
        ax.plot(common_n[:len(ratios_duan)], ratios_duan,
                linestyle=gstyle, color='#ff7f0e', marker='^',
                label=f'Duan / Binary ({gtype})')

    ax.axhline(y=1.0, color='black', linestyle='-', alpha=0.3, label='Parity (ratio=1)')
    ax.set_xlabel('Number of Vertices (n)')
    ax.set_ylabel('Time Ratio (Algorithm / Dijkstra Binary Heap)')
    ax.set_title('Crossover Analysis: Algorithm Time Relative to Dijkstra')
    ax.set_xscale('log')
    ax.legend(loc='best', fontsize=7.5)
    ax.grid(True, which='both', alpha=0.3)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    fig.tight_layout()
    fig.savefig('figures/crossover_analysis.png')
    fig.savefig('figures/crossover_analysis.pdf')
    plt.close(fig)
    print("  Saved figures/crossover_analysis.png/.pdf")


def plot_memory_comparison(data):
    """Plot peak memory vs n for all algorithms."""
    fig, ax = plt.subplots(figsize=(8, 5.5))

    for gtype in ['sparse', 'worst_case']:
        for algo, style in ALGO_STYLES.items():
            rows = filter_data(data, graph_type=gtype, algorithm=algo)
            rows.sort(key=lambda r: r['n'])
            ns = [r['n'] for r in rows]
            mems = [r.get('peak_memory_kb', 0) for r in rows]
            if not ns or max(mems) == 0:
                continue
            linestyle = '-' if gtype == 'sparse' else '--'
            ax.plot(ns, mems, linestyle=linestyle,
                    color=style['color'], marker=style['marker'],
                    label=f"{style['label']} ({gtype})")

    ax.set_xlabel('Number of Vertices (n)')
    ax.set_ylabel('Peak Memory (KB)')
    ax.set_title('Peak Memory Usage vs n')
    ax.set_xscale('log')
    ax.legend(loc='upper left', fontsize=8)
    ax.grid(True, which='both', alpha=0.3)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    fig.tight_layout()
    fig.savefig('figures/memory_comparison.png')
    fig.savefig('figures/memory_comparison.pdf')
    plt.close(fig)
    print("  Saved figures/memory_comparison.png/.pdf")


def main():
    os.makedirs('figures', exist_ok=True)
    data = load_data()
    print(f"Loaded {len(data)} benchmark results")

    # 1. Scaling time - sparse
    print("Generating scaling_time_sparse...")
    plot_scaling_time(data, 'sparse', 'Sparse Graphs (m = 3n)', 'scaling_time_sparse')

    # 2. Scaling time - dense (using grid as dense proxy since we have grid data)
    print("Generating scaling_time_dense...")
    plot_scaling_time(data, 'grid', 'Grid Graphs (m ≈ 4n)', 'scaling_time_dense')

    # Also make a worst_case timing plot
    print("Generating scaling_time_worst_case...")
    plot_scaling_time(data, 'worst_case', 'Worst-Case Graphs (m ≈ 2n)', 'scaling_time_worst_case')

    # 3. Scaling ops - sparse
    print("Generating scaling_ops_sparse...")
    plot_scaling_ops(data, 'sparse', 'Sparse Graphs (m = 3n)', 'scaling_ops_sparse')

    # 4. Scaling ops - dense (grid)
    print("Generating scaling_ops_dense...")
    plot_scaling_ops(data, 'grid', 'Grid Graphs (m ≈ 4n)', 'scaling_ops_dense')

    # 5. Crossover analysis
    print("Generating crossover_analysis...")
    plot_crossover_analysis(data)

    # 6. Memory comparison
    print("Generating memory_comparison...")
    plot_memory_comparison(data)

    print("\nAll scaling plots generated successfully!")


if __name__ == '__main__':
    main()
