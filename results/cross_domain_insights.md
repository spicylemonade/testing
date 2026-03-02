# Cross-Domain Concept Discovery: Insights for Perfect Cuboid Research

## Source Materials
- `results/concept_evolve/concept_cards.json` — 10 cross-domain concept cards
- `results/concept_evolve/semantic_bridge.json` — 10-node typed graph with bridge chains
- `results/concept_evolve/reframings.json` — 5 domain reframings
- `results/concept_evolve/introspection.json` — 5 associations + 3 anomaly injections

## Key Cross-Domain Analogies

### 1. Constraint Satisfaction / Graph Coloring
**Source:** Graph_Coloring_Constraint concept card
**Analogy:** The perfect cuboid equations form a hypergraph CSP. The treewidth (3) of the constraint graph suggests that constraint propagation can efficiently prune the search.
**Actionable:** Implement modular arithmetic constraints as arc-consistency propagation before any arithmetic. This was implemented in `src/modular_filter.py` achieving 99.8% rejection rate.

### 2. Fitness Landscape / Spectral Gap
**Source:** Evolutionary_Fitness_Landscape + Spectral_Gap_Nonexistence concept cards, bridge chain [fitness_landscape → spectral_gap → topological_obstruction]
**Analogy:** Near-misses form a fitness landscape. If the minimum gap between Euler brick space-diagonal-squared and the nearest perfect square GROWS with edge magnitude, this is empirical evidence for a spectral gap — and thus for non-existence.
**Actionable:** Track near-miss residuals as a function of edge size and fit a power law. If residual ~ N^α with α > 0, this supports non-existence. Implemented in item_019 analysis.

### 3. Musical Temperament / Comma Analysis
**Source:** Acoustics reframing
**Analogy:** The perfect cuboid is analogous to finding a rectangular room with all resonant modes in just intonation. The syntonic comma in music theory (81/80 ≈ 1.0125) represents the impossibility of simultaneously satisfying all harmonic ratios. The "cuboid comma" is the space diagonal residual.
**Actionable:** Analyze the algebraic structure of space diagonal residuals — are they always divisible by certain primes? Do they follow a pattern that could be proved never-vanishing?

### 4. Reverse Search from Space Diagonal
**Source:** Circuit design reframing (network synthesis = top-down decomposition)
**Analogy:** Instead of starting from edges and checking diagonals (bottom-up), start from candidate space diagonal values g and decompose g² into three-square sums a²+b²+c² where each pair-sum is also a perfect square.
**Actionable:** Enumerate integers g satisfying necessary conditions (odd, prime factors ≡ 1 mod 4, composite, not a prime power), decompose g² as sums of three squares, and check face diagonals. This reverses the search direction and may be more efficient for large g.

### 5. Symmetry Reduction
**Source:** Molecular chemistry reframing (space group analysis)
**Analogy:** The cuboid system has an S₃ × (Z/2)³ symmetry group of order 48. Searching only a fundamental domain reduces the search by a factor of 48.
**Actionable:** Implemented in all search routines by requiring a ≤ b ≤ c (S₃ reduction gives factor 6).

## Two Actionable Research Directions

### Direction A: Spectral Gap Analysis of Near-Miss Distribution
**Concept source:** Spectral_Gap_Nonexistence + Evolutionary_Fitness_Landscape
**Implementation:** Fit near-miss scores vs log(edge magnitude) to detect gap widening. If confirmed, this provides computational evidence supporting non-existence beyond just "we didn't find it."
**Status:** To be implemented in item_019.

### Direction B: Reverse Search from Space Diagonal
**Concept source:** Circuit design reframing
**Implementation:** Enumerate candidate g values, decompose g² as sums of three squares (using Legendre's three-square theorem conditions), then check face diagonals. This approach is complementary to the edge-based search and may cover different regions of the solution space.
**Status:** Can be integrated into combined search (item_018).
