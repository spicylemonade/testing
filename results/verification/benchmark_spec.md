# Benchmark Spec

## Audit Provenance

This audit was intended to use the `benchmark_auditor`, `explorer`, and `integrator` roles. A partial child artifact landed as `results/verification/benchmark_inputs_note.md`, but the full role round did not return the complete audit pack and local `codex exec` child launches were blocked by policy, so the audit below is the direct integrated review over the required local files plus that partial note.

## Approval Status

- Status: `approve_with_caveats`
- Scope of approval: the current non-CA baseline setup is fair enough to use as the matched control pack for the first frontier pilot.
- Non-approved interpretation: the current smoke batch is not evidence that any method is competitive on order `668`; it only validates that the baselines share one representation, one harness, and one accounting scheme before H1 is introduced.

## Seed Matching

- All four baselines read the same q/s seed-file format through `scripts/run_baseline.py`.
- The smoke run uses the same seed file for every method: `results/baselines/smoke_seed_n7_q3.json`.
- The frontier template in `results/baselines/README.md` points every baseline at the same canonical order-`668` seed file: `results/frontier/order_668_64m/seed_sequences.json`.
- This satisfies the seed-matching requirement as long as H1 is launched from the same seed file or a byte-for-byte copied q/s payload.

## Representation Control

- `hadamard_ca.search` uses one coordinate system for all four baselines: compact q/s sequences of common length `l`.
- The move basis is also shared: one packet flips one q-bit or one s-bit, so the neighborhood is identical across `greedy`, `tabu`, `simulated_annealing`, and `stochastic_hillclimb`.
- The shared objective comes from `hadamard_ca.harness.objective_summary(q, s)`, derived from the same `q, s -> (A, B, C, D)` map used for the recovered order-`668` frontier seed.
- This is sufficient representation control for the first frontier kill test. Any H1 comparison must stay inside the same q/s state space; otherwise any gain could come from the representation rather than from CA dynamics.

## Equal-Budget Accounting

- The current pilot configs all use the same explicit budget cap: `evaluation_budget = 80`.
- The current pilot configs all use the same restart count: `restart_count = 3`.
- The current pilot configs all use the same RNG seed: `seed = 17`.
- The shared restart diversification knob is also matched: `restart_packet_flips = 2`.
- Method-specific parameters (`tabu_tenure`, annealing temperature/cooling, stochastic sample size) change the move policy but do not change the accounting cap.
- Actual objective evaluations consumed before early stop are reported per run through the harness field `objective_evaluations`. This is the correct comparison field for later experiments, together with `wall_seconds`.

## Restart Comparability

- Every baseline uses the same restart index schedule and the same deterministic RNG seeding pattern `seed + restart_index`.
- Every baseline reports `restart_statistics` with requested restarts, completed restarts, and the best restart index.
- This is adequate for the first frontier pilot, but later result tables must report distributions across methods rather than only the best restart trace.

## Symmetry And Output Handling

- The harness reports a `canonical_fingerprint` for every terminal q/s state.
- Current canonicalization controls the shared q/s sign symmetries by minimizing over `(q, s)`, `(-q, s)`, `(q, -s)`, and `(-q, -s)`.
- This is enough to prevent trivial double-counting inside the present q/s representation.
- This is not a full Hadamard-equivalence canonicalization over row/column permutations or broader structured-family symmetries, so later novelty and family-leakage checks still need to stay explicit.

## Exact-Hit Reporting

- `exact_hit` is defined through the shared harness as zero nonzero correlation defects after the `q, s -> (A, B, C, D)` lift.
- The harness also reports `off_diagonal_gram_defect_support_size` and `max_defect_magnitude`, so exactness is not inferred from a soft proxy metric.
- `results/verification/harness_validation.md` confirms the harness on two solved controls (`l = 5`, `l = 7`) with exact-hit, zero correlation defects, and zero off-diagonal Gram defects.
- This exact-hit definition must remain the primary gate for H1. Lower defect counts alone do not count as success.

## Smoke-Run Readout

- `results/baselines/smoke_summary.md` shows that the four baselines all start from the same non-exact seed and reach exactness under the same shared budget/restart cap.
- The simulated-annealing run ends at a different canonical q/s fingerprint than the exhaustively recovered reference control, which is acceptable because the exact-hit test is representation-level exactness, not fingerprint matching to one exemplar.

## Blocking Caveats Before Frontier Runs

- The approved part is the benchmark scaffold, not the specific pilot budget `80`; frontier experiments must still lock one shared experiment config before execution.
- Only one smoke seed has been exercised so far. This is enough to validate the setup, not enough to support performance claims.
- H1 has not yet been implemented, so no CA-versus-baseline fairness claim should be made yet.
- The current fingerprint canonicalization is representation-local, not full Hadamard equivalence; if frontier runs generate multiple exact states, broader equivalence handling may be needed in later verification.

## Decision

Proceed to Phase 3 and the first H1 build, with these rules held fixed:

1. H1 must use the same q/s seed payload and the same evaluation-budget accounting.
2. Frontier experiments must compare methods under one locked shared budget and one locked restart policy.
3. Exact-hit rate remains the primary gate; near-exact improvements do not count as solving order `668`.
