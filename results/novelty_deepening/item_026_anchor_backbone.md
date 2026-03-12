# Item 026: Anchor/Offset Backbone

## Result

Negative certificate. The anchor-centered backbone separates record windows from the chosen controls only through an extremal right-edge correction, and that correction alphabet does not stay inside the training-time support.

## Independent Checker

- The separately written checker agrees with the baseline generator through `10^5` steps.
- Agreement artifact: `results/novelty_deepening/checker_agreement.json`.

## Shared Corpus

- Baseline record windows with `gap >= 20`: `5`.
- Anchor-centered matched non-record windows: `45`.
- Size-matched affine surrogate windows: `50`.

## Backbone Test

- Fixed training prefix: all baseline records up to step `10^5`; training correction support = `[(4, 4), (7, 2), (8, 4)]`.
- Held-out record correction pairs: `[[17, 1], [14, 2]]`.
- Bounded-support check: `False`.
- Held-out AUROC for the extremal anchor score `-left_of_anchor`: `0.922`.

## Why This Falsifies A Low-Memory Novel Mechanism

1. The anchor itself is theorem-level and universal: every true row gap contains the previous column term exactly once.
2. On the matched anchor-centered controls, the only strong discriminator is that the record window is the unique rightmost fully covered anchored interval of its length.
3. That discriminator depends on the fresh right-edge correction `r_{n+1} - c_n`, not on a bounded alphabet learned from early records.
4. The held-out records at gaps `28` and `30` introduce new correction pairs outside the training support, so the bounded-correction requirement fails exactly where novelty would need to survive.

## Conclusion

The anchor/offset lane remains mathematically useful as a rigid geometric description of the frontier, but it does not currently supply a bounded-memory novel mechanism beyond the tautological extremality of the actual record window.
