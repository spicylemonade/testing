# Hypothesis Negative Space

This refresh supersedes the stale earlier draft. It is grounded in the current repo state: `results/research_context.md`, `results/literature/prior_art_gap.md`, `results/literature/gap_frontier.md`, `results/swarm/director_brief.md`, `results/concept_evolve/*`, `results/swarm/falsifier.md`, and the benchmark / novelty audits.

Constraint that does not move:
- Do not spend real search budget until a shared exact integer decoder / verifier for six-line witnesses is recovered or implemented. Every direction below is only admissible under exact decode, no repair, label-shuffle controls, and decoder-matched baselines.

Solution families to avoid repeating:
- Re-proposing `H1` itself as the main negative-space story. It is already the champion lane and heavily analyzed.
- Re-proposing `H2` sparse defects as the default next branch. It remains backup only, not fresh negative space.
- Observer-guided macrocells, neural CA, reversible / glider libraries, flow-firing / odometer proxies, number-conserving current screens, and modular-shadow-first curricula. These are retired or explicitly deprioritized unless new exact evidence appears.
- Any fixed-small-alphabet or bounded-slope story that cannot survive complexity sweeps and `X`-label shuffling.

## 1. Spatially Coupled Exact-Certificate Ladders

- Gap attacked:
  Prior work can describe or search for local witness gadgets, but it has not actually tested whether exact singleton-certificate templates can be coupled into a stable forcing wave on larger product grids. This is the scaling gap, not the local-generation gap.
- Hypothesis:
  Start from tiny exact-valid micro-gadgets and treat them as CA macrocells on stage-indexed slabs. Add only narrow exact interface channels between adjacent slabs so a small boundary seed launches a monotone forcing wave across the ladder. If the coupling is real, the exact score density should beat uncoupled repetition at matched `m(G)+|R|`.
- Why this is negative space:
  It attacks what earlier branches could not scale, while avoiding the already-explored "search the whole witness directly" framing.
- First test:
  Build `6-10` coupled slabs from one micro-gadget family, sweep coupling width and boundary seeds, and compare exact score, exact-valid hit rate, and label-shuffle collapse against uncoupled repeats and the decoder-matched non-CA comparator.
- Angle to avoid:
  `Geometry-Only Wave Story`  
  Kill this direction if the apparent gain survives `X`-label shuffling or depends on proxy wave metrics rather than exact forcing.

## 2. SAT-Pruned Local Rule Synthesis with E-Graph Span Caching

- Gap attacked:
  The repo never actually tested whether a CA family adds value once illegal local rules and span-equivalent certificate fragments are removed up front. That missing test is a real scalability bottleneck because exact search budget is otherwise wasted on malformed or redundant candidates.
- Hypothesis:
  Use SAT to enumerate only short-period local rules whose decoded spacetime blocks are witness-legal, then canonicalize local linear-span derivations in an e-graph before rollout. A CA built on this symbolic backbone should raise exact-valid yield enough to make larger exact sweeps feasible.
- Why this is negative space:
  It attacks what prior work failed to test, namely whether the hard part is better local rule design rather than more search volume or richer proxy dynamics.
- First test:
  Enumerate tiny radius / short-period rule families under legality constraints, then compare exact-valid hit rate, verifier time, and score distribution against random rule sampling and the decoder-matched witness-search comparator.
- Angle to avoid:
  `Compiler Does The Work`  
  If the gain disappears when the same SAT / e-graph pruning is handed to a non-CA baseline, this is infrastructure only, not a real CA direction.

## 3. Interface-Typed Macrocell Grammar CA

- Gap attacked:
  Flat-lattice CA ignore recursive constructibility. Most explored branches mutated local fields or whole witnesses, but they did not make the copy-and-glue interface grammar itself the automaton state.
- Hypothesis:
  Freeze a small library of exact-valid gadget macrocells whose boundary states encode legal gluing, active labels in `X`, and singleton-certificate exposure. Run a synchronous or asynchronous macrocell automaton that only composes compatible interfaces, so recursive legality is enforced by local state instead of repaired later.
- Why this is negative space:
  It targets the representation mismatch that prior work mostly ignored and could scale better than raw edge-level CA because recursion is built into the alphabet.
- First test:
  Fix `8-16` macrocell types from tiny exact seeds, search `3x3` macroboards, then test `4x4` and `5x5` holdouts for exact-valid yield, score density, and failure-mode stability under geometry and label shuffles.
- Angle to avoid:
  `Pretty Tiling Trap`  
  Do not reopen the SFT / tiling analogy unless every macrocell carries verifier-legal proof fragments and exact score improves after full decode.

## Recommended Order

1. Recover or implement the exact verifier first.
2. Open `SAT-Pruned Local Rule Synthesis with E-Graph Span Caching` first, because it most directly tests whether exact-valid yield can scale without decoder leakage.
3. Open `Spatially Coupled Exact-Certificate Ladders` only after at least one exact micro-gadget family exists.
4. Keep `Interface-Typed Macrocell Grammar CA` as the reserve representation branch if flat edge-level search remains too brittle.
