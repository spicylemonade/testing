from __future__ import annotations

from pathlib import Path

from minigrav.io.scenarios import load_scenario
from minigrav.runner import run_scenario
from minigrav.verification.convergence import run_dt_halving_series


ROOT = Path(__file__).resolve().parents[1]


def test_runner_emits_reproducibility_hooks() -> None:
    result = run_scenario(ROOT / "scenarios" / "circular_two_body.json")
    assert "trajectory_fingerprint" in result["metadata"]
    assert "terminal_state_fingerprint" in result["metadata"]
    assert "roundtrip" in result["metadata"]
    assert "claim_map" in result["metadata"]


def test_dt_halving_series_emits_three_levels() -> None:
    config = load_scenario(ROOT / "scenarios" / "circular_two_body.json")
    series = run_dt_halving_series(config, levels=3)
    assert len(series["runs"]) == 3
    assert len(series["pairwise_deltas"]) == 2
