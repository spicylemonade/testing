# Arithmetic Sensitivity Phase Transition

## Status

Failed.

## Reason

This item requires a positive exact-valid family whose performance can then be
measured under:

- rational-complexity sweeps;
- held-out legal alphabets;
- `X`-label shuffling;
- proof-state canonicalization changes.

The current pass never reached that stage.  The exact search kept failing
earlier, at the local activation level:

- every exact-valid audited `2 x 2` witness is a rigid `7/4` warm-up gadget;
- widths `2` and `3` have no one-sided local activation over the audited
  palette;
- no exact-valid strip or macrocell family below the target score was found.

## Consequence

Without a positive family, any arithmetic-sensitivity plot would be degenerate:
the candidate families already collapse before `X`-label shuffling is applied.
That does not satisfy the acceptance criterion, which specifically asks for a
counterintuitive collapse boundary or survival zone.
