# Convergent Hankel Detector Analysis

## What was implemented

The experiment follows the concept card literally:
- compute convergent blocks for each slope,
- sample `x_j = floor(q_j r)` on every second convergent denominator,
- build exact integer Hankel blocks,
- recover an annihilating polynomial from the first 12 samples,
- validate the same recurrence on a 20-sample exact holdout.

## Main finding

- `phi` and `1 + sqrt(2)` survive with low-order exact recurrences.
- `plastic`, the Salem quartic control, and `e` do not admit any order-`<=4` exact recurrence under the frozen even-convergent construction.
- `sqrt(2)` also survives, so the mechanism exposed here is not Pisot-only. It is better described as a periodic-continued-fraction / quadratic-convergent mechanism.

## Why this matters

This front-end converts the vague phrase "quadratic irrationals look special" into an exact detectable phenomenon with certificates and controls. It also gives a reusable false-positive detector: higher-degree algebraic and transcendental controls stop surviving once the search is forced to stay within the frozen order range `d <= 4`.
