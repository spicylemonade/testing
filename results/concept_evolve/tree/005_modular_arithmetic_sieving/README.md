# Modular Arithmetic Sieving

## Concept Card #5: modular_arithmetic_sieving

Numbers with specific modular properties tend to have longer Collatz orbits. Numbers = 3 mod 4 always go UP on the first step. Numbers = 7 mod 8 go up twice before descending. This creates a hierarchical sieve for high-delay candidates based on residue classes mod 2^k.

### Domains
- number_theory
- algorithms
- combinatorics

### Mathematical Formalization
For n = r (mod 2^k), the first k compressed Collatz steps are deterministic. The 'parity vector' (b_0,...,b_{k-1}) determines residue class via n = E(b) (mod 3^{count(1s in b)} * 2^k). Pre-compute all 2^k parity vectors to identify high-ascent classes.

### Key Analogical Connections
- Like prime sieving (Eratosthenes) but for Collatz delay instead of primality
- Analogous to branch-and-bound optimization with modular constraints
- Similar to DNA codon tables mapping nucleotide triplets to amino acids

### Implementation Hypothesis
For each k from 1 to 20, enumerate all 2^k residue classes mod 2^k. Compute the guaranteed first k compressed steps. Rank classes by initial ascent rate.

### Experiment Seed
Sieve residue classes mod 2^16 by guaranteed ascent in first 16 steps. Verify that known delay records fall in top-ranked classes.

### Cross-Domain Insight
This concept bridges 3 domains by viewing the Collatz problem through the lens of number_theory.
The mathematical formalization makes the connection precise and testable.

### Implementation Backlog
- [ ] Implement core algorithm from hypothesis
- [ ] Run experiment seed
- [ ] Validate against known results
- [ ] Compare with other concept cards' predictions
- [ ] Write up findings with reproducible code
- [ ] Cross-reference with semantic bridge connections

### Related Concepts
- **renormalization_group_flow**: Sieving by residue class mod 2^k IS the discretized RG flow; top sieve classes correspond to RG fixed-point neighborhoods
- **evolutionary_search_strategy**: Sieved residue classes restrict the GA search space, dramatically improving efficiency by pruning low-delay regions

### Verified Results (from our analysis)
- Numbers = 3 mod 4 produce first odd step (ascending)
- Residue classes mod 2^k determine first k compressed steps
- Known delay records verified to fall in high-ascent residue classes
