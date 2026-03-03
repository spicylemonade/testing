#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "results" / "experiments" / "raw" / "run_manifest.jsonl"
SENSITIVITY = ROOT / "results" / "experiments" / "sensitivity_dt_softening.json"
BASELINE_METRICS = ROOT / "results" / "baseline" / "metrics.json"
OUT_JSON = ROOT / "results" / "experiments" / "statistics.json"
OUT_MD = ROOT / "results" / "experiments" / "statistics.md"


def bootstrap_median_ci(values: list[float], n_boot: int = 5000, seed: int = 42) -> tuple[float, float, float]:
    arr = np.asarray(values, dtype=np.float64)
    med = float(np.median(arr))
    if len(arr) == 1:
        return med, med, med
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(arr), size=(n_boot, len(arr)))
    sample_medians = np.median(arr[idx], axis=1)
    low = float(np.percentile(sample_medians, 2.5))
    high = float(np.percentile(sample_medians, 97.5))
    return med, low, high


def load_manifest() -> list[dict]:
    rows = []
    for line in MANIFEST.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def orbit_error_pct(run_file: Path) -> float:
    payload = json.loads(run_file.read_text())
    frames = payload["trajectory"]["frames"]
    first = np.array(frames[0]["positions"], dtype=np.float64)
    r0 = float(np.mean(np.linalg.norm(first, axis=1)))
    errs = []
    for frame in frames:
        pos = np.array(frame["positions"], dtype=np.float64)
        radii = np.linalg.norm(pos, axis=1)
        rel = (radii - r0) / max(1e-15, r0)
        errs.extend((100.0 * rel).tolist())
    return float(np.sqrt(np.mean(np.square(errs))))


def summarize_cis(rows: list[dict], metric_keys: list[str]) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["method"], row["scenario"])].append(row)

    summary = []
    for (method, scenario), group_rows in sorted(grouped.items()):
        for metric in metric_keys:
            values = [float(r["metrics"][metric]) for r in group_rows]
            med, lo, hi = bootstrap_median_ci(values)
            summary.append(
                {
                    "method": method,
                    "scenario": scenario,
                    "metric": metric,
                    "n": len(values),
                    "median": med,
                    "ci95_low": lo,
                    "ci95_high": hi,
                }
            )
    return summary


def effect_sizes_vs_baseline(rows: list[dict], metric_keys: list[str]) -> list[dict]:
    by_triplet = {(r["method"], r["scenario"], int(r["seed"])): r for r in rows}
    scenarios = sorted(set(r["scenario"] for r in rows))
    methods = sorted(set(r["method"] for r in rows) - {"baseline"})
    seeds = sorted(set(int(r["seed"]) for r in rows))

    effects = []
    for scenario in scenarios:
        for method in methods:
            for metric in metric_keys:
                diffs = []
                pct_changes = []
                wins = 0
                total = 0
                for seed in seeds:
                    base = by_triplet.get(("baseline", scenario, seed))
                    alt = by_triplet.get((method, scenario, seed))
                    if not base or not alt:
                        continue
                    b = float(base["metrics"][metric])
                    a = float(alt["metrics"][metric])
                    diffs.append(a - b)
                    pct_changes.append((a - b) / max(1e-15, abs(b)) * 100.0)
                    if a < b:
                        wins += 1
                    total += 1

                if not diffs:
                    continue
                med_diff, lo_diff, hi_diff = bootstrap_median_ci(diffs)
                med_pct, lo_pct, hi_pct = bootstrap_median_ci(pct_changes)
                effects.append(
                    {
                        "scenario": scenario,
                        "method": method,
                        "metric": metric,
                        "n_pairs": total,
                        "median_difference": med_diff,
                        "ci95_difference": [lo_diff, hi_diff],
                        "median_percent_change": med_pct,
                        "ci95_percent_change": [lo_pct, hi_pct],
                        "win_rate_vs_baseline": wins / max(1, total),
                    }
                )
    return effects


def sensitivity_summary() -> dict:
    payload = json.loads(SENSITIVITY.read_text())
    rows = payload["rows"]

    by_dt = defaultdict(list)
    by_soft = defaultdict(list)
    by_grid = defaultdict(list)
    for r in rows:
        by_dt[float(r["dt"])].append(float(r["max_energy_drift_pct"]))
        by_soft[float(r["softening"])].append(float(r["max_energy_drift_pct"]))
        by_grid[(float(r["dt"]), float(r["softening"]))].append(float(r["max_energy_drift_pct"]))

    dt_table = []
    for dt in sorted(by_dt):
        med, lo, hi = bootstrap_median_ci(by_dt[dt])
        dt_table.append({"dt": dt, "median_energy_drift_pct": med, "ci95": [lo, hi]})

    soft_table = []
    for soft in sorted(by_soft):
        med, lo, hi = bootstrap_median_ci(by_soft[soft])
        soft_table.append({"softening": soft, "median_energy_drift_pct": med, "ci95": [lo, hi]})

    grid_table = []
    for key in sorted(by_grid):
        med, lo, hi = bootstrap_median_ci(by_grid[key])
        grid_table.append(
            {
                "dt": key[0],
                "softening": key[1],
                "median_energy_drift_pct": med,
                "ci95": [lo, hi],
            }
        )

    return {
        "dt_sensitivity": dt_table,
        "softening_sensitivity": soft_table,
        "grid": grid_table,
    }


def threshold_pass_fail(rows: list[dict]) -> list[dict]:
    # Thresholds from item_002.
    thresholds = {
        "energy_drift_pct": 0.10,
        "angular_drift_pct": 0.01,
        "orbit_error_pct": 1.0,
        "runtime_per_step_ms": 1.0,
    }

    by_method_scenario = defaultdict(list)
    for r in rows:
        by_method_scenario[(r["method"], r["scenario"])].append(r)

    two_body_sym = by_method_scenario[("symplectic", "two_body")]
    energy_vals = [float(r["metrics"]["max_energy_drift_pct"]) for r in two_body_sym]
    angular_vals = [float(r["metrics"]["max_angular_momentum_drift_pct"]) for r in two_body_sym]

    energy_med, energy_lo, energy_hi = bootstrap_median_ci(energy_vals)
    angular_med, angular_lo, angular_hi = bootstrap_median_ci(angular_vals)

    orbit_vals = []
    for r in two_body_sym:
        orbit_vals.append(orbit_error_pct(ROOT / r["artifact_path"]))
    orbit_med, orbit_lo, orbit_hi = bootstrap_median_ci(orbit_vals)

    baseline_metrics = json.loads(BASELINE_METRICS.read_text())
    n256_row = next(item for item in baseline_metrics["results"] if int(item["n"]) == 256)
    runtime_val = float(n256_row["mean_step_time_ms"])

    checks = [
        {
            "metric": "energy_drift_pct",
            "threshold": thresholds["energy_drift_pct"],
            "estimate": energy_med,
            "ci95": [energy_lo, energy_hi],
            "status": "PASS" if energy_hi <= thresholds["energy_drift_pct"] else "FAIL",
            "source": "symplectic two_body (seeded runs)",
        },
        {
            "metric": "angular_drift_pct",
            "threshold": thresholds["angular_drift_pct"],
            "estimate": angular_med,
            "ci95": [angular_lo, angular_hi],
            "status": "PASS" if angular_hi <= thresholds["angular_drift_pct"] else "FAIL",
            "source": "symplectic two_body (seeded runs)",
        },
        {
            "metric": "orbit_error_pct",
            "threshold": thresholds["orbit_error_pct"],
            "estimate": orbit_med,
            "ci95": [orbit_lo, orbit_hi],
            "status": "PASS" if orbit_hi <= thresholds["orbit_error_pct"] else "FAIL",
            "source": "symplectic two_body derived orbit-radius RMS",
        },
        {
            "metric": "runtime_per_step_ms",
            "threshold": thresholds["runtime_per_step_ms"],
            "estimate": runtime_val,
            "ci95": [runtime_val, runtime_val],
            "status": "PASS" if runtime_val <= thresholds["runtime_per_step_ms"] else "FAIL",
            "source": "baseline N=256 from results/baseline/metrics.json",
        },
    ]
    return checks


def build_markdown(stats: dict) -> str:
    lines = [
        "# Statistical Analysis and Robustness Checks",
        "",
        f"Generated at: {stats['generated_at']}",
        f"Commit: {stats['commit']}",
        "",
        "## Confidence intervals (median, bootstrap 95%)",
        "",
        "| Method | Scenario | Metric | n | Median | 95% CI |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]
    for row in stats["ci_summary"]:
        lines.append(
            f"| {row['method']} | {row['scenario']} | {row['metric']} | {row['n']} | {row['median']:.6f} | [{row['ci95_low']:.6f}, {row['ci95_high']:.6f}] |"
        )

    lines += [
        "",
        "## Effect sizes vs baseline",
        "",
        "| Scenario | Method | Metric | Median diff | 95% CI diff | Median % change | Win rate |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in stats["effect_sizes_vs_baseline"]:
        lo, hi = row["ci95_difference"]
        plo, phi = row["ci95_percent_change"]
        lines.append(
            f"| {row['scenario']} | {row['method']} | {row['metric']} | {row['median_difference']:.6f} | [{lo:.6f}, {hi:.6f}] | {row['median_percent_change']:.2f}% [{plo:.2f}, {phi:.2f}] | {100.0*row['win_rate_vs_baseline']:.1f}% |"
        )

    lines += [
        "",
        "## dt sensitivity (baseline random-N64)",
        "",
        "| dt | Median energy drift % | 95% CI |",
        "| ---: | ---: | ---: |",
    ]
    for row in stats["sensitivity"]["dt_sensitivity"]:
        lo, hi = row["ci95"]
        lines.append(f"| {row['dt']:.6f} | {row['median_energy_drift_pct']:.6f} | [{lo:.6f}, {hi:.6f}] |")

    lines += [
        "",
        "## softening sensitivity (baseline random-N64)",
        "",
        "| softening | Median energy drift % | 95% CI |",
        "| ---: | ---: | ---: |",
    ]
    for row in stats["sensitivity"]["softening_sensitivity"]:
        lo, hi = row["ci95"]
        lines.append(f"| {row['softening']:.6f} | {row['median_energy_drift_pct']:.6f} | [{lo:.6f}, {hi:.6f}] |")

    lines += [
        "",
        "## Threshold pass/fail against item_002",
        "",
        "| Metric | Threshold | Estimate | 95% CI | Status | Source |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in stats["threshold_checks"]:
        lo, hi = row["ci95"]
        lines.append(
            f"| {row['metric']} | {row['threshold']:.6f} | {row['estimate']:.6f} | [{lo:.6f}, {hi:.6f}] | {row['status']} | {row['source']} |"
        )

    overall = "PASS" if all(r["status"] == "PASS" for r in stats["threshold_checks"]) else "FAIL"
    lines += [
        "",
        f"Overall threshold verdict: **{overall}**.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    rows = load_manifest()
    metric_keys = [
        "max_energy_drift_pct",
        "max_angular_momentum_drift_pct",
        "center_of_mass_drift",
        "runtime_per_step_ms",
        "throughput_steps_per_s",
    ]

    stats = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commit": rows[0]["commit_hash"] if rows else "unknown",
        "ci_summary": summarize_cis(rows, metric_keys),
        "effect_sizes_vs_baseline": effect_sizes_vs_baseline(
            rows,
            ["max_energy_drift_pct", "max_angular_momentum_drift_pct", "runtime_per_step_ms"],
        ),
        "sensitivity": sensitivity_summary(),
        "threshold_checks": threshold_pass_fail(rows),
    }

    OUT_JSON.write_text(json.dumps(stats, indent=2) + "\n")
    OUT_MD.write_text(build_markdown(stats))
    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
