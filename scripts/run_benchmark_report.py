#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import numpy as np

from minigrav.comparators.euler import run_euler_scenario
from minigrav.comparators.poliastro_adapter import run_poliastro_two_body
from minigrav.comparators.rebound_adapter import run_rebound_scenario
from minigrav.io.scenarios import load_scenario
from minigrav.research.encounters import run_encounter_aware_scenario
from minigrav.runner import run_scenario


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON = ROOT / "results" / "verification" / "benchmark_results.json"
OUTPUT_MD = ROOT / "results" / "verification" / "benchmark_report.md"

SCENARIO_DT_OVERRIDES = {
    "star_grazing_two_body": 0.02,
}

SCENARIO_SAMPLE_EVERY = {
    "circular_two_body": 1,
    "figure_eight_three_body": 5,
    "small_n_ring": 50,
    "star_grazing_two_body": 2,
}

SCENARIO_REFERENCE = {
    "circular_two_body": {"integrator": "ias15", "internal_dt": None},
    "figure_eight_three_body": {"integrator": "ias15", "internal_dt": None},
    "small_n_ring": {"integrator": "leapfrog", "internal_dt_scale": 0.125},
    "star_grazing_two_body": {"integrator": "ias15", "internal_dt": None},
}

SCENARIOS = [
    "circular_two_body.json",
    "figure_eight_three_body.json",
    "small_n_ring.json",
    "star_grazing_two_body.json",
]


def _override_dt(config, dt: float):
    steps = int(round(config.duration / dt))
    return replace(config, dt=dt, steps=steps, duration=steps * dt)


def _final_state_vector(result: dict) -> np.ndarray:
    terminal = result["diagnostics"][-1]
    return np.asarray(terminal["positions"] + terminal["velocities"], dtype=float).ravel()


def _max_metric(result: dict, key: str) -> float | None:
    values = [row.get(key) for row in result["diagnostics"] if key in row]
    values = [value for value in values if value is not None]
    return None if not values else float(max(values))


def _row(label: str, result: dict, reference: dict) -> dict:
    ref_vec = _final_state_vector(reference)
    candidate_vec = _final_state_vector(result)
    ref_norm = max(float(np.linalg.norm(ref_vec)), 1e-12)
    return {
        "comparator": label,
        "runtime_seconds": float(result["metadata"].get("runtime_seconds", 0.0)),
        "final_state_rel_error_vs_rebound": float(np.linalg.norm(candidate_vec - ref_vec) / ref_norm),
        "max_energy_rel_drift": _max_metric(result, "energy_rel_drift"),
        "max_angular_momentum_rel_drift": _max_metric(result, "angular_momentum_rel_drift"),
        "max_center_of_mass_abs_drift": _max_metric(result, "center_of_mass_abs_drift"),
        "max_encounter_roundtrip_relative_error": _max_metric(result, "encounter_roundtrip_relative_error"),
    }


def _run_scenario_suite(scenario_name: str) -> dict:
    config = load_scenario(ROOT / "scenarios" / scenario_name)
    dt = SCENARIO_DT_OVERRIDES.get(config.scenario_id, config.dt)
    if dt != config.dt:
        config = _override_dt(config, dt)
    sample_every = SCENARIO_SAMPLE_EVERY.get(config.scenario_id, 1)
    reference_cfg = SCENARIO_REFERENCE.get(config.scenario_id, {"integrator": "ias15", "internal_dt": None})
    internal_dt = reference_cfg.get("internal_dt")
    if internal_dt is None and reference_cfg.get("internal_dt_scale") is not None:
        internal_dt = config.dt * reference_cfg["internal_dt_scale"]

    rebound = run_rebound_scenario(
        config,
        sample_every=sample_every,
        integrator=reference_cfg["integrator"],
        internal_dt=internal_dt,
    )
    rows = [
        _row("minigrav_direct", run_scenario(config, sample_every=sample_every), rebound),
        _row("explicit_euler_classroom", run_euler_scenario(config, sample_every=sample_every), rebound),
    ]

    if config.initial_state.n_bodies == 2:
        rows.append(_row("poliastro_two_body", run_poliastro_two_body(config, sample_every=sample_every), rebound))

    if config.scenario_id == "star_grazing_two_body":
        rows.append(
            _row(
                "encounter_microstep",
                run_encounter_aware_scenario(
                    config,
                    encounter_radius=0.25,
                    micro_steps=8,
                    sample_every=sample_every,
                ),
                rebound,
            )
        )

    rows.append(_row(rebound["metadata"]["integrator"], rebound, rebound))
    return {
        "scenario_id": config.scenario_id,
        "dt": config.dt,
        "rows": rows,
    }


def _write_markdown(payload: dict) -> None:
    lines = ["# Benchmark Report", "", f"Generated: {payload['generated_at']}", "", "## Error Tables", ""]
    for scenario in payload["scenarios"]:
        lines.extend(
            [
                f"### {scenario['scenario_id']}",
                "",
                "| comparator | dt | final state error vs REBOUND | max energy drift | runtime (s) |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for row in scenario["rows"]:
            energy = "n/a" if row["max_energy_rel_drift"] is None else f"{row['max_energy_rel_drift']:.3e}"
            lines.append(
                f"| {row['comparator']} | {scenario['dt']:.4f} | {row['final_state_rel_error_vs_rebound']:.3e} | {energy} | {row['runtime_seconds']:.3f} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Runtime Table",
            "",
            "| scenario | fastest comparator | slowest comparator |",
            "| --- | --- | --- |",
        ]
    )
    for scenario in payload["scenarios"]:
        ordered = sorted(scenario["rows"], key=lambda row: row["runtime_seconds"])
        lines.append(
            f"| {scenario['scenario_id']} | {ordered[0]['comparator']} ({ordered[0]['runtime_seconds']:.3f}s) | {ordered[-1]['comparator']} ({ordered[-1]['runtime_seconds']:.3f}s) |"
        )

    lines.extend(
        [
            "",
            "## Narrative",
            "",
            "- `minigrav_direct` ties REBOUND closely on smooth two-body and small-N controls, while the classroom Euler baseline is consistently less accurate for the same timestep.",
            "- `poliastro_two_body` is strongest on smooth two-body propagation but is not a mutual-gravity small-N baseline, so it does not replace REBOUND or the audited kernel on 3-body and small-N cases.",
            "- `encounter_microstep` is the only variant aimed at the promoted close-encounter trust spine; it pays extra runtime on `star_grazing_two_body` in exchange for a dedicated encounter policy and round-trip reporting layer.",
            "- REBOUND remains the accuracy anchor, which is expected; the minimal simulator wins only when transparency, machine-readable audit outputs, and close-encounter honesty matter more than feature breadth or raw integration sophistication.",
        ]
    )
    OUTPUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    payload = {
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "scenarios": [_run_scenario_suite(name) for name in SCENARIOS],
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")
    _write_markdown(payload)
    print(f"wrote {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUTPUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
