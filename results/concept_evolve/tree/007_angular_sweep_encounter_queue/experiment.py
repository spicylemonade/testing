#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from minigrav.io.scenarios import load_scenario
from minigrav.research.encounters import build_angular_sweep_queue
from minigrav.core.forces import ForceConfig, compute_pairwise_forces
from minigrav.core.integrators import step_leapfrog


ROOT = Path(__file__).resolve().parents[4]
OUTPUT_PATH = Path(__file__).with_name("results.json")


def brute_force_pairs(state, dt: float, encounter_radius: float) -> set[tuple[int, int]]:
    drift_positions = state.positions + dt * state.velocities
    pairs = set()
    for i in range(state.n_bodies - 1):
        for j in range(i + 1, state.n_bodies):
            midpoint_i = 0.5 * (state.positions[i] + drift_positions[i])
            midpoint_j = 0.5 * (state.positions[j] + drift_positions[j])
            distances = [
                float(np.linalg.norm(state.positions[i] - state.positions[j])),
                float(np.linalg.norm(drift_positions[i] - drift_positions[j])),
                float(np.linalg.norm(midpoint_i - midpoint_j)),
            ]
            if min(distances) < encounter_radius:
                pairs.add((i, j))
    return pairs


def evaluate(scenario_name: str, encounter_radius: float, steps: int) -> dict:
    config = load_scenario(ROOT / "scenarios" / scenario_name)
    state = config.initial_state.copy()
    force_config = ForceConfig(config.gravitational_constant)
    recalls = []
    candidate_counts = []
    all_pair_count = state.n_bodies * (state.n_bodies - 1) // 2
    for _ in range(steps):
        queue = set(build_angular_sweep_queue(state, config.dt, encounter_radius))
        truth = brute_force_pairs(state, config.dt, encounter_radius)
        if truth:
            recalls.append(len(queue & truth) / len(truth))
        candidate_counts.append(len(queue))
        state, _ = step_leapfrog(state, config.dt, force_config)
    return {
        "scenario_id": config.scenario_id,
        "encounter_radius": encounter_radius,
        "mean_recall": float(np.mean(recalls)) if recalls else 1.0,
        "max_candidates": int(max(candidate_counts) if candidate_counts else 0),
        "mean_candidates": float(np.mean(candidate_counts) if candidate_counts else 0.0),
        "all_pair_count": all_pair_count,
    }


def main() -> int:
    payload = {
        "concept": "angular_sweep_encounter_queue",
        "evaluations": [
            evaluate("star_grazing_two_body.json", encounter_radius=0.25, steps=50),
            evaluate("small_n_ring.json", encounter_radius=0.2, steps=120),
        ],
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
