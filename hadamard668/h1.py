from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from hadamard668.core import bits_from_support, l1_distance
from hadamard668.verifiers import support_objective, support_state


@dataclass(frozen=True)
class SupportInstance:
    label: str
    length: int
    weight: int
    target: List[int]


def support_instance_from_artifact(artifact: Mapping[str, object]) -> SupportInstance:
    if "solution" in artifact:
        weight = int(artifact["solution"]["weight"])
    else:
        weight = int(artifact["unknown_vector"]["required_weight"])
    return SupportInstance(
        label=str(artifact["label"]),
        length=int(artifact["length"]),
        weight=weight,
        target=[int(value) for value in artifact["target_periodic_autocorrelation_half"]],
    )


def cycle_matchings(length: int) -> List[List[Tuple[int, int]]]:
    if length % 2 == 0:
        return [
            [(idx, idx + 1) for idx in range(0, length - 1, 2)] + [(length - 1, 0)],
            [(idx, idx + 1) for idx in range(1, length - 1, 2)],
        ]
    return [
        [(idx, idx + 1) for idx in range(0, length - 1, 2)],
        [(idx, idx + 1) for idx in range(1, length - 1, 2)],
        [(length - 1, 0)],
    ]


def apply_swaps(bits: Sequence[int], edges: Iterable[Tuple[int, int]]) -> List[int]:
    updated = [int(value) for value in bits]
    for left, right in edges:
        updated[left], updated[right] = updated[right], updated[left]
    return updated


def swap_delta_half(bits: Sequence[int], edge: Tuple[int, int]) -> List[int]:
    left, right = edge
    if bits[left] == bits[right]:
        return [0] * (len(bits) // 2)
    swapped = {
        left: int(bits[right]),
        right: int(bits[left]),
    }
    length = len(bits)
    half = length // 2
    delta: List[int] = []
    for shift in range(1, half + 1):
        starts = {left, right, (left - shift) % length, (right - shift) % length}
        change = 0
        for start in starts:
            end = (start + shift) % length
            old_left = int(bits[start])
            old_right = int(bits[end])
            new_left = swapped.get(start, old_left)
            new_right = swapped.get(end, old_right)
            change += (new_left * new_right) - (old_left * old_right)
        delta.append(change)
    return delta


def candidate_swaps(
    bits: Sequence[int],
    corr: Sequence[int],
    target: Sequence[int],
    edges: Sequence[Tuple[int, int]],
) -> List[Dict[str, object]]:
    current_distance = l1_distance(corr, target)
    candidates: List[Dict[str, object]] = []
    for edge in edges:
        left, right = edge
        if bits[left] == bits[right]:
            continue
        delta = swap_delta_half(bits, edge)
        next_corr = [int(value) + change for value, change in zip(corr, delta)]
        next_distance = l1_distance(next_corr, target)
        candidates.append(
            {
                "edge": edge,
                "gain": current_distance - next_distance,
                "next_distance": next_distance,
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
    for index, candidate in enumerate(candidates):
        gain = gains[index]
        if gain < min_gain:
            continue
        lower = max(0, index - window)
        upper = min(len(candidates), index + window + 1)
        if all(gain >= gains[offset] for offset in range(lower, upper)) and any(
            gain > gains[offset]
            for offset in range(lower, upper)
            if offset != index
        ):
            selected.append(dict(candidate))
    return selected


def random_support_seed(length: int, weight: int, seed: int) -> Dict[str, object]:
    rng = random.Random(seed)
    support = rng.sample(range(length), weight)
    return {
        "seed_family": "random_weight",
        "seed_value": seed,
        "bits": bits_from_support(length, support),
    }


def perturbed_solution_seed(
    solution_support: Sequence[int],
    length: int,
    perturb_swaps: int,
    seed: int,
) -> Dict[str, object]:
    rng = random.Random(seed)
    bits = bits_from_support(length, solution_support)
    applied = 0
    while applied < perturb_swaps:
        edge = rng.randrange(length)
        neighbour = (edge + 1) % length
        if bits[edge] == bits[neighbour]:
            continue
        bits[edge], bits[neighbour] = bits[neighbour], bits[edge]
        applied += 1
    return {
        "seed_family": "perturbed_solution",
        "seed_value": seed,
        "perturb_swaps": perturb_swaps,
        "bits": bits,
    }


def projected_pm1_seed(
    sequence: Sequence[int],
    weight: int,
    shift: int,
) -> Dict[str, object]:
    length = len(sequence)
    shifted = [int(sequence[(idx - shift) % length]) for idx in range(length)]
    positives = [idx for idx, value in enumerate(shifted) if value > 0]
    negatives = [idx for idx, value in enumerate(shifted) if value < 0]
    if len(positives) > weight:
        trimmed = list(positives)
        while len(trimmed) > weight:
            drop = min(len(trimmed) - 1, len(trimmed) // 2)
            trimmed.pop(drop)
        positives = trimmed
    elif len(positives) < weight:
        positives = positives + negatives[: weight - len(positives)]
    bits = bits_from_support(length, positives[:weight])
    return {
        "seed_family": "modular_projection",
        "seed_value": shift,
        "bits": bits,
    }


def snapshot(step: int, state: Mapping[str, object]) -> Dict[str, object]:
    return {
        "step": step,
        "closest_target_distance": int(state["closest_target_distance"]),
        "max_defect_magnitude": int(state["max_defect_magnitude"]),
        "exact_hit": bool(state["exact_hit"]),
    }


def run_support_search(
    instance: SupportInstance,
    start_bits: Sequence[int],
    method: str,
    steps: int,
    method_params: Mapping[str, object],
    seed_family: str,
    seed_value: int,
) -> Dict[str, object]:
    start = time.perf_counter()
    bits = [int(value) for value in start_bits]
    state = support_state(bits, instance.target)
    best_state = dict(state)
    best_step = 0
    exact_hit_step = 0 if bool(state["exact_hit"]) else None
    snapshots = [snapshot(0, state)]
    seen_orbits = {str(state["canonical_orbit"])}
    matchings = cycle_matchings(instance.length)
    edge_evaluations = 0
    accepted_moves = 0
    rng = random.Random(int(seed_value))
    phase_move_cap = int(method_params.get("phase_move_cap", 4))
    for step in range(1, steps + 1):
        edges = matchings[(step - 1) % len(matchings)]
        edge_evaluations += len(edges)
        corr = [int(value) for value in state["periodic_autocorrelation_half"]]
        candidates = candidate_swaps(bits, corr, instance.target, edges)
        selected_edges: List[Tuple[int, int]] = []
        if method == "parallel_gain_ca":
            chosen = select_local_dominant(
                candidates,
                window=int(method_params.get("window", 2)),
                min_gain=int(method_params.get("min_gain", 6)),
            )
            chosen = sorted(
                chosen,
                key=lambda item: (
                    -int(item["gain"]),
                    int(item["next_distance"]),
                    tuple(item["edge"]),
                ),
            )
            selected_edges = [tuple(candidate["edge"]) for candidate in chosen[:phase_move_cap]]
        elif method == "direct_greedy":
            improving = [candidate for candidate in candidates if int(candidate["gain"]) > 0]
            if improving:
                improving = sorted(
                    improving,
                    key=lambda item: (
                        -int(item["gain"]),
                        int(item["next_distance"]),
                        tuple(item["edge"]),
                    ),
                )
                selected_edges = [tuple(candidate["edge"]) for candidate in improving[:phase_move_cap]]
        elif method == "random_rule_ca":
            fire_probability = float(method_params.get("fire_probability", 0.25))
            shuffled = list(candidates)
            rng.shuffle(shuffled)
            for candidate in shuffled:
                if rng.random() < fire_probability:
                    selected_edges.append(tuple(candidate["edge"]))
                if len(selected_edges) >= phase_move_cap:
                    break
        elif method == "random_walk":
            admissible = [tuple(candidate["edge"]) for candidate in candidates]
            if admissible:
                selected_edges = [rng.choice(admissible)]
        else:
            raise ValueError(f"unknown support-search method: {method}")
        if selected_edges:
            bits = apply_swaps(bits, selected_edges)
            accepted_moves += len(selected_edges)
            state = support_state(bits, instance.target)
        seen_orbits.add(str(state["canonical_orbit"]))
        if support_objective(state) < support_objective(best_state):
            best_state = dict(state)
            best_step = step
        if exact_hit_step is None and bool(state["exact_hit"]):
            exact_hit_step = step
        if step == steps or step % int(method_params.get("snapshot_every", 12)) == 0:
            snapshots.append(snapshot(step, state))
    elapsed = time.perf_counter() - start
    return {
        "branch": "H1",
        "instance_label": instance.label,
        "method": method,
        "method_params": dict(method_params),
        "seed_family": seed_family,
        "deterministic_seed": int(seed_value),
        "budget_steps": steps,
        "matching_schedule": "odd-cycle-3-matching" if instance.length % 2 else "even-cycle-2-matching",
        "edge_evaluations": edge_evaluations,
        "accepted_moves": accepted_moves,
        "visited_states": steps + 1,
        "unique_orbits": len(seen_orbits),
        "orbit_collapse_ratio": len(seen_orbits) / float(steps + 1),
        "best_state": best_state,
        "best_step": best_step,
        "final_state": state,
        "exact_hit": bool(best_state["exact_hit"]),
        "exact_hit_step": exact_hit_step,
        "elapsed_seconds": elapsed,
        "snapshots": snapshots,
    }
