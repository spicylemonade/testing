"""Mutation-based search: systematic perturbation of known high-scoring machines.

Takes known champion TMs as seeds and applies single/double transition mutations,
filters non-halting machines with deciders, and simulates remaining candidates.
"""

from __future__ import annotations

import json
import os
import random
import time
from typing import Dict, List, Tuple

from src.tm_simulator import TuringMachine, HALT_STATE
from src.tm_accelerated import AcceleratedTuringMachine, _C_AVAILABLE
from src.deciders import LoopDecider, CTLDecider


def all_single_mutations(notation: str) -> List[str]:
    """Generate all single-transition mutations of a TM.

    For a 6-state, 2-symbol TM with 12 transitions, each transition can be
    changed to any of (2 writes × 2 directions × 7 states) = 28 values.
    Total single mutations: 12 × 27 = 324 (excluding the original value).
    """
    tm = TuringMachine.from_compact(notation)
    state_names = tm.states
    n = tm.num_states
    all_states = state_names + [HALT_STATE]

    mutations = []
    for state in state_names:
        for sym in range(2):
            if sym not in tm.transitions.get(state, {}):
                continue
            orig_write, orig_dir, orig_next = tm.transitions[state][sym]
            for write in range(2):
                for direction in ["L", "R"]:
                    for next_state in all_states:
                        if (write, direction, next_state) == (orig_write, orig_dir, orig_next):
                            continue
                        # Create mutated TM
                        new_trans = {
                            s: dict(syms) for s, syms in tm.transitions.items()
                        }
                        new_trans[state][sym] = (write, direction, next_state)
                        mutant = TuringMachine(new_trans)
                        mutations.append(mutant.to_compact())

    return mutations


def mutation_search(
    seed_notations: List[str],
    step_limit: int = 10**6,
    double_mutations: bool = True,
    max_double: int = 5000,
    rng_seed: int = 42,
) -> Dict:
    """Run mutation search from seed machines.

    Args:
        seed_notations: List of compact notations for seed machines.
        step_limit: Max steps for simulation.
        double_mutations: Whether to do double mutations on promising singles.
        max_double: Max double mutations to try.
        rng_seed: Random seed.

    Returns:
        Results dict with candidates found.
    """
    rng = random.Random(rng_seed)
    loop_decider = LoopDecider(max_steps=5000)
    ctl_decider = CTLDecider(max_steps=5000)

    start_time = time.time()
    all_candidates = []
    total_explored = 0
    total_halting = 0
    total_filtered = 0
    seen = set()

    for seed_idx, seed_notation in enumerate(seed_notations):
        print(f"  Seed {seed_idx + 1}: {seed_notation[:30]}...")

        # Generate all single mutations
        singles = all_single_mutations(seed_notation)
        print(f"    Single mutations: {len(singles)}")

        promising_singles = []

        for notation in singles:
            if notation in seen:
                continue
            seen.add(notation)
            total_explored += 1

            # Quick filter with deciders
            tm = TuringMachine.from_compact(notation)

            # Check CTL first (faster)
            ctl_result = ctl_decider.decide(tm)
            if ctl_result == "non_halting":
                total_filtered += 1
                continue

            # Check loop decider
            loop_result = loop_decider.decide(tm)
            if loop_result == "non_halting":
                total_filtered += 1
                continue

            if loop_result == "halts" or ctl_result == "halts":
                # Known to halt — simulate to get score
                if _C_AVAILABLE:
                    atm = AcceleratedTuringMachine.from_compact(notation)
                    steps, ones, halted, _ = atm.simulate_c(max_steps=step_limit)
                else:
                    atm = AcceleratedTuringMachine.from_compact(notation)
                    steps, ones, halted, _ = atm.simulate(max_steps=step_limit)

                if halted:
                    total_halting += 1
                    all_candidates.append({
                        "notation": notation,
                        "steps": steps,
                        "sigma": ones,
                        "source": f"single_mutation_of_seed_{seed_idx}",
                    })
                    if ones > 100:
                        promising_singles.append(notation)
            else:
                # Unknown — simulate with step limit
                if _C_AVAILABLE:
                    atm = AcceleratedTuringMachine.from_compact(notation)
                    steps, ones, halted, _ = atm.simulate_c(max_steps=step_limit)
                else:
                    atm = AcceleratedTuringMachine.from_compact(notation)
                    steps, ones, halted, _ = atm.simulate(max_steps=step_limit)

                if halted:
                    total_halting += 1
                    all_candidates.append({
                        "notation": notation,
                        "steps": steps,
                        "sigma": ones,
                        "source": f"single_mutation_of_seed_{seed_idx}",
                    })
                    if ones > 100:
                        promising_singles.append(notation)

        print(f"    Promising singles: {len(promising_singles)}")

        # Double mutations on promising singles
        if double_mutations and promising_singles:
            double_count = 0
            for base in promising_singles:
                if double_count >= max_double:
                    break
                doubles = all_single_mutations(base)
                rng.shuffle(doubles)
                for notation in doubles[:50]:  # Sample from doubles
                    if notation in seen:
                        continue
                    seen.add(notation)
                    total_explored += 1
                    double_count += 1

                    if _C_AVAILABLE:
                        atm = AcceleratedTuringMachine.from_compact(notation)
                        steps, ones, halted, _ = atm.simulate_c(max_steps=step_limit)
                    else:
                        atm = AcceleratedTuringMachine.from_compact(notation)
                        steps, ones, halted, _ = atm.simulate(max_steps=step_limit)

                    if halted:
                        total_halting += 1
                        all_candidates.append({
                            "notation": notation,
                            "steps": steps,
                            "sigma": ones,
                            "source": f"double_mutation_of_seed_{seed_idx}",
                        })

            print(f"    Double mutations explored: {double_count}")

    elapsed = time.time() - start_time

    # Sort by sigma
    all_candidates.sort(key=lambda x: x["sigma"], reverse=True)

    return {
        "strategy": "mutation_search",
        "seed_count": len(seed_notations),
        "total_explored": total_explored,
        "total_halting": total_halting,
        "total_filtered_non_halting": total_filtered,
        "step_limit": step_limit,
        "wall_time_seconds": round(elapsed, 2),
        "best_sigma": all_candidates[0]["sigma"] if all_candidates else 0,
        "best_steps": max((c["steps"] for c in all_candidates), default=0),
        "top_candidates": all_candidates[:100],
    }


if __name__ == "__main__":
    # Seed machines: known BB(6) champions that are "normal" enough to mutate
    seeds = [
        "1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE",  # Kropitz t15
        "1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE",  # mxdys
        "1RB1LE_1RC1RF_1LD0RB_1RE1LA_0LA1RZ_1RC0RE",  # Kropitz e1B
    ]

    print("Running mutation search...")
    results = mutation_search(seeds, step_limit=10**6, rng_seed=42)

    print(f"\nResults:")
    print(f"  Total explored: {results['total_explored']}")
    print(f"  Halting machines: {results['total_halting']}")
    print(f"  Filtered non-halting: {results['total_filtered_non_halting']}")
    print(f"  Best sigma: {results['best_sigma']}")
    print(f"  Best steps: {results['best_steps']}")
    print(f"  Wall time: {results['wall_time_seconds']}s")

    if results['top_candidates']:
        print(f"\n  Top 10 candidates:")
        for c in results['top_candidates'][:10]:
            print(f"    {c['notation']}: sigma={c['sigma']}, steps={c['steps']}")

    os.makedirs("results/mutation_search", exist_ok=True)
    with open("results/mutation_search/results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to results/mutation_search/results.json")
