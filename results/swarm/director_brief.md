# Director Brief

Date: 2026-03-13
Task: Improve the Ramsey number `R(5,5)` bound
Working frontier: `43 <= R(5,5) <= 46`

## Decision

Champion: `H1` orbit-stable extension-obstruction atlas for lifting `42`-vertex frontier graphs.

Backup: `H2` decomposition-primitive upgrade beyond split-vertex and transverse-edge gluing.

Reserve: `H3` proof-carrying reusable obstruction certificates, but only as an attachment to `H1` or `H2`, not as a standalone novelty claim.

## Why `H1` Wins

- It has the strongest novelty moat in the current materials because it targets a reusable Ramsey object: recurring minimal obstruction cores in failed `42 -> 43` extensions.
- It is the fastest honest kill. If those cores do not recur across orbit-distinct parents, fail leave-one-parent-out transfer, or break witness-survival tests, the direction dies quickly.
- It bridges the currently siloed lower-bound and upper-bound lines. The same obstruction dictionary can become both search pruning and proof-grade forbidden-pattern lemmas.
- It avoids the main falsifier trap of "same search, better engine" because the claimed output is structural compression, not a nicer optimizer trajectory.

## Why `H2` Is Backup

- It points directly at the upper-bound bottleneck identified in the scout outputs: the decomposition language may be weaker than the solver layer.
- It remains riskier on novelty because it sits closer to the Angeltveit-McKay and Gauthier line, so it can easily collapse into "same decomposition, stronger SAT."
- Keep it as backup because it still has a clean falsifier: matched proof-footprint benchmarks on solved subcases can kill it quickly.

## Why `H3` Is Reserve Only

- Reusable certificates are valuable, but on their own they risk becoming infrastructure rather than a bound-moving idea.
- Promote `H3` only if it is attached to a concrete obstruction family from `H1` or a genuinely new decomposition primitive from `H2`.

## Immediate Handoff Specs

For `H1`, the next researcher action should be specification only: define a canonical atlas for the available `42`-vertex critical colorings, enumerate orbit-distinct one-vertex extensions, and predefine the transfer test that would kill the hypothesis if obstruction cores do not generalize beyond one parent lineage.

For `H2`, the first benchmark spec should compare adjacent-pair, nonadjacent-pair, and small-shell decompositions against the current split/gluing baseline under the same solver, proof logging, and checker regime.

## Deprioritized Branches

- Generic defect minimization, GA, SA, RL, or rare-event search without a new reusable obstruction.
- Generic LP, flag, SDP, or Terwilliger tightening without a rational or exact certificate path.
- IC3, PDR, CEGAR, or clause-learning narratives that leave the underlying decomposition unchanged.

## Unresolved Blocker

The prompt named `results/swarm/hypothesis_bridge.md` and `results/swarm/hypothesis_negative_space.md`, but those files are absent in the workspace. The synthesis above is therefore based on `gap_map.md`, `falsifier.md`, the prior-art gap notes, the cached probe files, and the existing tool-plan notes.

If tighter arbitration is required before execution, the exact next step is to regenerate those two missing scout summaries from the already cached local artifacts only, then rerun ranking. Do not widen literature search until that gap is closed.
