# Final Package Draft

## Claim

### Theorem-backed
- Rational cases come first. If `r = p/q`, the arithmetic-progression selector `n_k = kq` gives `b_k = floor(kq r) = kp`, so every rational `r > 0` is already a positive value-recurrence case.
- In the proved eventually-periodic-gap lane - concretely, arithmetic progressions and finite unions of arithmetic progressions - exact value recurrence occurs if and only if `r` is rational.

### Empirical
- In the frozen sparse panel, the only exact-certified irrational ordered value sequences are the `quadratic_convergent_even` cases for `phi - 1`, `phi`, `sqrt(2)`, and `1 + sqrt(2)`.
- The revision follow-up runs all 15 `uncertified_exact_holdout` rows to length `320`: `salem_quartic / ost_suffix_001` fails by `80`, while the remaining long exact leaks stay empirical only.

### Scope discipline
- No family-level claim is carried forward for quadratics, periodic continued fractions, or zero intercept.
- The failed higher-degree Pisot lane is used only as a falsifier outcome, not as evidence for a positive theorem.

## Support

### Theorem-backed
- The package is about value recurrence of the ordered integer sequence `b_k = floor(n_k r)`, not symbolic word recurrence of a mechanical or Sturmian gap word.
- The package is also about ordered subsequences `n_0 < n_1 < ...`, not unordered Beatty sets `{floor(nr) : n >= 1}`.
- For arithmetic progressions and finite-union selectors, an exact constant-coefficient recurrence for `b_k` would force eventual periodicity of the bounded first-difference sequence, while the corresponding irrational rotation codings are not eventually periodic.

### Empirical
- Across the frozen matrix, the AP/FUAP rows yield 28 exact cases, all rational.
- The only sparse exact-certified cases are the 4 `quadratic_convergent_even` identities.
- The 15 `uncertified_exact_holdout` rows split into 11 persistent leaks and 4 broken cases under the 320-term revision follow-up; none is upgraded to theorem status.
- The tested higher-degree Pisot, Salem, and transcendental controls do not produce any exact certificate in the current frozen constructions.

### Scope discipline
- Prefix fits, modular-shadow survivors, and finite exact holdout survival do not count as theorem claims.
- The package separates proved exact identity, exact-certified examples, and empirical leakage cases, and it should stay that way in any outward-facing version.

## Limitations

- No theorem is claimed for arbitrary subsequences, sparse selectors in general, symbolic linear recurrence, or unordered Beatty-set embeddings.
- The sparse irrational cases remain experimental: they are limited to the current selector family, search range, recurrence orders, and exact holdout windows.
- Stronger sparse-lane claims would still need intercept controls, continued-fraction-prefix-matched nonquadratic controls, and infinite certificates for the surviving leaks.
