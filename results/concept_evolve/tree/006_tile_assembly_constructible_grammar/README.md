# Tile Assembly Constructible Grammar

Compile recursive constructibility into a tile grammar where each macro-tile encodes a small verified gadget and boundary colors encode allowed gluing interfaces. Sparse nonzero edges become sparse defect tiles, so the search shifts from graph enumeration to local grammar design.

## Context
Let \mathcal{T} be a Wang-tile set whose edge colors encode interface states (copy index, boundary certificate, slope class). A valid tiling \tau of an L_1\times\cdots\times L_k board induces d_i, the support of each f_i, and seed data R,T. Search tile sets and defect budgets q minimizing S(\tau) while preserving local matching constraints.

## Implementation Backlog
- Prototype the bridge: Start from a tile set for a tiny verified gadget, expose only defect tiles and boundary colors to search, decode each completed tiling to the six-line witness format, and exact-verify it.
- Run the seed test: Use 8-16 tile types on a 3x3 macroboard, then test whether tile grammars that work on 3x3 generalize to 4x4 and 5x5 boards with stable score density.
- Add label-shuffle, geometry-shuffle, and density-matched controls before trusting any signal.
- Keep the direction only if exact verifier outcomes improve, not just proxy metrics.

## Closest Prior Art
- Theory of algorithmic self-assembly (10.1145/2380656.2380675)
- Algorithmic Self-Assembly of DNA Sierpinski Triangles (10.1371/journal.pbio.0020424)
- Pattern Problems related to the Arithmetic Kakeya Conjecture (arXiv:2011.07056)

## Novelty Delta
This transfers algorithmic self-assembly from target-pattern construction to exact arithmetic witness generation with a verifier-defined semantics.

## Why It Is Distinct
Unlike DNA-pattern papers, the tiles do not merely realize a picture; they assemble explicit arithmetic proof data that is scored by the verifier.
