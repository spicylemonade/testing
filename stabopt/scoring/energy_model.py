"""Additive-plus-pairwise energy model for multi-mutant scoring.

Implements: ddG(S) = sum_i(ddG_i) + sum_{i<j}(epsilon_{ij})
where ddG_i are single-mutation effects and epsilon_{ij} are pairwise epistasis.

Reference: Faure et al. (2024) "The genetic architecture of protein stability"
"""

from __future__ import annotations

from typing import List, Tuple, Optional, Dict, Any
import numpy as np
import pandas as pd


class EnergyModel:
    """Energy model combining single-mutation and pairwise epistasis terms.

    Supports three modes:
    - additive_only: ddG(S) = sum_i(ddG_i)
    - additive_pairwise: ddG(S) = sum_i(ddG_i) + sum_{i<j}(epsilon_{ij})
    - full_pairwise: Same as additive_pairwise but no distance filtering
    """

    def __init__(
        self,
        single_scores: pd.DataFrame,
        epistasis_matrix: Optional[np.ndarray] = None,
        mode: str = "additive_pairwise",
    ):
        """Initialize energy model.

        Args:
            single_scores: DataFrame with [position, wildtype, mutant, score]
            epistasis_matrix: K x K symmetric epistasis matrix (or None for additive-only)
            mode: One of 'additive_only', 'additive_pairwise', 'full_pairwise'
        """
        self.single_scores = single_scores.reset_index(drop=True)
        self.epistasis_matrix = epistasis_matrix
        self.mode = mode

        # Build lookup from (position, mutant) -> (index, score)
        self._score_lookup: Dict[Tuple[int, str], Tuple[int, float]] = {}
        for idx, row in self.single_scores.iterrows():
            key = (int(row["position"]), str(row["mutant"]))
            self._score_lookup[key] = (int(idx), float(row["score"]))

    def score(self, mutation_indices: List[int]) -> float:
        """Score a set of mutations by their indices in the candidates DataFrame.

        Args:
            mutation_indices: List of indices into self.single_scores

        Returns:
            Predicted ddG (more negative = more stabilizing)
        """
        # Additive term
        additive = sum(
            self.single_scores.iloc[i]["score"] for i in mutation_indices
        )

        # Pairwise epistasis term
        pairwise = 0.0
        if self.mode != "additive_only" and self.epistasis_matrix is not None:
            for a in range(len(mutation_indices)):
                for b in range(a + 1, len(mutation_indices)):
                    i = mutation_indices[a]
                    j = mutation_indices[b]
                    pairwise += self.epistasis_matrix[i, j]

        return additive + pairwise

    def score_by_mutations(
        self, mutations: List[Tuple[int, str]]
    ) -> float:
        """Score by (position, mutant_aa) tuples.

        Args:
            mutations: List of (position, mutant_aa) tuples

        Returns:
            Predicted ddG
        """
        indices = []
        for pos, mut in mutations:
            if (pos, mut) in self._score_lookup:
                idx, _ = self._score_lookup[(pos, mut)]
                indices.append(idx)
            else:
                return float("inf")  # Unknown mutation
        return self.score(indices)

    def marginal_gain(
        self, current_indices: List[int], new_index: int
    ) -> float:
        """Compute marginal gain of adding a mutation to the current set.

        Args:
            current_indices: Indices of currently selected mutations
            new_index: Index of mutation to potentially add

        Returns:
            Marginal improvement in score
        """
        # Additive component of marginal gain
        gain = self.single_scores.iloc[new_index]["score"]

        # Pairwise component: interaction with all currently selected mutations
        if self.mode != "additive_only" and self.epistasis_matrix is not None:
            for idx in current_indices:
                gain += self.epistasis_matrix[idx, new_index]

        return gain

    @property
    def n_candidates(self) -> int:
        return len(self.single_scores)

    def get_candidate_positions(self) -> np.ndarray:
        return self.single_scores["position"].values

    def format_mutations(self, indices: List[int]) -> str:
        """Format mutation indices as human-readable string."""
        parts = []
        for idx in sorted(indices):
            row = self.single_scores.iloc[idx]
            parts.append(f"{row['wildtype']}{row['position']}{row['mutant']}")
        return "+".join(parts)
