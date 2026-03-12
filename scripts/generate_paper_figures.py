#!/usr/bin/env python3
"""Prepare figure data files for the prime-separator manuscript."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results' / 'paper'


def load(path: str | Path):
    return json.loads(Path(path).read_text())


def write_tsv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as fh:
        writer = csv.writer(fh, delimiter='\t')
        writer.writerow(header)
        writer.writerows(rows)


def downsample_pairs(xs: list[int], ys: list[float], max_points: int = 3500) -> list[tuple[int, float]]:
    if len(xs) <= max_points:
        return list(zip(xs, ys))
    out = []
    for k in range(max_points):
        idx = round(k * (len(xs) - 1) / (max_points - 1))
        out.append((xs[idx], ys[idx]))
    return out


def quantile(sorted_vals: list[int], q: float) -> float:
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])
    pos = q * (len(sorted_vals) - 1)
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return float(sorted_vals[lo])
    frac = pos - lo
    return float(sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac)


def log_binned_quantiles(xs: list[int], ys: list[int], bins: int = 60) -> list[tuple[float, float, float, float]]:
    xmin = max(1, min(xs))
    xmax = max(xs)
    edges = sorted({int(round(10 ** (math.log10(xmin) + i * (math.log10(xmax) - math.log10(xmin)) / bins))) for i in range(bins + 1)})
    if edges[-1] < xmax:
        edges.append(xmax)
    out = []
    for left, right in zip(edges[:-1], edges[1:]):
        block = [y for x, y in zip(xs, ys) if left <= x < right]
        if not block:
            continue
        block.sort()
        center = math.sqrt(left * max(left + 1, right))
        out.append((center, quantile(block, 0.1), quantile(block, 0.5), quantile(block, 0.9)))
    return out


def prepare_growth() -> None:
    row = load(ROOT / 'results/experiments/run_1000000/row_terms.json')
    col = load(ROOT / 'results/experiments/run_1000000/column_terms.json')
    xs = list(range(1, len(row) + 1))
    row_ratio = [row[i - 1] / i for i in xs]
    col_ratio = [col[i - 1] / i for i in xs]
    offset = [col[i] - row[i] for i in range(len(row))]
    growth_rows = [[x, rr, cr, off] for (x, rr), (_, cr), off in zip(downsample_pairs(xs, row_ratio), downsample_pairs(xs, col_ratio), [offset[round(k * (len(offset) - 1) / (3500 - 1))] for k in range(3500)] if len(offset) > 3500 else offset)]
    write_tsv(OUT / 'growth.tsv', ['n', 'row_ratio', 'col_ratio', 'offset'], growth_rows)
    offset_rows = [[c, q10, q50, q90] for c, q10, q50, q90 in log_binned_quantiles(xs, offset)]
    write_tsv(OUT / 'offset_quantiles.tsv', ['n', 'q10', 'q50', 'q90'], offset_rows)


def step_series(contract: dict) -> list[list[int]]:
    rows = [[0, 0]]
    current = 0
    for item in contract['gap_locations']:
        step = int(item['step'])
        gap = int(item['gap'])
        rows.append([step, current])
        rows.append([step, gap])
        current = gap
    return rows


def prepare_record_trajectories() -> None:
    files = {
        'baseline': ROOT / 'results/experiments/run_1000000/contract.json',
        'row_immediate': ROOT / 'results/experiments/row_immediate_1000000/contract.json',
        'column_immediate': ROOT / 'results/experiments/column_immediate_1000000/contract.json',
    }
    for name, path in files.items():
        contract = load(path)
        write_tsv(OUT / f'{name}_record_trajectory.tsv', ['step', 'record_gap'], step_series(contract))
        points = [[int(item['step']), int(item['gap'])] for item in contract['gap_locations']]
        write_tsv(OUT / f'{name}_record_points.tsv', ['step', 'gap'], points)


def prepare_witness_metrics() -> None:
    mapping = {
        'baseline': ROOT / 'results/experiments/run_1000000/record_gap_summary.json',
        'column_immediate': ROOT / 'results/experiments/column_immediate_1000000/record_gap_summary.json',
    }
    for name, path in mapping.items():
        gaps = [g for g in load(path)['gaps'] if int(g['gap']) >= 13]
        rows = []
        for g in gaps:
            rows.append([
                int(g['gap']),
                int(g['step']),
                float(g['singleton_share']),
                float(g['min_factor_le_10_share']),
                float(g['min_factor_gt_100_share']),
                int(g['skipped_prime_count']),
            ])
        write_tsv(
            OUT / f'{name}_witness_metrics.tsv',
            ['gap', 'step', 'singleton_share', 'tiny_share', 'balanced_share', 'skipped_primes'],
            rows,
        )


def prepare_hypergraph_tables() -> None:
    baseline = load(ROOT / 'results/analysis/full_witness_hypergraphs_gap21_25_28_30.json')['gaps']
    variant = load(ROOT / 'results/experiments/column_immediate_1000000/full_witness_gap31.json')['gaps']
    for gap in baseline + variant:
        g = int(gap['gap'])
        rows = []
        for skipped in gap['skipped']:
            value = int(skipped['value'])
            for pair in skipped['all_pairs']:
                rows.append([value, int(pair['row_term']), int(pair['column_term'])])
        write_tsv(OUT / f'hypergraph_gap{g}.tsv', ['value', 'row_factor', 'column_factor'], rows)


def prepare_gap_distribution() -> None:
    row = load(ROOT / 'results/experiments/run_1000000/row_terms.json')
    diffs = [row[i] - row[i - 1] for i in range(1, len(row))]
    windows = [
        ('le1e3', diffs[:999]),
        ('1e3to1e4', diffs[999:9999]),
        ('1e4to1e5', diffs[9999:99999]),
        ('1e5to1e6', diffs[99999:]),
    ]
    summary_rows = []
    for label, data in windows:
        ordered = sorted(data)
        summary_rows.append([label, min(data), quantile(ordered, 0.25), median(data), quantile(ordered, 0.75), max(data), mean(data)])
    write_tsv(OUT / 'gap_window_summary.tsv', ['window', 'min', 'q1', 'median', 'q3', 'max', 'mean'], summary_rows)

    threshold_rows = []
    for label, data in windows:
        n = len(data)
        for t in range(1, max(diffs) + 1):
            survivor = sum(1 for x in data if x >= t) / n
            threshold_rows.append([label, t, survivor])
    write_tsv(OUT / 'gap_survivor.tsv', ['window', 'threshold', 'survivor'], threshold_rows)


def prepare_summary() -> None:
    row = load(ROOT / 'results/experiments/run_1000000/row_terms.json')
    col = load(ROOT / 'results/experiments/run_1000000/column_terms.json')
    base_contract = load(ROOT / 'results/experiments/run_1000000/contract.json')
    col_contract = load(ROOT / 'results/experiments/column_immediate_1000000/contract.json')
    payload = {
        'baseline': {
            'steps': int(base_contract['steps']),
            'row_last': int(base_contract['row_last']),
            'column_last': int(base_contract['column_last']),
            'largest_record_gap': int(base_contract['largest_record_gap']),
            'record_gap_count': int(base_contract['record_gap_count']),
            'mean_gap_last_window': mean([row[i] - row[i - 1] for i in range(100000, len(row))]),
            'median_gap_last_window': median([row[i] - row[i - 1] for i in range(100000, len(row))]),
            'max_offset': max(c - r for r, c in zip(row, col)),
        },
        'column_immediate': {
            'largest_record_gap': int(col_contract['largest_record_gap']),
            'record_gap_count': int(col_contract['record_gap_count']),
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'figure_summary.json').write_text(json.dumps(payload, indent=2) + '\n')


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    prepare_growth()
    prepare_record_trajectories()
    prepare_witness_metrics()
    prepare_hypergraph_tables()
    prepare_gap_distribution()
    prepare_summary()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
