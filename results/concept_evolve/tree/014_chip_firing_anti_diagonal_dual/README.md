# chip_firing_anti_diagonal_dual
Treat edge labels as signed chip-transfer channels carrying slope mass between neighboring copies of a subgraph. A vertex is forced when local cancellations leave only anti-diagonal charge outside the already-infected region, so sandpile-style potentials can guide where sparse edges should concentrate or dissipate mass.
## Domains
chip_firing, cellular_automata, additive_combinatorics
## Mathematical Sketch
A state is c: V -> Z^2 with legal moves c -> c + v(delta_u - delta_v) for each edge uv labelled v and c -> c + x delta_u for each initial seed x. Force e when c|_{V \ (T union {e})} = 0 and c(e) = a(1,-1), a != 0; search for edge layouts minimizing score while steering c toward such sparse anti-diagonal residues.
## Why This Bridge Might Matter
The new ingredient is a conserved-charge dual picture for arithmetic Kakeya certificates, intended to produce search heuristics and potentials rather than a direct theorem.
## Implementation Backlog
- Build: solver/chip_dual.py
- Build: solver/potential_functions.py
- Test: On fixed small constructible graphs, compare potential-guided edge mutations against uniform random mutations and track which search finds forceable instances faster.
- Check: Existing bootstrap-percolation papers optimize infection thresholds or times; this concept introduces vector-valued charge conservation and anti-diagonal concentration as the core search proxy.
## Closest Prior Art
- Linear algebra and bootstrap percolation (arXiv:1107.1410)
- U-bootstrap percolation: Characterizations and metastability (arXiv:1806.11405)
- Generalized Arithmetic Kakeya (arXiv:2411.13395)
