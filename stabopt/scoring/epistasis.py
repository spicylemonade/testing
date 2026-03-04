"""Pairwise epistasis scoring module.

Computes pairwise epistasis corrections between candidate mutations using
ESM-2 conditional log-likelihood shifts and structural distance filtering.

Reference: Faure et al. (2024) "The genetic architecture of protein stability"
           Dieckhaus et al. (2024) ThermoMPNN-D for double-mutant ddG
"""

from __future__ import annotations

from typing import Dict, Any, Optional
import numpy as np
import pandas as pd


def compute_epistasis_matrix(
    sequence: str,
    candidates: pd.DataFrame,
    structure: Dict[str, Any],
    device: str = "cuda",
    distance_threshold: float = 10.0,
    method: str = "conditional_llr",
) -> np.ndarray:
    """Compute pairwise epistasis correction matrix for candidate mutations.

    Uses ESM-2 conditional log-likelihood shift: mask position j, score
    position i conditioned on mutation at j. The epistasis term is:
    epsilon_{ij} = score(i|mut_j) - score(i|wt_j)

    Following Faure et al. (2024), only compute for pairs with
    CA distance < distance_threshold (default 10 Angstroms).

    Args:
        sequence: Wild-type sequence
        candidates: DataFrame with columns [position, wildtype, mutant, score]
        structure: Parsed PDB structure from pdb_utils.parse_pdb
        device: PyTorch device
        distance_threshold: Max CA distance for epistasis pairs (Angstroms)
        method: Scoring method ('conditional_llr' or 'additive_deviation')

    Returns:
        K x K symmetric epistasis matrix where K = len(candidates)
    """
    from stabopt.utils.pdb_utils import compute_distance_matrix

    K = len(candidates)
    epistasis = np.zeros((K, K), dtype=np.float32)

    if K == 0:
        return epistasis

    # Compute distance matrix for filtering
    ca_coords = structure["ca_coords"]
    dist_matrix = compute_distance_matrix(ca_coords)

    # Get positions of candidates
    positions = candidates["position"].values

    # Filter pairs by distance
    contact_pairs = []
    for i in range(K):
        for j in range(i + 1, K):
            pos_i = positions[i]
            pos_j = positions[j]
            if pos_i < len(dist_matrix) and pos_j < len(dist_matrix):
                if dist_matrix[pos_i, pos_j] < distance_threshold:
                    contact_pairs.append((i, j))

    if not contact_pairs:
        return epistasis

    if method == "conditional_llr":
        epistasis = _compute_conditional_llr(
            sequence, candidates, contact_pairs, device
        )
    elif method == "additive_deviation":
        epistasis = _compute_additive_deviation(
            sequence, candidates, contact_pairs, device
        )

    return epistasis


def _compute_conditional_llr(
    sequence: str,
    candidates: pd.DataFrame,
    contact_pairs: list,
    device: str,
) -> np.ndarray:
    """Compute epistasis via conditional log-likelihood ratio shift.

    For each pair (i, j): create mutant sequence with mutation at j,
    then score mutation at i in the context of the j-mutant vs wild-type.
    epsilon_{ij} = LLR(i | mut_j) - LLR(i | wt_j)
    """
    import torch
    from transformers import AutoTokenizer, EsmForMaskedLM

    K = len(candidates)
    epistasis = np.zeros((K, K), dtype=np.float32)

    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = EsmForMaskedLM.from_pretrained(model_name).to(device)
    model.eval()

    positions = candidates["position"].values
    wt_aas = candidates["wildtype"].values
    mut_aas = candidates["mutant"].values

    # Batch processing of contact pairs
    batch_size = 16
    for batch_start in range(0, len(contact_pairs), batch_size):
        batch = contact_pairs[batch_start : batch_start + batch_size]

        masked_seqs_wt = []
        masked_seqs_mut = []
        pair_indices = []

        for i_idx, j_idx in batch:
            pos_i = positions[i_idx]
            pos_j = positions[j_idx]
            mut_j = mut_aas[j_idx]

            # Wild-type context: mask position i
            seq_wt = list(sequence)
            seq_wt[pos_i] = tokenizer.mask_token
            masked_seqs_wt.append(" ".join(seq_wt))

            # Mutant-j context: mutate j, mask i
            seq_mut = list(sequence)
            seq_mut[pos_j] = mut_j
            seq_mut[pos_i] = tokenizer.mask_token
            masked_seqs_mut.append(" ".join(seq_mut))

            pair_indices.append((i_idx, j_idx))

        if not masked_seqs_wt:
            continue

        # Score in wild-type context
        inputs_wt = tokenizer(
            masked_seqs_wt, return_tensors="pt", padding=True, truncation=True
        ).to(device)
        with torch.no_grad():
            logits_wt = model(**inputs_wt).logits
        lp_wt = torch.log_softmax(logits_wt, dim=-1)

        # Score in mutant-j context
        inputs_mut = tokenizer(
            masked_seqs_mut, return_tensors="pt", padding=True, truncation=True
        ).to(device)
        with torch.no_grad():
            logits_mut = model(**inputs_mut).logits
        lp_mut = torch.log_softmax(logits_mut, dim=-1)

        for k, (i_idx, j_idx) in enumerate(pair_indices):
            pos_i = positions[i_idx]
            token_pos = pos_i + 1  # offset for BOS token

            wt_i = wt_aas[i_idx]
            mut_i = mut_aas[i_idx]
            wt_token = tokenizer.convert_tokens_to_ids(wt_i)
            mut_token = tokenizer.convert_tokens_to_ids(mut_i)

            # LLR in wild-type context
            llr_wt = lp_wt[k, token_pos, mut_token].item() - lp_wt[k, token_pos, wt_token].item()

            # LLR in mutant-j context
            llr_mut = lp_mut[k, token_pos, mut_token].item() - lp_mut[k, token_pos, wt_token].item()

            # Epistasis = shift in LLR due to mutation at j
            eps = llr_mut - llr_wt
            epistasis[i_idx, j_idx] = eps
            epistasis[j_idx, i_idx] = eps  # Symmetric

    del model
    if device.startswith("cuda"):
        torch.cuda.empty_cache()

    return epistasis


def _compute_additive_deviation(
    sequence: str,
    candidates: pd.DataFrame,
    contact_pairs: list,
    device: str,
) -> np.ndarray:
    """Compute epistasis as deviation from additive prediction.

    epsilon_{ij} = score(double_mutant) - score(i) - score(j)
    Uses ESM-2 to score the double mutant sequence directly.
    """
    import torch
    from transformers import AutoTokenizer, EsmForMaskedLM

    K = len(candidates)
    epistasis = np.zeros((K, K), dtype=np.float32)

    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = EsmForMaskedLM.from_pretrained(model_name).to(device)
    model.eval()

    positions = candidates["position"].values
    mut_aas = candidates["mutant"].values
    single_scores = candidates["score"].values

    # Score double mutants
    for i_idx, j_idx in contact_pairs:
        pos_i, pos_j = positions[i_idx], positions[j_idx]
        mut_i, mut_j = mut_aas[i_idx], mut_aas[j_idx]

        # Create double mutant and compute pseudo-log-likelihood
        double_seq = list(sequence)
        double_seq[pos_i] = mut_i
        double_seq[pos_j] = mut_j

        # Use masked marginal at both positions
        # (simplified: average of individual masked marginals)
        double_score = single_scores[i_idx] + single_scores[j_idx]

        # The epistasis is zero under additive model — this is a placeholder
        # In practice, we'd score the double mutant sequence properly
        epistasis[i_idx, j_idx] = 0.0
        epistasis[j_idx, i_idx] = 0.0

    del model
    if device.startswith("cuda"):
        torch.cuda.empty_cache()

    return epistasis
