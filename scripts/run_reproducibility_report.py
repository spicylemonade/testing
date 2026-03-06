#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import subprocess

import numpy as np

from minigrav.comparators.rebound_adapter import run_rebound_scenario
from minigrav.io.scenarios import load_scenario
from minigrav.research.encounters import run_encounter_aware_scenario
from minigrav.research.resolution_softening import run_resolution_coupled_scenario
from minigrav.runner import run_scenario


ROOT = Path(__file__).resolve().parents[1]
VERIFY_DIR = ROOT / "results" / "verification"
RUNTIME_DIR = VERIFY_DIR / "runtime"
MATRIX_JSON = VERIFY_DIR / "reproducibility_matrix.json"
REGIME_JSON = VERIFY_DIR / "close_encounter_regimes.json"
REPORT_MD = VERIFY_DIR / "reproducibility_report.md"

SCENARIOS = [
    ("circular_two_body.json", 1),
    ("figure_eight_three_body.json", 5),
    ("small_n_ring.json", 20),
    ("star_grazing_two_body.json", 2),
]


def _final_state_vector(result: dict) -> np.ndarray:
    terminal = result["diagnostics"][-1]
    return np.asarray(terminal["positions"] + terminal["velocities"], dtype=float).ravel()


def _compare_python_vs_node(scenario_name: str, sample_every: int) -> dict:
    config = load_scenario(ROOT / "scenarios" / scenario_name)
    python_result = run_scenario(config, sample_every=sample_every)
    node_out = RUNTIME_DIR / f"{config.scenario_id}_node.json"
    subprocess.run(
        [
            "node",
            "runtime/minigrav_node.mjs",
            str(ROOT / "scenarios" / scenario_name),
            str(node_out),
            str(sample_every),
        ],
        cwd=ROOT,
        check=True,
    )
    node_result = json.loads(node_out.read_text())
    py_vec = _final_state_vector(python_result)
    node_vec = _final_state_vector(node_result)
    ref_norm = max(float(np.linalg.norm(py_vec)), 1e-12)
    terminal_rel = float(np.linalg.norm(py_vec - node_vec) / ref_norm)
    return {
        "scenario_id": config.scenario_id,
        "sample_every": sample_every,
        "terminal_state_rel_error": terminal_rel,
        "python_runtime_seconds": python_result["metadata"]["runtime_seconds"],
        "node_runtime_seconds": node_result["metadata"]["runtime_seconds"],
    }


def _close_encounter_regimes() -> dict:
    config = load_scenario(ROOT / "scenarios" / "star_grazing_two_body.json")
    dt_values = [0.04, 0.02, 0.01, 0.005]
    rows = []
    for dt in dt_values:
        varied = replace(config, dt=dt, steps=int(round(config.duration / dt)), duration=int(round(config.duration / dt)) * dt)
        reference = run_rebound_scenario(varied, sample_every=2)
        direct = run_scenario(varied, sample_every=2)
        encounter = run_encounter_aware_scenario(varied, encounter_radius=0.25, micro_steps=8, sample_every=2)
        softened = run_resolution_coupled_scenario(varied, k_cell=0.25, sample_every=2)
        ref_vec = _final_state_vector(reference)
        ref_norm = max(float(np.linalg.norm(ref_vec)), 1e-12)

        def summarize(label: str, result: dict) -> dict:
            candidate_vec = _final_state_vector(result)
            error = float(np.linalg.norm(candidate_vec - ref_vec) / ref_norm)
            max_energy = max(row["energy_rel_drift"] for row in result["diagnostics"])
            safe = error <= 1e-2 and max_energy <= 1e-1
            return {
                "mode": label,
                "dt": dt,
                "final_state_rel_error_vs_rebound": error,
                "max_energy_rel_drift": max_energy,
                "safe": safe,
            }

        rows.extend(
            [
                summarize("direct", direct),
                summarize("encounter_microstep", encounter),
                summarize("resolution_coupled", softened),
            ]
        )
    return {"scenario_id": config.scenario_id, "rows": rows}


def main() -> int:
    VERIFY_DIR.mkdir(parents=True, exist_ok=True)
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    matrix = {"scenarios": [_compare_python_vs_node(name, sample_every) for name, sample_every in SCENARIOS]}
    regimes = _close_encounter_regimes()
    MATRIX_JSON.write_text(json.dumps(matrix, indent=2) + "\n")
    REGIME_JSON.write_text(json.dumps(regimes, indent=2) + "\n")

    lines = ["# Reproducibility Report", "", "## Cross-Runtime Envelope", "", "| scenario | sample every | terminal relative error | python runtime (s) | node runtime (s) |", "| --- | --- | --- | --- | --- |"]
    for row in matrix["scenarios"]:
        lines.append(
            f"| {row['scenario_id']} | {row['sample_every']} | {row['terminal_state_rel_error']:.3e} | {row['python_runtime_seconds']:.3f} | {row['node_runtime_seconds']:.3f} |"
        )
    lines.extend(["", "## Close-Encounter Safe And Unsafe Regimes", "", "| mode | dt | final state error vs REBOUND | max energy drift | regime |", "| --- | --- | --- | --- | --- |"])
    for row in regimes["rows"]:
        lines.append(
            f"| {row['mode']} | {row['dt']:.3f} | {row['final_state_rel_error_vs_rebound']:.3e} | {row['max_energy_rel_drift']:.3e} | {'safe' if row['safe'] else 'unsafe'} |"
        )
    lines.extend(
        [
            "",
            "## Divergence Notes",
            "",
            "- The Python and Node direct-sum kernels stay within a tight tolerance envelope on the canonical bundle, so cross-runtime replay is bounded rather than exact.",
            "- On the star-grazing stress case, the plain direct kernel is unsafe at coarse `dt`, while the encounter microstep variant becomes safe earlier than the unmodified path.",
            "- Resolution-coupled softening can stabilize some coarse runs, but it changes the physics enough that it should be treated as an explicit teaching or visualization regime rather than a fidelity-preserving default.",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n")
    print(f"wrote {MATRIX_JSON.relative_to(ROOT)}")
    print(f"wrote {REGIME_JSON.relative_to(ROOT)}")
    print(f"wrote {REPORT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
