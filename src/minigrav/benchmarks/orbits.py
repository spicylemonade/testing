from __future__ import annotations

import math
from typing import Any

import numpy as np


def relative_state_from_record(record: dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    positions = np.asarray(record["positions"], dtype=float)
    velocities = np.asarray(record["velocities"], dtype=float)
    return positions[1] - positions[0], velocities[1] - velocities[0]


def wrapped_angle_distance(angle_a: float, angle_b: float) -> float:
    raw = (angle_a - angle_b + math.pi) % (2.0 * math.pi) - math.pi
    return abs(raw)


def orbital_elements_from_relative_state(r: np.ndarray, v: np.ndarray, mu: float) -> dict[str, float]:
    r_norm = float(np.linalg.norm(r))
    v_norm = float(np.linalg.norm(v))
    h = np.cross(r, v)
    h_norm = float(np.linalg.norm(h))
    e_vec = np.cross(v, h) / mu - r / r_norm
    e = float(np.linalg.norm(e_vec))
    specific_energy = 0.5 * v_norm**2 - mu / r_norm
    semi_major_axis = math.inf if abs(specific_energy) < 1e-12 else -mu / (2.0 * specific_energy)
    inclination = 0.0 if h_norm == 0.0 else math.acos(max(-1.0, min(1.0, h[2] / h_norm)))
    argument_of_periapsis = 0.0 if e < 1e-12 else math.atan2(e_vec[1], e_vec[0])
    return {
        "semi_major_axis": float(semi_major_axis),
        "eccentricity": e,
        "inclination": float(inclination),
        "argument_of_periapsis": float(argument_of_periapsis),
        "specific_energy": float(specific_energy),
    }


def estimate_period_from_diagnostics(diagnostics: list[dict[str, Any]]) -> float | None:
    angles = []
    times = []
    for row in diagnostics:
        r, _ = relative_state_from_record(row)
        angles.append(math.atan2(float(r[1]), float(r[0])))
        times.append(float(row["time"]))
    unwrapped = np.unwrap(np.asarray(angles, dtype=float))
    target = unwrapped[0] + 2.0 * math.pi
    for idx in range(1, len(unwrapped)):
        if unwrapped[idx] >= target:
            t0 = times[idx - 1]
            t1 = times[idx]
            a0 = float(unwrapped[idx - 1])
            a1 = float(unwrapped[idx])
            if a1 == a0:
                return t1
            fraction = (target - a0) / (a1 - a0)
            return float(t0 + fraction * (t1 - t0))
    return None
