from __future__ import annotations

from pathlib import Path

import numpy as np

from minigrav.core.forces import ForceConfig, compute_pairwise_forces
from minigrav.io.scenarios import load_scenario
from minigrav.runner import run_scenario


ROOT = Path(__file__).resolve().parents[1]


def test_pairwise_force_preserves_net_momentum() -> None:
    config = load_scenario(ROOT / "scenarios" / "circular_two_body.json")
    force_report = compute_pairwise_forces(
        config.initial_state,
        ForceConfig(gravitational_constant=config.gravitational_constant),
    )
    net_force = np.sum(config.initial_state.masses[:, None] * force_report.accelerations, axis=0)
    assert np.allclose(net_force, 0.0)


def test_baseline_scenarios_run_and_record_diagnostics() -> None:
    for name in [
        "circular_two_body.json",
        "figure_eight_three_body.json",
        "small_n_ring.json",
    ]:
        result = run_scenario(ROOT / "scenarios" / name)
        assert result["metadata"]["steps"] + 1 == len(result["diagnostics"])
        assert result["metadata"]["force_model"] == "direct_sum_newtonian"
