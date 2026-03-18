# Benchmark Spec

## Scope

This benchmark contract covers the current non-CA baselines in `hadamard_ca/search.py`:

- `greedy`
- `tabu`
- `simulated_annealing`
- `stochastic_hillclimb`

All four methods are launched through `scripts/run_baseline.py` and evaluated only through `hadamard_ca.harness.run_harness(...)`.

## Shared Seed / Representation Rules

- Every matched batch must use the same q/s seed file format: a JSON object with compact length-`l` arrays `q` and `s`.
- Every matched batch must reuse the same exact seed file path across all methods.
- The current smoke batch uses `results/baselines/smoke_seed_n7_q3.json`.
- The canonical frontier seed for later order-668 runs is `results/frontier/order_668_64m/seed_sequences.json`.
- All baselines operate in the same compact q/s coordinate system and the same packet basis: one packet equals one sign flip in either `q[i]` or `s[i]`.
- No baseline may switch to a different search representation, act directly on the explicit `668 x 668` sign matrix, or use family-specific parameterizations unavailable to the CA branch.

## Accounting Rules

- A matched batch must share the same:
  - `evaluation_budget`
  - `restart_count`
  - `seed`
  - `metadata.restart_packet_flips`
- The current pilot configs in `results/baselines/*.json` use:
  - evaluation budget `80`
  - restart count `3`
  - RNG seed `17`
  - restart perturbation `2`
- Method-specific hyperparameters are allowed only inside method metadata and must be recorded with the result file:
  - `tabu_tenure`
  - `initial_temperature`
  - `cooling`
  - `sample_size`
- Fairness is enforced by a shared evaluation cap, not by forcing every method to consume the same number of evaluations. Early exit on exact hit is allowed and must remain visible in `objective_evaluations`.
- Non-blocking caveat: the current restart wrapper reevaluates the start state once per restart and counts that evaluation. This accounting is consistent across the four baselines, so it does not break within-batch fairness for the present study.

## Restart Rules

- Restart `0` must use the unmodified input seed.
- Restarts `1..R-1` must be derived only through the shared deterministic restart rule in `hadamard_ca.search._restart_state(...)`.
- The restart RNG is tied to `config.seed + restart_index`.
- `restart_packet_flips` must match across all methods in a compared batch.
- `restart_statistics` must be saved for every run and include requested restarts, completed restarts, and best restart index.

## Symmetry / Output Rules

- Reporting uses the harness `canonical_fingerprint`, which identifies q/s states up to independent global sign flips of `q` and `s`.
- Fingerprint equality is a reporting aid only. It is not the success criterion.
- All reported runs must save:
  - `method_name`
  - `objective_evaluations`
  - `restart_statistics`
  - `objective_summary`
  - `defect_histogram`
  - `canonical_fingerprint`
  - `exact_hit`
  - `config`
  - `seed_file`

## Exact-Hit Rule

- `exact_hit` is `True` if and only if the nonzero-lag correlation-defect support is zero in the shared q/s harness.
- Off-diagonal Gram-defect metrics remain required, but they are secondary diagnostics rather than the primary success definition.
- Defect-count-only improvement does not count as success.
- `results/verification/harness_validation.md` validates the harness on exact smaller controls.
- `results/baselines/smoke_summary.md` verifies that the four baselines all use the same exactness interface on one shared non-exact control seed; simulated annealing reaches exactness through a different exact fingerprint, which is acceptable because exactness is not defined by fingerprint matching.

## Frontier Go / No-Go Status

Audit status: **Approve** for Phase 3 implementation work and for planning the first matched order-668 kill test.

Reason:

- seed matching is explicit
- representation parity is explicit
- evaluation-budget accounting is shared
- restart policy is shared
- symmetry handling is documented
- exact-hit reporting is independent of a single reference fingerprint

Boundary:

- **Go** for implementing and prechecking `H1_defect_syndrome_ca_64m`.
- **Go** for the first seed-matched order-668 kill test once the stop-rule gate in `results/verification/benchmark_gate.md` exists.
- **No-go** for broad frontier sweeps or claims of advantage before `item_010` defines the gate metrics and `item_016` logs matched control experiments under the same accounting.
