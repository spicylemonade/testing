"""Guided search strategy using structural features of champion machines.

Analyzes transition graph topology, counter patterns, and state connectivity
of known high-scoring machines to bias enumeration toward promising regions.

References:
    - Ligocki 2022: Shift Overflow Counters
    - Doucette: SOC pattern identification
"""

from __future__ import annotations

import json
import os
import random
from collections import defaultdict
from typing import Dict, List, Set, Tuple

from src.tm_simulator import TuringMachine, HALT_STATE


def extract_features(notation: str) -> Dict:
    """Extract structural features from a TM's transition table.

    Features include:
    - Transition graph properties (connectivity, in/out degree)
    - Symbol writing patterns (balance of 0s vs 1s)
    - Direction patterns (balance of L vs R moves)
    - Self-loop count
    - Halt reachability (which states can reach halt)
    """
    tm = TuringMachine.from_compact(notation)
    n = tm.num_states

    # Build state transition graph
    edges = []
    self_loops = 0
    write_ones = 0
    write_zeros = 0
    move_right = 0
    move_left = 0
    halt_transitions = 0

    for state, syms in tm.transitions.items():
        for sym, (write, direction, next_state) in syms.items():
            if next_state == HALT_STATE:
                halt_transitions += 1
            else:
                edges.append((state, next_state))
                if state == next_state:
                    self_loops += 1

            if write == 1:
                write_ones += 1
            else:
                write_zeros += 1

            if direction == "R":
                move_right += 1
            else:
                move_left += 1

    total_transitions = write_ones + write_zeros

    # Graph connectivity
    adjacency = defaultdict(set)
    for src, dst in edges:
        adjacency[src].add(dst)

    # Reachable states from A
    reachable = set()
    queue = ["A"]
    while queue:
        state = queue.pop()
        if state in reachable:
            continue
        reachable.add(state)
        for next_s in adjacency.get(state, set()):
            if next_s not in reachable:
                queue.append(next_s)

    # In-degree and out-degree
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    for src, dst in edges:
        out_degree[src] += 1
        in_degree[dst] += 1

    return {
        "notation": notation,
        "num_states": n,
        "num_transitions": total_transitions,
        "self_loops": self_loops,
        "halt_transitions": halt_transitions,
        "write_ratio": write_ones / max(total_transitions, 1),
        "direction_ratio": move_right / max(total_transitions, 1),
        "reachable_states": len(reachable),
        "all_states_reachable": len(reachable) == n,
        "max_in_degree": max(in_degree.values()) if in_degree else 0,
        "max_out_degree": max(out_degree.values()) if out_degree else 0,
        "avg_in_degree": sum(in_degree.values()) / max(len(in_degree), 1),
        "graph_density": len(edges) / max(n * n, 1),
    }


def feature_similarity_score(features: Dict, target_features: Dict) -> float:
    """Score how similar a machine's features are to a target (champion) profile.

    Returns a score in [0, 1] where 1 = perfect match.
    """
    score = 0.0
    weights = {
        "write_ratio": 2.0,
        "direction_ratio": 1.0,
        "self_loops": 1.5,
        "halt_transitions": 2.0,
        "all_states_reachable": 3.0,
        "graph_density": 1.0,
    }

    for key, weight in weights.items():
        if key in features and key in target_features:
            if isinstance(features[key], bool):
                score += weight * (1.0 if features[key] == target_features[key] else 0.0)
            else:
                diff = abs(features[key] - target_features[key])
                max_val = max(abs(features[key]), abs(target_features[key]), 1e-10)
                score += weight * max(0, 1.0 - diff / max_val)

    total_weight = sum(weights.values())
    return score / total_weight


def generate_biased_machine(
    num_states: int,
    target_features: Dict,
    rng: random.Random,
) -> str:
    """Generate a random TM biased toward target feature profile.

    Uses the target features to set probabilities for:
    - Write symbol (biased toward target write_ratio)
    - Direction (biased toward target direction_ratio)
    - Self-loops vs new states
    - Number of halt transitions
    """
    state_names = [chr(ord("A") + i) for i in range(num_states)]
    write_prob = target_features.get("write_ratio", 0.5)
    right_prob = target_features.get("direction_ratio", 0.5)
    self_loop_rate = target_features.get("self_loops", 2) / max(num_states * 2, 1)
    halt_target = target_features.get("halt_transitions", 1)

    transitions = {}
    halt_placed = 0

    # First transition fixed: A,0 -> 1,R,B
    transitions["A"] = {0: (1, "R", "B")}

    # Fill remaining transitions
    for si, state in enumerate(state_names):
        if state not in transitions:
            transitions[state] = {}
        for sym in range(2):
            if sym in transitions[state]:
                continue

            # Write symbol
            write = 1 if rng.random() < write_prob else 0
            # Direction
            direction = "R" if rng.random() < right_prob else "L"

            # Next state
            if halt_placed < halt_target and rng.random() < halt_target / (num_states * 2 - 1):
                next_state = HALT_STATE
                halt_placed += 1
            elif rng.random() < self_loop_rate:
                next_state = state
            else:
                next_state = rng.choice(state_names)

            transitions[state][sym] = (write, direction, next_state)

    # Ensure at least one halt transition
    if halt_placed == 0:
        # Pick a random non-first transition and make it halt
        candidates = [
            (s, sym)
            for s in state_names
            for sym in range(2)
            if not (s == "A" and sym == 0)
        ]
        s, sym = rng.choice(candidates)
        write, direction, _ = transitions[s][sym]
        transitions[s][sym] = (write, direction, HALT_STATE)

    # Convert to compact notation
    tm = TuringMachine(transitions)
    return tm.to_compact()


def guided_search(
    num_machines: int = 10000,
    step_limit: int = 10**6,
    seed: int = 42,
) -> Dict:
    """Run guided search biased by champion features.

    Returns results dict with top candidates.
    """
    rng = random.Random(seed)

    # Extract features from known champions
    champion_notations = [
        "1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE",  # Kropitz t15
        "1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE",  # mxdys
    ]

    target_features = {}
    for notation in champion_notations:
        features = extract_features(notation)
        for key, val in features.items():
            if isinstance(val, (int, float)):
                if key not in target_features:
                    target_features[key] = []
                target_features[key].append(val)

    # Average the target features
    avg_features = {k: sum(v) / len(v) for k, v in target_features.items()}

    # Import accelerated simulator
    from src.tm_accelerated import AcceleratedTuringMachine, _C_AVAILABLE

    results = []
    halting_count = 0
    best_sigma = 0
    best_steps = 0

    for i in range(num_machines):
        notation = generate_biased_machine(6, avg_features, rng)

        if _C_AVAILABLE:
            tm = AcceleratedTuringMachine.from_compact(notation)
            steps, ones, halted, _ = tm.simulate_c(max_steps=step_limit)
        else:
            tm = AcceleratedTuringMachine.from_compact(notation)
            steps, ones, halted, _ = tm.simulate(max_steps=step_limit)

        if halted:
            halting_count += 1
            if ones > best_sigma:
                best_sigma = ones
            if steps > best_steps:
                best_steps = steps
            if ones > 100 or steps > 10000:
                features = extract_features(notation)
                results.append({
                    "notation": notation,
                    "steps": steps,
                    "sigma": ones,
                    "features": features,
                })

    # Sort by sigma score
    results.sort(key=lambda x: x["sigma"], reverse=True)

    return {
        "strategy": "guided_search",
        "num_machines": num_machines,
        "step_limit": step_limit,
        "seed": seed,
        "halting_count": halting_count,
        "halting_rate": halting_count / max(num_machines, 1),
        "best_sigma": best_sigma,
        "best_steps": best_steps,
        "top_candidates": results[:100],
        "champion_features": avg_features,
    }


if __name__ == "__main__":
    print("Running guided search (10,000 machines)...")
    results = guided_search(num_machines=10000, step_limit=10**6, seed=42)

    print(f"  Halting machines: {results['halting_count']}/{results['num_machines']} ({results['halting_rate']:.1%})")
    print(f"  Best sigma: {results['best_sigma']}")
    print(f"  Best steps: {results['best_steps']}")
    print(f"  Interesting candidates: {len(results['top_candidates'])}")

    if results['top_candidates']:
        print(f"\n  Top 5 candidates:")
        for c in results['top_candidates'][:5]:
            print(f"    {c['notation']}: sigma={c['sigma']}, steps={c['steps']}")

    os.makedirs("results", exist_ok=True)
    with open("results/feature_analysis.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to results/feature_analysis.json")
