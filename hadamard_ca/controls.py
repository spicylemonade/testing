from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import numpy as np

from .harness import canonical_fingerprint, correlation_coefficients


@dataclass(frozen=True)
class ExactControl:
    length: int
    order: int
    q: tuple[int, ...]
    s: tuple[int, ...]
    canonical_fingerprint: str


def _canonical_pair(q: tuple[int, ...], s: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray]:
    q_vec = np.asarray(q, dtype=np.int8)
    s_vec = np.asarray(s, dtype=np.int8)
    variants = [
        (q_vec, s_vec),
        (-q_vec, s_vec),
        (q_vec, -s_vec),
        (-q_vec, -s_vec),
    ]
    canonical = min(
        variants,
        key=lambda pair: (
            "".join("+" if int(v) > 0 else "-" for v in pair[0].tolist()),
            "".join("+" if int(v) > 0 else "-" for v in pair[1].tolist()),
        ),
    )
    return canonical


def solve_exact_control(length: int) -> ExactControl:
    if length <= 0 or length % 2 == 0:
        raise ValueError("control length must be a positive odd integer")
    for bits in product((-1, 1), repeat=2 * length):
        q = tuple(int(v) for v in bits[:length])
        s = tuple(int(v) for v in bits[length:])
        coeffs = correlation_coefficients(np.asarray(q, dtype=np.int8), np.asarray(s, dtype=np.int8))
        if np.count_nonzero(coeffs[1:]) != 0:
            continue
        q_vec, s_vec = _canonical_pair(q, s)
        return ExactControl(
            length=length,
            order=4 * length,
            q=tuple(int(v) for v in q_vec.tolist()),
            s=tuple(int(v) for v in s_vec.tolist()),
            canonical_fingerprint=canonical_fingerprint(q_vec, s_vec),
        )
    raise RuntimeError(f"no exact control found for length {length}")


def default_exact_controls() -> list[ExactControl]:
    return [solve_exact_control(length) for length in (5, 7)]
