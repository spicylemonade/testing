#!/usr/bin/env python3
"""
Generate publication-quality figures for GCD algorithm benchmarks.
Produces 5 figures in figures/ (PNG 300 DPI + PDF).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

np.random.seed(42)

# Style
sns.set_theme(style='whitegrid', font_scale=1.1)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9

os.makedirs('figures', exist_ok=True)

# Load data
raw = pd.read_csv('results/phase4/raw_trials.csv')
summary = pd.read_csv('results/phase4/full_benchmarks.csv')

# Color scheme
ALGO_COLORS = {
    'euclid': '#636363',
    'stein_classic': '#2171b5',
    'binary_ctz': '#6baed6',
    'binary_opt': '#9ecae1',
    'branchless_hybrid': '#fc8d59',
    'novel_best': '#fdae61',
    'lut_hybrid': '#fee08b',
    'lut_hybrid_mod': '#d9ef8b',
    'combined': '#e31a1c',
    'combined_nolut': '#fb6a4a',
    'combined_128': '#e31a1c',
}

ALGO_ORDER_64 = ['euclid', 'stein_classic', 'binary_ctz', 'binary_opt',
                 'branchless_hybrid', 'novel_best', 'lut_hybrid',
                 'lut_hybrid_mod', 'combined_nolut', 'combined']
ALGO_LABELS = {
    'euclid': 'Euclidean',
    'stein_classic': "Stein's Classic",
    'binary_ctz': 'Binary+CTZ',
    'binary_opt': 'Binary+Opt',
    'branchless_hybrid': 'Branchless',
    'novel_best': 'Novel Best',
    'lut_hybrid': 'LUT Hybrid',
    'lut_hybrid_mod': 'LUT+Mod',
    'combined_nolut': 'Combined (no LUT)',
    'combined': 'Combined (Ours)',
    'combined_128': 'Combined 128-bit',
}

# ============================================================
# Figure 1: Bar chart — all algorithms, 64-bit, uniform
# ============================================================
print("Figure 1: 64-bit uniform comparison...")
fig, ax = plt.subplots(figsize=(10, 5))

df64_uniform = summary[(summary['bit_width'] == 64) & (summary['distribution'] == 'uniform')]
df64_uniform = df64_uniform.set_index('algorithm').reindex(ALGO_ORDER_64).reset_index()

colors = [ALGO_COLORS.get(a, '#999999') for a in df64_uniform['algorithm']]
bars = ax.bar(range(len(df64_uniform)), df64_uniform['median_ns'],
              yerr=[df64_uniform['median_ns'] - df64_uniform['p5_ns'],
                    df64_uniform['p95_ns'] - df64_uniform['median_ns']],
              color=colors, edgecolor='black', linewidth=0.5,
              capsize=3, error_kw={'linewidth': 0.8})

# Highlight the winner
winner_idx = df64_uniform['algorithm'].tolist().index('combined')
bars[winner_idx].set_edgecolor('#e31a1c')
bars[winner_idx].set_linewidth(2)

ax.set_xticks(range(len(df64_uniform)))
ax.set_xticklabels([ALGO_LABELS.get(a, a) for a in df64_uniform['algorithm']],
                   rotation=35, ha='right')
ax.set_ylabel('Median Latency (ns/op)')
ax.set_title('GCD Algorithm Comparison — 64-bit Uniform Random Inputs')

# Add value labels
for i, (_, row) in enumerate(df64_uniform.iterrows()):
    ax.text(i, row['median_ns'] + 3, f"{row['median_ns']:.1f}",
            ha='center', va='bottom', fontsize=7.5)

# Reference line for stein_classic
stein_val = df64_uniform[df64_uniform['algorithm'] == 'stein_classic']['median_ns'].values[0]
ax.axhline(y=stein_val, color='#2171b5', linestyle='--', alpha=0.5, linewidth=0.8)
ax.text(len(df64_uniform)-0.5, stein_val + 1, f"Stein's: {stein_val:.1f}ns",
        fontsize=8, color='#2171b5', ha='right')

ax.set_ylim(0, max(df64_uniform['median_ns']) * 1.15)
plt.tight_layout()
fig.savefig('figures/fig1_64bit_uniform.png', dpi=300, bbox_inches='tight')
fig.savefig('figures/fig1_64bit_uniform.pdf', bbox_inches='tight')
plt.close()

# ============================================================
# Figure 2: Grouped bar chart — combined vs baselines, all distributions
# ============================================================
print("Figure 2: Combined vs baselines across distributions...")
fig, ax = plt.subplots(figsize=(11, 5.5))

compare_algos = ['euclid', 'stein_classic', 'binary_ctz', 'combined']
dists = ['uniform', 'skewed', 'nearly_equal', 'fibonacci', 'coprime']
dist_labels = ['Uniform', 'Skewed', 'Nearly Equal', 'Fibonacci', 'Coprime']

x = np.arange(len(dists))
width = 0.20
offsets = np.array([-1.5, -0.5, 0.5, 1.5]) * width

for i, algo in enumerate(compare_algos):
    vals = []
    errs_lo = []
    errs_hi = []
    for dist in dists:
        row = summary[(summary['algorithm'] == algo) & (summary['bit_width'] == 64) &
                       (summary['distribution'] == dist)]
        if len(row) == 0:
            vals.append(0)
            errs_lo.append(0)
            errs_hi.append(0)
        else:
            vals.append(row['median_ns'].values[0])
            errs_lo.append(row['median_ns'].values[0] - row['p5_ns'].values[0])
            errs_hi.append(row['p95_ns'].values[0] - row['median_ns'].values[0])
    
    bars = ax.bar(x + offsets[i], vals, width,
                  yerr=[errs_lo, errs_hi],
                  label=ALGO_LABELS[algo],
                  color=ALGO_COLORS[algo], edgecolor='black', linewidth=0.4,
                  capsize=2, error_kw={'linewidth': 0.6})

ax.set_xticks(x)
ax.set_xticklabels(dist_labels)
ax.set_ylabel('Median Latency (ns/op)')
ax.set_title('GCD Algorithm Performance Across Input Distributions (64-bit)')
ax.legend(loc='upper right', fontsize=9)
ax.set_ylim(0, 260)
plt.tight_layout()
fig.savefig('figures/fig2_distributions_comparison.png', dpi=300, bbox_inches='tight')
fig.savefig('figures/fig2_distributions_comparison.pdf', bbox_inches='tight')
plt.close()

# ============================================================
# Figure 3: 128-bit comparison bar chart
# ============================================================
print("Figure 3: 128-bit comparison...")
fig, ax = plt.subplots(figsize=(10, 5))

algos_128 = ['euclid', 'stein_classic', 'binary_ctz', 'binary_opt', 'combined_128']
df128_uniform = summary[(summary['bit_width'] == 128) & (summary['distribution'] == 'uniform')]
df128_uniform = df128_uniform.set_index('algorithm').reindex(algos_128).reset_index()

colors_128 = [ALGO_COLORS.get(a, '#999999') for a in df128_uniform['algorithm']]
bars = ax.bar(range(len(df128_uniform)), df128_uniform['median_ns'],
              yerr=[df128_uniform['median_ns'] - df128_uniform['p5_ns'],
                    df128_uniform['p95_ns'] - df128_uniform['median_ns']],
              color=colors_128, edgecolor='black', linewidth=0.5,
              capsize=3, error_kw={'linewidth': 0.8})

ax.set_xticks(range(len(df128_uniform)))
ax.set_xticklabels([ALGO_LABELS.get(a, a) for a in df128_uniform['algorithm']],
                   rotation=25, ha='right')
ax.set_ylabel('Median Latency (ns/op)')
ax.set_title('GCD Algorithm Comparison — 128-bit Uniform Random Inputs')

for i, (_, row) in enumerate(df128_uniform.iterrows()):
    ax.text(i, row['median_ns'] + 5, f"{row['median_ns']:.1f}",
            ha='center', va='bottom', fontsize=8)

ax.set_ylim(0, max(df128_uniform['median_ns']) * 1.12)
plt.tight_layout()
fig.savefig('figures/fig3_128bit_uniform.png', dpi=300, bbox_inches='tight')
fig.savefig('figures/fig3_128bit_uniform.pdf', bbox_inches='tight')
plt.close()

# ============================================================
# Figure 4: Speedup heatmap — combined vs stein_classic
# ============================================================
print("Figure 4: Speedup heatmap...")
fig, ax = plt.subplots(figsize=(8, 5))

# Build speedup matrix: bit_width x distribution
bit_widths = [64, 128]
bw_labels = ['64-bit', '128-bit']

speedup_data = []
for bw in bit_widths:
    row = []
    for dist in dists:
        if bw == 64:
            baseline_row = summary[(summary['algorithm'] == 'stein_classic') & 
                                   (summary['bit_width'] == bw) & (summary['distribution'] == dist)]
            novel_row = summary[(summary['algorithm'] == 'combined') &
                                (summary['bit_width'] == bw) & (summary['distribution'] == dist)]
        else:
            baseline_row = summary[(summary['algorithm'] == 'stein_classic') &
                                   (summary['bit_width'] == bw) & (summary['distribution'] == dist)]
            novel_row = summary[(summary['algorithm'] == 'combined_128') &
                                (summary['bit_width'] == bw) & (summary['distribution'] == dist)]
        
        if len(baseline_row) > 0 and len(novel_row) > 0:
            sp = baseline_row['median_ns'].values[0] / novel_row['median_ns'].values[0]
            row.append(sp)
        else:
            row.append(1.0)
    speedup_data.append(row)

speedup_arr = np.array(speedup_data)

# Custom colormap: red < 1.0, white = 1.0, green > 1.0
from matplotlib.colors import TwoSlopeNorm
vmin = min(speedup_arr.min(), 0.7)
vmax = max(speedup_arr.max(), 3.0)
norm = TwoSlopeNorm(vmin=vmin, vcenter=1.0, vmax=vmax)

im = ax.imshow(speedup_arr, cmap='RdYlGn', norm=norm, aspect='auto')

ax.set_xticks(range(len(dists)))
ax.set_xticklabels(dist_labels)
ax.set_yticks(range(len(bw_labels)))
ax.set_yticklabels(bw_labels)

# Annotate cells
for i in range(len(bw_labels)):
    for j in range(len(dists)):
        val = speedup_arr[i, j]
        color = 'white' if abs(val - 1.0) > 0.8 else 'black'
        pct = (val - 1.0) * 100
        sign = '+' if pct > 0 else ''
        ax.text(j, i, f"{val:.2f}x\n({sign}{pct:.0f}%)",
                ha='center', va='center', fontsize=9, color=color, fontweight='bold')

ax.set_title('Speedup: Combined / Stein\'s Classic (>1.0 = novel is faster)')
plt.colorbar(im, ax=ax, label='Speedup Ratio', shrink=0.8)
plt.tight_layout()
fig.savefig('figures/fig4_speedup_heatmap.png', dpi=300, bbox_inches='tight')
fig.savefig('figures/fig4_speedup_heatmap.pdf', bbox_inches='tight')
plt.close()

# ============================================================
# Figure 5: Box/violin plot of trial distributions for key algorithms
# ============================================================
print("Figure 5: Trial distribution violin plots...")
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

key_algos = ['stein_classic', 'combined', 'lut_hybrid']
key_dists = ['uniform', 'skewed', 'nearly_equal']

for ax_i, dist in enumerate(key_dists):
    ax = axes[ax_i]
    plot_data = []
    for algo in key_algos:
        trials = raw[(raw['algorithm'] == algo) & (raw['bit_width'] == 64) &
                      (raw['distribution'] == dist)]['ns_per_op'].values
        for t in trials:
            plot_data.append({'Algorithm': ALGO_LABELS[algo], 'ns/op': t})
    
    plot_df = pd.DataFrame(plot_data)
    
    palette = {ALGO_LABELS[a]: ALGO_COLORS[a] for a in key_algos}
    sns.violinplot(data=plot_df, x='Algorithm', y='ns/op', ax=ax,
                   palette=palette, inner='box', linewidth=0.8, cut=0)
    ax.set_title(dist_labels[key_dists.index(dist)])
    ax.set_xlabel('')
    if ax_i > 0:
        ax.set_ylabel('')
    else:
        ax.set_ylabel('Latency (ns/op)')
    ax.tick_params(axis='x', rotation=20)

fig.suptitle('Trial Distribution for Key Algorithms (64-bit, 50 trials each)', fontsize=12, y=1.02)
plt.tight_layout()
fig.savefig('figures/fig5_violin_distributions.png', dpi=300, bbox_inches='tight')
fig.savefig('figures/fig5_violin_distributions.pdf', bbox_inches='tight')
plt.close()

print("All figures generated in figures/")
print("Files:")
for f in sorted(os.listdir('figures')):
    size = os.path.getsize(f'figures/{f}')
    print(f"  {f} ({size:,} bytes)")
