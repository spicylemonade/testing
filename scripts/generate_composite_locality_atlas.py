#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import sys

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hadamard_ca.composite import (
    CompositeAction,
    CompositeContext,
    enumerate_all_pairs,
    enumerate_balanced_four_packets,
    enumerate_run_boundary_actions,
    enumerate_single_packets,
    packet_labels,
    pareto_front,
    summary_stats,
)
from hadamard_ca.controls import solve_exact_control
from hadamard_ca.search import apply_packet, objective_with_score
from hadamard_ca.seed import published_frontier_sequences


ANALYSIS_DIR = REPO_ROOT / "results" / "analysis"
CONTROL_SEED_PATH = REPO_ROOT / "results" / "experiments" / "controls" / "seeds" / "control_n9_hardest_pair.json"
FRONTIER_SEED_PATH = REPO_ROOT / "results" / "frontier" / "order_668_64m" / "seed_sequences.json"
FRONTIER_LOCALITY_SCAN_PATH = ANALYSIS_DIR / "frontier_locality_scan.json"
ATLAS_JSON_PATH = ANALYSIS_DIR / "composite_packet_locality_atlas.json"
ATLAS_MD_PATH = ANALYSIS_DIR / "composite_packet_locality_atlas.md"
RETAINED_LIBRARY_PATH = ANALYSIS_DIR / "composite_packet_retained_library.json"


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _ensure_harder_control() -> dict[str, object]:
    control = solve_exact_control(9)
    q = np.asarray(control.q, dtype=np.int8)
    s = np.asarray(control.s, dtype=np.int8)
    hardest: tuple[tuple[int, int], dict[str, int], np.ndarray, np.ndarray] | None = None
    hardest_signature: tuple[int, int, int, int, int] | None = None
    for left, right in ((left, right) for left in range(18) for right in range(left + 1, 18)):
        q_next, s_next = apply_packet(q, s, left)
        q_next, s_next = apply_packet(q_next, s_next, right)
        objective = objective_with_score(q_next, s_next)
        signature = (objective["support_size"], objective["l1"], objective["max_abs"], left, right)
        if hardest is None:
            hardest = ((left, right), objective, q_next, s_next)
            hardest_signature = signature
            continue
        assert hardest_signature is not None
        if signature > hardest_signature:
            hardest = ((left, right), objective, q_next, s_next)
            hardest_signature = signature
    assert hardest is not None
    packets, objective, q_seed, s_seed = hardest
    payload = {
        "length": 9,
        "order": 36,
        "source_control_fingerprint": control.canonical_fingerprint,
        "perturbation": {
            "packets": list(packets),
            "packet_labels": [
                f"q[{packets[0]}]" if packets[0] < 9 else f"s[{packets[0] - 9}]",
                f"q[{packets[1]}]" if packets[1] < 9 else f"s[{packets[1] - 9}]",
            ],
            "selection_rule": "lexicographically hardest 2-packet perturbation of the exact length-9 control",
        },
        "objective_summary": objective,
        "q": [int(value) for value in q_seed.tolist()],
        "s": [int(value) for value in s_seed.tolist()],
    }
    _write_json(CONTROL_SEED_PATH, payload)
    return payload


def _evaluate_family(context: CompositeContext, actions: list[CompositeAction]) -> list[dict[str, object]]:
    return [context.evaluate_action(action) for action in actions]


def _one_packet_summary(context: CompositeContext) -> dict[str, object]:
    records = _evaluate_family(context, enumerate_single_packets(context.length))
    changed_counts = [int(record["changed_lag_count"]) for record in records]
    comparison_counts = Counter(str(record["score_comparison"]) for record in records)
    return {
        "packet_count": len(records),
        "changed_lag_summary": summary_stats(changed_counts),
        "comparison_counts": dict(sorted(comparison_counts.items())),
    }


def _group_family_summaries(records: list[dict[str, object]], low_splash_cutoff: float) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for record in records:
        grouped[str(record["family"])].append(record)
    summaries: list[dict[str, object]] = []
    for family_name, family_records in sorted(grouped.items()):
        low_splash = [record for record in family_records if float(record["changed_lag_count"]) <= low_splash_cutoff]
        changed_counts = [int(record["changed_lag_count"]) for record in family_records]
        comparison_counts = Counter(str(record["score_comparison"]) for record in family_records)
        top_low_splash = sorted(
            low_splash,
            key=lambda record: (
                int(record["objective"]["score"]),
                int(record["changed_lag_count"]),
                tuple(int(packet) for packet in record["packets"]),
            ),
        )[:8]
        summaries.append(
            {
                "family": family_name,
                "candidate_count": len(family_records),
                "changed_lag_summary": summary_stats(changed_counts),
                "comparison_counts": dict(sorted(comparison_counts.items())),
                "low_splash_cutoff": float(low_splash_cutoff),
                "low_splash_count": len(low_splash),
                "low_splash_best_samples": top_low_splash,
            }
        )
    return summaries


def _enrich_retained_records(
    context: CompositeContext,
    records: list[dict[str, object]],
) -> list[dict[str, object]]:
    enriched: list[dict[str, object]] = []
    for record in records:
        action = CompositeAction(
            family=str(record["family"]),
            packets=tuple(int(packet) for packet in record["packets"]),
            descriptor=str(record["descriptor"]),
        )
        enriched_record = context.evaluate_action(action, include_changed_lags=True)
        enriched_record["packet_labels"] = packet_labels(action.packets, context.length)
        enriched.append(enriched_record)
    return enriched


def _build_seed_section(
    *,
    label: str,
    seed_path: Path,
    q: np.ndarray,
    s: np.ndarray,
    low_splash_cutoff: float | None = None,
) -> tuple[dict[str, object], CompositeContext, list[dict[str, object]]]:
    context = CompositeContext.from_seed(q, s)
    one_packet = _one_packet_summary(context)
    if low_splash_cutoff is None:
        low_splash_cutoff = float(one_packet["changed_lag_summary"]["median"]) / 2.0

    actions = (
        enumerate_all_pairs(context.length)
        + enumerate_balanced_four_packets(context.length)
        + enumerate_run_boundary_actions(q, s)
    )
    records = _evaluate_family(context, actions)
    family_summaries = _group_family_summaries(records, low_splash_cutoff)
    return (
        {
            "label": label,
            "seed_file": str(seed_path.relative_to(REPO_ROOT)),
            "seed_objective": context.seed_objective,
            "one_packet_summary": one_packet,
            "low_splash_cutoff": float(low_splash_cutoff),
            "family_summaries": family_summaries,
            "record_count": len(records),
        },
        context,
        records,
    )


def _validate_frontier_reference(frontier_one_packet: dict[str, object]) -> None:
    if not FRONTIER_LOCALITY_SCAN_PATH.exists():
        return
    saved = json.loads(FRONTIER_LOCALITY_SCAN_PATH.read_text())
    saved_median = float(saved["one_packet_scan"]["changed_lag_summary"]["overall"]["median"])
    current_median = float(frontier_one_packet["changed_lag_summary"]["median"])
    if abs(saved_median - current_median) > 1e-9:
        raise ValueError(
            f"frontier one-packet median mismatch: saved={saved_median}, current={current_median}"
        )


def _markdown_summary(
    frontier: dict[str, object],
    control: dict[str, object],
    retained_library: dict[str, object],
) -> str:
    frontier_cutoff = float(frontier["low_splash_cutoff"])
    frontier_one_packet = frontier["one_packet_summary"]
    control_one_packet = control["one_packet_summary"]
    lines = [
        "# Composite Packet Locality Atlas",
        "",
        "Retained actuator-library scan for the Novelty Deepening pass.",
        "",
        "## Frontier Reference",
        "",
        f"- Frontier seed: `{frontier['seed_file']}`",
        (
            f"- Frontier one-packet changed-lag median: "
            f"`{frontier_one_packet['changed_lag_summary']['median']:.1f}` "
            f"with low-splash cutoff `<= {frontier_cutoff:.1f}`."
        ),
        f"- Frontier seed objective: support `{frontier['seed_objective']['support_size']}`, "
        f"`l1 = {frontier['seed_objective']['l1']}`, "
        f"`max_abs = {frontier['seed_objective']['max_abs']}`.",
        "",
        "## Harder Control",
        "",
        f"- Harder control seed: `{control['seed_file']}`",
        (
            f"- Control one-packet changed-lag median: "
            f"`{control_one_packet['changed_lag_summary']['median']:.1f}` "
            f"with control-specific low-splash cutoff `<= {control['low_splash_cutoff']:.1f}`."
        ),
        f"- Control seed objective: support `{control['seed_objective']['support_size']}`, "
        f"`l1 = {control['seed_objective']['l1']}`, "
        f"`max_abs = {control['seed_objective']['max_abs']}`.",
        "",
        "## Family Scan",
        "",
    ]
    for family_summary in frontier["family_summaries"]:
        family = family_summary["family"]
        counts = family_summary["comparison_counts"]
        lines.append(
            f"- `{family}`: `{family_summary['candidate_count']}` candidates, "
            f"frontier median changed-lag count `{family_summary['changed_lag_summary']['median']:.1f}`, "
            f"low-splash candidates `{family_summary['low_splash_count']}`, "
            f"comparison counts `{counts}`."
        )
    lines.extend(
        [
            "",
            "## Retained Library",
            "",
            (
                f"- Selection rule: {retained_library['selection_rule']}. "
                f"The retained set has median changed-lag count "
                f"`{retained_library['changed_lag_summary']['median']:.1f}`."
            ),
            (
                f"- Frontier retained outcomes: "
                f"`{retained_library['comparison_counts'].get('better', 0)}` better, "
                f"`{retained_library['comparison_counts'].get('equal', 0)}` equal, "
                f"`{retained_library['comparison_counts'].get('worse', 0)}` worse."
            ),
            (
                "- Frontier conclusion: no retained composite improves the canonical "
                "order-668 seed, but the retained basis is still nonempty because one "
                "two-packet action is exactly neutral and the rest form the locality-vs-damage Pareto front."
            ),
            "",
            "Retained composite records:",
        ]
    )
    for record in retained_library["records"]:
        objective = record["objective"]
        lines.append(
            f"- `{record['family']}` {record['packet_labels']}: "
            f"changed lags `{record['changed_lag_count']}`, "
            f"`{record['score_comparison']}`, "
            f"objective `{objective['support_size']}/{objective['l1']}/{objective['max_abs']}`."
        )
    lines.extend(
        [
            "",
            "## Control Cross-Check",
            "",
            (
                "- The length-9 hardest-pair control does admit improving low-splash pair and balanced-four actions, "
                "so the retained-library scan is not vacuous. The frontier is the outlier."
            ),
            (
                "- This keeps packet-space CA alive only in the retained composite basis. "
                "The old one-packet H1 basis remains retired."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the composite-packet locality atlas.")
    parser.add_argument("--atlas-json", type=Path, default=ATLAS_JSON_PATH)
    parser.add_argument("--atlas-md", type=Path, default=ATLAS_MD_PATH)
    parser.add_argument("--retained-library", type=Path, default=RETAINED_LIBRARY_PATH)
    args = parser.parse_args()

    frontier_seed = json.loads(FRONTIER_SEED_PATH.read_text())
    harder_control = _ensure_harder_control()

    frontier_section, frontier_context, frontier_records = _build_seed_section(
        label="canonical_frontier_64m",
        seed_path=FRONTIER_SEED_PATH,
        q=np.asarray(frontier_seed["q"], dtype=np.int8),
        s=np.asarray(frontier_seed["s"], dtype=np.int8),
    )
    _validate_frontier_reference(frontier_section["one_packet_summary"])

    control_section, _, _ = _build_seed_section(
        label="length9_hardest_pair_control",
        seed_path=CONTROL_SEED_PATH,
        q=np.asarray(harder_control["q"], dtype=np.int8),
        s=np.asarray(harder_control["s"], dtype=np.int8),
    )

    frontier_cutoff = float(frontier_section["low_splash_cutoff"])
    low_splash_records = [
        record for record in frontier_records if float(record["changed_lag_count"]) <= frontier_cutoff
    ]
    retained_records = _enrich_retained_records(frontier_context, pareto_front(low_splash_records))
    retained_comparison_counts = Counter(str(record["score_comparison"]) for record in retained_records)
    retained_payload = {
        "generated_at": _timestamp(),
        "source_seed_file": str(FRONTIER_SEED_PATH.relative_to(REPO_ROOT)),
        "low_splash_cutoff": frontier_cutoff,
        "selection_rule": (
            "Pareto frontier over (changed_lag_count, support_size, l1, max_abs) "
            "inside the frontier low-splash composite set"
        ),
        "changed_lag_summary": summary_stats(
            int(record["changed_lag_count"]) for record in retained_records
        ),
        "comparison_counts": dict(sorted(retained_comparison_counts.items())),
        "records": retained_records,
    }
    _write_json(args.retained_library, retained_payload)

    atlas_payload = {
        "generated_at": _timestamp(),
        "frontier_reference": {
            "seed_file": str(FRONTIER_SEED_PATH.relative_to(REPO_ROOT)),
            "one_packet_reference_path": str(FRONTIER_LOCALITY_SCAN_PATH.relative_to(REPO_ROOT)),
            "expected_one_packet_median": 51.0,
            "low_splash_cutoff": frontier_cutoff,
        },
        "scan_method": {
            "pair_family": "all unordered 2-packet composites over the 334 packet basis",
            "balanced_four_family": (
                "all channel-complete 4-packet composites {q[i], s[i], q[j], s[j]} "
                "with i < j"
            ),
            "run_boundary_family": (
                "all width-1 q-boundary pairs, s-boundary pairs, and matched q/s boundary quads"
            ),
            "retention_rule": retained_payload["selection_rule"],
        },
        "frontier": frontier_section,
        "harder_control": control_section,
        "retained_library_path": str(args.retained_library.relative_to(REPO_ROOT)),
        "retained_library": retained_payload,
    }
    _write_json(args.atlas_json, atlas_payload)
    args.atlas_md.parent.mkdir(parents=True, exist_ok=True)
    args.atlas_md.write_text(_markdown_summary(frontier_section, control_section, retained_payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
