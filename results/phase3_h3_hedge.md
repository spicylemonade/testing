# Phase 3 H3 Hedge

## Route

`H3_slope_bloom`

## Scope

One hedge pass only.

Use a single narrow rule class on the same corridor family:

- height `H = 2`
- fixed local rule width `2`
- fixed small interface alphabet inherited from H1

The only additional freedom is to allow the extracted nonzero label set to vary with level under a pre-registered small budget schedule.

## Exact Unrolling-To-Certificate Extractor

- The extractor remains the same legal corridor extractor from H1.
- The hedge changes only how the shared interface classes map to label tokens across levels.
- Every level still extracts directly to legal `(X; d_i; f_i; T; R)` data with no repair.

## Measured Quantities

- exact score,
- realized nonzero slope count,
- rational-complexity summary of the extracted label set,
- periodicity or repetition of the interface-to-label map.

## Kill Condition

Reject H3 immediately if either of the following happens:

1. realized slope complexity stays `O(1)` across level,
2. the label dynamics quickly become periodic while exact score does not beat matched bounded-slope controls.

## Why This Remains Reserve-Only

If the hedge survives, it still must beat the bounded-slope and direct no-CA controls on exact extracted score. Otherwise it is only a rephrased bounded-slope search.
