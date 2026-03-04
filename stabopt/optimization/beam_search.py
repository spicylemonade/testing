"""Beam search combinatorial optimizer with epistasis-aware scoring.

Maintains top-B partial solutions at each depth, expanding by adding
candidate mutations and pruning using the energy model.
"""

from __future__ import annotations

import time
from typing import List, Dict, Any, Tuple

import pandas as pd
import numpy as np


def beam_search(
    energy_model: "EnergyModel",
    candidates: pd.DataFrame,
    k: int,
    beam_width: int = 100,
    top_results: int = 50,
) -> List[Dict[str, Any]]:
    """Beam search over mutation combinations.

    At each depth d (1..k), maintain the top beam_width partial solutions.
    Expand each by adding each remaining candidate mutation, score the
    expanded set, and keep the top beam_width.

    Args:
        energy_model: EnergyModel instance for scoring
        candidates: DataFrame of candidate single mutations
        k: Target number of simultaneous mutations
        beam_width: Number of partial solutions to maintain at each depth
        top_results: Number of top complete solutions to return

    Returns:
        List of result dicts sorted by score, each with:
        mutations, predicted_ddG, confidence, indices
    """
    start = time.time()
    N = energy_model.n_candidates

    # Initialize beam with empty set
    # Each beam entry: (score, indices, positions_set)
    beam: List[Tuple[float, List[int], set]] = [(0.0, [], set())]

    for depth in range(k):
        new_beam: List[Tuple[float, List[int], set]] = []

        for score, indices, positions in beam:
            for idx in range(N):
                if idx in indices:
                    continue
                pos = int(candidates.iloc[idx]["position"])
                if pos in positions:
                    continue

                new_indices = indices + [idx]
                new_positions = positions | {pos}
                new_score = energy_model.score(new_indices)
                new_beam.append((new_score, new_indices, new_positions))

        # Prune to beam_width
        new_beam.sort(key=lambda x: x[0], reverse=True)
        beam = new_beam[:beam_width]

        elapsed = time.time() - start
        if beam:
            print(
                f"  Beam depth {depth + 1}/{k}: "
                f"{len(new_beam)} candidates -> {len(beam)} kept "
                f"(best={beam[0][0]:.4f}, t={elapsed:.2f}s)"
            )

    elapsed = time.time() - start

    # Convert to result dicts
    results = []
    for score, indices, _ in beam[:top_results]:
        mutations_str = energy_model.format_mutations(indices)
        results.append({
            "mutations": mutations_str,
            "predicted_ddG": score,
            "confidence": _compute_confidence(score, beam),
            "indices": indices,
        })

    print(
        f"Beam search complete: {len(results)} solutions in {elapsed:.2f}s"
    )
    if results:
        print(f"Best: {results[0]['mutations']} = {results[0]['predicted_ddG']:.4f}")

    return results


def _compute_confidence(score: float, beam: list) -> float:
    """Compute a confidence score based on position in beam.

    Higher confidence if the score is well-separated from alternatives.
    """
    if not beam:
        return 0.0
    scores = [s for s, _, _ in beam]
    best = max(scores)
    worst = min(scores)
    if best == worst:
        return 1.0
    # Normalize to [0, 1] based on position in range
    return max(0.0, min(1.0, (score - worst) / (best - worst)))
