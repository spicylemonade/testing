from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class SimConfig:
    dt: float
    steps: int
    softening: float = 1e-3
    g: float = 1.0
    method: str = "baseline"
    snapshot_every: int = 1
    theta: float = 0.7
    leaf_size: int = 8
    bh_min_n: int = 64


def accelerations(positions: np.ndarray, masses: np.ndarray, g: float, softening: float) -> np.ndarray:
    n = positions.shape[0]
    acc = np.zeros_like(positions, dtype=np.float64)
    eps2 = softening * softening

    for i in range(n):
        for j in range(i + 1, n):
            delta = positions[j] - positions[i]
            r2 = float(delta[0] * delta[0] + delta[1] * delta[1] + eps2)
            inv_r = 1.0 / np.sqrt(r2)
            inv_r3 = inv_r / r2
            force = g * delta * inv_r3
            acc[i] += masses[j] * force
            acc[j] -= masses[i] * force
    return acc


def step_baseline_euler(
    positions: np.ndarray,
    velocities: np.ndarray,
    masses: np.ndarray,
    dt: float,
    g: float,
    softening: float,
    accel_fn: Callable[[np.ndarray, np.ndarray, float, float], np.ndarray] = accelerations,
) -> tuple[np.ndarray, np.ndarray]:
    acc = accel_fn(positions, masses, g, softening)
    new_positions = positions + velocities * dt
    new_velocities = velocities + acc * dt
    return new_positions, new_velocities


def step_symplectic_leapfrog(
    positions: np.ndarray,
    velocities: np.ndarray,
    masses: np.ndarray,
    dt: float,
    g: float,
    softening: float,
    accel_fn: Callable[[np.ndarray, np.ndarray, float, float], np.ndarray] = accelerations,
) -> tuple[np.ndarray, np.ndarray]:
    # Kick-drift symplectic Euler (single force evaluation per step).
    acc = accel_fn(positions, masses, g, softening)
    new_velocities = velocities + dt * acc
    new_positions = positions + dt * new_velocities
    return new_positions, new_velocities


def total_energy(positions: np.ndarray, velocities: np.ndarray, masses: np.ndarray, g: float, softening: float) -> float:
    kinetic = 0.5 * np.sum(masses[:, None] * velocities * velocities)
    potential = 0.0
    eps2 = softening * softening
    n = positions.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            delta = positions[j] - positions[i]
            r2 = float(delta[0] * delta[0] + delta[1] * delta[1] + eps2)
            potential -= g * masses[i] * masses[j] / np.sqrt(r2)
    return float(kinetic + potential)


def total_angular_momentum(positions: np.ndarray, velocities: np.ndarray, masses: np.ndarray) -> float:
    # 2D scalar angular momentum (z-component).
    return float(np.sum(masses * (positions[:, 0] * velocities[:, 1] - positions[:, 1] * velocities[:, 0])))


def center_of_mass(positions: np.ndarray, masses: np.ndarray) -> np.ndarray:
    total_mass = float(np.sum(masses))
    return np.sum(positions * masses[:, None], axis=0) / total_mass


def simulate(
    positions: np.ndarray,
    velocities: np.ndarray,
    masses: np.ndarray,
    config: SimConfig,
) -> dict:
    positions = positions.astype(np.float64, copy=True)
    velocities = velocities.astype(np.float64, copy=True)
    masses = masses.astype(np.float64, copy=True)

    if config.method not in {"baseline", "symplectic", "barnes_hut"}:
        raise ValueError(f"Unsupported method: {config.method}")

    accel_fn: Callable[[np.ndarray, np.ndarray, float, float], np.ndarray] = accelerations
    if config.method == "barnes_hut":
        from .barnes_hut import accelerations_barnes_hut

        def _bh_accel(pos: np.ndarray, m: np.ndarray, g: float, soft: float) -> np.ndarray:
            return accelerations_barnes_hut(
                pos,
                m,
                g,
                soft,
                theta=config.theta,
                leaf_size=config.leaf_size,
                min_n_direct=config.bh_min_n,
            )

        accel_fn = _bh_accel

    frames = []

    def record(step: int, time: float):
        if step % config.snapshot_every == 0:
            frames.append(
                {
                    "step": int(step),
                    "time": float(time),
                    "positions": np.round(positions, 12).tolist(),
                    "velocities": np.round(velocities, 12).tolist(),
                    "energy": total_energy(positions, velocities, masses, config.g, config.softening),
                    "angular_momentum": total_angular_momentum(positions, velocities, masses),
                    "center_of_mass": np.round(center_of_mass(positions, masses), 12).tolist(),
                }
            )

    record(step=0, time=0.0)
    time = 0.0
    for step in range(1, config.steps + 1):
        if config.method in {"baseline", "barnes_hut"}:
            positions, velocities = step_baseline_euler(
                positions,
                velocities,
                masses,
                config.dt,
                config.g,
                config.softening,
                accel_fn=accel_fn,
            )
        else:
            positions, velocities = step_symplectic_leapfrog(
                positions,
                velocities,
                masses,
                config.dt,
                config.g,
                config.softening,
                accel_fn=accel_fn,
            )
        time += config.dt
        record(step=step, time=time)

    return {
        "method": config.method,
        "dt": config.dt,
        "steps": config.steps,
        "softening": config.softening,
        "g": config.g,
        "n_bodies": int(masses.shape[0]),
        "frames": frames,
    }
