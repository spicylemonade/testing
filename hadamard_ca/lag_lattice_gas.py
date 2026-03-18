from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations
from typing import Callable, Sequence

import numpy as np

from .composite import CompositeAction, CompositeContext, enumerate_single_packets
from .harness import derived_quadruple
from .retained_state_graph import RetainedStateGraph
from .seed import prime_involution


@dataclass(frozen=True)
class TransportSignature:
    support_flux: int
    l1_gain: int
    max_gain: int
    danger_reduction: int
    reservoir_exchange: int
    reservoir_abs: int
    transport_span: int
    transport_peak: int
    positive_mass: int
    negative_mass: int
    changed_lag_count: int
    changed_lags: tuple[int, ...]
    delta_profile: tuple[tuple[int, int], ...]
    current_profile: tuple[tuple[int, int], ...]


def build_single_action_records(q: np.ndarray, s: np.ndarray) -> list[dict[str, object]]:
    context = CompositeContext.from_seed(q, s)
    return [
        context.evaluate_action(action, include_changed_lags=True)
        for action in enumerate_single_packets(context.length)
    ]


def build_single_action_graph(
    q: np.ndarray,
    s: np.ndarray,
    *,
    cone_union_limit: int,
) -> RetainedStateGraph:
    return RetainedStateGraph.from_records(
        q=np.asarray(q, dtype=np.int8),
        s=np.asarray(s, dtype=np.int8),
        records=build_single_action_records(q, s),
        cone_union_limit=cone_union_limit,
    )


def transport_signature(before_coefficients: np.ndarray, after_coefficients: np.ndarray) -> TransportSignature:
    before = np.asarray(before_coefficients, dtype=np.int32)[1:]
    after = np.asarray(after_coefficients, dtype=np.int32)[1:]
    delta = (after - before).astype(np.int32)
    reservoir_exchange = int(np.sum(delta))
    balanced_delta = delta.copy()
    if balanced_delta.size:
        balanced_delta[-1] -= reservoir_exchange
    currents = -np.cumsum(balanced_delta[:-1], dtype=np.int64)
    changed = np.flatnonzero(delta) + 1
    delta_profile = tuple((int(lag), int(delta[lag - 1])) for lag in changed.tolist())
    current_profile = tuple(
        (int(edge_after_lag + 1), int(currents[edge_after_lag]))
        for edge_after_lag in np.flatnonzero(currents).tolist()
    )
    positive_mass = int(np.clip(delta, 0, None).sum())
    negative_mass = int(np.clip(-delta, 0, None).sum())
    before_abs = np.abs(before)
    after_abs = np.abs(after)
    return TransportSignature(
        support_flux=int(np.count_nonzero(after) - np.count_nonzero(before)),
        l1_gain=int(np.sum(before_abs) - np.sum(after_abs)),
        max_gain=(
            int(np.max(before_abs)) if before_abs.size else 0
        )
        - (
            int(np.max(after_abs)) if after_abs.size else 0
        ),
        danger_reduction=int(np.maximum(0, before_abs - after_abs).sum()),
        reservoir_exchange=reservoir_exchange,
        reservoir_abs=abs(reservoir_exchange),
        transport_span=int(np.sum(np.abs(currents))),
        transport_peak=int(np.max(np.abs(currents))) if currents.size else 0,
        positive_mass=positive_mass,
        negative_mass=negative_mass,
        changed_lag_count=int(len(changed)),
        changed_lags=tuple(int(lag) for lag in changed.tolist()),
        delta_profile=delta_profile,
        current_profile=current_profile,
    )


def update_warning_field(
    warning_field: np.ndarray,
    changed_lags: Sequence[int],
    *,
    decay: int,
    boost: int,
    cap: int,
) -> np.ndarray:
    updated = np.maximum(np.asarray(warning_field, dtype=np.int16) - int(decay), 0)
    for lag in changed_lags:
        updated[int(lag) - 1] = min(cap, int(updated[int(lag) - 1]) + int(boost))
    return updated.astype(np.int16)


def warning_overlap(warning_field: np.ndarray, changed_lags: Sequence[int]) -> int:
    return int(sum(int(warning_field[int(lag) - 1]) for lag in changed_lags))


def nontrivial_periods(sequence: np.ndarray) -> list[int]:
    vector = np.asarray(sequence, dtype=np.int8)
    periods: list[int] = []
    for period in range(1, len(vector)):
        if len(vector) % period != 0:
            continue
        if np.array_equal(vector, np.tile(vector[:period], len(vector) // period)):
            periods.append(int(period))
    return periods


def family_leakage_audit_payload(
    *,
    q: np.ndarray,
    s: np.ndarray,
    method_name: str,
    winning_packet_labels: Sequence[str],
    mechanism_statement: str,
) -> dict[str, object]:
    q_vec = np.asarray(q, dtype=np.int8)
    s_vec = np.asarray(s, dtype=np.int8)
    sequences = derived_quadruple(q_vec, s_vec)
    sequence_names = ("s", "s_prime", "qs", "qs_prime")
    periods = {
        name: nontrivial_periods(sequence)
        for name, sequence in zip(sequence_names, sequences)
    }
    symmetry_flags = {
        "q_palindromic": bool(np.array_equal(q_vec, q_vec[::-1]) or np.array_equal(q_vec, -q_vec[::-1])),
        "s_palindromic": bool(np.array_equal(s_vec, s_vec[::-1]) or np.array_equal(s_vec, -s_vec[::-1])),
        "q_prime_involution_fixed": bool(
            np.array_equal(q_vec, prime_involution(q_vec)) or np.array_equal(q_vec, -prime_involution(q_vec))
        ),
        "s_prime_involution_fixed": bool(
            np.array_equal(s_vec, prime_involution(s_vec)) or np.array_equal(s_vec, -prime_involution(s_vec))
        ),
        "q_equals_pm_s": bool(np.array_equal(q_vec, s_vec) or np.array_equal(q_vec, -s_vec)),
    }

    return {
        "method_name": method_name,
        "winning_packet_labels": list(winning_packet_labels),
        "mechanism_statement": mechanism_statement,
        "sequence_periods": periods,
        "symmetry_flags": symmetry_flags,
        "family_checks": {
            "Williamson": {
                "pass": not (
                    symmetry_flags["q_palindromic"]
                    and symmetry_flags["s_palindromic"]
                    and symmetry_flags["q_prime_involution_fixed"]
                ),
                "reason": (
                    "The winning state is not constrained to the symmetric / amicable packet relations "
                    "characteristic of Williamson-type subfamilies, and the branch never hard-codes them."
                ),
            },
            "Turyn": {
                "pass": True,
                "reason": (
                    "The branch uses only exact lag-delta transport features and never introduces "
                    "supplementary-sequence identities or multiplication templates."
                ),
            },
            "Goethals-Seidel": {
                "pass": True,
                "reason": (
                    "The repo-wide Goethals-Seidel lift remains the shared evaluation harness only. "
                    "No branch rule restricts the search to a Goethals-Seidel family subspace."
                ),
            },
            "cocyclic": {
                "pass": True,
                "reason": (
                    "No cocycle coordinates, group generators, or `D_{4t}` constraints appear in the state, "
                    "candidate generation, or acceptance rule."
                ),
            },
            "block_circulant": {
                "pass": not any(periods.values()),
                "reason": (
                    "The improved state has no nontrivial period in any derived channel, so the trajectory does not "
                    "collapse into a block- or quasi-circulant template."
                ),
            },
        },
    }


def _current_objective(graph: RetainedStateGraph, state_id: int) -> dict[str, int]:
    return graph.states[int(state_id)].objective


def _improves(current_objective: dict[str, int], candidate_objective: dict[str, int]) -> bool:
    return int(candidate_objective["score"]) < int(current_objective["score"])


def _direct_kind(
    current_objective: dict[str, int],
    candidate_objective: dict[str, int],
    signature: TransportSignature,
) -> str:
    if signature.support_flux < 0:
        return "direct_annihilation"
    if signature.support_flux == 0 and _improves(current_objective, candidate_objective):
        return "direct_move"
    if signature.support_flux > 0 and _improves(current_objective, candidate_objective):
        return "direct_split"
    return "direct_blocked"


def _carrier_kind(
    current_objective: dict[str, int],
    middle_objective: dict[str, int],
    candidate_objective: dict[str, int],
    signature: TransportSignature,
) -> str:
    if middle_objective["support_size"] > current_objective["support_size"] and signature.support_flux <= 0:
        return "split_annihilate"
    if middle_objective["support_size"] == current_objective["support_size"] and signature.support_flux <= 0:
        return "move_annihilate"
    if signature.support_flux < 0:
        return "carrier_annihilation"
    if signature.support_flux == 0 and _improves(current_objective, candidate_objective):
        return "carrier_move"
    return "carrier_blocked"


def _single_candidates(
    graph: RetainedStateGraph,
    *,
    state_id: int,
    warning_field: np.ndarray,
) -> list[dict[str, object]]:
    current_objective = _current_objective(graph, state_id)
    before = graph.coefficients_by_state[int(state_id)]
    candidates: list[dict[str, object]] = []
    for action in graph.actions:
        next_state = int(graph.transitions[int(state_id)][action.index])
        after = graph.coefficients_by_state[next_state]
        signature = transport_signature(before, after)
        candidates.append(
            {
                "action_indices": (int(action.index),),
                "action_labels": [list(action.packet_labels)],
                "action_count": 1,
                "event_kind": _direct_kind(current_objective, graph.states[next_state].objective, signature),
                "start_state_id": int(state_id),
                "middle_state_id": None,
                "end_state_id": int(next_state),
                "objective": dict(graph.states[next_state].objective),
                "signature": asdict(signature),
                "warning_overlap": warning_overlap(warning_field, signature.changed_lags),
                "lookup_cost": 1,
            }
        )
    return candidates


def _carrier_candidates(
    graph: RetainedStateGraph,
    *,
    state_id: int,
    warning_field: np.ndarray,
) -> list[dict[str, object]]:
    current_objective = _current_objective(graph, state_id)
    before = graph.coefficients_by_state[int(state_id)]
    candidates: list[dict[str, object]] = []
    for root in range(len(graph.actions)):
        for edge in graph.causal_cones[root]:
            next_state = int(graph.transitions[int(state_id)][int(edge[0])])
            end_state = int(graph.transitions[next_state][int(edge[1])])
            after = graph.coefficients_by_state[end_state]
            signature = transport_signature(before, after)
            middle_objective = graph.states[next_state].objective
            candidates.append(
                {
                    "action_indices": tuple(int(value) for value in edge),
                    "action_labels": [list(graph.actions[index].packet_labels) for index in edge],
                    "action_count": 2,
                    "event_kind": _carrier_kind(
                        current_objective,
                        middle_objective,
                        graph.states[end_state].objective,
                        signature,
                    ),
                    "start_state_id": int(state_id),
                    "middle_state_id": int(next_state),
                    "end_state_id": int(end_state),
                    "objective": dict(graph.states[end_state].objective),
                    "signature": asdict(signature),
                    "warning_overlap": warning_overlap(warning_field, signature.changed_lags),
                    "lookup_cost": 2,
                }
            )
    return candidates


def lattice_gas_rank(candidate: dict[str, object]) -> tuple[object, ...]:
    signature = candidate["signature"]
    return (
        int(signature["support_flux"]),
        int(signature["reservoir_abs"]),
        int(signature["transport_span"]),
        int(candidate["warning_overlap"]),
        -int(signature["l1_gain"]),
        -int(signature["max_gain"]),
        int(candidate["objective"]["score"]),
        tuple(int(value) for value in candidate["action_indices"]),
    )


def warning_field_rank(candidate: dict[str, object]) -> tuple[object, ...]:
    signature = candidate["signature"]
    return (
        int(signature["support_flux"]),
        -int(signature["danger_reduction"]),
        int(candidate["warning_overlap"]),
        int(signature["reservoir_abs"]),
        int(candidate["objective"]["score"]),
        tuple(int(value) for value in candidate["action_indices"]),
    )


def greedy_rank(candidate: dict[str, object]) -> tuple[object, ...]:
    objective = candidate["objective"]
    return (
        int(objective["support_size"]),
        int(objective["l1"]),
        int(objective["max_abs"]),
        tuple(int(value) for value in candidate["action_indices"]),
    )


def _run_policy(
    graph: RetainedStateGraph,
    *,
    method_name: str,
    start_state_id: int,
    lookup_budget: int,
    candidate_factory: Callable[[RetainedStateGraph, int, np.ndarray], list[dict[str, object]]],
    rank_fn: Callable[[dict[str, object]], tuple[object, ...]],
    accept_fn: Callable[[dict[str, int], dict[str, object]], bool],
    warning_decay: int = 1,
    warning_boost: int = 2,
    warning_cap: int = 8,
) -> dict[str, object]:
    current_state = int(start_state_id)
    best_state = int(start_state_id)
    lookups = 0
    warning_field = np.zeros(graph.context.length - 1, dtype=np.int16)
    trace: list[dict[str, object]] = []

    while True:
        candidates = candidate_factory(graph, current_state, warning_field)
        if not candidates:
            break
        if lookups + sum(int(candidate["lookup_cost"]) for candidate in candidates) > int(lookup_budget):
            break
        lookups += sum(int(candidate["lookup_cost"]) for candidate in candidates)
        current_objective = dict(graph.states[current_state].objective)
        admissible = [candidate for candidate in candidates if accept_fn(current_objective, candidate)]
        if not admissible:
            break
        chosen = min(admissible, key=rank_fn)
        current_state = int(chosen["end_state_id"])
        if int(graph.states[current_state].objective["score"]) < int(graph.states[best_state].objective["score"]):
            best_state = current_state
        warning_field = update_warning_field(
            warning_field,
            changed_lags=chosen["signature"]["changed_lags"],
            decay=warning_decay,
            boost=warning_boost,
            cap=warning_cap,
        )
        trace.append(
            {
                "step": len(trace) + 1,
                "event_kind": str(chosen["event_kind"]),
                "action_indices": list(chosen["action_indices"]),
                "action_labels": list(chosen["action_labels"]),
                "start_state_id": int(chosen["start_state_id"]),
                "middle_state_id": (
                    int(chosen["middle_state_id"]) if chosen["middle_state_id"] is not None else None
                ),
                "end_state_id": int(chosen["end_state_id"]),
                "objective": dict(chosen["objective"]),
                "signature": dict(chosen["signature"]),
                "warning_overlap": int(chosen["warning_overlap"]),
                "warning_field_nonzero": int(np.count_nonzero(warning_field)),
                "warning_field_sum": int(np.sum(warning_field)),
                "lookups_after_step": int(lookups),
            }
        )

    return {
        "method_name": method_name,
        "lookup_budget": int(lookup_budget),
        "transition_lookups": int(lookups),
        "start_state": graph.state_payload(start_state_id),
        "end_state": graph.state_payload(current_state),
        "best_state": graph.state_payload(best_state),
        "trace": trace,
        "accepted_update_count": len(trace),
    }


def run_lattice_gas_ca(
    graph: RetainedStateGraph,
    *,
    start_state_id: int,
    lookup_budget: int,
    warning_decay: int = 1,
    warning_boost: int = 2,
    warning_cap: int = 8,
    reservoir_cap: int = 16,
) -> dict[str, object]:
    def candidate_factory(local_graph: RetainedStateGraph, state_id: int, warning_field: np.ndarray) -> list[dict[str, object]]:
        singles = _single_candidates(local_graph, state_id=state_id, warning_field=warning_field)
        current_objective = _current_objective(local_graph, state_id)
        if any(_improves(current_objective, candidate["objective"]) for candidate in singles):
            return singles
        return singles + _carrier_candidates(local_graph, state_id=state_id, warning_field=warning_field)

    def accept_fn(current_objective: dict[str, int], candidate: dict[str, object]) -> bool:
        if not _improves(current_objective, candidate["objective"]):
            return False
        if int(candidate["action_count"]) == 1:
            return True
        signature = candidate["signature"]
        return (
            int(signature["support_flux"]) <= 0
            and int(signature["reservoir_abs"]) <= int(reservoir_cap)
            and int(signature["l1_gain"]) > 0
        )

    result = _run_policy(
        graph,
        method_name="defect_charge_lattice_gas_ca",
        start_state_id=start_state_id,
        lookup_budget=lookup_budget,
        candidate_factory=candidate_factory,
        rank_fn=lattice_gas_rank,
        accept_fn=accept_fn,
        warning_decay=warning_decay,
        warning_boost=warning_boost,
        warning_cap=warning_cap,
    )
    result["mode"] = {
        "warning_decay": int(warning_decay),
        "warning_boost": int(warning_boost),
        "warning_cap": int(warning_cap),
        "reservoir_cap": int(reservoir_cap),
        "candidate_set": "single_action_plus_two_step_carriers",
    }
    return result


def run_lag_greedy_control(
    graph: RetainedStateGraph,
    *,
    start_state_id: int,
    lookup_budget: int,
) -> dict[str, object]:
    def candidate_factory(local_graph: RetainedStateGraph, state_id: int, warning_field: np.ndarray) -> list[dict[str, object]]:
        del warning_field
        return _single_candidates(local_graph, state_id=state_id, warning_field=np.zeros(local_graph.context.length - 1, dtype=np.int16))

    def accept_fn(current_objective: dict[str, int], candidate: dict[str, object]) -> bool:
        return _improves(current_objective, candidate["objective"])

    result = _run_policy(
        graph,
        method_name="lag_greedy_control",
        start_state_id=start_state_id,
        lookup_budget=lookup_budget,
        candidate_factory=candidate_factory,
        rank_fn=greedy_rank,
        accept_fn=accept_fn,
        warning_decay=0,
        warning_boost=0,
        warning_cap=0,
    )
    result["mode"] = {
        "candidate_set": "single_action_only",
        "selection_rule": "best direct lexicographic objective in lag space",
    }
    return result


def run_warning_field_control(
    graph: RetainedStateGraph,
    *,
    start_state_id: int,
    lookup_budget: int,
    warning_decay: int = 1,
    warning_boost: int = 2,
    warning_cap: int = 8,
) -> dict[str, object]:
    def candidate_factory(local_graph: RetainedStateGraph, state_id: int, warning_field: np.ndarray) -> list[dict[str, object]]:
        return _single_candidates(local_graph, state_id=state_id, warning_field=warning_field)

    def accept_fn(current_objective: dict[str, int], candidate: dict[str, object]) -> bool:
        return _improves(current_objective, candidate["objective"])

    result = _run_policy(
        graph,
        method_name="warning_field_control",
        start_state_id=start_state_id,
        lookup_budget=lookup_budget,
        candidate_factory=candidate_factory,
        rank_fn=warning_field_rank,
        accept_fn=accept_fn,
        warning_decay=warning_decay,
        warning_boost=warning_boost,
        warning_cap=warning_cap,
    )
    result["mode"] = {
        "candidate_set": "single_action_only",
        "warning_decay": int(warning_decay),
        "warning_boost": int(warning_boost),
        "warning_cap": int(warning_cap),
    }
    return result


def candidate_signature_key(candidate: dict[str, object]) -> tuple[object, ...]:
    signature = candidate["signature"]
    delta_profile = tuple(tuple(int(value) for value in pair) for pair in signature["delta_profile"])
    return (
        str(candidate["event_kind"]),
        int(signature["support_flux"]),
        int(signature["reservoir_abs"]),
        int(signature["changed_lag_count"]),
        delta_profile,
    )


def _normalized_event_kind(event_kind: str) -> str:
    text = str(event_kind)
    if "split_annihilate" in text:
        return "split_annihilate"
    if "move_annihilate" in text:
        return "move_annihilate"
    if "annihilation" in text:
        return "annihilation"
    if "move" in text:
        return "move"
    if "split" in text:
        return "split"
    return text


def _support_class(support_flux: int) -> str:
    value = int(support_flux)
    if value < 0:
        return "decrease"
    if value == 0:
        return "conserve"
    return "increase"


def _reservoir_bin(reservoir_abs: int) -> str:
    value = int(reservoir_abs)
    if value == 0:
        return "0"
    if value <= 4:
        return "1_4"
    if value <= 8:
        return "5_8"
    if value <= 16:
        return "9_16"
    return "17_plus"


def _changed_count_bin(changed_count: int) -> str:
    value = int(changed_count)
    if value <= 1:
        return "1"
    if value <= 2:
        return "2"
    if value <= 4:
        return "3_4"
    if value <= 8:
        return "5_8"
    return "9_plus"


def _transport_bin(transport_span: int, *, length: int) -> str:
    ratio = float(transport_span) / float(max(1, int(length)))
    if ratio <= 2.0:
        return "tight"
    if ratio <= 6.0:
        return "mid"
    return "wide"


def _canonical_sign_runs(delta_profile: Sequence[Sequence[int]]) -> tuple[tuple[int, int], ...]:
    signs = [1 if int(value) > 0 else -1 for _, value in delta_profile]
    if not signs:
        return tuple()

    def runs(values: Sequence[int]) -> tuple[tuple[int, int], ...]:
        encoded: list[tuple[int, int]] = []
        current_sign = int(values[0])
        current_count = 1
        for value in values[1:]:
            if int(value) == current_sign:
                current_count += 1
                continue
            encoded.append((current_sign, current_count))
            current_sign = int(value)
            current_count = 1
        encoded.append((current_sign, current_count))
        return tuple(encoded)

    variants = [
        runs(signs),
        runs(list(reversed(signs))),
        runs([-value for value in signs]),
        runs([-value for value in reversed(signs)]),
    ]
    return min(variants)


def orbit_signature_for_event(candidate: dict[str, object], *, length: int) -> tuple[object, ...]:
    signature = candidate["signature"]
    return (
        _normalized_event_kind(str(candidate["event_kind"])),
        int(candidate["action_count"]),
        _support_class(int(signature["support_flux"])),
        _changed_count_bin(int(signature["changed_lag_count"])),
        _transport_bin(int(signature["transport_span"]), length=int(length)),
        len(_canonical_sign_runs(signature["delta_profile"])),
    )


def pair_candidates_from_state(
    graph: RetainedStateGraph,
    *,
    state_id: int,
) -> list[dict[str, object]]:
    return _carrier_candidates(
        graph,
        state_id=state_id,
        warning_field=np.zeros(graph.context.length - 1, dtype=np.int16),
    )


def single_candidates_from_state(
    graph: RetainedStateGraph,
    *,
    state_id: int,
) -> list[dict[str, object]]:
    return _single_candidates(
        graph,
        state_id=state_id,
        warning_field=np.zeros(graph.context.length - 1, dtype=np.int16),
    )


def best_improving_event(
    graph: RetainedStateGraph,
    *,
    state_id: int,
    include_pairs: bool,
) -> dict[str, object] | None:
    candidates = single_candidates_from_state(graph, state_id=state_id)
    if include_pairs:
        candidates.extend(pair_candidates_from_state(graph, state_id=state_id))
    current_objective = _current_objective(graph, state_id)
    improving = [candidate for candidate in candidates if _improves(current_objective, candidate["objective"])]
    if not improving:
        return None
    return min(improving, key=lambda candidate: int(candidate["objective"]["score"]))


def control_training_examples(graph: RetainedStateGraph, *, state_limit: int = 16) -> list[dict[str, object]]:
    examples: list[dict[str, object]] = []
    for state in graph.states[: int(state_limit)]:
        best = best_improving_event(graph, state_id=state.state_id, include_pairs=True)
        if best is None:
            continue
        examples.append(best)
    return examples
