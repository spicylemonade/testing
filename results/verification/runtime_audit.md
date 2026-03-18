# Runtime Audit

## Scope

This audit covers every reported run in the two matched experiment batches:

- controls: `results/experiments/controls/runs/`
- canonical frontier: `results/experiments/order_668_64m/runs/`

The direct inventory is recorded in `results/verification/runtime_inventory.json`.
Specialist side notes used during this audit:

- `results/verification/runtime_benchmark_note.md`
- `results/verification/runtime_monitor_note.md`
- `results/verification/runtime_integrator_note.md`

## Completeness Check

- Audited run count: `15`
  - controls: `10`
  - frontier: `5`
- Required top-level fields checked on every run:
  - `method_name`
  - `order`
  - `seed_length`
  - `exact_hit`
  - `correlation_defect_support_size`
  - `off_diagonal_gram_defect_support_size`
  - `max_defect_magnitude`
  - `objective_summary`
  - `wall_seconds`
  - `objective_evaluations`
  - `restart_statistics`
  - `canonical_fingerprint`
  - `metadata`
  - `best_objective`
  - `trace`
  - `seed_file`
  - `config`
- Result: `15/15` runs contain every required field. No run is missing seed provenance, config provenance, runtime accounting, restart accounting, canonicalized output, or trace payload.

## Batch Readout

- Control batch:
  - Every run points to one of the two locked seed files under `results/experiments/controls/seeds/`.
  - Wall-clock range: `0.0341s` to `0.0824s`.
  - Objective-evaluation range: `10` to `80`.
  - Trace-length range: `5` to `40`.
- Frontier batch:
  - Every run points to `results/frontier/order_668_64m/seed_sequences.json`.
  - Wall-clock range: `0.0789s` to `2.1292s`.
  - Objective-evaluation range: `26` to `80`.
  - Trace-length range: `2` to `31`.

## Restart Accounting

- Partial restart completion is present in the logs and is not missing data.
- Control runs that completed fewer than the requested `3` restarts:
  - `results/experiments/controls/runs/control_n5_q0/tabu.json` completed `2/3` because the shared `80`-evaluation budget was exhausted.
  - `results/experiments/controls/runs/control_n7_q0/simulated_annealing.json` completed `1/3` for the same reason.
- Frontier runs that completed fewer than the requested `3` restarts:
  - `results/experiments/order_668_64m/runs/greedy.json` completed `1/3`.
  - `results/experiments/order_668_64m/runs/tabu.json` completed `1/3`.
  - `results/experiments/order_668_64m/runs/simulated_annealing.json` completed `1/3`.
- H1 and `stochastic_hillclimb` completed `3/3` restarts on the frontier batch because their runs stopped earlier within each restart and therefore stayed below the shared evaluation cap longer.

## Trace And Output Consistency

- Every audited run has a non-empty trace.
- The baseline traces record accepted-state snapshots along the shared q/s search path rather than evaluation-complete logs.
- The H1 traces additionally record CA-specific fields such as `step`, `active_packets`, and `active_lag_count`; this is a method-specific extension, not a mismatch in the audit contract.
- The run top level is `best_over_run`, not `trace[-1]` terminal state. For per-restart terminal auditing, use `restart_statistics` together with restart-segmented trace entries rather than the overall trace tail.
- Every run records a `canonical_fingerprint`, and every fingerprint is a `64`-hex-character digest.
- Control-batch fingerprints show both exact-solution agreement and legitimate alternate exact outputs.
- Frontier-batch fingerprints all resolve to the canonical seed representative as the best recorded state, which is consistent with the item 017 kill-test summary in `results/experiments/order_668_64m/summary.md`.

## Verdict

- Runtime evidence is complete for every reported run in both batches.
- Caveat: the saved traces are sampled raw logs of accepted states, not evaluation-complete replay logs, and the top-level output semantics are `best_over_run`. Those limitations do not remove any field required by item `018`, but they should remain explicit in later verification writing.
- Missing control data does not invalidate the batch because no control run is missing required fields; the only irregularity is budget-limited partial restart completion, and that condition is explicitly recorded in `restart_statistics` and `objective_evaluations`.
- Item `018` acceptance is satisfied: logs, seeds, restart counts, wall-clock time, objective evaluations, and canonicalized outputs are all present and auditable.
