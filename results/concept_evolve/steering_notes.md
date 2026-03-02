# ConceptEvolve Steering Notes

## Three Concrete Steering Directions

### Direction 1: Information-Theoretic Memory Detection (PRIORITY)
**Concept source**: "Parity Sequence as Information Channel" + "Collatz as Lossy Compression"

Compute mutual information I(X_k; Y_t) between k-bit windows of binary(n) and parity sequence at step t. If MI plateaus above zero for large t, this provides **direct computational evidence against the stochastic independence assumption** underlying Kontorovich-Lagarias and Tao's probabilistic models. This would be genuinely newsworthy because it challenges the dominant theoretical framework.

**Informs rubric items**: item_014 (information theory), item_019 (significance testing), item_022 (deep dive)

**Why prioritized first**: This is the most likely to produce a clear, quantifiable, headline-worthy result. Either MI decays to zero (confirming stochastic models) or it doesn't (contradicting them). Both outcomes are publishable. The computation is tractable and the result is instantly verifiable.

### Direction 2: Modular Resonance Discovery
**Concept source**: "Modular Resonance as Phase Locking" + "2-adic Contraction"

Systematically scan stopping_time(n) mod m for m = 2..500 and identify all moduli where the distribution is significantly non-uniform. The known trivial resonances are at powers of 2 and products 2^a * 3^b. **Any resonance at a prime p > 3 coprime to 6 would be a new arithmetic constraint** on Collatz dynamics not predicted by any existing model.

**Informs rubric items**: item_015 (modular resonance), item_019 (significance), item_020 (scale invariance)

**Why second**: This is a systematic scan with clear novelty criteria. The computation is fast and the statistical tests are well-defined. Finding unexpected resonances at primes coprime to 6 would be immediately surprising to number theorists.

### Direction 3: Phase Transition in Generalized Collatz Family
**Concept source**: "Phase Diagram as Critical Phenomenon" + "Carry Propagation as Avalanche"

Map the convergence/divergence boundary in (a,b) parameter space for generalized maps. **If the critical boundary has fractal dimension > 1, this connects Collatz to universality in statistical mechanics** — a deep cross-domain bridge. Power-law divergence of escape times at the boundary would confirm a genuine phase transition.

**Informs rubric items**: item_017 (generalized Collatz), item_019 (significance), item_020 (scale invariance)

**Why third**: Most ambitious and potentially most impactful, but also most computationally intensive and risk of inconclusive results. Best attempted after establishing baseline with Directions 1 and 2.

## Summary
- **Direction 1** (MI memory detection) → highest probability of clean, publishable result
- **Direction 2** (modular resonance scan) → systematic discovery with clear novelty criteria
- **Direction 3** (phase transitions) → highest potential impact but most risk

All three directions target genuine gaps confirmed by the literature review: no prior work on MI analysis, systematic modular scanning, or fractal phase boundary characterization for Collatz.
