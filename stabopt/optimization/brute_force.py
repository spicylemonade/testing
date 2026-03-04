"""Brute-force enumeration baseline for combinatorial mutation search.

Enumerates all C(N,k) combinations of mutations and scores each under
the energy model.
"""

from __future__ import annotations

import time
from itertools import combinations
from typing import List, Dict, Any
from math import comb

import pandas as pd


def brute_force_search(
    energy_model: "EnergyModel",
    candidates: pd.DataFrame,
    k: int,
    max_combinations: int = 10_000_000,
) -> List[Dict[str, Any]]:
    """Enumerate all k-combinations and return ranked results.

    Args:
        energy_model: EnergyModel instance for scoring
        candidates: DataFrame of candidate single mutations
        k: Number of simultaneous mutations
        max_combinations: Safety limit on total combinations

    Returns:
        List of result dicts sorted by score (best first),
        each with keys: mutations, predicted_ddG, confidence, indices
    """
    N = energy_model.n_candidates
    n_combos = comb(N, k)

    print(f"Brute-force: C({N},{k}) = {n_combos:,} combinations")

    if n_combos > max_combinations:
        estimated_time = n_combos * 0.0001  # ~0.1ms per scoring
        print(
            f"WARNING: {n_combos:,} combinations exceeds limit of {max_combinations:,}. "
            f"Estimated time: {estimated_time:.0f} seconds ({estimated_time / 60:.1f} minutes). "
            f"This exceeds the 15-minute budget — use beam search or evolutionary optimizer instead."
        )
        # Still proceed but cap at max_combinations
        if n_combos > max_combinations * 10:
            raise ValueError(
                f"Too many combinations ({n_combos:,}). "
                f"Use --optimizer beam or --optimizer evolutionary for k={k}, N={N}."
            )

    start = time.time()
    results = []

    for combo in combinations(range(N), k):
        indices = list(combo)
        # Check no two mutations at the same position
        positions = [candidates.iloc[i]["position"] for i in indices]
        if len(set(positions)) != len(positions):
            continue

        score = energy_model.score(indices)
        mutations_str = energy_model.format_mutations(indices)
        results.append({
            "mutations": mutations_str,
            "predicted_ddG": score,
            "confidence": 1.0,  # Exact enumeration
            "indices": indices,
        })

    elapsed = time.time() - start

    # Sort by score (most positive = most stabilizing in our convention)
    results.sort(key=lambda x: x["predicted_ddG"], reverse=True)

    print(
        f"Brute-force complete: {len(results):,} valid combinations "
        f"in {elapsed:.2f} seconds"
    )
    if results:
        print(f"Best: {results[0]['mutations']} = {results[0]['predicted_ddG']:.4f}")

    return results


def estimate_brute_force_time(N: int, k: int) -> Dict[str, Any]:
    """Estimate brute-force computation time without running it.

    Returns dict with: n_combinations, estimated_seconds, feasible
    """
    n_combos = comb(N, k)
    est_seconds = n_combos * 0.0001  # Conservative estimate
    feasible = est_seconds < 900  # 15-minute budget

    return {
        "N": N,
        "k": k,
        "n_combinations": n_combos,
        "estimated_seconds": est_seconds,
        "estimated_minutes": est_seconds / 60,
        "feasible_15min": feasible,
    }
