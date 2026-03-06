# Baseline Architecture

## Reference Runtime

- Primary implementation runtime: Python 3.10 reference kernel.
- Cross-runtime target: a later Node.js mirror of the same fixed-step direct-sum path for reproducibility testing.
- Baseline claim: correctness and auditability for small deterministic workloads, not high-N throughput.

## State Representation

- Canonical body state is stored in structure-of-arrays form:
  - `mass[n]`
  - `position[n, 3]`
  - `velocity[n, 3]`
  - `radius[n]` for encounter diagnostics and reporting only
  - `label[n]` as stable scenario-defined identifiers
- Simulation metadata travels separately from numeric state:
  - `scenario_id`, `seed`, `unit_system`, `gravitational_constant`, `dt`, `steps`, `integrator`, `softening_policy`, `benchmark_tags`
- Output snapshots keep the same body ordering as the scenario file to make Python/Node comparisons index-stable.

## Force Model

- Baseline force model: Newtonian mutual gravity with direct summation.
- Pairwise acceleration uses
  - `a_ij = G * m_j * r_ij / (||r_ij||^2 + eps_ij^2)^(3/2)`
- Baseline `eps_ij = 0` unless a scenario explicitly enables a research softening policy.
- Force accumulation is symmetric and pairwise so momentum conservation can be checked from the same loop.

## Integrator Boundary

- Baseline integrator: fixed-step kick-drift-kick leapfrog.
- Boundary contract:
  - `compute_accelerations(state, force_config) -> accelerations, pair_metrics`
  - `step_leapfrog(state, dt, force_config) -> next_state, step_report`
  - `run_scenario(config) -> trajectory, diagnostics, metadata`
- Research extensions plug in around this boundary rather than replacing it wholesale:
  - encounter queue hooks
  - round-trip verification hooks
  - invariant projection hooks
  - calibrated preset overrides

## Scenario File Format

- Scenario files will be JSON with top-level fields:
  - `scenario_id`
  - `description`
  - `unit_system` (`normalized` or `si`)
  - `seed`
  - `gravitational_constant`
  - `duration`
  - `dt`
  - optional `steps` override when the desired analytic duration is not exactly divisible by `dt`
  - `expected_metrics`
  - `benchmark_tags`
  - `bodies` (ordered array)
- Each body record will include:
  - `id`
  - `mass`
  - `radius`
  - `position` (3-vector)
  - `velocity` (3-vector)
  - optional `fixed` flag for special analytic controls only

## Deterministic Update Order

- Scenario loader preserves body order exactly as written on disk.
- Pairwise force accumulation iterates `i` from `0..n-1` and `j` from `i+1..n-1` with no hash-based ordering or parallel reduction.
- Diagnostics are computed after every whole step in a fixed order: energy, angular momentum, center-of-mass, encounter stats, round-trip stats.
- Any adaptive or research-only refinement must remain deterministic by deriving triggers solely from current state, declared thresholds, and stable body ordering.

## Units And Normalization

- Default benchmark pack uses normalized units with explicit `G` to keep formulas simple and cross-runtime comparisons stable.
- Physical-unit scenarios are allowed, but the loader must either:
  - run them directly in SI, or
  - convert them into an explicit normalized form and record that transform in metadata.
- All reports must state the unit system, `G`, and whether softening or normalization changed the raw scenario values.

## Module Boundaries

- Physics core
  - state containers, pairwise force loop, integrator stepping, encounter queue helpers
- Diagnostics
  - invariants, round-trip error, close-encounter summaries, timestep-halving convergence summaries
- Scenario IO
  - JSON parsing, normalization checks, deterministic body ordering, scenario bundle export/import
- Benchmark harness
  - analytic controls, matched-baseline runs, report tables, figure generation, machine-readable result dumps

## Planned File Layout

- `src/minigrav/core/`
- `src/minigrav/diagnostics/`
- `src/minigrav/io/`
- `src/minigrav/benchmarks/`
- `scenarios/`
- `scripts/`
- `runtime/` for the Node.js reproducibility mirror
