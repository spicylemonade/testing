#!/usr/bin/env python3
"""
Generate publication-grade benchmark figures for DEFLATE decoder comparison.
"""
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

RESULTS_FILE = 'results/benchmark_final.json'
FIGURES_DIR = 'figures'

def load_results(path):
    with open(path) as f:
        d = json.load(f)
    return d['results']

def build_data(results):
    """Build dict: (file, level, decoder) -> median_throughput"""
    data = {}
    for entry in results:
        f = entry['file']
        level = entry['compression_level']
        dec = entry['decoder']
        median = entry['throughput_MBps']['median']
        data[(f, level, dec)] = median
    return data

def geomean(values):
    values = [v for v in values if v > 0]
    if not values:
        return 0
    return np.exp(np.mean(np.log(values)))

def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    results = load_results(RESULTS_FILE)
    data = build_data(results)

    decoders = ['naive', 'zlib', 'zlib-ng', 'libdeflate', 'fast']
    decoder_labels = ['Naive', 'zlib', 'zlib-ng', 'libdeflate', 'Ours (fast)']
    colors = ['#999999', '#4477AA', '#228833', '#EE6677', '#CCBB44']

    # Get unique files (sorted)
    files = sorted(set(f for (f, l, d) in data.keys()))
    levels = sorted(set(l for (f, l, d) in data.keys()))

    # Shorten filenames
    def short_name(f):
        f = f.replace('.txt', '').replace('.bin', '').replace('.c', '')
        f = f.replace('.json', '').replace('.xml', '').replace('.html', '')
        f = f.replace('.css', '').replace('.js', '').replace('.csv', '')
        return f

    short_names = [short_name(f) for f in files]

    # ==================================================================
    # Figure 1: Throughput bar chart (level 6)
    # ==================================================================
    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(files))
    width = 0.15

    for i, (dec, label, color) in enumerate(zip(decoders, decoder_labels, colors)):
        vals = [data.get((f, 6, dec), 0) for f in files]
        display = [min(v, 45000) for v in vals]
        ax.bar(x + i * width - 2 * width, display, width,
               label=label, color=color, edgecolor='white', linewidth=0.3)

    ax.set_xlabel('Corpus File', fontsize=11)
    ax.set_ylabel('Throughput (MB/s)', fontsize=11)
    ax.set_title('DEFLATE Decompression Throughput Comparison (Level 6)', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(short_names, rotation=45, ha='right', fontsize=8)
    ax.legend(fontsize=9, loc='upper left', ncol=5)
    ax.set_yscale('log')
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.set_ylim(50, 50000)
    ax.grid(axis='y', alpha=0.3, which='both')

    plt.tight_layout()
    for fmt in ['png', 'pdf']:
        plt.savefig(f'{FIGURES_DIR}/throughput_comparison.{fmt}', dpi=150)
    print('Saved throughput_comparison.png/pdf')
    plt.close()

    # ==================================================================
    # Figure 2: Speedup heatmap (level 6)
    # ==================================================================
    compare_decoders = ['naive', 'zlib-ng', 'libdeflate', 'fast']
    compare_labels = ['Naive', 'zlib-ng', 'libdeflate', 'Ours']

    speedup_matrix = []
    for f in files:
        row = []
        zlib_thr = data.get((f, 6, 'zlib'), 1)
        for dec in compare_decoders:
            thr = data.get((f, 6, dec), 0)
            row.append(thr / zlib_thr if zlib_thr > 0 else 0)
        speedup_matrix.append(row)

    speedup_arr = np.array(speedup_matrix)

    fig, ax = plt.subplots(figsize=(8, 10))
    im = ax.imshow(speedup_arr, cmap='RdYlGn', aspect='auto',
                   vmin=0, vmax=max(4, speedup_arr.max() * 0.9))

    ax.set_xticks(range(len(compare_labels)))
    ax.set_xticklabels(compare_labels, fontsize=10)
    ax.set_yticks(range(len(files)))
    ax.set_yticklabels(short_names, fontsize=8)
    ax.set_title('Speedup over zlib (Level 6)', fontsize=13, fontweight='bold')

    for i in range(len(files)):
        for j in range(len(compare_decoders)):
            val = speedup_arr[i, j]
            color = 'white' if val < 0.5 or val > 3.5 else 'black'
            ax.text(j, i, f'{val:.2f}x', ha='center', va='center',
                    fontsize=7, color=color, fontweight='bold')

    cbar = plt.colorbar(im, label='Speedup vs zlib', shrink=0.8)
    plt.tight_layout()
    for fmt in ['png', 'pdf']:
        plt.savefig(f'{FIGURES_DIR}/speedup_heatmap.{fmt}', dpi=150)
    print('Saved speedup_heatmap.png/pdf')
    plt.close()

    # ==================================================================
    # Figure 3: Geomean summary by compression level
    # ==================================================================
    fig, ax = plt.subplots(figsize=(8, 5))
    bar_width = 0.15
    x_levels = np.arange(len(levels))

    for i, (dec, label, color) in enumerate(zip(decoders, decoder_labels, colors)):
        gmeans = []
        for level in levels:
            vals = [data.get((f, level, dec), 0) for f in files]
            gmeans.append(geomean(vals))
        bars = ax.bar(x_levels + i * bar_width - 2 * bar_width, gmeans, bar_width,
                      label=label, color=color, edgecolor='white', linewidth=0.3)
        # Add value labels
        for bar, gm in zip(bars, gmeans):
            if gm > 100:
                ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 30,
                        f'{gm:.0f}', ha='center', va='bottom', fontsize=6, rotation=90)

    ax.set_xlabel('Compression Level', fontsize=11)
    ax.set_ylabel('Geometric Mean Throughput (MB/s)', fontsize=11)
    ax.set_title('Decompression Throughput by Compression Level', fontsize=13, fontweight='bold')
    ax.set_xticks(x_levels)
    ax.set_xticklabels([f'Level {l}' for l in levels], fontsize=10)
    ax.legend(fontsize=9, ncol=3, loc='upper left')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    for fmt in ['png', 'pdf']:
        plt.savefig(f'{FIGURES_DIR}/throughput_by_level.{fmt}', dpi=150)
    print('Saved throughput_by_level.png/pdf')
    plt.close()

    # ==================================================================
    # Summary statistics
    # ==================================================================
    print('\n=== Geometric Mean Throughput (MB/s) ===')
    for level in levels:
        print(f'\n  Level {level}:')
        zlib_gm = geomean([data.get((f, level, 'zlib'), 0) for f in files])
        for dec, label in zip(decoders, decoder_labels):
            vals = [data.get((f, level, dec), 0) for f in files]
            gm = geomean(vals)
            print(f'    {label:15s}: {gm:8.1f} MB/s  ({gm/zlib_gm:.2f}x zlib)')

    # Per-file speedup of fast vs zlib-ng at level 6
    print('\n=== Per-file: fast vs zlib-ng (Level 6) ===')
    for f in files:
        fast_thr = data.get((f, 6, 'fast'), 0)
        zlibng_thr = data.get((f, 6, 'zlib-ng'), 0)
        ratio = fast_thr / zlibng_thr if zlibng_thr > 0 else 0
        print(f'  {short_name(f):25s}: fast={fast_thr:8.1f}  zlib-ng={zlibng_thr:8.1f}  ratio={ratio:.2f}')

if __name__ == '__main__':
    main()
