from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Sequence

import numpy as np

from .h1_ca import _autocorr_delta_for_index
from .harness import correlation_coefficients, derived_quadruple
from .search import apply_packet, objective_with_score


@dataclass(frozen=True)
class CompositeAction:
    family: str
    packets: tuple[int, ...]
    descriptor: str


@dataclass
class CompositeContext:
    q: np.ndarray
    s: np.ndarray
    sequence_values: np.ndarray
    single_delta_table: np.ndarray
    seed_coefficients: np.ndarray
    seed_objective: dict[str, int]

    @classmethod
    def from_seed(cls, q: np.ndarray, s: np.ndarray) -> "CompositeContext":
        q_vec = np.asarray(q, dtype=np.int8).copy()
        s_vec = np.asarray(s, dtype=np.int8).copy()
        sequences = np.stack(derived_quadruple(q_vec, s_vec), axis=0).astype(np.int8)
        single_delta_table = np.stack(
            [
                np.stack(
                    [_autocorr_delta_for_index(sequence, index) for index in range(len(q_vec))],
                    axis=0,
                )
                for sequence in sequences
            ],
            axis=0,
        ).astype(np.int32)
        return cls(
            q=q_vec,
            s=s_vec,
            sequence_values=sequences,
            single_delta_table=single_delta_table,
            seed_coefficients=correlation_coefficients(q_vec, s_vec),
            seed_objective=objective_with_score(q_vec, s_vec),
        )

    @property
    def length(self) -> int:
        return int(len(self.q))

    def _packet_index_parity(self, packets: Sequence[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
        q_counts: dict[int, int] = {}
        s_counts: dict[int, int] = {}
        for packet in packets:
            packet_id = int(packet)
            if packet_id < self.length:
                q_counts[packet_id] = q_counts.get(packet_id, 0) ^ 1
            else:
                local_index = packet_id - self.length
                s_counts[local_index] = s_counts.get(local_index, 0) ^ 1
        q_indices = tuple(sorted(index for index, parity in q_counts.items() if parity))
        s_indices = tuple(sorted(index for index, parity in s_counts.items() if parity))
        return q_indices, s_indices

    def changed_index_sets(self, packets: Sequence[int]) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
        q_indices, s_indices = self._packet_index_parity(packets)
        sq_indices = tuple(sorted(set(q_indices) ^ set(s_indices)))
        return q_indices, s_indices, sq_indices

    def delta_for_packets(self, packets: Sequence[int]) -> np.ndarray:
        _, s_indices, sq_indices = self.changed_index_sets(packets)
        delta = np.zeros(self.length, dtype=np.int32)
        for sequence_id, changed_indices in ((0, s_indices), (1, s_indices), (2, sq_indices), (3, sq_indices)):
            if not changed_indices:
                continue
            delta += self.single_delta_table[sequence_id, list(changed_indices)].sum(axis=0)
            if len(changed_indices) < 2:
                continue
            values = self.sequence_values[sequence_id]
            for left, right in combinations(changed_indices, 2):
                delta[abs(right - left)] += 4 * int(values[left]) * int(values[right])
        return delta

    def apply_packets(self, packets: Sequence[int]) -> tuple[np.ndarray, np.ndarray]:
        q_state = self.q.copy()
        s_state = self.s.copy()
        for packet in packets:
            q_state, s_state = apply_packet(q_state, s_state, int(packet))
        return q_state, s_state

    def objective_from_delta(self, delta: np.ndarray) -> dict[str, int]:
        coefficients = self.seed_coefficients + np.asarray(delta, dtype=np.int32)
        support = coefficients[1:]
        support_size = int(np.count_nonzero(support))
        l1 = int(np.sum(np.abs(support)))
        max_abs = int(np.max(np.abs(support))) if support_size else 0
        return {
            "support_size": support_size,
            "l1": l1,
            "max_abs": max_abs,
            "score": support_size * 1_000_000 + l1 * 1_000 + max_abs,
        }

    def evaluate_action(self, action: CompositeAction, *, include_changed_lags: bool = False) -> dict[str, object]:
        delta = self.delta_for_packets(action.packets)
        objective = self.objective_from_delta(delta)
        seed = self.seed_objective
        score_comparison = "equal"
        if objective["score"] < seed["score"]:
            score_comparison = "better"
        elif objective["score"] > seed["score"]:
            score_comparison = "worse"

        support_comparison = "equal"
        if objective["support_size"] < seed["support_size"]:
            support_comparison = "lower"
        elif objective["support_size"] > seed["support_size"]:
            support_comparison = "higher"

        q_indices, s_indices, sq_indices = self.changed_index_sets(action.packets)
        record: dict[str, object] = {
            "family": action.family,
            "descriptor": action.descriptor,
            "packets": [int(packet) for packet in action.packets],
            "packet_count": int(len(action.packets)),
            "packet_labels": packet_labels(action.packets, self.length),
            "q_indices": list(q_indices),
            "s_indices": list(s_indices),
            "sq_toggle_indices": list(sq_indices),
            "changed_lag_count": int(np.count_nonzero(delta[1:])),
            "score_comparison": score_comparison,
            "support_comparison": support_comparison,
            "objective": objective,
        }
        if include_changed_lags:
            record["changed_lags"] = (np.flatnonzero(delta[1:]) + 1).astype(int).tolist()
        return record


def packet_label(packet: int, length: int) -> str:
    if int(packet) < int(length):
        return f"q[{int(packet)}]"
    return f"s[{int(packet) - int(length)}]"


def packet_labels(packets: Sequence[int], length: int) -> list[str]:
    return [packet_label(int(packet), int(length)) for packet in packets]


def run_boundaries(sequence: Sequence[int]) -> list[int]:
    vector = np.asarray(sequence, dtype=np.int8)
    return [int(index) for index in range(1, len(vector)) if int(vector[index]) != int(vector[index - 1])]


def enumerate_single_packets(length: int) -> list[CompositeAction]:
    return [
        CompositeAction(
            family="one_packet",
            packets=(packet,),
            descriptor=f"single_{packet_label(packet, length)}",
        )
        for packet in range(2 * int(length))
    ]


def enumerate_all_pairs(length: int) -> list[CompositeAction]:
    return [
        CompositeAction(
            family="pair",
            packets=(int(left), int(right)),
            descriptor="unordered_pair",
        )
        for left, right in combinations(range(2 * int(length)), 2)
    ]


def enumerate_balanced_four_packets(length: int) -> list[CompositeAction]:
    return [
        CompositeAction(
            family="balanced4",
            packets=(int(left), int(length + left), int(right), int(length + right)),
            descriptor="channel_complete_two_site",
        )
        for left, right in combinations(range(int(length)), 2)
    ]


def enumerate_run_boundary_actions(q: Sequence[int], s: Sequence[int]) -> list[CompositeAction]:
    length = len(q)
    actions: list[CompositeAction] = []
    for boundary in run_boundaries(q):
        actions.append(
            CompositeAction(
                family="q_boundary_pair",
                packets=(boundary - 1, boundary),
                descriptor=f"q_boundary_shift_{boundary}",
            )
        )
    for boundary in run_boundaries(s):
        actions.append(
            CompositeAction(
                family="s_boundary_pair",
                packets=(length + boundary - 1, length + boundary),
                descriptor=f"s_boundary_shift_{boundary}",
            )
        )
    for boundary in sorted(set(run_boundaries(q)) | set(run_boundaries(s))):
        actions.append(
            CompositeAction(
                family="boundary_quad",
                packets=(boundary - 1, boundary, length + boundary - 1, length + boundary),
                descriptor=f"matched_boundary_quad_{boundary}",
            )
        )
    return actions


def summary_stats(values: Iterable[int]) -> dict[str, float]:
    array = np.asarray(list(values), dtype=np.float64)
    if array.size == 0:
        return {"min": 0.0, "median": 0.0, "mean": 0.0, "max": 0.0}
    return {
        "min": float(np.min(array)),
        "median": float(np.median(array)),
        "mean": float(np.mean(array)),
        "max": float(np.max(array)),
    }


def pareto_front(records: Sequence[dict[str, object]]) -> list[dict[str, object]]:
    metric_keys = ("changed_lag_count", "support_size", "l1", "max_abs")
    frontier: list[dict[str, object]] = []
    normalized: list[tuple[dict[str, object], tuple[int, int, int, int]]] = []
    for record in records:
        objective = record["objective"]
        assert isinstance(objective, dict)
        normalized.append(
            (
                record,
                (
                    int(record["changed_lag_count"]),
                    int(objective["support_size"]),
                    int(objective["l1"]),
                    int(objective["max_abs"]),
                ),
            )
        )
    for record, metrics in normalized:
        dominated = False
        for other_record, other_metrics in normalized:
            if other_record is record:
                continue
            if all(other <= value for other, value in zip(other_metrics, metrics)) and any(
                other < value for other, value in zip(other_metrics, metrics)
            ):
                dominated = True
                break
        if not dominated:
            frontier.append(record)
    frontier.sort(
        key=lambda record: (
            int(record["changed_lag_count"]),
            int(record["objective"]["support_size"]),
            int(record["objective"]["l1"]),
            int(record["objective"]["max_abs"]),
            str(record["family"]),
            tuple(int(packet) for packet in record["packets"]),
        )
    )
    return frontier
