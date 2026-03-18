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
