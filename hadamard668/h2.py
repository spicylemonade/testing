from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Dict, List, Mapping, Sequence, Tuple

from hadamard668.verifiers import (
    modular_metrics_from_combined,
    modular_objective,
    modular_objective_value,
    structured_qs_state,
)


@dataclass(frozen=True)
class StructuredQSInstance:
    label: str
    q: List[int]
    s: List[int]
    target_modulus: int | None
    control_mode: str


def line_phases(length: int) -> List[List[int]]:
    return [
        list(range(0, length, 2)),
        list(range(1, length, 2)),
    ]


def flip_positions(which: str) -> Tuple[str, ...]:
    if which == "s":
        return ("A", "B", "C", "D")
    if which == "q":
        return ("C", "D")
    raise ValueError(f"unknown variable family: {which}")


def operation_delta(
    sequences: Mapping[str, Sequence[int]],
    which: str,
    index: int,
) -> List[int]:
    labels = flip_positions(which)
    length = len(next(iter(sequences.values())))
    delta: List[int] = []
    for shift in range(1, length):
        change = 0
        for label in labels:
            sequence = sequences[label]
            old_value = int(sequence[index])
            if index + shift < length:
                change += ((-old_value) * int(sequence[index + shift])) - (
                    old_value * int(sequence[index + shift])
                )
            if index - shift >= 0:
                change += (int(sequence[index - shift]) * (-old_value)) - (
                    int(sequence[index - shift]) * old_value
                )
        delta.append(change)
    return delta


def apply_operation(
    q: Sequence[int],
    s: Sequence[int],
    which: str,
    index: int,
) -> tuple[List[int], List[int]]:
    next_q = [int(value) for value in q]
    next_s = [int(value) for value in s]
    if which == "s":
        next_s[index] *= -1
    elif which == "q":
        next_q[index] *= -1
    else:
        raise ValueError(f"unknown variable family: {which}")
    return next_q, next_s


def candidate_operations(
    state: Mapping[str, object],
    which: str,
    indices: Sequence[int],
) -> List[Dict[str, object]]:
    combined = [int(value) for value in state["combined_aperiodic_pm1_autocorrelation"]]
    current_value = modular_objective_value(state)
    sequences = state["sequences"]
    target_modulus = state["target_modulus"]
    candidates: List[Dict[str, object]] = []
    for index in indices:
        delta = operation_delta(sequences, which, index)
        next_combined = [value + change for value, change in zip(combined, delta)]
        next_metrics = modular_metrics_from_combined(next_combined, target_modulus=target_modulus)
        next_value = modular_objective_value(next_metrics)
        candidates.append(
            {
                "which": which,
                "index": index,
                "gain": current_value - next_value,
                "next_metrics": next_metrics,
            }
        )
    return candidates


def select_local_dominant(
    candidates: Sequence[Dict[str, object]],
    window: int,
    min_gain: int,
) -> List[Dict[str, object]]:
    if not candidates:
        return []
    gains = [int(candidate["gain"]) for candidate in candidates]
    selected: List[Dict[str, object]] = []
    for offset, candidate in enumerate(candidates):
        gain = gains[offset]
        if gain < min_gain:
            continue
        lower = max(0, offset - window)
        upper = min(len(candidates), offset + window + 1)
        if all(gain >= gains[item] for item in range(lower, upper)) and any(
            gain > gains[item]
            for item in range(lower, upper)
            if item != offset
        ):
            selected.append(dict(candidate))
    return selected


def snapshot(step: int, state: Mapping[str, object]) -> Dict[str, object]:
    return {
        "step": step,
        "quality_rank": int(state["quality_rank"]),
        "two_adic_modulus": int(state["two_adic_modulus"]),
        "defect_count": int(state["defect_count"]),
        "max_defect_magnitude": int(state["max_defect_magnitude"]),
        "l1_defect": int(state["l1_defect"]),
        "exact_certificate": bool(state["exact_certificate"]),
    }


def run_structured_qs_search(
    instance: StructuredQSInstance,
    start_q: Sequence[int],
    start_s: Sequence[int],
    method: str,
    variable_family: str,
    steps: int,
    method_params: Mapping[str, object],
    seed_family: str,
    seed_value: int,
) -> Dict[str, object]:
    start = time.perf_counter()
    q = [int(value) for value in start_q]
    s = [int(value) for value in start_s]
    state = structured_qs_state(q, s, target_modulus=instance.target_modulus)
    best_state = dict(state)
    best_step = 0
    goal_hit = (
        bool(state["exact_certificate"])
        if instance.control_mode == "exact-repair"
        else bool(state["target_modulus_met"])
    )
    exact_hit_step = 0 if goal_hit else None
    snapshots = [snapshot(0, state)]
    seen_orbits = {str(state["canonical_orbit"])}
    phases = line_phases(len(s))
    variable_evaluations = 0
    accepted_moves = 0
    rng = random.Random(int(seed_value))
    phase_move_cap = int(method_params.get("phase_move_cap", 4))
    for step in range(1, steps + 1):
        indices = phases[(step - 1) % len(phases)]
        variable_evaluations += len(indices)
        candidates = candidate_operations(state, variable_family, indices)
        selected: List[Dict[str, object]] = []
        if method == "parallel_gain_ca":
            selected = select_local_dominant(
                candidates,
                window=int(method_params.get("window", 1)),
                min_gain=int(method_params.get("min_gain", 100)),
            )
            selected = sorted(
                selected,
                key=lambda item: (
                    -int(item["gain"]),
                    int(item["index"]),
                ),
            )[:phase_move_cap]
        elif method == "direct_greedy":
            improving = [candidate for candidate in candidates if int(candidate["gain"]) > 0]
            if improving:
                selected = sorted(
                    improving,
                    key=lambda item: (
                        -int(item["gain"]),
                        int(item["index"]),
                    ),
                )[:phase_move_cap]
        elif method == "random_rule_ca":
            fire_probability = float(method_params.get("fire_probability", 0.25))
            shuffled = list(candidates)
            rng.shuffle(shuffled)
            selected = [
                dict(candidate)
                for candidate in shuffled
                if rng.random() < fire_probability
            ][:phase_move_cap]
        elif method == "random_walk":
            if candidates:
                selected = [dict(rng.choice(candidates))]
        else:
            raise ValueError(f"unknown structured-q/s method: {method}")
        if selected:
            for candidate in selected:
                q, s = apply_operation(q, s, variable_family, int(candidate["index"]))
            accepted_moves += len(selected)
            state = structured_qs_state(q, s, target_modulus=instance.target_modulus)
        seen_orbits.add(str(state["canonical_orbit"]))
        if modular_objective(state) < modular_objective(best_state):
            best_state = dict(state)
            best_step = step
        goal_hit = (
            bool(state["exact_certificate"])
            if instance.control_mode == "exact-repair"
            else bool(state["target_modulus_met"])
        )
        if exact_hit_step is None and goal_hit:
            exact_hit_step = step
        if step == steps or step % int(method_params.get("snapshot_every", 8)) == 0:
            snapshots.append(snapshot(step, state))
    elapsed = time.perf_counter() - start
    final_goal_hit = (
        bool(best_state["exact_certificate"])
        if instance.control_mode == "exact-repair"
        else bool(best_state["target_modulus_met"])
    )
    return {
        "branch": "H2",
        "instance_label": instance.label,
        "control_mode": instance.control_mode,
        "method": method,
        "variable_family": variable_family,
        "method_params": dict(method_params),
        "seed_family": seed_family,
        "deterministic_seed": int(seed_value),
        "budget_steps": steps,
        "matching_schedule": "line-2-phase",
        "variable_evaluations": variable_evaluations,
        "accepted_moves": accepted_moves,
        "visited_states": steps + 1,
        "unique_orbits": len(seen_orbits),
        "orbit_collapse_ratio": len(seen_orbits) / float(steps + 1),
        "best_state": best_state,
        "best_step": best_step,
        "final_state": state,
        "exact_hit": bool(best_state["exact_certificate"]),
        "goal_hit": final_goal_hit,
        "exact_hit_step": exact_hit_step,
        "goal_hit_step": exact_hit_step,
        "elapsed_seconds": elapsed,
        "snapshots": snapshots,
    }
