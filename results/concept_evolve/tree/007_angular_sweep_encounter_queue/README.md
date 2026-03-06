# angular_sweep_encounter_queue

## Context
In nearly planar scenes, sweep over angle or x-intervals to build a shortlist of bodies whose trajectories can come close during the next step. It turns broad-phase collision geometry into a gravitational encounter scheduler, so expensive local refinement is only spent on pairs that geometry says can matter.

## Domains
- computational_geometry
- astrophysics
- computer_graphics

## Mathematical Formalization
For each body i, build swept interval I_i = [phi_i^min - rho, phi_i^max + rho] or [x_i^min - rho, x_i^max + rho]; during a sweep-line pass, enqueue pair (i, j) whenever I_i intersects I_j and d_perp(i, j) < rho

## Closest Prior Art
- Algorithms for Reporting and Counting Geometric Intersections (`62278010df9000e5496ea2523d46e98bb2206c56`)
- REBOUND: An open-source multi-purpose N-body code for collisional dynamics (`5240c4a18da2b6dcae3fbfa633c01bee1670d0a0`)
- Symplectic integrators in the shearing sheet (`c3ae70601355411b026e65f87e96d7f91be8afc5`)

## Novelty
The key novelty is to use geometry not for collision response, but for deciding when gravitational integration should temporarily become more expensive.

## Differentiation
REBOUND's sweep is about collisions in elongated or ring-like systems. This concept redirects the same geometric idea into encounter triage and local solver escalation, so it is not just a collision detector copied into a new codebase.

## Experiment Seed
Use a 2D asteroid belt and a narrow ring scene; compare candidate-pair recall and runtime against brute-force O(N^2) close-pass scans.

## Implementation Backlog
1. Compute swept x or phi intervals over one tentative step.
2. Maintain a sweep-line active set.
3. Emit candidate close-pass pairs only.
4. Feed the queue into encounter-aware integration.
5. Benchmark recall versus brute-force scanning.

## Planned Paths
- `results/concept_evolve/tree/007_angular_sweep_encounter_queue/concept.json`
- `results/concept_evolve/tree/007_angular_sweep_encounter_queue/README.md`
- `results/concept_evolve/tree/007_angular_sweep_encounter_queue/literature.json`
- `prototypes/minigrav/geometry/angular_sweep.py`
- `prototypes/minigrav/tests/test_angular_sweep.py`
