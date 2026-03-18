# Benchmark Report

Snapshot date: 2026-03-18 UTC

## Scope

This report audits the blocked phase-4 pass recorded in:

- `results/experiments/h1_tiny_grid_report.md`
- `results/experiments/h1_controls.md`
- `results/experiments/complexity_sweep.md`
- `results/verification/verification_summary.md`
- `results/core/lane_gates.md`

The required specialist roles for this checkpoint were launched:

- `monitor`
- `benchmark_auditor`
- `falsifier`
- `integrator`

The first waits on those threads timed out. Their final short memos were then recovered on close and synthesized with the blocker artifacts below.

## Audit Verdict

- Benchmark integrity for the blocked pass: `pass`
- Experimental execution readiness: `fail`

The pass verdict means the run preserved compute parity and negative results honestly while blocked. The fail verdict means no actual benchmark comparison could be executed without an exact verifier.

## Matched Budgets

Pass.

- The planned first-gate budget remained explicit: at most `3` H1 families and at most `10^3` exact decodes per family.
- The spent budget was also explicit: `0 / 3` families and `0` exact decodes.
- No CA baseline, non-CA baseline, decoder-matched baseline, or complexity regime was allowed to consume hidden extra compute under proxy metrics.

## Identical Decoder Usage

Blocked operationally, parity preserved.

- No exact decoder or verifier was available for any method.
- Therefore no method received privileged decoder access and no method was evaluated under a weaker or different decoder.
- The run preserved parity by refusing proxy decoder usage, but true decoder-parity testing remains impossible until a shared exact decoder exists.

## Full Score Accounting

Pass.

- The exact score formula `(m(G)+|R|)/(n(G)-|T|)` was preserved as the only admissible objective.
- No proxy score, modular surrogate, local-density score, or repaired witness score was substituted.
- Empty score distributions in the experiment reports are therefore a sign of accounting discipline, not missing bookkeeping.

## Negative-Result Preservation

Pass.

- `results/experiments/h1_tiny_grid_report.md` records the blocked run directly instead of implying a weak positive.
- `results/experiments/h1_controls.md` reports empty control distributions rather than invented collapse claims.
- `results/experiments/complexity_sweep.md` records blocked regimes and retains the bounded-slope and modular-mirage rejection rules.

## Audit Findings

1. `benchmark_auditor`: matched budgets, exact score accounting, and negative-result preservation all pass; the benchmark phase is an integrity pass, not an execution pass.
2. `falsifier`: wording must stay strict. The safe formulation is `integrity pass; execution blocked`, not `benchmark pass` in an unqualified sense.
3. `monitor`: the recorded operational state is consistent everywhere: `0 / 3` H1 families, `0 / 10^3` exact decodes, `0` promoted families, and later phases correctly kept closed.
4. `integrator`: compute parity is documented rather than exercised. No empirical superiority, robustness, or decoder-matched fairness claim is supported yet.
5. The main unresolved risk is infrastructure, not reporting integrity: there is still no exact integer verifier.
