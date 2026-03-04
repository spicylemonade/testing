# 003: Information Entropy of Collatz Trajectories

## Overview

Every Collatz trajectory generates a binary parity sequence: 1 for odd steps, 0 for even steps. The Shannon entropy of this sequence measures how "random" the trajectory appears. High-delay numbers produce parity sequences with entropy approaching the theoretical maximum, suggesting a deep connection between information theory and number-theoretic dynamics.

## Key Insight

The completeness C(n) = O(n)/E(n) determines the Shannon entropy of the parity sequence:
- H = -p*log2(p) - (1-p)*log2(1-p) where p = C/(1+C)
- For C = 0.6054 (current completeness record): H ~ 0.971 bits
- For C = ln(2)/ln(3) ~ 0.6309 (theoretical maximum): H ~ 0.979 bits

High-delay numbers live in a narrow entropy band near the maximum. This provides a principled way to filter candidates.

## Connection to Kolmogorov Complexity

The parity sequence of a high-delay number should have high Kolmogorov complexity (be incompressible). This connects to:
- Algorithmic randomness (Martin-Lof)
- Lempel-Ziv compressibility
- The Busy Beaver function (which encodes maximum Kolmogorov complexity for given program length)

## Implementation Backlog

1. [ ] Compute parity sequences for delay records #1-#147
2. [ ] Calculate Shannon entropy, Lempel-Ziv complexity, and autocorrelation for each
3. [ ] Build entropy-based filter for the Collatz sieve
4. [ ] Test: do high-entropy sieve survivors correlate with high delay?
5. [ ] Implement early-abort based on running entropy during trajectory computation
6. [ ] Compare entropy distribution of delay records vs random numbers of same magnitude
