# Gap Map: Negative Space Around Cellular-Automata Search for Arithmetic Kakeya

Snapshot date: 2026-03-18 UTC

## Decision Frame

- This refresh is repo-first. I used the required context files, the existing swarm memos, the concept-evolution tree, and local benchmark notes before considering any new external search.
- The stored watchlist remains malformed and low-signal for this topic. The meaningful constraints in this run come from the arithmetic-Kakeya formulation itself, the falsifier memo, and the repo's own blocked experiment records.
- "Under-served" here means directions that are neither another tiny hand-built witness, nor generic automated search, nor modular-only play, nor a fixed-small-alphabet CA story.

## Ranked Gaps

### 1. Exact verifier-coupled proof state over `\mathbb{Z}`

- Priority: highest
- Type: core scientific gap plus infrastructure blocker
- Why this looks genuinely under-served:
  The real object is not local propagation. It is exact `\mathbb{Z}`-linear elimination with singleton support and `T`-masking. The repo has multiple design documents for verifier-coupled search, but the current snapshot still does not expose an exact decoder or exact verifier for six-line `(X,G,R,T)` witnesses. That means there is still no executable loop in which a CA state can be judged on the true object it is supposed to discover.
- Failure mode if ignored:
  A CA can look successful on diffusion, entropy, current, or certificate-growth proxies while never producing a legal singleton `(a,-a)` certificate after exact closure. At that point the decoder or repair layer is doing the hard work, not the automaton.
- Concrete next move:
  Recover or implement the exact six-line decoder/verifier first, then restrict search to proof-carrying encodings whose state can be audited directly against exact legality and exact score.
- Evidence anchors:
  `results/context_sync.md`, `results/core/lane_gates.md`, `results/swarm/falsifier.md`, `results/experiments/h1_controls.md`, `results/experiments/complexity_sweep.md`

### 2. Constructibility-native dynamics instead of flat realized-graph CA

- Priority: high
- Type: under-explored representation gap
- Why this looks genuinely under-served:
  Legal witnesses live in the recursive product-grid representation `(d_1,\dots,d_k,f_1,\dots,f_k)` with copy-and-glue ancestry. A flat CA on the final edge-labeled graph, or on an image-like lattice, forgets the stage structure that determines legality, edge cost, and the support pattern of valid forcing data. The repo keeps circling this issue, but there is still no mature search parameterization that makes recursive constructibility native rather than reconstructed after the fact.
- Failure mode if ignored:
  Search will find regular-looking local motifs that are either illegal as constructible graphs or only become legal after nonlocal repair, which immediately breaks score faithfulness.
- Concrete next move:
  Move the active search space onto stage-indexed fibers, construction trees, stage-indexed certificate tensors, or tile/macrocell grammars that emit `f_i`, `R`, and `T` directly.
- Evidence anchors:
  `results/swarm/director_brief.md`, `results/swarm/hypothesis_negative_space.md`, `results/core/h1_design.md`, `results/concept_evolve/tree/006_tile_assembly_constructible_grammar/README.md`, `results/concept_evolve/tree/phase_2_baselines/003_stage_indexed_certificate_tensor/README.md`

### 3. Escape mechanisms from bounded-slope / low-rational-complexity trapping

- Priority: high
- Type: frontier failure mode
- Why this looks genuinely under-served:
  A CA with a fixed small alphabet is naturally biased toward tiny slope sets and low rational complexity. The repo already treats that regime as structurally dangerous, and the planned complexity sweep is still empty. What remains missing is any concrete mechanism by which a local-rule program can leave the low-complexity comfort zone while staying verifier-faithful.
- Failure mode if ignored:
  The search will repeatedly rediscover small, periodic, low-complexity families and misread them as progress toward the `<= 1.675` target, even though they sit in the exact regime the current notes warn against.
- Concrete next move:
  Treat `|X|`, rational complexity, and verified score as joint objectives; require wins in medium and unrestricted regimes; and prefer architectures where the effective alphabet can grow, mutate, or be re-indexed across scales instead of staying frozen.
- Evidence anchors:
  `results/swarm/falsifier.md`, `results/core/lane_gates.md`, `results/experiments/complexity_sweep.md`, `results/literature/prior_art_gap.md`

### 4. Honest bridges from modular or proxy dynamics back to integer witnesses

- Priority: medium-high
- Type: bridge gap
- Why this looks genuinely under-served:
  Finite-state automata naturally want `\mathbb{F}_p` or `\mathbb{Z}/N\mathbb{Z}` alphabets, and several concrete repo branches already push toward proxy dynamics such as bootstrap-style activation, odometer concentration, or spatially coupled peeling. Those are plausible curricula or screening tools, but the missing piece is a deterministic lift or transfer test back to exact integer witnesses in the original forcing-pair problem.
- Failure mode if ignored:
  Modular cancellations, percolation thresholds, or odometer features become a modular or local-dynamics mirage: attractive, measurable, and completely irrelevant to verified score over `\mathbb{Z}`.
- Concrete next move:
  Every modular or proxy branch should report an integer-lift success rate, exact-score transfer rate, and comparison against trivial graph baselines before it is treated as signal.
- Evidence anchors:
  `results/swarm/falsifier.md`, `results/experiments/complexity_sweep.md`, `results/concept_evolve/tree/008_odometer_sink_compilers/README.md`, `results/concept_evolve/tree/003_bootstrap_certificate_percolation/README.md`, `results/concept_evolve/tree/002_spatially_coupled_peeling_ladders/README.md`

### 5. Sparse, nonuniform witness families and family-level benchmarks

- Priority: medium-high
- Type: under-explored setting plus benchmarking gap
- Why this looks genuinely under-served:
  The popular extremes are already obvious: another tiny self-similar gadget, or a broad many-slope asymptotic story. The local negative space is the middle regime: cheap recursive backgrounds plus sparse defects, nonuniform stage schedules, spatial coupling, or tile grammars that may only reveal their value at the family level rather than as one polished witness. The repo has concept sketches for this regime, but no decoder-matched benchmark suite and no out-of-distribution evidence.
- Failure mode if ignored:
  The program overfits one grid size, one encoding, or one geometry, then reports a single attractive construction that cannot survive held-out sizes, aspect ratios, or matched non-CA baselines.
- Concrete next move:
  Build a family-level benchmark around sparse-defect, spatially coupled, and tile-grammar witness generators, with decoder-matched baselines, held-out shapes, and distributional reporting instead of best-of-many anecdotes.
- Evidence anchors:
  `results/swarm/hypothesis_negative_space.md`, `results/swarm/falsifier.md`, `results/experiments/h1_controls.md`, `results/concept_evolve/tree/002_spatially_coupled_peeling_ladders/README.md`, `results/concept_evolve/tree/006_tile_assembly_constructible_grammar/README.md`

## Directions To Deprioritize

- Generic neural CA or generic agentic search without proof-carrying state and exact verifier coupling.
- Fixed-small-alphabet or bounded-slope CA stories presented as if they address the frontier score target.
- Modular-only wins, reversible-pattern wins, or odometer/percolation wins that do not transfer back to exact integer witnesses.
- Another tidy one-off gadget that lacks family-level evidence across legal shapes and complexity regimes.

## Bottom Line

- The strongest under-served gaps are not "use cellular automata" in the abstract.
- They are:
  - exact verifier-coupled proof state over `\mathbb{Z}`,
  - constructibility-native dynamics,
  - escape from bounded-slope trapping,
  - honest lift from modular or proxy dynamics,
  - and family-level search over sparse, nonuniform witness regimes.
- Until those five gaps are addressed, the CA program remains easier to mistake for generic search or bounded-complexity toy behavior than for real progress on the arithmetic-Kakeya witness target.
