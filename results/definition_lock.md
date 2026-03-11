# Definition Lock

## Problem statement used for this run
For a real number `r > 0`, study whether there exists an increasing integer sequence `n_0 < n_1 < ...` from a predeclared selector family such that the extracted value sequence

`b_k = floor(n_k r)`

satisfies a homogeneous constant-coefficient linear recurrence over `Z`:

`c_0 b_k + c_1 b_{k+1} + ... + c_d b_{k+d} = 0` for all `k >= K`, with `d >= 1` and `c_d != 0`.

## Scope decisions forced by the falsifier and director brief
- `r` domain: all positive reals `r > 0`; the main panel is centered on `r >= 1`, but low-slope controls in `(0,1)` are pre-registered now so they do not count as post-hoc expansion later.
- Subsequence meaning: an extracted ordered sequence of values, not a set and not a symbolic factor. Every claim is about the numeric sequence `floor(n_k r)` in order.
- Recurrence meaning: homogeneous, constant-coefficient, integer-coefficient recurrence. Variable-coefficient, inhomogeneous, approximate, and floating-point-only fits do not count.
- Eventuality: a candidate may start after a finite burn-in `K`, but the recurrence must then hold identically, not just on a sampled prefix.

## Degeneracy policy
- Positivity for the project question uses the broad arithmetic notion above, so degenerate recurrences are allowed.
- Reason: excluding classical degeneracies would incorrectly erase the rational arithmetic-progression baseline that the falsifier identifies as mandatory.
- Still, each candidate is tagged with a `nondegenerate` diagnostic flag using the classical root-ratio test; this flag informs novelty claims but does not redefine the problem.

## Allowed selector families
Only the following predeclared selector schemas are allowed in this run.

1. Arithmetic progressions: `n_k = a k + b` with fixed integers `a >= 1`, `b >= 0`.
2. Finite unions of arithmetic progressions: the selector is the increasing enumeration of a fixed finite union of residue classes (possibly with fixed offsets) and therefore has eventually periodic gaps.
3. Ostrowski-definable selectors: indices defined by fixed predicates on the Ostrowski expansion attached to the tested irrational slope. The predicate template is fixed before running experiments; only the slope-specific numeration changes.
4. Linear-recursive selectors: increasing integer sequences produced by a fixed homogeneous linear recurrence. This family includes named control sequences (Fibonacci, Pell, Padovan/Tribonacci-style controls) and slope-attached canonical constructions that are declared up front, such as periodic-continued-fraction convergent subsequences for quadratic slopes and beta-endpoint numeration sequences for the named Pisot follow-up.

## Frozen benchmark panel inherited from the director brief
- Primary slopes: `2`, `3/2`, `5/3`, `phi`, `sqrt(2)`, the plastic constant `rho`, the Salem number `sigma` given by the largest real root of `x^4 - x^3 - x^2 - x + 1`, and `e`.
- Low-slope sanity controls because the domain is `r > 0`: `1/2` and `phi - 1`.
- Recurrence orders: `d = 1, 2, 3, 4`.
- Moduli for shadow diagnostics: `2, 3, 5, 7, 11`.
- Prime-square follow-up modulus for any survivor: `25`.

## What is not allowed
- No arbitrary subsequence mining.
- No selector tuning after seeing a failure, except when the change is logged as a new hypothesis outside the frozen panel.
- No symbolic-dynamics substitution of the original question: linearly recurrent words, return words, or central sets are evidence only if they are explicitly mapped back to the numeric value sequence `floor(n_k r)`.
- No set-membership arguments that ignore ordering.

## Operational consequence
All later code, experiments, and theorem statements are interpreted through this lock: positive cases must be exact numeric recurrences on one of the approved selector schemas, and negative cases must specify which selector family they rule out.
