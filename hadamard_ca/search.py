from __future__ import annotations

import json
import math
from dataclasses import asdict
from pathlib import Path
from typing import Callable

import numpy as np

from .harness import SearchConfig, SearchResult, objective_summary


Packet = int


def packet_count(length: int) -> int:
    return 2 * int(length)


def apply_packet(q: np.ndarray, s: np.ndarray, packet: Packet) -> tuple[np.ndarray, np.ndarray]:
    q_next = np.asarray(q, dtype=np.int8).copy()
    s_next = np.asarray(s, dtype=np.int8).copy()
    if packet < len(q_next):
        q_next[packet] *= -1
    else:
        s_next[packet - len(q_next)] *= -1
    return q_next, s_next


def objective_with_score(q: np.ndarray, s: np.ndarray) -> dict[str, int]:
    summary = objective_summary(q, s)
    summary["score"] = (
        summary["support_size"] * 1_000_000
        + summary["l1"] * 1_000
        + summary["max_abs"]
    )
    return summary


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


def _search_over_restarts(
    initial_q: np.ndarray,
    initial_s: np.ndarray,
    config: SearchConfig,
    runner: Callable[[np.ndarray, np.ndarray, SearchConfig, int, int], tuple[np.ndarray, np.ndarray, int, list[dict[str, int]]]],
) -> SearchResult:
    best_q = np.asarray(initial_q, dtype=np.int8)
    best_s = np.asarray(initial_s, dtype=np.int8)
    best_objective = objective_with_score(best_q, best_s)
    evaluations = 1
    trace: list[dict[str, int]] = [
        {"restart": 0, **best_objective}
    ]
    best_restart = 0
    completed_restarts = 0

    for restart_index in range(config.restart_count):
        if evaluations >= config.evaluation_budget:
            break
        start_q, start_s = _restart_state(initial_q, initial_s, config, restart_index)
        remaining = config.evaluation_budget - evaluations
        end_q, end_s, used, restart_trace = runner(
            start_q,
            start_s,
            config,
            restart_index,
            remaining,
        )
        evaluations += used
        completed_restarts += 1
        current_objective = objective_with_score(end_q, end_s)
        trace.extend(restart_trace)
        if current_objective["score"] < best_objective["score"]:
            best_q = end_q
            best_s = end_s
            best_objective = current_objective
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
        best_objective=best_objective,
        trace=trace,
    )


def greedy_search(initial_q: np.ndarray, initial_s: np.ndarray, config: SearchConfig) -> SearchResult:
    def runner(q_state, s_state, _config, restart_index, budget):
        evaluations = 1
        current = objective_with_score(q_state, s_state)
        restart_trace = [{"restart": restart_index, **current}]
        while evaluations < budget:
            best_packet = None
            best_candidate = current
            best_q = q_state
            best_s = s_state
            for packet in range(packet_count(len(q_state))):
                if evaluations >= budget:
                    break
                cand_q, cand_s = apply_packet(q_state, s_state, packet)
                candidate = objective_with_score(cand_q, cand_s)
                evaluations += 1
                if candidate["score"] < best_candidate["score"]:
                    best_packet = packet
                    best_candidate = candidate
                    best_q, best_s = cand_q, cand_s
            if best_packet is None:
                break
            q_state, s_state = best_q, best_s
            current = best_candidate
            restart_trace.append({"restart": restart_index, "packet": int(best_packet), **current})
            if current["support_size"] == 0:
                break
        return q_state, s_state, evaluations, restart_trace

    return _search_over_restarts(initial_q, initial_s, config, runner)


def tabu_search(initial_q: np.ndarray, initial_s: np.ndarray, config: SearchConfig) -> SearchResult:
    tabu_tenure = int(config.metadata.get("tabu_tenure", 7) or 7)

    def runner(q_state, s_state, _config, restart_index, budget):
        evaluations = 1
        tabu_until = np.zeros(packet_count(len(q_state)), dtype=int)
        step = 0
        current = objective_with_score(q_state, s_state)
        best = current
        best_q = q_state
        best_s = s_state
        restart_trace = [{"restart": restart_index, **current}]
        while evaluations < budget:
            chosen_packet = None
            chosen_candidate = None
            chosen_q = q_state
            chosen_s = s_state
            for packet in range(packet_count(len(q_state))):
                if evaluations >= budget:
                    break
                cand_q, cand_s = apply_packet(q_state, s_state, packet)
                candidate = objective_with_score(cand_q, cand_s)
                evaluations += 1
                is_tabu = tabu_until[packet] > step
                aspiration = candidate["score"] < best["score"]
                if is_tabu and not aspiration:
                    continue
                if chosen_candidate is None or candidate["score"] < chosen_candidate["score"]:
                    chosen_packet = packet
                    chosen_candidate = candidate
                    chosen_q, chosen_s = cand_q, cand_s
            if chosen_packet is None or chosen_candidate is None:
                break
            step += 1
            q_state, s_state = chosen_q, chosen_s
            tabu_until[chosen_packet] = step + tabu_tenure
            current = chosen_candidate
            if current["score"] < best["score"]:
                best = current
                best_q, best_s = q_state, s_state
            restart_trace.append({"restart": restart_index, "packet": int(chosen_packet), **current})
            if best["support_size"] == 0:
                break
        return best_q, best_s, evaluations, restart_trace

    return _search_over_restarts(initial_q, initial_s, config, runner)


def simulated_annealing_search(initial_q: np.ndarray, initial_s: np.ndarray, config: SearchConfig) -> SearchResult:
    initial_temperature = float(config.metadata.get("initial_temperature", 500.0) or 500.0)
    cooling = float(config.metadata.get("cooling", 0.995) or 0.995)

    def runner(q_state, s_state, _config, restart_index, budget):
        rng = _rng(_config, restart_index)
        evaluations = 1
        current = objective_with_score(q_state, s_state)
        best = current
        best_q = q_state
        best_s = s_state
        temperature = initial_temperature
        restart_trace = [{"restart": restart_index, **current}]
        while evaluations < budget:
            packet = int(rng.integers(packet_count(len(q_state))))
            cand_q, cand_s = apply_packet(q_state, s_state, packet)
            candidate = objective_with_score(cand_q, cand_s)
            evaluations += 1
            delta = candidate["score"] - current["score"]
            accept = delta <= 0
            if not accept and temperature > 0.0:
                accept = rng.random() < math.exp(-delta / temperature)
            if accept:
                q_state, s_state = cand_q, cand_s
                current = candidate
                restart_trace.append({"restart": restart_index, "packet": packet, **current})
                if current["score"] < best["score"]:
                    best = current
                    best_q, best_s = q_state, s_state
            temperature *= cooling
            if best["support_size"] == 0:
                break
        return best_q, best_s, evaluations, restart_trace

    return _search_over_restarts(initial_q, initial_s, config, runner)


def stochastic_hillclimb_search(initial_q: np.ndarray, initial_s: np.ndarray, config: SearchConfig) -> SearchResult:
    sample_size = int(config.metadata.get("sample_size", 16) or 16)

    def runner(q_state, s_state, _config, restart_index, budget):
        rng = _rng(_config, restart_index)
        evaluations = 1
        current = objective_with_score(q_state, s_state)
        best = current
        best_q = q_state
        best_s = s_state
        restart_trace = [{"restart": restart_index, **current}]
        while evaluations < budget:
            packets = rng.choice(packet_count(len(q_state)), size=min(sample_size, packet_count(len(q_state))), replace=False)
            improved = False
            for packet in packets.tolist():
                if evaluations >= budget:
                    break
                cand_q, cand_s = apply_packet(q_state, s_state, int(packet))
                candidate = objective_with_score(cand_q, cand_s)
                evaluations += 1
                if candidate["score"] < current["score"]:
                    q_state, s_state = cand_q, cand_s
                    current = candidate
                    improved = True
                    restart_trace.append({"restart": restart_index, "packet": int(packet), **current})
                    if current["score"] < best["score"]:
                        best = current
                        best_q, best_s = q_state, s_state
                    break
            if not improved:
                break
            if best["support_size"] == 0:
                break
        return best_q, best_s, evaluations, restart_trace

    return _search_over_restarts(initial_q, initial_s, config, runner)


METHODS = {
    "greedy": greedy_search,
    "tabu": tabu_search,
    "simulated_annealing": simulated_annealing_search,
    "stochastic_hillclimb": stochastic_hillclimb_search,
}


def load_sequence_pair(path: Path | str, q_key: str = "q", s_key: str = "s") -> tuple[np.ndarray, np.ndarray]:
    payload = json.loads(Path(path).read_text())
    if isinstance(payload, list):
        raise ValueError("expected a JSON object with q and s keys, got a list")
    return (
        np.asarray(payload[q_key], dtype=np.int8),
        np.asarray(payload[s_key], dtype=np.int8),
    )
