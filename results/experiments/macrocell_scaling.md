# Macrocell Scaling

## Status

Failed.

## Exact micro-gadget bank available

The only exact-valid micro-gadget bank produced in this pass is the exhaustive
`2 x 2` trace corpus under
`results/theory/forcing_traces/tiny_2x2_full_seeds_le3/`.

Its exact properties are rigid:

- `48` exact-valid witnesses in the audited regime;
- every one has score `7/4`;
- every one has the same two-layer corner-nucleation trace skeleton.

## Scaling attempt outcome

This micro-bank did not scale into an interface-typed macrocell library:

- the width-`2` coverability obstruction from
  `results/theory/abelian_coverability_duality.md` shows that fresh seedless
  columns cannot activate unilaterally;
- the local-rule atlas in
  `results/theory/local_rule_no_go_atlas.md` shows zero one-sided strict
  improvements in widths `2` and `3`;
- random exact searches on full `2 x N` ladders with sparse seeds never
  produced a scalable coupled family.

## Why the item fails

The acceptance criterion requires three exact-verified scales, maintained or
improved score density, and a largest-scale win over flat-lattice CA and static
grammar enumeration.  None of those prerequisites exists yet because the
available micro-gadget does not compose into a verified macrocell interface.
