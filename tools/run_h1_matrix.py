#!/usr/bin/env python3
"""Run or summarize the H1 startup matrix artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import subprocess
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LANE_ROOT = REPO_ROOT / "results" / "concept_evolve" / "tree" / "001_packet_scout_handoff_root"
MANIFEST_PATH = LANE_ROOT / "results" / "manifests" / "startup_matrix_manifest.json"
RUNLOG_PATH = LANE_ROOT / "results" / "manifests" / "startup_runlog.jsonl"
RAW_ROOT = LANE_ROOT / "results" / "raw" / "startup"
TABLE_PATH = LANE_ROOT / "tables" / "startup_results.csv"
SUMMARY_PATH = LANE_ROOT / "tables" / "startup_summary.json"
BENCHMARK_TABLE_PATH = LANE_ROOT / "tables" / "benchmark_comparison.csv"
BENCHMARK_SUMMARY_PATH = LANE_ROOT / "tables" / "benchmark_summary.json"
NGSPICE_BIN = REPO_ROOT / "tools" / "ngspice-local"

CORE_DESIGNS = ["champion", "fixed", "nonaware"]
DESIGN_ORDER = CORE_DESIGNS + ["source_blind", "time_constant_ranked", "blind_packet_merge"]
DECKS = {
    "champion": LANE_ROOT
    / "netlists"
    / "champion"
    / "packet_scout_handoff"
    / "variant_01_rc_ranked_packet_gate"
    / "rc_ranked_packet_gate.cir",
    "fixed": LANE_ROOT
    / "netlists"
    / "baselines"
    / "fixed_startup_path"
    / "fixed_startup_path.cir",
    "nonaware": LANE_ROOT
    / "netlists"
    / "baselines"
    / "nonaware_multi_input_startup"
    / "nonaware_multi_input_startup.cir",
    "source_blind": LANE_ROOT
    / "netlists"
    / "ablations"
    / "source_blind_packet_gate"
    / "source_blind_packet_gate.cir",
    "time_constant_ranked": LANE_ROOT
    / "netlists"
    / "ablations"
    / "time_constant_ranked_arbiter"
    / "time_constant_ranked_arbiter.cir",
    "blind_packet_merge": LANE_ROOT
    / "netlists"
    / "ablations"
    / "blind_packet_merge"
    / "blind_packet_merge.cir",
}

PARAM_RE = {
    "VLEVEL": re.compile(r"(?m)^\.param\s+VLEVEL=.*$"),
    "VOC_A": re.compile(r"(?m)^\.param\s+VOC_A=.*$"),
    "VOC_B": re.compile(r"(?m)^\.param\s+VOC_B=.*$"),
    "RATIO": re.compile(r"(?m)^\.param\s+RATIO=.*$"),
    "POL_A": re.compile(r"(?m)^\.param\s+POL_A=.*$"),
    "POL_B": re.compile(r"(?m)^\.param\s+POL_B=.*$"),
    "R_A": re.compile(r"(?m)^\.param\s+R_A=.*$"),
    "R_B": re.compile(r"(?m)^\.param\s+R_B=.*$"),
    "RAMP_MVPS": re.compile(r"(?m)^\.param\s+RAMP_MVPS=.*$"),
    "TSTOP": re.compile(r"(?m)^\.param\s+TSTOP=.*$"),
    "TRAN": re.compile(r"(?m)^\.tran\s+.*$"),
    "INCLUDE": re.compile(r'(?m)^\.include\s+(\S+)$'),
}

MEASURE_PATTERNS = {
    "startup_ok": r"startup_ok\s*=\s*([-+0-9.eE]+)",
    "t_handoff_s": r"t_handoff\s*=\s*([-+0-9.eE]+)",
    "t_handoff_fall_s": r"t_handoff_fall\s*=\s*([-+0-9.eE]+)",
    "t_handoff_rise2_s": r"t_handoff_rise2\s*=\s*([-+0-9.eE]+)",
    "handoff_seen_v": r"handoff_seen_final\s*=\s*([-+0-9.eE]+)",
    "t_store_proxy_s": r"t_store_proxy\s*=\s*([-+0-9.eE]+)",
    "t_store_proxy_fall_s": r"t_store_proxy_fall\s*=\s*([-+0-9.eE]+)",
    "t_store_proxy_rise2_s": r"t_store_proxy_rise2\s*=\s*([-+0-9.eE]+)",
    "e_backdrive_j": r"e_backdrive\s*=\s*([-+0-9.eE]+)",
    "e_ctrl_j": r"e_ctrl\s*=\s*([-+0-9.eE]+)",
    "e_backdrive_full_j": r"e_backdrive_full\s*=\s*([-+0-9.eE]+)",
    "e_ctrl_full_j": r"e_ctrl_full\s*=\s*([-+0-9.eE]+)",
    "vstore_final_v": r"vstore_final\s*=\s*([-+0-9.eE]+)",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text())


def save_manifest(payload: dict) -> None:
    payload["updated_at"] = utc_now()
    MANIFEST_PATH.write_text(json.dumps(payload, indent=2) + "\n")


def select_cases(manifest: dict, case_ids: str | None) -> list[dict]:
    cases = manifest["cases"]
    if not case_ids:
        return cases
    wanted = {part.strip() for part in case_ids.split(",") if part.strip()}
    return [case for case in cases if case["case_id"] in wanted]


def select_designs(designs: str | None) -> list[str]:
    if not designs:
        return CORE_DESIGNS
    chosen = [part.strip() for part in designs.split(",") if part.strip()]
    for design in chosen:
        if design not in DECKS:
            raise SystemExit(f"unknown design: {design}")
    return chosen


def absolutize_includes(text: str, deck_path: Path) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = match.group(1).strip('"')
        include_path = (deck_path.parent / raw).resolve()
        return f'.include "{include_path}"'

    return PARAM_RE["INCLUDE"].sub(repl, text)


def inject_extra_params(text: str, extra_params: dict[str, str]) -> str:
    if not extra_params:
        return text
    lines = [f".param {key}={value}" for key, value in extra_params.items()]
    marker = re.search(r"(?m)^VMEAS_A\s", text)
    if not marker:
        raise RuntimeError("failed to find VMEAS_A marker for extra parameter injection")
    return text[: marker.start()] + "\n".join(lines) + "\n\n" + text[marker.start() :]


def render_netlist(design: str, case: dict) -> str:
    deck_path = DECKS[design]
    text = absolutize_includes(deck_path.read_text(), deck_path)
    voc_a_mv = case.get("voc_a_mv", case["voltage_mv"])
    voc_b_mv = case.get("voc_b_mv", case["voltage_mv"])
    replacements = {
        "VLEVEL": f".param VLEVEL={max(voc_a_mv, voc_b_mv)}m",
        "VOC_A": f".param VOC_A={voc_a_mv}m",
        "VOC_B": f".param VOC_B={voc_b_mv}m",
        "RATIO": f".param RATIO={case['ratio_b_to_a']}",
        "POL_A": f".param POL_A={case['pol_a']}",
        "POL_B": f".param POL_B={case['pol_b']}",
        "R_A": f".param R_A={case['r_a_ohm']}",
        "R_B": f".param R_B={case['r_b_ohm']}",
        "RAMP_MVPS": f".param RAMP_MVPS={case['ramp_mvps']}",
        "TSTOP": f".param TSTOP={case['t_stop_s']}",
        "TRAN": f".tran {case['tran_step_s']} {case['t_stop_s']} 0 {case['tran_step_s']}",
    }
    for key, replacement in replacements.items():
        pattern = PARAM_RE[key]
        text, count = pattern.subn(replacement, text, count=1)
        if count != 1:
            raise RuntimeError(f"failed to rewrite {key} for {design} {case['case_id']}")
    text = inject_extra_params(text, case.get("extra_params", {}))
    header = [
        "* Auto-generated by tools/run_h1_matrix.py",
        f"* case_id={case['case_id']}",
        f"* polarity_mode={case['polarity_mode']}",
        f"* voltage_mv={case['voltage_mv']}",
        f"* voc_a_mv={voc_a_mv}",
        f"* voc_b_mv={voc_b_mv}",
        f"* ramp_mvps={case['ramp_mvps']}",
        f"* ratio_b_to_a={case['ratio_b_to_a']}",
        f"* t_stop_s={case['t_stop_s']}",
        f"* tran_step_s={case['tran_step_s']}",
    ]
    for key, value in case.get("extra_params", {}).items():
        header.append(f"* {key}={value}")
    return "\n".join(header) + "\n" + text


def parse_log(log_text: str) -> dict:
    parsed = {}
    for key, pattern in MEASURE_PATTERNS.items():
        match = re.search(pattern, log_text)
        parsed[key] = float(match.group(1)) if match else None
    return parsed


def run_case(design: str, case: dict) -> dict:
    case_dir = RAW_ROOT / design / case["case_id"]
    case_dir.mkdir(parents=True, exist_ok=True)
    rendered_path = case_dir / f"{design}_{case['case_id']}.cir"
    log_path = case_dir / f"{design}_{case['case_id']}.log"
    json_path = case_dir / f"{design}_{case['case_id']}.json"
    rendered_path.write_text(render_netlist(design, case))
    proc = subprocess.run(
        [str(NGSPICE_BIN), "-b", "-o", str(log_path), str(rendered_path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    parsed = parse_log(log_path.read_text())
    row = {
        "design": design,
        "case_id": case["case_id"],
        "return_code": proc.returncode,
        "status": "ok" if proc.returncode == 0 else "blocked",
        "polarity_mode": case["polarity_mode"],
        "voltage_mv": case["voltage_mv"],
        "voc_a_mv": case.get("voc_a_mv", case["voltage_mv"]),
        "voc_b_mv": case.get("voc_b_mv", case["voltage_mv"]),
        "ramp_mvps": case["ramp_mvps"],
        "ratio_b_to_a": case["ratio_b_to_a"],
        "pol_a": case["pol_a"],
        "pol_b": case["pol_b"],
        "r_a_ohm": case["r_a_ohm"],
        "r_b_ohm": case["r_b_ohm"],
        "t_stop_s": case["t_stop_s"],
        "tran_step_s": case["tran_step_s"],
        "extra_params": case.get("extra_params", {}),
        **parsed,
        "rendered_netlist": str(rendered_path.relative_to(REPO_ROOT)),
        "log_path": str(log_path.relative_to(REPO_ROOT)),
    }
    json_path.write_text(json.dumps(row, indent=2) + "\n")
    return row


def collect_existing() -> list[dict]:
    rows = []
    for design in DESIGN_ORDER:
        design_dir = RAW_ROOT / design
        if not design_dir.exists():
            continue
        for case_dir in sorted(path for path in design_dir.iterdir() if path.is_dir()):
            json_path = case_dir / f"{design}_{case_dir.name}.json"
            if json_path.exists():
                rows.append(json.loads(json_path.read_text()))
    return rows


def write_runlog(rows: list[dict]) -> None:
    RUNLOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RUNLOG_PATH.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps({"timestamp": utc_now(), **row}) + "\n")


def write_table(rows: list[dict]) -> None:
    TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "design",
        "case_id",
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
        "e_backdrive_j",
        "e_ctrl_j",
        "e_backdrive_full_j",
        "e_ctrl_full_j",
        "vstore_final_v",
        "t_stop_s",
        "tran_step_s",
        "extra_params",
        "rendered_netlist",
        "log_path",
    ]
    with TABLE_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted(rows, key=lambda item: (item["design"], item["case_id"])):
            payload = dict(row)
            payload["extra_params"] = json.dumps(payload.get("extra_params", {}), sort_keys=True)
            writer.writerow({key: payload.get(key) for key in fieldnames})


def median_or_none(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def write_summary(rows: list[dict], manifest: dict | None = None) -> None:
    counts = {}
    for design in DESIGN_ORDER:
        subset = [row for row in rows if row["design"] == design]
        if not subset:
            continue
        successful = [row for row in subset if (row.get("startup_ok") or 0.0) >= 0.5 and row.get("t_handoff_s") is not None]
        counts[design] = {
            "total_cases": len(subset),
            "ok_cases": sum(1 for row in subset if row["status"] == "ok"),
            "startup_successes": len(successful),
            "mixed_cases": sum(1 for row in subset if row["polarity_mode"] == "mixed"),
            "median_t_handoff_s_success": median_or_none([row["t_handoff_s"] for row in successful]),
            "median_e_ctrl_j_success": median_or_none([row["e_ctrl_j"] for row in successful if row.get("e_ctrl_j") is not None]),
            "median_e_ctrl_full_j_success": median_or_none(
                [row.get("e_ctrl_full_j") for row in successful if row.get("e_ctrl_full_j") is not None]
            ),
        }
    payload = {
        "suite": "startup_matrix_v2",
        "designs": [design for design in DESIGN_ORDER if design in counts],
        "manifest_path": str(MANIFEST_PATH.relative_to(REPO_ROOT)),
        "table_path": str(TABLE_PATH.relative_to(REPO_ROOT)),
        "runlog_path": str(RUNLOG_PATH.relative_to(REPO_ROOT)),
        "counts": counts,
        "updated_at": utc_now(),
    }
    if manifest is not None:
        payload["case_count"] = len(manifest.get("cases", []))
    SUMMARY_PATH.write_text(json.dumps(payload, indent=2) + "\n")


def anchor_for_case(row: dict) -> tuple[str, str]:
    ratio = int(float(row["ratio_b_to_a"]))
    if row["polarity_mode"] == "mixed":
        if ratio >= 20:
            return (
                "kuai2022dualpolarityjssc; weng2024osece; chen2024collaborative",
                "Mixed-polarity extreme-asymmetry startup regime tied to the dual-polarity TEG family and the closest 2024 multi-input self-powered interface family.",
            )
        return (
            "cao2019bipolarinput; kuai2022dualpolarityjssc; chen2024collaborative",
            "Mixed-polarity startup regime tied to the bipolar-input TEG and self-powered multi-input interface families.",
        )
    if ratio == 1:
        return (
            "goppert2016startup70mv; quintero2019cmosstartup",
            "Same-polarity low-asymmetry startup regime, closest to the recovered single-source TEG startup family.",
        )
    return (
        "alhawari2016multisourcepmu; alghisi2017batteryless; gogolou2025multisourcereview; wang2023serialstack",
        "Same-polarity multi-source regime with impedance asymmetry, closest to the multi-source PMU and interface family.",
    )


def write_benchmark_artifacts(rows: list[dict]) -> None:
    by_case_design = {(row["case_id"], row["design"]): row for row in rows if row["design"] in CORE_DESIGNS}
    case_ids = sorted(
        case_id
        for case_id in {row["case_id"] for row in rows if row["design"] in CORE_DESIGNS}
        if all((case_id, design) in by_case_design for design in CORE_DESIGNS)
    )
    fieldnames = [
        "case_id",
        "polarity_mode",
        "voltage_mv",
        "voc_a_mv",
        "voc_b_mv",
        "ramp_mvps",
        "ratio_b_to_a",
        "literature_anchor",
        "regime_note",
        "champion_startup_ok",
        "champion_t_handoff_s",
        "champion_e_backdrive_j",
        "champion_e_ctrl_j",
        "champion_e_ctrl_full_j",
        "fixed_startup_ok",
        "fixed_t_handoff_s",
        "fixed_e_backdrive_j",
        "fixed_e_ctrl_j",
        "fixed_e_ctrl_full_j",
        "nonaware_startup_ok",
        "nonaware_t_handoff_s",
        "nonaware_e_backdrive_j",
        "nonaware_e_ctrl_j",
        "nonaware_e_ctrl_full_j",
        "champion_vs_fixed_t_handoff_s",
        "champion_vs_nonaware_t_handoff_s",
        "champion_vs_fixed_e_ctrl_j",
        "champion_vs_nonaware_e_ctrl_j",
    ]
    with BENCHMARK_TABLE_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for case_id in case_ids:
            champion = by_case_design[(case_id, "champion")]
            fixed = by_case_design[(case_id, "fixed")]
            nonaware = by_case_design[(case_id, "nonaware")]
            anchor, note = anchor_for_case(champion)
            writer.writerow(
                {
                    "case_id": case_id,
                    "polarity_mode": champion["polarity_mode"],
                    "voltage_mv": champion["voltage_mv"],
                    "voc_a_mv": champion["voc_a_mv"],
                    "voc_b_mv": champion["voc_b_mv"],
                    "ramp_mvps": champion["ramp_mvps"],
                    "ratio_b_to_a": champion["ratio_b_to_a"],
                    "literature_anchor": anchor,
                    "regime_note": note,
                    "champion_startup_ok": champion["startup_ok"],
                    "champion_t_handoff_s": champion["t_handoff_s"],
                    "champion_e_backdrive_j": champion["e_backdrive_j"],
                    "champion_e_ctrl_j": champion["e_ctrl_j"],
                    "champion_e_ctrl_full_j": champion.get("e_ctrl_full_j"),
                    "fixed_startup_ok": fixed["startup_ok"],
                    "fixed_t_handoff_s": fixed["t_handoff_s"],
                    "fixed_e_backdrive_j": fixed["e_backdrive_j"],
                    "fixed_e_ctrl_j": fixed["e_ctrl_j"],
                    "fixed_e_ctrl_full_j": fixed.get("e_ctrl_full_j"),
                    "nonaware_startup_ok": nonaware["startup_ok"],
                    "nonaware_t_handoff_s": nonaware["t_handoff_s"],
                    "nonaware_e_backdrive_j": nonaware["e_backdrive_j"],
                    "nonaware_e_ctrl_j": nonaware["e_ctrl_j"],
                    "nonaware_e_ctrl_full_j": nonaware.get("e_ctrl_full_j"),
                    "champion_vs_fixed_t_handoff_s": (
                        None
                        if champion["t_handoff_s"] is None or fixed["t_handoff_s"] is None
                        else float(champion["t_handoff_s"]) - float(fixed["t_handoff_s"])
                    ),
                    "champion_vs_nonaware_t_handoff_s": (
                        None
                        if champion["t_handoff_s"] is None or nonaware["t_handoff_s"] is None
                        else float(champion["t_handoff_s"]) - float(nonaware["t_handoff_s"])
                    ),
                    "champion_vs_fixed_e_ctrl_j": (
                        None
                        if champion["e_ctrl_j"] is None or fixed["e_ctrl_j"] is None
                        else float(champion["e_ctrl_j"]) - float(fixed["e_ctrl_j"])
                    ),
                    "champion_vs_nonaware_e_ctrl_j": (
                        None
                        if champion["e_ctrl_j"] is None or nonaware["e_ctrl_j"] is None
                        else float(champion["e_ctrl_j"]) - float(nonaware["e_ctrl_j"])
                    ),
                }
            )

    summary = {
        "updated_at": utc_now(),
        "case_count": len(case_ids),
        "champion_better_startup_than_fixed": 0,
        "champion_better_startup_than_nonaware": 0,
        "champion_faster_than_fixed": 0,
        "champion_faster_than_nonaware": 0,
        "champion_lower_backdrive_than_fixed": 0,
        "champion_lower_backdrive_than_nonaware": 0,
        "champion_lower_ctrl_than_fixed": 0,
        "champion_lower_ctrl_than_nonaware": 0,
        "median_t_handoff_s_success": {},
        "median_e_ctrl_j_all": {},
        "median_e_ctrl_j_success": {},
        "median_e_ctrl_full_j_all": {},
    }
    for case_id in case_ids:
        champion = by_case_design[(case_id, "champion")]
        fixed = by_case_design[(case_id, "fixed")]
        nonaware = by_case_design[(case_id, "nonaware")]
        if float(champion["startup_ok"] or 0.0) > float(fixed["startup_ok"] or 0.0):
            summary["champion_better_startup_than_fixed"] += 1
        if float(champion["startup_ok"] or 0.0) > float(nonaware["startup_ok"] or 0.0):
            summary["champion_better_startup_than_nonaware"] += 1
        if champion["t_handoff_s"] is not None and fixed["t_handoff_s"] is not None and float(champion["startup_ok"] or 0.0) >= 0.5 and float(fixed["startup_ok"] or 0.0) >= 0.5:
            if float(champion["t_handoff_s"]) < float(fixed["t_handoff_s"]):
                summary["champion_faster_than_fixed"] += 1
        if champion["t_handoff_s"] is not None and nonaware["t_handoff_s"] is not None and float(champion["startup_ok"] or 0.0) >= 0.5 and float(nonaware["startup_ok"] or 0.0) >= 0.5:
            if float(champion["t_handoff_s"]) < float(nonaware["t_handoff_s"]):
                summary["champion_faster_than_nonaware"] += 1
        if champion["e_backdrive_j"] is not None and fixed["e_backdrive_j"] is not None and float(champion["e_backdrive_j"]) < float(fixed["e_backdrive_j"]):
            summary["champion_lower_backdrive_than_fixed"] += 1
        if champion["e_backdrive_j"] is not None and nonaware["e_backdrive_j"] is not None and float(champion["e_backdrive_j"]) < float(nonaware["e_backdrive_j"]):
            summary["champion_lower_backdrive_than_nonaware"] += 1
        if champion["e_ctrl_j"] is not None and fixed["e_ctrl_j"] is not None and float(champion["e_ctrl_j"]) < float(fixed["e_ctrl_j"]):
            summary["champion_lower_ctrl_than_fixed"] += 1
        if champion["e_ctrl_j"] is not None and nonaware["e_ctrl_j"] is not None and float(champion["e_ctrl_j"]) < float(nonaware["e_ctrl_j"]):
            summary["champion_lower_ctrl_than_nonaware"] += 1

    for design in CORE_DESIGNS:
        subset = [row for row in rows if row["design"] == design]
        success = [row for row in subset if row["t_handoff_s"] is not None and float(row["startup_ok"] or 0.0) >= 0.5]
        summary["median_t_handoff_s_success"][design] = median_or_none([float(row["t_handoff_s"]) for row in success])
        summary["median_e_ctrl_j_all"][design] = median_or_none([float(row["e_ctrl_j"]) for row in subset if row.get("e_ctrl_j") is not None])
        summary["median_e_ctrl_j_success"][design] = median_or_none(
            [float(row["e_ctrl_j"]) for row in success if row.get("e_ctrl_j") is not None]
        )
        summary["median_e_ctrl_full_j_all"][design] = median_or_none(
            [float(row["e_ctrl_full_j"]) for row in subset if row.get("e_ctrl_full_j") is not None]
        )

    BENCHMARK_SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n")


def cmd_run(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    cases = select_cases(manifest, args.cases)
    designs = select_designs(args.designs)
    manifest["designs"] = designs
    manifest["write_raw"] = True
    save_manifest(manifest)
    rows = []
    for design in designs:
        for case in cases:
            rows.append(run_case(design, case))
    all_rows = collect_existing()
    write_runlog(all_rows)
    write_table(all_rows)
    write_summary(all_rows, manifest)
    print(json.dumps({"ran": len(rows), "collected": len(all_rows), "cases": len(cases), "designs": designs}, indent=2))
    return 0


def cmd_summarize(_: argparse.Namespace) -> int:
    manifest = load_manifest()
    rows = collect_existing()
    manifest["designs"] = sorted({row["design"] for row in rows}, key=lambda design: DESIGN_ORDER.index(design))
    manifest["write_raw"] = True
    save_manifest(manifest)
    write_runlog(rows)
    write_table(rows)
    write_summary(rows, manifest)
    print(json.dumps({"collected": len(rows), "table_path": str(TABLE_PATH.relative_to(REPO_ROOT))}, indent=2))
    return 0


def cmd_benchmark(_: argparse.Namespace) -> int:
    rows = collect_existing()
    write_benchmark_artifacts(rows)
    print(
        json.dumps(
            {
                "collected": len(rows),
                "benchmark_table": str(BENCHMARK_TABLE_PATH.relative_to(REPO_ROOT)),
                "benchmark_summary": str(BENCHMARK_SUMMARY_PATH.relative_to(REPO_ROOT)),
            },
            indent=2,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_parser = sub.add_parser("run")
    run_parser.add_argument("--cases")
    run_parser.add_argument("--designs")
    run_parser.set_defaults(func=cmd_run)

    sum_parser = sub.add_parser("summarize")
    sum_parser.set_defaults(func=cmd_summarize)

    bench_parser = sub.add_parser("benchmark")
    bench_parser.set_defaults(func=cmd_benchmark)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
