# Glider Motif Mining

Mine gliders, blinkers, and collision motifs from small CA rules, then reinterpret them as portable witness fragments: worldlines become repeated copy interfaces and collisions become candidate certificate births. This yields a reusable gadget library before full witness assembly.

## Context
For a rule F let M(F) be the set of periodic localized spacetime motifs modulo translation and phase. A decoder D maps m\in M(F) to partial witness deltas (\Delta f,\Delta R,\Delta T). Search motif multisets maximizing \Delta(n-t)/(\Delta m+\Delta r) subject to compatibility and constructibility constraints.

## Implementation Backlog
- Prototype the bridge: Use Wuensche-style exhaustive motif search or SAT-enumerated short orbits to populate a motif database, cluster motifs by decoded effect, and compose only the highest-yield motifs into larger recursive scaffolds.
- Run the seed test: Enumerate motifs up to bounding box 6x6x8 for a small reversible or conservative rule family and compare motif-composed witnesses against direct random full-witness search.
- Add label-shuffle, geometry-shuffle, and density-matched controls before trusting any signal.
- Keep the direction only if exact verifier outcomes improve, not just proxy metrics.

## Closest Prior Art
- Finding Gliders in Cellular Automata (10.1007/978-1-4471-0129-1_13)
- Growing Neural Cellular Automata (10.23915/distill.00023)
- Pattern Problems related to the Arithmetic Kakeya Conjecture (arXiv:2011.07056)

## Novelty Delta
The new step is decoding dynamical motifs into arithmetic proof fragments instead of treating them as purely dynamical curiosities.

## Why It Is Distinct
Motif discovery is only accepted when the motifs integrate into exact constructible graphs and forcing pairs with measurable score.
