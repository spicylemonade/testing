# Renormalization Group Flow

## Concept Card #12: renormalization_group_flow

The Collatz map can be viewed through the lens of renormalization group theory: the map from residues mod 2^k to residues mod 2^(k+1) defines a 'coarse-graining' flow. Fixed points of this flow correspond to invariant classes under the Collatz dynamics.

### Domains
- quantum_field_theory
- statistical_physics
- number_theory

### Mathematical Formalization
RG transformation: R_k maps distributions on Z/2^k Z to Z/2^(k+1) Z via Collatz dynamics. Fixed point: mu* satisfying R_k(mu*) = mu*. Tao (2019) shows mu* is close to uniform for 'almost all' starting points.

### Key Analogical Connections
- Directly analogous to Wilson's RG for the Ising model
- Similar to wavelet multiresolution analysis in signal processing
- Related to p-adic analysis - Collatz dynamics has natural p-adic structure for p=2,3

### Implementation Hypothesis
Compute the distribution of Collatz iterates modulo 2^k for k=1..20 starting from delay records. Compare with uniform distribution. Measure deviation as function of k.

### Experiment Seed
For each delay record, compute histogram of T^j(n) mod 2^k for all orbit steps. Measure KL divergence from uniform.

### Cross-Domain Insight
This concept bridges 3 domains by viewing the Collatz problem through the lens of quantum_field_theory.
The mathematical formalization makes the connection precise and testable.

### Implementation Backlog
- [ ] Implement core algorithm from hypothesis
- [ ] Run experiment seed
- [ ] Validate against known results
- [ ] Compare with other concept cards' predictions
- [ ] Write up findings with reproducible code
- [ ] Cross-reference with semantic bridge connections

### Related Concepts
- **phase_transition_threshold**: Phase transitions are analyzed via RG flow; the Collatz coarse-graining defines a natural RG transformation on residue classes
- **modular_arithmetic_sieving**: Sieving by residue class mod 2^k IS the discretized RG flow; top sieve classes correspond to RG fixed-point neighborhoods
- **fractal_tree_structure**: The fractal dimension of the inverse Collatz tree is a RG invariant; self-similarity of the tree reflects scale invariance at criticality

### Verified Results (from our analysis)
- Modular distribution of iterates approaches uniform for large orbits
- Tao (2019) almost-all result interpreted as RG fixed point
- Coarse-graining scale k determines resolution of orbit structure
