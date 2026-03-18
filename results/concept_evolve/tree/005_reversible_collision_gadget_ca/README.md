# Reversible Collision Gadget Ca

Build partitioned reversible cellular automata whose particle collisions implement only verifier-legal signed-vector operations. Reversibility narrows the search toward low-hidden-state gadgets that can be reused as sparse collision libraries for constructible witnesses.

## Context
Let F be a Margolus-block rule on local states carrying slope species and phase bits. Require F to be bijective and every nontrivial collision to decode to a legal signed update such as (x@u,x@v) \leftrightarrow (x@u,-x@v) plus transport states. Decode a periodic spacetime diagram \Omega into witness W and minimize S(W) subject to reversibility.

## Implementation Backlog
- Prototype the bridge: Enumerate tiny reversible block rules with 3-6 active symbols, mine short collision motifs, compose motifs into macro-gadgets for recursive interfaces, and keep only motifs whose decoded operations are exactly verifier-legal.
- Run the seed test: Exhaustively enumerate 2x2 block rules with two species plus vacancy, decode all period<=8 collision motifs, and measure motif reuse versus exact-score performance.
- Add label-shuffle, geometry-shuffle, and density-matched controls before trusting any signal.
- Keep the direction only if exact verifier outcomes improve, not just proxy metrics.

## Closest Prior Art
- Reversibility and surjectivity problems of cellular automata (10.1016/S0022-0000(05)80025-X)
- Finding Gliders in Cellular Automata (10.1007/978-1-4471-0129-1_13)
- On the arithmetic Kakeya conjecture of Katz and Tao (10.1007/s10998-018-0270-z)

## Novelty Delta
Reversibility becomes a structural prior for arithmetic witness gadgets, turning low-entropy collision libraries into candidate proof components.

## Why It Is Distinct
This is not reversible-CA classification for its own sake; every accepted rule must decode into exact forcing operations in the witness format.
