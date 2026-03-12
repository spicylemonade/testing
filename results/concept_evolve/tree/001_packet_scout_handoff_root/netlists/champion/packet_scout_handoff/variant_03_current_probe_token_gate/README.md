# Variant 03: Current-Probe Token Gate

- Role: helper-free probe and handoff variant
- Source inference:
  - use a comparatorless switched-cap current probe and infer deliverability from the resulting voltage delta
- Minimum-energy accumulation:
  - feed the shared startup reservoir with a fixed packet train while the probe logic remains active only long enough to keep the ranking stable
- Handoff gating:
  - use a token integrator so the main arbiter is released only after sustained energy surplus rather than a single threshold crossing
- Dependency list:
  - `netlists/shared/source_pair_models.inc`
  - `netlists/shared/startup_cells.inc`
  - switched-cap current probe
  - delta-hold capacitor
  - comparatorless latch
  - token integrator
  - reset path
- Predicted failure mode:
  - probe disturbance and token leakage erase the benefit, making the variant slower and no safer than the simpler RC-ranked packet gate
