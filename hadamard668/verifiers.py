from __future__ import annotations

import math
from typing import Dict, Mapping, Sequence

from hadamard668.core import (
    combined_aperiodic_pm1_autocorrelation,
    cyclic_canonical_binary,
    l1_distance,
    max_abs,
    pointwise_product,
    periodic_binary_autocorrelation_half,
    power_spectral_density,
    signed_reversal_canonical_tuple,
    support_from_bits,
    two_adic_modulus,
)


def psd_check(bits: Sequence[int], tolerance: float = 1e-9) -> Dict[str, object]:
    values = power_spectral_density(bits)
    minimum = min(values, default=0.0)
    maximum = max(values, default=0.0)
    return {
        "sample_count": len(values),
        "min_value": minimum,
        "max_value": maximum,
        "nonnegative_with_tolerance": minimum >= -tolerance,
        "tolerance": tolerance,
    }


def support_state(bits: Sequence[int], target: Sequence[int]) -> Dict[str, object]:
    corr = periodic_binary_autocorrelation_half(bits)
    debt = [int(left) - int(right) for left, right in zip(corr, target)]
    return {
        "length": len(bits),
        "weight": int(sum(bits)),
        "support": support_from_bits(bits),
        "canonical_orbit": cyclic_canonical_binary(bits),
        "periodic_autocorrelation_half": corr,
        "autocorrelation_debt": debt,
        "closest_target_distance": l1_distance(corr, target),
        "max_defect_magnitude": max_abs(debt),
        "exact_hit": corr == list(target),
        "psd_check": psd_check(bits),
    }


def support_objective(state: Mapping[str, object]) -> tuple[int, int]:
    return (
        int(state["closest_target_distance"]),
        int(state["max_defect_magnitude"]),
    )


def structured_sequences(q: Sequence[int], s: Sequence[int]) -> Dict[str, list[int]]:
    q_list = [int(value) for value in q]
    s_list = [int(value) for value in s]
    if len(q_list) != len(s_list):
        raise ValueError("q and s must have equal length")
    half = len(s_list) // 2 + 1
    s_zero = [
        int(value) if idx < half else -int(value)
        for idx, value in enumerate(s_list)
    ]
    sq = pointwise_product(s_list, q_list)
    sq_zero = [
        int(value) if idx < half else -int(value)
        for idx, value in enumerate(sq)
    ]
    return {
        "A": s_list,
        "B": s_zero,
        "C": sq,
        "D": sq_zero,
    }


def modular_metrics_from_combined(
    combined: Sequence[int],
    target_modulus: int | None = None,
) -> Dict[str, object]:
    nonzero = [
        {"shift": shift, "value": int(value)}
        for shift, value in enumerate(combined, start=1)
        if int(value) != 0
    ]
    modulus = two_adic_modulus(combined)
    exact_certificate = not nonzero
    quality_rank = 100 if exact_certificate else int(math.log2(modulus)) if modulus else 0
    return {
        "combined_aperiodic_pm1_autocorrelation": [int(value) for value in combined],
        "nonzero_defects": nonzero,
        "defect_count": len(nonzero),
        "max_defect_magnitude": max_abs(combined),
        "l1_defect": sum(abs(int(value)) for value in combined),
        "two_adic_modulus": modulus,
        "exact_certificate": exact_certificate,
        "target_modulus": target_modulus,
        "target_modulus_met": bool(target_modulus) and modulus >= int(target_modulus),
        "quality_rank": quality_rank,
    }


def structured_qs_state(
    q: Sequence[int],
    s: Sequence[int],
    target_modulus: int | None = None,
    combined_override: Sequence[int] | None = None,
) -> Dict[str, object]:
    sequences = structured_sequences(q, s)
    combined = (
        [int(value) for value in combined_override]
        if combined_override is not None
        else combined_aperiodic_pm1_autocorrelation(
            [
                sequences["A"],
                sequences["B"],
                sequences["C"],
                sequences["D"],
            ]
        )
    )
    state = modular_metrics_from_combined(combined, target_modulus=target_modulus)
    state.update(
        {
            "length": len(q),
            "q": [int(value) for value in q],
            "s": [int(value) for value in s],
            "sequences": sequences,
            "canonical_orbit": signed_reversal_canonical_tuple([q, s]),
        }
    )
    return state


def modular_objective_value(state: Mapping[str, object]) -> int:
    quality_rank = int(state["quality_rank"])
    defect_count = int(state["defect_count"])
    l1_defect = int(state["l1_defect"])
    max_defect = int(state["max_defect_magnitude"])
    return -(quality_rank * 1_000_000) + (l1_defect * 100) + (defect_count * 10) + max_defect


def modular_objective(state: Mapping[str, object]) -> tuple[int, int, int, int]:
    return (
        -int(state["quality_rank"]),
        int(state["l1_defect"]),
        int(state["defect_count"]),
        int(state["max_defect_magnitude"]),
    )
