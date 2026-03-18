# Lattice-Gas CA Summary

Defect-charge lattice-gas CA on the exact lag core with retained composite actuators on the frontier seed.

## Setup

- Frontier seed: `results/frontier/order_668_64m/seed_sequences.json`
- Retained frontier library: `results/analysis/composite_packet_retained_library.json`
- Harder control seed: `results/experiments/controls/seeds/control_n9_hardest_pair.json`
- Lookup budget per run: `256` transition lookups.
- Warning field: decay `1`, boost `2`, cap `8`.
- Reservoir cap for carrier acceptance: `16`.

## Canonical Frontier

- `defect_charge_lattice_gas_ca`: best `13/2744/480`, accepted updates `1`, lookups `242`.
- `lag_greedy_control`: best `13/2880/512`, accepted updates `0`, lookups `9`.
- `warning_field_control`: best `13/2880/512`, accepted updates `0`, lookups `9`.

## Harder Control

- `defect_charge_lattice_gas_ca`: best `0/0/0`, accepted updates `2`, lookups `36`.
- `lag_greedy_control`: best `0/0/0`, accepted updates `2`, lookups `54`.
- `warning_field_control`: best `0/0/0`, accepted updates `2`, lookups `54`.

## Leakage Audit

- `Williamson`: `pass`. The winning state is not constrained to the symmetric / amicable packet relations characteristic of Williamson-type subfamilies, and the branch never hard-codes them.
- `Turyn`: `pass`. The branch uses only exact lag-delta transport features and never introduces supplementary-sequence identities or multiplication templates.
- `Goethals-Seidel`: `pass`. The repo-wide Goethals-Seidel lift remains the shared evaluation harness only. No branch rule restricts the search to a Goethals-Seidel family subspace.
- `cocyclic`: `pass`. No cocycle coordinates, group generators, or `D_{4t}` constraints appear in the state, candidate generation, or acceptance rule.
- `block_circulant`: `pass`. The improved state has no nontrivial period in any derived channel, so the trajectory does not collapse into a block- or quasi-circulant template.

## Verdict

- The lattice-gas branch survives this item: on the canonical frontier seed it reaches `13/2744/480`, while both single-action lag-space controls stay at `13/2880/512`.
