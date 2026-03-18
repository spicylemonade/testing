from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .harness import SearchConfig, SearchResult, correlation_coefficients
from .search import apply_packet, load_sequence_pair, objective_with_score, packet_count


@dataclass
class DefectSyndromeView:
    q: np.ndarray
    s: np.ndarray
    coefficients: np.ndarray
    lag_mask: np.ndarray
    active_lags: np.ndarray
    raw_pressure: np.ndarray
    coupled_pressure: np.ndarray
    refractory: np.ndarray


def _rng(config: SearchConfig, restart_index: int = 0) -> np.random.Generator:
    return np.random.default_rng(config.seed + restart_index)


def _restart_state(
    initial_q: np.ndarray,
    initial_s: np.ndarray,
    config: SearchConfig,
    restart_index: int,
) -> tuple[np.ndarray, np.ndarray]:
    q_state = np.asarray(initial_q, dtype=np.int8).copy()
    s_state = np.asarray(initial_s, dtype=np.int8).copy()
    restart_packet_flips = int(config.metadata.get("restart_packet_flips", 0) or 0)
    if restart_index == 0 or restart_packet_flips <= 0:
        return q_state, s_state
    rng = _rng(config, restart_index)
    for _ in range(restart_packet_flips):
        q_state, s_state = apply_packet(
            q_state,
            s_state,
            int(rng.integers(packet_count(len(q_state)))),
        )
    return q_state, s_state


def _autocorr_delta_for_index(seq: np.ndarray, index: int) -> np.ndarray:
    vector = np.asarray(seq, dtype=np.int8)
    n = len(vector)
    delta = np.zeros(n, dtype=np.int32)
    value = int(vector[index])
    for lag in range(1, n):
        change = 0
        if index + lag < n:
            change -= 2 * value * int(vector[index + lag])
        if index - lag >= 0:
            change -= 2 * int(vector[index - lag]) * value
        delta[lag] = change
    return delta


def _packet_delta_vector(q: np.ndarray, s: np.ndarray, packet: int) -> np.ndarray:
    q_vec = np.asarray(q, dtype=np.int8)
    s_vec = np.asarray(s, dtype=np.int8)
    sq = (q_vec * s_vec).astype(np.int8)
    midpoint = (len(q_vec) + 1) // 2
    packet_index = int(packet % len(q_vec))

    s_prime = s_vec.copy()
    s_prime[midpoint:] *= -1
    sq_prime = sq.copy()
    sq_prime[midpoint:] *= -1

    if packet < len(q_vec):
        return (
            _autocorr_delta_for_index(sq, packet_index)
            + _autocorr_delta_for_index(sq_prime, packet_index)
        )

    return (
        _autocorr_delta_for_index(s_vec, packet_index)
        + _autocorr_delta_for_index(s_prime, packet_index)
        + _autocorr_delta_for_index(sq, packet_index)
        + _autocorr_delta_for_index(sq_prime, packet_index)
    )


def _lag_mask(coefficients: np.ndarray, radius: int) -> tuple[np.ndarray, np.ndarray]:
    coeffs = np.asarray(coefficients, dtype=np.int32)
    active_lags = np.flatnonzero(coeffs[1:]) + 1
    mask = np.zeros(len(coeffs), dtype=bool)
    if not active_lags.size:
        return mask, active_lags
    for lag in active_lags.tolist():
        lo = max(1, lag - radius)
        hi = min(len(coeffs), lag + radius + 1)
        mask[lo:hi] = True
    return mask, active_lags


def _packet_neighbors(packet: int, length: int, radius: int) -> list[int]:
    channel = packet // length
    index = packet % length
    base = channel * length
    neighbors = []
    for offset in range(1, radius + 1):
        neighbors.append(base + ((index - offset) % length))
        neighbors.append(base + ((index + offset) % length))
    neighbors.append(((1 - channel) * length) + index)
    return neighbors


def _conflict_packets(packet: int, length: int, radius: int) -> set[int]:
    channel = packet // length
    index = packet % length
    base = channel * length
    conflicts = {packet, ((1 - channel) * length) + index}
    for offset in range(1, radius + 1):
        conflicts.add(base + ((index - offset) % length))
        conflicts.add(base + ((index + offset) % length))
    return conflicts


def _packet_pressures(
    q: np.ndarray,
    s: np.ndarray,
    coefficients: np.ndarray,
    lag_mask: np.ndarray,
    active_lags: np.ndarray,
    config: SearchConfig,
) -> np.ndarray:
    length = len(q)
    if not np.any(lag_mask):
        return np.zeros(packet_count(length), dtype=np.float64)

    active_bonus = float(config.metadata.get("active_lag_bonus", 1.0) or 1.0)
    spill_l1_penalty = float(config.metadata.get("spill_l1_penalty", 0.25) or 0.25)
    spill_support_penalty = float(config.metadata.get("spill_support_penalty", 16.0) or 16.0)
    weights = np.ones(len(coefficients), dtype=np.float64)
    if active_lags.size:
        weights[active_lags] += active_bonus

    raw = np.zeros(packet_count(length), dtype=np.float64)
    coeff_slice = coefficients[lag_mask].astype(np.int32)
    weight_slice = weights[lag_mask]
    outside_mask = ~lag_mask
    if outside_mask.size:
        outside_mask[0] = False
    outside_before = coefficients[outside_mask]

    for packet in range(packet_count(length)):
        delta = _packet_delta_vector(q, s, packet)
        candidate = coefficients + delta
        candidate_slice = candidate[lag_mask]
        improvement = np.abs(coeff_slice) - np.abs(candidate_slice)
        spill = 0.0
        if np.any(outside_mask):
            outside_after = candidate[outside_mask]
            spill += spill_l1_penalty * float(
                np.sum(np.maximum(0, np.abs(outside_after) - np.abs(outside_before)))
            )
            spill += spill_support_penalty * float(
                max(
                    0,
                    int(np.count_nonzero(outside_after)) - int(np.count_nonzero(outside_before)),
                )
            )
        raw[packet] = float(np.sum(weight_slice * improvement) - spill)
    return raw


def _coupled_pressure(
    raw_pressure: np.ndarray,
    refractory: np.ndarray,
    length: int,
    config: SearchConfig,
) -> np.ndarray:
    radius = int(config.metadata.get("packet_neighborhood_radius", 2) or 2)
    same_channel_weight = float(config.metadata.get("same_channel_weight", 0.15) or 0.15)
    cross_channel_weight = float(config.metadata.get("cross_channel_weight", 0.35) or 0.35)
    refractory_penalty = float(config.metadata.get("refractory_penalty", 0.75) or 0.75)

    coupled = raw_pressure.astype(np.float64).copy()
    for packet in range(len(raw_pressure)):
        channel = packet // length
        index = packet % length
        base = channel * length
        local = coupled[packet]
        for offset in range(1, radius + 1):
            local += same_channel_weight * raw_pressure[base + ((index - offset) % length)]
            local += same_channel_weight * raw_pressure[base + ((index + offset) % length)]
        local += cross_channel_weight * raw_pressure[((1 - channel) * length) + index]
        local -= refractory_penalty * float(refractory[packet] > 0)
        coupled[packet] = local
    return coupled


def _select_packets(
    coupled_pressure: np.ndarray,
    length: int,
    config: SearchConfig,
) -> list[int]:
    radius = int(config.metadata.get("packet_neighborhood_radius", 2) or 2)
    activation_threshold = float(config.metadata.get("activation_threshold", 0.5) or 0.5)
    max_active_packets = int(config.metadata.get("max_active_packets", 4) or 4)
    fallback_best_packet = bool(config.metadata.get("fallback_best_packet", True))

    blocked = np.zeros(len(coupled_pressure), dtype=bool)
    selected: list[int] = []
    order = np.argsort(-coupled_pressure)
    for packet in order.tolist():
        if coupled_pressure[packet] <= activation_threshold:
            break
        if blocked[packet]:
            continue
        local_max = max(coupled_pressure[neighbor] for neighbor in _packet_neighbors(packet, length, radius))
        if coupled_pressure[packet] < local_max:
            continue
        selected.append(packet)
        for conflict in _conflict_packets(packet, length, radius):
            blocked[conflict] = True
        if len(selected) >= max_active_packets:
            break

    if not selected and fallback_best_packet:
        best_packet = int(order[0])
        if coupled_pressure[best_packet] > 0.0:
            selected = [best_packet]
    return selected


def defect_syndrome_view(
    q: np.ndarray,
    s: np.ndarray,
    refractory: np.ndarray,
    config: SearchConfig,
) -> DefectSyndromeView:
    coefficients = correlation_coefficients(q, s)
    lag_mask, active_lags = _lag_mask(
        coefficients,
        int(config.metadata.get("lag_neighborhood_radius", 1) or 1),
    )
    raw_pressure = _packet_pressures(q, s, coefficients, lag_mask, active_lags, config)
    coupled_pressure = _coupled_pressure(raw_pressure, refractory, len(q), config)
    return DefectSyndromeView(
        q=np.asarray(q, dtype=np.int8),
        s=np.asarray(s, dtype=np.int8),
        coefficients=coefficients,
        lag_mask=lag_mask,
        active_lags=active_lags,
        raw_pressure=raw_pressure,
        coupled_pressure=coupled_pressure,
        refractory=np.asarray(refractory, dtype=np.int16),
    )


def _restart_trace_entry(
    restart_index: int,
    step: int,
    active_packets: list[int],
    view: DefectSyndromeView,
    objective: dict[str, int],
) -> dict[str, Any]:
    return {
        "restart": restart_index,
        "step": step,
        "active_packets": [int(packet) for packet in active_packets],
        "active_lag_count": int(len(view.active_lags)),
        "max_coupled_pressure": float(np.max(view.coupled_pressure)) if view.coupled_pressure.size else 0.0,
        **objective,
    }


def defect_syndrome_ca_search(
    initial_q: np.ndarray,
    initial_s: np.ndarray,
    config: SearchConfig,
) -> SearchResult:
    base_q = np.asarray(initial_q, dtype=np.int8)
    base_s = np.asarray(initial_s, dtype=np.int8)
    best_q = base_q.copy()
    best_s = base_s.copy()
    best_objective = objective_with_score(best_q, best_s)
    evaluations = 1
    best_restart = 0
    completed_restarts = 0
    trace: list[dict[str, Any]] = []

    refractory_steps = int(config.metadata.get("refractory_steps", 2) or 2)
    stagnation_limit = int(config.metadata.get("stagnation_limit", 12) or 12)
    field_evaluations = 0

    for restart_index in range(config.restart_count):
        if evaluations >= config.evaluation_budget:
            break

        q_state, s_state = _restart_state(base_q, base_s, config, restart_index)
        refractory = np.zeros(packet_count(len(q_state)), dtype=np.int16)
        current = objective_with_score(q_state, s_state)
        view = defect_syndrome_view(q_state, s_state, refractory, config)
        if np.any(view.lag_mask):
            field_evaluations += packet_count(len(q_state))
        trace.append(_restart_trace_entry(restart_index, 0, [], view, current))
        evaluations += 1
        completed_restarts += 1
        restart_best_q = q_state.copy()
        restart_best_s = s_state.copy()
        restart_best_objective = current
        stagnation = 0
        step = 0

        while evaluations < config.evaluation_budget and stagnation < stagnation_limit:
            active_packets = _select_packets(view.coupled_pressure, len(q_state), config)
            if not active_packets:
                break

            q_next = q_state.copy()
            s_next = s_state.copy()
            for packet in active_packets:
                q_next, s_next = apply_packet(q_next, s_next, int(packet))

            refractory = np.maximum(refractory - 1, 0)
            refractory[np.asarray(active_packets, dtype=int)] = refractory_steps
            q_state = q_next
            s_state = s_next
            current = objective_with_score(q_state, s_state)
            evaluations += 1
            step += 1
            view = defect_syndrome_view(q_state, s_state, refractory, config)
            if np.any(view.lag_mask):
                field_evaluations += packet_count(len(q_state))
            trace.append(_restart_trace_entry(restart_index, step, active_packets, view, current))

            if current["score"] < restart_best_objective["score"]:
                restart_best_q = q_state.copy()
                restart_best_s = s_state.copy()
                restart_best_objective = current
                stagnation = 0
            else:
                stagnation += 1

            if current["support_size"] == 0:
                break

        if restart_best_objective["score"] < best_objective["score"]:
            best_q = restart_best_q
            best_s = restart_best_s
            best_objective = restart_best_objective
            best_restart = restart_index

    return SearchResult(
        q=best_q,
        s=best_s,
        evaluations=evaluations,
        completed_restarts=completed_restarts,
        restart_statistics={
            "requested": config.restart_count,
            "completed": completed_restarts,
            "best_restart": best_restart,
        },
        metadata={
            "branch_id": "H1_defect_syndrome_ca_64m",
            "representation": "packet_lattice_plus_sparse_lag_syndrome",
            "pressure_update_mode": "exact_single_packet_delta_over_active_lag_mask",
            "ca_field_evaluations": int(field_evaluations),
            "conserved_quantities": [
                "fixed_qs_length",
                "binary_packet_alphabet",
                "fixed_prime_involution_lift",
                "shared_packet_graph_topology",
            ],
        },
        best_objective=best_objective,
        trace=trace,
    )


def load_h1_seed(path: str, q_key: str = "q", s_key: str = "s") -> tuple[np.ndarray, np.ndarray]:
    return load_sequence_pair(path, q_key=q_key, s_key=s_key)
