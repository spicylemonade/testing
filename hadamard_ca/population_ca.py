from __future__ import annotations

import math
from typing import Sequence

import numpy as np

from .orbit_ca import fallback_orbit_rank, orbit_representatives_for_state, rule_rank_index
from .retained_state_graph import RetainedStateGraph


def _softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits)
    weights = np.exp(shifted)
    return weights / np.sum(weights)


def _base_scores(
    representatives: Sequence[dict[str, object]],
    *,
    rule_index: dict[tuple[object, ...], int],
    current_score: int,
    length: int,
) -> np.ndarray:
    scores = np.zeros(len(representatives), dtype=np.float64)
    for index, entry in enumerate(representatives):
        signature = tuple(entry["orbit_signature"])
        rank = int(rule_index.get(signature, 10_000))
        fallback = fallback_orbit_rank(signature)
        gain = float(entry["signature"]["l1_gain"]) / float(max(1, int(length)))
        score_bonus = 0.25 if int(entry["objective"]["score"]) < int(current_score) else 0.0
        scores[index] = (
            -0.035 * float(min(rank, 60))
            -0.01 * float(sum(fallback))
            + 0.12 * gain
            + score_bonus
        )
    return scores


def _neighbor_masses(representatives: Sequence[dict[str, object]], memory: np.ndarray) -> np.ndarray:
    signature_to_index = {
        tuple(entry["orbit_signature"]): offset
        for offset, entry in enumerate(representatives)
    }
    masses = np.zeros(len(representatives), dtype=np.float64)
    for index, entry in enumerate(representatives):
        local = float(memory[index])
        for neighbor in entry["orbit_neighbor_signatures"]:
            neighbor_index = signature_to_index.get(tuple(neighbor))
            if neighbor_index is None:
                continue
            local += float(memory[neighbor_index])
        masses[index] = local
    return masses


def _sorted_objective_tuple(payload: dict[str, object]) -> tuple[int, int, int]:
    objective = payload["objective"]
    assert isinstance(objective, dict)
    return (
        int(objective["support_size"]),
        int(objective["l1"]),
        int(objective["max_abs"]),
    )


def run_population_self_stabilizing_ca(
    graph: RetainedStateGraph,
    *,
    start_state_id: int,
    lookup_budget: int,
    orbit_rule_table: Sequence[dict[str, object]],
    rng_seed: int,
    population_size: int = 64,
    coupling_strength: float = 1.6,
    temperature: float = 1.2,
    contraction_threshold: float = 0.42,
    memory_mix: float = 0.55,
    max_rounds_per_step: int = 6,
) -> dict[str, object]:
    rng = np.random.default_rng(int(rng_seed))
    rank_index = rule_rank_index(orbit_rule_table)
    current_state = int(start_state_id)
    best_state = int(start_state_id)
    lookups = 0
    trace: list[dict[str, object]] = []

    while True:
        representatives = orbit_representatives_for_state(graph, state_id=current_state, include_pairs=True)
        if not representatives:
            break
        current_score = int(graph.states[current_state].objective["score"])
        step_cost = len(representatives) * int(max_rounds_per_step)
        if lookups + step_cost > int(lookup_budget):
            break

        base_scores = _base_scores(
            representatives,
            rule_index=rank_index,
            current_score=current_score,
            length=graph.context.length,
        )
        memory = np.full(len(representatives), 1.0 / float(len(representatives)), dtype=np.float64)
        initial_entropy: float | None = None
        accepted = False

        for round_index in range(int(max_rounds_per_step)):
            lookups += len(representatives)
            neighbor_mass = _neighbor_masses(representatives, memory)
            logits = base_scores + float(coupling_strength) * neighbor_mass
            noise = rng.gumbel(0.0, float(temperature), size=len(representatives))
            probabilities = _softmax(logits + noise)
            votes = rng.choice(len(representatives), size=int(population_size), replace=True, p=probabilities)
            counts = np.bincount(votes, minlength=len(representatives)).astype(np.float64)
            vote_share = counts / float(max(1, int(population_size)))
            entropy = float(-np.sum(vote_share[vote_share > 0.0] * np.log(vote_share[vote_share > 0.0])))
            if initial_entropy is None:
                initial_entropy = entropy

            top_index = int(np.argmax(vote_share))
            top_share = float(vote_share[top_index])
            chosen = representatives[top_index]
            improving = int(chosen["objective"]["score"]) < current_score
            contraction = bool(
                top_share >= float(contraction_threshold)
                and entropy <= float(initial_entropy)
            )
            if improving and contraction:
                current_state = int(chosen["end_state_id"])
                if int(graph.states[current_state].objective["score"]) < int(graph.states[best_state].objective["score"]):
                    best_state = current_state
                trace.append(
                    {
                        "step": len(trace) + 1,
                        "round": round_index + 1,
                        "orbit_signature": list(chosen["orbit_signature"]),
                        "action_indices": list(chosen["action_indices"]),
                        "action_labels": list(chosen["action_labels"]),
                        "end_state_id": int(chosen["end_state_id"]),
                        "objective": dict(chosen["objective"]),
                        "top_share": top_share,
                        "entropy": entropy,
                        "phase": "contraction",
                        "raw_member_count": int(chosen["raw_member_count"]),
                        "lookups_after_step": int(lookups),
                    }
                )
                accepted = True
                break

            memory = float(memory_mix) * memory + (1.0 - float(memory_mix)) * vote_share

        if accepted:
            continue

        trace.append(
            {
                "step": len(trace) + 1,
                "round": int(max_rounds_per_step),
                "orbit_signature": None,
                "action_indices": [],
                "action_labels": [],
                "end_state_id": int(current_state),
                "objective": dict(graph.states[current_state].objective),
                "top_share": float(np.max(memory)) if memory.size else 0.0,
                "entropy": float(-np.sum(memory[memory > 0.0] * np.log(memory[memory > 0.0]))) if memory.size else 0.0,
                "phase": "diffusion",
                "raw_member_count": 0,
                "lookups_after_step": int(lookups),
            }
        )
        break

    return {
        "method_name": "population_self_stabilizing_ca",
        "lookup_budget": int(lookup_budget),
        "transition_lookups": int(lookups),
        "start_state": graph.state_payload(start_state_id),
        "end_state": graph.state_payload(current_state),
        "best_state": graph.state_payload(best_state),
        "trace": trace,
        "accepted_update_count": sum(1 for entry in trace if entry["phase"] == "contraction"),
            "mode": {
                "rng_seed": int(rng_seed),
                "population_size": int(population_size),
                "coupling_strength": float(coupling_strength),
                "temperature": float(temperature),
                "contraction_threshold": float(contraction_threshold),
                "memory_mix": float(memory_mix),
                "max_rounds_per_step": int(max_rounds_per_step),
            },
    }


def run_zero_coupling_population(
    graph: RetainedStateGraph,
    *,
    start_state_id: int,
    lookup_budget: int,
    orbit_rule_table: Sequence[dict[str, object]],
    rng_seed: int,
    population_size: int = 64,
    temperature: float = 1.2,
    contraction_threshold: float = 0.42,
    memory_mix: float = 0.55,
    max_rounds_per_step: int = 6,
) -> dict[str, object]:
    result = run_population_self_stabilizing_ca(
        graph,
        start_state_id=start_state_id,
        lookup_budget=lookup_budget,
        orbit_rule_table=orbit_rule_table,
        rng_seed=rng_seed,
        population_size=population_size,
        coupling_strength=0.0,
        temperature=temperature,
        contraction_threshold=contraction_threshold,
        memory_mix=memory_mix,
        max_rounds_per_step=max_rounds_per_step,
    )
    result["method_name"] = "zero_coupling_population"
    return result


def median_objective_payload(runs: Sequence[dict[str, object]]) -> dict[str, int]:
    ordered = sorted(
        (
            (
                int(run["best_state"]["objective"]["support_size"]),
                int(run["best_state"]["objective"]["l1"]),
                int(run["best_state"]["objective"]["max_abs"]),
                dict(run["best_state"]["objective"]),
            )
            for run in runs
        ),
        key=lambda row: (row[0], row[1], row[2]),
    )
    return ordered[len(ordered) // 2][3]


def phase_label(run: dict[str, object]) -> str:
    phases = [entry["phase"] for entry in run["trace"]]
    if any(phase == "contraction" for phase in phases):
        return "contraction"
    return "diffusion"
