#!/usr/bin/env python3
"""Execute and summarize the bounded DEEPEN near-tie matrix."""

from __future__ import annotations

import csv
import json
import statistics
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt

import run_h1_matrix as matrix_runner


REPO_ROOT = Path(__file__).resolve().parents[1]
LANE_ROOT = REPO_ROOT / "results" / "concept_evolve" / "tree" / "001_packet_scout_handoff_root"
MANIFEST_PATH = LANE_ROOT / "results" / "manifests" / "deepen_near_tie_manifest.json"
RUNLOG_PATH = LANE_ROOT / "results" / "manifests" / "deepen_near_tie_runlog.jsonl"
RAW_ROOT = LANE_ROOT / "results" / "raw" / "deepen"
TABLE_PATH = LANE_ROOT / "tables" / "deepen_results.csv"
SUMMARY_PATH = LANE_ROOT / "tables" / "deepen_summary.json"
FIGURE_PATH = REPO_ROOT / "figures" / "h1_deepen_confidence_tradeoff.svg"
DESIGN_ORDER = ["confidence_gated", "source_blind", "time_constant_ranked", "blind_packet_merge"]
PALETTE = {
    "confidence_gated": "#1d6b57",
    "source_blind": "#4d657f",
    "time_constant_ranked": "#b35c1e",
    "blind_packet_merge": "#9c2f2f",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text())


def build_case(spec: dict) -> dict:
    voc_a_mv = spec["voc_a_mv"]
    voc_b_mv = spec["voc_b_mv"]
    ramp_mvps = spec["ramp_mvps"]
    vmax_mv = max(voc_a_mv, voc_b_mv)
    ratio = spec["ratio_b_to_a"]
    t_stop_s = 1.25 * vmax_mv / ramp_mvps
    tran_step_s = max(0.0005, t_stop_s / 8000)
    extra_params = {}
    if spec["delay_b_s"] > 0:
        extra_params = {
            "T_COLLAPSE_B": "0",
            "T_RECOVER_B": str(spec["delay_b_s"]),
            "COLLAPSE_SCALE_B": "0",
        }
    return {
        "case_id": spec["case_id"],
        "family": spec["family"],
        "polarity_mode": spec["polarity_mode"],
        "voltage_mv": vmax_mv,
        "voc_a_mv": voc_a_mv,
        "voc_b_mv": voc_b_mv,
        "ramp_mvps": ramp_mvps,
        "ratio_b_to_a": ratio,
        "pol_a": 1,
        "pol_b": 1,
        "r_a_ohm": 1000.0,
        "r_b_ohm": 1000.0 * ratio,
        "t_stop_s": t_stop_s,
        "tran_step_s": tran_step_s,
        "extra_params": extra_params,
        "designs": spec["designs"],
        "delay_b_s": spec["delay_b_s"],
    }


def run_one(case: dict, design: str) -> dict:
    case_dir = RAW_ROOT / design / case["case_id"]
    case_dir.mkdir(parents=True, exist_ok=True)
    rendered_path = case_dir / f"{design}_{case['case_id']}.cir"
    log_path = case_dir / f"{design}_{case['case_id']}.log"
    json_path = case_dir / f"{design}_{case['case_id']}.json"
    rendered_path.write_text(matrix_runner.render_netlist(design, case))
    proc = subprocess.run(
        [str(matrix_runner.NGSPICE_BIN), "-b", "-o", str(log_path), str(rendered_path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    parsed = matrix_runner.parse_log(log_path.read_text())
    row = {
        "timestamp": utc_now(),
        "design": design,
        "case_id": case["case_id"],
        "family": case["family"],
        "delay_b_s": case["delay_b_s"],
        "return_code": proc.returncode,
        "status": "ok" if proc.returncode == 0 else "blocked",
        "polarity_mode": case["polarity_mode"],
        "voltage_mv": case["voltage_mv"],
        "voc_a_mv": case["voc_a_mv"],
        "voc_b_mv": case["voc_b_mv"],
        "ramp_mvps": case["ramp_mvps"],
        "ratio_b_to_a": case["ratio_b_to_a"],
        "r_a_ohm": case["r_a_ohm"],
        "r_b_ohm": case["r_b_ohm"],
        "t_stop_s": case["t_stop_s"],
        "tran_step_s": case["tran_step_s"],
        "extra_params": case["extra_params"],
        **parsed,
        "rendered_netlist": str(rendered_path.relative_to(REPO_ROOT)),
        "log_path": str(log_path.relative_to(REPO_ROOT)),
    }
    json_path.write_text(json.dumps(row, indent=2) + "\n")
    return row


def write_runlog(rows: list[dict]) -> None:
    RUNLOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RUNLOG_PATH.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def write_table(rows: list[dict]) -> None:
    fieldnames = [
        "timestamp",
        "design",
        "case_id",
        "family",
        "delay_b_s",
        "status",
        "return_code",
        "polarity_mode",
        "voltage_mv",
        "voc_a_mv",
        "voc_b_mv",
        "ramp_mvps",
        "ratio_b_to_a",
        "startup_ok",
        "t_handoff_s",
        "t_handoff_fall_s",
        "t_handoff_rise2_s",
        "handoff_seen_v",
        "t_store_proxy_s",
        "t_store_proxy_fall_s",
        "t_store_proxy_rise2_s",
        "t_commit_s",
        "conf_final_v",
        "e_backdrive_j",
        "e_ctrl_j",
        "e_backdrive_full_j",
        "e_ctrl_full_j",
        "vstore_final_v",
        "rendered_netlist",
        "log_path",
    ]
    TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TABLE_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            payload = dict(row)
            writer.writerow({key: payload.get(key) for key in fieldnames})


def median_or_none(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def summarize(rows: list[dict]) -> dict:
    families: dict[str, dict[str, dict[str, float | int | None]]] = {}
    for family in ["static", "late"]:
        families[family] = {}
        for design in ["confidence_gated", "source_blind", "time_constant_ranked"]:
            subset = [row for row in rows if row["family"] == family and row["design"] == design]
            families[family][design] = {
                "cases": len(subset),
                "startup_successes": sum(1 for row in subset if (row.get("startup_ok") or 0.0) >= 0.5),
                "median_t_handoff_s": median_or_none([row["t_handoff_s"] for row in subset if row.get("t_handoff_s") is not None]),
                "median_e_ctrl_j": median_or_none([row["e_ctrl_j"] for row in subset if row.get("e_ctrl_j") is not None]),
                "commit_count": sum(1 for row in subset if row.get("t_commit_s") is not None),
                "median_t_commit_s": median_or_none([row["t_commit_s"] for row in subset if row.get("t_commit_s") is not None]),
            }

    pairwise: dict[str, dict[str, float | int | None]] = {}
    for family in ["static", "late"]:
        family_rows = [row for row in rows if row["family"] == family and row["design"] in {"confidence_gated", "source_blind", "time_constant_ranked"}]
        by_case = {
            case_id: {row["design"]: row for row in family_rows if row["case_id"] == case_id}
            for case_id in sorted({row["case_id"] for row in family_rows})
        }
        gains_vs_blind = []
        gains_vs_tc = []
        wins_vs_blind = 0
        wins_vs_tc = 0
        for design_rows in by_case.values():
            if {"confidence_gated", "source_blind"}.issubset(design_rows):
                cg = design_rows["confidence_gated"]
                sb = design_rows["source_blind"]
                if cg["t_handoff_s"] is not None and sb["t_handoff_s"] is not None:
                    gain = float(sb["t_handoff_s"]) - float(cg["t_handoff_s"])
                    gains_vs_blind.append(gain)
                    if gain > 1e-3:
                        wins_vs_blind += 1
            if {"confidence_gated", "time_constant_ranked"}.issubset(design_rows):
                cg = design_rows["confidence_gated"]
                tc = design_rows["time_constant_ranked"]
                if cg["t_handoff_s"] is not None and tc["t_handoff_s"] is not None:
                    gain = float(tc["t_handoff_s"]) - float(cg["t_handoff_s"])
                    gains_vs_tc.append(gain)
                    if gain > 1e-3:
                        wins_vs_tc += 1
        pairwise[family] = {
            "confidence_vs_source_blind_wins": wins_vs_blind,
            "confidence_vs_source_blind_median_gain_s": median_or_none(gains_vs_blind),
            "confidence_vs_time_constant_wins": wins_vs_tc,
            "confidence_vs_time_constant_median_gain_s": median_or_none(gains_vs_tc),
        }

    control_rows = [row for row in rows if row["design"] in {"blind_packet_merge", "source_blind", "confidence_gated"} and "v103" in row["case_id"]]
    controls: dict[str, dict[str, float | int | None]] = {}
    for design in ["blind_packet_merge", "confidence_gated", "source_blind"]:
        subset = [row for row in control_rows if row["design"] == design]
        controls[design] = {
            "cases": len(subset),
            "median_t_handoff_s": median_or_none([row["t_handoff_s"] for row in subset if row.get("t_handoff_s") is not None]),
            "median_e_backdrive_j": median_or_none([row["e_backdrive_j"] for row in subset if row.get("e_backdrive_j") is not None]),
            "median_e_ctrl_j": median_or_none([row["e_ctrl_j"] for row in subset if row.get("e_ctrl_j") is not None]),
        }

    survives_vs_blind = (
        families["static"]["confidence_gated"]["startup_successes"] == families["static"]["source_blind"]["startup_successes"]
        and families["late"]["confidence_gated"]["startup_successes"] == families["late"]["source_blind"]["startup_successes"]
        and (pairwise["late"]["confidence_vs_source_blind_median_gain_s"] or 0.0) > 0.1
        and (pairwise["static"]["confidence_vs_source_blind_median_gain_s"] or 0.0) > -0.01
    )

    return {
        "updated_at": utc_now(),
        "manifest_path": str(MANIFEST_PATH.relative_to(REPO_ROOT)),
        "table_path": str(TABLE_PATH.relative_to(REPO_ROOT)),
        "runlog_path": str(RUNLOG_PATH.relative_to(REPO_ROOT)),
        "figure_path": str(FIGURE_PATH.relative_to(REPO_ROOT)),
        "families": families,
        "pairwise": pairwise,
        "controls": controls,
        "decision": {
            "survives_vs_source_blind_gate": survives_vs_blind,
            "claim_boundary": (
                "confidence gating survives only as a temporal-separability controller: it improves over source_blind on late-arrival cases, "
                "collapses to the blind posture on static near ties, and does not beat time_constant_ranked on this matrix"
            ),
        },
    }


def write_summary(payload: dict) -> None:
    SUMMARY_PATH.write_text(json.dumps(payload, indent=2) + "\n")


def plot(rows: list[dict], summary: dict) -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "figure.dpi": 160,
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.8))

    families = ["static", "late"]
    designs = ["confidence_gated", "source_blind", "time_constant_ranked"]
    x = list(range(len(families)))
    width = 0.22
    offsets = [-width, 0.0, width]
    for design, offset in zip(designs, offsets):
        values = [summary["families"][family][design]["median_t_handoff_s"] for family in families]
        axes[0].bar(
            [value + offset for value in x],
            values,
            width=width * 0.92,
            color=PALETTE[design],
            label=design.replace("_", " "),
        )
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(["Static near tie", "Late arrival"])
    axes[0].set_ylabel("Median explicit handoff time (s)")
    axes[0].set_title("DEEPEN Core Matrix")
    axes[0].legend(frameon=False, loc="upper left")
    for idx, family in enumerate(families):
        commit_count = summary["families"][family]["confidence_gated"]["commit_count"]
        axes[0].text(
            idx - width,
            summary["families"][family]["confidence_gated"]["median_t_handoff_s"] + 0.04,
            f"commit {commit_count}/6",
            ha="center",
            va="bottom",
            fontsize=8,
            color=PALETTE["confidence_gated"],
        )

    control_cases = ["static_r1_v103", "static_r3_v103", "late_r1_v103", "late_r3_v103"]
    markers = {
        "static_r1_v103": "o",
        "static_r3_v103": "s",
        "late_r1_v103": "^",
        "late_r3_v103": "D",
    }
    for design in ["source_blind", "confidence_gated", "blind_packet_merge"]:
        subset = [row for row in rows if row["design"] == design and row["case_id"] in control_cases]
        axes[1].scatter(
            [1e9 * float(row["e_backdrive_j"] or 0.0) for row in subset],
            [row["t_handoff_s"] for row in subset],
            s=46,
            color=PALETTE[design],
            label=design.replace("_", " "),
            marker="o",
            alpha=0.95,
        )
        for row in subset:
            axes[1].text(
                1e9 * float(row["e_backdrive_j"] or 0.0) + 0.03,
                float(row["t_handoff_s"]) + 0.01,
                row["case_id"].replace("_", "\n", 1),
                fontsize=7,
                color=PALETTE[design],
            )
    axes[1].set_xlabel("Pre-handoff back-drive (nJ)")
    axes[1].set_ylabel("Explicit handoff time (s)")
    axes[1].set_title("Control Frontier On Decisive Cases")
    axes[1].legend(frameon=False, loc="upper right")
    axes[1].set_xlim(left=-0.05)

    fig.tight_layout()
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_PATH, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    manifest = load_manifest()
    cases = [build_case(spec) for spec in manifest["cases"]]
    rows: list[dict] = []
    for case in cases:
        for design in case["designs"]:
            rows.append(run_one(case, design))
    write_runlog(rows)
    write_table(rows)
    summary = summarize(rows)
    write_summary(summary)
    plot(rows, summary)
    print(
        json.dumps(
            {
                "rows": len(rows),
                "case_count": len(cases),
                "table_path": str(TABLE_PATH.relative_to(REPO_ROOT)),
                "summary_path": str(SUMMARY_PATH.relative_to(REPO_ROOT)),
                "figure_path": str(FIGURE_PATH.relative_to(REPO_ROOT)),
                "survives_vs_source_blind_gate": summary["decision"]["survives_vs_source_blind_gate"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
