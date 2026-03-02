# ConceptEvolve Steering Notes

## Steering Direction 1: Multi-Prime Quadratic Residue CSP as Computational Backbone
**Source Concept**: "Constraint Satisfaction via Quadratic Residue Propagation"

The perfect cuboid equations create a constraint network where quadratic residue conditions modulo each prime p eliminate candidate triples. This is structurally identical to arc consistency propagation in CSP solvers. The key insight is that combining constraints from many primes multiplicatively reduces the search space — analogous to unit propagation in SAT solving.

**Informs rubric items**: item_008 (brute force filtering), item_012 (modular sieve), item_016 (constraint checker), item_022 (ablation study)

## Steering Direction 2: Elliptic Curve Fibration for Structured Search
**Source Concept**: "Elliptic Curve Fibration and Rational Points"

Fixing one edge transforms the perfect cuboid problem into a rational point search on an elliptic curve. Different edge values give different curves with varying ranks. Parametric Euler brick families (Saunderson, Euler) correspond to rational sections of the elliptic surface. The closest near-misses likely arise from curves with high Mordell-Weil rank.

**Informs rubric items**: item_013 (parametric families), item_015 (novel search with EC methods), item_017 (concept exploration)

## Steering Direction 3: Brauer-Manin Obstruction for Theoretical Non-Existence
**Source Concept**: "Topological Obstruction via Brauer Group" + bridge chain CSP→lattice→Brauer

If the Brauer group of the cuboid variety is non-trivial, it could prove non-existence despite local solvability. The bridge chain from computational sieving (showing extreme sparsity) through lattice point theory to Brauer-Manin obstruction connects our empirical observations to potential theoretical proofs.

**Informs rubric items**: item_005 (problem specification), item_014 (near-miss analysis — evidence for/against existence), item_019 (comprehensive near-miss analysis), item_025 (limitations and future directions)

## Priority: Direction 1 (Modular Sieve CSP)
**Rationale**: This is the most immediately actionable direction. It directly informs the core computational infrastructure (items 008, 012) that all later experiments depend on. The CSP framing provides a principled way to combine modular constraints, and the implementation is well-understood. Directions 2 and 3 build on the computational results from Direction 1.
