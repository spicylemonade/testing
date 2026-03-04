"""Naive greedy search baseline for combinatorial mutation optimization.

Iteratively adds the mutation that maximally improves the score,
starting from the best single mutation.
"""

from __future__ import annotations

import time
from typing import List, Dict, Any

import pandas as pd


def greedy_search(
    energy_model: "EnergyModel",
    candidates: pd.DataFrame,
    k: int,
) -> List[Dict[str, Any]]:
    """Iterative greedy mutation addition.

    Start with the best single mutation, then iteratively add the mutation
    that provides the largest marginal gain, until k mutations are selected.

    Args:
        energy_model: EnergyModel instance for scoring
        candidates: DataFrame of candidate single mutations
        k: Number of simultaneous mutations to select

    Returns:
        List of result dicts (single result for greedy), each with:
        mutations, predicted_ddG, confidence, indices
    """
    start = time.time()
    N = energy_model.n_candidates

    selected_indices: List[int] = []
    selected_positions: set = set()
    step_log: List[Dict[str, Any]] = []

    for step in range(k):
        best_gain = float("-inf")
        best_idx = -1

        for idx in range(N):
            if idx in selected_indices:
                continue
            # Check position conflict
            pos = int(candidates.iloc[idx]["position"])
            if pos in selected_positions:
                continue

            gain = energy_model.marginal_gain(selected_indices, idx)
            if gain > best_gain:
                best_gain = gain
                best_idx = idx

        if best_idx < 0:
            break

        selected_indices.append(best_idx)
        selected_positions.add(int(candidates.iloc[best_idx]["position"]))

        current_score = energy_model.score(selected_indices)
        step_time = time.time() - start

        row = candidates.iloc[best_idx]
        step_log.append({
            "step": step + 1,
            "added": f"{row['wildtype']}{row['position']}{row['mutant']}",
            "marginal_gain": best_gain,
            "total_score": current_score,
            "elapsed": step_time,
        })

        print(
            f"  Step {step + 1}/{k}: "
            f"Add {row['wildtype']}{row['position']}{row['mutant']} "
            f"(gain={best_gain:.4f}, total={current_score:.4f}, "
            f"t={step_time:.2f}s)"
        )

    elapsed = time.time() - start
    final_score = energy_model.score(selected_indices) if selected_indices else 0.0
    mutations_str = energy_model.format_mutations(selected_indices)

    print(f"Greedy complete: {mutations_str} = {final_score:.4f} in {elapsed:.2f}s")

    # Return the greedy solution as the top result
    results = [{
        "mutations": mutations_str,
        "predicted_ddG": final_score,
        "confidence": 0.5,  # Lower confidence than exhaustive search
        "indices": selected_indices,
        "step_log": step_log,
    }]

    return results
