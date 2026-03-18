# Benchmark Report

## Verdict

- Fairness of benchmark design: `pass`
- Evidence that CA beats matched baselines: `fail`

## Supporting evidence

- `H1` used the same support representation, same phase schedule, same move cap, same step budget, and same verifier for CA and non-CA search.
- `H2` used the same start state, same variable family, same neighborhood, same step budget, and same verifier for CA and non-CA search.
- Negative controls were present in both branches.
- Equivalence-aware orbit accounting was recorded in the run artifacts.

## Failure points

- `H1`:
  - `direct_greedy` beats `parallel_gain_ca` on both the solved control and the exact target.
- `H2`:
  - the toy ladder is not decisive because random controls also solve most starts;
  - the real order-`668` attempt ties exactly on the decisive metrics.

## Residual risks

- The `H2` toy ladder is small and should not be oversold.
- Reserve branches still need matched baselines of their own before they can inherit this benchmark packet.

## Recommendation

Keep the current benchmark packet as the standard for any follow-on branch, and stop the present CA branches.
