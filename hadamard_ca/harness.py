from __future__ import annotations

import hashlib
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np

from .seed import aperiodic_autocorrelation, gs_matrix, prime_involution


ArrayLike = np.ndarray


@dataclass
class SearchConfig:
    method_name: str
    evaluation_budget: int
    restart_count: int = 1
    seed: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    q: ArrayLike
    s: ArrayLike
    evaluations: int
    completed_restarts: int
    restart_statistics: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)
    best_objective: dict[str, int] | None = None
    trace: list[dict[str, Any]] = field(default_factory=list)


SearchMethod = Callable[[ArrayLike, ArrayLike, SearchConfig], SearchResult]


def derived_quadruple(q: ArrayLike, s: ArrayLike) -> tuple[ArrayLike, ArrayLike, ArrayLike, ArrayLike]:
    q_vec = np.asarray(q, dtype=np.int8)
    s_vec = np.asarray(s, dtype=np.int8)
    sq = (q_vec * s_vec).astype(np.int8)
    return s_vec, prime_involution(s_vec), sq, prime_involution(sq)


def correlation_coefficients(q: ArrayLike, s: ArrayLike) -> np.ndarray:
    a, b, c, d = derived_quadruple(q, s)
    return (
        aperiodic_autocorrelation(a)
        + aperiodic_autocorrelation(b)
        + aperiodic_autocorrelation(c)
        + aperiodic_autocorrelation(d)
    ).astype(np.int32)


def objective_summary(q: ArrayLike, s: ArrayLike) -> dict[str, int]:
    coeffs = correlation_coefficients(q, s)[1:]
    support = coeffs[np.nonzero(coeffs)]
    return {
        "support_size": int(np.count_nonzero(coeffs)),
        "l1": int(np.sum(np.abs(coeffs))),
        "max_abs": int(np.max(np.abs(coeffs))) if support.size else 0,
    }


def _sign_string(seq: ArrayLike) -> str:
    return "".join("+" if int(value) > 0 else "-" for value in np.asarray(seq).tolist())


def canonical_fingerprint(q: ArrayLike, s: ArrayLike) -> str:
    q_vec = np.asarray(q, dtype=np.int8)
    s_vec = np.asarray(s, dtype=np.int8)
    variants = [
        (_sign_string(q_vec), _sign_string(s_vec)),
        (_sign_string(-q_vec), _sign_string(s_vec)),
        (_sign_string(q_vec), _sign_string(-s_vec)),
        (_sign_string(-q_vec), _sign_string(-s_vec)),
    ]
    canonical = min(variants)
    return hashlib.sha256(f"{canonical[0]}|{canonical[1]}".encode("ascii")).hexdigest()


def _full_gram_defect(q: ArrayLike, s: ArrayLike) -> np.ndarray:
    matrix = gs_matrix(*derived_quadruple(q, s))
    order = matrix.shape[0]
    return (matrix @ matrix.T) - order * np.eye(order, dtype=np.int32)


def evaluate_state(
    q: ArrayLike,
    s: ArrayLike,
    *,
    method_name: str,
    evaluations: int,
    wall_seconds: float,
    restart_statistics: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    q_vec = np.asarray(q, dtype=np.int8)
    s_vec = np.asarray(s, dtype=np.int8)
    coeffs = correlation_coefficients(q_vec, s_vec)
    coeff_support = coeffs[1:]
    defect = _full_gram_defect(q_vec, s_vec)
    off_diagonal = defect[~np.eye(defect.shape[0], dtype=bool)]
    nonzero_off_diagonal = off_diagonal[np.nonzero(off_diagonal)]
    defect_histogram = {
        str(value): count
        for value, count in sorted(Counter(int(value) for value in nonzero_off_diagonal).items())
    }
    return {
        "method_name": method_name,
        "order": int(4 * len(q_vec)),
        "seed_length": int(len(q_vec)),
        "exact_hit": bool(np.count_nonzero(coeff_support) == 0),
        "correlation_defect_support_size": int(np.count_nonzero(coeff_support)),
        "off_diagonal_gram_defect_support_size": int(np.count_nonzero(off_diagonal)),
        "max_defect_magnitude": int(np.max(np.abs(nonzero_off_diagonal))) if nonzero_off_diagonal.size else 0,
        "defect_histogram": defect_histogram,
        "objective_summary": objective_summary(q_vec, s_vec),
        "wall_seconds": float(wall_seconds),
        "objective_evaluations": int(evaluations),
        "restart_statistics": restart_statistics or {},
        "canonical_fingerprint": canonical_fingerprint(q_vec, s_vec),
        "metadata": metadata or {},
    }


def run_harness(
    method: SearchMethod,
    initial_q: ArrayLike,
    initial_s: ArrayLike,
    config: SearchConfig,
) -> dict[str, Any]:
    start = time.perf_counter()
    result = method(np.asarray(initial_q, dtype=np.int8), np.asarray(initial_s, dtype=np.int8), config)
    wall_seconds = time.perf_counter() - start
    metrics = evaluate_state(
        result.q,
        result.s,
        method_name=config.method_name,
        evaluations=result.evaluations,
        wall_seconds=wall_seconds,
        restart_statistics=result.restart_statistics,
        metadata={**config.metadata, **result.metadata},
    )
    if result.best_objective is not None:
        metrics["best_objective"] = result.best_objective
    if result.trace:
        metrics["trace"] = result.trace
    return metrics
