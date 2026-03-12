from __future__ import annotations

from typing import Any


BLOCKER_TAXONOMY = {
    "rational_triviality": "A positive hit is explained entirely by the rational arithmetic-progression baseline.",
    "word_value_confusion": "The evidence comes from symbolic recurrence or word structure rather than the integer value sequence.",
    "set_sequence_confusion": "The argument proves unordered Beatty-set membership facts instead of ordered subsequence facts.",
    "post_selection_leakage": "A sparse or highly tuned selector yields a recurrence-looking prefix without a structural infinite certificate.",
}


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
    return {
        "exact_hit_rate": exact_hits / len(runs) if runs else 0.0,
        "false_positive_rate": false_positives / len(adversarial_controls) if adversarial_controls else 0.0,
        "modulus_consistency_score": sum(modulus_scores) / len(modulus_scores) if modulus_scores else 0.0,
    }
