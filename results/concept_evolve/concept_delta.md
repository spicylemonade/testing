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

## 2026-03-18: Probe Pass -> H1 Implementation

- Suggestion:
  - Probe the main unresolved question directly: can a genuinely local defect-syndrome CA in the compact q/s packet space beat the matched non-CA controls without collapsing into generic local search?
- Implementation:
  - Ran the mandatory `python3 .archivara/concept_evolve.py probe ...` command on the H1 locality question.
  - Read `results/concept_evolve/probe_result.json` and the generated probe debug/state files.
  - Because the helper run failed with a transport-level parse error rather than a substantive suggestion, proceeded from the saved swarm/concept artifacts and implemented the executable H1 branch in `hadamard_ca/h1_ca.py`, plus the launcher `scripts/run_h1_ca.py` and the branch brief `results/branches/H1_defect_syndrome_ca_64m.md`.
- Result:
  - The probe produced a recorded failure artifact instead of a new concept recommendation.
  - H1 is now an executable packet-lattice / lag-syndrome CA branch with explicit locality knobs, refractory behavior, and shared-harness compatibility.
- Novelty Delta:
  - The failed probe did not widen the claim space; it reinforced the need to keep the novelty claim narrow and evidence-driven.
  - The implemented H1 branch is novel, if at all, only as a seeded defect-repair dynamic on the recovered order-668 frontier object, not as a general CA Hadamard-construction method.
