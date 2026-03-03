# Baseline Simulator Design Spec

## Scope

Implement a deterministic Newtonian gravity baseline as the reference system for all later experiments and method comparisons.

## State schema

- `positions`: float64 array shaped `(N, 2)` in simulation length units.
- `velocities`: float64 array shaped `(N, 2)` in simulation length/time units.
- `masses`: float64 array shaped `(N,)` in simulation mass units.
- `time`: scalar float64.
- `step`: scalar int.
- Optional diagnostics stream per step: total energy, total angular momentum, center of mass.

## Units

- Use normalized code units with `G = 1.0`.
- Length, time, and mass are dimensionless but consistently tracked in metadata.
- All state and derived quantities use float64 for deterministic stability.

## Force law

Pairwise Newtonian gravity with Plummer softening:

`a_i = sum_{j != i} G * m_j * (r_j - r_i) / (||r_j-r_i||^2 + eps^2)^(3/2)`

Potential term for diagnostics:

`U = -sum_{i<j} G * m_i * m_j / sqrt(||r_j-r_i||^2 + eps^2)`

## Softening policy

- Default `eps = 1e-3` in code units.
- Keep `eps` fixed within each run.
- Sensitivity to `eps` is evaluated in phase 4 robustness checks.

## Fixed-step integrator

- Baseline integrator: explicit Euler (intentionally simple baseline).
- Time stepping: constant `dt` for all bodies and all steps.
- Symplectic and scalable variants are compared against this baseline in phase 3.

## Deterministic seed strategy

- Seed all random scenario generation through `numpy.random.default_rng(seed)`.
- Default seed for reproducible experiments: `42`.
- Record seed in every artifact metadata block and run manifest.

## CLI contract (planned)

`python3 -m gravity_sim.cli run --method baseline --scenario <two_body|three_body|random> --n <int> --steps <int> --dt <float> --seed <int> --softening <float> --out <path>`

Required outputs:

- trajectory JSON (`results/.../trajectories/*.json`)
- metrics JSON/MD where requested
- run metadata fields: method, scenario, N, dt, seed, softening, steps

## Dependencies on phase-1 artifacts

- `results/repo_analysis/problem_statement.md`: metric thresholds and research questions.
- `results/literature/literature_review.md`: force/integrator/scaling references.
- `results/literature/subagent_phase1/synthesis.md`: actionable method priorities and citation chains.
- `results/concept_evolve/steering_notes.md`: baseline-first deterministic direction.
- `sources.bib`: bibliographic ground truth for design claims.
