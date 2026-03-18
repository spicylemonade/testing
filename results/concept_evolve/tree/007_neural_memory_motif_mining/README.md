# neural_memory_motif_mining

## Topic context
Mine the newly expanded landscape of robust neural-CA memories for motifs that naturally heal local perturbations and propagate domain walls. The hypothesis is that some of these healing rules correspond to reusable low-overhead forcing fronts after exact extraction.

Primary domains: statistical_physics, neural_cellular_automata, additive_combinatorics.

Mathematical sketch:
Sample a family of learned memory rules \{\phi_i\}. For each \phi_i, estimate robustness R_i under noise and damage, and define an extraction operator E(\phi_i) that maps stable wavefront motifs to candidate certificate modules. Search for high-R_i, low-S(E(\phi_i)) pairs on a Pareto frontier.

Closest prior art:
- Exploring the Landscape of Non-Equilibrium Memories with Neural Cellular Automata (arXiv:2508.15726)
- A Toom rule that increases the thickness of sets (DOI:10.1007/BF01015567)
- Universality for two-dimensional critical cellular automata (arXiv:1406.6680)

Novelty claim:
The novelty is using memory-rule discovery as a motif mine for exact arithmetic witnesses, rather than claiming the Kakeya problem itself is a memory-phase question.

Differentiation:
This is not a reimplementation of nonequilibrium memories because the target observable is not lifetime or phase coexistence. It is the verifier score of extracted arithmetic certificates.

## Implementation backlog
- Build a minimal exact extractor for this concept before any broad search.
- Benchmark against raw arithmetic features and a no-CA baseline on the same small instances.
- Track description length, seed count, and exact score together to avoid proxy overfitting.
- Record an explicit falsifier for the concept after the first pilot sweep.
