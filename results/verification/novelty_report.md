# Novelty Report

Verification phase: `post_deepen`

## Scope

This pass reads the required context files plus the live post-H1 paper and code artifacts:

- `results/research_context.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/swarm/director_brief.md`
- `research_paper.tex`
- `results/writeup/claims_table.md`
- `results/writeup/methods_brief.md`
- `results/branches/H_causal_cone_hypergraph_ca_668.md`
- `results/branches/H_defect_charge_lattice_gas_167.md`
- `results/branches/H_orbit_quotient_ca_668.md`
- `results/branches/H_population_self_stabilizing_ca_668.md`
- `results/experiments/order_668_hypergraph_ca/summary.md`
- `results/experiments/order_668_lattice_gas/summary.md`
- `results/experiments/order_668_orbit_ca/summary.md`
- `results/experiments/order_668_population_ca/summary.md`
- `results/verification/radius_limited_locality_barrier.md`
- `results/verification/family_leakage_audit.md`
- `hadamard_ca/h1_ca.py`
- `hadamard_ca/retained_state_graph.py`
- `hadamard_ca/lag_lattice_gas.py`
- `hadamard_ca/orbit_ca.py`
- `hadamard_ca/population_ca.py`
- `scripts/run_hypergraph_ca.py`
- `scripts/run_orbit_ca.py`

Closest literature anchors used in this comparison:

- Eliahou, *A 64-Modular Hadamard Matrix of Order 668* (2025)
- Tsompanas et al., *Cellular Automata Applications in Shortest Path Problem* (2018 chapter / 2017 preprint line)
- Suksmono, *Finding a Hadamard Matrix by Simulated Quantum Annealing* (2018)
- Suksmono and Minato, *Finding Hadamard Matrices by a Quantum Annealing Machine* (2019)
- Bright et al., *The SAT+CAS method for combinatorial search with applications to best matrices* (2019)
- Mariot et al., *Mutually Orthogonal Latin Squares Based on Cellular Automata* (2020)
- Gadouleau, Mariot, and Picek, *Bent Functions from Cellular Automata* (2020)
- self-organizing / neural CA line, represented here by Sudhakaran et al., *Goal-Guided Neural Cellular Automata* (2022)

## Overall Assessment

The claimed contribution is materially distinct from prior art only after narrowing.

What survives as genuinely distinct is:

- a seed-specific exact barrier/counterexample result on top of Eliahou's published `64`-modular order-`668` frontier object, and
- an honest negative robustness result for the population branch.

What does **not** yet survive cleanly as a materially distinct method contribution is the stronger claim that the post-H1 hypergraph, lattice-gas, and orbit branches establish a new CA-style Hadamard search family. Those branches reuse one tiny retained nine-action library, one retained-state graph, one favorable perturbation ladder, and mostly compare pair-capable methods against single-action baselines. That is enough to support a narrow structural result. It is not yet enough to support a broad "distinct CA method" or "transfer/generalization" claim.

## Major Claim Checks

### 1. Seeded order-668 frontier work

- Closest paper or line:
  - Eliahou (2025)
  - Suksmono (2018, 2019) as the closest direct Hadamard-search heuristic line
- Assessment:
  - Not novel by itself.
  - The repo contributes no new order-`668` seed, no exact witness, and no exact improvement over the published seed.
- Concrete overlap signals:
  - The canonical q/s seed and the `13` exceptional coefficients come directly from the Eliahou frontier object.
  - All successful branches still end at a non-exact state `13/2744/480`, not at an exact Hadamard witness.
- Surviving claim:
  - Distinct only as downstream experimentation on top of the published near-solution.

### 2. H1 as a CA repair method

- Closest paper or line:
  - Tsompanas et al. for CA-as-search methodology
  - Suksmono (2018, 2019) for heuristic Hadamard search
- Assessment:
  - H1 survives as a valid negative control, not as a materially distinct CA method contribution.
- Concrete overlap signals:
  - `hadamard_ca/h1_ca.py` still computes exact per-packet deltas over all `334` packets before coupling and refractory logic are applied.
  - The benchmark pack still lacks matched CA-off ablations on the same frontier seed.
  - The saved H1 batch remains one canonical seed, one RNG seed, and narrow restart coverage.
- Surviving claim:
  - "Seeded CA falsification scaffold" is defensible.
  - "New CA repair method for order 668" is not.

### 3. Exact depth-1 locality barrier and first depth-2 counterexample

- Closest paper or line:
  - Bright et al. (2019) and the broader exact combinatorial-search / certification line
- Assessment:
  - This is the strongest real novelty in the package.
  - It is materially distinct if phrased narrowly: an exact checked-class barrier plus the first certified escape on one published frontier seed.
- Concrete overlap signals:
  - The barrier checker explicitly certifies no improvement among all `334` one-packet moves, all `55,611` unordered two-packet moves, and all `9` retained composites.
  - The first certified escape is a radius-`1`, depth-`2` retained cone ending at `13/2744/480`.
- Weak differentiation:
  - The theorem is seed-limited and actuator-class-limited.
  - "Locality barrier" is safe only when immediately qualified as "in the checked class on the canonical seed."
- Surviving claim:
  - Acceptable as a narrow barrier/counterexample theorem.

### 4. Hypergraph CA as a new method win

- Closest paper or line:
  - Tsompanas et al. for CA-for-search shape
  - graph / hypergraph local-neighborhood search over precomputed move libraries
- Assessment:
  - Weakly differentiated as a CA-method claim.
  - Stronger as evidence that the retained graph contains an improving depth-2 local cone.
- Concrete overlap signals:
  - `scripts/run_hypergraph_ca.py` sets `lookup_budget = max(256, graph.lookup_cost_for_full_hypergraph_scan())`, so the canonical run is budgeted to sweep the full retained cone set.
  - `_run_hypergraph_method(...)` scores every admissible 2-step cone and takes the global best improving cone.
  - The comparison baselines in the same script (`pairwise_graph_ca`, `zero_coupling`, `zero_refractory`, `scorer_only`) are all `single_action`.
  - The ladder itself is selection-conditioned: states are kept only if they have no immediate retained-action improvement but do have at least one improving 2-step cone.
- Consequence:
  - The current evidence supports "exact retained-cone counterexample exists and can be replayed by the hypergraph rule."
  - It does **not** yet isolate a distinct CA mechanism from a same-library exhaustive 2-step scorer.

### 5. Lattice-gas branch as independent novelty

- Closest paper or line:
  - lattice-gas / conservative CA line
  - nearest in-package comparator is the same retained-cone counterexample already found by the hypergraph branch
- Assessment:
  - Moderately distinct as a representation-level reinterpretation.
  - Weak as an independent search novelty claim.
- Concrete overlap signals:
  - `hadamard_ca/lag_lattice_gas.py` uses the same retained graph and the same 2-step carrier cones once single actions are blocked.
  - The branch reaches the same end state `13/2744/480` as hypergraph CA.
  - Its controls (`lag_greedy_control`, `warning_field_control`) remain single-action only.
  - The family-leakage audit is useful and important, but it only rules out collapse into a short list of known structured families; it does not prove an independently novel search space.
- Surviving claim:
  - "Lag-space reinterpretation of the same local escape" is defensible.
  - "Second independent discovery of a new CA search mechanism" is too strong.

### 6. Orbit quotient transfer and generalization

- Closest paper or line:
  - symmetry-reduced / orbit-representative search in combinatorial optimization
  - structured-family exact-search line as a ceiling for what "transfer" would need to mean rigorously
- Assessment:
  - This is the most novelty-fragile positive claim.
  - The compression idea is real, but the present transfer story is partly trained-on and partly selection-conditioned.
- Concrete overlap signals:
  - `results/experiments/order_668_orbit_ca/training_manifest.json` shows the rule table was trained not only on controls but also on four frontier perturbation states from the same ladder.
  - `scripts/run_orbit_ca.py` evaluates orbit representatives built from single actions **and** 2-step carriers, but compares them to `raw_coordinate_baseline` and carried-over `scorer_only` runs that are both single-action only.
  - The perturbation suite is inherited from the hypergraph ladder, which was already filtered to contain improving 2-step cones.
- Consequence:
  - The current evidence supports "the same retained counterexample family can be compressed into orbit signatures and replayed on the curated ladder."
  - It does **not** yet support a strong generalization or holdout-transfer claim.

### 7. Population self-stabilization

- Closest paper or line:
  - self-organizing / neural CA line, represented here by Sudhakaran et al. (2022)
- Assessment:
  - Low novelty-inflation risk, because this branch fails honestly.
  - It does not establish a self-organization advantage over zero-coupling.
- Concrete overlap signals:
  - Coupled and zero-coupling medians tie on the canonical seed and across the ladder.
  - The coupled branch records zero strict ladder wins over zero-coupling.
- Surviving claim:
  - "Population self-stabilization does not separate from zero-coupling in the saved regime" is supported.

## Strongest Novelty Illusions

- "Cellular automata are new for Hadamard search."
  - Not defensible against Tsompanas-style CA-for-search work or CA-based combinatorial-design work such as Mariot et al. and Gadouleau et al.

- "The post-H1 branches are three independent confirmations."
  - Weak.
  - Hypergraph, lattice-gas, and orbit all reuse the same retained nine-action library and land on the same six-packet target state.

- "The hypergraph branch proves a distinct CA mechanism."
  - Weak in the current implementation.
  - The canonical run is effectively a full retained-cone sweep with global best-cone selection, while the baselines are single-action only.

- "The orbit branch proves out-of-sample transfer."
  - Weak.
  - The rule table excludes the canonical seed, but it is trained on four frontier-neighbor ladder states from the same curated perturbation family.

- "The barrier proves locality is fake in general."
  - Too broad.
  - What is certified is a barrier for the explicit checked actuator class on the canonical seed.

- "The family-leakage audit by itself establishes broad novelty."
  - False.
  - It rules out several important structured-family collapses, but it does not by itself prove a new search family.

## Weak Differentiation and Missing Gap Evidence

- Missing same-library 2-step non-CA baseline.
  - This is the biggest gap for the positive post-H1 branches.
  - The current comparisons mostly test pair-capable methods against single-action baselines.

- Missing unbiased perturbation suite.
  - The ladder is built from structural-barrier states that already contain improving 2-step cones.
  - That is useful for mechanism diagnosis, but weak for generalization claims.

- Missing holdout evaluation for orbit transfer.
  - Leave frontier perturbations out of training, then test on a fresh nearby-seed suite not selected by the improving-cone filter.

- Missing alternative local actuator family.
  - The retained library is deliberately tiny.
  - Without at least one slightly larger or differently constructed local family, the barrier can be misread as more general than it is.

- Missing post-H1 claim inventory discipline.
  - `results/writeup/claims_table.md` is still mostly H1-scoped while the manuscript now foregrounds barrier, hypergraph, lattice-gas, orbit, and population claims.

- Missing literature-positioning precision.
  - The narrow novelty framing is mostly correct, but still lives too much in author synthesis rather than one explicit prior-art gap table.

## Bottom Line

The materially distinct contribution is **not** "cellular automata solve or substantially advance Hadamard order 668." It is narrower:

- an exact checked-class barrier on the published order-`668` frontier seed,
- the first certified retained-cone local counterexample crossing that barrier,
- a lag-space reinterpretation and an orbit-signature compression of the same escape,
- and an honest negative result for the population robustness story.

If the paper is rewritten around that narrow barrier/counterexample contribution, the novelty case is defensible. If it insists on stronger claims about a new CA method family, independent branch confirmation, or orbit-level transfer/generalization, the present evidence is still too thin.

VERDICT: REVISE
