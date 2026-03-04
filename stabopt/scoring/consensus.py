"""Consensus re-ranking with ProteinMPNN structural consistency filter.

Re-scores top multi-mutant candidates by computing ProteinMPNN
log-likelihood of the full mutant sequence given the wild-type backbone.
"""

from __future__ import annotations

from typing import List, Dict, Any

import numpy as np


def rerank_candidates(
    results: List[Dict[str, Any]],
    pdb_path: str,
    chain: str,
    sequence: str,
    device: str = "cuda",
    alpha: float = 0.5,
    max_candidates: int = 100,
) -> List[Dict[str, Any]]:
    """Re-rank candidates using ProteinMPNN structural consistency.

    For each candidate:
    1. Construct mutant sequence
    2. Compute ProteinMPNN log-likelihood of mutant sequence given WT backbone
    3. Combine original score with ProteinMPNN score via weighted sum

    Args:
        results: List of result dicts from optimizer
        pdb_path: Path to PDB file
        chain: Chain ID
        sequence: Wild-type sequence
        device: PyTorch device
        alpha: Weight for original score (1-alpha for ProteinMPNN score)
        max_candidates: Maximum candidates to re-rank

    Returns:
        Re-ranked results list
    """
    from stabopt.scoring.proteinmpnn import score_sequence

    candidates = results[:max_candidates]

    # Score wild-type sequence as baseline
    wt_score = score_sequence(sequence, pdb_path, chain, device)

    reranked = []
    for result in candidates:
        mutations_str = result.get("mutations", "")
        original_score = result.get("predicted_ddG", 0.0)

        # Construct mutant sequence
        mutant_seq = _apply_mutations(sequence, mutations_str)

        # Score mutant with ProteinMPNN
        mut_score = score_sequence(mutant_seq, pdb_path, chain, device)
        mpnn_delta = mut_score - wt_score  # Positive = mutant fits structure better

        # Combined score
        combined = alpha * original_score + (1 - alpha) * mpnn_delta

        reranked.append({
            "mutations": mutations_str,
            "predicted_ddG": combined,
            "confidence": result.get("confidence", 0.0),
            "original_score": original_score,
            "mpnn_delta": mpnn_delta,
            "indices": result.get("indices", []),
        })

    # Re-sort by combined score
    reranked.sort(key=lambda x: x["predicted_ddG"], reverse=True)

    return reranked


def _apply_mutations(sequence: str, mutations_str: str) -> str:
    """Apply mutation string to wild-type sequence.

    mutations_str format: "A10G+L20F+..."
    """
    if not mutations_str:
        return sequence

    seq_list = list(sequence)

    for mut in mutations_str.split("+"):
        if len(mut) < 3:
            continue
        wt_aa = mut[0]
        mut_aa = mut[-1]
        pos = int(mut[1:-1])

        if 0 <= pos < len(seq_list):
            seq_list[pos] = mut_aa

    return "".join(seq_list)
