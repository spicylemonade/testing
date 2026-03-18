# sweep_decoder_defect_transport

## Topic context
Represent unsolved target-direction obligations as defects on a locally Euclidean product graph and import sweep-decoder intuition for moving them. A local CA should transport these defects until they annihilate or condense into a single legal (1,-1) singleton, after which exact arithmetic verification takes over.

Primary domains: topological_codes, cellular_automata_decoders, additive_combinatorics.

Mathematical sketch:
Assign to each unsolved local relation a defect charge q_v\in\mathbb{Z}^2. A local transport rule \sigma updates q by moving charge downhill relative to an orientation or height function h. Accept only if repeated transport yields \sum_v q_v=(1,-1)e_u for some u and the transport history can be realized by legal certificate operations.

Closest prior art:
- Cellular-automaton decoders with provable thresholds for topological codes (arXiv:1809.10145)
- Strictly local one-dimensional topological quantum error correction with symmetry-constrained cellular automata (arXiv:1711.08196)
- A local automaton for the 2D toric code (arXiv:2412.19803)

Novelty claim:
The new step is defect transport in an integer relation lattice compiled into arithmetic Kakeya witnesses, not generic decoding of physical noise.

Differentiation:
No cited decoder is designed for singleton-supported integer relations or the score (m+r)/(n-t). The analogy is operational only if transport moves survive exact compilation into the verifier's rule set.

## Implementation backlog
- Build a minimal exact extractor for this concept before any broad search.
- Benchmark against raw arithmetic features and a no-CA baseline on the same small instances.
- Track description length, seed count, and exact score together to avoid proxy overfitting.
- Record an explicit falsifier for the concept after the first pilot sweep.
