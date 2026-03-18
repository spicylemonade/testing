# H1 Branch Brief: Defect-Syndrome CA on the 64-Modular Order-668 Seed

## Scope

`H1_defect_syndrome_ca_64m` is the champion branch for the first seeded order-668 kill test. The implementation lives in `hadamard_ca/h1_ca.py` and is launched through `scripts/run_h1_ca.py`.

The branch claim stays narrow:

- state is the compact q/s representation plus a compressed defect field, not a raw `668 x 668` sign lattice
- search starts from the canonical recovered 2025 `64`-modular seed
- success means exact orthogonality under the shared harness, not a nicer defect trace

## Compressed State Representation

The implemented CA uses two coupled compressed objects:

1. A sparse lag-syndrome field over the combined aperiodic autocorrelation coefficients.
   - `coefficients = correlation_coefficients(q, s)`
   - active defect cells are the nonzero off-origin lags
   - the working lag neighborhood is an expanded mask around active lags, controlled by `lag_neighborhood_radius`

2. A two-channel packet lattice of length `l`.
   - channel 0: `q[i]` packet cells
   - channel 1: `s[i]` packet cells
   - each packet corresponds to one admissible sign flip in the shared q/s coordinates

This is smaller than the explicit order-668 matrix. For the frontier seed, the operative state is `166` off-origin lag cells plus `334` packet cells instead of `668 x 668` matrix entries.

## Local Update Rule

One asynchronous CA step is:

1. Compute the current lag-syndrome field.
2. Build a lag mask around the active defect support.
3. For every packet cell, compute an exact single-packet defect delta restricted to the active lag mask.
   - `q[i]` packets only perturb the `sq` and `sq'` channels.
   - `s[i]` packets perturb `s`, `s'`, `sq`, and `sq'`.
4. Convert those deltas into a raw local pressure score by summing weighted absolute-defect improvement over the masked lag cells.
5. Couple packet pressures through a local neighborhood:
   - same-channel neighbors within `packet_neighborhood_radius`
   - opposite-channel packet at the same index
   - refractory penalty on recently fired packets
6. Select local maxima above `activation_threshold`, with a cap `max_active_packets`.
7. Apply the selected packet flips, recompute the exact shared objective, and continue until exactness, stagnation, or budget exhaustion.

The implemented search is therefore not a raw matrix CA. It is a packet-lattice automaton driven by a sparse lag-syndrome field.

## Neighborhood

- Lag neighborhood:
  - controlled by `lag_neighborhood_radius`
  - only defect cells near the active support contribute to packet pressure
- Packet neighborhood:
  - same-channel coupling on a periodic 1D ring over q-packets or s-packets
  - cross-channel coupling between `q[i]` and `s[i]`
- Refractory neighborhood:
  - recently fired packets are temporarily penalized through `refractory_steps` and `refractory_penalty`

## Conserved Quantities

The implementation keeps the following invariants fixed across the branch:

- q/s length remains fixed
- packet alphabet remains binary (`+1/-1`)
- the prime-involution lift `q, s -> (s, s', sq, (sq)')` is fixed
- packet-graph topology is fixed for the chosen q/s length

## Seed Loading

- Seed loader: `hadamard_ca.h1_ca.load_h1_seed(...)`
- Canonical frontier seed: `results/frontier/order_668_64m/seed_sequences.json`
- Shared smaller control seed used for smoke validation: `results/baselines/smoke_seed_n7_q3.json`

## Instrumentation

The H1 search metadata records:

- `branch_id`
- `representation`
- `pressure_update_mode`
- `ca_field_evaluations`
- `conserved_quantities`

This keeps later runtime audits from confusing cheap CA field updates with the harness-level `objective_evaluations` counter.

## Initial Smoke Readout

Two direct smoke checks were run before freezing this brief:

- On `results/baselines/smoke_seed_n7_q3.json`, H1 reaches exactness with `13` shared-harness objective evaluations.
- On a very small frontier pilot (`40` evaluation budget, `1` restart), H1 runs cleanly but does not improve the canonical order-668 seed yet.

That is enough to confirm the branch is executable. It is not enough to claim competitive behavior on order `668`; the matched control and frontier experiments remain Phase 4 work.
