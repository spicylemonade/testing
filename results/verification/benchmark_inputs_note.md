# Benchmark Inputs Note

This note summarizes the current non-CA baseline setup that feeds `item_009` of `research_rubric.json`.

## Seed Matching

- `scripts/run_baseline.py` loads one JSON seed file and passes the same `q` / `s` arrays into `hadamard_ca.harness.run_harness(...)` for every baseline.
- The current matched smoke batch uses `results/baselines/smoke_seed_n7_q3.json`, a single non-exact perturbation of the exact length-`7` control.
- `results/baselines/README.md` also fixes the frontier launch template to the canonical recovered order-668 seed at `results/frontier/order_668_64m/seed_sequences.json`, which exposes the same `q` / `s` keys.

## Representation Control

- All four baselines operate in the same compact q/s coordinate system used by the recovered order-668 frontier seed, not on a raw `668 x 668` sign matrix.
- `hadamard_ca.search.apply_packet(...)` defines one shared move basis: flip one entry of `q` or one entry of `s`.
- `hadamard_ca.harness.derived_quadruple(...)` maps every method output through the same deterministic `q,s -> (s, s', sq, (sq)')` construction before scoring or certification.

## Evaluation-Budget Accounting

- Each baseline config in `results/baselines/*.json` sets the same `evaluation_budget = 80`, `restart_count = 3`, and `seed = 17` for the smoke batch.
- `hadamard_ca.search._search_over_restarts(...)` enforces a global evaluation cap across restarts by passing each restart only the remaining budget.
- `hadamard_ca.harness.run_harness(...)` reports the consumed total as `objective_evaluations`.
- Concrete smoke outputs in `results/baselines/smoke_runs/*.json` show the same budget ceiling with method-specific early stopping once an exact hit is found.
- Implementation caveat: the search layer scores the initial state before the restart loop and each runner scores its restart start state again, so the accounting is consistent across methods but not minimal.

## Restart Policy

- Restart behavior is centralized in `hadamard_ca.search._restart_state(...)`.
- Restart `0` uses the seed unchanged. Later restarts deterministically apply `restart_packet_flips` random packet flips using RNG seed `config.seed + restart_index`.
- The shared smoke configs set `restart_packet_flips = 2` for all methods, while method-specific metadata only affects the internal move policy (`tabu_tenure`, annealing schedule, sampled packet count).
- Restart completion and the best restart index are surfaced in `restart_statistics`.

## Symmetry And Canonical Fingerprints

- The harness computes one `canonical_fingerprint` for every terminal state using `hadamard_ca.harness.canonical_fingerprint(...)`.
- Current canonicalization only quotients by independent global sign flips of `q` and/or `s`.
- No cyclic shift, reversal, block permutation, or broader Goethals-Seidel symmetry is canonicalized at this stage.
- The smoke summary already demonstrates why exact-hit status must be separated from fingerprint equality: simulated annealing reaches `exact_hit: true` with a different canonical fingerprint than the exhaustively recovered reference control.

## Exact-Hit Reporting

- `hadamard_ca.harness.evaluate_state(...)` sets `exact_hit` when the derived combined aperiodic correlation coefficients have zero nonzero off-origin entries.
- The harness reports both correlation-level and full Gram-level defect summaries: `correlation_defect_support_size`, `off_diagonal_gram_defect_support_size`, `max_defect_magnitude`, `defect_histogram`, and `objective_summary`.
- `results/verification/harness_validation.md` shows that the same interface certifies two exact controls (`l = 5` and `l = 7`) to zero correlation and zero off-diagonal Gram defect.
