# ConceptEvolve Steering Notes

## Steering Direction 1: CSP/SAT Encoding with Modular Pre-pruning
**From concept cards:** Graph_Coloring_Constraint, Modular_Sieve_as_Error_Correcting_Code
**Informs rubric items:** item_008 (modular filter), item_015 (constraint solver), item_016 (quadratic sieve)
**Description:** Encode the perfect cuboid problem as a constraint satisfaction problem where modular arithmetic constraints become unit clauses. Pre-compute quadratic residue tables for primes up to 1000 and use them as arc-consistency propagation to prune the search space before any expensive integer square root operations. The bridge chain [graph_coloring_constraint → modular_sieve → CRT_reconstruction] provides the full pipeline.

## Steering Direction 2: Near-Miss Spectral Gap Analysis
**From concept cards:** Spectral_Gap_Nonexistence, Evolutionary_Fitness_Landscape, Topological_Obstruction
**Informs rubric items:** item_009 (near-miss tracker), item_019 (near-miss statistics), item_017 (non-existence analysis)
**Description:** Track not just the best near-misses but the distribution of near-miss scores as a function of edge magnitude. If the minimum residual grows with scale (spectral gap), this is empirical evidence for non-existence via a Brauer-Manin-type obstruction. Plot near-miss score vs log(edge magnitude) and fit a power law to detect any gap widening.

## Steering Direction 3: Pythagorean Triple Fragment Assembly
**From concept cards:** Resonance_Condition, anomaly injection (protein folding analogy)
**Informs rubric items:** item_007 (Euler brick generator), item_012 (triple decomposition), item_013 (elliptic families)
**Description:** Instead of searching triples (a,b,c) directly, pre-compute all Pythagorean triples up to a bound and index them by leg values. Then find all pairs of triples sharing a common leg — these correspond to two faces of a potential cuboid. Check whether the remaining face and space diagonal also form valid triples. This fragment assembly approach is dramatically more efficient than brute force because it only examines combinations that already satisfy 2 of 4 constraints.

## Priority
**Direction 3 (Fragment Assembly) first** because it directly addresses the computational bottleneck in Phase 2 and Phase 3. By pre-computing Pythagorean triple pairs sharing legs, we can generate Euler bricks orders of magnitude faster than brute force, enabling larger search ranges. Directions 1 and 2 are applied on top of this foundation.
