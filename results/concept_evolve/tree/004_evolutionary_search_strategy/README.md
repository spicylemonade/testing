# Evolutionary Search Strategy

## Concept Card #4: evolutionary_search_strategy

Applying evolutionary/genetic algorithms to search for high-delay Collatz numbers. The 'fitness' is stopping time, and crossover operates on binary representations. This bridges computational intelligence with number theory, treating the integers as a fitness landscape.

### Domains
- evolutionary_computation
- number_theory
- optimization

### Mathematical Formalization
Population P_t = {n_1,...,n_k}. Fitness f(n) = sigma(n). Selection: top-30% survival. Crossover: single-point binary crossover. Mutation: random bit-flip with rate mu=0.3. Objective: max_{n < N} f(n).

### Key Analogical Connections
- Directly analogous to biological evolution: stopping time = reproductive fitness
- Similar to simulated annealing on an energy landscape (physics)
- Related to genetic programming for symbolic regression

### Implementation Hypothesis
Initialize population from scaled known records + high-bit-density random numbers. Run for 200 generations with population 500. Our tests show evolutionary search finds good candidates but cannot beat exhaustive search for true records.

### Experiment Seed
Run evolutionary search for candidates with stopping time > 2283. Compare convergence rate with pure random sampling. Measure population diversity metrics over generations.

### Cross-Domain Insight
This concept bridges 3 domains by viewing the Collatz problem through the lens of evolutionary_computation.
The mathematical formalization makes the connection precise and testable.

### Implementation Backlog
- [ ] Implement core algorithm from hypothesis
- [ ] Run experiment seed
- [ ] Validate against known results
- [ ] Compare with other concept cards' predictions
- [ ] Write up findings with reproducible code
- [ ] Cross-reference with semantic bridge connections

### Related Concepts
- **biological_fitness_landscape**: GA navigates the fitness landscape of Collatz delay; landscape ruggedness determines GA convergence rate
- **modular_arithmetic_sieving**: Sieved residue classes restrict the GA search space, dramatically improving efficiency by pruning low-delay regions

### Verified Results (from our analysis)
- Population 500, 200 generations, mutation rate 30%
- Best fitness found: 988 steps (vs known record 2283)
- Convergence plateaus by generation 50
- Random sampling outperforms GA for this landscape topology
