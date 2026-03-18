# Runtime Benchmark Note

Status: `item_018` is not yet satisfied.

Scope: reviewed `item_018`, `results/verification/benchmark_spec.md`, `results/verification/benchmark_gate.md`, `results/experiments/controls/summary.json`, all 10 control run JSONs, `results/experiments/order_668_64m/summary.json`, and all 5 order-668 run JSONs.

## Confirmed

- All 15 expected run JSONs exist. Every run includes `seed_file`, `seed_length`, `config`, `restart_statistics`, `objective_evaluations`, `wall_seconds`, defect summaries, `canonical_fingerprint`, and a non-empty `trace`.
- `results/experiments/controls/summary.json` matches the raw runs on `exact_hit`, terminal support, `objective_evaluations`, `wall_seconds`, and `canonical_fingerprint`.
- `results/experiments/order_668_64m/summary.json` matches the raw runs on `exact_hit`, `objective_evaluations`, `wall_seconds`, `completed_restarts`, and the per-restart terminal objectives recoverable from each trace.
- Canonical output reporting is present everywhere. The order-668 batch reports one shared best-seen fingerprint with no method beating the seed objective. Exact control hits have zero correlation and zero Gram defects, with the already-acknowledged alternate exact fingerprint on `control_n5_q0:simulated_annealing`.

## Gaps

- The traces are not evaluation-complete. Examples: order-668 `greedy` has `2` trace points for `80` objective evaluations, `simulated_annealing` `2/80`, `tabu` `3/80`, and `control_n5_q0:greedy` `5/34`. These are sparse snapshots, not replayable runtime logs.
- Several raw runs do not end on the reported top-level output. `control_n5_q0:H1_defect_syndrome_ca_64m` is `exact_hit=true`, but its last trace point is still `(support 1, l1 4, max_abs 4)`. On order `668`, H1's top-level output remains the seed/best state while the three restart terminals are `(33,2368,384)`, `(40,2356,408)`, and `(23,2216,384)`. The run JSON top level is therefore `best_over_run`, not terminal output.
- Restart policy is matched only at the requested-config level. Every run requests `restart_count=3`, but executed restarts differ: order-668 `greedy`, `tabu`, and `simulated_annealing` complete `1/3`, and `control_n5_q0:tabu` completes `2/3`. This is logged, but it weakens any claim of matched restart coverage.
- Seed/config provenance is not closed for rerun certification. The artifacts store seed paths, seed lengths, and embedded parameter values, but no seed hash, config checksum or config path pointer, and no code revision.

## Decision

- No control artifact is missing, so the batch is not invalidated by absent control data.
- Keep `item_018` open. The pack is good enough for a coarse benchmark readout, but it does not support the stronger acceptance claim that runtime logs, restart evidence, and provenance are complete for every reported run.

## Minimum Repair

- Add explicit per-restart terminal records and an `output_semantics` field such as `best_over_run` versus `terminal_last_restart`.
- Add seed, config, and code digests to every run JSON.
- Emit either evaluation-complete traces or a clearly labeled sampled-trace schema.
