#!/usr/bin/env python3
"""Generate reproducible sensitivity artifacts for the H1 startup lane."""

from __future__ import annotations

import csv
import json
import math
import statistics
from pathlib import Path
from xml.sax.saxutils import escape


REPO_ROOT = Path(__file__).resolve().parents[1]
LANE_ROOT = REPO_ROOT / "results" / "concept_evolve" / "tree" / "001_packet_scout_handoff_root"
TABLE_ROOT = LANE_ROOT / "tables"
FIGURE_ROOT = REPO_ROOT / "figures"

STARTUP_RESULTS = TABLE_ROOT / "startup_results.csv"
FALSIFIER_RESULTS = TABLE_ROOT / "falsifier_results.csv"

SENSITIVITY_TABLE = TABLE_ROOT / "analysis_sensitivity.csv"
PAIRWISE_TABLE = TABLE_ROOT / "analysis_pairwise.csv"
ANALYSIS_SUMMARY = TABLE_ROOT / "analysis_summary.json"
STARTUP_FIGURE = FIGURE_ROOT / "h1_startup_sensitivity.svg"
BOUNDARY_FIGURE = FIGURE_ROOT / "h1_falsifier_boundary.svg"

DESIGN_ORDER = ["champion", "fixed", "nonaware"]
DESIGN_LABELS = {
    "champion": "Champion",
    "fixed": "Fixed",
    "nonaware": "Nonaware",
}
FACTOR_SPECS = [
    ("polarity_mode", "Polarity Mix", ["same", "mixed"], {"same": "same", "mixed": "mixed"}),
    ("ratio_b_to_a", "Impedance Spread", ["1", "5", "20"], {"1": "1:1", "5": "1:5", "20": "1:20"}),
    ("ramp_mvps", "Ramp Rate (mV/s)", ["0.1", "1", "10", "100"], {"0.1": "0.1", "1": "1", "10": "10", "100": "100"}),
]


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if math.isnan(number):
        return None
    return number


def canonical_value(factor: str, raw: str) -> str:
    if factor == "ratio_b_to_a":
        return str(int(round(float(raw))))
    if factor == "ramp_mvps":
        value = float(raw)
        return str(int(value)) if value.is_integer() else str(value)
    return raw


def load_rows(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            record = dict(row)
            for key in ["startup_ok", "t_handoff_s", "e_backdrive_j", "e_ctrl_j", "voltage_mv", "ramp_mvps", "ratio_b_to_a"]:
                record[key] = parse_float(record.get(key))
            if "polarity_mode" in record and record["polarity_mode"] is not None:
                record["polarity_mode"] = str(record["polarity_mode"])
            record["case_id"] = str(record["case_id"])
            record["design"] = str(record["design"])
            rows.append(record)
    return rows


def median_or_none(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def summarize_startup(rows: list[dict]) -> list[dict]:
    output: list[dict] = []
    for factor, _, order, _ in FACTOR_SPECS:
        for value in order:
            for design in DESIGN_ORDER:
                subset = [
                    row
                    for row in rows
                    if row["design"] == design and canonical_value(factor, str(row[factor])) == value
                ]
                successful = [row for row in subset if (row["startup_ok"] or 0.0) >= 0.5]
                output.append(
                    {
                        "factor": factor,
                        "value": value,
                        "design": design,
                        "total_cases": len(subset),
                        "startup_successes": len(successful),
                        "startup_success_rate": (len(successful) / len(subset)) if subset else None,
                        "median_t_handoff_s_success": median_or_none(
                            [row["t_handoff_s"] for row in successful if row["t_handoff_s"] is not None]
                        ),
                        "median_e_ctrl_j_success": median_or_none(
                            [row["e_ctrl_j"] for row in successful if row["e_ctrl_j"] is not None]
                        ),
                        "median_e_backdrive_j_all": median_or_none(
                            [row["e_backdrive_j"] for row in subset if row["e_backdrive_j"] is not None]
                        ),
                    }
                )
    return output


def summarize_pairwise(rows: list[dict]) -> list[dict]:
    by_case_design = {(row["case_id"], row["design"]): row for row in rows}
    output: list[dict] = []
    for factor, _, order, _ in FACTOR_SPECS:
        case_values = {
            case_id: canonical_value(factor, str(next(row[factor] for row in rows if row["case_id"] == case_id)))
            for case_id in sorted({row["case_id"] for row in rows})
        }
        for value in order:
            case_ids = [case_id for case_id, case_value in case_values.items() if case_value == value]
            for baseline in ["fixed", "nonaware"]:
                better_startup = faster = lower_ctrl = lower_backdrive = 0
                for case_id in case_ids:
                    champion = by_case_design[(case_id, "champion")]
                    rival = by_case_design[(case_id, baseline)]
                    champion_ok = champion["startup_ok"] or 0.0
                    rival_ok = rival["startup_ok"] or 0.0
                    if champion_ok > rival_ok:
                        better_startup += 1
                    if (
                        champion_ok >= 0.5
                        and rival_ok >= 0.5
                        and champion["t_handoff_s"] is not None
                        and rival["t_handoff_s"] is not None
                        and champion["t_handoff_s"] < rival["t_handoff_s"]
                    ):
                        faster += 1
                    if champion["e_ctrl_j"] is not None and rival["e_ctrl_j"] is not None and champion["e_ctrl_j"] < rival["e_ctrl_j"]:
                        lower_ctrl += 1
                    if champion["e_backdrive_j"] is not None and rival["e_backdrive_j"] is not None and champion["e_backdrive_j"] < rival["e_backdrive_j"]:
                        lower_backdrive += 1
                output.append(
                    {
                        "factor": factor,
                        "value": value,
                        "comparison": baseline,
                        "total_cases": len(case_ids),
                        "champion_better_startup_cases": better_startup,
                        "champion_faster_cases": faster,
                        "champion_lower_ctrl_cases": lower_ctrl,
                        "champion_lower_backdrive_cases": lower_backdrive,
                    }
                )
    return output


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def success_fill(successes: int, total: int) -> str:
    if total <= 0:
        return "#efefef"
    rate = successes / total
    if rate >= 0.99:
        return "#b7e4c7"
    if rate >= 0.75:
        return "#d8f3dc"
    if rate >= 0.5:
        return "#fff3b0"
    if rate > 0:
        return "#ffd6a5"
    return "#f4acb7"


def falsifier_fill(startup_ok: bool, backdrive: float | None) -> str:
    if startup_ok and (backdrive or 0.0) <= 1e-12:
        return "#b7e4c7"
    if startup_ok:
        return "#fff3b0"
    if (backdrive or 0.0) > 1e-12:
        return "#ffd6a5"
    return "#f4acb7"


def sci(value: float | None) -> str:
    if value is None:
        return "-"
    if abs(value) < 1e-12:
        return "0.00e+00"
    return f"{value:.2e}"


def render_startup_figure(summary_rows: list[dict]) -> None:
    FIGURE_ROOT.mkdir(parents=True, exist_ok=True)
    width = 1220
    height = 1140
    x_margin = 40
    y = 48
    cell_w = 150
    cell_h = 76
    row_header_w = 130
    title = "H1 Startup Sensitivity"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fcfcf8"/>',
        f'<text x="{x_margin}" y="28" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#1f2933">{escape(title)}</text>',
        f'<text x="{x_margin}" y="46" font-family="Arial, sans-serif" font-size="12" fill="#52606d">Each cell shows startup successes and the median successful control energy for the grouped primary-matrix cases.</text>',
    ]

    row_lookup = {
        (row["factor"], row["value"], row["design"]): row for row in summary_rows
    }

    for factor, heading, order, labels in FACTOR_SPECS:
        parts.append(
            f'<text x="{x_margin}" y="{y}" font-family="Arial, sans-serif" font-size="16" font-weight="700" fill="#102a43">{escape(heading)}</text>'
        )
        y += 18
        table_x = x_margin
        table_y = y
        parts.append(f'<rect x="{table_x}" y="{table_y}" width="{row_header_w}" height="{cell_h}" fill="#e9ecef" stroke="#bcccdc"/>')
        parts.append(f'<text x="{table_x + 16}" y="{table_y + 44}" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#102a43">Design</text>')
        for col_index, value in enumerate(order):
            x = table_x + row_header_w + col_index * cell_w
            parts.append(f'<rect x="{x}" y="{table_y}" width="{cell_w}" height="{cell_h}" fill="#e9ecef" stroke="#bcccdc"/>')
            parts.append(
                f'<text x="{x + cell_w / 2}" y="{table_y + 30}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#102a43">{escape(labels[value])}</text>'
            )
        for row_index, design in enumerate(DESIGN_ORDER):
            y0 = table_y + cell_h + row_index * cell_h
            parts.append(f'<rect x="{table_x}" y="{y0}" width="{row_header_w}" height="{cell_h}" fill="#f0f4f8" stroke="#bcccdc"/>')
            parts.append(
                f'<text x="{table_x + 16}" y="{y0 + 30}" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#102a43">{escape(DESIGN_LABELS[design])}</text>'
            )
            for col_index, value in enumerate(order):
                item = row_lookup[(factor, value, design)]
                x = table_x + row_header_w + col_index * cell_w
                fill = success_fill(int(item["startup_successes"]), int(item["total_cases"]))
                parts.append(f'<rect x="{x}" y="{y0}" width="{cell_w}" height="{cell_h}" fill="{fill}" stroke="#bcccdc"/>')
                parts.append(
                    f'<text x="{x + cell_w / 2}" y="{y0 + 28}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#102a43">S {int(item["startup_successes"])}/{int(item["total_cases"])}</text>'
                )
                parts.append(
                    f'<text x="{x + cell_w / 2}" y="{y0 + 52}" text-anchor="middle" font-family="Courier New, monospace" font-size="11" fill="#243b53">E {escape(sci(item["median_e_ctrl_j_success"]))}</text>'
                )
        y = table_y + cell_h * (len(DESIGN_ORDER) + 1) + 34

    parts.append("</svg>")
    STARTUP_FIGURE.write_text("\n".join(parts) + "\n", encoding="utf-8")


def render_falsifier_figure(rows: list[dict]) -> None:
    FIGURE_ROOT.mkdir(parents=True, exist_ok=True)
    width = 1240
    height = 390
    x_margin = 40
    y_margin = 56
    row_header_w = 130
    cell_w = 170
    cell_h = 76
    case_ids = sorted({row["case_id"] for row in rows})
    attack_labels = {
        case_id: next(row["attack_class"] for row in rows if row["case_id"] == case_id)
        for case_id in case_ids
    }
    by_case_design = {(row["case_id"], row["design"]): row for row in rows}

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fcfcf8"/>',
        f'<text x="{x_margin}" y="28" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#1f2933">H1 Falsifier Boundary</text>',
        f'<text x="{x_margin}" y="46" font-family="Arial, sans-serif" font-size="12" fill="#52606d">Green: startup with zero measured back-drive. Amber: startup or fail with measurable wrong-way energy. Red: fail with no measured back-drive.</text>',
    ]

    parts.append(f'<rect x="{x_margin}" y="{y_margin}" width="{row_header_w}" height="{cell_h}" fill="#e9ecef" stroke="#bcccdc"/>')
    parts.append(f'<text x="{x_margin + 16}" y="{y_margin + 44}" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#102a43">Design</text>')
    for col_index, case_id in enumerate(case_ids):
        x = x_margin + row_header_w + col_index * cell_w
        parts.append(f'<rect x="{x}" y="{y_margin}" width="{cell_w}" height="{cell_h}" fill="#e9ecef" stroke="#bcccdc"/>')
        parts.append(
            f'<text x="{x + cell_w / 2}" y="{y_margin + 24}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#102a43">{escape(case_id)}</text>'
        )
        parts.append(
            f'<text x="{x + cell_w / 2}" y="{y_margin + 46}" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#243b53">{escape(attack_labels[case_id])}</text>'
        )
    for row_index, design in enumerate(DESIGN_ORDER):
        y = y_margin + cell_h + row_index * cell_h
        parts.append(f'<rect x="{x_margin}" y="{y}" width="{row_header_w}" height="{cell_h}" fill="#f0f4f8" stroke="#bcccdc"/>')
        parts.append(
            f'<text x="{x_margin + 16}" y="{y + 30}" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#102a43">{escape(DESIGN_LABELS[design])}</text>'
        )
        for col_index, case_id in enumerate(case_ids):
            row = by_case_design[(case_id, design)]
            x = x_margin + row_header_w + col_index * cell_w
            ok = (row["startup_ok"] or 0.0) >= 0.5
            backdrive = row["e_backdrive_j"]
            fill = falsifier_fill(ok, backdrive)
            parts.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="{fill}" stroke="#bcccdc"/>')
            parts.append(
                f'<text x="{x + cell_w / 2}" y="{y + 28}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#102a43">{"S" if ok else "F"}</text>'
            )
            parts.append(
                f'<text x="{x + cell_w / 2}" y="{y + 50}" text-anchor="middle" font-family="Courier New, monospace" font-size="10" fill="#243b53">B {escape(sci(backdrive))}</text>'
            )

    parts.append("</svg>")
    BOUNDARY_FIGURE.write_text("\n".join(parts) + "\n", encoding="utf-8")


def build_summary(startup_rows: list[dict], falsifier_rows: list[dict], pairwise_rows: list[dict]) -> dict:
    by_case_design = {(row["case_id"], row["design"]): row for row in falsifier_rows}
    surviving_cases = []
    for case_id in sorted({row["case_id"] for row in falsifier_rows}):
        champion = by_case_design[(case_id, "champion")]
        fixed = by_case_design[(case_id, "fixed")]
        nonaware = by_case_design[(case_id, "nonaware")]
        champion_ok = (champion["startup_ok"] or 0.0) >= 0.5
        fixed_ok = (fixed["startup_ok"] or 0.0) >= 0.5
        nonaware_ok = (nonaware["startup_ok"] or 0.0) >= 0.5
        nonaware_backdrive = nonaware["e_backdrive_j"] or 0.0
        champion_backdrive = champion["e_backdrive_j"] or 0.0
        faster_than_nonaware = (
            champion_ok
            and nonaware_ok
            and champion["t_handoff_s"] is not None
            and nonaware["t_handoff_s"] is not None
            and champion["t_handoff_s"] < nonaware["t_handoff_s"]
        )
        if (
            (champion_ok and not fixed_ok)
            or (champion_ok and not nonaware_ok)
            or (champion_ok and nonaware_ok and faster_than_nonaware and champion_backdrive < nonaware_backdrive)
        ):
            surviving_cases.append(case_id)

    return {
        "startup_source": str(STARTUP_RESULTS.relative_to(REPO_ROOT)),
        "falsifier_source": str(FALSIFIER_RESULTS.relative_to(REPO_ROOT)),
        "sensitivity_table": str(SENSITIVITY_TABLE.relative_to(REPO_ROOT)),
        "pairwise_table": str(PAIRWISE_TABLE.relative_to(REPO_ROOT)),
        "startup_figure": str(STARTUP_FIGURE.relative_to(REPO_ROOT)),
        "boundary_figure": str(BOUNDARY_FIGURE.relative_to(REPO_ROOT)),
        "surviving_falsifier_cases": surviving_cases,
        "primary_matrix_pairwise_totals": {
            row["comparison"]: {
                "lower_ctrl_total": sum(
                    item["champion_lower_ctrl_cases"]
                    for item in pairwise_rows
                    if item["comparison"] == row["comparison"] and item["factor"] == "ramp_mvps"
                ),
                "better_startup_total": sum(
                    item["champion_better_startup_cases"]
                    for item in pairwise_rows
                    if item["comparison"] == row["comparison"] and item["factor"] == "ramp_mvps"
                ),
            }
            for row in pairwise_rows
            if row["factor"] == "ramp_mvps"
        },
    }


def main() -> int:
    startup_rows = load_rows(STARTUP_RESULTS)
    falsifier_rows = load_rows(FALSIFIER_RESULTS)
    sensitivity_rows = summarize_startup(startup_rows)
    pairwise_rows = summarize_pairwise(startup_rows)

    write_csv(
        SENSITIVITY_TABLE,
        sensitivity_rows,
        [
            "factor",
            "value",
            "design",
            "total_cases",
            "startup_successes",
            "startup_success_rate",
            "median_t_handoff_s_success",
            "median_e_ctrl_j_success",
            "median_e_backdrive_j_all",
        ],
    )
    write_csv(
        PAIRWISE_TABLE,
        pairwise_rows,
        [
            "factor",
            "value",
            "comparison",
            "total_cases",
            "champion_better_startup_cases",
            "champion_faster_cases",
            "champion_lower_ctrl_cases",
            "champion_lower_backdrive_cases",
        ],
    )

    render_startup_figure(sensitivity_rows)
    render_falsifier_figure(falsifier_rows)

    ANALYSIS_SUMMARY.write_text(
        json.dumps(build_summary(startup_rows, falsifier_rows, pairwise_rows), indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "sensitivity_table": str(SENSITIVITY_TABLE.relative_to(REPO_ROOT)),
                "pairwise_table": str(PAIRWISE_TABLE.relative_to(REPO_ROOT)),
                "summary": str(ANALYSIS_SUMMARY.relative_to(REPO_ROOT)),
                "startup_figure": str(STARTUP_FIGURE.relative_to(REPO_ROOT)),
                "boundary_figure": str(BOUNDARY_FIGURE.relative_to(REPO_ROOT)),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
