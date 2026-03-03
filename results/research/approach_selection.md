# Approach Selection for Phase 3

This selection uses phase-1 literature evidence, baseline gap findings, and concept-tree walk paths from `results/concept_evolve/walk_session.json`.

## Method comparison matrix

| Method | Stability | Complexity | Implementation risk | Literature support | Decision |
| --- | --- | --- | --- | --- | --- |
| Fixed-step symplectic integration (leapfrog / velocity-Verlet) | High long-horizon invariant behavior; lower secular drift than Euler baseline | Low to medium | Low | Strong support from geometric integration and N-body practice (`[@forest1990; @yoshida1990; @wisdom1991; @reintamayo2015]`) | **Selected first** |
| Barnes-Hut force approximation | Medium-to-high; controlled by opening angle and softening; requires error monitoring | Medium | Medium | Canonical scaling evidence (`[@barnes1986; @springel2005; @potter2017]`) | **Selected second** |
| Adaptive or hybrid timestep symplectic methods | Potentially high for close encounters, but risk of reproducibility and metric confounds | Medium to high | High | Strong but more complex evidence (`[@duncan1998; @chambers1999; @rein2019]`) | Deferred after core phase-3 goals |

## Selection rationale

1. Baseline metrics show catastrophic drift, so structure-preserving integration is the highest-priority corrective path.
2. Phase-3 also requires throughput gains for high N; Barnes-Hut provides the cleanest next step without introducing full adaptive scheduling complexity.
3. Adaptive/hybrid stepping remains valuable for follow-up ablations but is deferred to avoid conflating stability and scalability effects in initial comparisons.

## Dependency evidence from concept-tree walk

- Walk paths consistently include `newtonian_force_kernel -> fixed_step_integrator -> diagnostics_metrics_contract`, supporting the sequence: symplectic integrator first, scalable force next.
- CLI/reproducibility nodes are downstream in all selected paths, reinforcing the need for controlled method comparisons under fixed seed and fixed reporting contracts.
