# Literature Review for Minimal Gravity Simulation

This review focuses on sources that directly inform baseline correctness, long-horizon stability, and scalable force approximation.

## Force computation and scalability

- `[@barnes1986]` introduced the Barnes-Hut tree method (`O(N log N)`), which motivates our scalable-force branch and error-vs-speed trade-off analysis.
- `[@greengard1987]` formalized the Fast Multipole Method (`O(N)` asymptotics), providing a reference point for how far beyond tree approximations scaling can go.
- `[@springel2005]` demonstrated practical large-scale TreePM architecture and benchmarking discipline, informing our run-manifest and throughput reporting design.
- `[@potter2017]` shows modern high-scale cosmological execution constraints (memory, decomposition, and throughput), guiding what "scalable" should mean in our phase-3 evaluations.

## Symplectic integration and numerical stability

- `[@yoshida1990]` provides composition rules for higher-order symplectic schemes, informing our method-selection matrix and extension path.
- `[@forest1990]` established fourth-order symplectic formulations, highlighting why geometric structure-preserving methods reduce secular drift.
- `[@wisdom1991]` is a canonical reference for long-horizon orbital mapping with symplectic methods and motivates using energy/angle drift as primary diagnostics.
- `[@duncan1998]` introduced multi-time-step symplectic handling of close encounters, informing potential follow-up ablations and hybrid variants.
- `[@chambers1999]` showed hybrid symplectic switching strategies that maintain efficiency while handling close passes, directly relevant to hybrid proposal design.
- `[@rein2019]` modernized hybrid symplectic integration practice and implementation details, useful for reconciling numerical fidelity with practical complexity.

## Open-source reproducibility and benchmark references

- `[@rein2012]` (REBOUND) provides a clean reproducible N-body framework and multiple integrator options, serving as an implementation and validation reference.
- `[@reinspiegel2015]` (IAS15) defines a high-accuracy adaptive baseline for error benchmarking and long-horizon precision expectations.
- `[@reintamayo2015]` (WHFast) demonstrates practical, high-performance symplectic implementation choices that inform runtime and bias evaluation criteria.

## Synthesis

The literature converges on a two-track strategy: (1) preserve invariants with symplectic design where long-horizon fidelity matters, and (2) reduce computational cost at higher N via hierarchical approximations. This directly supports the baseline -> symplectic -> scalable-force progression in the rubric.
