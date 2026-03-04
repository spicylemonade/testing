# Biological Fitness Landscape

## Concept Card #8: biological_fitness_landscape

Viewing Collatz stopping time as a 'fitness function' over the integers, the delay records form a fitness landscape analogous to protein fitness landscapes in evolutionary biology. The ruggedness, correlation length, and neutrality determine the difficulty of finding records.

### Domains
- evolutionary_biology
- optimization
- number_theory

### Mathematical Formalization
Fitness landscape F: Z+ -> Z+, F(n) = sigma(n). Autocorrelation: rho(d) = Corr(F(n), F(n+d)). NK-landscape analogy: N = log2(n) bits, K = number of interacting bit positions.

### Key Analogical Connections
- Directly analogous to protein fitness landscapes (mutations = bit flips)
- Similar to loss landscapes in neural network training
- Related to spin glass energy landscapes in condensed matter physics

### Implementation Hypothesis
Compute F(n) for n in [10^6, 10^6 + 10^5]. Measure autocorrelation function. Estimate correlation length.

### Experiment Seed
Sample stopping times in a window of 100K consecutive integers. Compute spatial autocorrelation. Measure landscape ruggedness.

### Cross-Domain Insight
This concept bridges 3 domains by viewing the Collatz problem through the lens of evolutionary_biology.
The mathematical formalization makes the connection precise and testable.

### Implementation Backlog
- [ ] Implement core algorithm from hypothesis
- [ ] Run experiment seed
- [ ] Validate against known results
- [ ] Compare with other concept cards' predictions
- [ ] Write up findings with reproducible code
- [ ] Cross-reference with semantic bridge connections

### Related Concepts
- **evolutionary_search_strategy**: GA navigates the fitness landscape of Collatz delay; landscape ruggedness determines GA convergence rate
- **collatz_delay_record_search**: Delay records are 'fitness peaks' in the Collatz landscape; understanding landscape topology guides record search
- **fractal_tree_structure**: The inverse Collatz tree IS the fitness landscape viewed as a phylogenetic tree; delay = evolutionary distance from the root organism (1)
- **phase_transition_threshold**: The critical point lambda=0 is analogous to the 'error threshold' in quasispecies theory; beyond it, genetic information (convergence) is lost

### Verified Results (from our analysis)
- Collatz stopping time landscape is highly rugged
- Local perturbations (+/- 10K) from delay records show no improvement
- Landscape correlation length appears very short
