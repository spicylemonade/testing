# Harness Interface

The shared evaluation entry point is `hadamard_ca.harness.run_harness(method, initial_q, initial_s, config)`.

Expected method contract:

- Input:
  - `initial_q`, `initial_s`: binary length-`l` sequences in the same compact q/s coordinate system used for the recovered order-668 frontier seed.
  - `config`: `SearchConfig(method_name, evaluation_budget, restart_count, seed, metadata)`.
- Output:
  - `SearchResult(q, s, evaluations, completed_restarts, restart_statistics, metadata, best_objective, trace)`.

Metrics computed by the harness from the same interface for every method:

- `exact_hit`
- `correlation_defect_support_size`
- `off_diagonal_gram_defect_support_size`
- `max_defect_magnitude`
- `defect_histogram`
- `wall_seconds`
- `objective_evaluations`
- `restart_statistics`
- `canonical_fingerprint`
- `objective_summary` (`support_size`, `l1`, `max_abs`)

Validation status:

- `results/controls/exact_controls.json` contains two exact smaller controls found by exhaustive search in the same q/s coordinate system (`l = 5` and `l = 7`).
- `results/verification/harness_validation.md` records the validation runs.
- Both controls validate to `exact_hit: True`, zero correlation-defect support, zero off-diagonal Gram defects, and zero max defect magnitude.
