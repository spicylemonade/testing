"""
Benchmark harness for evaluating TSP solvers on ATSP instances.

Loads instances from data/benchmarks/, runs solvers, records metrics,
and outputs results as JSON.
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

import numpy as np

BENCHMARKS_DIR = Path(__file__).parent.parent / "data" / "benchmarks"
RESULTS_DIR = Path(__file__).parent.parent / "results"


def load_instance(filepath: str) -> dict:
    """Load a benchmark instance from JSON."""
    with open(filepath) as f:
        data = json.load(f)
    data["matrix"] = np.array(data["duration_matrix"])
    return data


def load_all_instances(benchmarks_dir: str = None) -> list[dict]:
    """Load all benchmark instances from the directory."""
    bdir = Path(benchmarks_dir) if benchmarks_dir else BENCHMARKS_DIR
    instances = []
    for fname in sorted(bdir.glob("*.json")):
        instances.append(load_instance(str(fname)))
    return instances


def validate_tour(tour: list[int], n: int) -> bool:
    """Check that a tour visits all n nodes exactly once."""
    return len(tour) == n and set(tour) == set(range(n))


def compute_tour_cost(tour: list[int], matrix: np.ndarray) -> float:
    """Compute total tour cost from distance matrix."""
    cost = 0.0
    n = len(tour)
    for i in range(n):
        cost += matrix[tour[i], tour[(i + 1) % n]]
    return cost


def run_solver_on_instance(
    solver_fn: Callable,
    instance: dict,
    solver_name: str,
    **solver_kwargs,
) -> dict:
    """Run a single solver on a single instance and record metrics."""
    matrix = instance["matrix"]
    n = matrix.shape[0]

    try:
        result = solver_fn(matrix, **solver_kwargs)
        tour = result["tour"]

        # Validate tour
        if not validate_tour(tour, n):
            return {
                "instance": instance["name"],
                "solver": solver_name,
                "status": "invalid_tour",
                "error": f"Tour has {len(tour)} nodes, expected {n}",
            }

        # Verify cost
        verified_cost = compute_tour_cost(tour, matrix)

        return {
            "instance": instance["name"],
            "solver": solver_name,
            "status": "ok",
            "cost": verified_cost,
            "solver_reported_cost": result.get("cost", None),
            "wall_time": result.get("wall_time", None),
            "n": n,
            "city": instance.get("city", "unknown"),
            "city_type": instance.get("city_type", "unknown"),
        }
    except Exception as e:
        return {
            "instance": instance["name"],
            "solver": solver_name,
            "status": "error",
            "error": str(e),
        }


def compute_gaps(results: list[dict], reference_solver: str = "lkh3") -> list[dict]:
    """Compute gap vs reference solver for each result."""
    # Build reference costs per instance
    ref_costs = {}
    for r in results:
        if r.get("solver") == reference_solver and r.get("status") == "ok":
            ref_costs[r["instance"]] = r["cost"]

    # Add gap to each result
    for r in results:
        if r.get("status") == "ok" and r["instance"] in ref_costs:
            ref = ref_costs[r["instance"]]
            if ref > 0:
                r["gap_vs_ref"] = (r["cost"] / ref - 1) * 100  # percentage
                r["gap_vs_ref_abs"] = r["cost"] - ref
            else:
                r["gap_vs_ref"] = None
        else:
            r["gap_vs_ref"] = None

    return results


def compute_summary(results: list[dict]) -> dict:
    """Compute summary statistics across instance categories."""
    summary = {}

    # Group by solver
    solvers = set(r["solver"] for r in results if r.get("status") == "ok")

    for solver in sorted(solvers):
        solver_results = [r for r in results if r["solver"] == solver and r["status"] == "ok"]
        if not solver_results:
            continue

        gaps = [r["gap_vs_ref"] for r in solver_results if r.get("gap_vs_ref") is not None]
        times = [r["wall_time"] for r in solver_results if r.get("wall_time") is not None]
        costs = [r["cost"] for r in solver_results]

        solver_summary = {
            "num_instances": len(solver_results),
            "mean_cost": float(np.mean(costs)),
            "total_cost": float(np.sum(costs)),
        }

        if gaps:
            solver_summary.update({
                "mean_gap_pct": float(np.mean(gaps)),
                "median_gap_pct": float(np.median(gaps)),
                "max_gap_pct": float(np.max(gaps)),
                "min_gap_pct": float(np.min(gaps)),
            })

        if times:
            solver_summary.update({
                "mean_time": float(np.mean(times)),
                "median_time": float(np.median(times)),
                "total_time": float(np.sum(times)),
            })

        # Breakdown by size category
        for size_cat, size_range in [("small", (0, 101)), ("medium", (101, 501)), ("large", (501, 10001))]:
            cat_results = [r for r in solver_results if size_range[0] <= r.get("n", 0) < size_range[1]]
            if cat_results:
                cat_gaps = [r["gap_vs_ref"] for r in cat_results if r.get("gap_vs_ref") is not None]
                solver_summary[f"mean_gap_{size_cat}"] = float(np.mean(cat_gaps)) if cat_gaps else None

        # Breakdown by city type
        for city_type in ["grid", "organic", "mixed"]:
            type_results = [r for r in solver_results if r.get("city_type") == city_type]
            if type_results:
                type_gaps = [r["gap_vs_ref"] for r in type_results if r.get("gap_vs_ref") is not None]
                solver_summary[f"mean_gap_{city_type}"] = float(np.mean(type_gaps)) if type_gaps else None

        summary[solver] = solver_summary

    return summary


def run_benchmark(
    solver_configs: dict[str, tuple[Callable, dict]],
    instances: Optional[list[dict]] = None,
    output_file: str = None,
) -> dict:
    """
    Run full benchmark suite.

    Parameters
    ----------
    solver_configs : dict
        Mapping of solver_name -> (solver_fn, kwargs)
    instances : list of dicts, optional
        Benchmark instances. If None, loads all from data/benchmarks/.
    output_file : str, optional
        Path to save results JSON.

    Returns
    -------
    dict with keys: results, summary, metadata
    """
    if instances is None:
        instances = load_all_instances()

    all_results = []

    for inst in instances:
        print(f"Instance: {inst['name']} (n={inst['matrix'].shape[0]})")
        for solver_name, (solver_fn, kwargs) in solver_configs.items():
            print(f"  Running {solver_name}...", end=" ", flush=True)
            result = run_solver_on_instance(solver_fn, inst, solver_name, **kwargs)
            all_results.append(result)
            if result["status"] == "ok":
                print(f"cost={result['cost']:.1f}  time={result.get('wall_time', 0):.3f}s")
            else:
                print(f"FAILED: {result.get('error', 'unknown')}")

    # Compute gaps vs LKH-3
    all_results = compute_gaps(all_results, reference_solver="lkh3")
    summary = compute_summary(all_results)

    output = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "num_instances": len(instances),
            "num_solvers": len(solver_configs),
            "solvers": list(solver_configs.keys()),
        },
        "results": all_results,
        "summary": summary,
    }

    if output_file:
        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(output, f, indent=2, default=str)
        print(f"\nResults saved to {output_file}")

    return output


if __name__ == "__main__":
    from src.solvers.baselines import (
        nearest_neighbor,
        random_insertion,
        vroom_solver,
    )
    from src.solvers.lkh_solver import solve_atsp as lkh_solve

    # Define solver configurations
    solver_configs = {
        "lkh3": (lkh_solve, {"max_trials": 100, "runs": 1, "seed": 42}),
        "nearest_neighbor": (nearest_neighbor, {"seed": 42}),
        "random_insertion": (random_insertion, {"seed": 42}),
        "vroom": (vroom_solver, {"seed": 42}),
    }

    # Run on first 3 instances as a test
    instances = load_all_instances()[:3]
    print(f"Testing harness on {len(instances)} instances...")
    print()

    output = run_benchmark(
        solver_configs,
        instances=instances,
        output_file="results/harness_test.json",
    )

    print("\n=== Summary ===")
    for solver, stats in output["summary"].items():
        gap_str = f"mean_gap={stats.get('mean_gap_pct', 'N/A'):.2f}%" if stats.get("mean_gap_pct") is not None else ""
        time_str = f"mean_time={stats.get('mean_time', 0):.3f}s" if stats.get("mean_time") is not None else ""
        print(f"  {solver:20s}: {gap_str}  {time_str}")
