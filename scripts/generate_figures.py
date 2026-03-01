"""Generate publication-quality figures for HiBRA paper.

Produces 5+ figures in both PNG (300 DPI) and PDF formats.
"""

import sys, os, csv, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 9,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.figsize': (7, 5),
    'lines.linewidth': 1.5,
    'lines.markersize': 6,
})

COLORS = {
    'hibra': '#e74c3c',
    'dijkstra_fib': '#3498db',
    'dijkstra_bin': '#2ecc71',
    'batch_dijkstra': '#9b59b6',
}
MARKERS = {
    'hibra': 'o',
    'dijkstra_fib': 's',
    'dijkstra_bin': '^',
    'batch_dijkstra': 'D',
}
LABELS = {
    'hibra': 'HiBRA (k-ary Fib)',
    'dijkstra_fib': 'Dijkstra (Fib heap)',
    'dijkstra_bin': 'Dijkstra (binary heap)',
    'batch_dijkstra': 'Batch Dijkstra',
}


def load_csv(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def group_median(rows, algo, gtype, col='total_ops'):
    data = {}
    for r in rows:
        if r['algorithm'] == algo and r['graph_type'] == gtype:
            n = int(r['n'])
            val = float(r[col])
            data.setdefault(n, []).append(val)
    return {n: sorted(vs)[len(vs)//2] for n, vs in sorted(data.items())}


def save_fig(fig, name):
    for ext in ['png', 'pdf']:
        path = f'figures/{name}.{ext}'
        fig.savefig(path, dpi=300, bbox_inches='tight')
    print(f'  Saved figures/{name}.png and .pdf')
    plt.close(fig)


def fig1_ops_vs_n_sparse(rows):
    """Figure 1: Operation count vs n on sparse graphs (log-log)."""
    fig, ax = plt.subplots()
    gtype = 'sparse_er'
    for algo in ['hibra', 'dijkstra_fib', 'dijkstra_bin', 'batch_dijkstra']:
        data = group_median(rows, algo, gtype)
        if data:
            ns = list(data.keys())
            ops = list(data.values())
            ax.loglog(ns, ops, marker=MARKERS[algo], color=COLORS[algo],
                     label=LABELS[algo], alpha=0.85)

    # Reference lines
    ns_ref = np.logspace(3, 5, 50)
    ax.loglog(ns_ref, 2.8 * ns_ref * np.log(ns_ref), '--', color='gray',
             alpha=0.4, label=r'$c \cdot n \log n$')
    ax.loglog(ns_ref, 6.8 * ns_ref * np.log(ns_ref) / np.log(np.log(ns_ref)),
             ':', color='gray', alpha=0.4, label=r'$c \cdot n \log n / \log\log n$')

    ax.set_xlabel('Number of vertices (n)')
    ax.set_ylabel('Total operations')
    ax.set_title('Operation Count vs Graph Size (Sparse Erdos-Renyi, m=4n)')
    ax.legend(loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    save_fig(fig, 'fig1_ops_vs_n_sparse')


def fig2_ops_vs_n_dense(rows):
    """Figure 2: Operation count vs n on dense graphs."""
    fig, ax = plt.subplots()
    gtype = 'dense'
    for algo in ['hibra', 'dijkstra_bin', 'batch_dijkstra']:
        data = group_median(rows, algo, gtype)
        if data:
            ns = list(data.keys())
            ops = list(data.values())
            ax.loglog(ns, ops, marker=MARKERS[algo], color=COLORS[algo],
                     label=LABELS[algo], alpha=0.85)

    ns_ref = np.logspace(3, 4.1, 50)
    ax.loglog(ns_ref, 2 * ns_ref**2, '--', color='gray', alpha=0.4,
             label=r'$c \cdot n^2$ (edge-dominated)')

    ax.set_xlabel('Number of vertices (n)')
    ax.set_ylabel('Total operations')
    ax.set_title('Operation Count vs Graph Size (Dense, m=n(n-1)/2)')
    ax.legend(loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    save_fig(fig, 'fig2_ops_vs_n_dense')


def fig3_speedup_ratio(rows):
    """Figure 3: Speedup ratio (Dijkstra ops / HiBRA ops) across families."""
    fig, ax = plt.subplots()
    families = ['adversarial', 'sparse_er', 'layered_dag', 'grid', 'planted_spt']
    sizes = [1000, 10000, 100000]
    x = np.arange(len(families))
    width = 0.25

    for i, n in enumerate(sizes):
        ratios = []
        for gtype in families:
            dij = group_median(rows, 'dijkstra_fib', gtype)
            hib = group_median(rows, 'hibra', gtype)
            if n in dij and n in hib and hib[n] > 0:
                ratios.append(dij[n] / hib[n])
            elif n in hib:
                # Use dijkstra_bin as fallback
                dij_b = group_median(rows, 'dijkstra_bin', gtype)
                if n in dij_b and hib[n] > 0:
                    ratios.append(dij_b[n] / hib[n])
                else:
                    ratios.append(0)
            else:
                ratios.append(0)
        ax.bar(x + i * width, ratios, width, label=f'n={n:,}',
              alpha=0.8)

    ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Parity (ratio=1)')
    ax.set_xlabel('Graph Family')
    ax.set_ylabel('Operation Ratio (Dijkstra Fib / HiBRA)')
    ax.set_title('Relative Operation Count: Dijkstra vs HiBRA')
    ax.set_xticks(x + width)
    ax.set_xticklabels(families, rotation=15, ha='right')
    ax.legend(framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y')
    save_fig(fig, 'fig3_speedup_ratio')


def fig4_scalability(scale_rows):
    """Figure 4: Scalability plot n=1k to 500k."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    for gtype in ['sparse_er', 'adversarial']:
        for algo in ['hibra', 'dijkstra_bin']:
            data_ops = group_median(scale_rows, algo, gtype, 'total_ops')
            data_time = group_median(scale_rows, algo, gtype, 'wall_time_ms')
            if data_ops:
                ns = list(data_ops.keys())
                ops = list(data_ops.values())
                times = [data_time.get(n, 0) for n in ns]
                style = '-' if gtype == 'sparse_er' else '--'
                ax1.loglog(ns, ops, style, marker=MARKERS[algo],
                          color=COLORS[algo], alpha=0.85,
                          label=f'{LABELS[algo]} ({gtype})')
                ax2.loglog(ns, times, style, marker=MARKERS[algo],
                          color=COLORS[algo], alpha=0.85,
                          label=f'{LABELS[algo]} ({gtype})')

    ax1.set_xlabel('Number of vertices (n)')
    ax1.set_ylabel('Total operations')
    ax1.set_title('Scalability: Operations')
    ax1.legend(fontsize=7, framealpha=0.9)
    ax1.grid(True, alpha=0.3)

    ax2.set_xlabel('Number of vertices (n)')
    ax2.set_ylabel('Wall-clock time (ms)')
    ax2.set_title('Scalability: Wall-Clock Time')
    ax2.legend(fontsize=7, framealpha=0.9)
    ax2.grid(True, alpha=0.3)

    fig.suptitle('Scalability from n=1,000 to n=500,000', fontsize=14)
    fig.tight_layout()
    save_fig(fig, 'fig4_scalability')


def fig5_op_breakdown(rows):
    """Figure 5: Breakdown of operation types."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for idx, algo in enumerate(['hibra', 'dijkstra_bin']):
        ax = axes[idx]
        gtype = 'sparse_er'
        data_cmp = group_median(rows, algo, gtype, 'comparisons')
        data_add = group_median(rows, algo, gtype, 'additions')
        data_heap = group_median(rows, algo, gtype, 'heap_ops')

        ns = sorted(set(data_cmp.keys()) & set(data_add.keys()) & set(data_heap.keys()))
        cmps = [data_cmp[n] for n in ns]
        adds = [data_add[n] for n in ns]
        heaps = [data_heap[n] for n in ns]

        x = np.arange(len(ns))
        width = 0.28
        ax.bar(x - width, cmps, width, label='Comparisons', color='#e74c3c', alpha=0.8)
        ax.bar(x, adds, width, label='Additions', color='#3498db', alpha=0.8)
        ax.bar(x + width, heaps, width, label='Heap ops', color='#2ecc71', alpha=0.8)

        ax.set_xlabel('Graph size (n)')
        ax.set_ylabel('Operation count')
        ax.set_title(f'Operation Breakdown: {LABELS[algo]}')
        ax.set_xticks(x)
        ax.set_xticklabels([f'{n//1000}k' for n in ns], rotation=45)
        ax.legend(framealpha=0.9)
        ax.set_yscale('log')
        ax.grid(True, alpha=0.3, axis='y')

    fig.suptitle('Operation Type Breakdown (Sparse Erdos-Renyi)', fontsize=14)
    fig.tight_layout()
    save_fig(fig, 'fig5_op_breakdown')


def fig6_all_families(rows):
    """Figure 6: HiBRA performance across all graph families."""
    fig, ax = plt.subplots()
    families = ['adversarial', 'sparse_er', 'layered_dag', 'grid', 'planted_spt']
    colors_fam = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']

    for i, gtype in enumerate(families):
        data = group_median(rows, 'hibra', gtype)
        if data:
            ns = list(data.keys())
            ops = [data[n] / (n * math.log(n)) for n in ns]
            ax.semilogx(ns, ops, marker='o', color=colors_fam[i],
                       label=gtype, alpha=0.85)

    ax.set_xlabel('Number of vertices (n)')
    ax.set_ylabel('Operations / (n log n)')
    ax.set_title('HiBRA: Normalized Operation Count Across Graph Families')
    ax.legend(framealpha=0.9)
    ax.grid(True, alpha=0.3)
    save_fig(fig, 'fig6_all_families')


def main():
    print("Generating publication figures...")

    bench_rows = load_csv('results/comprehensive_benchmark.csv')
    scale_rows = load_csv('results/scalability.csv')

    fig1_ops_vs_n_sparse(bench_rows)
    fig2_ops_vs_n_dense(bench_rows)
    fig3_speedup_ratio(bench_rows)
    fig4_scalability(scale_rows)
    fig5_op_breakdown(bench_rows)
    fig6_all_families(bench_rows)

    print("\nAll figures generated in figures/")


if __name__ == "__main__":
    main()
