#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / 'figures'
RESULTS = ROOT / 'results'

PALETTE = {
    'navy': '#1f3b5c',
    'blue': '#2d6a9f',
    'sky': '#6baed6',
    'teal': '#2a9d8f',
    'green': '#4c956c',
    'gold': '#e9c46a',
    'orange': '#f4a261',
    'vermilion': '#d95d39',
    'crimson': '#b23a48',
    'slate': '#5c677d',
    'ink': '#22223b',
    'fog': '#edf2f4',
    'line': '#d0d7de',
    'white': '#ffffff',
}

plt.rcParams.update({
    'figure.facecolor': PALETTE['white'],
    'axes.facecolor': PALETTE['white'],
    'axes.edgecolor': PALETTE['line'],
    'axes.labelcolor': PALETTE['ink'],
    'axes.titleweight': 'bold',
    'axes.titlesize': 15,
    'axes.labelsize': 11,
    'font.family': 'DejaVu Serif',
    'font.size': 10,
    'xtick.color': PALETTE['ink'],
    'ytick.color': PALETTE['ink'],
    'grid.color': '#d9e2ec',
    'grid.linewidth': 0.8,
    'legend.frameon': False,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.08,
})


def load_json(path: Path):
    with path.open() as fh:
        return json.load(fh)


def save(fig: plt.Figure, stem: str):
    fig.savefig(FIG_DIR / f'{stem}.pdf')
    fig.savefig(FIG_DIR / f'{stem}.png', dpi=600)
    plt.close(fig)


def route_counts():
    idx = load_json(RESULTS / 'concept_evolve' / 'tree' / 'index.json')
    counts = {'H1': 0, 'H2': 0, 'H3': 0}
    for row in idx:
        counts[row['route']] += 1
    return counts


def bridge_status_counts():
    rows = load_json(RESULTS / 'concept_evolve' / 'bridge_candidates.json')
    counts = {'promote': 0, 'hold': 0, 'retire': 0}
    for row in rows:
        counts[row['promotion_decision']] += 1
    return counts


def artifact_presence():
    h1_artifacts = [
        'results/h1/frontier_parents.jsonl',
        'results/h1/extension_cases.jsonl',
        'results/h1/failure_witnesses.jsonl',
        'results/h1/obstruction_cores.jsonl',
        'results/h1/transfer_records.jsonl',
        'results/h1/atlas_summary.md',
        'results/h1/witness_safety_audit.md',
    ]
    infra = [
        'orbit-distinct 42->43 enumerator',
        'independent 44-vertex witness verifier',
        '45-vertex certificate checker',
        'frozen benchmark manifest',
        'solved certificate replay ledger',
    ]
    h1_exists = [int((ROOT / p).exists()) for p in h1_artifacts]
    infra_exists = [0 for _ in infra]
    return h1_artifacts, h1_exists, infra, infra_exists


def exact_counts():
    route = route_counts()
    bridge = bridge_status_counts()
    rubric = load_json(ROOT / 'research_rubric.json')
    lit = load_json(RESULTS / 'literature' / 'literature_snapshot.json')['ramsey_specific_review']
    sources_count = sum(1 for line in (ROOT / 'sources.bib').read_text().splitlines() if line.startswith('@'))
    h1_artifacts, h1_exists, infra, infra_exists = artifact_presence()
    rungs = [
        h1_exists[0:3],
        h1_exists[3:5],
        [h1_exists[5]],
        [h1_exists[6]],
    ]
    rung_complete = [int(all(group)) for group in rungs]
    return {
        'route': route,
        'bridge': bridge,
        'rubric_completed': rubric['summary']['completed'],
        'rubric_total': rubric['summary']['total_items'],
        'known_papers': 106,
        'sources_count': sources_count,
        'ramsey_papers': len(lit['papers']),
        'code_artifacts': len(lit['code_artifacts']),
        'survey_sources': len(lit['survey_sources']),
        'h1_artifacts_present': sum(h1_exists),
        'h1_artifacts_total': len(h1_exists),
        'infra_present': sum(infra_exists),
        'infra_total': len(infra_exists),
        'rungs_complete': sum(rung_complete),
        'rungs_total': len(rung_complete),
        'benchmark_rows_present': 0,
        'benchmark_rows_total': 8,
        'concept_floor_present': sum(route.values()),
        'concept_floor_total': 10,
        'promoted_h1_bridges': 5,
        'promoted_h1_bridge_total': 5,
    }


def figure_pipeline():
    fig, ax = plt.subplots(figsize=(12.8, 4.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis('off')

    boxes = [
        (0.4, 2.2, 2.0, 1.25, PALETTE['navy'], 'Frontier\nparents', 'Exoo / Ge / Lehavi packet'),
        (2.75, 2.2, 2.0, 1.25, PALETTE['blue'], 'Orbit-distinct\nextensions', '42 -> 43 cases'),
        (5.1, 2.2, 2.0, 1.25, PALETTE['sky'], 'Failure\nwitnesses', 'Monochromatic K5 forcing sets'),
        (7.45, 2.2, 2.0, 1.25, PALETTE['teal'], 'Canonical\ncores', 'Minimal obstruction quotient'),
        (9.8, 2.2, 1.8, 1.25, PALETTE['green'], 'Transfer +\nsafety audit', 'LOPO + witness oracle'),
    ]

    for x, y, w, h, color, title, subtitle in boxes:
        patch = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.18',
                               linewidth=1.5, edgecolor=color, facecolor=PALETTE['fog'])
        ax.add_patch(patch)
        ax.text(x + 0.12, y + 0.82, title, fontsize=12, fontweight='bold', color=color, va='center')
        ax.text(x + 0.12, y + 0.32, subtitle, fontsize=9.4, color=PALETTE['ink'], va='center')

    for i in range(len(boxes) - 1):
        x0 = boxes[i][0] + boxes[i][2]
        x1 = boxes[i + 1][0]
        arrow = FancyArrowPatch((x0 + 0.12, 2.82), (x1 - 0.12, 2.82), arrowstyle='-|>',
                                mutation_scale=14, linewidth=1.8, color=PALETTE['slate'])
        ax.add_patch(arrow)

    ax.text(0.45, 4.45, 'H1 obstruction-atlas pipeline specified by the repository',
            fontsize=15, fontweight='bold', color=PALETTE['ink'])
    ax.text(0.45, 4.05,
            'The pipeline is structurally complete as a specification, but none of the `results/h1/*` artifacts has been materialized.',
            fontsize=10.2, color=PALETTE['slate'])

    threshold_box = FancyBboxPatch((0.45, 0.35), 11.1, 1.15, boxstyle='round,pad=0.03,rounding_size=0.16',
                                   linewidth=1.2, edgecolor=PALETTE['gold'], facecolor='#fffaf0')
    ax.add_patch(threshold_box)
    ax.text(0.7, 1.2, 'Acceptance thresholds encoded in the route sheet and acceptance contract',
            fontsize=10.7, fontweight='bold', color=PALETTE['ink'])
    ax.text(0.7, 0.78,
            'top-25 cores cover >=30% of failed extensions | held-out transfer >=50% of training-side coverage | zero witness kills | no family >50% support | canonical compression >=2x',
            fontsize=9.2, color=PALETTE['ink'])

    save(fig, 'h1_pipeline')


def figure_prior_art_surface():
    rows = [
        'Exoo 1989',
        'Ge et al. 2022',
        'Lehavi 2024',
        'McKay-Radziszowski 1992',
        'Angeltveit-McKay 2018',
        'Angeltveit-McKay 2024',
        'Gauthier 2025',
        'Gauthier-Brown 2024',
        'Narvaez-Song-Zhang 2024',
        'This manuscript',
    ]
    cols = [
        'Constructive\nwitness line',
        'OVE /\nchecking',
        'Upper-bound\ndecomposition',
        'Formal proof /\ncertificate',
        'Cross-family\nobstruction atlas',
        'No-go /\nclaim grammar',
    ]
    data = np.array([
        [1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 1],
    ])

    fig, ax = plt.subplots(figsize=(11.2, 6.8))
    cmap = ListedColormap([PALETTE['fog'], PALETTE['blue']])
    ax.imshow(data, cmap=cmap, vmin=0, vmax=1, aspect='auto')
    ax.set_xticks(np.arange(len(cols)), labels=cols)
    ax.set_yticks(np.arange(len(rows)), labels=rows)
    ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)
    plt.setp(ax.get_xticklabels(), rotation=0, ha='center')

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            ax.text(j, i, '●' if data[i, j] else '', ha='center', va='center', color=PALETTE['white'], fontsize=12)

    for edge in ['top', 'bottom', 'left', 'right']:
        ax.spines[edge].set_visible(False)
    ax.set_xticks(np.arange(-.5, data.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-.5, data.shape[0], 1), minor=True)
    ax.grid(which='minor', color=PALETTE['white'], linestyle='-', linewidth=2)
    ax.tick_params(which='minor', bottom=False, left=False)
    ax.set_title('Prior-art surface map used to keep the manuscript inside a real novelty gap')
    ax.text(-0.48, -1.1,
            'A filled cell marks the dominant contribution surface of a prior line. The current manuscript occupies only the obstruction-atlas / no-go-governance corner.',
            fontsize=9.2, color=PALETTE['slate'])

    save(fig, 'prior_art_surface')


def figure_experiment_ladder():
    fig, ax = plt.subplots(figsize=(12.5, 5.3))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    y = 2.7
    rung_specs = [
        ('Rung 0', 'Frontier reconstruction', 'frontier_parents.jsonl\nextension_cases.jsonl\nfailure_witnesses.jsonl', PALETTE['navy']),
        ('Rung 1', 'Atlas pass', 'obstruction_cores.jsonl\natlas_summary.md', PALETTE['blue']),
        ('Rung 2', 'Held-out transfer', 'transfer_records.jsonl', PALETTE['teal']),
        ('Rung 3', 'Witness safety', 'witness_safety_audit.md', PALETTE['green']),
    ]
    x_positions = [0.6, 3.45, 6.3, 9.15]
    widths = [2.3, 2.3, 2.3, 2.3]
    for (label, title, artifact, color), x, w in zip(rung_specs, x_positions, widths):
        patch = FancyBboxPatch((x, y), w, 1.45, boxstyle='round,pad=0.02,rounding_size=0.14',
                               linewidth=1.4, edgecolor=color, facecolor=PALETTE['fog'])
        ax.add_patch(patch)
        ax.text(x + 0.15, y + 1.05, label, fontsize=10.3, fontweight='bold', color=color)
        ax.text(x + 0.15, y + 0.72, title, fontsize=11.5, fontweight='bold', color=PALETTE['ink'])
        ax.text(x + 0.15, y + 0.22, artifact, fontsize=9.3, color=PALETTE['ink'])

    for x0, x1 in zip([2.9, 5.75, 8.6], [3.35, 6.2, 9.05]):
        ax.add_patch(FancyArrowPatch((x0, y + 0.72), (x1, y + 0.72), arrowstyle='-|>',
                                     mutation_scale=14, linewidth=1.8, color=PALETTE['slate']))

    gate = FancyBboxPatch((0.6, 0.55), 10.85, 1.15, boxstyle='round,pad=0.03,rounding_size=0.14',
                          linewidth=1.3, edgecolor=PALETTE['vermilion'], facecolor='#fff5f2')
    ax.add_patch(gate)
    ax.text(0.85, 1.35, 'Expansion gate', fontsize=10.8, fontweight='bold', color=PALETTE['vermilion'])
    ax.text(0.85, 0.9,
            'No broader compute, no H2 opening, and no structural claim beyond route specification until all four rungs complete cleanly.',
            fontsize=9.3, color=PALETTE['ink'])

    ax.text(0.62, 4.85, 'Exact evaluation ladder frozen in Phase 4', fontsize=15, fontweight='bold', color=PALETTE['ink'])
    ax.text(0.62, 4.45, 'The repository contains the ladder specification but none of the rung artifacts.', fontsize=10.2, color=PALETTE['slate'])

    invalidators = FancyBboxPatch((11.0, 2.15), 1.55, 2.0, boxstyle='round,pad=0.03,rounding_size=0.14',
                                  linewidth=1.2, edgecolor=PALETTE['gold'], facecolor='#fffaf0')
    ax.add_patch(invalidators)
    ax.text(11.17, 3.82, 'Fastest\ninvalidators', fontsize=10.4, fontweight='bold', color=PALETTE['ink'])
    ax.text(11.17, 3.07, 'anti_exoo\n_holdout', fontsize=9.1, color=PALETTE['ink'])
    ax.text(11.17, 2.55, 'witness\n_pressure', fontsize=9.1, color=PALETTE['ink'])
    ax.text(11.17, 2.08, 'rare_core\n_tail', fontsize=9.1, color=PALETTE['ink'])

    save(fig, 'experiment_ladder')


def figure_evidence_heatmap():
    h1_artifacts, h1_exists, infra, infra_exists = artifact_presence()
    rows = [
        'frontier_parents',
        'extension_cases',
        'failure_witnesses',
        'obstruction_cores',
        'transfer_records',
        'atlas_summary',
        'witness_safety_audit',
        'orbit-distinct enumerator',
        'independent 44 verifier',
        '45 certificate checker',
        'benchmark manifest',
        'certificate replay',
    ]
    exists_now = h1_exists + infra_exists
    needed_h1 = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0]
    needed_bound = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    data = np.array(list(zip(exists_now, needed_h1, needed_bound)))

    fig, ax = plt.subplots(figsize=(8.7, 7.8))
    cmap = ListedColormap([PALETTE['fog'], PALETTE['vermilion'], PALETTE['blue']])
    # Encode 0 absent, 1 required, 2 present. First column is present/absent; convert 1->2 there.
    display = data.copy()
    display[:, 0] = np.where(display[:, 0] == 1, 2, 0)
    display[:, 1:] = np.where(display[:, 1:] == 1, 1, 0)
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)
    ax.imshow(display, cmap=cmap, norm=norm, aspect='auto')
    ax.set_xticks(np.arange(3), labels=['Exists now', 'Needed for\nH1 result', 'Needed for\nbound claim'])
    ax.set_yticks(np.arange(len(rows)), labels=rows)
    for i in range(display.shape[0]):
        for j in range(display.shape[1]):
            label = ''
            if j == 0:
                label = 'yes' if display[i, j] == 2 else 'no'
            else:
                label = 'yes' if display[i, j] == 1 else ''
            ax.text(j, i, label, ha='center', va='center', color=PALETTE['ink'], fontsize=9)

    for edge in ['top', 'bottom', 'left', 'right']:
        ax.spines[edge].set_visible(False)
    ax.set_xticks(np.arange(-.5, display.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-.5, display.shape[0], 1), minor=True)
    ax.grid(which='minor', color=PALETTE['white'], linestyle='-', linewidth=2)
    ax.tick_params(which='minor', bottom=False, left=False)
    ax.set_title('Evidence-gap heatmap: every present-cell is currently in the “missing” column')

    save(fig, 'evidence_gap_heatmap')


def figure_concept_status():
    route = route_counts()
    bridge = bridge_status_counts()

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.8), gridspec_kw={'width_ratios': [1.05, 1.0]})

    ax = axes[0]
    keys = list(route.keys())
    vals = [route[k] for k in keys]
    colors = [PALETTE['navy'], PALETTE['blue'], PALETTE['teal']]
    bars = ax.bar(keys, vals, color=colors, width=0.58)
    ax.set_ylim(0, max(vals) + 2)
    ax.set_ylabel('Concept folders')
    ax.set_title('Route coverage in the concept tree')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 0.1, str(v), ha='center', va='bottom', fontsize=11)

    ax = axes[1]
    keys = ['promote', 'hold', 'retire']
    labels = ['Promoted', 'Held', 'Retired']
    vals = [bridge[k] for k in keys]
    colors = [PALETTE['green'], PALETTE['gold'], PALETTE['vermilion']]
    bars = ax.bar(labels, vals, color=colors, width=0.58)
    ax.set_ylim(0, max(vals) + 2)
    ax.set_ylabel('Bridge count')
    ax.set_title('Iterate-era bridge decisions')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 0.1, str(v), ha='center', va='bottom', fontsize=11)

    fig.suptitle('Concept-evolution outputs: broad exploration succeeded, execution did not start', fontsize=15, fontweight='bold', y=1.02)
    save(fig, 'concept_status')


def figure_completeness_dashboard():
    counts = exact_counts()
    categories = [
        'Concept floor',
        'Promoted H1\nbridges',
        'H1 evidence\nartifacts',
        'Exact ladder\nrungs',
        'Benchmark\nrows',
        'Validation\ninfrastructure',
    ]
    present = np.array([
        counts['concept_floor_present'],
        counts['promoted_h1_bridges'],
        counts['h1_artifacts_present'],
        counts['rungs_complete'],
        counts['benchmark_rows_present'],
        counts['infra_present'],
    ], dtype=float)
    target = np.array([
        counts['concept_floor_total'],
        counts['promoted_h1_bridge_total'],
        counts['h1_artifacts_total'],
        counts['rungs_total'],
        counts['benchmark_rows_total'],
        counts['infra_total'],
    ], dtype=float)

    x = np.arange(len(categories))
    fig, ax = plt.subplots(figsize=(11.6, 5.2))
    ax.bar(x, target, color=PALETTE['fog'], edgecolor=PALETTE['line'], width=0.72, label='Target or required count')
    ax.bar(x, present, color=PALETTE['teal'], width=0.5, label='Present count')
    ax.set_xticks(x, categories)
    ax.set_ylabel('Count')
    ax.set_title('Repository completeness dashboard for an H1 execution claim')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.legend(loc='upper right')
    for xi, p, t in zip(x, present, target):
        ax.text(xi, max(p, t) + 0.12, f'{int(p)}/{int(t)}', ha='center', va='bottom', fontsize=10)
    ax.text(-0.42, -1.17,
            'Only the planning-side categories are complete. Every execution-side category remains empty, which is why the manuscript stays in the no-go / route-specification claim class.',
            transform=ax.transData, fontsize=9.2, color=PALETTE['slate'])
    save(fig, 'completeness_dashboard')


def main():
    FIG_DIR.mkdir(exist_ok=True)
    figure_pipeline()
    figure_prior_art_surface()
    figure_experiment_ladder()
    figure_evidence_heatmap()
    figure_concept_status()
    figure_completeness_dashboard()


if __name__ == '__main__':
    main()
