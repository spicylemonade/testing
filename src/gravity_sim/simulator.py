from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class SimConfig:
    dt: float
    steps: int
    softening: float = 1e-3
    g: float = 1.0
    method: str = "baseline"
    snapshot_every: int = 1


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
) -> tuple[np.ndarray, np.ndarray]:
    acc = accelerations(positions, masses, g, softening)
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
) -> tuple[np.ndarray, np.ndarray]:
    acc0 = accelerations(positions, masses, g, softening)
    v_half = velocities + 0.5 * dt * acc0
    new_positions = positions + dt * v_half
    acc1 = accelerations(new_positions, masses, g, softening)
    new_velocities = v_half + 0.5 * dt * acc1
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

    if config.method not in {"baseline", "symplectic"}:
        raise ValueError(f"Unsupported method: {config.method}")

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
        if config.method == "baseline":
            positions, velocities = step_baseline_euler(
                positions,
                velocities,
                masses,
                config.dt,
                config.g,
                config.softening,
            )
        else:
            positions, velocities = step_symplectic_leapfrog(
                positions,
                velocities,
                masses,
                config.dt,
                config.g,
                config.softening,
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
