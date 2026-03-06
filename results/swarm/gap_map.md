# Gap Map

The current literature surface is dominated by adjacent or off-target work (`GX Simulator`, borehole monitoring, black-hole trajectory studies, and medical uses of "gravity"), while `results/literature/gap_frontier.md` is even farther from the task. The strongest opportunities therefore sit in the missing middle: small, trustworthy, portable gravity simulators rather than another high-fidelity domain simulator.

## 1. Invariant-aware minimal reference kernel

- Why this looks under-served: the current watchlist shows large or specialized simulators, while toy gravity demos rarely publish error budgets or reference checks.
- Concrete failure mode: visually stable orbits can still leak energy or angular momentum badly, especially with Euler-like updates.
- Under-explored setting: a tiny 2-body/3-body/N-body core with built-in conservation diagnostics, regression tests, and known-good scenarios.
- Why prioritize it: it is central to "minimal" and appears much less crowded than solar, borehole, or relativistic simulator branches.

## 2. Close-encounter and collision handling in tiny simulators

- Why this looks under-served: robust singularity handling usually lives in heavyweight astrophysics codes, not stripped-down educational or reference simulators.
- Concrete failure mode: near-collisions trigger numerical blow-ups, timestep collapse, tunneling, or undisclosed softening that changes the physics.
- Under-explored setting: minimal policies for adaptive stepping, softening, merge/bounce rules, and honest failure reporting when the model leaves its safe regime.
- Why prioritize it: this is where "minimal" simulators most often break, yet it is less fashionable than scaling to huge particle counts.

## 3. Deterministic low-precision deployment (browser/WASM/mobile)

- Why this looks under-served: many gravity simulators are demos, but determinism across JS engines, WASM, mobile, and float32 budgets is rarely treated as a first-class problem.
- Concrete failure mode: the same initial state diverges across devices because integration is coupled to frame rate, precision, or body update order.
- Under-explored setting: a simulator that is intentionally designed for fixed-step, low-resource, cross-platform reproducibility.
- Why prioritize it: low-resource reliability is less saturated than GPU or HPC acceleration and maps directly to a minimal distribution story.

## 4. Unit-safe and scale-safe scenario authoring

- Why this looks under-served: minimal simulators often mix pixels, arbitrary gravitational constants, and real units, while scientific codes assume expert users who already know how to normalize systems.
- Concrete failure mode: users create pretty but physically meaningless systems because masses, distances, and time steps are incoherent.
- Under-explored setting: dimensionless normalization, automatic rescaling, unit checks, and clean conversion between classroom toy systems and real celestial data.
- Why prioritize it: it addresses a real correctness gap that is usually ignored because it is neither glamorous nor computationally expensive.

## 5. Tiny benchmark and audit suite for gravity simulators

- Why this looks under-served: the current artifacts do not surface any canonical benchmark set for minimal gravity simulators, only adjacent domain simulators and distant frontier papers.
- Concrete failure mode: every simulator is judged on hand-picked "pretty orbit" cases, making accuracy, stability, and novelty claims hard to compare.
- Under-explored setting: a compact benchmark pack with invariant drift, phase error, close-encounter stress tests, escape or capture cases, and reproducible expected outputs.
- Why prioritize it: benchmark infrastructure is often ignored, but it creates the clearest differentiation and protects against novelty illusions.

## Best Immediate Wedge

- The strongest combined direction is `1 + 2 + 3`: a minimal, invariant-aware gravity core that survives close encounters and behaves reproducibly across browser, WASM, and mobile targets.
- Add `5` early if the goal is research credibility; add `4` early if the goal is education or broad user adoption.
- Deprioritize large solar, borehole, and relativistic branches for now because those look closer to the existing literature than the missing middle above.
