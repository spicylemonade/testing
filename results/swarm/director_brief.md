# Director Brief

- Inputs used: `results/research_context.md`, `results/literature/prior_art_watchlist.md`, `results/literature/prior_art_gap.md`, `results/literature/gap_frontier.md`, `results/swarm/gap_map.md`, and `results/swarm/falsifier.md`.
- Missing scout files at review time: `results/swarm/hypothesis_bridge.md` and `results/swarm/hypothesis_negative_space.md` were not present, so the synthesis leans on the gap map and falsifier outputs.

## Decision

- Champion: `H1` audit-first deterministic reference kernel.
- Backup: `H2` honest close-encounter minimal core.

## Why H1 Wins

- It is the cleanest way to make a minimal gravity simulator more than a textbook orbit demo.
- It shifts the contribution away from crowded claims like `easy`, `interactive`, `web-based`, or `from scratch` and toward a falsifiable reference artifact.
- It aligns with the strongest gap in `results/swarm/gap_map.md`: invariant-aware minimal kernels plus reproducibility and benchmark discipline.
- It matches the falsifier's demands directly: analytic controls, conservation diagnostics, timestep convergence, and a trusted baseline comparison.
- It can be disproven quickly and verified clearly, which is exactly what the selection criteria reward.

## Champion Claim Discipline

- Claim a tiny Newtonian reference kernel for 2-body, 3-body, and small-N scenarios; do not market it as a new integrator or a general high-performance N-body engine.
- Make the benchmark pack part of the contribution, not supporting material.
- Treat cross-runtime reproducibility as a research constraint, not a UI feature.
- Use REBOUND or an equivalent trusted baseline as the external reality check.

## Backup Logic

- `H2` stays alive because close encounters are where minimal simulators most visibly fail, and the falsifier already highlights this as a trust gap.
- Promote `H2` only if the deterministic audited-kernel angle turns out to be crowded or technically brittle.
- Keep `H2` narrow: the publishable output is an honest failure envelope and policy disclosure, not a claim of broad algorithmic novelty.

## Directions To Avoid

- Do not lead with `we built a minimal gravity simulator`; that is the easiest possible rejection path.
- Do not claim novelty from Barnes-Hut, RK4, leapfrog, browser delivery, visualization, or classroom friendliness alone.
- Do not drift into solar, borehole, relativistic, or other application-specific simulator branches surfaced by the watchlist.
- Do not call a fixed-central-mass or test-particle model a general N-body simulator.

## Immediate Proof Obligations

- Closed-form two-body recovery: circular orbit, ellipse, period, escape velocity, and orbital elements.
- Invariant tracking: energy, angular momentum, and center-of-mass drift over long horizons.
- Timestep convergence: repeated `dt` halving with a visible stabilization criterion.
- Baseline comparison: matched scenarios against REBOUND or another trusted direct-sum reference.
- Runtime reproducibility: the same scenario bundle run in at least two runtimes with declared tolerance envelopes.

## Kill Criteria

- Existing lightweight tools already provide the same audited deterministic reference profile.
- The simulator cannot meet its own invariant or convergence thresholds on basic controls.
- Cross-runtime reproducibility fails so badly that the determinism angle becomes a liability.
- The only surviving distinction is code size or interface polish.
