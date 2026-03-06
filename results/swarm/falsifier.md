# Falsifier

The easiest adversarial read is that the current novelty screen is not yet credible. `results/literature/prior_art_watchlist.md` is dominated by keyword collisions (solar modeling, borehole monitoring, airway-on-a-chip) rather than the nearest neighbors for a minimal Newtonian/orbital gravity simulator. A reviewer can reject the work immediately by saying the search missed the actual literature branch.

## Easiest Failure Modes

### 1. "This is not research; it is a textbook exercise."
- A minimal two-body or N-body gravity simulator is already standard teaching material and common hobby/open-source work.
- Representative overlap already exists in educational and accessible tools: `Orbital Mechanics Two-Body Model for Educational Purposes` (2024), PhET `Gravity and Orbits`, and Universe Sandbox classroom use.
- If the claim is only "we built a small simulator that shows orbits," the prior-art overlap accusation is trivial.

### 2. "This is a thinner clone of mature existing software."
- `REBOUND: An open-source multi-purpose N-body code for collisional dynamics` (2011, 805 citations) already covers symplectic integration, Barnes-Hut acceleration, and practical N-body simulation.
- `poliastro: a Python library for interactive astrodynamics` (2022) and Orekit already cover accessible orbit propagation APIs, visualization, and astrodynamics workflows.
- Any claim of "easy-to-use gravity simulator" or "open-source gravity simulator" must explain why these are not already sufficient.

### 3. Algorithmic novelty collapses fast.
- `A hierarchical O(N log N) force-calculation algorithm` (Barnes and Hut, 1986, 3760 citations) already occupies the standard fast-gravity branch.
- If the simulator uses direct summation, Euler, RK4, leapfrog, Verlet, or Barnes-Hut, the method is probably conventional rather than novel.
- Without a new integrator, new error analysis, or a problem-specific reduction, there is no strong algorithmic claim.

### 4. Visual plausibility can be mistaken for physical correctness.
- Nice-looking orbits, trails, and real-time animation do not validate the physics.
- Without closed-form controls and conservation diagnostics, the artifact is vulnerable to being called an animation rather than a simulator.

### 5. The educational angle is also crowded.
- "Accessible gravity simulator for teaching" overlaps with PhET, Universe Sandbox, and recent teaching-oriented orbital models.
- Without a user study or a measurable pedagogical advantage, this reads like another demo rather than a research contribution.

### 6. The scope can be overstated.
- If the implementation fixes a central mass or uses test particles, it is not a general self-gravitating N-body simulator.
- A reviewer can easily attack any claim that blurs two-body propagation, restricted-body approximations, and full mutual-gravity simulation.

## Missing Controls That Would Sink Weak Claims

- Analytic two-body control: recover circular and elliptical orbits, period, escape velocity, and orbital elements against closed-form expectations.
- Conservation control: track total energy, angular momentum, and center-of-mass drift over long horizons.
- Integrator control: compare against at least one standard baseline such as leapfrog/Verlet or a trusted library; otherwise accuracy claims float free of evidence.
- Timestep convergence: halve `dt` repeatedly and show the result stabilizes.
- Softening sensitivity: if an `epsilon` term is used, show claims do not depend on hidden smoothing.
- Reference control: compare outputs against REBOUND, poliastro, Orekit, or a direct-sum baseline on identical initial conditions.
- Regime control: test close encounters, high eccentricity, unequal masses, and simple chaotic cases; only showing stable circular demos is cherry-picking.
- Units control: if arbitrary units or a rescaled `G` are used, show unit consistency and explain what physical claims still survive.

## Benchmark Traps

- Short-horizon demos hide energy drift and phase error.
- Small `N` hides the fact that direct-sum performance claims do not generalize.
- 2D-only tests get marketed as "gravity simulation" while avoiding 3D and frame-handling issues.
- Comparing against naive Python loops or unvectorized baselines makes ordinary engineering cleanup look novel.
- Counting rendering time together with physics time obscures whether the improvement is in simulation or visualization.
- Hand-tuning `dt`, softening, or tree thresholds separately for each baseline makes comparisons meaningless.
- Reporting "real-time" for `N < 100` is weak; hobby repos and commercial tools already do this.

## Novelty Illusions

- "Minimal" usually means smaller code, not new science.
- "From scratch" is not a contribution.
- "Interactive" or "web-based" is packaging, not research novelty.
- "Uses Barnes-Hut / leapfrog / RK4" signals adoption of known methods, not invention.
- "Solar system demo" is the default hello-world for this area.
- Visual extras such as trails, vector fields, camera controls, and 3D rendering are already common in open-source demos and Universe Sandbox-like tools.

## Literature Branches Most Likely To Invalidate Weak Claims

### Educational two-body and orbit simulators
- `Orbital Mechanics Two-Body Model for Educational Purposes` (2024).
- PhET `Gravity and Orbits`.
- Invalidates claims like "simple teaching simulator" or "minimal orbit demonstrator".

### Mature N-body codes and integrator ecosystems
- `REBOUND: An open-source multi-purpose N-body code for collisional dynamics` (2011).
- Barnes and Hut (1986).
- Invalidates claims like "N-body engine," "fast gravity simulator," or "tree-based simulator".

### Interactive astrodynamics libraries
- `poliastro: a Python library for interactive astrodynamics` (2022).
- Orekit.
- Invalidates claims like "easy API plus visualization plus orbit propagation".

### Commercial and classroom gravity sandboxes
- Universe Sandbox.
- `HOW TO (DIS-)ASSEMBLE A PLANETARY SYSTEM (by turning a video game into an educational game)` (2021).
- Invalidates claims like "interactive real-time gravity sandbox" or "engaging educational gravity simulator".

### Hobby and student open-source demos
- `OrbitSim`.
- `Gravity-Simulator`.
- `gravity-simulator` with Euler, Verlet, and PEFRL.
- `celestial-simulator` using Barnes-Hut.
- Barnes-Hut JavaScript demos dating back at least to 2014.
- Invalidates any claim that a working demo, web UI, or basic interactive prototype is itself novel.

## Bottom Line

The default hostile reading is: this is a reimplementation of standard orbital/N-body material, backed by an off-target literature review. Unless claims are kept very narrow and supported by analytic controls, established baselines, and a literature review centered on actual N-body/orbital/educational prior art, the easiest accusation is prior-art rehash rather than a research contribution.
