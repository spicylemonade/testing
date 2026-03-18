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
