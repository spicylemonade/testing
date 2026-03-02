#!/usr/bin/env python3
"""Operation-count analysis to validate asymptotic claims (item_020).

Produces:
  - results/operation_analysis.json
  - figures/operation_ratios.png
"""

import json
import math
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
    with open('results/full_benchmarks.json') as f:
        return json.load(f)


def filter_valid(data, graph_type, algorithm):
    rows = [r for r in data if r['graph_type'] == graph_type
            and r['algorithm'] == algorithm and 'error' not in r]
    rows.sort(key=lambda r: r['n'])
    return rows


def r_squared(y_actual, y_predicted):
    """Compute R² goodness of fit."""
    y_actual = np.array(y_actual, dtype=float)
    y_predicted = np.array(y_predicted, dtype=float)
    ss_res = np.sum((y_actual - y_predicted) ** 2)
    ss_tot = np.sum((y_actual - np.mean(y_actual)) ** 2)
    if ss_tot == 0:
        return 1.0 if ss_res == 0 else 0.0
    return 1.0 - ss_res / ss_tot


def fit_and_evaluate(ns, ms, ops, label):
    """Fit ops to candidate complexity functions and compute R² values."""
    ns = np.array(ns, dtype=float)
    ms = np.array(ms, dtype=float)
    ops = np.array(ops, dtype=float)

    if len(ns) < 2 or np.max(ops) < 10:
        return None

    results = {}

    # Candidate 1: c1*m + c2*n*log(n)
    basis_mnlogn = ms + ns * np.log2(ns)
    c_mnlogn = np.sum(ops * basis_mnlogn) / np.sum(basis_mnlogn ** 2)
    pred_mnlogn = c_mnlogn * basis_mnlogn
    r2_mnlogn = r_squared(ops, pred_mnlogn)
    results['m_plus_nlogn'] = {
        'formula': 'c*(m + n*log(n))',
        'c': float(c_mnlogn),
        'R2': float(r2_mnlogn),
        'predicted': pred_mnlogn.tolist(),
    }

    # Candidate 2: c*m*log^{2/3}(n)
    basis_mlog23 = ms * np.power(np.log2(ns), 2.0 / 3.0)
    c_mlog23 = np.sum(ops * basis_mlog23) / np.sum(basis_mlog23 ** 2)
    pred_mlog23 = c_mlog23 * basis_mlog23
    r2_mlog23 = r_squared(ops, pred_mlog23)
    results['m_log23n'] = {
        'formula': 'c*m*log^(2/3)(n)',
        'c': float(c_mlog23),
        'R2': float(r2_mlog23),
    }

    # Candidate 3: c*m*sqrt(log(n))
    basis_msqrtlog = ms * np.sqrt(np.log2(ns))
    c_msqrtlog = np.sum(ops * basis_msqrtlog) / np.sum(basis_msqrtlog ** 2)
    pred_msqrtlog = c_msqrtlog * basis_msqrtlog
    r2_msqrtlog = r_squared(ops, pred_msqrtlog)
    results['m_sqrtlogn'] = {
        'formula': 'c*m*sqrt(log(n))',
        'c': float(c_msqrtlog),
        'R2': float(r2_msqrtlog),
    }

    # Candidate 4: c*m (linear in m)
    c_m = np.sum(ops * ms) / np.sum(ms ** 2)
    pred_m = c_m * ms
    r2_m = r_squared(ops, pred_m)
    results['m_linear'] = {
        'formula': 'c*m',
        'c': float(c_m),
        'R2': float(r2_m),
    }

    # Ratio of actual ops to m + n log n
    ratio_mnlogn = (ops / (ms + ns * np.log2(ns))).tolist()

    return {
        'label': label,
        'n_values': ns.tolist(),
        'm_values': ms.tolist(),
        'total_ops': ops.tolist(),
        'ratio_to_mnlogn': ratio_mnlogn,
        'fits': results,
    }


def main():
    os.makedirs('results', exist_ok=True)
    os.makedirs('figures', exist_ok=True)

    data = load_data()
    print(f"Loaded {len(data)} results")

    analysis = {}

    # Analyze each algorithm on each graph type
    for gtype in ['sparse', 'grid', 'worst_case']:
        for algo in ['dijkstra_fibonacci', 'dijkstra_binary', 'duan_stoc2025', 'dams_sssp']:
            rows = filter_valid(data, gtype, algo)
            if not rows:
                continue

            ns = [r['n'] for r in rows]
            ms = [r['m'] for r in rows]
            total_ops = [r['comparisons'] + r['additions'] + r['heap_ops'] for r in rows]

            key = f"{algo}__{gtype}"
            result = fit_and_evaluate(ns, ms, total_ops, f"{algo} on {gtype}")
            if result:
                analysis[key] = result

    # Save analysis
    with open('results/operation_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"Saved results/operation_analysis.json ({len(analysis)} entries)")

    # Print summary table
    print("\n" + "=" * 90)
    print(f"{'Algorithm + Graph':<40s} {'c*m':>8s} {'c*(m+nlogn)':>12s} {'c*m·lg^2/3':>12s} {'c*m·√lg':>12s}")
    print("=" * 90)
    for key, val in sorted(analysis.items()):
        fits = val['fits']
        print(f"{val['label']:<40s} "
              f"{fits['m_linear']['R2']:>8.4f} "
              f"{fits['m_plus_nlogn']['R2']:>12.4f} "
              f"{fits['m_log23n']['R2']:>12.4f} "
              f"{fits['m_sqrtlogn']['R2']:>12.4f}")
    print("=" * 90)

    # ---- Generate figures/operation_ratios.png ----
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for idx, gtype in enumerate(['sparse', 'grid', 'worst_case']):
        ax = axes[idx]
        gtype_label = {'sparse': 'Sparse', 'grid': 'Grid', 'worst_case': 'Worst-Case'}[gtype]

        for algo, color, marker, label in [
            ('dijkstra_fibonacci', '#1f77b4', 'o', 'Dijkstra+Fib'),
            ('dijkstra_binary', '#2ca02c', 's', 'Dijkstra+Bin'),
            ('duan_stoc2025', '#ff7f0e', '^', 'Duan 2025'),
            ('dams_sssp', '#d62728', 'D', 'DAMS-SSSP'),
        ]:
            key = f"{algo}__{gtype}"
            if key not in analysis:
                continue
            val = analysis[key]
            ns = val['n_values']
            ratios = val['ratio_to_mnlogn']
            ax.plot(ns, ratios, color=color, marker=marker, label=label)

        ax.set_xlabel('n')
        ax.set_ylabel('Ops / (m + n log n)')
        ax.set_title(f'{gtype_label} Graphs')
        ax.set_xscale('log')
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    fig.suptitle('Operation Count Ratios Relative to O(m + n log n)', fontsize=14, y=1.02)
    fig.tight_layout()
    fig.savefig('figures/operation_ratios.png')
    fig.savefig('figures/operation_ratios.pdf')
    plt.close(fig)
    print("\nSaved figures/operation_ratios.png/.pdf")

    # ---- Generate R² bar chart ----
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for idx, gtype in enumerate(['sparse', 'grid', 'worst_case']):
        ax = axes[idx]
        gtype_label = {'sparse': 'Sparse', 'grid': 'Grid', 'worst_case': 'Worst-Case'}[gtype]

        algos_present = []
        r2_vals = {fn: [] for fn in ['m_linear', 'm_plus_nlogn', 'm_log23n', 'm_sqrtlogn']}

        for algo in ['dijkstra_binary', 'duan_stoc2025', 'dams_sssp']:
            key = f"{algo}__{gtype}"
            if key not in analysis:
                continue
            short = {'dijkstra_binary': 'Bin', 'duan_stoc2025': 'Duan', 'dams_sssp': 'DAMS'}[algo]
            algos_present.append(short)
            for fn in r2_vals:
                r2_vals[fn].append(analysis[key]['fits'][fn]['R2'])

        x = np.arange(len(algos_present))
        width = 0.18
        colors = ['#aec7e8', '#1f77b4', '#ff7f0e', '#d62728']
        labels_fn = ['c·m', 'c·(m+n lg n)', 'c·m·lg²/³ n', 'c·m·√lg n']

        for i, (fn, col, lab) in enumerate(zip(r2_vals, colors, labels_fn)):
            ax.bar(x + i * width, r2_vals[fn], width, color=col, label=lab)

        ax.set_xticks(x + 1.5 * width)
        ax.set_xticklabels(algos_present)
        ax.set_ylabel('R²')
        ax.set_title(f'{gtype_label}')
        ax.set_ylim(0.9, 1.005)
        ax.legend(fontsize=7, loc='lower right')
        ax.grid(True, alpha=0.3, axis='y')

    fig.suptitle('Regression R² for Candidate Complexity Functions', fontsize=14, y=1.02)
    fig.tight_layout()
    fig.savefig('figures/r2_comparison.png')
    fig.savefig('figures/r2_comparison.pdf')
    plt.close(fig)
    print("Saved figures/r2_comparison.png/.pdf")


if __name__ == '__main__':
    main()
