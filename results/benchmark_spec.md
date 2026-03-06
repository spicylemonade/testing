# Benchmark Specification

## Scope

- All baseline controls use deterministic initial conditions with seed `42` where stochastic sampling would otherwise appear.
- Unless stated otherwise, formulas are written in normalized units with gravitational parameter `mu = G * (m1 + m2)` for relative two-body motion.
- Reporting tables must list the scenario id, `dt`, runtime, integrator path, softening policy, and whether the row is a pass or fail.

## Analytic Two-Body Controls

### 1. Circular Orbit Recovery

- Control quantity: circular speed
  - `v_c = sqrt(mu / r0)`
- Measured metric: radial RMS relative error
  - `err_r = rms(|r(t)| - r0) / r0`
- Pass threshold: `err_r <= 1e-2`
- Reporting unit: relative error

### 2. Elliptical Orbit Recovery

- Control quantities:
  - periapsis `r_p = a * (1 - e)`
  - apoapsis `r_a = a * (1 + e)`
- Measured metrics:
  - `err_rp = |r_p_hat - r_p| / r_p`
  - `err_ra = |r_a_hat - r_a| / r_a`
- Pass threshold: `err_rp <= 2e-2` and `err_ra <= 2e-2`
- Reporting unit: relative error

### 3. Period Recovery

- Control quantity:
  - `T = 2 * pi * sqrt(a^3 / mu)`
- Measured metric:
  - `err_T = |T_hat - T| / T`
- Pass threshold: `err_T <= 1e-2`
- Reporting unit: relative error

### 4. Escape Velocity Check

- Control quantity:
  - `v_esc = sqrt(2 * mu / r0)`
- Measured metrics:
  - classification correctness of bound versus unbound motion from the sign of specific orbital energy
  - `err_vinf = |v_inf_hat - v_inf| / max(v_inf, 1e-12)` for super-escape runs
- Pass threshold: classification must be correct and `err_vinf <= 5e-2` when `v_inf` is reported
- Reporting unit: boolean plus relative error

### 5. Orbital Element Recovery

- Derived quantities from relative state `(r, v)`:
  - specific angular momentum `h = r x v`
  - eccentricity vector `e_vec = (v x h) / mu - r / |r|`
  - eccentricity `e = |e_vec|`
  - semimajor axis `a = -mu / (2 * eps)` where `eps = |v|^2 / 2 - mu / |r|`
  - inclination `i = arccos(h_z / |h|)`
  - argument of periapsis `omega = atan2(e_y, e_x)` in planar controls
- Measured metrics:
  - `err_a = |a_hat - a| / a`
  - `err_e = |e_hat - e| / max(e, 1e-12)`
  - `err_i = |i_hat - i|`
  - `err_omega = wrapped_angle_distance(omega_hat, omega)`
- Pass threshold:
  - `err_a <= 2e-2`
  - `err_e <= 2e-2`
  - `err_i <= 1e-6` rad for planar controls
  - `err_omega <= 5e-2` rad
- Reporting unit: relative error for `a` and `e`, radians for `i` and `omega`

## Drift And Conservation Metrics

### 6. Total Energy Drift

- Formula:
  - `Delta_E_rel(t) = |E(t) - E(0)| / max(|E(0)|, 1e-12)`
- Long-horizon pass threshold: `max_t Delta_E_rel(t) <= 1e-2`
- Reporting unit: relative error

### 7. Angular Momentum Drift

- Formula:
  - `Delta_L_rel(t) = ||L(t) - L(0)|| / max(||L(0)||, 1e-12)`
- Long-horizon pass threshold: `max_t Delta_L_rel(t) <= 1e-2`
- Reporting unit: relative error

### 8. Center-of-Mass Drift

- Formulas:
  - `R_com(t) = sum_i m_i * r_i(t) / sum_i m_i`
  - `V_com(t) = sum_i m_i * v_i(t) / sum_i m_i`
  - `Delta_R_com(t) = ||R_com(t) - R_com(0)||`
  - `Delta_V_com(t) = ||V_com(t) - V_com(0)||`
- Pass threshold:
  - `max_t Delta_R_com(t) <= 1e-9`
  - `max_t Delta_V_com(t) <= 1e-9`
- Reporting unit: absolute normalized units and normalized velocity units

## Timestep Convergence Metrics

- For any observable `q(dt)` under timestep halving, report
  - `conv(dt_k -> dt_{k+1}) = ||q(dt_k) - q(dt_{k+1})||`
- Default observables:
  - final relative position for two-body controls
  - full-state snapshot at fixed horizon for three-body and small-N controls
  - `max_t Delta_E_rel(t)` and `max_t Delta_L_rel(t)`
- Pass criterion:
  - the finest-step run must improve or hold relative to the middle-step run for every reported observable
  - at least one observable must show a >= 2x reduction from coarse to fine `dt` for the analytic controls
- Reporting unit: scenario-native norm plus relative drift

## Required Reporting Units

- position and distance: normalized length units or SI meters, explicitly labeled
- velocity: normalized velocity units or SI meters per second, explicitly labeled
- time and period: normalized time units or seconds, explicitly labeled
- energies and angular momenta: scenario-native scalar values plus relative drift
- angles: radians

## Benchmark Pack To Execute Later

- circular two-body
- eccentric two-body ellipse
- period-recovery two-body orbit
- escape-velocity threshold sweep
- orbital-element recovery case
- figure-eight three-body choreography
- small-N central-mass ring
