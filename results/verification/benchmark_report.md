# Benchmark Report

## Verdict

- Verdict: partial support.
- The frozen matrix is disciplined and useful: 145 executed cases, 20 justified waivers, 10 exact recurrence cases, and the risky cases are downgraded to `prefix_fit`, `selector_shadow_failure`, or `sparse_subsequence_leak` instead of being promoted.

## Blockers

- The benchmark supports the H1 theorem core only in combination with the proof memo; by itself it is still a finite exact screen with `d <= 4` and 12-fit/20-holdout windows.
- The exact irrational lane is a single-selector phenomenon (`quadratic_convergent_even`), so the benchmark should not be read as a broad irrational-family theorem.

## Recommended Follow-Up

- Keep the external claim narrow: theorem-backed for arithmetic progressions and finite AP unions, experimental for sparse selectors.
- Use the beta-endpoint negative results as evidence against easy higher-degree extensions, not as a proof that every higher-degree Pisot mechanism fails.
