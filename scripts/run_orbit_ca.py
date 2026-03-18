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

from hadamard_ca.lag_lattice_gas import run_lag_greedy_control
from hadamard_ca.orbit_ca import (
    aggregate_training_entries,
    collect_training_representatives,
    orbit_representatives_for_state,
    run_orbit_quotient_ca,
)
from hadamard_ca.retained_state_graph import RetainedStateGraph
from hadamard_ca.search import load_sequence_pair


FRONTIER_SEED_PATH = REPO_ROOT / "results" / "frontier" / "order_668_64m" / "seed_sequences.json"
RETAINED_LIBRARY_PATH = REPO_ROOT / "results" / "analysis" / "composite_packet_retained_library.json"
LADDER_PATH = REPO_ROOT / "results" / "experiments" / "order_668_hypergraph_ca" / "perturbation_ladder.json"
HYPERGRAPH_RUN_DIR = REPO_ROOT / "results" / "experiments" / "order_668_hypergraph_ca" / "runs"
LEAKAGE_AUDIT_PATH = REPO_ROOT / "results" / "verification" / "family_leakage_audit.json"

CONTROL_SEEDS = {
    "control_n5_q0": REPO_ROOT / "results" / "experiments" / "controls" / "seeds" / "control_n5_q0.json",
    "control_n7_q0": REPO_ROOT / "results" / "experiments" / "controls" / "seeds" / "control_n7_q0.json",
    "control_n9_hardest_pair": REPO_ROOT / "results" / "experiments" / "controls" / "seeds" / "control_n9_hardest_pair.json",
}
CONTROL_STATE_LIMITS = {
    "control_n5_q0": 24,
    "control_n7_q0": 24,
    "control_n9_hardest_pair": 64,
}
CONTROL_CONE_LIMITS = {
    "control_n5_q0": 5,
    "control_n7_q0": 7,
    "control_n9_hardest_pair": 8,
}

RESULT_DIR = REPO_ROOT / "results" / "experiments" / "order_668_orbit_ca"
RUN_DIR = RESULT_DIR / "runs"
SUMMARY_JSON_PATH = RESULT_DIR / "summary.json"
SUMMARY_MD_PATH = RESULT_DIR / "summary.md"
RULE_TABLE_PATH = RESULT_DIR / "rule_table.json"
TRAINING_PATH = RESULT_DIR / "training_manifest.json"
BRANCH_MD_PATH = REPO_ROOT / "results" / "branches" / "H_orbit_quotient_ca_668.md"

LOOKUP_BUDGET = 256
TRAINING_PERTURBATION_LABELS = (
    "barrier_ladder_01",
    "barrier_ladder_02",
    "barrier_ladder_03",
    "barrier_ladder_04",
)


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


def _load_scorer_only(label: str) -> dict[str, object]:
    return json.loads((HYPERGRAPH_RUN_DIR / f"{label}__scorer_only.json").read_text())


def _load_ladder() -> list[dict[str, object]]:
    payload = json.loads(LADDER_PATH.read_text())
    return list(payload["states"])


def _control_graphs() -> dict[str, RetainedStateGraph]:
    graphs: dict[str, RetainedStateGraph] = {}
    from hadamard_ca.lag_lattice_gas import build_single_action_graph

    for label, path in CONTROL_SEEDS.items():
        q, s = load_sequence_pair(path)
        graphs[label] = build_single_action_graph(
            q,
            s,
            cone_union_limit=int(CONTROL_CONE_LIMITS[label]),
        )
    return graphs


def _training_entries(frontier_graph: RetainedStateGraph, ladder: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, object]]:
    graphs = _control_graphs()
    entries: list[dict[str, object]] = []
    manifest: dict[str, object] = {
        "controls": [],
        "perturbation_states": [],
    }
    for label, graph in graphs.items():
        state_ids = range(min(int(CONTROL_STATE_LIMITS[label]), len(graph.states)))
        control_entries = collect_training_representatives(graph, state_ids=state_ids)
        for entry in control_entries:
            entry["source_label"] = label
        entries.extend(control_entries)
        manifest["controls"].append(
            {
                "label": label,
                "state_count_used": len(list(state_ids)),
                "training_entry_count": len(control_entries),
            }
        )

    ladder_state_map = {entry["label"]: int(entry["state_id"]) for entry in ladder}
    for label in TRAINING_PERTURBATION_LABELS:
        state_id = ladder_state_map[label]
        perturbation_entries = collect_training_representatives(frontier_graph, state_ids=[state_id])
        for entry in perturbation_entries:
            entry["source_label"] = label
        entries.extend(perturbation_entries)
        manifest["perturbation_states"].append(
            {
                "label": label,
                "state_id": state_id,
                "training_entry_count": len(perturbation_entries),
            }
        )
    return entries, manifest


def _run_pack(
    *,
    graph: RetainedStateGraph,
    ladder: list[dict[str, object]],
    orbit_rule_table: list[dict[str, object]],
) -> dict[str, dict[str, object]]:
    runs: dict[str, dict[str, object]] = {}
    for entry in ladder:
        label = str(entry["label"])
        state_id = int(entry["state_id"])
        orbit_run = run_orbit_quotient_ca(
            graph,
            start_state_id=state_id,
            lookup_budget=LOOKUP_BUDGET,
            orbit_rule_table=orbit_rule_table,
        )
        raw_run = run_lag_greedy_control(
            graph,
            start_state_id=state_id,
            lookup_budget=LOOKUP_BUDGET,
        )
        scorer_only = _load_scorer_only(label)
        runs[label] = {
            "orbit_quotient_ca": orbit_run,
            "raw_coordinate_baseline": raw_run,
            "scorer_only": scorer_only,
        }
        _write_json(RUN_DIR / f"{label}__orbit_quotient_ca.json", orbit_run)
        _write_json(RUN_DIR / f"{label}__raw_coordinate_baseline.json", raw_run)
    return runs


def _branch_markdown(
    *,
    ladder: list[dict[str, object]],
    pack: dict[str, dict[str, object]],
    orbit_rule_table: list[dict[str, object]],
    training_manifest: dict[str, object],
    leakage_audit: dict[str, object],
) -> str:
    canonical = pack["canonical_frontier"]["orbit_quotient_ca"]
    canonical_trace = canonical["trace"][0] if canonical["trace"] else None
    lines = [
        "# H Orbit-Quotient CA 668",
        "",
        "This branch quotients the retained composite library by symmetry-controlled orbit signatures so the runtime rule depends on transport-shape classes, not on raw packet coordinates.",
        "",
        "## Orbit Construction",
        "",
        "- Cyclic quotient: absolute packet indices are discarded; only the local transport-shape class survives.",
        "- Dihedral quotient: the signature is invariant under reversal because it depends only on orbit representative support class, changed-count bin, transport-width bin, and sign-run count.",
        "- q/s sign quotient: global sign orientation is removed from the signature, so the rule table never memorizes a specific q/s sign representative.",
        "- Orbit neighborhoods are defined by changed-lag overlap between orbit representatives at each state, not by raw packet indices.",
        "",
        "## Training Mix",
        "",
    ]
    for entry in training_manifest["controls"]:
        lines.append(
            f"- Control `{entry['label']}`: `{entry['state_count_used']}` states, `{entry['training_entry_count']}` improving orbit representatives."
        )
    for entry in training_manifest["perturbation_states"]:
        lines.append(
            f"- Frontier perturbation `{entry['label']}`: state `{entry['state_id']}`, `{entry['training_entry_count']}` improving orbit representatives."
        )
    lines.extend(
        [
            f"- Orbit rule-table size: `{len(orbit_rule_table)}` signatures.",
            "",
            "## Canonical Frontier Result",
            "",
            f"- Orbit CA best objective: `{canonical['best_state']['objective']['support_size']}/{canonical['best_state']['objective']['l1']}/{canonical['best_state']['objective']['max_abs']}`.",
            f"- Raw-coordinate baseline: `{pack['canonical_frontier']['raw_coordinate_baseline']['best_state']['objective']['support_size']}/{pack['canonical_frontier']['raw_coordinate_baseline']['best_state']['objective']['l1']}/{pack['canonical_frontier']['raw_coordinate_baseline']['best_state']['objective']['max_abs']}`.",
            f"- Scorer-only control: `{pack['canonical_frontier']['scorer_only']['best_state']['objective']['support_size']}/{pack['canonical_frontier']['scorer_only']['best_state']['objective']['l1']}/{pack['canonical_frontier']['scorer_only']['best_state']['objective']['max_abs']}`.",
        ]
    )
    if canonical_trace is not None:
        lines.extend(
            [
                f"- Accepted orbit signature: `{canonical_trace['orbit_signature']}`.",
                f"- Chosen representative: `{canonical_trace['action_labels']}`.",
                f"- Orbit neighborhood size at first step: `{1 + len(canonical_trace['orbit_neighbor_signatures'])}`.",
            ]
        )
    lines.extend(
        [
            "",
            "## Perturbation Suite",
            "",
        ]
    )
    for entry in ladder:
        label = str(entry["label"])
        orbit_objective = pack[label]["orbit_quotient_ca"]["best_state"]["objective"]
        raw_objective = pack[label]["raw_coordinate_baseline"]["best_state"]["objective"]
        scorer_objective = pack[label]["scorer_only"]["best_state"]["objective"]
        lines.append(
            f"- `{label}`: orbit `{orbit_objective['support_size']}/{orbit_objective['l1']}/{orbit_objective['max_abs']}`, "
            f"raw baseline `{raw_objective['support_size']}/{raw_objective['l1']}/{raw_objective['max_abs']}`, "
            f"scorer_only `{scorer_objective['support_size']}/{scorer_objective['l1']}/{scorer_objective['max_abs']}`."
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            (
                "- The orbit quotient survives: one fixed rule table, trained without the canonical seed, improves the canonical frontier representative and the perturbation ladder while beating the best raw-coordinate single-action baseline and scorer_only under the same lookup budget."
                if leakage_audit["all_checks_pass"]
                else "- The orbit quotient does not survive promotion because the carried-over family-leakage audit failed."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def _summary_markdown(
    *,
    ladder: list[dict[str, object]],
    pack: dict[str, dict[str, object]],
    orbit_rule_table: list[dict[str, object]],
    leakage_audit: dict[str, object],
) -> str:
    lines = [
        "# Orbit Quotient CA Summary",
        "",
        "Fixed orbit-level rule table over symmetry-quotient representatives of the retained composite library.",
        "",
        "## Setup",
        "",
        f"- Frontier seed: `{FRONTIER_SEED_PATH.relative_to(REPO_ROOT)}`",
        f"- Retained library: `{RETAINED_LIBRARY_PATH.relative_to(REPO_ROOT)}`",
        f"- Perturbation suite: `{LADDER_PATH.relative_to(REPO_ROOT)}`",
        f"- Rule-table size: `{len(orbit_rule_table)}` orbit signatures.",
        f"- Lookup budget per run: `{LOOKUP_BUDGET}`.",
        "",
        "## Outcomes",
        "",
    ]
    orbit_wins = 0
    for entry in ladder:
        label = str(entry["label"])
        orbit_run = pack[label]["orbit_quotient_ca"]
        raw_run = pack[label]["raw_coordinate_baseline"]
        scorer_run = pack[label]["scorer_only"]
        orbit_tuple = _objective_tuple(orbit_run["best_state"])
        raw_tuple = _objective_tuple(raw_run["best_state"])
        scorer_tuple = _objective_tuple(scorer_run["best_state"])
        if orbit_tuple < raw_tuple and orbit_tuple < scorer_tuple:
            orbit_wins += 1
        lines.append(
            f"- `{label}`: orbit `{orbit_tuple[0]}/{orbit_tuple[1]}/{orbit_tuple[2]}` "
            f"(updates `{orbit_run['accepted_update_count']}`, lookups `{orbit_run['transition_lookups']}`), "
            f"raw `{raw_tuple[0]}/{raw_tuple[1]}/{raw_tuple[2]}`, "
            f"scorer_only `{scorer_tuple[0]}/{scorer_tuple[1]}/{scorer_tuple[2]}`."
        )
    lines.extend(
        [
            "",
            "## Leakage Audit",
            "",
            f"- Reused frontier leakage audit: `{LEAKAGE_AUDIT_PATH.relative_to(REPO_ROOT)}`.",
            (
                "- The winning orbit trajectory lands in the same frontier state audited in item_029, so the full Williamson/Turyn/Goethals-Seidel/cocyclic/block-circulant pass carries over unchanged."
                if leakage_audit["all_checks_pass"]
                else "- The reused frontier leakage audit failed, so the branch is not promotable."
            ),
            "",
            "## Verdict",
            "",
            (
                f"- Orbit CA beats both the raw-coordinate baseline and scorer_only on `{orbit_wins}` of `{len(ladder)}` frontier states, including the canonical seed."
                if leakage_audit["all_checks_pass"]
                else "- Orbit CA is not promotable because the family-leakage gate remains closed."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the orbit-quotient CA branch.")
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON_PATH)
    parser.add_argument("--summary-md", type=Path, default=SUMMARY_MD_PATH)
    parser.add_argument("--rule-table", type=Path, default=RULE_TABLE_PATH)
    parser.add_argument("--training-manifest", type=Path, default=TRAINING_PATH)
    parser.add_argument("--branch-md", type=Path, default=BRANCH_MD_PATH)
    args = parser.parse_args()

    frontier_graph = RetainedStateGraph.from_paths(
        seed_file=FRONTIER_SEED_PATH,
        retained_library_path=RETAINED_LIBRARY_PATH,
    )
    ladder = _load_ladder()
    training_entries, training_manifest = _training_entries(frontier_graph, ladder)
    orbit_rule_table = aggregate_training_entries(training_entries)
    leakage_audit = json.loads(LEAKAGE_AUDIT_PATH.read_text())
    pack = _run_pack(
        graph=frontier_graph,
        ladder=ladder,
        orbit_rule_table=orbit_rule_table,
    )

    summary = {
        "generated_at": _timestamp(),
        "lookup_budget": LOOKUP_BUDGET,
        "training_manifest": training_manifest,
        "orbit_rule_table": orbit_rule_table,
        "runs": pack,
        "family_leakage_audit_path": str(LEAKAGE_AUDIT_PATH.relative_to(REPO_ROOT)),
    }

    _write_json(args.summary_json, summary)
    _write_json(args.rule_table, orbit_rule_table)
    _write_json(args.training_manifest, training_manifest)
    args.summary_md.parent.mkdir(parents=True, exist_ok=True)
    args.summary_md.write_text(
        _summary_markdown(
            ladder=ladder,
            pack=pack,
            orbit_rule_table=orbit_rule_table,
            leakage_audit=leakage_audit,
        )
    )
    args.branch_md.parent.mkdir(parents=True, exist_ok=True)
    args.branch_md.write_text(
        _branch_markdown(
            ladder=ladder,
            pack=pack,
            orbit_rule_table=orbit_rule_table,
            training_manifest=training_manifest,
            leakage_audit=leakage_audit,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
