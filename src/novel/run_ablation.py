"""
Ablation study for the hybrid multi-config ATSP solver.

Systematically removes one component at a time and measures impact on
the gap vs baseline LKH-3. This validates that each component of the
hybrid solver contributes to the overall improvement.

Components tested:
1. Full solver (control)
2. No warm-start: Disable asymmetry-aware initial tours (Phase 1+2)
3. Single config: Use one default LKH config instead of 5 diverse configs
4. No ILS: Disable Iterated Local Search (Phase 4)
5. No or-opt: Disable or-opt post-processing (Phase 5)
6. No ATSP perturbations: ILS uses only double-bridge (no segment reversal/relocate)

Outputs:
- results/ablation_results.json: Detailed ablation results
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

NODE_ID = os.environ.get("NODE_ID", "c250b5b6")

# Ablation configurations: each removes one component
ABLATION_CONFIGS = {
    "full": {
        "description": "Full solver (all components)",
        "params": {
            "use_initial_tours": True,
            "use_multiconfig": True,
            "use_ils": True,
            "use_oropt": True,
            "ils_perturbation_types": "all",
        },
    },
    "no_warmstart": {
        "description": "No asymmetry-aware initial tours (Phase 1+2 disabled)",
        "params": {
            "use_initial_tours": False,
            "use_multiconfig": True,
            "use_ils": True,
            "use_oropt": True,
            "ils_perturbation_types": "all",
        },
    },
    "single_config": {
        "description": "Single default LKH config (multi-config Phase 3 disabled)",
        "params": {
            "use_initial_tours": True,
            "use_multiconfig": False,
            "use_ils": True,
            "use_oropt": True,
            "ils_perturbation_types": "all",
        },
    },
    "no_ils": {
        "description": "No ILS (Phase 4 disabled, time redistributed to Phase 3)",
        "params": {
            "use_initial_tours": True,
            "use_multiconfig": True,
            "use_ils": False,
            "use_oropt": True,
            "ils_perturbation_types": "all",
        },
    },
    "no_oropt": {
        "description": "No or-opt post-processing (Phase 5 disabled)",
        "params": {
            "use_initial_tours": True,
            "use_multiconfig": True,
            "use_ils": True,
            "use_oropt": False,
            "ils_perturbation_types": "all",
        },
    },
    "no_atsp_pert": {
        "description": "ILS uses only double-bridge (no ATSP-specific perturbations)",
        "params": {
            "use_initial_tours": True,
            "use_multiconfig": True,
            "use_ils": True,
            "use_oropt": True,
            "ils_perturbation_types": "double_bridge_only",
        },
    },
}


def load_baseline_lkh_costs(results_file: str) -> dict:
    """Load LKH-3 reference costs from baseline results."""
    with open(results_file) as f:
        data = json.load(f)
    costs = {}
    for r in data["results"]:
        if r["solver"] == "lkh3" and r["status"] == "ok":
            costs[r["instance"]] = r["cost"]
    return costs


def get_instance_config(n: int) -> dict:
    """Get solver time/trial config based on instance size."""
    if n <= 100:
        return dict(max_trials=500, runs_per_seed=1, time_limit=40)
    elif n <= 250:
        return dict(max_trials=600, runs_per_seed=1, time_limit=80)
    else:
        return dict(max_trials=800, runs_per_seed=1, time_limit=150)


def main():
    instances = load_all_instances()
    baseline_file = project_root / "results" / "baseline_results.json"
    lkh_ref_costs = load_baseline_lkh_costs(str(baseline_file))

    print(f"Loaded {len(instances)} instances")
    print(f"Baseline LKH-3 costs: {len(lkh_ref_costs)} instances")
    print(f"Node ID: {NODE_ID}")
    print(f"Ablation configs: {list(ABLATION_CONFIGS.keys())}")
    print()

    all_results = []  # List of {config, instance, cost, gap, ...}

    for config_name, config in ABLATION_CONFIGS.items():
        print(f"\n{'='*70}")
        print(f"ABLATION: {config_name}")
        print(f"  {config['description']}")
        print(f"{'='*70}")

        config_gaps = []

        for inst in instances:
            name = inst["name"]
            n = inst["matrix"].shape[0]
            ref_cost = lkh_ref_costs.get(name, None)

            size_config = get_instance_config(n)

            print(f"\n  {name} (n={n}):", end=" ", flush=True)

            t0 = time.perf_counter()
            try:
                result = solve_hybrid(
                    inst["matrix"],
                    seed=42,
                    **size_config,
                    **config["params"],
                )
            except Exception as e:
                print(f"FAILED: {e}")
                traceback.print_exc()
                all_results.append({
                    "config": config_name,
                    "instance": name,
                    "n": n,
                    "status": "error",
                    "error": str(e),
                })
                continue
            elapsed = time.perf_counter() - t0

            tour_valid = validate_tour(result["tour"], n)
            verified_cost = compute_tour_cost(result["tour"], inst["matrix"])

            gap_vs_baseline = None
            if ref_cost is not None and ref_cost > 0:
                gap_vs_baseline = (verified_cost / ref_cost - 1) * 100
                config_gaps.append(gap_vs_baseline)

            print(f"cost={verified_cost:.1f}  gap={gap_vs_baseline:+.4f}%  "
                  f"time={elapsed:.1f}s  valid={tour_valid}")

            all_results.append({
                "config": config_name,
                "instance": name,
                "n": n,
                "city": inst.get("city", ""),
                "city_type": inst.get("city_type", ""),
                "status": "ok" if tour_valid else "invalid_tour",
                "cost": float(verified_cost),
                "baseline_lkh_cost": float(ref_cost) if ref_cost else None,
                "gap_vs_baseline_pct": float(gap_vs_baseline) if gap_vs_baseline is not None else None,
                "wall_time": float(elapsed),
                "ils_iters": result.get("params", {}).get("ils_iters", 0),
                "population_size": result.get("population_size", 0),
            })

        if config_gaps:
            mean_gap = float(np.mean(config_gaps))
            print(f"\n  => {config_name} mean gap: {mean_gap:+.4f}%  "
                  f"(score: {-mean_gap:.4f})")

    # Compute summary table
    print(f"\n\n{'='*70}")
    print("ABLATION SUMMARY")
    print(f"{'='*70}")
    print(f"{'Config':<20s} {'Mean Gap%':>10s} {'Score':>10s} {'Improved':>10s} {'Worse':>8s}")
    print("-" * 60)

    config_scores = {}
    for config_name in ABLATION_CONFIGS:
        config_results = [r for r in all_results
                          if r["config"] == config_name and r.get("gap_vs_baseline_pct") is not None]
        if config_results:
            gaps = [r["gap_vs_baseline_pct"] for r in config_results]
            mean_gap = float(np.mean(gaps))
            score = -mean_gap
            improved = sum(1 for g in gaps if g < -0.001)
            worse = sum(1 for g in gaps if g > 0.001)
            config_scores[config_name] = score
            print(f"{config_name:<20s} {mean_gap:>+10.4f} {score:>10.4f} "
                  f"{improved:>10d} {worse:>8d}")
        else:
            config_scores[config_name] = 0.0
            print(f"{config_name:<20s} {'N/A':>10s}")

    # Compute component contributions
    full_score = config_scores.get("full", 0.0)
    print(f"\nComponent contributions (full score - ablated score):")
    for config_name in ABLATION_CONFIGS:
        if config_name == "full":
            continue
        ablated_score = config_scores.get(config_name, 0.0)
        contribution = full_score - ablated_score
        pct = (contribution / full_score * 100) if full_score != 0 else 0
        print(f"  {config_name:<20s}: {contribution:+.4f} ({pct:+.1f}% of total improvement)")

    # Per-instance comparison table
    print(f"\n\nPer-instance gap vs baseline LKH-3 (%):")
    inst_names = sorted(set(r["instance"] for r in all_results))
    header = f"{'Instance':<20s}"
    for cn in ABLATION_CONFIGS:
        header += f" {cn:>14s}"
    print(header)
    print("-" * len(header))
    for iname in inst_names:
        row = f"{iname:<20s}"
        for cn in ABLATION_CONFIGS:
            match = [r for r in all_results
                     if r["config"] == cn and r["instance"] == iname
                     and r.get("gap_vs_baseline_pct") is not None]
            if match:
                row += f" {match[0]['gap_vs_baseline_pct']:>+14.4f}"
            else:
                row += f" {'N/A':>14s}"
        print(row)

    # Save results
    output = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "node_id": NODE_ID,
            "study_type": "ablation",
            "num_instances": len(instances),
            "num_configs": len(ABLATION_CONFIGS),
            "configs": {k: v["description"] for k, v in ABLATION_CONFIGS.items()},
        },
        "results": all_results,
        "summary": {
            "config_scores": config_scores,
            "full_score": full_score,
            "component_contributions": {
                cn: full_score - config_scores.get(cn, 0.0)
                for cn in ABLATION_CONFIGS if cn != "full"
            },
        },
    }

    results_dir = project_root / "results"
    results_dir.mkdir(exist_ok=True)
    results_file = results_dir / "ablation_results.json"
    with open(results_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {results_file}")

    # Write metric for orchestrator (use full solver score)
    metrics_dir = project_root / ".archivara" / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    metric = {
        "metric_name": "score",
        "value": float(full_score),
        "valid": True,
    }
    metric_file = metrics_dir / f"{NODE_ID}.json"
    with open(metric_file, "w") as f:
        json.dump(metric, f, indent=2)
    print(f"Metric saved to {metric_file}")
    print(f"Score: {full_score:.6f}")


if __name__ == "__main__":
    main()
