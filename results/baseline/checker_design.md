# Exact Checker Design

## Exact arithmetic choices
- Slopes are represented as exact SymPy objects: rationals, quadratic radicals, algebraic `RootOf` objects, or `E`.
- Sequence values are computed as exact integers via `floor(n * r)`, never by floating-point fitting.
- Candidate recurrences are found by exact rational nullspace calculations on Hankel-style relation matrices.

## Output policy
- A relation found on the tested prefix is reported as a `candidate_recurrence` with integer coefficients and verified windows.
- A case is promoted to `exact_recurrence` only when the checker also has a structural infinite certificate.
- In the current baseline, the implemented structural certificate is the rational arithmetic-progression identity: if `r = p/q` and the selector step is divisible by `q`, then the sampled values are exactly an arithmetic progression.

## What the smoke run proves
- `results/baseline/baseline_smoke.json` recovers the rational baseline for `3/2` and `5/3` with the expected order-2 relation `x_k - 2 x_{k+1} + x_{k+2} = 0`.
- The same smoke run also records an uncertified low-order fit for `phi` on Fibonacci indices and labels it `finite_prefix_fit_insufficient`, which is the required guard against overclaiming from exact-but-unproved prefix behavior.
