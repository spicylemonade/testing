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
