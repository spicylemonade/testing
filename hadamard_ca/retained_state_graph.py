from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import json
from pathlib import Path
from typing import Sequence

import numpy as np

from .composite import CompositeContext, packet_labels
from .search import load_sequence_pair


@dataclass(frozen=True)
class RetainedAction:
    index: int
    family: str
    packets: tuple[int, ...]
    packet_labels: tuple[str, ...]
    changed_lags: tuple[int, ...]
    changed_lag_count: int


@dataclass(frozen=True)
class RetainedState:
    state_id: int
    packet_mask: tuple[int, ...]
    packet_labels: tuple[str, ...]
    action_subset_masks: tuple[int, ...]
    objective: dict[str, int]
    active_lags: tuple[int, ...]


def _packet_mask_from_packets(packets: Sequence[int]) -> frozenset[int]:
    toggled: set[int] = set()
    for packet in packets:
        packet_id = int(packet)
        if packet_id in toggled:
            toggled.remove(packet_id)
        else:
            toggled.add(packet_id)
    return frozenset(sorted(toggled))


def _state_sort_key(packet_mask: frozenset[int]) -> tuple[int, tuple[int, ...]]:
    return (len(packet_mask), tuple(sorted(int(packet) for packet in packet_mask)))


class RetainedStateGraph:
    def __init__(
        self,
        *,
        context: CompositeContext,
        actions: list[RetainedAction],
        states: list[RetainedState],
        state_index_by_mask: dict[frozenset[int], int],
        transitions: list[list[int]],
        neighbors: list[list[int]],
        causal_cones: list[list[tuple[int, int]]],
    ) -> None:
        self.context = context
        self.actions = actions
        self.states = states
        self.state_index_by_mask = state_index_by_mask
        self.transitions = transitions
        self.neighbors = neighbors
        self.causal_cones = causal_cones

    @classmethod
    def from_paths(
        cls,
        *,
        seed_file: Path | str,
        retained_library_path: Path | str,
        cone_union_limit: int = 25,
    ) -> "RetainedStateGraph":
        q, s = load_sequence_pair(seed_file)
        context = CompositeContext.from_seed(q, s)
        payload = json.loads(Path(retained_library_path).read_text())
        actions = [
            RetainedAction(
                index=index,
                family=str(record["family"]),
                packets=tuple(int(packet) for packet in record["packets"]),
                packet_labels=tuple(str(label) for label in record["packet_labels"]),
                changed_lags=tuple(int(lag) for lag in record["changed_lags"]),
                changed_lag_count=int(record["changed_lag_count"]),
            )
            for index, record in enumerate(payload["records"])
        ]

        unique_masks: dict[frozenset[int], list[int]] = {}
        for subset_mask in range(1 << len(actions)):
            packet_mask: set[int] = set()
            for action in actions:
                if not (subset_mask >> action.index) & 1:
                    continue
                packet_mask ^= set(action.packets)
            frozen_mask = frozenset(sorted(packet_mask))
            unique_masks.setdefault(frozen_mask, []).append(subset_mask)

        state_index_by_mask: dict[frozenset[int], int] = {}
        states: list[RetainedState] = []
        for frozen_mask in sorted(unique_masks, key=_state_sort_key):
            state_index = len(states)
            delta = context.delta_for_packets(tuple(sorted(frozen_mask)))
            coefficients = context.seed_coefficients + delta
            active_lags = tuple((np.flatnonzero(coefficients[1:]) + 1).astype(int).tolist())
            states.append(
                RetainedState(
                    state_id=state_index,
                    packet_mask=tuple(int(packet) for packet in sorted(frozen_mask)),
                    packet_labels=tuple(packet_labels(tuple(sorted(frozen_mask)), context.length)),
                    action_subset_masks=tuple(int(mask) for mask in unique_masks[frozen_mask]),
                    objective=context.objective_from_delta(delta),
                    active_lags=active_lags,
                )
            )
            state_index_by_mask[frozen_mask] = state_index

        action_masks = [_packet_mask_from_packets(action.packets) for action in actions]
        transitions: list[list[int]] = []
        for state in states:
            state_mask = frozenset(state.packet_mask)
            transitions.append(
                [
                    state_index_by_mask[frozenset(state_mask ^ action_masks[action.index])]
                    for action in actions
                ]
            )

        neighbors: list[list[int]] = []
        for action in actions:
            local_neighbors = [
                other.index
                for other in actions
                if other.index != action.index
                and bool(set(action.changed_lags) & set(other.changed_lags))
            ]
            neighbors.append(sorted(local_neighbors))

        causal_cones: list[list[tuple[int, int]]] = []
        for action in actions:
            cones: list[tuple[int, int]] = []
            for neighbor in neighbors[action.index]:
                other = actions[neighbor]
                if len(set(action.changed_lags) | set(other.changed_lags)) > int(cone_union_limit):
                    continue
                cones.append((action.index, neighbor))
            causal_cones.append(cones)

        return cls(
            context=context,
            actions=actions,
            states=states,
            state_index_by_mask=state_index_by_mask,
            transitions=transitions,
            neighbors=neighbors,
            causal_cones=causal_cones,
        )

    def state_payload(self, state_id: int) -> dict[str, object]:
        state = self.states[int(state_id)]
        return {
            "state_id": int(state.state_id),
            "packet_mask": list(state.packet_mask),
            "packet_labels": list(state.packet_labels),
            "action_subset_masks": list(state.action_subset_masks),
            "objective": dict(state.objective),
            "active_lags": list(state.active_lags),
        }

    def best_immediate_score(self, state_id: int) -> int:
        return min(
            int(self.states[next_state].objective["score"])
            for next_state in self.transitions[int(state_id)]
        )

    def best_two_step_cone_score(self, state_id: int) -> int | None:
        state_index = int(state_id)
        candidates: list[int] = []
        for cone_list in self.causal_cones:
            for left, right in cone_list:
                next_state = self.transitions[state_index][left]
                end_state = self.transitions[next_state][right]
                candidates.append(int(self.states[end_state].objective["score"]))
        if not candidates:
            return None
        return min(candidates)

    def structural_barrier_states(self, limit: int | None = None) -> list[int]:
        candidate_ids: list[int] = []
        for state in self.states:
            current_score = int(state.objective["score"])
            if self.best_immediate_score(state.state_id) < current_score:
                continue
            best_two_step = self.best_two_step_cone_score(state.state_id)
            if best_two_step is None or best_two_step >= current_score:
                continue
            candidate_ids.append(state.state_id)
        candidate_ids.sort(
            key=lambda state_id: (
                int(self.states[state_id].objective["score"]),
                len(self.states[state_id].packet_mask),
                int(state_id),
            )
        )
        if limit is not None:
            return candidate_ids[: int(limit)]
        return candidate_ids

    def lookup_cost_for_full_hypergraph_scan(self) -> int:
        return int(sum(len(cone) * 2 for cone in self.causal_cones))

    def immediate_candidates(self, state_id: int, *, last_action: int | None, coupled: bool) -> list[int]:
        if not coupled or last_action is None:
            return [action.index for action in self.actions]
        return sorted(set(self.neighbors[int(last_action)]))
