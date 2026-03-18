# Concept: lag_residue_ca_167

- Topic Context: solve Hadamard 668. method which hasn't been tried is cellar automata. try that as a method to find it
- Domains: sequence_design, cellular_automata, message_passing
- Status: promoted as the champion branch for the next pass (`pivot to H2`).

## Implementation Backlog
- [ ] Implement one lag-residue state representation with exact packet-to-lag delta tables.
- [ ] Run the family-leakage audit against Williamson, Turyn, Goethals-Seidel, cocyclic, and block-circulant collapse.
- [ ] Add one matched lag-space non-CA control and one warning-propagation side-field control in the same coordinates.
- [ ] Run one narrow order-668 pilot with exact-hit, terminal support, and terminal magnitude as the gate.

## Promotion Note

- Evidence path:
  - `results/verification/verification_summary.md`
  - `results/verification/novelty_report.md`
  - `results/branches/H2_gate.md`
  - `results/concept_evolve/probe_result.json`
- Promotion reason:
  - the verified H1 failure points to the lag field as the more honest local object
  - H2 is the governed next branch once H1 fails for principled locality reasons
  - this branch stays active only if it survives the family-leakage audit against Williamson, Turyn, Goethals-Seidel, cocyclic, and block-circulant collapse
