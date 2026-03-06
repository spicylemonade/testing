# differentiable_softening_calibration

## Context
Treat the minimal simulator's shortcuts - softening, timestep, opening angle, even encounter radius - as learnable knobs fit against a reference trajectory corpus. This imports differentiable programming not to learn a policy, but to automatically tune a stripped-down gravity engine until it behaves like a more faithful teacher.

## Domains
- differentiable_programming
- astrophysics
- software_engineering

## Mathematical Formalization
min_theta sum_s sum_t ||x_t^mini(theta, s) - x_t^ref(s)||^2 + alpha * Drift(theta, s) + beta * Cost(theta), where theta = {eps, dt, theta_open, rho_enc}

## Closest Prior Art
- DiffTaichi: Differentiable Programming for Physical Simulation (`666aaf80f647faf52d5058ff951e2d4b9a8844f5`)
- End-to-End Differentiable Physics for Learning and Control (`0933f3dd33cf907e07aa938ce9465fb0d4250394`)
- Fast and Feature-Complete Differentiable Physics for Articulated Rigid Bodies with Contact (`60d9bf409dd7c5027ee95eb9b2ebe95bc3e85382`)

## Novelty
The novelty is to use gradients for simulator simplification tuning rather than for control, contact learning, or robot policy optimization.

## Differentiation
Differentiable-physics papers usually optimize control signals or hidden physical parameters of a complex system. This concept instead tunes the approximation knobs of a deliberately tiny gravity engine, keeping the model simple while borrowing fidelity from a teacher.

## Experiment Seed
Train on circular, eccentric, and flyby scenes; evaluate on held-out three-body traces to see whether one calibrated preset generalizes or whether multiple named presets are needed.

## Implementation Backlog
1. Export teacher traces from analytic or REBOUND runs.
2. Implement a differentiable simulator step.
3. Optimize epsilon, dt, opening-angle, and encounter presets.
4. Validate on held-out scenes.
5. Save preset packs and error surfaces.

## Planned Paths
- `results/concept_evolve/tree/004_differentiable_softening_calibration/concept.json`
- `results/concept_evolve/tree/004_differentiable_softening_calibration/README.md`
- `results/concept_evolve/tree/004_differentiable_softening_calibration/literature.json`
- `prototypes/minigrav/calibration/diff_fit.py`
- `prototypes/minigrav/calibration/preset_registry.json`
