# H1 Modular-Shadow Memo

## Exact claim being pursued

Champion claim `H1` is split into one theorem-backed part and one screened extension.

1. **Theorem-backed positive-density statement.**
   For the frozen selector classes consisting of arithmetic progressions and finite unions of arithmetic progressions, the extracted value sequence `b_k = floor(n_k r)` satisfies a homogeneous constant-coefficient recurrence over `Z` if and only if `r` is rational.

2. **Screened zero-density extension.**
   For the frozen zero-density classes (Ostrowski-definable selectors and linear-recursive selectors), every candidate exact recurrence must survive a cross-modulus shadow test on `2,3,5,7,11,25`; in the current smoke artifacts this kills generic prefix mirages and leaves only structured survivor lanes to the quadratic and Pisot backup phases.

## Recurrence profiles and selector classes covered

- Recurrence orders in scope: `d = 1..4` in the frozen panel.
- Coefficient ring: `Z`, with exact verification only; approximate or floating-point fits do not count.
- Selector classes covered directly by proof: arithmetic progressions and finite unions of arithmetic progressions.
- Selector classes covered by screening rather than proof: linear-recursive selectors and Ostrowski-definable selectors.

## Why the positive-density theorem is plausible

### Arithmetic progressions
Let `n_k = a k + b` with `a >= 1`. Then

`Delta b_k = floor((a(k+1)+b) r) - floor((a k + b) r)`

is bounded. If `b_k` were an integer linear recurrence, then `Delta b_k` would also be an integer linear recurrence. A bounded integer linear recurrence is eventually periodic. But for irrational `r`, the difference sequence along an arithmetic progression is a mechanical two-value coding of irrational rotation and is not eventually periodic. Therefore irrational `r` cannot survive in the arithmetic-progression family. If `r = p/q` is rational, choosing `a` divisible by `q` makes `floor((a k+b) r)` an arithmetic progression, so every rational survives.

### Finite unions of arithmetic progressions
The ordered enumeration of a fixed finite union of residue classes has eventually periodic gaps. Taking one full period of the gap pattern yields residue subsequences of the form

`b_{m t + j} = floor((Q t + c_j) r)`

for fixed integers `Q > 0` and `c_j`. Each residue subsequence of a putative linear recurrence is itself a linear recurrence, so the arithmetic-progression argument applies to every residue subsequence. Hence irrational `r` is excluded here as well, while rationals still survive via the arithmetic baseline.

## Role of the modular-shadow / p-adic layer

- Any exact integer recurrence projects to every modulus, so a real survivor should exhibit consistent residue behavior modulo `2,3,5,7,11`, and then modulo `25` if it remains alive.
- `results/baseline/modular_shadow_smoke.json` shows how this filter behaves on the frozen panel templates:
  - `3/2` on `ap_2_0` is a certified exact recurrence with full modular consistency.
  - `phi` on `fib_indices` is a zero-density survivor candidate and is therefore quarantined as `sparse_subsequence_leak` until a structural proof upgrades it.
  - `plastic` on `ap_2_0` is an explicit `selector_shadow_failure`.
  - `plastic` on `union_mod3_01` stays only at `prefix_fit`, not theorem status.
- The p-adic intuition is that exact recurrences force eventually semilinear residue shadows; the smoke screen uses those shadows to demote long prefix fits before they become theorem language.

## Traceability to the frozen panel

- Rational survivors: `2`, `3/2`, `5/3`, and the low-slope control `1/2` are covered by the same arithmetic-progression proof and exact checker.
- Irrational exclusions in the positive-density lane: `phi`, `sqrt(2)`, the plastic constant, the Salem quartic root, `e`, and the low-slope control `phi - 1` all fall under the irrational side of the theorem for arithmetic and finite-union selectors.
- Zero-density survivors are intentionally not upgraded here; they are handed off to `H2` or `H3` after the modular screen.

## Remaining proof obligations

- Upgrade or kill the quadratic zero-density survivor lane by supplying exact structural certificates rather than prefix evidence.
- Test whether higher-degree Pisot endpoint selectors can freeze the error cocycle strongly enough to produce a genuine recurrence.
- If no higher-degree Pisot survivor passes, sharpen the final statement to a selector-family characterization rather than a universal irrational claim.
