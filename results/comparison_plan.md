# Comparison Plan

## Comparator Roster

### Trusted Reference

- `REBOUND` with `IAS15`
  - Role: high-accuracy external reference for 2-body, 3-body, and small-N matched scenarios.
  - Why frozen now: it is the strongest trusted neighbor surfaced in Phase 1 and already constrains any claim of integrator novelty or large-N novelty.

### Lightweight / Educational Baselines

- `poliastro` numerical propagation
  - Role: accessible astrodynamics-library baseline for the analytic two-body controls.
  - Scope: circular orbit, ellipse, period, escape velocity, and orbital-element recovery only.

- `explicit_euler_classroom`
  - Role: in-repo classroom and hobby baseline representing the educational branch that prioritizes intuitive implementation over audit discipline.
  - Scope: 2-body, 3-body, and small-N scenarios using the same ordered JSON scenarios as the reference kernel.

## Matched Initial Conditions

- Canonical scenario bundle:
  - `scenarios/circular_two_body.json`
  - `scenarios/figure_eight_three_body.json`
  - `scenarios/small_n_ring.json`
- All baselines must read or derive from the same body ordering, masses, positions, velocities, `G`, and nominal `dt` family.
- For `poliastro`, the mutual two-body scenarios are reduced to the equivalent relative orbit with `mu = G * (m1 + m2)` and then reconstructed back into relative-state outputs for comparison.

## Timestep Policies

- Fixed-step grid for audit experiments:
  - coarse: `dt = 0.02`
  - medium: `dt = 0.01`
  - fine: `dt = 0.005`
- If a scenario uses a smaller native `dt`, the grid scales by halves around the native value instead of violating stability by rounding upward.
- `REBOUND IAS15` may use internal adaptive substeps, but outputs must be sampled on the same saved times as the fixed-step runs.
- `explicit_euler_classroom` must use the same fixed `dt` values as the reference kernel with no hidden adaptivity.

## Frozen Output Variables

- `time`
- body positions and velocities in scenario order
- relative-state errors for analytic two-body controls
- total energy
- angular-momentum norm
- center-of-mass position and velocity
- minimum pair distance and identity
- wall-clock runtime for the physics step loop only

## Frozen Reporting Tables

- `analytic_controls_table`
  - scenario, `dt`, comparator, radius/period/escape/orbital-element errors, pass/fail
- `drift_table`
  - scenario, `dt`, comparator, max energy drift, max angular-momentum drift, max center-of-mass drift, pass/fail
- `runtime_table`
  - scenario, `dt`, comparator, simulated steps, acceleration evaluations if available, wall-clock seconds
- `comparison_narrative`
  - concise prose on where the audited kernel wins, ties, or loses against REBOUND, poliastro, and the classroom baseline

## Frozen Interpretation Rules

- Wins are allowed only on auditability, reproducibility clarity, or close-encounter honesty; not on raw accuracy versus `IAS15`.
- Ties are allowed when the reference kernel matches REBOUND within tolerance on the frozen metrics.
- Losses are expected for coarse `dt` or stiff close encounters and must be documented rather than hidden.
