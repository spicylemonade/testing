# Information-Theoretic Sieve

## Concept

Uses Kolmogorov complexity — approximated in practice by compression ratio — to
sieve for Collatz starting numbers with high delay. The hypothesis is that
numbers with intermediate effective complexity (neither trivially structured nor
maximally random) occupy a "Goldilocks zone" that produces long, complex
trajectories. The binary Shannon entropy of the bit pattern serves as a fast
proxy: numbers with H(bits(n)) in the range 0.6-0.8 are predicted to be
enriched for high-delay outliers.

## Cross-Domain Connections

- **Edge of chaos in cellular automata** (complex systems): Langton's lambda
  parameter identifies a critical transition zone between ordered and chaotic
  dynamics where computation is maximized; the intermediate-complexity sieve
  targets an analogous transition in integer structure.
- **Intermediate genome complexity** (genomics): Biological genomes are neither
  fully random nor fully repetitive; the most functionally rich genomes exhibit
  intermediate compressibility, paralleling the hypothesis that intermediate-
  complexity integers produce the richest Collatz dynamics.
- **Critical phenomena** (statistical physics): At phase transitions, systems
  exhibit maximal correlation lengths and fluctuations; the sieve targets a
  structural "critical point" in bit-string space where Collatz dynamics are
  most sensitive and unpredictable.

## Implementation Backlog

1. **Compression-ratio sieve** — For each candidate number, compute the zlib
   compression ratio of its binary representation and bin candidates into
   complexity strata (low / Goldilocks / high).
2. **Shannon entropy calculator** — Compute sliding-window bit entropy over the
   binary representation to characterize local structure; correlate windowed
   entropy profiles with delay.
3. **Stratified sampling experiment** — Sample 100K numbers in the 2^50 to 2^60
   range, stratified by compression ratio, and compare delay distributions
   across strata to test the Goldilocks hypothesis.
4. **Complexity-delay correlation analysis** — Fit regression models (delay ~
   compression_ratio + bit_length + interactions) to quantify the predictive
   power of complexity measures.
5. **Cross-module handoff** — Pass Goldilocks-zone candidates to the genetic
   delay maximizer (concept 002) as seed population and to the energy landscape
   navigator (concept 004) as starting points.

## Key References

- Li, M., & Vitanyi, P. (2019). *An Introduction to Kolmogorov Complexity and
  Its Applications.* 4th ed., Springer.
- Langton, C. G. (1990). *Computation at the edge of chaos: phase transitions
  and emergent computation.* Physica D.
- Crutchfield, J. P. (2012). *The organization of intrinsic computation:
  complexity-entropy diagrams and the diversity of natural information
  processing.* Physics of Life Reviews.
