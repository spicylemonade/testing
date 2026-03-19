# Spatial Coupling Threshold

## Status

Failed.

## Exact seed bank used

The exact-valid seed bank available in this pass is the rigid `2 x 2` warm-up
family recorded in
`results/theory/forcing_traces/tiny_2x2_full_seeds_le3/`.

## Coupling evidence gathered

The search produced negative rather than positive coupling evidence:

- the one-sided strip atlas in widths `2` and `3` has zero strict-improvement
  cases;
- full `2 x N` ladders with sparse exact seeds did not produce a forcing wave
  in direct exact search;
- full `3 x N` strips with two exact seeds also failed to produce a promoted
  exact-valid family.

So while the warm-up gadget proves that a local coupled nucleation event exists,
the pass did not recover a six-to-ten-slab exact ladder whose score density or
hit rate beats uncoupled repetition and the matched baselines.

## Why the item fails

The acceptance criterion requires:

- a coupled slab family;
- at least two coupling widths;
- a clear exact score-density or hit-rate advantage;
- collapse under template randomization or `X`-label shuffling.

No such family was found, so the item fails on missing positive evidence rather
than on missing bookkeeping.
