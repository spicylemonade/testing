# Benchmark Report

Verification phase: `post_deepen`

## Verdict

- Internal benchmark verdict: `partial_support`.
- Publication-quality benchmark verdict: `not supported`.

The current artifact pack supports three narrow statements:

- `H1_defect_syndrome_ca_64m` is a valid negative control only for the original canonical-seed pilot in `results/experiments/order_668_64m/summary.json`: no exact hit, no improvement over the published seed objective `13/2880/512`, and no reason to continue broad H1 sweeps.
- The post-deepen retained-library branches support a much narrower claim than the manuscript currently hints at: inside the frontier-tuned retained action library, several local controllers reach `13/2744/480` while the chosen single-action controls do not.
- `H_population_self_stabilizing_ca_668` fails honestly. The saved summary already reports equal coupled and zero-coupling medians on all six evaluated states, and a direct read of `results/experiments/order_668_population_ca/summary.json` shows that on the canonical frontier the coupled and zero-coupling variants match seed-by-seed across all five RNG seeds.

What the pack does **not** support is a publication-grade claim of CA competitiveness, held-out generalization, robust mechanism identification, or a broadly representative frontier benchmark.

## Evidence Reviewed

This audit re-read:

- `research_rubric.json`
- `results/research_context.md`
- `results/swarm/falsifier.md`
- `results/verification/benchmark_spec.md`
- `results/verification/benchmark_gate.md`
- `results/verification/runtime_audit.md`
- `results/verification/runtime_benchmark_note.md`
- `results/verification/radius_limited_locality_barrier.md`
- `results/analysis/composite_packet_locality_atlas.md`
- `results/analysis/frontier_locality_scan.md`
- `results/analysis/frontier_population_phase_map.md`
- `results/experiments/controls/summary.md`
- `results/experiments/controls/summary.json`
- `results/experiments/order_668_64m/summary.md`
- `results/experiments/order_668_64m/summary.json`
- `results/experiments/order_668_hypergraph_ca/summary.md`
- `results/experiments/order_668_hypergraph_ca/summary.json`
- `results/experiments/order_668_lattice_gas/summary.md`
- `results/experiments/order_668_lattice_gas/summary.json`
- `results/experiments/order_668_orbit_ca/summary.md`
- `results/experiments/order_668_orbit_ca/summary.json`
- `results/experiments/order_668_orbit_ca/training_manifest.json`
- `results/experiments/order_668_population_ca/summary.md`
- `results/experiments/order_668_population_ca/summary.json`
- `results/experiments/order_668_population_ca/training_manifest.json`
- `results/analysis/composite_packet_retained_library.json`
- `hadamard_ca/retained_state_graph.py`
- `hadamard_ca/h1_ca.py`
- `scripts/run_hypergraph_ca.py`
- `scripts/run_lattice_gas_ca.py`
- `scripts/run_orbit_ca.py`
- `scripts/run_population_ca.py`

Direct repo check used in this audit:

- `hadamard_ca/retained_state_graph.py` explicitly enumerates all `1 << len(actions)` retained-action subsets.
- With the saved retained library in `results/analysis/composite_packet_retained_library.json`, that gives a `512`-state retained graph, matching `results/experiments/order_668_hypergraph_ca/summary.json`.
- A direct enumeration of that saved graph shows that the retained-library optimum `13/2744/480` is attained by exactly two states, `53` and `165`. The hypergraph, lattice-gas, orbit, and successful population runs all land on state `53`.

That direct check matters because it turns the missing-baseline problem from a theoretical concern into a concrete benchmark defect.

## Missing Baselines

### 1. No exhaustive or oracle baseline on the retained graph

The positive post-deepen branches all operate inside a saved `9`-action retained library, hence a `512`-state graph. Yet none of the experiment summaries reports:

- the exact retained-graph optimum,
- the number of optima,
- the shortest-path distance to an optimum from each evaluated start state,
- or a non-CA graph-search baseline over that explicit graph.

Why this matters:

- The current positive pack can only say that some CA-shaped controllers find state `53`.
- It cannot say whether those controllers are doing anything stronger than solving a tiny explicit graph that the repo already materializes exactly.

Falsifiable repair:

- Add one exhaustive retained-graph report with the best objective, all optimal state IDs, and shortest paths from `canonical_frontier` plus every ladder state.
- Add one non-CA planner baseline over the same graph, such as exhaustive BFS, best-first search, or dynamic programming on the retained transitions.

Pass rule:

- Keep strong retained-branch benchmark language only if the CA-style controllers still show an advantage that is not explained by the explicit graph optimum and a trivial graph-search oracle.

### 2. No depth-matched non-CA comparator for the retained-library wins

The hypergraph winner is a `two_step_hyperedge` method. The lattice-gas winner uses precomputed two-step carrier cones. The orbit branch applies a learned rule table over multi-step orbit representatives. But the reported comparators are still mostly depth-`1` or scorer-only:

- hypergraph compares against `pairwise_graph_ca`, `zero_coupling`, `zero_refractory`, and `scorer_only`,
- lattice-gas compares against `lag_greedy_control` and `warning_field_control`,
- orbit compares against `raw_coordinate_baseline` and `scorer_only`.

`results/verification/radius_limited_locality_barrier.md` already certifies that depth-`1` single-actuator rules are blocked on the canonical seed. So beating depth-`1` baselines is necessary, but not benchmark-sufficient.

Falsifiable repair:

- Add unrestricted depth-`2` non-CA search over the same retained actions.
- Add shuffled-pair and no-overlap pair baselines under the same lookup cap.
- Add a carrier-cone baseline that sees the same candidate two-step events as the lattice-gas branch but removes the defect-charge ranking.

Pass rule:

- Keep mechanism claims only if the promoted branches beat depth-matched non-CA search, not just depth-`1` local controls.

### 3. H1 is still missing CA-off mechanism baselines

The old H1 pilot remains a fair branch-kill test, but not a benchmark-grade mechanism study. The canonical frontier pack still lacks matched H1 variants with:

- zero coupling,
- zero refractory,
- scorer-only packet selection,
- fallback disabled.

Falsifiable repair:

- Re-run the full control batch plus the canonical frontier seed with full H1 and the four CA-off variants above.

Pass rule:

- If full H1 does not beat its own CA-off variants on exact hit rate or on median terminal support plus `max_abs`, drop any CA-mechanism claim and keep H1 as a negative control only.

## Missing Controls And Ablations

### 1. The retained library is target-tuned to the evaluation seed

`results/analysis/composite_packet_retained_library.json` records:

- `source_seed_file = results/frontier/order_668_64m/seed_sequences.json`
- a selection rule based on the **frontier** low-splash composite set.

Hypergraph, lattice-gas, orbit, and population all consume that same frontier-tuned library.

Why this matters:

- The action basis was selected on the same canonical frontier representative that later becomes the main evaluation target.
- This is not a held-out feature space.

Falsifiable repair:

- Freeze one retained library from disjoint controls or from a separate frontier split, then rerun the current branches unchanged on the canonical frontier and the ladder.

Pass rule:

- Keep the retained-library story only if the same `13/2744/480` improvement survives library freezing on data that excludes the evaluation representative.

### 2. The hypergraph ladder is method-selected, not benchmark-neutral

`scripts/run_hypergraph_ca.py` builds the ladder with `graph.structural_barrier_states(limit=6)`. In `hadamard_ca/retained_state_graph.py`, a structural barrier state is defined by:

- no improving immediate retained action, and
- at least one improving two-step causal-cone hyperedge.

So the five non-canonical ladder states are mined to satisfy the promoted method's success condition.

Why this matters:

- The `6/6` hypergraph win statement is not a held-out win rate.
- Five of those six states were selected precisely because immediate methods fail and a two-step cone escape exists.

Falsifiable repair:

- Evaluate on all barrier states, or on a predeclared random/stratified sample chosen before probing hyperedges.

Pass rule:

- Report held-out win rate over that neutral set, not only over the mined six-state ladder.

### 3. Orbit CA has direct training/evaluation leakage

`results/experiments/order_668_orbit_ca/training_manifest.json` and `scripts/run_orbit_ca.py` show that the orbit rule table is trained on:

- all three controls, and
- `barrier_ladder_01` through `barrier_ladder_04`.

The reported outcome table then scores those same ladder states.

Why this matters:

- The headline `6/6` orbit win is not a clean generalization result.
- Most of the frontier perturbation suite is partially in-sample.

Falsifiable repair:

- Rerun orbit CA with controls-only training.
- Then rerun with leave-one-ladder-state-out training so each evaluated ladder state is held out from rule construction.

Pass rule:

- Keep the orbit generalization claim only if the held-out ladder wins remain.

### 4. Population CA tunes on the same frontier ladder it later evaluates

`scripts/run_population_ca.py` constructs `results/analysis/frontier_population_phase_map.md` by sweeping:

- `coupling_strength` over `(0.0, 0.8, 1.6)`,
- `contraction_threshold` over `(0.35, 0.42, 0.55)`,
- using the canonical frontier plus the full ladder,
- on seeds `(11, 13, 17)`.

The chosen operating point is then hard-coded as:

- coupling `1.6`,
- threshold `0.42`,

and evaluated on the same frontier family with seeds `(11, 13, 17, 19, 23)`.

Why this matters:

- The operating point is not frozen on a held-out validation split.
- The evaluation is partly tuned on the test family.

Falsifiable repair:

- Choose the operating point on controls only, or on a disjoint validation split of frontier states and seeds, then rerun on untouched test states/seeds.

Pass rule:

- Keep any population robustness language only if the chosen operating point still beats zero coupling on the held-out split.

### 5. Orbit and population have no held-out control family for rule learning

Both learned-rule branches train on all three available controls:

- `control_n5_q0`,
- `control_n7_q0`,
- `control_n9_hardest_pair`.

Nothing is reserved as a genuine validation or test control family.

Falsifiable repair:

- Hold out at least one control family from rule construction and use it as a blind control evaluation set.

Pass rule:

- Keep learned-rule claims only if performance survives that hold-out.

### 6. H1 control and frontier coverage is still too narrow

The original H1 benchmark still rests on:

- two tiny solved controls (`n=5`, `n=7`),
- one canonical frontier seed,
- one RNG seed (`17`),
- one budget (`80`),
- one restart perturbation setting (`restart_packet_flips = 2`).

Falsifiable repair:

- Add harder multi-flip/high-support controls.
- Add nearby frontier perturbations and symmetry-equivalent representatives.
- Add budget, seed, and restart sweeps.

Pass rule:

- Keep any method-level H1 claim only if it survives the wider grid.

### 7. The H1 near-exact stop gate is still under-supported by executed restart coverage

`results/verification/benchmark_gate.md` requires the near-exact comparison to hold across the run distribution. But in the saved frontier batch:

- H1 completes `3/3` restarts,
- `stochastic_hillclimb` completes `3/3`,
- `greedy`, `tabu`, and `simulated_annealing` complete only `1/3`.

So the reported medians are not drawn from matched restart exposure for every method.

Why this matters:

- The branch-kill decision is still directionally reasonable because H1 had more restart exposure and still failed.
- It is not benchmark-grade evidence for a distributional near-exact ordering.

Falsifiable repair:

- Rerun with a fixed per-restart cap, or require every method to complete the same number of restarts before applying the median support/magnitude gate.

Pass rule:

- Keep the near-exact stop claim only if H1 still loses under equal executed restart coverage.

### 8. H1 was never benchmarked against the certified depth-2 escape class

`results/verification/radius_limited_locality_barrier.md` upgrades the locality story materially:

- depth-`1` single-actuator rules are blocked,
- the first certified escape appears at radius `1`, depth `2`, on the retained hyperedge `[3, 7]`.

But the saved H1 benchmark and sensitivity probe never test H1 against that escape class. The current H1 family still operates as a single-packet pressure policy with `max_active_packets = 1` in the saved frontier config.

Why this matters:

- Without one H1-family ablation that can schedule the certified retained hyperedge, the claimed `locality failure` can still be criticized as `policy failure`.

Falsifiable repair:

- Add one H1 ablation that can explicitly schedule the certified retained-hyperedge pair, or add a small overlapping two-step beam over retained actions.

Pass rule:

- If the H1 family still cannot improve `13/2880/512` after that ablation, the locality-failure interpretation becomes materially stronger.

## Missing Error Analysis

### 1. The positive branches collapse to one winning state and one action sequence

On the canonical frontier:

- hypergraph reaches state `53`,
- lattice-gas reaches state `53`,
- orbit reaches state `53`,
- population reaches state `53` on its successful seeds.

The canonical hypergraph, lattice-gas, and orbit traces all use the same action sequence `[3, 7]`, i.e. the same retained two-step move.

Why this matters:

- The current positive evidence is one retained-library escape rediscovered by several wrappers.
- That is weaker than showing multiple independent wins or a broader mechanism class.

Falsifiable repair:

- Report the number of distinct winning states and distinct winning action sequences across branches.
- Add a check for whether the second retained optimum (state `165`) is ever found under blind evaluation.

Pass rule:

- Keep broad mechanism language only if the benchmark shows more than one non-equivalent win.

### 2. The post-deepen branches have no run-level runtime audit comparable to the old H1 pack

`results/verification/runtime_audit.md` explicitly covers only:

- `results/experiments/controls/runs/`
- `results/experiments/order_668_64m/runs/`

There is no equivalent provenance audit for:

- `order_668_hypergraph_ca`,
- `order_668_lattice_gas`,
- `order_668_orbit_ca`,
- `order_668_population_ca`.

Falsifiable repair:

- Extend the runtime audit schema to every post-deepen branch.
- Include per-run seed/config/code digests, explicit output semantics, and replay-meaningful traces.

Pass rule:

- Treat the post-deepen branches as publication-grade only after the newer run families are audited to the same standard as the original H1/control batch.

### 3. H1 still has a real work-accounting gap

The raw H1 frontier run records:

- `objective_evaluations = 32`
- `metadata.ca_field_evaluations = 10354`
- `wall_seconds = 2.129...`

while the matched non-CA baselines report only `objective_evaluations` plus much smaller wall-clock times.

Why this matters:

- Accepted objective evaluations do not charge H1's dense field rescoring fairly.
- The current H1 comparison is usable for branch elimination, but not for publication-grade cost claims.

Falsifiable repair:

- Report both objective-evaluation counts and field-evaluation counts for H1-like methods, or normalize comparisons by wall-clock time under fixed hardware.

Pass rule:

- Keep cost or competitiveness language only if the H1 negative result survives fair work accounting.

### 4. Population failure is stronger than the summary text says, but the report does not expose it directly

The saved canonical-frontier population runs show that the coupled and zero-coupling methods match exactly on every seed:

- both reach state `53` on seeds `11`, `19`, and `23`,
- both stay at state `0` on seeds `13` and `17`.

This is a benchmark-positive point for the audit because it makes the negative result robust, but the summary only states equal medians and contraction counts.

Falsifiable repair:

- Add per-seed comparison tables for the population branch rather than median-only reporting.

Pass rule:

- Keep the branch-level negative result as robust only if the per-seed equality remains under held-out tuning and additional seeds.

### 5. H1 diffusion is described qualitatively but not instrumented well enough to explain

The saved H1 summary correctly notes the diffusion pattern:

- best objective stays at the seed,
- later restart terminals spread support above `13`,
- `l1` and `max_abs` can still drop.

But the raw trace schema is too thin to show *why* that happens. It records accepted states and CA-specific fields such as active packets and pressures, but it does not expose step-wise support deltas, changed-lag counts, spill outside the intended lag mask, or a clear separation between restart perturbation effects and CA update effects.

Falsifiable repair:

- Extend the H1 trace with per-step `support_delta`, changed-lag count, spill/out-of-mask mass, and an explicit source label for `restart_perturbation` versus `ca_update`.

Pass rule:

- Keep the diffusion mechanism story only if those added trace fields show the same spill signature recurring across failed restarts.

## Missing Stress Tests

### 1. No retained-branch budget sweep

The positive retained-library branches are all reported at `lookup_budget = 256` and nowhere else.

Falsifiable repair:

- Rerun at a small grid such as `64`, `128`, `256`, and `512`.

Pass rule:

- Keep robustness language only if the same ordering survives the budget sweep.

### 2. No tie-breaking or action-order stress test for the deterministic retained branches

Hypergraph, lattice-gas, and orbit are each reported as one deterministic trajectory per start state. There is no test that perturbs:

- action ordering,
- orbit priority ties,
- carrier ranking ties,
- or equal-score choice rules.

Falsifiable repair:

- Add randomized tie-breaking or shuffled priority variants for each deterministic branch.

Pass rule:

- Keep mechanism claims only if the same winning state/objective survives those perturbations.

### 3. No held-out frontier perturbation suite independent of the construction pipeline

Current frontier evaluation states are:

- the canonical frontier seed, and
- a five-state ladder derived from the retained library and the hypergraph barrier logic.

This is not an independent perturbation suite.

Falsifiable repair:

- Predeclare a fresh frontier perturbation set that is sampled before retained-library and hypergraph analysis, then rerun all retained branches on that set.

Pass rule:

- Keep transfer or robustness claims only if the same ordering survives on the untouched perturbation suite.

## Publication-Quality Claim Status

- `H1_defect_syndrome_ca_64m`: benchmark-grade negative control for internal gating, not a publication-grade mechanism or cost comparison.
- `H_causal_cone_hypergraph_ca_668`: promising retained-library counterexample, but not a publication-grade benchmark because the evaluation suite is method-selected and the baselines are depth-mismatched.
- `H_defect_charge_lattice_gas_167`: best framed as a reinterpretation of the same retained escape, not as an independently benchmarked advance.
- `H_orbit_quotient_ca_668`: not publication-grade until the frontier perturbation leakage is removed from training.
- `H_population_self_stabilizing_ca_668`: negative claim supported; positive self-stabilization claim rejected.

## Highest-Value Falsifiable Repairs

1. Add an exhaustive retained-graph benchmark.
   Report the exact optimum, all optimal states, shortest paths, and a non-CA planner baseline over the saved `512`-state graph.

2. Remove target leakage from the post-deepen evaluation stack.
   Freeze the retained library off-target, train orbit on controls only or leave-one-state-out, and tune population on a separate validation split.

3. Depth-match the retained-branch comparators.
   Compare hypergraph, lattice-gas, and orbit against unrestricted depth-`2` non-CA search under the same lookup budget.

4. Expand the held-out stress suite.
   Add fresh frontier perturbations, harder controls, budget sweeps, RNG/tie-break sweeps, and symmetry-representative checks.

5. Extend runtime and provenance auditing to the post-deepen branches.
   Keep the same explicit audit standard already used for the original control/H1 batch.

If those five repairs fail, the right publication framing is narrower: one explicit depth-`1` locality barrier, one retained-library depth-`2` escape, one symmetry-transfer sketch with leakage caveats, and one failed population robustness branch. If they pass, the benchmark story becomes materially stronger and falsifiable rather than rhetorical.
