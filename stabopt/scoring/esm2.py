"""ESM-2 based single-mutation scoring using masked marginal log-likelihood ratios.

Reference: Meier et al. (2021) "Language models enable zero-shot prediction"
           Lin et al. (2023) "Evolutionary-scale prediction"
"""

from __future__ import annotations

from typing import Optional
import pandas as pd
import numpy as np


# Canonical amino acids
AMINO_ACIDS = list("ACDEFGHIKLMNPQRSTVWY")


def score_single_mutations(
    sequence: str,
    device: str = "cuda",
    model_name: str = "facebook/esm2_t33_650M_UR50D",
    batch_size: int = 8,
) -> pd.DataFrame:
    """Compute log-likelihood ratio scores for all single mutations.

    Uses the masked marginal approach: for each position i, mask the residue,
    compute log p(mutant_aa | context) - log p(wildtype_aa | context).

    Args:
        sequence: Wild-type amino acid sequence (1-letter codes)
        device: PyTorch device
        model_name: HuggingFace ESM-2 model name
        batch_size: Number of positions to process in parallel

    Returns:
        DataFrame with columns [position, wildtype, mutant, score]
        where score = log p(mut) - log p(wt), positive = stabilizing
    """
    import torch
    from transformers import AutoTokenizer, EsmForMaskedLM

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = EsmForMaskedLM.from_pretrained(model_name).to(device)
    model.eval()

    n = len(sequence)
    results = []

    # Process positions in batches
    for batch_start in range(0, n, batch_size):
        batch_end = min(batch_start + batch_size, n)
        batch_positions = list(range(batch_start, batch_end))

        # Create masked sequences for this batch
        masked_seqs = []
        for pos in batch_positions:
            masked_seq = list(sequence)
            masked_seq[pos] = tokenizer.mask_token
            masked_seqs.append("".join(masked_seq))

        # Tokenize batch — ESM-2 expects space-separated single characters
        spaced_seqs = [" ".join(s) for s in masked_seqs]
        inputs = tokenizer(
            spaced_seqs,
            return_tensors="pt",
            padding=True,
            truncation=True,
        ).to(device)

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits  # (batch, seq_len, vocab_size)

        # Extract log-probabilities at masked positions
        log_probs = torch.log_softmax(logits, dim=-1)

        for i, pos in enumerate(batch_positions):
            wt_aa = sequence[pos]
            # The masked position in the tokenized sequence is offset by 1
            # (BOS token), so token_pos = pos + 1
            token_pos = pos + 1

            wt_token_id = tokenizer.convert_tokens_to_ids(wt_aa)
            wt_log_prob = log_probs[i, token_pos, wt_token_id].item()

            for mut_aa in AMINO_ACIDS:
                if mut_aa == wt_aa:
                    continue
                mut_token_id = tokenizer.convert_tokens_to_ids(mut_aa)
                mut_log_prob = log_probs[i, token_pos, mut_token_id].item()

                # Log-likelihood ratio: positive means mutant is more likely
                score = mut_log_prob - wt_log_prob
                results.append({
                    "position": pos,
                    "wildtype": wt_aa,
                    "mutant": mut_aa,
                    "score": score,
                })

    # Clean up GPU memory
    del model
    if device.startswith("cuda"):
        torch.cuda.empty_cache()

    df = pd.DataFrame(results)
    return df
