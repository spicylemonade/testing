from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
import math
from typing import Any

import numpy as np

from minigrav.benchmarks.orbits import (
    estimate_period_from_diagnostics,
    orbital_elements_from_relative_state,
    relative_state_from_record,
    wrapped_angle_distance,
)
from minigrav.io.scenarios import load_scenario
from minigrav.runner import run_scenario


ROOT = Path(__file__).resolve().parents[3]
SCENARIO_DIR = ROOT / "scenarios"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _dt_grid(base_dt: float) -> list[float]:
    return [base_dt * 2.0, base_dt, base_dt / 2.0]


def _run_with_dt(scenario_name: str, dt: float) -> dict[str, Any]:
    config = load_scenario(SCENARIO_DIR / scenario_name)
    steps = int(round(config.duration / dt))
    varied = replace(config, dt=dt, steps=steps, duration=steps * dt)
    return run_scenario(varied)


def _relative_separations(diagnostics: list[dict[str, Any]]) -> np.ndarray:
    values = []
    for row in diagnostics:
        r, _ = relative_state_from_record(row)
        values.append(float(np.linalg.norm(r)))
    return np.asarray(values, dtype=float)


def _circular_control(dt: float) -> dict[str, Any]:
    result = _run_with_dt("circular_two_body.json", dt)
    expected = result["expected_metrics"]
    separations = _relative_separations(result["diagnostics"])
    r0 = float(expected["relative_separation"])
    rms_rel = float(np.sqrt(np.mean((separations - r0) ** 2)) / r0)
    return {
        "dt": dt,
        "metric": "radial_rms_relative_error",
        "value": rms_rel,
        "threshold": 1e-2,
        "pass": rms_rel <= 1e-2,
    }


def _ellipse_control(dt: float) -> dict[str, Any]:
    result = _run_with_dt("elliptic_two_body.json", dt)
    expected = result["expected_metrics"]
    separations = _relative_separations(result["diagnostics"])
    rp_err = abs(float(np.min(separations)) - float(expected["periapsis"])) / float(expected["periapsis"])
    ra_err = abs(float(np.max(separations)) - float(expected["apoapsis"])) / float(expected["apoapsis"])
    return {
        "dt": dt,
        "metric": "periapsis_apoapsis_relative_error",
        "periapsis_error": rp_err,
        "apoapsis_error": ra_err,
        "threshold": 2e-2,
        "pass": rp_err <= 2e-2 and ra_err <= 2e-2,
    }


def _period_control(dt: float) -> dict[str, Any]:
    result = _run_with_dt("elliptic_two_body.json", dt)
    expected_period = float(result["expected_metrics"]["period"])
    period_hat = estimate_period_from_diagnostics(result["diagnostics"])
    err = math.inf if period_hat is None else abs(period_hat - expected_period) / expected_period
    return {
        "dt": dt,
        "metric": "period_relative_error",
        "period_estimate": period_hat,
        "value": err,
        "threshold": 1e-2,
        "pass": err <= 1e-2,
    }


def _escape_control(dt: float) -> dict[str, Any]:
    result = _run_with_dt("escape_velocity_two_body.json", dt)
    terminal = result["diagnostics"][-1]
    r, v = relative_state_from_record(terminal)
    mu = float(result["metadata"]["gravitational_constant"])
    elements = orbital_elements_from_relative_state(r, v, mu)
    specific_energy = elements["specific_energy"]
    expected = result["expected_metrics"]
    predicted_unbound = specific_energy > 0.0
    v_inf_hat = math.sqrt(max(0.0, 2.0 * specific_energy))
    v_inf_expected = math.sqrt(max(0.0, float(expected["launch_speed"]) ** 2 - float(expected["escape_speed"]) ** 2))
    err = abs(v_inf_hat - v_inf_expected) / max(v_inf_expected, 1e-12)
    return {
        "dt": dt,
        "metric": "escape_classification_and_vinf_error",
        "predicted_unbound": predicted_unbound,
        "expected_unbound": bool(expected["expected_unbound"]),
        "v_inf_hat": v_inf_hat,
        "v_inf_expected": v_inf_expected,
        "value": err,
        "threshold": 5e-2,
        "pass": predicted_unbound == bool(expected["expected_unbound"]) and err <= 5e-2,
    }


def _orbital_elements_control(dt: float) -> dict[str, Any]:
    result = _run_with_dt("orbital_elements_two_body_3d.json", dt)
    terminal = result["diagnostics"][-1]
    r, v = relative_state_from_record(terminal)
    mu = float(result["metadata"]["gravitational_constant"])
    recovered = orbital_elements_from_relative_state(r, v, mu)
    expected = result["expected_metrics"]
    err_a = abs(recovered["semi_major_axis"] - float(expected["semi_major_axis"])) / float(expected["semi_major_axis"])
    err_e = abs(recovered["eccentricity"] - float(expected["eccentricity"])) / max(float(expected["eccentricity"]), 1e-12)
    err_i = abs(recovered["inclination"] - float(expected["inclination"]))
    err_omega = wrapped_angle_distance(recovered["argument_of_periapsis"], float(expected["argument_of_periapsis"]))
    return {
        "dt": dt,
        "metric": "orbital_element_errors",
        "semi_major_axis_error": err_a,
        "eccentricity_error": err_e,
        "inclination_error": err_i,
        "argument_of_periapsis_error": err_omega,
        "thresholds": {
            "semi_major_axis": 2e-2,
            "eccentricity": 2e-2,
            "inclination": 1e-6,
            "argument_of_periapsis": 5e-2,
        },
        "pass": err_a <= 2e-2 and err_e <= 2e-2 and err_i <= 1e-6 and err_omega <= 5e-2,
    }


def run_analytic_controls() -> dict[str, Any]:
    base_dt = load_scenario(SCENARIO_DIR / "circular_two_body.json").dt
    dt_values = _dt_grid(base_dt)
    controls = {
        "circular_orbit": [_circular_control(dt) for dt in dt_values],
        "ellipse_shape": [_ellipse_control(dt) for dt in dt_values],
        "period_recovery": [_period_control(dt) for dt in dt_values],
        "escape_velocity": [_escape_control(dt) for dt in dt_values],
        "orbital_elements": [_orbital_elements_control(dt) for dt in dt_values],
    }
    return {
        "generated_at": _now(),
        "dt_values": dt_values,
        "controls": controls,
    }
