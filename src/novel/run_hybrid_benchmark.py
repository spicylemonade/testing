"""
Run the hybrid multi-config solver on all ATSP benchmark instances and compare
against baseline LKH-3 results.

Outputs:
- results/hybrid_results.json: Full benchmark results
- .archivara/metrics/<NODE_ID>.json: Score metric for orchestrator
"""

import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# Ensure project root is on path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.benchmark_harness import load_all_instances, validate_tour, compute_tour_cost
from src.novel.asymmetric_ils import solve_hybrid

# Node ID from environment or default
NODE_ID = os.environ.get("NODE_ID", "96d65801")


def load_baseline_lkh_costs(results_file: str) -> dict:
    """Load LKH-3 reference costs from baseline results."""
    with open(results_file) as f:
        data = json.load(f)
    costs = {}
    for r in data["results"]:
        if r["solver"] == "lkh3" and r["status"] == "ok":
            costs[r["instance"]] = r["cost"]
    return costs


def main():
    instances = load_all_instances()
    baseline_file = project_root / "results" / "baseline_results.json"
    lkh_ref_costs = load_baseline_lkh_costs(str(baseline_file))

    print(f"Loaded {len(instances)} instances")
    print(f"Baseline LKH-3 costs: {len(lkh_ref_costs)} instances")
    print(f"Node ID: {NODE_ID}")
    print()

    results = []
    all_gaps = []

    for inst in instances:
        name = inst["name"]
        n = inst["matrix"].shape[0]
        ref_cost = lkh_ref_costs.get(name, None)

        print(f"=== {name} (n={n}) ===")
        if ref_cost is not None:
            print(f"  Baseline LKH-3 cost: {ref_cost:.1f}")

        # Configure solver based on instance size
        # Tuned: generous time for medium/large where ILS+perturbation helps most
        if n <= 100:
            # Small: LKH finds optimal quickly; moderate time for ILS exploration
            config = dict(
                max_trials=700, runs_per_seed=1,
                time_limit=60, use_initial_tours=True,
            )
        elif n <= 250:
            # Medium: increased time for deeper ILS exploration
            config = dict(
                max_trials=800, runs_per_seed=1,
                time_limit=130, use_initial_tours=True,
            )
        else:
            # Large: max time for ILS - biggest improvement opportunity
            config = dict(
                max_trials=1000, runs_per_seed=1,
                time_limit=240, use_initial_tours=True,
            )

        t0 = time.perf_counter()
        try:
            result = solve_hybrid(inst["matrix"], seed=42, **config)
        except Exception as e:
            print(f"  FAILED: {e}")
            traceback.print_exc()
            results.append({
                "instance": name, "n": n, "solver": "hybrid_multiconfig",
                "status": "error", "error": str(e),
            })
            continue
        elapsed = time.perf_counter() - t0

        # Validate tour
        tour_valid = validate_tour(result["tour"], n)
        verified_cost = compute_tour_cost(result["tour"], inst["matrix"])

        print(f"  Hybrid cost:   {verified_cost:.1f}")
        print(f"  LKH best:      {result['lkh_cost']:.1f}")
        print(f"  Tour valid:    {tour_valid}")
        print(f"  Seeds tried:   {result.get('seeds_tried', '?')}")
        print(f"  Warm starts:   {result.get('warm_starts', '?')}")
        print(f"  Population:    {result.get('population_size', '?')}")
        print(f"  Total time:    {elapsed:.1f}s")

        gap_vs_baseline = None
        if ref_cost is not None and ref_cost > 0:
            gap_vs_baseline = (verified_cost / ref_cost - 1) * 100
            all_gaps.append(gap_vs_baseline)
            print(f"  Gap vs baseline LKH: {gap_vs_baseline:+.4f}%")

        improvement_vs_own_lkh = result.get("improvement_pct", 0.0)
        print(f"  Improvement vs own LKH: {improvement_vs_own_lkh:+.4f}%")
        print()

        results.append({
            "instance": name,
            "n": n,
            "city": inst.get("city", ""),
            "city_type": inst.get("city_type", ""),
            "solver": "hybrid_multiconfig",
            "status": "ok" if tour_valid else "invalid_tour",
            "cost": float(verified_cost),
            "lkh_cost": float(result["lkh_cost"]),
            "baseline_lkh_cost": float(ref_cost) if ref_cost else None,
            "gap_vs_baseline_pct": float(gap_vs_baseline) if gap_vs_baseline is not None else None,
            "improvement_vs_own_lkh_pct": float(improvement_vs_own_lkh),
            "wall_time": float(elapsed),
            "lkh_time": float(result.get("lkh_time", 0)),
            "population_size": result.get("population_size", 0),
            "seeds_tried": result.get("seeds_tried", 0),
            "warm_starts": result.get("warm_starts", 0),
            "params": result.get("params", {}),
        })

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if all_gaps:
        mean_gap = float(np.mean(all_gaps))
        print(f"Mean gap vs baseline LKH-3: {mean_gap:+.4f}%")
        print(f"Min gap:  {min(all_gaps):+.4f}%")
        print(f"Max gap:  {max(all_gaps):+.4f}%")

        improvements = sum(1 for g in all_gaps if g < -0.001)
        ties = sum(1 for g in all_gaps if abs(g) <= 0.001)
        worse = sum(1 for g in all_gaps if g > 0.001)
        print(f"Improved: {improvements}/{len(all_gaps)}")
        print(f"Tied:     {ties}/{len(all_gaps)}")
        print(f"Worse:    {worse}/{len(all_gaps)}")

        # Score: negative gap = improvement (positive score)
        score = -mean_gap
        print(f"\nScore (negative mean gap = improvement): {score:.6f}")
    else:
        score = 0.0
        mean_gap = 0.0
        print("No gaps computed (missing baseline data)")

    # Save results
    output = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "solver": "hybrid_multiconfig",
            "num_instances": len(instances),
            "description": "Multi-config LKH (ALPHA + NN candidates + deep search + patching) "
                           "with asymmetry-aware warm starts and or-opt post-processing",
        },
        "results": results,
        "summary": {
            "mean_gap_vs_baseline_pct": float(mean_gap) if all_gaps else None,
            "score": float(score),
            "num_improved": sum(1 for g in all_gaps if g < -0.001),
            "num_tied": sum(1 for g in all_gaps if abs(g) <= 0.001),
            "num_worse": sum(1 for g in all_gaps if g > 0.001),
            "all_gaps": [float(g) for g in all_gaps],
        },
    }

    results_dir = project_root / "results"
    results_dir.mkdir(exist_ok=True)
    results_file = results_dir / "hybrid_results.json"
    with open(results_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {results_file}")

    # Write metric for orchestrator
    metrics_dir = project_root / ".archivara" / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    metric = {
        "metric_name": "score",
        "value": float(score),
        "valid": True,
    }
    metric_file = metrics_dir / f"{NODE_ID}.json"
    with open(metric_file, "w") as f:
        json.dump(metric, f, indent=2)
    print(f"Metric saved to {metric_file}")
    print(f"Score: {score:.6f}")


if __name__ == "__main__":
    main()
