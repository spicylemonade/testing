# Gap Map: Negative Space Around `create gravity sim`

## Pivot

- The local watchlist is not usable as a direct novelty map. It is dominated by unrelated matches on the word `gravity`, so this gap map treats the task as a Newtonian/orbital/N-body simulator problem rather than quantum gravity, gravity waves, or gravity-field inversion.
- The crowded territory is raw solver speed, generic orbital demos, and yet another integrator paper. The negative space sits in the seams between accurate dynamics, interactivity, diagnosis, reproducibility, and user trust.

## Mainstream Directions To Avoid

- Faster raw force evaluation as the whole contribution. GPU/WebGPU, Barnes-Hut, FMM, and large-N acceleration are already crowded.
- Another general-purpose high-accuracy integrator as the main idea. REBOUND, WHFast, IAS15, MERCURIUS, TRACE, JANUS, and related families already cover the obvious solver positions.
- `Runs in the browser` as the novelty claim. Browser mode, WebAssembly ports, and real-time visual front ends already exist.
- Generic `interactive educational gravity sim` claims. Interactive demos are common; that alone is not a research wedge.
- Smooth differentiable gravity simulation for benign parameter fitting. Differentiable N-body and orbit-inference tooling is already emerging.

## Priority Gaps

### 1. Self-diagnosing cross-regime integrator orchestration

- Gap: Existing packages expose many integrators, but they still expect the user to know when fixed-step symplectic methods are unsafe, when close encounters require a hybrid solver, and when precision should be escalated.
- Why it still looks open: The missing layer is not another solver, but an orchestration system that detects regime shifts, switches methods safely, and explains why it intervened.
- Concrete failure mode: A user runs a long-horizon simulation with a fixed step, misses a close encounter or high-eccentricity episode, and gets a visually plausible but physically wrong outcome with no warning.
- Why this is under-served: It sits between numerical analysis and usable systems design, so it matters in practice but is not the default target of solver papers.
- Evidence anchors: REBOUND integrator docs, WHFast512 feature limits, and recent close-encounter/adaptive symplectic work.

### 2. Commodity-hardware gravity simulation with deterministic replay and fidelity envelopes

- Gap: Real-time browser and commodity-GPU gravity sims exist, but cross-device determinism, decoupled render/physics timing, and explicit error envelopes on non-HPC hardware are still thin.
- Why it still looks open: Most existing systems optimize either for native scientific accuracy or for accessible demos, leaving a middle ground with weak guarantees.
- Concrete failure mode: The same seed and initial conditions diverge across browsers, GPUs, or frame rates, but the interface presents all outputs as equally trustworthy.
- Why this is under-served: Browser/runtime variability is a systems problem that falls outside the main astro-simulation publishing path.
- Evidence anchors: REBOUND browser mode, SimulationArchive/native reproducibility tooling, and the absence of a standard deterministic replay story in browser gravity demos.

### 3. Event-aware differentiable gravity simulation

- Gap: Differentiable gravity tools already exist for smooth orbit fitting and inference, but robust gradients through close encounters, captures, merges, collisions, or integrator switches remain much less mature.
- Why it still looks open: The useful creator and research workflows are exactly the ones where the dynamics become non-smooth and naive differentiation breaks.
- Concrete failure mode: Optimization works on benign trajectories, then collapses or becomes misleading exactly when bodies graze, scatter, merge, or enter a regime that forces solver changes.
- Why this is under-served: It requires combining differentiable programming with hybrid integrators and event handling, which is much harder than smooth-force differentiation.
- Evidence anchors: Recent differentiable orbit-inference/N-body efforts plus close-encounter solvers such as TRACE and related REBOUND methods.

### 4. Uncertainty-aware visualization for chaotic multi-body systems

- Gap: Most gravity sims still show a single crisp future trajectory even when the system is chaotic, numerically sensitive, or parameter-uncertain.
- Why it still looks open: There is relevant work on long-horizon solar-system chaos and some uncertainty visualization for trajectory ensembles, but little general-purpose tooling for creator-facing or exploratory gravity simulators.
- Concrete failure mode: Users interpret one rendered orbit as a prediction instead of one sample from a highly unstable future.
- Why this is under-served: It is partly an HCI and visual analytics problem, so solver-centric projects usually leave it out.
- Evidence anchors: Long-term solar-system chaos/reliability work using high-precision references and trajectory-uncertainty visualization literature.

### 5. Cross-regime benchmark suite for gravity-sim systems

- Gap: There are benchmark fragments for speed, separate work on numerical reliability, and isolated domain datasets, but no standard suite that jointly measures long-horizon invariants, close-encounter capture, chaotic sensitivity, determinism, latency, and interactive constraints.
- Why it still looks open: Each sub-community measures its own local objective, so a simulator can look strong on FPS or mean energy drift while still failing in the regimes users actually care about.
- Concrete failure mode: A project reports throughput or average energy error, but never reveals missed encounters, hardware-dependent divergence, or failure under interactive perturbation.
- Why this is under-served: It spans astro numerics, systems, graphics, and HCI, so no single field naturally owns the benchmark.
- Evidence anchors: REBOUND reproducibility tooling, the `vanilla` solar-system benchmark, and recent open cislunar high-fidelity trajectory benchmarks.

## Hidden Assumptions To State Explicitly

- `Gravity sim` is interpreted here as Newtonian/orbital/N-body simulation, not geophysics, gravity waves, or relativistic/quantum gravity.
- The target is a general-purpose or creator-facing simulator, not a domain-specific astrophysics production code or a full spacecraft mission-analysis stack.
- Novelty should come from orchestration, diagnosis, evaluation, uncertainty handling, or hybrid capability, not from claiming the first browser demo or the first GPU kernel.
- `Under-served` means sparse coverage at the intersection of accurate dynamics and usable systems behavior, not total absence of prior work.
- This is a gap map, not an exhaustive literature review. The local repo artifacts were corrected with a narrow, targeted search pass because the initial seed query was visibly off-target.

## Recommended Angle

- If this project wants a credible research wedge, the strongest openings are:
  - a self-diagnosing gravity simulator that automatically detects unsafe regimes and explains solver and precision changes,
  - an event-aware differentiable gravity pipeline with explicit fallbacks when gradients stop being trustworthy, or
  - a commodity-hardware simulator with deterministic replay and published fidelity envelopes.
- Those angles sit adjacent to mature solver families instead of competing head-on with them.
