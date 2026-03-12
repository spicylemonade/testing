from __future__ import annotations

from typing import Any

import sympy as sp


BLOCKER_TAXONOMY = {
    "rational_triviality": "A positive hit is explained entirely by the rational arithmetic-progression baseline.",
    "word_value_confusion": "The evidence comes from symbolic recurrence or word structure rather than the integer value sequence.",
    "set_sequence_confusion": "The argument proves unordered Beatty-set membership facts instead of ordered subsequence facts.",
    "post_selection_leakage": "A sparse or highly tuned selector yields a recurrence-looking prefix without a structural infinite certificate.",
}


def recurrence_coefficients(result: dict[str, Any]) -> list[int] | None:
    certificate = result.get("certificate") or {}
    if certificate.get("certified_coefficients") is not None:
        return [int(value) for value in certificate["certified_coefficients"]]
    shadow = result.get("shadow_probe") or {}
    candidate = shadow.get("candidate_from_prefix") or result.get("candidate_recurrence") or {}
    if candidate.get("coefficients") is not None:
        return [int(value) for value in candidate["coefficients"]]
    return None


def nondegenerate_status(result: dict[str, Any]) -> bool | None:
    coefficients = recurrence_coefficients(result)
    if not coefficients or len(coefficients) <= 2:
        return None
    x = sp.Symbol("x")
    poly = sp.Poly(sum(coefficients[idx] * x**idx for idx in range(len(coefficients))), x)
    degree = int(poly.degree())
    if degree <= 0:
        return None
    roots = [complex(root.evalf(50)) for root in poly.nroots(n=degree, maxsteps=200)]
    for idx, left in enumerate(roots):
        if abs(left) == 0:
            return False
        for jdx in range(idx + 1, len(roots)):
            ratio = left / roots[jdx]
            for power in range(1, 25):
                if abs(ratio**power - 1.0) < 1e-8:
                    return False
    return True


def risk_tags(result: dict[str, Any]) -> list[str]:
    tags = blocker_tags(result)
    shadow = result.get("shadow_probe") or {}
    verification = shadow.get("full_length_verification") or {}
    if verification.get("holds") and result.get("certificate") is None:
        tags.append("uncertified_exact_holdout")
    classification = shadow.get("classification")
    if classification == "selector_shadow_failure":
        tags.append("modular_shadow_failure")
    if classification == "no_candidate":
        tags.append("order_cap_or_true_negative")
    if result.get("certificate") is not None:
        tags.append("exact_certificate")
    deduped: list[str] = []
    for tag in tags:
        if tag not in deduped:
            deduped.append(tag)
    return deduped


def selector_complexity(result: dict[str, Any]) -> int:
    selector_id = result["selector_id"]
    if selector_id.startswith("ap_"):
        return 2
    if selector_id.startswith("union_"):
        return 4
    if selector_id in {"fib_indices", "pell_indices", "padovan_indices"}:
        return 3
    return 5


def modulus_consistency_score(result: dict[str, Any]) -> float:
    shadow = result.get("shadow_probe") or {}
    profiles = shadow.get("residue_profiles") or {}
    if not profiles:
        return 0.0
    holds = [1.0 if entry.get("relation_holds") else 0.0 for entry in profiles.values()]
    return sum(holds) / len(holds)


def blocker_tags(result: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    if str(result.get("slope_id", "")).startswith("rational_") or result.get("slope_id") == "half":
        tags.append("rational_triviality")
    if result.get("selector_family") == "linear_recursive" and result.get("certificate") is None:
        tags.append("post_selection_leakage")
    if result.get("selector_family") == "finite_union_of_arithmetic_progressions" and result.get("certificate") is None:
        tags.append("set_sequence_confusion")
    return tags


def summarize_runs(runs: list[dict[str, Any]]) -> dict[str, Any]:
    exact_hits = sum(1 for run in runs if run.get("shadow_probe", {}).get("classification") == "exact_recurrence")
    adversarial_controls = [run for run in runs if run.get("case_role") == "adversarial_control"]
    false_positives = sum(
        1
        for run in adversarial_controls
        if run.get("shadow_probe", {}).get("classification") == "exact_recurrence"
    )
    modulus_scores = [modulus_consistency_score(run) for run in runs]
    exact_runs = [run for run in runs if run.get("shadow_probe", {}).get("classification") == "exact_recurrence"]
    nondegenerate_split = {
        "true": sum(1 for run in exact_runs if nondegenerate_status(run) is True),
        "false": sum(1 for run in exact_runs if nondegenerate_status(run) is False),
        "unknown": sum(1 for run in exact_runs if nondegenerate_status(run) is None),
    }
    return {
        "exact_hit_rate": exact_hits / len(runs) if runs else 0.0,
        "false_positive_rate": false_positives / len(adversarial_controls) if adversarial_controls else 0.0,
        "modulus_consistency_score": sum(modulus_scores) / len(modulus_scores) if modulus_scores else 0.0,
        "exact_hit_count": exact_hits,
        "nondegenerate_exact_split": nondegenerate_split,
    }
