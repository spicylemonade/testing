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

from hadamard_ca.lag_lattice_gas import build_single_action_graph
from hadamard_ca.orbit_ca import aggregate_training_entries, collect_training_representatives
from hadamard_ca.population_ca import (
    median_objective_payload,
    phase_label,
    run_population_self_stabilizing_ca,
    run_zero_coupling_population,
)
from hadamard_ca.retained_state_graph import RetainedStateGraph
from hadamard_ca.search import load_sequence_pair


FRONTIER_SEED_PATH = REPO_ROOT / "results" / "frontier" / "order_668_64m" / "seed_sequences.json"
RETAINED_LIBRARY_PATH = REPO_ROOT / "results" / "analysis" / "composite_packet_retained_library.json"
LADDER_PATH = REPO_ROOT / "results" / "experiments" / "order_668_hypergraph_ca" / "perturbation_ladder.json"
ORBIT_SUMMARY_PATH = REPO_ROOT / "results" / "experiments" / "order_668_orbit_ca" / "summary.json"
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

RESULT_DIR = REPO_ROOT / "results" / "experiments" / "order_668_population_ca"
RUN_DIR = RESULT_DIR / "runs"
SUMMARY_JSON_PATH = RESULT_DIR / "summary.json"
SUMMARY_MD_PATH = RESULT_DIR / "summary.md"
RULE_TABLE_PATH = RESULT_DIR / "rule_table.json"
TRAINING_PATH = RESULT_DIR / "training_manifest.json"
PHASE_MAP_MD_PATH = REPO_ROOT / "results" / "analysis" / "frontier_population_phase_map.md"
PHASE_MAP_JSON_PATH = REPO_ROOT / "results" / "analysis" / "frontier_population_phase_map.json"
BRANCH_MD_PATH = REPO_ROOT / "results" / "branches" / "H_population_self_stabilizing_ca_668.md"

LOOKUP_BUDGET = 256
SELECTED_SEEDS = (11, 13, 17, 19, 23)
PHASE_MAP_SEEDS = (11, 13, 17)

POPULATION_SIZE = 64
COUPLING_STRENGTH = 1.6
TEMPERATURE = 1.2
CONTRACTION_THRESHOLD = 0.42
MEMORY_MIX = 0.55
MAX_ROUNDS = 6

PHASE_COUPLINGS = (0.0, 0.8, 1.6)
PHASE_THRESHOLDS = (0.35, 0.42, 0.55)


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def _load_ladder() -> list[dict[str, object]]:
    payload = json.loads(LADDER_PATH.read_text())
    return list(payload["states"])


def _control_rule_table() -> tuple[list[dict[str, object]], dict[str, object]]:
    entries: list[dict[str, object]] = []
    manifest = {"controls": []}
    for label, path in CONTROL_SEEDS.items():
        q, s = load_sequence_pair(path)
        graph = build_single_action_graph(q, s, cone_union_limit=int(CONTROL_CONE_LIMITS[label]))
        state_ids = range(min(int(CONTROL_STATE_LIMITS[label]), len(graph.states)))
        training_entries = collect_training_representatives(graph, state_ids=state_ids)
        entries.extend(training_entries)
        manifest["controls"].append(
            {
                "label": label,
                "state_count_used": len(list(state_ids)),
                "training_entry_count": len(training_entries),
            }
        )
    return aggregate_training_entries(entries), manifest


def _load_raw_local_baselines() -> dict[str, dict[str, object]]:
    payload = json.loads(ORBIT_SUMMARY_PATH.read_text())
    return {
        label: runs["raw_coordinate_baseline"]
        for label, runs in payload["runs"].items()
    }


def _load_scorer_only(label: str) -> dict[str, object]:
    return json.loads((HYPERGRAPH_RUN_DIR / f"{label}__scorer_only.json").read_text())


def _run_seed_pack(
    *,
    graph: RetainedStateGraph,
    label: str,
    state_id: int,
    orbit_rule_table: list[dict[str, object]],
    seeds: tuple[int, ...],
    coupling_strength: float,
    contraction_threshold: float,
) -> dict[str, list[dict[str, object]]]:
    population_runs: list[dict[str, object]] = []
    zero_coupling_runs: list[dict[str, object]] = []
    for seed in seeds:
        population = run_population_self_stabilizing_ca(
            graph,
            start_state_id=state_id,
            lookup_budget=LOOKUP_BUDGET,
            orbit_rule_table=orbit_rule_table,
            rng_seed=seed,
            population_size=POPULATION_SIZE,
            coupling_strength=coupling_strength,
            temperature=TEMPERATURE,
            contraction_threshold=contraction_threshold,
            memory_mix=MEMORY_MIX,
            max_rounds_per_step=MAX_ROUNDS,
        )
        zero = run_zero_coupling_population(
            graph,
            start_state_id=state_id,
            lookup_budget=LOOKUP_BUDGET,
            orbit_rule_table=orbit_rule_table,
            rng_seed=seed,
            population_size=POPULATION_SIZE,
            temperature=TEMPERATURE,
            contraction_threshold=contraction_threshold,
            memory_mix=MEMORY_MIX,
            max_rounds_per_step=MAX_ROUNDS,
        )
        population_runs.append(population)
        zero_coupling_runs.append(zero)
        _write_json(RUN_DIR / f"{label}__population_seed_{seed}.json", population)
        _write_json(RUN_DIR / f"{label}__zero_coupling_seed_{seed}.json", zero)
    return {
        "population_self_stabilizing_ca": population_runs,
        "zero_coupling_population": zero_coupling_runs,
    }


def _phase_grid(
    *,
    graph: RetainedStateGraph,
    ladder: list[dict[str, object]],
    orbit_rule_table: list[dict[str, object]],
) -> dict[str, object]:
    cells: list[dict[str, object]] = []
    for coupling in PHASE_COUPLINGS:
        for threshold in PHASE_THRESHOLDS:
            labels: list[str] = []
            for entry in ladder:
                state_id = int(entry["state_id"])
                label = str(entry["label"])
                for seed in PHASE_MAP_SEEDS:
                    run = run_population_self_stabilizing_ca(
                        graph,
                        start_state_id=state_id,
                        lookup_budget=LOOKUP_BUDGET,
                        orbit_rule_table=orbit_rule_table,
                        rng_seed=seed,
                        population_size=POPULATION_SIZE,
                        coupling_strength=float(coupling),
                        temperature=TEMPERATURE,
                        contraction_threshold=float(threshold),
                        memory_mix=MEMORY_MIX,
                        max_rounds_per_step=MAX_ROUNDS,
                    )
                    labels.append(phase_label(run))
            contraction_count = sum(1 for label in labels if label == "contraction")
            total = len(labels)
            cells.append(
                {
                    "coupling_strength": float(coupling),
                    "contraction_threshold": float(threshold),
                    "contraction_fraction": float(contraction_count / max(1, total)),
                    "label": "contraction" if contraction_count > total / 2 else "diffusion",
                }
            )
    return {
        "generated_at": _timestamp(),
        "cells": cells,
        "selected_operating_point": {
            "coupling_strength": COUPLING_STRENGTH,
            "contraction_threshold": CONTRACTION_THRESHOLD,
        },
    }


def _phase_map_markdown(phase_map: dict[str, object]) -> str:
    rows = ["# Frontier Population Phase Map", "", "Contraction fraction over canonical frontier plus perturbation ladder, aggregated across seeds `11, 13, 17`.", "", "| coupling | threshold | contraction_fraction | label |", "| --- | --- | --- | --- |"]
    for cell in phase_map["cells"]:
        rows.append(
            f"| {cell['coupling_strength']:.2f} | {cell['contraction_threshold']:.2f} | {cell['contraction_fraction']:.3f} | {cell['label']} |"
        )
    rows.extend(
        [
            "",
            (
                f"Selected operating point: coupling `{phase_map['selected_operating_point']['coupling_strength']}`, "
                f"threshold `{phase_map['selected_operating_point']['contraction_threshold']}`."
            ),
        ]
    )
    return "\n".join(rows) + "\n"


def _summary_markdown(
    *,
    ladder: list[dict[str, object]],
    results: dict[str, dict[str, object]],
    leakage_audit: dict[str, object],
) -> str:
    lines = [
        "# Population CA Summary",
        "",
        "Self-stabilizing population CA over control-trained orbit representatives.",
        "",
        "## Setup",
        "",
        f"- Rule table trained on non-frontier controls only.",
        f"- RNG seeds: `{list(SELECTED_SEEDS)}`.",
        f"- Equal executed restart coverage: `{len(SELECTED_SEEDS)}` runs per state for both coupled and zero-coupling population methods.",
        f"- Population size `{POPULATION_SIZE}`, coupling `{COUPLING_STRENGTH}`, threshold `{CONTRACTION_THRESHOLD}`, temperature `{TEMPERATURE}`, memory mix `{MEMORY_MIX}`, max rounds `{MAX_ROUNDS}`.",
        "",
        "## Outcomes",
        "",
    ]
    wins_on_ladder = 0
    canonical_success = False
    for entry in ladder:
        label = str(entry["label"])
        payload = results[label]
        population = payload["population_median"]
        zero = payload["zero_coupling_median"]
        raw = payload["raw_local_baseline"]["best_state"]["objective"]
        scorer = payload["scorer_only"]["best_state"]["objective"]
        contraction_count = int(payload["population_contraction_count"])
        lines.append(
            f"- `{label}`: population median `{population['support_size']}/{population['l1']}/{population['max_abs']}`, "
            f"zero_coupling median `{zero['support_size']}/{zero['l1']}/{zero['max_abs']}`, "
            f"raw local `{raw['support_size']}/{raw['l1']}/{raw['max_abs']}`, "
            f"scorer_only `{scorer['support_size']}/{scorer['l1']}/{scorer['max_abs']}`, "
            f"population contractions `{contraction_count}/{len(SELECTED_SEEDS)}`."
        )
        pop_tuple = (population["support_size"], population["l1"], population["max_abs"])
        zero_tuple = (zero["support_size"], zero["l1"], zero["max_abs"])
        raw_tuple = (raw["support_size"], raw["l1"], raw["max_abs"])
        scorer_tuple = (scorer["support_size"], scorer["l1"], scorer["max_abs"])
        if label == "canonical_frontier":
            canonical_success = pop_tuple < zero_tuple and pop_tuple < raw_tuple and pop_tuple < scorer_tuple
            continue
        if pop_tuple < zero_tuple and pop_tuple < raw_tuple and pop_tuple < scorer_tuple:
            wins_on_ladder += 1
    success = bool(
        leakage_audit["all_checks_pass"]
        and canonical_success
        and wins_on_ladder > (len(ladder) - 1) // 2
    )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            (
                f"- The coupled population CA clears the item gate: canonical success = `{canonical_success}`, perturbation-suite wins = `{wins_on_ladder}` of `{len(ladder) - 1}`."
                if success
                else (
                    f"- The item fails honestly: canonical success = `{canonical_success}` and perturbation-suite wins = `{wins_on_ladder}` of `{len(ladder) - 1}`, "
                    "so the coupled population never separates from the zero-coupling ablation strongly enough to support a self-stabilization claim."
                )
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def _branch_markdown(
    *,
    training_manifest: dict[str, object],
    results: dict[str, dict[str, object]],
    phase_map: dict[str, object],
    leakage_audit: dict[str, object],
) -> str:
    canonical = results["canonical_frontier"]
    ladder_labels = [label for label in results if label != "canonical_frontier"]
    canonical_pop = canonical["population_median"]
    canonical_zero = canonical["zero_coupling_median"]
    canonical_raw = canonical["raw_local_baseline"]["best_state"]["objective"]
    canonical_scorer = canonical["scorer_only"]["best_state"]["objective"]
    canonical_success = (
        (canonical_pop["support_size"], canonical_pop["l1"], canonical_pop["max_abs"])
        < (canonical_zero["support_size"], canonical_zero["l1"], canonical_zero["max_abs"])
        and (canonical_pop["support_size"], canonical_pop["l1"], canonical_pop["max_abs"])
        < (canonical_raw["support_size"], canonical_raw["l1"], canonical_raw["max_abs"])
        and (canonical_pop["support_size"], canonical_pop["l1"], canonical_pop["max_abs"])
        < (canonical_scorer["support_size"], canonical_scorer["l1"], canonical_scorer["max_abs"])
    )
    ladder_wins = 0
    for label in ladder_labels:
        payload = results[label]
        pop = payload["population_median"]
        zero = payload["zero_coupling_median"]
        raw = payload["raw_local_baseline"]["best_state"]["objective"]
        scorer = payload["scorer_only"]["best_state"]["objective"]
        if (
            (pop["support_size"], pop["l1"], pop["max_abs"])
            < (zero["support_size"], zero["l1"], zero["max_abs"])
            and (pop["support_size"], pop["l1"], pop["max_abs"])
            < (raw["support_size"], raw["l1"], raw["max_abs"])
            and (pop["support_size"], pop["l1"], pop["max_abs"])
            < (scorer["support_size"], scorer["l1"], scorer["max_abs"])
        ):
            ladder_wins += 1
    success = bool(
        leakage_audit["all_checks_pass"]
        and canonical_success
        and ladder_wins > len(ladder_labels) // 2
    )
    lines = [
        "# H Population Self-Stabilizing CA 668",
        "",
        "This branch keeps the rule table fixed from non-frontier controls and adds a stochastic population layer that must self-contract onto one orbit class before any frontier update is accepted.",
        "",
        "## Control-Only Rule Table",
        "",
    ]
    for entry in training_manifest["controls"]:
        lines.append(
            f"- `{entry['label']}`: `{entry['state_count_used']}` control states, `{entry['training_entry_count']}` improving representatives."
        )
    lines.extend(
        [
            "",
            "## Self-Stabilization Rule",
            "",
            "- Each step forms a population over the current orbit representatives.",
            "- Coupling reinforces previously concentrated votes across neighboring orbit classes.",
            "- An update is accepted only after the population crosses the contraction threshold; otherwise the run is classified as diffusion and stops.",
            "",
            "## Canonical Frontier Result",
            "",
            f"- Population median: `{canonical['population_median']['support_size']}/{canonical['population_median']['l1']}/{canonical['population_median']['max_abs']}`.",
            f"- Zero-coupling median: `{canonical['zero_coupling_median']['support_size']}/{canonical['zero_coupling_median']['l1']}/{canonical['zero_coupling_median']['max_abs']}`.",
            f"- Raw local baseline: `{canonical['raw_local_baseline']['best_state']['objective']['support_size']}/{canonical['raw_local_baseline']['best_state']['objective']['l1']}/{canonical['raw_local_baseline']['best_state']['objective']['max_abs']}`.",
            f"- Scorer-only: `{canonical['scorer_only']['best_state']['objective']['support_size']}/{canonical['scorer_only']['best_state']['objective']['l1']}/{canonical['scorer_only']['best_state']['objective']['max_abs']}`.",
            f"- Population contractions: `{canonical['population_contraction_count']}/{len(SELECTED_SEEDS)}` seeds.",
            "",
            "## Phase Map",
            "",
            (
                f"- Selected operating point: coupling `{phase_map['selected_operating_point']['coupling_strength']}`, "
                f"threshold `{phase_map['selected_operating_point']['contraction_threshold']}`."
            ),
            f"- Phase map artifact: `{PHASE_MAP_MD_PATH.relative_to(REPO_ROOT)}`.",
            "",
            "## Verdict",
            "",
            (
                "- The population branch survives: one fixed control-trained rule table beats zero_coupling, scorer_only, and the best deterministic local baseline on the canonical seed and on a strict majority of the perturbation ladder, while the carried-over family-leakage audit remains clean."
                if success
                else (
                    f"- The population branch fails honestly. Canonical success = `{canonical_success}` and perturbation-suite wins = `{ladder_wins}` of `{len(ladder_labels)}` after equal seed coverage, so the coupled rule never establishes a robust self-stabilizing advantage over zero_coupling."
                )
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the population self-stabilizing CA branch.")
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON_PATH)
    parser.add_argument("--summary-md", type=Path, default=SUMMARY_MD_PATH)
    parser.add_argument("--rule-table", type=Path, default=RULE_TABLE_PATH)
    parser.add_argument("--training-manifest", type=Path, default=TRAINING_PATH)
    parser.add_argument("--phase-map-json", type=Path, default=PHASE_MAP_JSON_PATH)
    parser.add_argument("--phase-map-md", type=Path, default=PHASE_MAP_MD_PATH)
    parser.add_argument("--branch-md", type=Path, default=BRANCH_MD_PATH)
    args = parser.parse_args()

    frontier_graph = RetainedStateGraph.from_paths(
        seed_file=FRONTIER_SEED_PATH,
        retained_library_path=RETAINED_LIBRARY_PATH,
    )
    ladder = _load_ladder()
    orbit_rule_table, training_manifest = _control_rule_table()
    raw_local_baselines = _load_raw_local_baselines()
    leakage_audit = json.loads(LEAKAGE_AUDIT_PATH.read_text())

    results: dict[str, dict[str, object]] = {}
    for entry in ladder:
        label = str(entry["label"])
        state_id = int(entry["state_id"])
        seed_pack = _run_seed_pack(
            graph=frontier_graph,
            label=label,
            state_id=state_id,
            orbit_rule_table=orbit_rule_table,
            seeds=SELECTED_SEEDS,
            coupling_strength=COUPLING_STRENGTH,
            contraction_threshold=CONTRACTION_THRESHOLD,
        )
        population_median = median_objective_payload(seed_pack["population_self_stabilizing_ca"])
        zero_median = median_objective_payload(seed_pack["zero_coupling_population"])
        results[label] = {
            "population_runs": seed_pack["population_self_stabilizing_ca"],
            "zero_coupling_runs": seed_pack["zero_coupling_population"],
            "population_median": population_median,
            "zero_coupling_median": zero_median,
            "population_contraction_count": sum(
                1 for run in seed_pack["population_self_stabilizing_ca"] if phase_label(run) == "contraction"
            ),
            "zero_coupling_contraction_count": sum(
                1 for run in seed_pack["zero_coupling_population"] if phase_label(run) == "contraction"
            ),
            "raw_local_baseline": raw_local_baselines[label],
            "scorer_only": _load_scorer_only(label),
        }

    phase_map = _phase_grid(
        graph=frontier_graph,
        ladder=ladder,
        orbit_rule_table=orbit_rule_table,
    )

    summary = {
        "generated_at": _timestamp(),
        "lookup_budget": LOOKUP_BUDGET,
        "selected_seeds": list(SELECTED_SEEDS),
        "population_parameters": {
            "population_size": POPULATION_SIZE,
            "coupling_strength": COUPLING_STRENGTH,
            "temperature": TEMPERATURE,
            "contraction_threshold": CONTRACTION_THRESHOLD,
            "memory_mix": MEMORY_MIX,
            "max_rounds_per_step": MAX_ROUNDS,
        },
        "control_rule_table": orbit_rule_table,
        "training_manifest": training_manifest,
        "results": results,
        "phase_map_path": str(args.phase_map_md.relative_to(REPO_ROOT)),
        "family_leakage_audit_path": str(LEAKAGE_AUDIT_PATH.relative_to(REPO_ROOT)),
    }

    _write_json(args.summary_json, summary)
    _write_json(args.rule_table, orbit_rule_table)
    _write_json(args.training_manifest, training_manifest)
    _write_json(args.phase_map_json, phase_map)
    args.phase_map_md.parent.mkdir(parents=True, exist_ok=True)
    args.phase_map_md.write_text(_phase_map_markdown(phase_map))
    args.summary_md.parent.mkdir(parents=True, exist_ok=True)
    args.summary_md.write_text(
        _summary_markdown(
            ladder=ladder,
            results=results,
            leakage_audit=leakage_audit,
        )
    )
    args.branch_md.parent.mkdir(parents=True, exist_ok=True)
    args.branch_md.write_text(
        _branch_markdown(
            training_manifest=training_manifest,
            results=results,
            phase_map=phase_map,
            leakage_audit=leakage_audit,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
