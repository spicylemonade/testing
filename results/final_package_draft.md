# Final Package Draft

## Claim

### Theorem-backed
- Rational cases come first. If `r = p/q`, the arithmetic-progression selector `n_k = kq` gives `b_k = floor(kq r) = kp`, so every rational `r > 0` is already a positive value-recurrence case.
- In the proved eventually-periodic-gap lane - concretely, arithmetic progressions and finite unions of arithmetic progressions - exact value recurrence occurs if and only if `r` is rational.

### Empirical
- In the frozen zero-density panel, the only irrational ordered value sequences that survive the package's exact finite holdout protocol are the `quadratic_convergent_even` cases for `phi`, `sqrt(2)`, and `1 + sqrt(2)`.

### Conjectural
- The sparse irrational survivor mechanism looks periodic-continued-fraction / quadratic rather than broadly Pisot, but that refinement is not claimed as a theorem.

## Support

### Theorem-backed
- The package is about value recurrence of the ordered integer sequence `b_k = floor(n_k r)`, not symbolic word recurrence of a mechanical or Sturmian gap word.
- The package is also about ordered subsequences `n_0 < n_1 < ...`, not unordered Beatty sets `{floor(nr) : n >= 1}`.
- For arithmetic progressions and finite-union selectors, an exact constant-coefficient recurrence for `b_k` would force eventual periodicity of the bounded first-difference sequence, while the corresponding irrational rotation codings are not eventually periodic.

### Empirical
- Across the frozen matrix, positive-density families yield 7 exact cases, all rational.
- Zero-density families yield 3 exact cases, all from the single selector `quadratic_convergent_even`.
- Prefix fits, modular-shadow survivors, and floating approximations do not count as claims. Finite exact holdout survival is stronger than approximation, but still weaker than a proved infinite identity.
- The tested higher-degree Pisot, Salem, and transcendental controls do not produce exact survivors in the current frozen constructions.

### Conjectural
- The failed higher-degree Pisot lane supports using Pisot as a falsifier target, not as the basis for a positive theorem.

## Limitations

- No theorem is claimed for arbitrary subsequences, zero-density selectors in general, symbolic linear recurrence, or unordered Beatty-set embeddings.
- The sparse irrational cases remain experimental: they are limited to the current selector family, search range, recurrence orders, and exact holdout windows.
- No approximation claim is being made. The package separates proved exact identity, finite exact evidence, and conjecture, and it should stay that way in any outward-facing version.
