#!/usr/bin/env python3
"""Generate realistic graph comparison plot (item_021)."""

import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 13, 'axes.titlesize': 14,
    'legend.fontsize': 9, 'xtick.labelsize': 10, 'ytick.labelsize': 10,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'lines.linewidth': 1.8, 'lines.markersize': 8,
})

ALGO_COLORS = {
    'dijkstra_fibonacci': '#1f77b4',
    'dijkstra_binary': '#2ca02c',
    'duan_stoc2025': '#ff7f0e',
    'dams_sssp': '#d62728',
}
ALGO_LABELS = {
    'dijkstra_fibonacci': 'Dijkstra+Fib',
    'dijkstra_binary': 'Dijkstra+Bin',
    'duan_stoc2025': 'Duan 2025',
    'dams_sssp': 'DAMS-SSSP',
}


def main():
    os.makedirs('figures', exist_ok=True)
    with open('results/realistic_benchmarks.json') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} realistic benchmark results")

    # Group by graph type
    graph_types = sorted(set(r['graph_type'] for r in data))

    fig, axes = plt.subplots(1, len(graph_types), figsize=(6 * len(graph_types), 5))
    if len(graph_types) == 1:
        axes = [axes]

    for idx, gtype in enumerate(graph_types):
        ax = axes[idx]
        gdata = [r for r in data if r['graph_type'] == gtype and 'error' not in r]

        algos = ['dijkstra_fibonacci', 'dijkstra_binary', 'duan_stoc2025', 'dams_sssp']
        present_algos = [a for a in algos if any(r['algorithm'] == a for r in gdata)]

        x = np.arange(len(present_algos))
        times = []
        stds = []
        for algo in present_algos:
            rows = [r for r in gdata if r['algorithm'] == algo]
            if rows:
                times.append(rows[0]['median_time'])
                stds.append(rows[0]['std_time'])
            else:
                times.append(0)
                stds.append(0)

        colors = [ALGO_COLORS[a] for a in present_algos]
        labels = [ALGO_LABELS[a] for a in present_algos]

        bars = ax.bar(x, times, yerr=stds, capsize=4, color=colors, edgecolor='black', linewidth=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=9)

        n = gdata[0]['n'] if gdata else 0
        m = gdata[0]['m'] if gdata else 0
        gname_pretty = gtype.replace('_', ' ').title()
        ax.set_title(f'{gname_pretty}\n(n={n:,}, m={m:,})')
        ax.set_ylabel('Median Time (s)')
        ax.grid(True, alpha=0.3, axis='y')

        # Add time labels on bars
        for bar, t in zip(bars, times):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{t:.2f}s', ha='center', va='bottom', fontsize=8)

    fig.suptitle('Performance on Realistic Graph Instances', fontsize=15, y=1.02)
    fig.tight_layout()
    fig.savefig('figures/realistic_comparison.png')
    fig.savefig('figures/realistic_comparison.pdf')
    plt.close(fig)
    print("Saved figures/realistic_comparison.png/.pdf")


if __name__ == '__main__':
    main()
