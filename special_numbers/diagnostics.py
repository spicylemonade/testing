from __future__ import annotations

from typing import Any

from special_numbers.recurrence import find_exact_relation


DEFAULT_MODULI = [2, 3, 5, 7, 11]
DEFAULT_PRIME_SQUARE = 25


def density_class(selector_family: str) -> str:
    if selector_family in {"arithmetic_progression", "finite_union_of_arithmetic_progressions"}:
        return "positive_density"
    return "zero_density"


def verify_relation(sequence: list[int], coeffs: list[int]) -> dict[str, Any]:
    order = len(coeffs) - 1
    for start in range(len(sequence) - order):
        lhs = sum(coeffs[idx] * sequence[start + idx] for idx in range(order + 1))
        if lhs != 0:
            return {
                "holds": False,
                "failure_window": start,
                "failure_residual": lhs,
            }
    return {"holds": True, "failure_window": None, "failure_residual": 0}


def detect_period_tail(values: list[int], max_period: int = 12) -> dict[str, int | None]:
    if len(values) < 8:
        return {"period": None, "tail_start": None}
    for period in range(1, min(max_period, len(values) // 2) + 1):
        tail_start = len(values) - 2 * period
        if tail_start < 0:
            continue
        if values[tail_start : tail_start + period] == values[tail_start + period : tail_start + 2 * period]:
            return {"period": period, "tail_start": tail_start}
    return {"period": None, "tail_start": None}


def residue_profiles(sequence: list[int], coeffs: list[int], moduli: list[int], prime_square: int) -> dict[str, Any]:
    profiles: dict[str, Any] = {}
    for modulus in moduli + [prime_square]:
        residues = [value % modulus for value in sequence]
        relation_check = verify_relation(residues, coeffs)
        profiles[str(modulus)] = {
            "residues": residues,
            "relation_holds": relation_check["holds"],
            "failure_window": relation_check["failure_window"],
            "tail_period_guess": detect_period_tail(residues),
        }
    return profiles


def classify_candidate(
    *,
    has_certificate: bool,
    survives_holdout: bool,
    selector_family: str,
    residue_profiles_map: dict[str, Any],
) -> str:
    if has_certificate:
        return "exact_recurrence"
    if not survives_holdout:
        return "selector_shadow_failure"
    relation_holds_everywhere = all(profile["relation_holds"] for profile in residue_profiles_map.values())
    if not relation_holds_everywhere:
        return "selector_shadow_failure"
    if density_class(selector_family) == "zero_density":
        return "sparse_subsequence_leak"
    return "prefix_fit"


def run_shadow_case(result: dict[str, Any], *, fit_length: int = 12, max_order: int = 4) -> dict[str, Any]:
    values = list(result["values"])
    prefix = values[:fit_length]
    candidate = find_exact_relation(prefix, max_order=max_order)
    if candidate is None:
        return {
            **result,
            "shadow_probe": {
                "fit_length": fit_length,
                "candidate_from_prefix": None,
                "classification": "no_candidate",
            },
        }
    verification = verify_relation(values, candidate["coefficients"])
    profiles = residue_profiles(values, candidate["coefficients"], DEFAULT_MODULI, DEFAULT_PRIME_SQUARE)
    classification = classify_candidate(
        has_certificate=result["certificate"] is not None,
        survives_holdout=verification["holds"],
        selector_family=result["selector_family"],
        residue_profiles_map=profiles,
    )
    return {
        **result,
        "shadow_probe": {
            "fit_length": fit_length,
            "candidate_from_prefix": candidate,
            "full_length_verification": verification,
            "density_class": density_class(result["selector_family"]),
            "residue_profiles": profiles,
            "classification": classification,
        },
    }
