#!/usr/bin/env python3
"""Run a lightweight Monte Carlo robustness study for the H1 lane."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
import subprocess
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import run_h1_falsifier as falsifier_runner
import run_h1_matrix as matrix_runner


REPO_ROOT = Path(__file__).resolve().parents[1]
LANE_ROOT = REPO_ROOT / "results" / "concept_evolve" / "tree" / "001_packet_scout_handoff_root"
STARTUP_MANIFEST = LANE_ROOT / "results" / "manifests" / "startup_matrix_manifest.json"
FALSIFIER_MANIFEST = LANE_ROOT / "results" / "manifests" / "falsifier_cases.json"
RAW_ROOT = LANE_ROOT / "results" / "raw" / "robustness"
TABLE_PATH = LANE_ROOT / "tables" / "robustness_results.csv"
SUMMARY_PATH = LANE_ROOT / "tables" / "robustness_summary.json"
NGSPICE_BIN = REPO_ROOT / "tools" / "ngspice-local"

DEFAULT_CASES = ["fa_001", "fa_004", "fa_005", "sm_015"]
DEFAULT_DESIGNS = ["champion", "fixed", "nonaware", "source_blind", "time_constant_ranked", "blind_packet_merge", "confidence_gated"]

SCALE_RE = {
    "t": 1e12,
    "g": 1e9,
    "meg": 1e6,
    "k": 1e3,
    "m": 1e-3,
    "u": 1e-6,
    "n": 1e-9,
    "p": 1e-12,
    "f": 1e-15,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_numeric(value: str | float | int) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().lower()
    for suffix, scale in sorted(SCALE_RE.items(), key=lambda item: len(item[0]), reverse=True):
        if text.endswith(suffix):
            return float(text[: -len(suffix)]) * scale
    return float(text)


def to_spice(value: float) -> str:
    return f"{value:.6g}"


def load_case_catalog() -> dict[str, tuple[str, dict]]:
    catalog: dict[str, tuple[str, dict]] = {}
    for case in json.loads(STARTUP_MANIFEST.read_text())["cases"]:
        catalog[case["case_id"]] = ("startup", case)
    for case in json.loads(FALSIFIER_MANIFEST.read_text())["cases"]:
        catalog[case["case_id"]] = ("falsifier", case)
    return catalog


def select_cases(case_ids: str | None) -> list[str]:
    if not case_ids:
        return DEFAULT_CASES
    return [part.strip() for part in case_ids.split(",") if part.strip()]


def select_designs(designs: str | None) -> list[str]:
    if not designs:
        return DEFAULT_DESIGNS
    chosen = [part.strip() for part in designs.split(",") if part.strip()]
    for design in chosen:
        if design not in falsifier_runner.DECKS:
            raise SystemExit(f"unknown design: {design}")
    return chosen


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def vary_case(case: dict, design: str, rng: random.Random) -> tuple[dict, dict]:
    varied = deepcopy(case)
    overrides = dict(varied.get("extra_params", {}))

    r_a = float(varied["r_a_ohm"]) * max(0.6, 1.0 + rng.gauss(0.0, 0.08))
    r_b = float(varied["r_b_ohm"]) * max(0.6, 1.0 + rng.gauss(0.0, 0.08))
    varied["r_a_ohm"] = round(r_a, 6)
    varied["r_b_ohm"] = round(r_b, 6)

    base_c_store = parse_numeric(overrides.get("C_STORE", "10u"))
    overrides["C_STORE"] = to_spice(base_c_store * max(0.5, 1.0 + rng.gauss(0.0, 0.10)))

    base_vstart_dead = parse_numeric(overrides.get("VSTART_DEAD", "5m"))
    overrides["VSTART_DEAD"] = to_spice(clamp(base_vstart_dead * (1.0 + rng.gauss(0.0, 0.12)), 1e-3, 15e-3))

    if design in {"champion", "source_blind", "blind_packet_merge", "confidence_gated"}:
        overrides["SCOUT_R"] = to_spice(parse_numeric(overrides.get("SCOUT_R", "150k")) * max(0.6, 1.0 + rng.gauss(0.0, 0.12)))
        overrides["SCOUT_C"] = to_spice(parse_numeric(overrides.get("SCOUT_C", "5n")) * max(0.6, 1.0 + rng.gauss(0.0, 0.12)))
        overrides["G_SCOUT_CTRL"] = to_spice(parse_numeric(overrides.get("G_SCOUT_CTRL", "40n")) * max(0.5, 1.0 + rng.gauss(0.0, 0.10)))
    if design == "confidence_gated":
        overrides["CONF_EPS"] = to_spice(parse_numeric(overrides.get("CONF_EPS", "1m")) * max(0.6, 1.0 + rng.gauss(0.0, 0.10)))
        overrides["CONF_AMP_FLOOR"] = to_spice(parse_numeric(overrides.get("CONF_AMP_FLOOR", "10m")) * max(0.6, 1.0 + rng.gauss(0.0, 0.10)))
        overrides["CONF_R"] = to_spice(parse_numeric(overrides.get("CONF_R", "100k")) * max(0.6, 1.0 + rng.gauss(0.0, 0.12)))
        overrides["CONF_C"] = to_spice(parse_numeric(overrides.get("CONF_C", "500n")) * max(0.6, 1.0 + rng.gauss(0.0, 0.12)))
        overrides["G_CONF_CTRL"] = to_spice(parse_numeric(overrides.get("G_CONF_CTRL", "8n")) * max(0.5, 1.0 + rng.gauss(0.0, 0.10)))
    if design == "time_constant_ranked":
        overrides["TC_FAST_R"] = to_spice(parse_numeric(overrides.get("TC_FAST_R", "30k")) * max(0.6, 1.0 + rng.gauss(0.0, 0.12)))
        overrides["TC_FAST_C"] = to_spice(parse_numeric(overrides.get("TC_FAST_C", "1.5n")) * max(0.6, 1.0 + rng.gauss(0.0, 0.12)))
        overrides["TC_SLOW_R"] = to_spice(parse_numeric(overrides.get("TC_SLOW_R", "220k")) * max(0.6, 1.0 + rng.gauss(0.0, 0.12)))
        overrides["TC_SLOW_C"] = to_spice(parse_numeric(overrides.get("TC_SLOW_C", "7n")) * max(0.6, 1.0 + rng.gauss(0.0, 0.12)))
        overrides["G_TC_CTRL"] = to_spice(parse_numeric(overrides.get("G_TC_CTRL", "18n")) * max(0.5, 1.0 + rng.gauss(0.0, 0.10)))

    if "RLEAK_ROUTE" in overrides:
        leak = parse_numeric(overrides["RLEAK_ROUTE"])
        overrides["RLEAK_ROUTE"] = to_spice(leak * max(0.4, 1.0 + rng.gauss(0.0, 0.15)))

    for timing_key in ["T_COLLAPSE_A", "T_RECOVER_A", "T_COLLAPSE_B", "T_RECOVER_B"]:
        if timing_key in overrides:
            shift = rng.gauss(0.0, 0.12)
            overrides[timing_key] = to_spice(max(0.0, parse_numeric(overrides[timing_key]) + shift))
    for scale_key in ["COLLAPSE_SCALE_A", "COLLAPSE_SCALE_B"]:
        if scale_key in overrides:
            overrides[scale_key] = to_spice(clamp(parse_numeric(overrides[scale_key]) + rng.gauss(0.0, 0.04), 0.0, 1.0))

    varied["extra_params"] = overrides
    sampled = {
        "r_a_ohm": varied["r_a_ohm"],
        "r_b_ohm": varied["r_b_ohm"],
        "extra_params": overrides,
    }
    return varied, sampled


def run_sample(suite: str, design: str, case: dict, sample_idx: int, seed: int) -> dict:
    render = matrix_runner.render_netlist if suite == "startup" else falsifier_runner.render_netlist
    parse = matrix_runner.parse_log if suite == "startup" else falsifier_runner.parse_log
    case_dir = RAW_ROOT / suite / case["case_id"] / design / f"sample_{sample_idx:03d}"
    case_dir.mkdir(parents=True, exist_ok=True)
    rendered_path = case_dir / f"{design}_{case['case_id']}_s{sample_idx:03d}.cir"
    log_path = case_dir / f"{design}_{case['case_id']}_s{sample_idx:03d}.log"
    json_path = case_dir / f"{design}_{case['case_id']}_s{sample_idx:03d}.json"
    rendered_path.write_text(render(design, case))
    proc = subprocess.run(
        [str(NGSPICE_BIN), "-b", "-o", str(log_path), str(rendered_path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    parsed = parse(log_path.read_text())
    row = {
        "suite": suite,
        "case_id": case["case_id"],
        "design": design,
        "sample_idx": sample_idx,
        "seed": seed,
        "status": "ok" if proc.returncode == 0 else "blocked",
        "return_code": proc.returncode,
        "startup_ok": parsed.get("startup_ok"),
        "t_handoff_s": parsed.get("t_handoff_s"),
        "t_handoff_fall_s": parsed.get("t_handoff_fall_s"),
        "t_handoff_rise2_s": parsed.get("t_handoff_rise2_s"),
        "e_backdrive_j": parsed.get("e_backdrive_j"),
        "e_ctrl_j": parsed.get("e_ctrl_j"),
        "rendered_netlist": str(rendered_path.relative_to(REPO_ROOT)),
        "log_path": str(log_path.relative_to(REPO_ROOT)),
        "sampled_r_a_ohm": case["r_a_ohm"],
        "sampled_r_b_ohm": case["r_b_ohm"],
        "sampled_overrides": json.dumps(case.get("extra_params", {}), sort_keys=True),
    }
    json_path.write_text(json.dumps(row, indent=2) + "\n")
    return row


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total == 0:
        return (0.0, 0.0)
    p = successes / total
    denom = 1 + z**2 / total
    center = (p + z**2 / (2 * total)) / denom
    margin = z * math.sqrt((p * (1 - p) + z**2 / (4 * total)) / total) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))


def write_table(rows: list[dict]) -> None:
    fieldnames = [
        "suite",
        "case_id",
        "design",
        "sample_idx",
        "seed",
        "status",
        "return_code",
        "startup_ok",
        "t_handoff_s",
        "t_handoff_fall_s",
        "t_handoff_rise2_s",
        "e_backdrive_j",
        "e_ctrl_j",
        "sampled_r_a_ohm",
        "sampled_r_b_ohm",
        "sampled_overrides",
        "rendered_netlist",
        "log_path",
    ]
    with TABLE_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary(rows: list[dict], samples: int) -> None:
    summary: dict[str, dict[str, dict[str, object]]] = {}
    for case_id in sorted({row["case_id"] for row in rows}):
        summary[case_id] = {}
        for design in sorted({row["design"] for row in rows if row["case_id"] == case_id}):
            subset = [row for row in rows if row["case_id"] == case_id and row["design"] == design]
            successes = sum(1 for row in subset if (row.get("startup_ok") or 0.0) >= 0.5)
            ci_low, ci_high = wilson_interval(successes, len(subset))
            successful = [row for row in subset if (row.get("startup_ok") or 0.0) >= 0.5 and row.get("t_handoff_s") is not None]
            summary[case_id][design] = {
                "samples": len(subset),
                "startup_successes": successes,
                "startup_success_rate": successes / len(subset) if subset else None,
                "startup_success_ci95": [ci_low, ci_high],
                "median_t_handoff_s_success": statistics.median(
                    [row["t_handoff_s"] for row in successful]
                )
                if successful
                else None,
                "median_e_backdrive_j": statistics.median(
                    [row["e_backdrive_j"] for row in subset if row.get("e_backdrive_j") is not None]
                )
                if any(row.get("e_backdrive_j") is not None for row in subset)
                else None,
                "median_e_ctrl_j": statistics.median(
                    [row["e_ctrl_j"] for row in subset if row.get("e_ctrl_j") is not None]
                )
                if any(row.get("e_ctrl_j") is not None for row in subset)
                else None,
            }
    payload = {
        "updated_at": utc_now(),
        "samples_per_design_case": samples,
        "results_path": str(TABLE_PATH.relative_to(REPO_ROOT)),
        "summary": summary,
    }
    SUMMARY_PATH.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases")
    parser.add_argument("--designs")
    parser.add_argument("--samples", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260312)
    args = parser.parse_args()

    catalog = load_case_catalog()
    case_ids = select_cases(args.cases)
    designs = select_designs(args.designs)
    rows: list[dict] = []

    for case_offset, case_id in enumerate(case_ids):
        if case_id not in catalog:
            raise SystemExit(f"unknown robustness case: {case_id}")
        suite, base_case = catalog[case_id]
        for design_offset, design in enumerate(designs):
            for sample_idx in range(args.samples):
                seed = args.seed + case_offset * 10000 + design_offset * 1000 + sample_idx
                rng = random.Random(seed)
                varied_case, _sampled = vary_case(base_case, design, rng)
                rows.append(run_sample(suite, design, varied_case, sample_idx, seed))

    write_table(rows)
    write_summary(rows, args.samples)
    print(
        json.dumps(
            {
                "rows": len(rows),
                "cases": case_ids,
                "designs": designs,
                "table_path": str(TABLE_PATH.relative_to(REPO_ROOT)),
                "summary_path": str(SUMMARY_PATH.relative_to(REPO_ROOT)),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
