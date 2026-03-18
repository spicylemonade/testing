# Director Brief

## Decision

- Champion: `H1` - SAT-Pruned Quotient Proof-State CA.
- Backup: `H2` - Spatially Coupled Exact-Certificate Ladder CA.
- Reserve: `H3` - Interface-Typed Macrocell Grammar CA.

## Why H1 Wins

`H1` best fits the current selection criteria. It is the least cosmetic CA variant because the cell alphabet is canonicalized proof state rather than raw motifs, it confronts the decoder-leakage objection directly with a decoder-matched non-CA control, and it has the sharpest fast-kill tests: exact-valid yield, verified-score distribution, canonicalization ablation, `X`-label shuffle, held-out geometry, held-out `X`, and the planned complexity sweep. Relative to the falsifier memo, it is also the quickest lane to reject if the CA contributes nothing beyond symbolic pruning.

## Why H2 Is Backup

`H2` remains viable because it targets a real scaling gap: whether exact singleton-certificate templates can be coupled into larger forcing waves without paying the seed cost everywhere. It ranks below `H1` because it depends on an exact micro-gadget bank first, inherits more overlap with the existing spatially coupled branch, and is harder to interpret if it fails: a miss could come from bad templates, bad coupling, or the absence of any real arithmetic effect.

## Why H3 Stays Reserve

`H3` is the cleanest representation answer to the constructibility-native dynamics gap, but it has the largest implementation surface and the highest risk that interface design or decoder scaffolding does the hard work. Keep it reserve-only until the smaller, faster-to-kill lanes have been exhausted.

## Claim Boundary And Blocker

The repo still supports only a blocker-aware design claim, not "solve this using cellular automata." The frozen audit files say there is no shared exact no-repair `(X,G,R,T)` verifier or decoder in use, no exact decodes, no matched benchmark block, and no executed control suite. Until that changes, any stronger mathematical or empirical claim is off-limits.

## Exact Next Experiment

1. Locate or recover the shared exact no-repair decoder or verifier for six-line witnesses over `Z`. If it cannot be identified immediately, stop and log that blocker rather than expanding the CA search stack.
2. Open only `H1` at first: one SAT-constrained quotient-state rule schema, up to `3` rule families, and up to `10^3` exact decodes per family on tiny legal grids.
3. In the same block, run the decoder-matched non-CA baseline plus canonicalization ablation, `X`-label shuffle, held-out geometry, held-out `X`, and the planned complexity split.
4. Kill `H1` immediately if the gain disappears under the decoder-matched baseline or ablation, survives `X`-label shuffle, or appears only in the small-complexity regime.
5. Open `H2` only if `H1` clears the first exact gate or if `H1` fails for a narrow reason that leaves the coupling question genuinely unresolved.
