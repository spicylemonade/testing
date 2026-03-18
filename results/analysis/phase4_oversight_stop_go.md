# Phase 4 Oversight And Stop/Go Review

Prepared for rubric `item_020`.

## Oversight checkpoints

### Checkpoint 1: `H1` control and target sweep

- Scope reviewed:
  - `results/experiments/h1_control_sweep.json`
  - `results/experiments/h1_target_sweep.json`
  - `results/analysis/phase2_baseline_review.md`
  - `results/analysis/experiment_readout.md`
- Fairness status: pass.
  - CA and non-CA methods used the same support representation, the same odd-cycle phase schedule, the same accepted-move cap per phase, the same step budget, and the same verifier.
  - Negative controls were present through `random_rule_ca` and `random_walk`.
- Auditability note:
  - the fairness lock is explicit in `results/analysis/baseline_benchmark_sheet.md` and in the code paths for `hadamard668/h1.py`, but the H1 raw JSON does not serialize every fairness parameter symmetrically for CA and non-CA runs, so the benchmark sheet and code remain part of the load-bearing evidence.
- Decision: `stop` on `H1`.
  - `direct_greedy` beats `parallel_gain_ca` on both the solved control and the unresolved target.
  - The branch therefore fails the registered go gate before any broader search is justified.

### Checkpoint 2: `H2` promotion and order-`668` attempt

- Promotion condition status:
  - `H2` was opened only after `H1` failed its registered gate.
- Scope reviewed:
  - `results/experiments/h2_ladder.json`
  - `results/experiments/h2_seed_attempt.json`
  - `results/analysis/h2_design_brief.md`
  - `results/analysis/experiment_readout.md`
- Fairness status: pass.
  - The real `668` attempt fixed `q`, searched only by local `s` flips, and used the same seed, same variable family, same budget, and same verifier for CA and non-CA methods.
  - Negative controls were present and clearly worse, which helps confirm the verifier is not degenerate.
- Reproduction note:
  - a fresh scratch-space `python3 -m hadamard668.experiments run-all` reproduction matched all canonical non-timing summary aggregates exactly, so the decisive stop/go metrics are stable.
- Decision: `stop` on `H2`.
  - The toy ladder does not kill `H2`, but it also does not support a positive claim because random controls solve most starts.
  - The real order-`668` attempt is decisive and yields an exact tie between `parallel_gain_ca` and `direct_greedy`.

## Stop/Go summary

- `H1`: `stop`
- `H2`: `stop`
- `Reserve concepts`: `no-go for promotion in this run`

## Governance conclusion

The oversight review supports a hard stop on the implemented CA program. Any continuation must be recorded as a new branch rather than as an extension of the present rule families, and any rerun of `run-all` should be treated as a reproducibility check rather than as evidence that the historical branch-promotion chronology changed.
