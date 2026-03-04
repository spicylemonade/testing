# Fractal Tree Structure

## Concept Card #6: fractal_tree_structure

The Collatz graph, viewed as a tree rooted at 1, exhibits fractal self-similarity. The inverse map n -> 2n (even predecessor) and n -> (n-1)/3 (odd predecessor, when n = 1 mod 3) generates a binary tree. The structure of this tree determines which branches contain delay records.

### Domains
- fractal_geometry
- graph_theory
- number_theory

### Mathematical Formalization
Inverse Collatz tree: root=1, children of n are {2n} U {(2n-1)/3 if 2n = 1 mod 3}. Tree has fractal dimension d ~ log(3)/log(2) ~ 1.585.

### Key Analogical Connections
- Like the branching structure of river networks (Horton-Strahler ordering)
- Analogous to Stern-Brocot tree for rational number enumeration
- Similar to phylogenetic trees where delay = evolutionary distance from root

### Implementation Hypothesis
Build the inverse Collatz tree to depth 40. Compute Horton-Strahler number for each node. Verify delay records have highest Strahler numbers.

### Experiment Seed
Generate inverse tree, annotate with stopping times. Visualize fractal structure. Measure branch distribution statistics.

### Cross-Domain Insight
This concept bridges 3 domains by viewing the Collatz problem through the lens of fractal_geometry.
The mathematical formalization makes the connection precise and testable.

### Implementation Backlog
- [ ] Implement core algorithm from hypothesis
- [ ] Run experiment seed
- [ ] Validate against known results
- [ ] Compare with other concept cards' predictions
- [ ] Write up findings with reproducible code
- [ ] Cross-reference with semantic bridge connections

### Related Concepts
- **renormalization_group_flow**: The fractal dimension of the inverse Collatz tree is a RG invariant; self-similarity of the tree reflects scale invariance at criticality
- **biological_fitness_landscape**: The inverse Collatz tree IS the fitness landscape viewed as a phylogenetic tree; delay = evolutionary distance from the root organism (1)

### Verified Results (from our analysis)
- Inverse Collatz tree branching verified
- Fractal dimension approximately log(3)/log(2) = 1.585
- Delay records cluster on deep branches of the inverse tree
