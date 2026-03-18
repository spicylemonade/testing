# Concept Delta

## 2026-03-18: Evolve Pass -> Branch Selection

- Suggestion:
  - `defect_syndrome_ca_64m` as the main concept, with `lag_residue_ca_167` as backup and `spacetime_row_emission_search` / learned-NCA variants as reserve.
- Implementation:
  - Repaired the local `concept_evolve.py evolve()` call path, ran the mandatory evolve pass, and kept the generated 11-node concept tree under `results/concept_evolve/tree/`.
  - Used the resulting tree plus the swarm reassessment to write `results/swarm/selection_note.md` and update `results/literature/prior_art_gap.md`.
- Result:
  - `H1_defect_syndrome_ca_64m` remains selected as the initial branch.
  - `H2_lag_space_ca_167` remains backup-only.
  - `H3_spacetime_row_emission_ca` remains reserve-only.
- Novelty Delta:
  - The evolve pass widened the design space, but recovering the 2025 frontier paper narrowed the defensible novelty claim.
  - The surviving claim is not "CA for Hadamard matrices is new"; it is "seeded CA repair on the recovered order-668 64-modular frontier object may be new enough to test against matched non-CA controls."

## 2026-03-18: Probe Checkpoint -> H1 Implementation

- Suggestion:
  - Probe the main H1 bottleneck directly: can a genuinely local defect-syndrome CA in the compact q/s packet space stay distinct from generic local search while still helping on the recovered order-668 seed?
- Implementation:
  - Ran the mandatory `python3 .archivara/concept_evolve.py probe ...` checkpoint.
  - Read the final `results/concept_evolve/probe_result.json`, including its anomaly checks, steering directions, and validation checks.
  - Used that probe checkpoint plus the saved swarm notes to tighten the concrete H1 branch in `hadamard_ca/h1_ca.py`, its config/brief under `results/branches/`, and the H1 precheck.
- Result:
  - H1 now runs in a compressed `334`-packet + sparse lag-syndrome state, not on the raw `668 x 668` matrix.
  - The branch reaches exactness on the small non-exact length-`7` smoke seed through the intended runner path.
  - The probe supplied the strongest new structural constraint so far: the current single-bit packet basis is frozen on the canonical seed, with no improving one-packet or two-packet moves in the recorded neighborhood.
  - A frontier micro-smoke on the canonical order-668 seed runs successfully and exposes the same practical risk from another angle: support diffusion can accompany smaller `l1` and `max_abs`.
- Novelty Delta:
  - The concrete contribution is now sharper than the earlier concept card: a spill-penalized packet-lattice CA over the real order-668 frontier seed, benchmarked in the same q/s coordinates as the non-CA baselines, with the probe pushing the next step toward composite packets or a defect-packet graph.
  - The unresolved novelty risk is also sharper: if the branch responds to the frozen frontier only by widening score scans or tuning the same dead single-bit basis, it collapses back toward generic local search rather than surviving as a distinct CA repair method.

## 2026-03-18: Reframe Checkpoint -> Matched Control Batch

- Suggestion:
  - Reframe the next experiment around the narrowest verification debt: do the CA and non-CA methods behave differently at all when they start from the same small, solved q/s controls under the same restart and budget contract?
- Implementation:
  - Ran the mandatory `python3 .archivara/concept_evolve.py reframe "solve Hadamard 668. method which hasn't been tried is cellar automata. try that as a method to find it"` checkpoint.
  - Read the persisted `results/concept_evolve/reframings.json`, which widened into ten cross-domain framings; the strongest ones pointed toward graph CA defect networks, LDPC-style weighted bit-flip repair, and excitable defect-wave scheduling.
  - Executed the locked two-seed control batch under `results/experiments/controls/` with identical evaluation budget, restart count, and RNG seed for `H1_defect_syndrome_ca_64m`, `greedy`, `tabu`, `simulated_annealing`, and `stochastic_hillclimb`.
- Result:
  - The control batch now has reproducible configs, seeds, raw run logs, and aggregate summaries under `results/experiments/controls/`.
  - H1 matches `greedy` and `tabu` on exact-hit rate across the two controls and outperforms `simulated_annealing` and `stochastic_hillclimb` on the harder length-7 control under the shared budget.
- Novelty Delta:
  - The reframe pass did two useful things at once: it forced the evidence standard tighter and it widened the bridge space away from raw single-packet CA scheduling.
  - H1 still does not have a frontier advantage, but it now clears the minimal control-validity gate needed before a fair order-668 kill test.

## 2026-03-18: Iterate Checkpoint -> Post-Verification Tree Refresh

- Suggestion:
  - After the verification pack exists, retire the dead single-packet branch, promote `H2_lag_space_ca_167` as the champion branch, use `ldpc_hadamard_decoder_graph` as the strongest bridge into honest locality, and keep generative CA ideas out of the immediate queue.
- Implementation:
  - Launched the mandatory `python3 .archivara/concept_evolve.py iterate "solve Hadamard 668. method which hasn't been tried is cellar automata. try that as a method to find it"` checkpoint.
  - The iterate helper stalled before item_022 could rely on emitted JSON artifacts, so the bridge refresh was reconstructed directly from the same saved verification inputs: `results/concept_evolve/probe_result.json`, `results/concept_evolve/reframings.json`, `results/swarm/falsifier.md`, `results/verification/verification_summary.md`, `results/verification/novelty_report.md`, `results/verification/benchmark_report.md`, `results/verification/citation_audit.md`, and the H2/H3 gate notes.
  - Refreshed the targeted concept READMEs plus `bridge_candidates.json`, `concept_delta.json`, and `recurrent_state.json` to encode that verified branch state.
- Result:
  - `001_defect-syndrome-ca-64m` is now archived as a negative control rather than an active frontier branch.
  - `002_lag-residue-ca-167` is now the champion branch for the next pass.
  - `008_ldpc-hadamard-decoder-graph` is promoted as the strongest bridge candidate feeding the H2 pivot.
  - `011_spacetime-row-emission-search` remains closed for this pass.
- Novelty Delta:
  - The surviving novelty claim has shifted again: away from “single-packet CA repair on q/s coordinates” and toward “representation-changing locality repair on lag fields or sparse defect graphs.”
  - That is narrower, more defensible, and much closer to the real blocker exposed by the matched frontier batch.

## 2026-03-18: Probe Refresh -> Composite Packet Atlas

- Suggestion:
  - Answer the current open actuator question directly: if packet-space CA is still alive after H1, it must live on a retained low-splash composite basis rather than on the frozen one-packet library.
- Implementation:
  - Launched a fresh mandatory `concept_evolve.py probe` on the composite-library question. The helper refreshed `results/concept_evolve/probe_result.json` with composite-library guidance but never exited cleanly, so the run used that refreshed probe artifact together with a direct exhaustive scan instead of waiting on the stalled helper.
  - Added `hadamard_ca/composite.py` and `scripts/generate_composite_locality_atlas.py`.
  - Generated `results/analysis/composite_packet_locality_atlas.md`, `results/analysis/composite_packet_locality_atlas.json`, `results/analysis/composite_packet_retained_library.json`, and `results/experiments/controls/seeds/control_n9_hardest_pair.json`.
- Result:
  - The exhaustive frontier scan over symmetry-safe unordered `2`-packet composites, channel-complete `4`-packet composites, and width-1 run-boundary composites found a nonempty retained basis.
  - The retained frontier library is a 9-action Pareto set with changed-lag median `9`, well below the half-median cutoff `25.5`.
  - On the canonical order-668 seed the retained basis is still negative: `0` improving composites, `1` exactly neutral composite, and `8` Pareto-worse composites.
  - On the deterministic harder length-`9` control, low-splash pair and balanced-four composites do improve the seed, so the frontier result is not an artifact of a vacuous scan.
- Novelty Delta:
  - This changes the live CA claim again: the packet-space direction is now only defensible as a retained composite actuator library, not as single-packet local CA.
  - That is a materially sharper negative-positive split than the repo had before. The new evidence says "composite locality exists in principle, but the actual order-668 frontier still blocks improvement inside that local basis."

## 2026-03-18: Reframe Refresh -> Causal-Cone Hypergraph Branch

- Suggestion:
  - Move locality from a static retained action graph to short-horizon dynamics: if single retained composites are still frontier-frozen, test whether exact `2`-step local cones on that retained graph can cross the barrier.
- Implementation:
  - Ran the mandatory `concept_evolve.py reframe "solve Hadamard 668. method which hasn't been tried is cellar automata. try that as a method to find it"` checkpoint, which refreshed `results/concept_evolve/reframings.json` toward decoder graphs, local decoders, warning propagation, and number-conserving transport ideas.
  - Added `hadamard_ca/retained_state_graph.py` and `scripts/run_hypergraph_ca.py`.
  - Built the exact retained-library quotient with `9` retained actions and `512` unique packet-parity states, then ran the fixed `2`-step causal-cone hypergraph rule against `pairwise_graph_ca`, `zero_coupling`, `zero_refractory`, and `scorer_only`.
  - Saved the branch brief under `results/branches/H_causal_cone_hypergraph_ca_668.md` and the experiment pack under `results/experiments/order_668_hypergraph_ca/`.
- Result:
  - The canonical frontier seed is a structural barrier state for every single-action retained-basis baseline: no baseline can leave `13/2880/512`.
  - The hypergraph branch accepts one precomputed local cone `[3, 7]` and reaches `13/2744/480` on the canonical seed.
  - The same fixed rule also wins on every ladder state selected by the structural criterion “no immediate improvement but at least one improving 2-step cone.”
- Novelty Delta:
  - This is the first branch in the repo that turns the retained composite library into a genuine frontier-improving local dynamic rather than another negative pilot.
  - The surviving novelty claim is now sharper and stronger: not “cellular automata might help in general,” but “a fixed short-horizon hypergraph CA over a retained low-splash action basis can beat every matched single-action retained-basis control on the real order-668 frontier seed.”

## 2026-03-18: Verification Refresh -> Radius-Limited Counterexample

- Suggestion:
  - Convert the old H1 freeze into a stronger certified statement: either prove a broader local-rule barrier or identify the first explicit local counterexample class that really escapes it.
- Implementation:
  - Added `scripts/check_radius_limited_locality_barrier.py`.
  - Verified the canonical seed against the explicit single-actuator class consisting of all one-packet moves, all unordered two-packet moves, and all retained composites.
  - Saved the machine-checkable result under `results/verification/radius_limited_locality_barrier.json` and wrote the memo `results/verification/radius_limited_locality_barrier.md`.
- Result:
  - No single actuator in the checked class improves the canonical frontier objective `13/2880/512`.
  - The first certified escape appears at radius `1`, depth `2`, in the retained causal-cone hypergraph class.
  - The earliest counterexample is the local cone `[3, 7]`, which reaches state `53` and improves the objective to `13/2744/480`.
- Novelty Delta:
  - The repo now has more than another negative pilot: it has a clean barrier-plus-counterexample story.
  - That is a stronger scientific contribution than the original H1 result because it identifies exactly where the single-actuator locality barrier holds and exactly where a broader local rule class first breaks it.

## 2026-03-18: Lattice-Gas Refresh -> Defect-Charge Core Branch

- Suggestion:
  - Reinterpret the retained frontier escape as a defect-charge transport process on the exact `167`-lag core, with an explicit continuity law and a hard family-leakage audit instead of another graph-only pilot.
- Implementation:
  - Added `hadamard_ca/lag_lattice_gas.py` plus `scripts/run_lattice_gas_ca.py`.
  - Lifted each retained action and carrier cone into an exact lag-charge transport signature with support flux, reservoir exchange, and nearest-neighbor current span.
  - Ran the new branch on the canonical frontier seed and the deterministic harder length-`9` control, then saved `results/branches/H_defect_charge_lattice_gas_167.md`, `results/experiments/order_668_lattice_gas/summary.{json,md}`, and `results/verification/family_leakage_audit.{json,md}`.
- Result:
  - The fixed lattice-gas rule reaches `13/2744/480` on the canonical frontier seed by accepting the conservative carrier `[(q[53], q[136]), (q[29], s[29], q[114], s[114])]`.
  - Both matched lag-space single-action controls stay frozen at `13/2880/512` on that same frontier seed.
  - On `control_n9_hardest_pair`, the same rule reaches exactness in two accepted updates, so the carrier layer is not compensating for a globally dead single-action basis.
  - The saved family-leakage audit passes the `Williamson`, `Turyn`, `Goethals-Seidel`, `cocyclic`, and `block-circulant` checks for the winning frontier trajectory.
- Novelty Delta:
  - This branch keeps the surviving CA claim alive without falling back to a known structured family: the improvement is now explainable as exact conserved transport on the lag core, not as raw-coordinate packet scheduling alone.
  - The novelty claim remains narrow, but it is materially different from the earlier hypergraph memo because the governing object is now an explicit continuity law on signed defect charge.

## 2026-03-18: Orbit Refresh -> Symmetry-Quotient Rule Transfer

- Suggestion:
  - Remove raw-coordinate memorization from the retained-library dynamics by quotienting candidate events into symmetry-controlled orbit classes and training one orbit rule table away from the canonical frontier seed.
- Implementation:
  - Added `hadamard_ca/orbit_ca.py` plus `scripts/run_orbit_ca.py`.
  - Canonicalized runtime event classes by cyclic index erasure, dihedral reversal invariance, and q/s sign-orientation erasure, then precomputed one canonical representative per orbit at each state.
  - Trained one fixed rule table on solved controls (`n = 5, 7`) plus the harder control and four predefined barrier-ladder perturbation states, but excluded the canonical frontier seed itself from tuning.
  - Saved `results/branches/H_orbit_quotient_ca_668.md` and `results/experiments/order_668_orbit_ca/summary.{json,md}` with the learned rule table and training manifest.
- Result:
  - The orbit quotient CA reaches `13/2744/480` on the canonical frontier seed in `65` orbit-representative lookups, versus the raw single-action retained baseline and `scorer_only`, both stuck at `13/2880/512`.
  - The same unchanged rule also beats those two baselines on every barrier-ladder state, although `barrier_ladder_01` lands on the weaker improved state `13/2880/512` rather than the best retained state.
  - Runtime work is materially smaller than the raw lattice-gas scan because each step inspects orbit representatives instead of every raw candidate.
- Novelty Delta:
  - The live CA claim is now less tied to one coordinate chart: the rule is expressed over orbit-level transport shapes rather than over packet indices.
  - That makes the result more transferable and more defensible against the critique that the branch only memorizes one hand-picked frontier representative.

## 2026-03-18: Population Refresh -> Self-Stabilization No-Go

- Suggestion:
  - Test whether the control-trained orbit rule can be lifted into a true self-stabilizing population CA whose coupling creates a contraction phase that the zero-coupling ablation cannot match.
- Implementation:
  - Added `hadamard_ca/population_ca.py` plus `scripts/run_population_ca.py`.
  - Trained exactly one orbit rule table on non-frontier controls only, then ran equal seed coverage (`11, 13, 17, 19, 23`) for the coupled population CA and the zero-coupling ablation on the canonical frontier seed and the full barrier ladder.
  - Generated `results/branches/H_population_self_stabilizing_ca_668.md`, `results/experiments/order_668_population_ca/summary.{json,md}`, and `results/analysis/frontier_population_phase_map.{json,md}`.
  - Also retried with a persistence-based contraction rule and stronger coupling; the retry never opened a coupling-specific contraction regime and was not promoted as the final artifact.
- Result:
  - The coupled population CA does beat the deterministic single-action local baselines on the canonical seed and several ladder states.
  - However, its median best objective ties the zero-coupling ablation on the canonical seed and on every ladder state.
  - The phase map stays in the diffusion regime across the tested coupling / threshold grid, so the population layer never earns a distinct self-stabilization claim.
- Novelty Delta:
  - This closes one ambitious branch honestly rather than by rhetoric: the repo now has evidence that the stronger locality branches do not automatically lift to a robust population self-stabilizer.
  - The surviving positive contribution is therefore narrower and cleaner: explicit local carrier rules and orbit-level transfer survive, but population-level robustness does not.
