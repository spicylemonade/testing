#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from minigrav.benchmarks.analytic_controls import run_analytic_controls


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_JSON = ROOT / "results" / "verification" / "analytic_controls.json"
OUTPUT_MD = ROOT / "results" / "verification" / "analytic_controls.md"


def _markdown_table_rows(name: str, rows: list[dict]) -> list[str]:
    lines = [f"## {name.replace('_', ' ').title()}", "", "| dt | key metric(s) | pass |", "| --- | --- | --- |"]
    for row in rows:
        if name == "circular_orbit":
            metric = f"radial_rms={row['value']:.3e}"
        elif name == "ellipse_shape":
            metric = f"rp={row['periapsis_error']:.3e}, ra={row['apoapsis_error']:.3e}"
        elif name == "period_recovery":
            metric = f"period_err={row['value']:.3e}"
        elif name == "escape_velocity":
            metric = f"unbound={row['predicted_unbound']}, v_inf_err={row['value']:.3e}"
        else:
            metric = (
                f"a={row['semi_major_axis_error']:.3e}, e={row['eccentricity_error']:.3e}, "
                f"i={row['inclination_error']:.3e}, omega={row['argument_of_periapsis_error']:.3e}"
            )
        lines.append(f"| {row['dt']:.3f} | {metric} | {'pass' if row['pass'] else 'fail'} |")
    lines.append("")
    return lines


def main() -> int:
    payload = run_analytic_controls()
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")

    md_lines = ["# Analytic Controls", "", f"Generated: {payload['generated_at']}", ""]
    for name, rows in payload["controls"].items():
        md_lines.extend(_markdown_table_rows(name, rows))
    OUTPUT_MD.write_text("\n".join(md_lines) + "\n")
    print(f"wrote {OUTPUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUTPUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
