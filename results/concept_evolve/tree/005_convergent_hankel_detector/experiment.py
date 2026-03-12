#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from special_numbers.diagnostics import verify_relation
from special_numbers.recurrence import find_exact_relation
from special_numbers.slopes import convergents, floor_value, get_slope


TARGET_SLOPES = [
    "phi",
    "one_plus_sqrt2",
    "plastic",
    "sqrt2",
    "salem_quartic",
    "e",
]


def hankel_rank(values: list[int], width: int = 4) -> int:
    import sympy as sp

    if len(values) < 2 * width - 1:
        return -1
    block = [[values[i + j] for j in range(width)] for i in range(width)]
    return int(sp.Matrix(block).rank())


def run_case(slope_id: str) -> dict[str, object]:
    triples = convergents(slope_id, 40)
    even_denoms = [q for idx, _p, q in triples if idx % 2 == 0][:20]
    sampled = [floor_value(slope_id, q) for q in even_denoms]
    candidate = find_exact_relation(sampled[:12], max_order=4)
    verification = verify_relation(sampled, candidate["coefficients"]) if candidate else None
    return {
        "slope_id": slope_id,
        "label": get_slope(slope_id).label,
        "kind": get_slope(slope_id).kind,
        "selector": {
            "family": "quadratic_convergent_even",
            "indices": even_denoms,
        },
        "sampled_values": sampled,
        "hankel_rank_4x4": hankel_rank(sampled),
        "candidate_from_first_12": candidate,
        "holdout_verification": verification,
        "exact_success": bool(verification and verification.get("holds")),
    }


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    payload = {
        "concept": "005_convergent_hankel_detector",
        "construction": "every second convergent denominator; recurrence fit on first 12 samples; exact holdout on first 20 samples",
        "runs": [run_case(slope_id) for slope_id in TARGET_SLOPES],
    }
    out_path = out_dir / "results.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(out_path)


if __name__ == "__main__":
    main()
