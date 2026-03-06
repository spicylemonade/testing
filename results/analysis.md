# Analysis

The final contribution is an audited deterministic minimal gravity reference kernel with a narrow close-encounter trust spine, not a new general-purpose N-body engine [@rein2011; @lu2024].

## What The Measurements Show

- Smooth analytic controls are already strong: circular, elliptic, period, escape, and orbital-element tests all pass across `dt = 0.02, 0.01, 0.005`, with errors dropping as `dt` halves [@mitocw2008; @wisdom1991].
- Long-horizon behavior is disciplined on the intended small-N regime: energy drift stays tiny for the circular and small-N ring cases, and the figure-eight choreography exposes a useful caveat where relative angular-momentum convergence is noise-sensitive because the true total angular momentum is near zero [@freno2026].
- The real failure regime is close encounters. On `star_grazing_two_body`, the plain direct kernel is unsafe at coarse and medium `dt`, while the encounter-microstep branch shifts the safe regime dramatically earlier.

## Why The Contribution Is Not Just A Toy Demo

- The project exports invariant drift, round-trip error, timestep-halving convergence, scenario-level benchmark metadata, and cross-runtime replay envelopes as first-class outputs, which directly addresses the `animation not simulator` criticism highlighted by the falsifier [@rein2011; @wasmtime2026].
- Python and Node direct-sum runs agree to roughly machine precision on the canonical scenario bundle, so the deterministic reference-kernel claim is evidence-backed rather than rhetorical [@webassembly2026; @wasmfloattest2026].
- The promoted CE-driven idea is genuinely narrow and testable: a geometry-triggered encounter queue plus reversible microsteps converts a failing close-pass regime into a safe one without pretending to beat REBOUND on raw breadth or sophistication [@lu2024; @rein2017].

## The Most Interesting Surprise

- The round-trip helper is not a standalone fidelity oracle. Even when the plain direct kernel diverges badly from REBOUND on the star-grazing case, its global round-trip error can remain tiny because the leapfrog path is internally reversible.
- That negative result is useful: it means the right trust story is not `reversibility proves correctness`, but `reversibility plus external references plus encounter-aware policy yields an honest simulator`.

## Negative Results That Sharpen The Claim

- Resolution-coupled softening does not rescue the close-encounter regime; it remains unsafe across all tested `dt` values and distorts trajectories more than the encounter-microstep branch [@rein2011].
- Large-N acceleration ideas such as neighbor trees, event-sparse far fields, and streaming patches remain scientifically interesting, but the current evidence says they would dilute the paper into a crowded performance branch before improving the main contribution [@barnes1986; @rein2011].

## Non-Claims

- This work does not claim a new integrator family [@wisdom1991].
- This work does not claim large-N performance, Barnes-Hut novelty, or a REBOUND replacement [@barnes1986; @rein2011].
- This work does not claim UI or educational novelty over PhET or Universe Sandbox [@phet2026; @universesandbox2025].
