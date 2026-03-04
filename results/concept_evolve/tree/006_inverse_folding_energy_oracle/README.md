# 006 — Inverse Folding Energy Oracle

## Topic Context

Inverse folding models predict amino acid sequences that fold into a given 3D structure. Their log-likelihoods have recently been shown to have a rigorous free-energy interpretation (Frellsen et al. 2025): the log-probability ratio between mutant and wild-type approximates the change in folding free energy, ddG.

**SPURS** (Li & Luo 2025, RECOMB/Nature Communications) demonstrates that combining a protein language model (ESM-2) with an inverse folding model (ESM-IF/ProteinMPNN) and fine-tuning on Mega-scale data achieves state-of-the-art stability prediction. The key insight is that sequence-based and structure-based models capture complementary information:

- **ESM-2** (sequence): captures evolutionary constraints, coevolution patterns, long-range dependencies
- **ProteinMPNN** (structure): captures local packing, hydrogen bonding geometry, backbone-side chain compatibility

Their combination is more robust than either alone, especially for multi-mutant predictions where structural context matters.

## Key Connections

- **Free energy interpretation**: likelihood ratios ARE approximate free energies, not just heuristic scores
- **Complementarity**: ESM-2 captures "sequence fitness" while ProteinMPNN captures "structural fitness" — their disagreement flags uncertainty

## Implementation Backlog

1. [ ] Implement ESM-2 masked marginal log-likelihood scorer
2. [ ] Implement ProteinMPNN conditional log-probability scorer
3. [ ] Implement linear combination with learnable weights
4. [ ] Add pairwise interaction terms for multi-mutant scoring
5. [ ] Train/calibrate weights on Mega-scale data split
6. [ ] Validate on FireProtDB external test set
7. [ ] Measure scorer agreement/disagreement as uncertainty estimate
8. [ ] Benchmark speed on A100 (target: <5ms per variant)
9. [ ] Add optional RaSP/Pythia as third scorer for ensemble
10. [ ] Implement caching of wild-type embeddings for efficiency
