from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Iterable

import numpy as np

FRONTIER_PDF_URL = "https://ajc.maths.uq.edu.au/pdf/93/ajc_v93_p422.pdf"
FRONTIER_PDF_SHA256 = "92e2e91953bfb6dbf26efe806137c55c40631cf6f59ef3680ed209a9065e4605"

Q_RUN_LENGTHS = (83, 2, 81, 1)
S_RUN_LENGTHS = (
    *(4 for _ in range(5)),
    *(value for _ in range(5) for value in (2, 1, 1)),
    1,
    5,
    *(4 for _ in range(4)),
    *(value for _ in range(6) for value in (2, 1, 1)),
    *(4 for _ in range(4)),
    3,
    *(value for _ in range(5) for value in (1, 2, 1)),
    3,
    *(4 for _ in range(4)),
    3,
    *(value for _ in range(5) for value in (1, 2, 1)),
)

Q_COMPACT_RLE = "(83, 2, 81, 1)"
S_COMPACT_RLE = (
    "(4)^5(2,1,1)^5(1,5)(4)^4(2,1,1)^6(4)^4(3)"
    "(1,2,1)^5(3)(4)^4(3)(1,2,1)^5"
)

EXPECTED_EXCEPTIONAL_COEFFICIENTS = {
    4: -512,
    8: 384,
    12: -256,
    16: 128,
    26: -64,
    30: 128,
    34: -192,
    38: 256,
    42: -320,
    46: 256,
    50: -192,
    54: 128,
    58: -64,
}


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def decode_run_lengths(run_lengths: Iterable[int], start_sign: int = 1) -> np.ndarray:
    values: list[int] = []
    sign = int(start_sign)
    for run in run_lengths:
        if int(run) <= 0:
            raise ValueError(f"run lengths must be positive, got {run}")
        values.extend([sign] * int(run))
        sign *= -1
    return np.asarray(values, dtype=np.int8)


def prime_involution(seq: np.ndarray) -> np.ndarray:
    result = np.asarray(seq, dtype=np.int8).copy()
    midpoint = (len(result) + 1) // 2
    result[midpoint:] *= -1
    return result


def aperiodic_autocorrelation(seq: np.ndarray) -> np.ndarray:
    vector = np.asarray(seq, dtype=np.int16)
    n = len(vector)
    return np.asarray(
        [
            int(np.dot(vector[: n - lag], vector[lag:]))
            for lag in range(n)
        ],
        dtype=np.int32,
    )


def circulant(first_row: np.ndarray) -> np.ndarray:
    row = np.asarray(first_row, dtype=np.int8)
    size = len(row)
    return np.asarray([np.roll(row, shift) for shift in range(size)], dtype=np.int8)


def gs_matrix(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    a_mat, b_mat, c_mat, d_mat = (circulant(seq) for seq in (a, b, c, d))
    size = len(a)
    back_identity = np.fliplr(np.eye(size, dtype=np.int8))
    return np.block(
        [
            [a_mat, b_mat @ back_identity, c_mat @ back_identity, d_mat @ back_identity],
            [-b_mat @ back_identity, a_mat, -(d_mat.T) @ back_identity, (c_mat.T) @ back_identity],
            [-c_mat @ back_identity, (d_mat.T) @ back_identity, a_mat, -(b_mat.T) @ back_identity],
            [-d_mat @ back_identity, -(c_mat.T) @ back_identity, (b_mat.T) @ back_identity, a_mat],
        ]
    ).astype(np.int16)


def published_frontier_sequences() -> dict[str, np.ndarray]:
    q = decode_run_lengths(Q_RUN_LENGTHS)
    s = decode_run_lengths(S_RUN_LENGTHS)
    sq = (q * s).astype(np.int8)
    return {
        "q": q,
        "s": s,
        "s_prime": prime_involution(s),
        "sq": sq,
        "sq_prime": prime_involution(sq),
    }


def published_frontier_coefficients() -> np.ndarray:
    sequences = published_frontier_sequences()
    coeffs = (
        aperiodic_autocorrelation(sequences["s"])
        + aperiodic_autocorrelation(sequences["s_prime"])
        + aperiodic_autocorrelation(sequences["sq"])
        + aperiodic_autocorrelation(sequences["sq_prime"])
    )
    return coeffs.astype(np.int32)


def _sign_string(seq: np.ndarray) -> str:
    return "".join("+" if int(value) > 0 else "-" for value in seq.tolist())


def _sequence_checksum(seq: np.ndarray) -> str:
    return _sha256_bytes(_sign_string(seq).encode("ascii"))


def published_frontier_validation() -> dict[str, object]:
    sequences = published_frontier_sequences()
    coeffs = published_frontier_coefficients()
    exceptional = {lag: int(coeffs[lag]) for lag in range(1, len(coeffs)) if int(coeffs[lag]) != 0}
    matrix = gs_matrix(
        sequences["s"],
        sequences["s_prime"],
        sequences["sq"],
        sequences["sq_prime"],
    )
    gram = matrix @ matrix.T
    expected_diagonal = 4 * len(sequences["q"])
    defect = gram - expected_diagonal * np.eye(matrix.shape[0], dtype=np.int32)
    nonzero_row = defect[0][np.nonzero(defect[0])[0]]
    row_histogram = {
        str(value): count
        for value, count in sorted(Counter(int(value) for value in nonzero_row).items())
    }
    return {
        "length": int(len(sequences["q"])),
        "order": int(matrix.shape[0]),
        "exceptional_coefficients": exceptional,
        "exceptional_match": exceptional == EXPECTED_EXCEPTIONAL_COEFFICIENTS,
        "nonzero_coeff_count": int(np.count_nonzero(coeffs[1:])),
        "row_nonzero_off_diagonal_count": int(np.count_nonzero(defect[0])),
        "row_defect_histogram": row_histogram,
        "max_abs_defect": int(np.max(np.abs(defect))),
        "mod_64_ok": bool(np.array_equal(gram % 64, (expected_diagonal * np.eye(matrix.shape[0], dtype=np.int32)) % 64)),
        "q_checksum": _sequence_checksum(sequences["q"]),
        "s_checksum": _sequence_checksum(sequences["s"]),
        "matrix_checksum": _sha256_bytes(matrix.tobytes()),
    }


def published_frontier_manifest_payload() -> dict[str, object]:
    sequences = published_frontier_sequences()
    validation = published_frontier_validation()
    return {
        "source": {
            "paper_title": "A 64-Modular Hadamard Matrix of Order 668",
            "paper_author": "Shalom Eliahou",
            "paper_year": 2025,
            "paper_venue": "Australasian Journal of Combinatorics",
            "paper_url": FRONTIER_PDF_URL,
            "paper_sha256": FRONTIER_PDF_SHA256,
            "relevant_pages": [5],
        },
        "raw_artifact_location": FRONTIER_PDF_URL,
        "encoding": {
            "q_compact_rle": Q_COMPACT_RLE,
            "s_compact_rle": S_COMPACT_RLE,
            "q_run_lengths": list(Q_RUN_LENGTHS),
            "s_run_lengths": list(S_RUN_LENGTHS),
        },
        "canonical_representative": {
            "description": (
                "Published start-sign convention preserved. No cyclic shift, global sign flip, "
                "or block permutation applied beyond the paper's compact encoding and the fixed "
                "prime involution used to derive s' and (sq)'."
            ),
            "q_signs": _sign_string(sequences["q"]),
            "s_signs": _sign_string(sequences["s"]),
            "q_checksum": validation["q_checksum"],
            "s_checksum": validation["s_checksum"],
            "matrix_checksum": validation["matrix_checksum"],
        },
        "symmetry_operations_applied": [
            {
                "operation": "identity",
                "reason": "The published compact encoding is already used as the canonical seed representative for this run.",
            }
        ],
        "validation": validation,
    }


def manifest_json() -> str:
    return json.dumps(published_frontier_manifest_payload(), indent=2)
