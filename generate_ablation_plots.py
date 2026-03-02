#!/usr/bin/env python3
"""Generate ablation study plots and analysis (item_022)."""

import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 13, 'axes.titlesize': 14,
    'legend.fontsize': 9, 'xtick.labelsize': 10, 'ytick.labelsize': 10,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'lines.linewidth': 1.8, 'lines.markersize': 6,
})


def load_data():
    with open('results/ablation_study.json') as f:
        return json.load(f)


def plot_ablation_scales(data):
    """Plot timing vs number of scales."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for idx, gtype in enumerate(['sparse', 'worst_case']):
        ax = axes[idx]
        scale_data = [r for r in data if r['ablation'] == 'num_scales'
                      and r['graph_type'] == gtype and 'error' not in r]

        variants = ['1_scale', 'sqrt_logn', 'logn', '2logn']
        variant_labels = ['1 scale', '√log n', 'log n', '2 log n']
        colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']

        for var, label, color in zip(variants, variant_labels, colors):
            rows = [r for r in scale_data if r['variant'] == var]
            rows.sort(key=lambda r: r['n'])
            ns = [r['n'] for r in rows]
            times = [r['median_time'] for r in rows]
            correct = [r.get('correct', True) for r in rows]

            ax.plot(ns, times, color=color, marker='o', label=label)
            # Mark incorrect points
            for i, c in enumerate(correct):
                if not c:
                    ax.plot(ns[i], times[i], 'x', color='red', markersize=12, markeredgewidth=3)

        ax.set_xlabel('n')
        ax.set_ylabel('Median Time (s)')
        ax.set_title(f'Number of Scales ({gtype.replace("_", " ").title()})')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
        ax.grid(True, alpha=0.3)

    fig.suptitle('Ablation: Number of Scales (red X = incorrect)', fontsize=14, y=1.02)
    fig.tight_layout()
    fig.savefig('figures/ablation_scales.png')
    fig.savefig('figures/ablation_scales.pdf')
    plt.close(fig)
    print("  Saved ablation_scales")


def plot_ablation_buckets(data):
    """Plot timing vs bucket count factor."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for idx, gtype in enumerate(['sparse', 'worst_case']):
        ax = axes[idx]
        bucket_data = [r for r in data if r['ablation'] == 'bucket_factor'
                       and r['graph_type'] == gtype and 'error' not in r]

        variants = ['0.25x_sqrt_n', '0.5x_sqrt_n', '1x_sqrt_n', '2x_sqrt_n']
        variant_labels = ['√n/4', '√n/2', '√n (default)', '2√n']
        colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']

        for var, label, color in zip(variants, variant_labels, colors):
            rows = [r for r in bucket_data if r['variant'] == var]
            rows.sort(key=lambda r: r['n'])
            ns = [r['n'] for r in rows]
            times = [r['median_time'] for r in rows]
            ax.plot(ns, times, color=color, marker='s', label=label)

        ax.set_xlabel('n')
        ax.set_ylabel('Median Time (s)')
        ax.set_title(f'Bucket Count ({gtype.replace("_", " ").title()})')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
        ax.grid(True, alpha=0.3)

    fig.suptitle('Ablation: Bucket Count Factor', fontsize=14, y=1.02)
    fig.tight_layout()
    fig.savefig('figures/ablation_buckets.png')
    fig.savefig('figures/ablation_buckets.pdf')
    plt.close(fig)
    print("  Saved ablation_buckets")


def plot_ablation_cleanup(data):
    """Plot timing vs cleanup passes."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for idx, gtype in enumerate(['sparse', 'worst_case']):
        ax = axes[idx]
        cleanup_data = [r for r in data if r['ablation'] == 'cleanup_passes'
                        and r['graph_type'] == gtype and 'error' not in r]

        variants = ['0_passes', '1_pass', '3_passes']
        variant_labels = ['0 passes', '1 pass', '3 passes (default)']
        colors = ['#1f77b4', '#ff7f0e', '#d62728']

        for var, label, color in zip(variants, variant_labels, colors):
            rows = [r for r in cleanup_data if r['variant'] == var]
            rows.sort(key=lambda r: r['n'])
            ns = [r['n'] for r in rows]
            times = [r['median_time'] for r in rows]
            correct = [r.get('correct', True) for r in rows]

            ax.plot(ns, times, color=color, marker='^', label=label)
            for i, c in enumerate(correct):
                if not c:
                    ax.plot(ns[i], times[i], 'x', color='red', markersize=12, markeredgewidth=3)

        ax.set_xlabel('n')
        ax.set_ylabel('Median Time (s)')
        ax.set_title(f'Cleanup Passes ({gtype.replace("_", " ").title()})')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
        ax.grid(True, alpha=0.3)

    fig.suptitle('Ablation: Cleanup Passes (red X = incorrect)', fontsize=14, y=1.02)
    fig.tight_layout()
    fig.savefig('figures/ablation_cleanup.png')
    fig.savefig('figures/ablation_cleanup.pdf')
    plt.close(fig)
    print("  Saved ablation_cleanup")


def plot_combined_ablation(data):
    """Combined ablation results figure."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Panel 1: Scales (sparse only, normalized to default)
    ax = axes[0]
    scale_data = [r for r in data if r['ablation'] == 'num_scales'
                  and r['graph_type'] == 'sparse' and 'error' not in r]
    default_times = {}
    for r in scale_data:
        if r['variant'] == 'sqrt_logn':
            default_times[r['n']] = r['median_time']

    for var, label, color in [('1_scale', '1 scale', '#1f77b4'),
                                ('sqrt_logn', '√log n (default)', '#2ca02c'),
                                ('logn', 'log n', '#ff7f0e'),
                                ('2logn', '2 log n', '#d62728')]:
        rows = [r for r in scale_data if r['variant'] == var]
        rows.sort(key=lambda r: r['n'])
        ns = [r['n'] for r in rows]
        ratios = [r['median_time'] / default_times.get(r['n'], r['median_time'])
                  for r in rows]
        ax.plot(ns, ratios, color=color, marker='o', label=label)

    ax.set_xlabel('n')
    ax.set_ylabel('Time / Default Time')
    ax.set_title('Number of Scales')
    ax.set_xscale('log')
    ax.axhline(y=1.0, color='black', alpha=0.3, linestyle='--')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 2: Buckets (sparse only, normalized)
    ax = axes[1]
    bucket_data = [r for r in data if r['ablation'] == 'bucket_factor'
                   and r['graph_type'] == 'sparse' and 'error' not in r]
    default_bt = {}
    for r in bucket_data:
        if r['variant'] == '1x_sqrt_n':
            default_bt[r['n']] = r['median_time']

    for var, label, color in [('0.25x_sqrt_n', '√n/4', '#1f77b4'),
                                ('0.5x_sqrt_n', '√n/2', '#2ca02c'),
                                ('1x_sqrt_n', '√n (default)', '#ff7f0e'),
                                ('2x_sqrt_n', '2√n', '#d62728')]:
        rows = [r for r in bucket_data if r['variant'] == var]
        rows.sort(key=lambda r: r['n'])
        ns = [r['n'] for r in rows]
        ratios = [r['median_time'] / default_bt.get(r['n'], r['median_time'])
                  for r in rows]
        ax.plot(ns, ratios, color=color, marker='s', label=label)

    ax.set_xlabel('n')
    ax.set_ylabel('Time / Default Time')
    ax.set_title('Bucket Count Factor')
    ax.set_xscale('log')
    ax.axhline(y=1.0, color='black', alpha=0.3, linestyle='--')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 3: Cleanup (sparse only, normalized)
    ax = axes[2]
    cleanup_data = [r for r in data if r['ablation'] == 'cleanup_passes'
                    and r['graph_type'] == 'sparse' and 'error' not in r]
    default_ct = {}
    for r in cleanup_data:
        if r['variant'] == '3_passes':
            default_ct[r['n']] = r['median_time']

    for var, label, color in [('0_passes', '0 passes', '#1f77b4'),
                                ('1_pass', '1 pass', '#ff7f0e'),
                                ('3_passes', '3 passes (default)', '#d62728')]:
        rows = [r for r in cleanup_data if r['variant'] == var]
        rows.sort(key=lambda r: r['n'])
        ns = [r['n'] for r in rows]
        ratios = [r['median_time'] / default_ct.get(r['n'], r['median_time'])
                  for r in rows]
        ax.plot(ns, ratios, color=color, marker='^', label=label)

    ax.set_xlabel('n')
    ax.set_ylabel('Time / Default Time')
    ax.set_title('Cleanup Passes')
    ax.set_xscale('log')
    ax.axhline(y=1.0, color='black', alpha=0.3, linestyle='--')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    fig.suptitle('Ablation Study: Normalized Performance (Sparse Graphs)', fontsize=14, y=1.02)
    fig.tight_layout()
    fig.savefig('figures/ablation_results.png')
    fig.savefig('figures/ablation_results.pdf')
    plt.close(fig)
    print("  Saved ablation_results (combined)")


def main():
    os.makedirs('figures', exist_ok=True)
    data = load_data()
    print(f"Loaded {len(data)} ablation results")

    plot_ablation_scales(data)
    plot_ablation_buckets(data)
    plot_ablation_cleanup(data)
    plot_combined_ablation(data)

    print("\nAll ablation plots generated!")


if __name__ == '__main__':
    main()
