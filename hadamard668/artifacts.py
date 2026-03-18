from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

from hadamard668.core import (
    alternating_pm1_from_runs,
    combined_aperiodic_pm1_autocorrelation,
    decode_base8_columns,
    ensure_dir,
    involution_zero,
    parse_run_length_notation,
    periodic_binary_autocorrelation_half,
    pointwise_product,
    support_from_bits,
    two_adic_modulus,
)
from hadamard668.verifiers import structured_qs_state

RESULTS_DIR = Path("results/artifacts")

CONTROL_79_ENCODED = (
    "4 3 3 2 7 1 0 1 7 4 6 3 1 0 0 0 1 5 7 3 6 1 1 1 6 5 5 4 3 4 7 4 6 2 0 2 "
    "7 0 5 4 0 1 0 3 2 0 6 6 4 3 0 3 4 1 1 2 5 1 5 2 7 7 1 5 4 0 0 1 3 2 0 7 "
    "5 0 5 7 2 7 3"
)
CONTROL_79_TARGET = [
    int(value)
    for value in (
        "22 23 25 25 26 24 25 21 22 23 24 22 24 21 24 21 24 26 25 24 24 21 25 "
        "25 22 24 21 22 21 26 20 21 23 23 23 21 25 23 22"
    ).split()
]
CONTROL_79_SOLUTION = (
    "1 1 1 0 1 1 0 1 1 0 0 1 1 0 0 0 1 1 1 1 0 1 1 1 0 1 1 0 1 0 1 0 0 0 0 0 "
    "1 0 1 0 0 1 0 1 0 0 0 0 0 1 0 1 0 1 1 0 1 1 1 0 1 1 1 1 0 0 0 1 1 0 0 1 "
    "1 0 1 1 0 1 1"
)

TARGET_167_ENCODED = (
    "1 6 1 6 7 1 1 6 1 0 7 6 6 0 6 0 7 0 1 7 0 0 1 6 1 0 6 7 7 6 0 1 6 7 1 6 "
    "0 0 0 0 6 7 7 1 1 0 1 0 1 0 1 1 7 0 0 1 0 1 1 1 6 6 7 6 1 0 1 7 6 1 7 6 "
    "1 0 1 1 0 6 6 6 0 1 6 0 7 0 0 6 0 7 7 0 6 0 7 1 0 7 0 0 6 6 7 0 6 6 1 0 "
    "0 0 1 7 0 0 1 7 0 6 6 0 1 0 6 7 7 7 1 0 7 6 1 7 7 0 7 6 6 0 7 1 7 1 7 1 "
    "7 0 0 6 1 6 6 6 1 7 7 7 6 1 6 7 0 0 0 1 6 0 0"
)
TARGET_167_AUTOCORR = [
    int(value)
    for value in (
        "41 37 40 39 41 39 35 38 36 34 42 39 37 37 32 37 37 36 36 36 40 39 36 "
        "37 39 38 35 33 39 35 37 41 42 40 41 38 43 41 34 39 39 36 42 39 38 41 "
        "40 40 37 38 37 37 35 37 37 37 36 38 37 34 37 40 39 37 38 38 42 38 42 "
        "37 34 39 39 37 41 36 34 37 38 42 45 39 40"
    ).split()
]

ELIAHOU_Q = "(83,2,81,1)"
ELIAHOU_S = (
    "(4)5(2,1,1)5(1,5)(4)4(2,1,1)6(4)4(3)(1,2,1)5(3)(4)4(3)(1,2,1)5"
)

STRUCTURED_H2_Q9 = [1, -1, -1, -1, -1, -1, -1, -1, -1]
STRUCTURED_H2_S9 = [-1, -1, 1, -1, -1, 1, -1, -1, -1]

CONSTANTINE_SOURCE = {
    "paper": "G. Constantine and T. Constantine, Convolution numbers: the cyclic case (2025)",
    "source_kind": "arXiv HTML mirror",
    "source_ref": "arXiv:2501.18066",
    "source_locator": {
        "control_lines": "lines 127-135",
        "target_lines": "lines 136-139",
    },
}

ELIAHOU_SOURCE = {
    "paper": "M. Eliahou, A 64-modular Hadamard matrix of order 668 (2025)",
    "source_kind": "journal PDF",
    "source_ref": "Australasian Journal of Combinatorics 93(2), pp. 422-429",
    "source_locator": {
        "construction_lines": "lines 155-160",
    },
}

STRUCTURED_H2_CONTROL_SOURCE = {
    "paper": "Hadamard-668 repository structured q/s control",
    "source_kind": "deterministic exhaustive in-repo search over all +/-1 q,s seeds of length 9",
    "source_ref": "python3 -m hadamard668.artifacts export",
    "source_locator": {
        "exact_q": "lexicographically minimal exact length-9 q sequence found by exhaustive search",
        "exact_s": "paired exact length-9 s sequence found by exhaustive search",
    },
}


def _binary_artifact(length: int, encoded: str, target: List[int], label: str) -> Dict[str, object]:
    vectors = decode_base8_columns(encoded)
    artifact = {
        "label": label,
        "length": length,
        "fixed_vectors": [],
        "target_periodic_autocorrelation_half": target,
    }
    for index, bits in enumerate(vectors, start=1):
        autocorr = periodic_binary_autocorrelation_half(bits)
        artifact["fixed_vectors"].append(
            {
                "name": f"fixed_{index}",
                "weight": int(sum(bits)),
                "support": support_from_bits(bits),
                "periodic_autocorrelation_half": autocorr,
            }
        )
    return artifact


def build_control_79() -> Dict[str, object]:
    artifact = _binary_artifact(79, CONTROL_79_ENCODED, CONTROL_79_TARGET, "control_4x79")
    solution_bits = [int(ch) for ch in CONTROL_79_SOLUTION.split()]
    if len(solution_bits) != 79:
        raise ValueError("79-control solution length mismatch")
    solution_autocorr = periodic_binary_autocorrelation_half(solution_bits)
    if solution_autocorr != CONTROL_79_TARGET:
        raise ValueError("79-control solution does not match target autocorrelation")
    artifact.update(
        {
            "source": CONSTANTINE_SOURCE,
            "template": "4 x p cyclic / supplementary-difference-set control",
            "solution": {
                "name": "solved_fourth_vector",
                "weight": int(sum(solution_bits)),
                "support": support_from_bits(solution_bits),
                "periodic_autocorrelation_half": solution_autocorr,
            },
            "verification": {
                "checks": [
                    "decoded fixed-vector weights must be [34, 34, 42]",
                    "solved fourth-vector weight must be 43",
                    "solved fourth-vector periodic autocorrelation must equal the target vector",
                ],
                "command": "python3 -m hadamard668.artifacts export",
            },
        }
    )
    weights = [item["weight"] for item in artifact["fixed_vectors"]]
    if weights != [34, 34, 42]:
        raise ValueError(f"Unexpected 79-control fixed-vector weights: {weights}")
    return artifact


def build_target_167() -> Dict[str, object]:
    artifact = _binary_artifact(167, TARGET_167_ENCODED, TARGET_167_AUTOCORR, "target_167_weight_80")
    artifact.update(
        {
            "source": CONSTANTINE_SOURCE,
            "template": "4 x p cyclic / supplementary-difference-set obstruction",
            "unknown_vector": {
                "required_weight": 80,
                "target_periodic_autocorrelation_half": TARGET_167_AUTOCORR,
            },
            "verification": {
                "checks": [
                    "decoded fixed-vector weights must be [76, 76, 77]",
                    "the unresolved fourth support must have weight 80",
                    "the stored target periodic autocorrelation is the exact vector reported in the paper",
                ],
                "command": "python3 -m hadamard668.artifacts export",
            },
        }
    )
    weights = [item["weight"] for item in artifact["fixed_vectors"]]
    if weights != [76, 76, 77]:
        raise ValueError(f"Unexpected 167-target fixed-vector weights: {weights}")
    return artifact


def build_seed_668_mod64() -> Dict[str, object]:
    q_runs = parse_run_length_notation(ELIAHOU_Q)
    s_runs = parse_run_length_notation(ELIAHOU_S)
    q = alternating_pm1_from_runs(q_runs, start=1)
    s = alternating_pm1_from_runs(s_runs, start=1)
    if len(q) != 167 or len(s) != 167:
        raise ValueError("Eliahou seed sequences must both have length 167")
    s_zero = involution_zero(s)
    sq = pointwise_product(s, q)
    sq_zero = involution_zero(sq)
    combined = combined_aperiodic_pm1_autocorrelation([s, s_zero, sq, sq_zero])
    nonzero = [
        {"shift": shift, "value": value}
        for shift, value in enumerate(combined, start=1)
        if value != 0
    ]
    artifact = {
        "label": "seed_668_mod64",
        "source": ELIAHOU_SOURCE,
        "length": 167,
        "order": 668,
        "construction_family": "Goethals-Seidel quadruple derived from (q, s)",
        "q_run_lengths": q_runs,
        "s_run_lengths": s_runs,
        "sequences": {
            "A": s,
            "B": s_zero,
            "C": sq,
            "D": sq_zero,
        },
        "combined_aperiodic_pm1_autocorrelation": combined,
        "nonzero_defects": nonzero,
        "two_adic_modulus": two_adic_modulus(combined),
        "verification": {
            "checks": [
                "all nonzero combined aperiodic autocorrelations are multiples of 64",
                "the two-adic modulus of the combined aperiodic autocorrelation vector is 64",
                "the nonzero shift set matches the theorem statement up to symmetry",
            ],
            "command": "python3 -m hadamard668.artifacts export",
        },
    }
    if artifact["two_adic_modulus"] != 64:
        raise ValueError(f"Unexpected two-adic modulus for Eliahou seed: {artifact['two_adic_modulus']}")
    return artifact


def build_structured_h2_control_n9() -> Dict[str, object]:
    exact_pair = None
    for q_mask in range(1 << 9):
        q = [1 if q_mask & (1 << idx) else -1 for idx in range(9)]
        for s_mask in range(1 << 9):
            s = [1 if s_mask & (1 << idx) else -1 for idx in range(9)]
            state = structured_qs_state(q, s, target_modulus=None)
            if bool(state["exact_certificate"]):
                candidate = (tuple(q), tuple(s))
                if exact_pair is None or candidate < exact_pair:
                    exact_pair = candidate
    if exact_pair is None:
        raise ValueError("expected at least one exact length-9 structured q/s control")
    exact_q = list(exact_pair[0])
    exact_s = list(exact_pair[1])
    exact_state = structured_qs_state(exact_q, exact_s, target_modulus=None)
    s_candidates = []
    q_candidates = []
    for index in range(9):
        start_s = list(exact_s)
        start_s[index] *= -1
        s_candidates.append(
            {
                "index": index,
                "q": list(exact_q),
                "s": start_s,
                "state": structured_qs_state(exact_q, start_s, target_modulus=None),
            }
        )
        start_q = list(exact_q)
        start_q[index] *= -1
        q_candidates.append(
            {
                "index": index,
                "q": start_q,
                "s": list(exact_s),
                "state": structured_qs_state(start_q, exact_s, target_modulus=None),
            }
        )
    s_candidates = [
        item
        for item in s_candidates
        if (not bool(item["state"]["exact_certificate"])) and int(item["state"]["quality_rank"]) > 0
    ]
    q_candidates = [
        item
        for item in q_candidates
        if (not bool(item["state"]["exact_certificate"])) and int(item["state"]["quality_rank"]) > 0
    ]
    if not s_candidates or not q_candidates:
        raise ValueError("expected nontrivial single-flip starts for the structured H2 control")
    sparse_s = min(
        s_candidates,
        key=lambda item: (
            -int(item["state"]["quality_rank"]),
            int(item["state"]["l1_defect"]),
            int(item["state"]["defect_count"]),
            int(item["index"]),
        ),
    )
    dense_s = max(
        s_candidates,
        key=lambda item: (
            int(item["state"]["quality_rank"]),
            int(item["state"]["l1_defect"]),
            int(item["state"]["defect_count"]),
            int(item["index"]),
        ),
    )
    best_q = min(
        q_candidates,
        key=lambda item: (
            -int(item["state"]["quality_rank"]),
            int(item["state"]["l1_defect"]),
            int(item["state"]["defect_count"]),
            int(item["index"]),
        ),
    )
    lift_starts = []
    for name, variable_family, candidate in (
        ("sflip_mod_sparse", "s", sparse_s),
        ("qflip_mod_sparse", "q", best_q),
        ("sflip_mod_dense", "s", dense_s),
    ):
        lift_starts.append(
            {
                "name": f"{name}_idx{candidate['index']}",
                "variable_family": variable_family,
                "operation": {"which": variable_family, "index": int(candidate["index"])},
                "q": candidate["q"],
                "s": candidate["s"],
                "state": candidate["state"],
            }
        )
    return {
        "label": "h2_control_structured_n9",
        "length": 9,
        "source": STRUCTURED_H2_CONTROL_SOURCE,
        "search_space": {
            "q_count": 512,
            "s_count": 512,
            "total_pairs": 262144,
        },
        "exact_seed": {
            "q": exact_q,
            "s": exact_s,
            "state": exact_state,
        },
        "lift_starts": lift_starts,
        "verification": {
            "checks": [
                "the exact structured q/s seed must have zero combined aperiodic autocorrelation",
                "the q-flip start must expose a nonzero modulus-lift task",
                "the two s-flip starts must expose distinct defect complexity under the same variable family",
            ],
            "command": "python3 -m hadamard668.artifacts export",
        },
    }


def export(output_dir: Path = RESULTS_DIR) -> Dict[str, Path]:
    ensure_dir(output_dir)
    control = build_control_79()
    target = build_target_167()
    seed = build_seed_668_mod64()
    h2_control = build_structured_h2_control_n9()
    outputs = {
        "control_4x79": output_dir / "control_4x79.json",
        "target_167_weight_80": output_dir / "target_167_weight_80.json",
        "seed_668_mod64": output_dir / "seed_668_mod64.json",
        "h2_control_structured_n9": output_dir / "h2_control_structured_n9.json",
    }
    outputs["control_4x79"].write_text(json.dumps(control, indent=2))
    outputs["target_167_weight_80"].write_text(json.dumps(target, indent=2))
    outputs["seed_668_mod64"].write_text(json.dumps(seed, indent=2))
    outputs["h2_control_structured_n9"].write_text(json.dumps(h2_control, indent=2))
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Hadamard-668 research artifacts from primary-source encodings.")
    parser.add_argument("command", choices=["export"])
    parser.add_argument("--output-dir", default=str(RESULTS_DIR))
    args = parser.parse_args()
    if args.command == "export":
        outputs = export(Path(args.output_dir))
        for label, path in outputs.items():
            print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
