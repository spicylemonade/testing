# Baseline Panel Specification

This file freezes the concrete benchmark matrix for the exact-checker pipeline.

## Slopes
- Primary panel: `2`, `3/2`, `5/3`, `phi`, `sqrt(2)`, the plastic constant, the Salem quartic root of `x^4 - x^3 - x^2 - x + 1`, and `e`.
- Low-slope controls, pre-registered now because the domain is `r > 0`: `1/2` and `phi - 1`.

## Selector families

### Arithmetic progressions
- `n_k = k`
- `n_k = 2k`
- `n_k = 3k + 1`
- `n_k = 5k + 2`

### Finite unions of arithmetic progressions
- ordered union of residues `{0,1} mod 3`
- ordered union of residues `{0,2} mod 5`
- ordered union of residues `{0,1,3} mod 6`

### Ostrowski-definable selectors
- exactly one nonzero Ostrowski digit
- suffix `01`
- suffix `001`

### Linear-recursive selectors
- Fibonacci indices `F_{k+2}`
- Pell indices `P_{k+1}`
- Padovan-style indices `A_{k+3}` with `A_{k+3} = A_{k+1} + A_k`
- every second convergent denominator for quadratic irrational slopes
- beta-endpoint / cylinder selectors with suffix `10` for named Pisot follow-ups

## Recurrence and modulus panel
- orders: `d = 1, 2, 3, 4`
- moduli: `2, 3, 5, 7, 11`
- prime-square follow-up for any survivor: `25`

## Lock condition
No selector, slope, or modulus outside this file may be added to the benchmark matrix unless a blocker memo records why the frozen panel is insufficient.
