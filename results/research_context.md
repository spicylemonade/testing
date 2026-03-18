# Research Context

- Stage: `phase_6_closed`
- Model: `gpt-5.4`
- Codex model ref: `openai/gpt-5.4`
- Reasoning effort: `xhigh`
- Rubric progress: `30` completed, `1` failed, `31` total
- Exact order-`668` Hadamard found: `no`
- Best frontier objective reached: `13/2744/480`
- Verification summary present: `yes`
- Family leakage audit present: `yes`
- Population phase map present: `yes`

## Current Interpretation

- The canonical `64`-modular frontier seed remains non-exact; no exact witness of order `668` was found.
- The strongest positive locality result is now narrow and explicit:
  - retained `2`-step local carrier rules improve the published frontier object from `13/2880/512` to `13/2744/480`,
  - the same carrier logic admits a defect-charge continuity-law interpretation on the `167` core,
  - and an orbit-quotient rule table transfers that improvement across the retained perturbation ladder without memorizing raw packet coordinates.
- The strongest negative result is also explicit:
  - single-actuator locality is certified blocked at depth `1`,
  - and the attempted population self-stabilizing lift fails because coupling never beats the zero-coupling ablation under equal seed coverage.

## Live Branch Status

- `H1_defect_syndrome_ca_64m`: retired negative control
- `H_causal_cone_hypergraph_ca_668`: positive local counterexample branch
- `H_defect_charge_lattice_gas_167`: positive continuity-law reinterpretation of the same retained escape
- `H_orbit_quotient_ca_668`: positive symmetry-transfer branch
- `H_population_self_stabilizing_ca_668`: failed robustness branch

## Closest Prior Art

- Cellular Automata Applications in Shortest Path Problem (2017)
- Learning Automata-Based Solutions to the Single Elevator Problem (2019)
- On the possibility of oscillating in the Ebola virus dynamics and investigating the effect of the lifetime of T lymphocytes (2022)
- Engineering Societies in the Agents World (2000)

## Final Position

- The repo now contains a sharper answer to the user’s cellular-automata question than it did at the start:
  - cellular automata did not solve Hadamard `668`,
  - but carefully constrained local CA-style dynamics did find a reproducible frontier improvement over the published `64`-modular object.
- That contribution stays below an exact-solution claim and below a robust population-CA claim.
