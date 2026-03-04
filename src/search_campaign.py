#!/usr/bin/env python3
"""Full BB(6) search campaign.

Runs all search strategies:
1. TNF enumeration (random sample from 6-state space)
2. Mutation search from known champions
3. TM breeding/recombination
4. Random biased search (guided by champion features)

Collects results, verifies top candidates, and produces analysis.
"""

import json
import os
import random
import time
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.tm_simulator import TuringMachine, HALT_STATE
from src.tm_accelerated import AcceleratedTuringMachine, _C_AVAILABLE
from src.mutation_search import all_single_mutations, mutation_search
from src.tm_breeding import breed_population
from src.guided_search import guided_search, generate_biased_machine, extract_features
from src.parallel_search import ParallelSearch, generate_random_machines
from src.deciders import LoopDecider, CTLDecider


def run_tnf_sample_search(num_machines=100000, step_limit=10**6, seed=42):
    """Strategy 1: Random sample from TNF 6-state space."""
    print(f"\n[Strategy 1] TNF Random Sample Search ({num_machines} machines)...")
    start = time.time()

    machines = generate_random_machines(num_machines, num_states=6, seed=seed)

    ps = ParallelSearch(step_limit=step_limit)
    results = ps.search(machines, batch_size=500)

    results["strategy"] = "tnf_random_sample"
    results["wall_time_seconds"] = round(time.time() - start, 2)

    print(f"  Explored: {results['total_explored']}")
    print(f"  Halting: {results['total_halting']}")
    print(f"  Best sigma: {results['best_sigma']}")
    print(f"  Time: {results['wall_time_seconds']}s")

    return results


def run_mutation_campaign(step_limit=10**6, seed=42):
    """Strategy 2: Mutation search from champions."""
    print(f"\n[Strategy 2] Mutation Search Campaign...")
    seeds = [
        "1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE",  # Kropitz t15
        "1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE",  # mxdys
        "1RB1LE_1RC1RF_1LD0RB_1RE1LA_0LA1RZ_1RC0RE",  # Kropitz e1B
        "1RB1LE_1RC1RF_1LD0RB_1RE0LC_1LA1RZ_1LD1RC",  # Kropitz 2010
    ]

    start = time.time()
    results = mutation_search(seeds, step_limit=step_limit, double_mutations=True, rng_seed=seed)
    results["wall_time_seconds"] = round(time.time() - start, 2)

    print(f"  Explored: {results['total_explored']}")
    print(f"  Halting: {results['total_halting']}")
    print(f"  Best sigma: {results['best_sigma']}")
    print(f"  Time: {results['wall_time_seconds']}s")

    return results


def run_breeding_campaign(step_limit=10**6, seed=42):
    """Strategy 3: TM breeding from champions."""
    print(f"\n[Strategy 3] TM Breeding Campaign...")
    parents = [
        "1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE",
        "1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE",
        "1RB1LE_1RC1RF_1LD0RB_1RE1LA_0LA1RZ_1RC0RE",
        "1RB1LE_1RC1RF_1LD0RB_1RE0LC_1LA1RZ_1LD1RC",
    ]

    start = time.time()
    results = breed_population(parents, num_offspring=10000, step_limit=step_limit, seed=seed)
    results["strategy"] = "tm_breeding"
    results["wall_time_seconds"] = round(time.time() - start, 2)

    print(f"  Unique offspring: {results['num_unique_offspring']}")
    print(f"  Halting: {results['num_halting']}")
    print(f"  Best sigma: {results['best_sigma']}")
    print(f"  Time: {results['wall_time_seconds']}s")

    return results


def run_guided_campaign(num_machines=100000, step_limit=10**6, seed=42):
    """Strategy 4: Guided search biased by champion features."""
    print(f"\n[Strategy 4] Guided Feature-Based Search ({num_machines} machines)...")
    start = time.time()
    results = guided_search(num_machines=num_machines, step_limit=step_limit, seed=seed)
    results["wall_time_seconds"] = round(time.time() - start, 2)

    print(f"  Halting: {results['halting_count']}/{results['num_machines']}")
    print(f"  Best sigma: {results['best_sigma']}")
    print(f"  Time: {results['wall_time_seconds']}s")

    return results


def verify_candidate(notation: str, step_limit: int = 10**7) -> dict:
    """Independently verify a candidate by simulating from scratch."""
    tm = TuringMachine.from_compact(notation)
    steps, ones, tape, halted = tm.simulate(max_steps=step_limit)

    # Also verify with accelerated simulator
    if _C_AVAILABLE:
        atm = AcceleratedTuringMachine.from_compact(notation)
        a_steps, a_ones, a_halted, _ = atm.simulate_c(max_steps=step_limit)
        cross_check = (steps == a_steps and ones == a_ones and halted == a_halted)
    else:
        cross_check = True

    return {
        "notation": notation,
        "steps": steps,
        "sigma": ones,
        "halted": halted,
        "cross_check_passed": cross_check,
    }


def main():
    os.makedirs("results/search_campaigns", exist_ok=True)

    print("=" * 60)
    print("BB(6) SEARCH CAMPAIGN")
    print("=" * 60)

    campaign_start = time.time()
    all_results = {}

    # Run all strategies
    all_results["tnf_random"] = run_tnf_sample_search(num_machines=500000, step_limit=10**5, seed=42)
    all_results["mutation"] = run_mutation_campaign(step_limit=10**6, seed=42)
    all_results["breeding"] = run_breeding_campaign(step_limit=10**6, seed=42)
    all_results["guided"] = run_guided_campaign(num_machines=500000, step_limit=10**5, seed=42)

    # Collect all candidates
    all_candidates = []
    for strategy_name, results in all_results.items():
        for c in results.get("top_candidates", []):
            c["search_strategy"] = strategy_name
            all_candidates.append(c)

    # Deduplicate and sort
    seen = set()
    unique_candidates = []
    for c in sorted(all_candidates, key=lambda x: x.get("sigma", 0), reverse=True):
        if c["notation"] not in seen:
            seen.add(c["notation"])
            unique_candidates.append(c)

    # Verify top candidates
    print(f"\n{'=' * 60}")
    print(f"VERIFICATION")
    print(f"{'=' * 60}")

    verified = []
    for c in unique_candidates[:100]:
        v = verify_candidate(c["notation"])
        v["search_strategy"] = c.get("search_strategy", "unknown")
        verified.append(v)

    total_explored = sum(
        r.get("total_explored", r.get("num_machines", 0))
        for r in all_results.values()
    )
    total_time = time.time() - campaign_start

    # Save results
    campaign_summary = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "total_machines_explored": total_explored,
        "total_wall_time_seconds": round(total_time, 2),
        "strategies": {
            name: {
                "explored": r.get("total_explored", r.get("num_machines", 0)),
                "halting": r.get("total_halting", r.get("halting_count", 0)),
                "best_sigma": r.get("best_sigma", 0),
                "best_steps": r.get("best_steps", 0),
                "wall_time": r.get("wall_time_seconds", 0),
            }
            for name, r in all_results.items()
        },
        "verified_candidates": verified,
        "overall_best_sigma": verified[0]["sigma"] if verified else 0,
        "overall_best_steps": max((v["steps"] for v in verified), default=0),
    }

    with open("results/search_campaigns/campaign_summary.json", "w") as f:
        json.dump(campaign_summary, f, indent=2)

    # Save individual strategy results
    for name, results in all_results.items():
        with open(f"results/search_campaigns/{name}_results.json", "w") as f:
            json.dump(results, f, indent=2)

    # Save verified candidates
    with open("results/verified_candidates.json", "w") as f:
        json.dump(verified, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"CAMPAIGN COMPLETE")
    print(f"{'=' * 60}")
    print(f"Total machines explored: {total_explored}")
    print(f"Total wall time: {round(total_time, 1)}s")
    print(f"Best sigma found: {campaign_summary['overall_best_sigma']}")
    print(f"Best steps found: {campaign_summary['overall_best_steps']}")

    if verified:
        print(f"\nTop 10 verified candidates:")
        for v in verified[:10]:
            print(f"  {v['notation']}: sigma={v['sigma']}, steps={v['steps']} "
                  f"[{'HALT' if v['halted'] else 'TIMEOUT'}] "
                  f"({'cross-check OK' if v['cross_check_passed'] else 'MISMATCH'})")

    return campaign_summary


if __name__ == "__main__":
    main()
