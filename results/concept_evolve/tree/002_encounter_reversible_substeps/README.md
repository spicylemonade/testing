# encounter_reversible_substeps

## Context
Run a cheap symplectic base integrator everywhere, but wrap close encounters in symmetric micro-steps triggered only when bodies enter an encounter envelope. The bridge is between hybrid planetary integrators and rare-event scheduling: expensive accuracy is reserved for the tiny fraction of time where human-visible errors actually happen.

## Domains
- astrophysics
- event_driven_simulation
- numerical_analysis

## Mathematical Formalization
Phi_dt(z) = S_base(dt)(z) if d_min > rho; else Phi_dt(z) = S_base(dt/2) o S_enc(dt/m)^m o S_base(dt/2), with ||Phi_-dt(Phi_dt(z)) - z|| kept below tau_rev

## Closest Prior Art
- TRACE: a code for time-reversible astrophysical close encounters (`9696edaf37f8ebd7cc544f1b3b0069d0d32632a1`)
- Symplectic maps for the N-body problem. (`377d069236ca0108a79170e634986a0d7edffdfa`)
- Molecular dynamics and time reversibility (`9d7ff20438c6cc21330cb254163a4c6667c18e68`)

## Novelty
The new part is the trigger policy and scope: only user-visible encounter windows activate the expensive reversible path, so the mechanism is tuned for a minimal interactive simulator rather than a general planetary code.

## Differentiation
TRACE and related hybrid maps are general-purpose research integrators. This concept repackages the idea as a tiny encounter-only service layer with explicit quality thresholds and a UI-facing notion of when accuracy mode should engage.

## Experiment Seed
Use slingshot, binary flyby, and star-grazing test scenes; compare energy drift and wall-clock time against a uniform small-timestep baseline.

## Implementation Backlog
1. Detect candidate encounters from the current state.
2. Add a symmetric micro-step wrapper around the base integrator.
3. Log forward/backward mismatch for each encounter.
4. Compare against a uniform small-timestep reference.
5. Stress test with slingshots and near-collisions.

## Planned Paths
- `results/concept_evolve/tree/002_encounter_reversible_substeps/concept.json`
- `results/concept_evolve/tree/002_encounter_reversible_substeps/README.md`
- `results/concept_evolve/tree/002_encounter_reversible_substeps/literature.json`
- `prototypes/minigrav/integrators/encounter_switch.py`
- `prototypes/minigrav/tests/test_encounter_switch.py`
