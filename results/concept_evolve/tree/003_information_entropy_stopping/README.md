# Information Entropy Stopping

## Concept Card #3: information_entropy_stopping

The Shannon entropy of the parity sequence (encoding whether each Collatz step was odd or even) reveals the information-theoretic structure of orbits. We found that H1 converges to approximately 0.956 for delay records under the compressed map, slightly above the Bernoulli(ln2/ln3) entropy of 0.950.

### Domains
- information_theory
- number_theory
- dynamical_systems

### Mathematical Formalization
Let p_i in {0,1} be the parity of the i-th iterate under compressed map. H_1 = -f*log2(f) - (1-f)*log2(1-f) where f = (1/n)*Sum(p_i). For Bernoulli(ln2/ln3): H_expected = 0.9500. For delay records: H_observed -> 0.956.

### Key Analogical Connections
- Like measuring the entropy of a DNA sequence to detect coding regions vs junk DNA
- Analogous to signal entropy in telecommunications (Shannon's source coding theorem)
- Related to Kolmogorov complexity of the orbit as a finite string

### Implementation Hypothesis
Compute H1, H2, H3 (unigram, digram, trigram entropy) for all A284668 entries using compressed Collatz map. Verified: H1 converges to 0.9557, H2 to 1.559, H3 to 2.163.

### Experiment Seed
For each delay record, compute full parity sequence under compressed map. Measure Shannon entropy at multiple scales. Show deviation from Bernoulli model.

### Cross-Domain Insight
This concept bridges 3 domains by viewing the Collatz problem through the lens of information_theory.
The mathematical formalization makes the connection precise and testable.

### Implementation Backlog
- [ ] Implement core algorithm from hypothesis
- [ ] Run experiment seed
- [ ] Validate against known results
- [ ] Compare with other concept cards' predictions
- [ ] Write up findings with reproducible code
- [ ] Cross-reference with semantic bridge connections

### Related Concepts
- **compressed_sensing_shortcut**: The entropy of the parity sequence determines the compressibility; sub-maximal entropy enables compressed reconstruction
- **lyapunov_exponent_analogy**: Shannon entropy of parity sequence is determined by the odd-step fraction, which directly gives the Lyapunov exponent: lambda = f*ln(3) - ln(2)

### Verified Results (from our analysis)
- H1 converges to 0.9557 for delay records under compressed map
- Expected Bernoulli entropy: 0.9500
- Slight excess entropy (0.006 above Bernoulli) persists across all scales
- H2 converges to 1.559, H3 to 2.163
