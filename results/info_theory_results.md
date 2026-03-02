# Information-Theoretic Analysis: Mutual Information in Collatz Trajectories

## Parameters
- N = 50000, max_step = 150, k = [4, 6, 8]

## Key Findings

### Mutual Information Decay

- **k=4**: Initial MI = 0.8567 bits, tail MI = 0.0015 ± 0.0011, excess over null = -0.0016, significant = False
- **k=6**: Initial MI = 0.9172 bits, tail MI = 0.0040 ± 0.0020, excess over null = 0.0009, significant = False
- **k=8**: Initial MI = 0.9172 bits, tail MI = 0.0132 ± 0.0047, excess over null = 0.0101, significant = False

### Interpretation

Mutual information decays to the null model level, consistent with the
stochastic independence assumption. However, the RATE of decay and its
dependence on k is itself informative about the mixing properties of
the Collatz map.
