# trajectory_mass_inference

## Context
Let the user draw or import a trajectory and infer masses or G that make the minimal simulator reproduce it. This turns the simulator into an inverse-problem sandbox, bridging educational interactivity and differentiable system identification.

## Domains
- scientific_inference
- differentiable_programming
- education_technology

## Mathematical Formalization
min_{m, G} sum_t ||x_t^sim(m, G) - x_t^obs||^2 + lambda * prior(m); optionally infer only a subset of masses while others remain fixed

## Closest Prior Art
- DiffTaichi: Differentiable Programming for Physical Simulation (`666aaf80f647faf52d5058ff951e2d4b9a8844f5`)
- End-to-End Differentiable Physics for Learning and Control (`0933f3dd33cf907e07aa938ce9465fb0d4250394`)
- Dynamic Visual Reasoning by Learning Differentiable Physics Models from Video and Language (`cbc40f2b5822219c09b0d974f9703d5351fbe48d`)

## Novelty
The novelty is to narrow differentiable inference to a human-authored gravity toy, where the main input is an orbit trail rather than a video stream or a control objective.

## Differentiation
Prior work usually infers physics from perception pipelines or optimizes policies through physics. This concept instead uses a tiny inverse solver as an educational affordance inside the simulator itself.

## Experiment Seed
Generate synthetic ellipses and noisy three-body traces, hide the true masses, and test recovery accuracy under full, partial, and noisy observations.

## Implementation Backlog
1. Collect or import trajectory samples.
2. Define a fit objective over masses and G.
3. Add autodiff or finite-difference optimization.
4. Build a `fit from trail` workflow.
5. Test recovery under noise and partial observations.

## Planned Paths
- `results/concept_evolve/tree/010_trajectory_mass_inference/concept.json`
- `results/concept_evolve/tree/010_trajectory_mass_inference/README.md`
- `results/concept_evolve/tree/010_trajectory_mass_inference/literature.json`
- `prototypes/minigrav/inference/fit_from_trail.py`
- `prototypes/minigrav/tests/test_mass_inference.py`
