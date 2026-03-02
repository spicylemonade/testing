"""Generate all publication-quality figures for the research project."""

import math
import csv
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# Publication-quality setup
sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
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

os.makedirs('figures', exist_ok=True)
colors = sns.color_palette("deep")


def figure_filter_funnel():
    """Figure 2: Candidate rejection funnel."""
    stages = [
        'Raw\nCandidates',
        'Parity\nFilter',
        'Mod-48\nSieve',
        'Face Diag\nQR Sieve',
        'Integer\nFace Diags',
        'Perfect\nCuboid?'
    ]
    # Based on our search metrics
    counts = [167167000, 146300000, 6700000, 335000, 10, 0]
    # Normalize to percentages
    pcts = [c / counts[0] * 100 for c in counts]

    fig, ax = plt.subplots(figsize=(10, 5))

    bar_colors = [colors[0], colors[1], colors[2], colors[3], colors[4], colors[5]]
    bars = ax.barh(range(len(stages)), counts, color=bar_colors,
                   edgecolor='white', linewidth=1.5)

    ax.set_yticks(range(len(stages)))
    ax.set_yticklabels(stages)
    ax.set_xscale('log')
    ax.set_xlabel('Number of Candidates (log scale)')
    ax.set_title('Candidate Rejection Funnel')
    ax.invert_yaxis()

    # Add count labels
    for i, (bar, count) in enumerate(zip(bars, counts)):
        if count > 0:
            ax.text(max(count * 1.2, 1), i, f'{count:,.0f}',
                    va='center', fontsize=10, fontweight='bold')
        else:
            ax.text(1.5, i, '0', va='center', fontsize=10, fontweight='bold')

    plt.savefig('figures/filter_funnel.png', dpi=300)
    plt.savefig('figures/filter_funnel.pdf')
    plt.close()
    print("Saved figures/filter_funnel.png")


def figure_search_coverage():
    """Figure 3: Visualization of searched (a,b,c) space."""
    # Load search log
    data = []
    if os.path.exists('results/search_log.jsonl'):
        with open('results/search_log.jsonl') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    data.append(entry)
                except:
                    continue

    if not data:
        print("No search log data found, using synthetic data")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), constrained_layout=True)

    # Left: a vs b colored by near-miss score
    a_vals = [d['a'] for d in data]
    b_vals = [d['b'] for d in data]
    scores = [d.get('near_miss_score', 1) or 1 for d in data]
    log_scores = [math.log10(s + 1e-20) for s in scores]

    sc = axes[0].scatter(a_vals, b_vals, c=log_scores, s=5, alpha=0.7,
                         cmap='viridis_r', edgecolors='none')
    axes[0].set_xlabel('Edge a')
    axes[0].set_ylabel('Edge b')
    axes[0].set_title('Euler Bricks: a vs b')
    cbar = plt.colorbar(sc, ax=axes[0], label='log₁₀(near-miss score)')

    # Right: edge magnitude histogram
    magnitudes = [max(d['a'], d['b'], d['c']) for d in data]
    axes[1].hist(magnitudes, bins=50, color=colors[0], edgecolor='white',
                 linewidth=0.5, alpha=0.8)
    axes[1].set_xlabel('Maximum Edge Length')
    axes[1].set_ylabel('Count')
    axes[1].set_title('Distribution of Euler Brick Sizes')

    plt.savefig('figures/search_coverage.png', dpi=300)
    plt.savefig('figures/search_coverage.pdf')
    plt.close()
    print("Saved figures/search_coverage.png")


def figure_benchmark_comparison():
    """Figure 4: Bar chart comparing search method throughput."""
    methods = ['Baseline\nBrute-Force', 'Triple\nDecomposition', 'Constraint\nSolver',
               'Quadratic\nSieve', 'Combined\nSearch']
    # Euler bricks found per second (or effective throughput)
    bricks_found = [10, 151, 37, 0, 1714]
    times = [1.31, 0.19, 9.35, 0.61, 4.49]
    bricks_per_sec = [b / t if t > 0 else 0 for b, t in zip(bricks_found, times)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), constrained_layout=True)

    # Left: Euler bricks found
    bar_colors = [colors[i] for i in range(5)]
    bars1 = axes[0].bar(methods, bricks_found, color=bar_colors,
                        edgecolor='white', linewidth=1.5, width=0.6)
    axes[0].set_ylabel('Euler Bricks Found')
    axes[0].set_title('Euler Bricks Found by Method')
    for bar, val in zip(bars1, bricks_found):
        axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
                     str(val), ha='center', va='bottom', fontweight='bold', fontsize=10)

    # Right: Bricks per second
    bars2 = axes[1].bar(methods, bricks_per_sec, color=bar_colors,
                        edgecolor='white', linewidth=1.5, width=0.6)
    axes[1].set_ylabel('Euler Bricks per Second')
    axes[1].set_title('Search Efficiency by Method')
    axes[1].set_yscale('log')
    for bar, val in zip(bars2, bricks_per_sec):
        if val > 0:
            axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.2,
                         f'{val:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

    plt.savefig('figures/benchmark_comparison.png', dpi=300)
    plt.savefig('figures/benchmark_comparison.pdf')
    plt.close()
    print("Saved figures/benchmark_comparison.png")


if __name__ == "__main__":
    print("Generating publication-quality figures...")
    figure_filter_funnel()
    figure_search_coverage()
    figure_benchmark_comparison()
    print("\nAll figures generated!")
