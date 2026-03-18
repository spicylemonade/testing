# Research Context

- Stage: final_documentation
- Model: gpt-5.4
- Codex model ref: openai/gpt-5.4
- Reasoning effort: xhigh
- Note: the seeded cellular-automaton H1 repair pilot was falsified on the canonical order-668 frontier seed, so the next gated branch is H2 rather than further H1 sweeps.
- Rubric progress: 25/25 completed
- `sources.bib` entries: 17
- Swarm hypotheses: 3
- Verification summary present: yes
- Selected next branch: `H2_lag_space_ca_167` (`lag_residue_ca_167` in the concept tree)
- Exact order-668 Hadamard matrix found: no
- Exact improvement over the published frontier seed: no

## Branch Status
- Retired after the matched frontier kill test: `H1_defect_syndrome_ca_64m`
- Selected for the next gated pass: `H2_lag_space_ca_167`
- Strongest promoted bridge: `LDPC-style decoder graph on a lag/check influence graph`
- Closed for this pass: `H3_spacetime_row_emission_ca`

## Blockers
- Before opening H2, complete the family-leakage audit against `Williamson`, `Turyn`, `Goethals-Seidel` relabeling, `cocyclic`, and `block-circulant` collapse.
- The current order-668 result is a negative seeded-optimizer / falsification scaffold only. There is no exact order-668 witness and no exact improvement over the frontier seed from `eliahou2025_64mod668`.

## Verification Artifacts
- `results/verification/novelty_report.md`: present
- `results/verification/citation_audit.md`: present
- `results/verification/benchmark_report.md`: present
- `results/verification/verification_summary.md`: present; decision `pivot to H2`
- `results/verification/runtime_audit.md`: present

## Canonical Experiment Artifacts
- Frontier seed: `results/frontier/order_668_64m/seed_sequences.json`
- Frontier seed manifest: `results/frontier/order_668_64m/seed_manifest.json`
- Control batch summary: `results/experiments/controls/summary.json`
- Frontier batch summary: `results/experiments/order_668_64m/summary.json`
- Concept-tree state: `results/concept_evolve/recurrent_state.json`
- Reproducibility handoff: `results/writeup/repro.md`

## Closest Prior Art
- `A 64-Modular Hadamard Matrix of Order 668 (2025)` as the frontier seed anchor
- `Cellular Automata Applications in Shortest Path Problem (2017)` as the closest CA-shape warning
- `Finding a Hadamard Matrix by Simulated Quantum Annealing (2018)` and `Finding Hadamard Matrices by a Quantum Annealing Machine (2019)` as direct optimizer comparators
- `The SAT+CAS method for combinatorial search with applications to best matrices (2019)` as the certificate-rich exact-search contrast
