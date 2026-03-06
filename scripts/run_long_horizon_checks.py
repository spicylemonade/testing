#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from minigrav.io.scenarios import load_scenario
from minigrav.runner import run_scenario
from minigrav.verification.convergence import run_dt_halving_series


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON = ROOT / "results" / "verification" / "long_horizon_metrics.json"
OUTPUT_MD = ROOT / "results" / "verification" / "long_horizon_drift.md"
FIGURE_PNG = ROOT / "figures" / "long_horizon_drift.png"
FIGURE_PDF = ROOT / "figures" / "long_horizon_drift.pdf"

SCENARIOS = [
    "circular_two_body.json",
    "figure_eight_three_body.json",
    "small_n_ring.json",
]


def _dt_grid(base_dt: float) -> list[float]:
    return [base_dt * 2.0, base_dt, base_dt / 2.0]


def _run_metrics(scenario_name: str) -> dict:
    config = load_scenario(ROOT / "scenarios" / scenario_name)
    scenario_rows = []
    for dt in _dt_grid(config.dt):
        varied = load_scenario(ROOT / "scenarios" / scenario_name)
        varied = type(varied)(
            scenario_id=varied.scenario_id,
            description=varied.description,
            unit_system=varied.unit_system,
            seed=varied.seed,
            gravitational_constant=varied.gravitational_constant,
            duration=int(round(varied.duration / dt)) * dt,
            dt=dt,
            steps=int(round(varied.duration / dt)),
            expected_metrics=varied.expected_metrics,
            benchmark_tags=varied.benchmark_tags,
            initial_state=varied.initial_state,
        )
        result = run_scenario(varied)
        diagnostics = result["diagnostics"]
        scenario_rows.append(
            {
                "dt": dt,
                "max_energy_rel_drift": max(row["energy_rel_drift"] for row in diagnostics),
                "max_angular_momentum_rel_drift": max(
                    row["angular_momentum_rel_drift"] for row in diagnostics
                ),
                "max_center_of_mass_abs_drift": max(
                    row["center_of_mass_abs_drift"] for row in diagnostics
                ),
                "max_center_of_mass_velocity_abs_drift": max(
                    row["center_of_mass_velocity_abs_drift"] for row in diagnostics
                ),
            }
        )
    convergence = run_dt_halving_series(config, levels=3)
    for row in scenario_rows:
        row["energy_pass"] = row["max_energy_rel_drift"] <= 1e-2
        row["angular_momentum_pass"] = row["max_angular_momentum_rel_drift"] <= 1e-2
        row["center_of_mass_pass"] = (
            row["max_center_of_mass_abs_drift"] <= 1e-9
            and row["max_center_of_mass_velocity_abs_drift"] <= 1e-9
        )
        row["overall_pass"] = row["energy_pass"] and row["angular_momentum_pass"] and row["center_of_mass_pass"]
    convergence_pass = all(
        delta["energy_drift_ratio"] <= 1.0 and delta["angular_momentum_drift_ratio"] <= 1.0
        for delta in convergence["pairwise_deltas"]
    )
    return {
        "scenario_id": config.scenario_id,
        "dt_runs": scenario_rows,
        "convergence": convergence,
        "convergence_pass": convergence_pass,
    }


def _write_markdown(payload: dict) -> None:
    lines = ["# Long-Horizon Drift", "", f"Generated: {payload['generated_at']}", ""]
    for scenario in payload["scenarios"]:
        lines.extend(
            [
                f"## {scenario['scenario_id']}",
                "",
                "| dt | max energy drift | max angular-momentum drift | max COM drift | pass |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for row in scenario["dt_runs"]:
            lines.append(
                f"| {row['dt']:.4f} | {row['max_energy_rel_drift']:.3e} | {row['max_angular_momentum_rel_drift']:.3e} | {row['max_center_of_mass_abs_drift']:.3e} | {'pass' if row['overall_pass'] else 'fail'} |"
            )
        lines.append("")
        lines.append(
            f"Convergence check: {'pass' if scenario['convergence_pass'] else 'fail'} based on monotonic improvement under timestep halving."
        )
        if not scenario["convergence_pass"] and scenario["scenario_id"] == "figure_eight_three_body":
            lines.append(
                "Figure-eight note: the angular-momentum convergence gate is flagged because this choreography starts near zero total angular momentum, so the relative-drift ratio is especially noise-sensitive."
            )
        lines.append("")
    OUTPUT_MD.write_text("\n".join(lines) + "\n")


def _write_figure(payload: dict) -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "figure.dpi": 300,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "legend.fontsize": 8,
            "font.family": "DejaVu Serif",
        }
    )

    rows = []
    for scenario in payload["scenarios"]:
        for row in scenario["dt_runs"]:
            rows.append(
                {
                    "scenario_id": scenario["scenario_id"],
                    "dt": row["dt"],
                    "energy": row["max_energy_rel_drift"],
                    "angular_momentum": row["max_angular_momentum_rel_drift"],
                    "center_of_mass": row["max_center_of_mass_abs_drift"],
                }
            )
    frame = pd.DataFrame(rows)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), constrained_layout=True)
    metrics = [
        ("energy", "Max relative energy drift"),
        ("angular_momentum", "Max relative angular momentum drift"),
        ("center_of_mass", "Max absolute COM drift"),
    ]
    palette = sns.color_palette("crest", n_colors=frame["scenario_id"].nunique())
    for axis, (column, label) in zip(axes, metrics):
        sns.lineplot(
            data=frame,
            x="dt",
            y=column,
            hue="scenario_id",
            marker="o",
            palette=palette,
            ax=axis,
        )
        axis.set_xscale("log")
        axis.set_yscale("log")
        axis.set_xlabel("dt")
        axis.set_ylabel(label)
        axis.set_title(label)
    axes[-1].legend(title="scenario", loc="upper right")
    fig.savefig(FIGURE_PNG, dpi=300, bbox_inches="tight")
    fig.savefig(FIGURE_PDF, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    payload = {
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "scenarios": [_run_metrics(name) for name in SCENARIOS],
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    FIGURE_PNG.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")
    _write_markdown(payload)
    _write_figure(payload)
    print(f"wrote {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUTPUT_MD.relative_to(ROOT)}")
    print(f"wrote {FIGURE_PNG.relative_to(ROOT)}")
    print(f"wrote {FIGURE_PDF.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
