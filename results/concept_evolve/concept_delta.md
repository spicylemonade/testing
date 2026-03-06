# Concept Delta

## 1. Deterministic Encounter Queue + Reversible Microsteps

1. CE suggestion
   - `angular_sweep_encounter_queue` proposed: estimate one-step swept intervals, sort interval endpoints, maintain an active set, emit candidate pairs only, and pass the shortlist to encounter-aware integration.
   - `encounter_reversible_substeps` proposed: maintain an encounter queue, use leapfrog outside the queue, and use a symmetric micro-step wrapper plus round-trip mismatch logging inside it.
2. What was implemented
   - Queue builder and encounter runner in `src/minigrav/research/encounters.py`.
   - Benchmark integration in `scripts/run_benchmark_report.py` and stress-regime reporting in `scripts/run_reproducibility_report.py`.
3. Result
   - The queue stays sparse while keeping full recall on the sampled stress case.
   - On `star_grazing_two_body`, the encounter mode cuts final-state error versus REBOUND by about `75x` at `dt=0.005`, `75x` at `dt=0.01`, `144x` at `dt=0.02`, and `486x` at `dt=0.04`.
   - The direct kernel is unsafe across the tested coarse and medium `dt` values, while the encounter mode becomes safe at `dt <= 0.02`.
4. Novel contribution
   - The novelty is not a new general integrator; it is a deterministic, geometry-triggered close-encounter layer that turns a tiny reference kernel into an honesty-preserving stress-tested system.

## 2. Round-Trip Error As A Trust Signal

1. CE suggestion
   - `forward_reverse_verification_loop` proposed: expose a `roundtrip_error(z0, T)` helper, add analytic scenarios to the regression suite, and use the round-trip mismatch as a runtime quality signal.
2. What was implemented
   - Round-trip helper in `src/minigrav/verification/roundtrip.py`.
   - Claim-linked audit outputs in `src/minigrav/runner.py` and `scripts/run_audit_bundle.py`.
   - Concept experiment in `results/concept_evolve/tree/008_forward_reverse_verification_loop/experiment.py`.
3. Result
   - The helper works and is numerically tiny on smooth controls.
   - Unexpectedly, the plain direct kernel can keep near-machine-precision round-trip error even when it diverges strongly from REBOUND on the star-grazing case.
4. Novel contribution
   - The useful novelty is the negative result: reversibility alone is not a sufficient fidelity proxy for close encounters, so trust reporting must combine round-trip diagnostics with external reference checks and encounter-aware policies.

## 3. Resolution-Coupled Softening

1. CE suggestion
   - `resolution_coupled_softening` proposed: measure local cell size in batch mode, set epsilon from that scale, and surface the effective smoothing scale explicitly.
2. What was implemented
   - Batch-mode local-cell estimator and scale-coupled epsilon runner in `src/minigrav/research/resolution_softening.py`.
   - Stress evaluation in `scripts/run_reproducibility_report.py` and concept experiment in `results/concept_evolve/tree/009_resolution_coupled_softening/experiment.py`.
3. Result
   - The branch never enters the declared safe regime on the star-grazing stress case.
   - It can smooth the singularity, but it distorts the trajectory more than the encounter-microstep branch and never becomes a fidelity-preserving default.
4. Novel contribution
   - The novelty here is a documented negative result: graphics-inspired scale blur is not a credible substitute for encounter-aware physics in a minimal gravity simulator.
