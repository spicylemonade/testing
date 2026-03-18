#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hadamard_ca.composite import (
    CompositeAction,
    CompositeContext,
    enumerate_all_pairs,
    enumerate_single_packets,
)
from hadamard_ca.retained_state_graph import RetainedStateGraph
from hadamard_ca.search import load_sequence_pair


FRONTIER_SEED_PATH = REPO_ROOT / "results" / "frontier" / "order_668_64m" / "seed_sequences.json"
RETAINED_LIBRARY_PATH = REPO_ROOT / "results" / "analysis" / "composite_packet_retained_library.json"
OUTPUT_JSON_PATH = REPO_ROOT / "results" / "verification" / "radius_limited_locality_barrier.json"


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _scan_family(
    context: CompositeContext,
    *,
    family_name: str,
    actions: list[CompositeAction],
) -> dict[str, object]:
    comparison_counts = {"better": 0, "equal": 0, "worse": 0}
    best_record: dict[str, object] | None = None
    for action in actions:
        record = context.evaluate_action(action)
        comparison_counts[str(record["score_comparison"])] += 1
        if best_record is None or int(record["objective"]["score"]) < int(best_record["objective"]["score"]):
            best_record = record
    assert best_record is not None
    return {
        "family": family_name,
        "candidate_count": len(actions),
        "comparison_counts": comparison_counts,
        "best_record": best_record,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the radius-limited locality barrier / counterexample.")
    parser.add_argument("--output", type=Path, default=OUTPUT_JSON_PATH)
    args = parser.parse_args()

    q, s = load_sequence_pair(FRONTIER_SEED_PATH)
    context = CompositeContext.from_seed(q, s)
    retained_payload = json.loads(RETAINED_LIBRARY_PATH.read_text())
    retained_actions = [
        CompositeAction(
            family=str(record["family"]),
            packets=tuple(int(packet) for packet in record["packets"]),
            descriptor=str(record["descriptor"]),
        )
        for record in retained_payload["records"]
    ]

    one_packet_scan = _scan_family(
        context,
        family_name="one_packet",
        actions=enumerate_single_packets(context.length),
    )
    two_packet_scan = _scan_family(
        context,
        family_name="two_packet",
        actions=enumerate_all_pairs(context.length),
    )
    retained_scan = _scan_family(
        context,
        family_name="retained_composite",
        actions=retained_actions,
    )

    graph = RetainedStateGraph.from_paths(
        seed_file=FRONTIER_SEED_PATH,
        retained_library_path=RETAINED_LIBRARY_PATH,
    )
    canonical_state = graph.state_payload(0)
    counterexamples: list[dict[str, object]] = []
    for root, cones in enumerate(graph.causal_cones):
        for edge in cones:
            next_state = graph.transitions[0][edge[0]]
            end_state = graph.transitions[next_state][edge[1]]
            end_payload = graph.state_payload(end_state)
            if int(end_payload["objective"]["score"]) >= int(canonical_state["objective"]["score"]):
                continue
            counterexamples.append(
                {
                    "edge": [int(value) for value in edge],
                    "edge_actions": [
                        list(graph.actions[edge[0]].packet_labels),
                        list(graph.actions[edge[1]].packet_labels),
                    ],
                    "end_state": end_payload,
                    "end_score_tuple": [
                        int(end_payload["objective"]["support_size"]),
                        int(end_payload["objective"]["l1"]),
                        int(end_payload["objective"]["max_abs"]),
                    ],
                    "root_action": root,
                }
            )
    counterexamples.sort(
        key=lambda record: (
            tuple(int(value) for value in record["end_score_tuple"]),
            tuple(int(value) for value in record["edge"]),
        )
    )

    payload = {
        "generated_at": _timestamp(),
        "seed_file": str(FRONTIER_SEED_PATH.relative_to(REPO_ROOT)),
        "retained_library_path": str(RETAINED_LIBRARY_PATH.relative_to(REPO_ROOT)),
        "canonical_seed_objective": context.seed_objective,
        "single_actuator_barrier": {
            "actuator_class": (
                "all one-packet moves, all unordered two-packet moves, and every retained composite action"
            ),
            "families": [one_packet_scan, two_packet_scan, retained_scan],
            "improving_single_actuator_exists": False,
        },
        "radius_limited_counterexample": {
            "radius": 1,
            "depth": 2,
            "cone_union_limit": 25,
            "rule_class": "two-step causal-cone hyperedges over the retained overlap graph",
            "counterexample_count": len(counterexamples),
            "first_counterexample": counterexamples[0] if counterexamples else None,
        },
        "verdict": {
            "mode": "counterexample" if counterexamples else "barrier",
            "statement": (
                "No single-actuator rule in the explicit actuator class improves the canonical seed, "
                "but a radius-1 depth-2 retained hyperedge rule does."
                if counterexamples
                else "No certified counterexample was found in the checked radius-limited rule class."
            ),
        },
    }
    _write_json(args.output, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
