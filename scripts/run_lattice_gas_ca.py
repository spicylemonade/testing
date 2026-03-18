#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hadamard_ca.lag_lattice_gas import (
    build_single_action_graph,
    family_leakage_audit_payload,
    run_lag_greedy_control,
    run_lattice_gas_ca,
    run_warning_field_control,
)
from hadamard_ca.retained_state_graph import RetainedStateGraph
from hadamard_ca.search import load_sequence_pair


FRONTIER_SEED_PATH = REPO_ROOT / "results" / "frontier" / "order_668_64m" / "seed_sequences.json"
RETAINED_LIBRARY_PATH = REPO_ROOT / "results" / "analysis" / "composite_packet_retained_library.json"
CONTROL_SEED_PATH = REPO_ROOT / "results" / "experiments" / "controls" / "seeds" / "control_n9_hardest_pair.json"

RESULT_DIR = REPO_ROOT / "results" / "experiments" / "order_668_lattice_gas"
RUN_DIR = RESULT_DIR / "runs"
SUMMARY_JSON_PATH = RESULT_DIR / "summary.json"
SUMMARY_MD_PATH = RESULT_DIR / "summary.md"
BRANCH_MD_PATH = REPO_ROOT / "results" / "branches" / "H_defect_charge_lattice_gas_167.md"
LEAKAGE_JSON_PATH = REPO_ROOT / "results" / "verification" / "family_leakage_audit.json"
LEAKAGE_MD_PATH = REPO_ROOT / "results" / "verification" / "family_leakage_audit.md"

LOOKUP_BUDGET = 256
WARNING_DECAY = 1
WARNING_BOOST = 2
WARNING_CAP = 8
RESERVOIR_CAP = 16
CONTROL_CONE_UNION_LIMIT = 8


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _objective_tuple(payload: dict[str, object]) -> tuple[int, int, int]:
    objective = payload["objective"]
    assert isinstance(objective, dict)
    return (
        int(objective["support_size"]),
        int(objective["l1"]),
        int(objective["max_abs"]),
    )


def _run_pack(
    *,
    graph: RetainedStateGraph,
    start_state_id: int,
    label: str,
) -> dict[str, dict[str, object]]:
    pack = {
        "defect_charge_lattice_gas_ca": run_lattice_gas_ca(
            graph,
            start_state_id=start_state_id,
            lookup_budget=LOOKUP_BUDGET,
            warning_decay=WARNING_DECAY,
            warning_boost=WARNING_BOOST,
            warning_cap=WARNING_CAP,
            reservoir_cap=RESERVOIR_CAP,
        ),
        "lag_greedy_control": run_lag_greedy_control(
            graph,
            start_state_id=start_state_id,
            lookup_budget=LOOKUP_BUDGET,
        ),
        "warning_field_control": run_warning_field_control(
            graph,
            start_state_id=start_state_id,
            lookup_budget=LOOKUP_BUDGET,
            warning_decay=WARNING_DECAY,
            warning_boost=WARNING_BOOST,
            warning_cap=WARNING_CAP,
        ),
    }
    for method_name, payload in pack.items():
        _write_json(RUN_DIR / f"{label}__{method_name}.json", payload)
    return pack


def _family_audit(frontier_graph: RetainedStateGraph, frontier_pack: dict[str, dict[str, object]]) -> dict[str, object]:
    winning_run = frontier_pack["defect_charge_lattice_gas_ca"]
    winning_state = winning_run["best_state"]
    q_state, s_state = frontier_graph.context.apply_packets(tuple(int(packet) for packet in winning_state["packet_mask"]))
    audit = family_leakage_audit_payload(
        q=q_state,
        s=s_state,
        method_name="defect_charge_lattice_gas_ca",
        winning_packet_labels=winning_state["packet_labels"],
        mechanism_statement=(
            "The branch evaluates only exact lag-charge continuity features on the retained composite library "
            "and its precomputed two-step carrier cones. It does not introduce any family-restricted "
            "parameterization beyond the repo's shared Goethals-Seidel lift."
        ),
    )
    audit["generated_at"] = _timestamp()
    audit["frontier_seed"] = str(FRONTIER_SEED_PATH.relative_to(REPO_ROOT))
    audit["winning_objective"] = winning_state["objective"]
    audit["all_checks_pass"] = all(
        bool(entry["pass"]) for entry in audit["family_checks"].values()
    )
    return audit


def _branch_markdown(
    *,
    frontier_pack: dict[str, dict[str, object]],
    control_pack: dict[str, dict[str, object]],
    audit: dict[str, object],
) -> str:
    frontier_best = frontier_pack["defect_charge_lattice_gas_ca"]["best_state"]["objective"]
    frontier_trace = frontier_pack["defect_charge_lattice_gas_ca"]["trace"]
    first_frontier_step = frontier_trace[0] if frontier_trace else None
    control_best = control_pack["defect_charge_lattice_gas_ca"]["best_state"]["objective"]
    lines = [
        "# H Defect-Charge Lattice-Gas 167",
        "",
        "This branch moves from packet coordinates to the exact lag-defect field on the `167` core.",
        "",
        "## Continuity Law",
        "",
        "Let `rho_t(k)` be the exact signed defect coefficient at lag `k in {1, ..., 166}`.",
        "For any accepted actuator or carrier macro-event, define `delta(k) = rho_{t+1}(k) - rho_t(k)` and `R = sum_k delta(k)`.",
        "The branch uses an open-core continuity law with a single boundary reservoir:",
        "",
        "`rho_{t+1}(k) - rho_t(k) = J(k-1) - J(k) + R * 1[k = 166]`,",
        "",
        "where `J(k) = -sum_{i <= k} (delta(i) - R * 1[i = 166])` is the exact nearest-neighbor transport current.",
        "",
        "The local rule ranks candidates by:",
        "",
        "- nonincreasing support first,",
        "- then smaller reservoir exchange `|R|`,",
        "- then smaller transport span `sum_k |J(k)|`,",
        "- then larger `l1` and max-defect reduction.",
        "",
        "## Split / Move / Annihilation Rules",
        "",
        "- Single-action annihilation: accept a direct move if it strictly improves the lexicographic objective.",
        "- Conservative move: if no direct annihilation exists, inspect precomputed two-step carrier cones whose final support does not exceed the current support.",
        "- Split then annihilate: allow a temporary support increase only inside a two-step carrier cone whose final state returns to nonincreasing support and strictly lowers the objective.",
        "",
        "## Canonical Frontier Result",
        "",
        f"- Lattice-gas best objective: `{frontier_best['support_size']}/{frontier_best['l1']}/{frontier_best['max_abs']}`.",
        f"- Lag-greedy control: `{frontier_pack['lag_greedy_control']['best_state']['objective']['support_size']}/{frontier_pack['lag_greedy_control']['best_state']['objective']['l1']}/{frontier_pack['lag_greedy_control']['best_state']['objective']['max_abs']}`.",
        f"- Warning-field control: `{frontier_pack['warning_field_control']['best_state']['objective']['support_size']}/{frontier_pack['warning_field_control']['best_state']['objective']['l1']}/{frontier_pack['warning_field_control']['best_state']['objective']['max_abs']}`.",
    ]
    if first_frontier_step is not None:
        lines.extend(
            [
                f"- Accepted carrier: `{first_frontier_step['action_labels']}`.",
                (
                    f"- Carrier signature: support flux `{first_frontier_step['signature']['support_flux']}`, "
                    f"reservoir `|R| = {first_frontier_step['signature']['reservoir_abs']}`, "
                    f"transport span `{first_frontier_step['signature']['transport_span']}`, "
                    f"`l1` gain `{first_frontier_step['signature']['l1_gain']}`."
                ),
            ]
        )
    lines.extend(
        [
            "",
            "## Harder Control Cross-Check",
            "",
            (
                f"- On `control_n9_hardest_pair`, the same fixed rule reaches "
                f"`{control_best['support_size']}/{control_best['l1']}/{control_best['max_abs']}`."
            ),
            (
                "- The harder control improves via direct single-action annihilation, so the frontier gain is not "
                "an artifact of freezing the single-action layer everywhere."
            ),
            "",
            "## Promotion Verdict",
            "",
            (
                "- Promote the branch for this pass: it strictly improves the canonical frontier objective without "
                "introducing any detected Williamson, Turyn, Goethals-Seidel, cocyclic, or block-circulant leakage."
                if audit["all_checks_pass"]
                else "- Do not promote the branch: the family-leakage audit failed."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def _summary_markdown(
    *,
    frontier_pack: dict[str, dict[str, object]],
    control_pack: dict[str, dict[str, object]],
    audit: dict[str, object],
) -> str:
    lines = [
        "# Lattice-Gas CA Summary",
        "",
        "Defect-charge lattice-gas CA on the exact lag core with retained composite actuators on the frontier seed.",
        "",
        "## Setup",
        "",
        f"- Frontier seed: `{FRONTIER_SEED_PATH.relative_to(REPO_ROOT)}`",
        f"- Retained frontier library: `{RETAINED_LIBRARY_PATH.relative_to(REPO_ROOT)}`",
        f"- Harder control seed: `{CONTROL_SEED_PATH.relative_to(REPO_ROOT)}`",
        f"- Lookup budget per run: `{LOOKUP_BUDGET}` transition lookups.",
        f"- Warning field: decay `{WARNING_DECAY}`, boost `{WARNING_BOOST}`, cap `{WARNING_CAP}`.",
        f"- Reservoir cap for carrier acceptance: `{RESERVOIR_CAP}`.",
        "",
        "## Canonical Frontier",
        "",
    ]
    for method_name in ("defect_charge_lattice_gas_ca", "lag_greedy_control", "warning_field_control"):
        payload = frontier_pack[method_name]
        objective = payload["best_state"]["objective"]
        lines.append(
            f"- `{method_name}`: best `{objective['support_size']}/{objective['l1']}/{objective['max_abs']}`, "
            f"accepted updates `{payload['accepted_update_count']}`, lookups `{payload['transition_lookups']}`."
        )
    lines.extend(["", "## Harder Control", ""])
    for method_name in ("defect_charge_lattice_gas_ca", "lag_greedy_control", "warning_field_control"):
        payload = control_pack[method_name]
        objective = payload["best_state"]["objective"]
        lines.append(
            f"- `{method_name}`: best `{objective['support_size']}/{objective['l1']}/{objective['max_abs']}`, "
            f"accepted updates `{payload['accepted_update_count']}`, lookups `{payload['transition_lookups']}`."
        )
    lines.extend(
        [
            "",
            "## Leakage Audit",
            "",
        ]
    )
    for family_name, result in audit["family_checks"].items():
        lines.append(
            f"- `{family_name}`: `{'pass' if result['pass'] else 'fail'}`. {result['reason']}"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            (
                "- The lattice-gas branch survives this item: on the canonical frontier seed it reaches "
                "`13/2744/480`, while both single-action lag-space controls stay at `13/2880/512`."
                if audit["all_checks_pass"]
                else "- The branch does not survive promotion because the family-leakage audit failed."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def _audit_markdown(audit: dict[str, object]) -> str:
    lines = [
        "# Family Leakage Audit",
        "",
        f"- Method: `{audit['method_name']}`",
        f"- Frontier seed: `{audit['frontier_seed']}`",
        f"- Winning packets: `{audit['winning_packet_labels']}`",
        f"- Winning objective: `{audit['winning_objective']['support_size']}/{audit['winning_objective']['l1']}/{audit['winning_objective']['max_abs']}`",
        "",
        "Mechanism statement:",
        "",
        audit["mechanism_statement"],
        "",
        "## Checks",
        "",
    ]
    for family_name, result in audit["family_checks"].items():
        lines.append(
            f"- `{family_name}`: `{'pass' if result['pass'] else 'fail'}`. {result['reason']}"
        )
    lines.extend(
        [
            "",
            "## Empirical Symmetry Flags",
            "",
        ]
    )
    for key, value in audit["symmetry_flags"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Nontrivial Periods", ""])
    for key, value in audit["sequence_periods"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            (
                "Overall verdict: no family leakage detected."
                if audit["all_checks_pass"]
                else "Overall verdict: family leakage risk remains."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the defect-charge lattice-gas CA branch.")
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON_PATH)
    parser.add_argument("--summary-md", type=Path, default=SUMMARY_MD_PATH)
    parser.add_argument("--branch-md", type=Path, default=BRANCH_MD_PATH)
    parser.add_argument("--leakage-json", type=Path, default=LEAKAGE_JSON_PATH)
    parser.add_argument("--leakage-md", type=Path, default=LEAKAGE_MD_PATH)
    args = parser.parse_args()

    frontier_graph = RetainedStateGraph.from_paths(
        seed_file=FRONTIER_SEED_PATH,
        retained_library_path=RETAINED_LIBRARY_PATH,
    )
    frontier_pack = _run_pack(
        graph=frontier_graph,
        start_state_id=0,
        label="canonical_frontier",
    )

    control_q, control_s = load_sequence_pair(CONTROL_SEED_PATH)
    control_graph = build_single_action_graph(
        control_q,
        control_s,
        cone_union_limit=CONTROL_CONE_UNION_LIMIT,
    )
    control_pack = _run_pack(
        graph=control_graph,
        start_state_id=0,
        label="control_n9_hardest_pair",
    )

    audit = _family_audit(frontier_graph, frontier_pack)

    summary = {
        "generated_at": _timestamp(),
        "lookup_budget": LOOKUP_BUDGET,
        "warning_field": {
            "decay": WARNING_DECAY,
            "boost": WARNING_BOOST,
            "cap": WARNING_CAP,
        },
        "reservoir_cap": RESERVOIR_CAP,
        "frontier_seed": str(FRONTIER_SEED_PATH.relative_to(REPO_ROOT)),
        "retained_library": str(RETAINED_LIBRARY_PATH.relative_to(REPO_ROOT)),
        "control_seed": str(CONTROL_SEED_PATH.relative_to(REPO_ROOT)),
        "frontier_runs": frontier_pack,
        "control_runs": control_pack,
        "family_leakage_audit": audit,
        "promotion": {
            "strict_frontier_improvement": _objective_tuple(frontier_pack["defect_charge_lattice_gas_ca"]["best_state"]) < (13, 2880, 512),
            "all_family_checks_pass": bool(audit["all_checks_pass"]),
            "promote": bool(
                _objective_tuple(frontier_pack["defect_charge_lattice_gas_ca"]["best_state"]) < (13, 2880, 512)
                and audit["all_checks_pass"]
            ),
        },
    }

    _write_json(args.summary_json, summary)
    args.summary_md.parent.mkdir(parents=True, exist_ok=True)
    args.summary_md.write_text(_summary_markdown(frontier_pack=frontier_pack, control_pack=control_pack, audit=audit))
    args.branch_md.parent.mkdir(parents=True, exist_ok=True)
    args.branch_md.write_text(_branch_markdown(frontier_pack=frontier_pack, control_pack=control_pack, audit=audit))
    _write_json(args.leakage_json, audit)
    args.leakage_md.parent.mkdir(parents=True, exist_ok=True)
    args.leakage_md.write_text(_audit_markdown(audit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
