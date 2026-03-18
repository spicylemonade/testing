# Benchmark Gate

## Primary Gate

- Primary success metric: `exact_hit_rate` under matched seeds, matched restart counts, matched evaluation budgets, and the shared q/s representation.
- Reporting rule: every batch must also report `objective_evaluations`, `wall_seconds`, `restart_statistics`, terminal `correlation_defect_support_size`, `off_diagonal_gram_defect_support_size`, and `max_defect_magnitude`.
- Non-success rule: lower defect counts, smaller defect magnitudes, or nicer-looking traces do not count as solving Hadamard order `668` unless `exact_hit_rate` is nonzero.

## Canonical First Frontier Gate

The first frontier decision is made on the canonical order-`668` seed in `results/frontier/order_668_64m/seed_sequences.json`.

H1 may continue past the first matched frontier batch only if at least one of these is true:

1. `H1` achieves an exact hit under a matched budget when every non-CA baseline fails.
2. `H1` achieves a strictly higher exact-hit rate than the best matched non-CA baseline.
3. No method reaches exactness, but `H1` shows a clearly better near-exact trajectory on the same seed and same budget, with a lower terminal defect support and lower defect magnitude than every matched baseline across the run distribution rather than in one cherry-picked restart.

If none of these conditions holds, do not expand H1 beyond the first kill test.

## Stop Rules

Stop H1 on the canonical seed if any of the following happens under matched controls:

1. Plateau:
   - terminal `correlation_defect_support_size` stops improving for the final third of the budget on most restarts, or
   - the median terminal support is indistinguishable from the best non-CA baseline.
2. Diffusion:
   - support spreads to more nonzero lags without a compensating decrease in `max_defect_magnitude`, or
   - the final support/magnitude pair is worse than the best value reached earlier in the same run on most restarts.
3. Lost advantage:
   - a matched non-CA baseline equals or beats H1 on exact-hit rate, or
   - no method is exact and H1 fails to hold a strict median advantage on both terminal support and terminal magnitude.

## Secondary Readouts

These metrics are diagnostic only and cannot override the primary gate:

- defect support trajectory
- defect magnitude trajectory
- wall-clock time
- best restart trace
- alternate canonical fingerprints

They are useful for debugging or deciding whether failure is due to weak implementation, but they do not justify claims of success on order `668`.

## Branch Decision Rule

- `continue H1`: only if H1 survives the canonical first frontier gate above.
- `pivot to H2`: only if H1 fails for principled locality reasons, not because the baseline setup was unfair or the H1 implementation was obviously weak.
- `stop H3`: remains the default unless both H1 and H2 fail for representation reasons.
