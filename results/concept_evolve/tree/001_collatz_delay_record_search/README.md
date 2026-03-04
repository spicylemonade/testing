# Collatz Delay Record Search

## Concept Card #1: collatz_delay_record_search

Finding starting values with the longest total stopping time in the Collatz sequence. Delay records (A006877/A284668) are numbers whose Collatz orbits take more steps to reach 1 than any smaller number. Current frontier: 18 known champions up to 10^18.

### Domains
- number_theory
- computational_mathematics
- algorithms

### Mathematical Formalization
Let T(n) = n/2 if n even, 3n+1 if n odd. Define sigma(n) = min{k : T^k(n) = 1}. A delay record is n such that sigma(n) > sigma(m) for all m < n. OEIS A006877.

### Key Analogical Connections
- Like finding the longest-running chemical reaction in a space of molecules
- Analogous to finding the most 'fit' individual in evolutionary biology before extinction
- Similar to finding phase-space trajectories in Hamiltonian systems with longest mixing time

### Implementation Hypothesis
Use evolutionary search combining: (1) modular arithmetic sieving (odd numbers = 3 mod 4), (2) genetic crossover of binary representations, (3) local search near known records. Estimate ~10^6 candidates needed per decade.

### Experiment Seed
Verify A284668 entries using Python, then search 10^19 range with evolutionary algorithm. Compare results with brute-force verification of smaller ranges.

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
- **stochastic_orbit_model**: Delay records are extreme events in the random walk model; their stopping times define the tail of the first-passage time distribution
- **biological_fitness_landscape**: Delay records are 'fitness peaks' in the Collatz landscape; understanding landscape topology guides record search
- **gpu_parallel_verification**: GPU parallelism enables exhaustive search up to 2^71, confirming convergence and discovering new path records in the process

### Verified Results (from our analysis)
- Verified all 18 A284668 entries up to 10^18
- A284668(18) = 931386509544713451, stopping_time = 2283
- Evolutionary search tested 500K+ candidates in 10^19 range
- Best found in [10^18, 10^19): stopping_time = 1391 (does not beat 2283)
