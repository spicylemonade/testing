from __future__ import annotations

from collections import defaultdict
from statistics import median
from typing import Iterable, Sequence

from .lag_lattice_gas import (
    lattice_gas_rank,
    orbit_signature_for_event,
    pair_candidates_from_state,
    single_candidates_from_state,
)
from .retained_state_graph import RetainedStateGraph


OrbitSignature = tuple[object, ...]


def orbit_representatives_for_state(
    graph: RetainedStateGraph,
    *,
    state_id: int,
    include_pairs: bool = True,
) -> list[dict[str, object]]:
    candidates = single_candidates_from_state(graph, state_id=state_id)
    if include_pairs:
        candidates.extend(pair_candidates_from_state(graph, state_id=state_id))

    grouped: dict[OrbitSignature, list[dict[str, object]]] = defaultdict(list)
    for candidate in candidates:
        signature = orbit_signature_for_event(candidate, length=graph.context.length)
        enriched = dict(candidate)
        enriched["orbit_signature"] = signature
        grouped[signature].append(enriched)

    representatives: list[dict[str, object]] = []
    changed_sets = {
        signature: set(int(lag) for lag in members[0]["signature"]["changed_lags"])
        for signature, members in grouped.items()
    }
    ordered_signatures = sorted(grouped)
    for signature in ordered_signatures:
        members = grouped[signature]
        representative = min(members, key=lambda candidate: tuple(int(value) for value in candidate["action_indices"]))
        representative = dict(representative)
        representative["raw_member_count"] = len(members)
        representative["orbit_neighbor_signatures"] = [
            neighbor
            for neighbor in ordered_signatures
            if neighbor != signature and changed_sets[signature] & changed_sets[neighbor]
        ]
        representatives.append(representative)
    return representatives


def aggregate_training_entries(training_entries: Sequence[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[OrbitSignature, list[dict[str, object]]] = defaultdict(list)
    for entry in training_entries:
        grouped[tuple(entry["orbit_signature"])].append(entry)

    rules: list[dict[str, object]] = []
    for signature, entries in grouped.items():
        objective_tuples = [
            (
                int(entry["objective"]["support_size"]),
                int(entry["objective"]["l1"]),
                int(entry["objective"]["max_abs"]),
            )
            for entry in entries
        ]
        reservoirs = [int(entry["signature"]["reservoir_abs"]) for entry in entries]
        transport_densities = [
            float(entry["signature"]["transport_span"]) / float(max(1, int(entry["length"])))
            for entry in entries
        ]
        l1_gains = [int(entry["signature"]["l1_gain"]) for entry in entries]
        max_gains = [int(entry["signature"]["max_gain"]) for entry in entries]
        rules.append(
            {
                "orbit_signature": list(signature),
                "count": len(entries),
                "median_objective": {
                    "support_size": int(median(value[0] for value in objective_tuples)),
                    "l1": int(median(value[1] for value in objective_tuples)),
                    "max_abs": int(median(value[2] for value in objective_tuples)),
                },
                "median_reservoir_abs": float(median(reservoirs)),
                "median_transport_density": float(median(transport_densities)),
                "median_l1_gain": float(median(l1_gains)),
                "median_max_gain": float(median(max_gains)),
            }
        )

    kind_order = {
        "annihilation": 0,
        "move_annihilate": 1,
        "split_annihilate": 2,
        "move": 3,
        "split": 4,
    }
    support_order = {
        "decrease": 0,
        "conserve": 1,
        "increase": 2,
    }
    changed_order = {
        "1": 0,
        "2": 1,
        "3_4": 2,
        "5_8": 3,
        "9_plus": 4,
    }
    transport_order = {
        "tight": 0,
        "mid": 1,
        "wide": 2,
    }
    rules.sort(
        key=lambda rule: (
            kind_order.get(str(rule["orbit_signature"][0]), 99),
            support_order.get(str(rule["orbit_signature"][2]), 99),
            int(rule["median_objective"]["support_size"]),
            int(rule["median_objective"]["l1"]),
            int(rule["median_objective"]["max_abs"]),
            changed_order.get(str(rule["orbit_signature"][3]), 99),
            transport_order.get(str(rule["orbit_signature"][4]), 99),
            int(rule["orbit_signature"][5]),
            float(rule["median_reservoir_abs"]),
            -float(rule["median_l1_gain"]),
            -int(rule["count"]),
            tuple(str(value) for value in rule["orbit_signature"]),
        )
    )
    for priority_rank, rule in enumerate(rules):
        rule["priority_rank"] = int(priority_rank)
    return rules


def rule_rank_index(rule_table: Sequence[dict[str, object]]) -> dict[OrbitSignature, int]:
    return {
        tuple(rule["orbit_signature"]): int(rule["priority_rank"])
        for rule in rule_table
    }


def fallback_orbit_rank(signature: OrbitSignature) -> tuple[int, int, int, int, int, int]:
    kind_order = {
        "annihilation": 0,
        "move_annihilate": 1,
        "split_annihilate": 2,
        "move": 3,
        "split": 4,
    }
    support_order = {
        "decrease": 0,
        "conserve": 1,
        "increase": 2,
    }
    changed_order = {
        "1": 0,
        "2": 1,
        "3_4": 2,
        "5_8": 3,
        "9_plus": 4,
    }
    transport_order = {
        "tight": 0,
        "mid": 1,
        "wide": 2,
    }
    return (
        kind_order.get(str(signature[0]), 99),
        int(signature[1]),
        support_order.get(str(signature[2]), 99),
        changed_order.get(str(signature[3]), 99),
        transport_order.get(str(signature[4]), 99),
        int(signature[5]),
    )


def run_orbit_quotient_ca(
    graph: RetainedStateGraph,
    *,
    start_state_id: int,
    lookup_budget: int,
    orbit_rule_table: Sequence[dict[str, object]],
) -> dict[str, object]:
    current_state = int(start_state_id)
    best_state = int(start_state_id)
    lookups = 0
    trace: list[dict[str, object]] = []
    rank_index = rule_rank_index(orbit_rule_table)

    while True:
        representatives = orbit_representatives_for_state(graph, state_id=current_state, include_pairs=True)
        step_cost = sum(int(entry["action_count"]) for entry in representatives)
        if not representatives or lookups + step_cost > int(lookup_budget):
            break
        lookups += step_cost
        current_score = int(graph.states[current_state].objective["score"])
        improving = [
            entry
            for entry in representatives
            if int(entry["objective"]["score"]) < current_score
        ]
        if not improving:
            break
        chosen = min(
            improving,
            key=lambda entry: (
                rank_index.get(tuple(entry["orbit_signature"]), 10_000),
                fallback_orbit_rank(tuple(entry["orbit_signature"])),
                lattice_gas_rank(entry),
            ),
        )
        current_state = int(chosen["end_state_id"])
        if int(graph.states[current_state].objective["score"]) < int(graph.states[best_state].objective["score"]):
            best_state = current_state
        trace.append(
            {
                "step": len(trace) + 1,
                "orbit_signature": list(chosen["orbit_signature"]),
                "rule_priority": int(rank_index.get(tuple(chosen["orbit_signature"]), 10_000)),
                "action_indices": list(chosen["action_indices"]),
                "action_labels": list(chosen["action_labels"]),
                "end_state_id": int(chosen["end_state_id"]),
                "objective": dict(chosen["objective"]),
                "signature": dict(chosen["signature"]),
                "raw_member_count": int(chosen["raw_member_count"]),
                "orbit_neighbor_signatures": [list(value) for value in chosen["orbit_neighbor_signatures"]],
                "lookups_after_step": int(lookups),
            }
        )

    return {
        "method_name": "orbit_quotient_ca",
        "lookup_budget": int(lookup_budget),
        "transition_lookups": int(lookups),
        "start_state": graph.state_payload(start_state_id),
        "end_state": graph.state_payload(current_state),
        "best_state": graph.state_payload(best_state),
        "trace": trace,
        "accepted_update_count": len(trace),
        "mode": {
            "candidate_set": "orbit_representatives_of_single_actions_and_two_step_carriers",
            "rule_table_size": len(orbit_rule_table),
        },
    }


def collect_training_representatives(
    graph: RetainedStateGraph,
    *,
    state_ids: Iterable[int],
) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for state_id in state_ids:
        current_score = int(graph.states[int(state_id)].objective["score"])
        for entry in orbit_representatives_for_state(graph, state_id=int(state_id), include_pairs=True):
            if int(entry["objective"]["score"]) >= current_score:
                continue
            enriched = dict(entry)
            enriched["length"] = int(graph.context.length)
            entries.append(enriched)
    return entries
