from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean, median
from typing import Dict, List, Mapping, Sequence

from hadamard668.artifacts import (
    ELIAHOU_Q,
    ELIAHOU_S,
    build_control_79,
    build_seed_668_mod64,
    build_structured_h2_control_n9,
    build_target_167,
)
from hadamard668.core import alternating_pm1_from_runs, parse_run_length_notation
from hadamard668.h1 import (
    perturbed_solution_seed,
    projected_pm1_seed,
    random_support_seed,
    run_support_search,
    support_instance_from_artifact,
)
from hadamard668.h2 import StructuredQSInstance, run_structured_qs_search

RESULTS_DIR = Path("results/experiments")

H1_CA_PARAMS = {
    "window": 2,
    "min_gain": 6,
    "phase_move_cap": 4,
    "snapshot_every": 12,
}
H1_RANDOM_CA_PARAMS = {
    "fire_probability": 0.2,
    "phase_move_cap": 4,
    "snapshot_every": 12,
}
H2_CA_PARAMS = {
    "window": 1,
    "min_gain": 100,
    "phase_move_cap": 4,
    "snapshot_every": 8,
}
H2_RANDOM_CA_PARAMS = {
    "fire_probability": 0.25,
    "phase_move_cap": 4,
    "snapshot_every": 8,
}


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def summarise_support_runs(runs: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    primary_values = [int(run["best_state"]["closest_target_distance"]) for run in runs]
    exact_hits = sum(1 for run in runs if bool(run["exact_hit"]))
    return {
        "run_count": len(runs),
        "exact_hit_rate": exact_hits / float(len(runs)) if runs else 0.0,
        "best_primary_min": min(primary_values) if primary_values else None,
        "best_primary_median": median(primary_values) if primary_values else None,
        "best_primary_mean": mean(primary_values) if primary_values else None,
        "median_unique_orbits": median(int(run["unique_orbits"]) for run in runs) if runs else None,
        "median_orbit_collapse_ratio": median(float(run["orbit_collapse_ratio"]) for run in runs) if runs else None,
        "median_accepted_moves": median(int(run["accepted_moves"]) for run in runs) if runs else None,
        "total_elapsed_seconds": sum(float(run["elapsed_seconds"]) for run in runs),
    }


def summarise_modular_runs(runs: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    primary_values = [int(run["best_state"]["l1_defect"]) for run in runs]
    exact_hits = sum(1 for run in runs if bool(run["exact_hit"]))
    goal_hits = sum(1 for run in runs if bool(run.get("goal_hit", run["exact_hit"])))
    return {
        "run_count": len(runs),
        "goal_hit_rate": goal_hits / float(len(runs)) if runs else 0.0,
        "exact_hit_rate": exact_hits / float(len(runs)) if runs else 0.0,
        "best_l1_min": min(primary_values) if primary_values else None,
        "best_l1_median": median(primary_values) if primary_values else None,
        "best_l1_mean": mean(primary_values) if primary_values else None,
        "best_two_adic_max": max(int(run["best_state"]["two_adic_modulus"]) for run in runs) if runs else None,
        "best_defect_count_min": min(int(run["best_state"]["defect_count"]) for run in runs) if runs else None,
        "best_max_defect_min": min(int(run["best_state"]["max_defect_magnitude"]) for run in runs) if runs else None,
        "median_unique_orbits": median(int(run["unique_orbits"]) for run in runs) if runs else None,
        "median_orbit_collapse_ratio": median(float(run["orbit_collapse_ratio"]) for run in runs) if runs else None,
        "median_accepted_moves": median(int(run["accepted_moves"]) for run in runs) if runs else None,
        "total_elapsed_seconds": sum(float(run["elapsed_seconds"]) for run in runs),
    }


def summary_by_field(
    runs: Sequence[Mapping[str, object]],
    field: str,
    summary_fn,
) -> Dict[str, object]:
    grouped: Dict[str, List[Mapping[str, object]]] = {}
    for run in runs:
        grouped.setdefault(str(run[field]), []).append(run)
    return {
        key: summary_fn(group_runs)
        for key, group_runs in sorted(grouped.items())
    }


def nested_summary(
    runs: Sequence[Mapping[str, object]],
    first_field: str,
    second_field: str,
    summary_fn,
) -> Dict[str, object]:
    grouped: Dict[str, List[Mapping[str, object]]] = {}
    for run in runs:
        grouped.setdefault(str(run[first_field]), []).append(run)
    return {
        first_key: summary_by_field(group_runs, second_field, summary_fn)
        for first_key, group_runs in sorted(grouped.items())
    }


def h1_control_runs() -> Dict[str, object]:
    artifact = build_control_79()
    instance = support_instance_from_artifact(artifact)
    steps = 96
    methods = {
        "parallel_gain_ca": H1_CA_PARAMS,
        "direct_greedy": {"snapshot_every": 12},
        "random_rule_ca": H1_RANDOM_CA_PARAMS,
        "random_walk": {"snapshot_every": 12},
    }
    seeds = []
    solution_support = artifact["solution"]["support"]
    for index, perturb in enumerate([2, 4, 6, 8, 10, 12, 14, 16], start=1):
        seeds.append(perturbed_solution_seed(solution_support, instance.length, perturb, 10_000 + index))
    for seed in range(8):
        seeds.append(random_support_seed(instance.length, instance.weight, 20_000 + seed))
    runs: List[Dict[str, object]] = []
    for seed_record in seeds:
        bits = seed_record["bits"]
        for method, params in methods.items():
            runs.append(
                run_support_search(
                    instance=instance,
                    start_bits=bits,
                    method=method,
                    steps=steps,
                    method_params=params,
                    seed_family=str(seed_record["seed_family"]),
                    seed_value=int(seed_record["seed_value"]),
                )
            )
    return {
        "branch": "H1",
        "instance_label": instance.label,
        "budget_steps": steps,
        "seed_count": len(seeds),
        "seed_families": sorted({str(seed["seed_family"]) for seed in seeds}),
        "method_summary": summary_by_field(runs, "method", summarise_support_runs),
        "summary_by_seed_family": summary_by_field(runs, "seed_family", summarise_support_runs),
        "summary_by_method_and_seed_family": nested_summary(runs, "method", "seed_family", summarise_support_runs),
        "runs": runs,
    }


def h1_target_runs() -> Dict[str, object]:
    target_artifact = build_target_167()
    modular_seed = build_seed_668_mod64()
    instance = support_instance_from_artifact(target_artifact)
    steps = 96
    methods = {
        "parallel_gain_ca": H1_CA_PARAMS,
        "direct_greedy": {"snapshot_every": 12},
        "random_rule_ca": H1_RANDOM_CA_PARAMS,
        "random_walk": {"snapshot_every": 12},
    }
    seeds = [random_support_seed(instance.length, instance.weight, 30_000 + seed) for seed in range(16)]
    for shift in range(8):
        seeds.append(projected_pm1_seed(modular_seed["sequences"]["A"], instance.weight, shift))
    runs: List[Dict[str, object]] = []
    for seed_record in seeds:
        bits = seed_record["bits"]
        for method, params in methods.items():
            runs.append(
                run_support_search(
                    instance=instance,
                    start_bits=bits,
                    method=method,
                    steps=steps,
                    method_params=params,
                    seed_family=str(seed_record["seed_family"]),
                    seed_value=int(seed_record["seed_value"]),
                )
            )
    return {
        "branch": "H1",
        "instance_label": instance.label,
        "budget_steps": steps,
        "seed_count": len(seeds),
        "seed_families": sorted({str(seed["seed_family"]) for seed in seeds}),
        "method_summary": summary_by_field(runs, "method", summarise_support_runs),
        "summary_by_seed_family": summary_by_field(runs, "seed_family", summarise_support_runs),
        "summary_by_method_and_seed_family": nested_summary(runs, "method", "seed_family", summarise_support_runs),
        "runs": runs,
    }


def h2_ladder_runs() -> Dict[str, object]:
    artifact = build_structured_h2_control_n9()
    exact_q = artifact["exact_seed"]["q"]
    exact_s = artifact["exact_seed"]["s"]
    methods = {
        "parallel_gain_ca": H2_CA_PARAMS,
        "direct_greedy": {"snapshot_every": 8},
        "random_rule_ca": H2_RANDOM_CA_PARAMS,
        "random_walk": {"snapshot_every": 8},
    }
    runs: List[Dict[str, object]] = []
    for start in artifact["lift_starts"]:
        instance = StructuredQSInstance(
            label=f"h2_ladder::{start['name']}",
            q=[int(value) for value in exact_q],
            s=[int(value) for value in exact_s],
            target_modulus=None,
            control_mode="exact-repair",
        )
        for method, params in methods.items():
            runs.append(
                run_structured_qs_search(
                    instance=instance,
                    start_q=start["q"],
                    start_s=start["s"],
                    method=method,
                    variable_family=str(start["variable_family"]),
                    steps=24,
                    method_params=params,
                    seed_family=str(start["name"]),
                    seed_value=40_000 + len(runs),
                )
            )
    return {
        "branch": "H2",
        "instance_label": "h2_ladder_structured_n9",
        "budget_steps": 24,
        "method_summary": summary_by_field(runs, "method", summarise_modular_runs),
        "summary_by_seed_family": summary_by_field(runs, "seed_family", summarise_modular_runs),
        "summary_by_method_and_seed_family": nested_summary(runs, "method", "seed_family", summarise_modular_runs),
        "runs": runs,
    }


def h2_seed_attempt_runs() -> Dict[str, object]:
    build_seed_668_mod64()
    q = alternating_pm1_from_runs(parse_run_length_notation(ELIAHOU_Q), start=1)
    s = alternating_pm1_from_runs(parse_run_length_notation(ELIAHOU_S), start=1)
    start_s = list(s)
    start_s[41] *= -1
    methods = {
        "parallel_gain_ca": H2_CA_PARAMS,
        "direct_greedy": {"snapshot_every": 8},
        "random_rule_ca": H2_RANDOM_CA_PARAMS,
        "random_walk": {"snapshot_every": 8},
    }
    instance = StructuredQSInstance(
        label="seed_668_mod64_structured",
        q=[int(value) for value in q],
        s=[int(value) for value in s],
        target_modulus=64,
        control_mode="modulus-lift",
    )
    runs: List[Dict[str, object]] = []
    for method, params in methods.items():
        runs.append(
            run_structured_qs_search(
                instance=instance,
                start_q=q,
                start_s=start_s,
                method=method,
                variable_family="s",
                steps=48,
                method_params=params,
                seed_family="seed_sflip41_mod16",
                seed_value=50_000 + len(runs),
            )
        )
    return {
        "branch": "H2",
        "instance_label": instance.label,
        "budget_steps": 48,
        "method_summary": summary_by_field(runs, "method", summarise_modular_runs),
        "summary_by_seed_family": summary_by_field(runs, "seed_family", summarise_modular_runs),
        "summary_by_method_and_seed_family": nested_summary(runs, "method", "seed_family", summarise_modular_runs),
        "runs": runs,
    }


def write_json(path: Path, payload: Mapping[str, object]) -> Path:
    path.write_text(json.dumps(payload, indent=2))
    return path


def run_all(output_dir: Path) -> Dict[str, Path]:
    ensure_dir(output_dir)
    return {
        "h1_control": write_json(output_dir / "h1_control_sweep.json", h1_control_runs()),
        "h1_target": write_json(output_dir / "h1_target_sweep.json", h1_target_runs()),
        "h2_ladder": write_json(output_dir / "h2_ladder.json", h2_ladder_runs()),
        "h2_seed_attempt": write_json(output_dir / "h2_seed_attempt.json", h2_seed_attempt_runs()),
    }


def run_h1(output_dir: Path) -> Dict[str, Path]:
    ensure_dir(output_dir)
    return {
        "h1_control": write_json(output_dir / "h1_control_sweep.json", h1_control_runs()),
        "h1_target": write_json(output_dir / "h1_target_sweep.json", h1_target_runs()),
    }


def run_h2(output_dir: Path) -> Dict[str, Path]:
    ensure_dir(output_dir)
    return {
        "h2_ladder": write_json(output_dir / "h2_ladder.json", h2_ladder_runs()),
        "h2_seed_attempt": write_json(output_dir / "h2_seed_attempt.json", h2_seed_attempt_runs()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Hadamard-668 H1/H2 experiment sweeps.")
    parser.add_argument("command", choices=["run-all", "run-h1", "run-h2"])
    parser.add_argument("--output-dir", default=str(RESULTS_DIR))
    args = parser.parse_args()
    if args.command == "run-h1":
        outputs = run_h1(Path(args.output_dir))
    elif args.command == "run-h2":
        outputs = run_h2(Path(args.output_dir))
    else:
        outputs = run_all(Path(args.output_dir))
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
