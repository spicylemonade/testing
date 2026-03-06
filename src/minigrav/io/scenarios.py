from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import numpy as np

from minigrav.core.state import BodyState


@dataclass(frozen=True)
class SimulationConfig:
    scenario_id: str
    description: str
    unit_system: str
    seed: int
    gravitational_constant: float
    duration: float
    dt: float
    steps: int
    expected_metrics: dict[str, Any]
    benchmark_tags: tuple[str, ...]
    initial_state: BodyState


def load_scenario(path: str | Path) -> SimulationConfig:
    payload = json.loads(Path(path).read_text())
    dt = float(payload["dt"])
    requested_duration = float(payload["duration"])
    if "steps" in payload:
        steps = int(payload["steps"])
        duration = steps * dt
    else:
        steps = int(round(requested_duration / dt))
        if not np.isclose(steps * dt, requested_duration):
            raise ValueError("duration must be an integer multiple of dt when steps is omitted")
        duration = steps * dt

    bodies = payload["bodies"]
    ids = tuple(body["id"] for body in bodies)
    masses = np.asarray([body["mass"] for body in bodies], dtype=float)
    radii = np.asarray([body.get("radius", 0.0) for body in bodies], dtype=float)
    positions = np.asarray([body["position"] for body in bodies], dtype=float)
    velocities = np.asarray([body["velocity"] for body in bodies], dtype=float)

    state = BodyState(
        ids=ids,
        masses=masses,
        radii=radii,
        positions=positions,
        velocities=velocities,
    )

    return SimulationConfig(
        scenario_id=payload["scenario_id"],
        description=payload["description"],
        unit_system=payload["unit_system"],
        seed=int(payload.get("seed", 42)),
        gravitational_constant=float(payload["gravitational_constant"]),
        duration=duration,
        dt=dt,
        steps=steps,
        expected_metrics=dict(payload.get("expected_metrics", {})),
        benchmark_tags=tuple(payload.get("benchmark_tags", [])),
        initial_state=state,
    )
