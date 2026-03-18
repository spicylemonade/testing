# Family Leakage Audit

- Method: `defect_charge_lattice_gas_ca`
- Frontier seed: `results/frontier/order_668_64m/seed_sequences.json`
- Winning packets: `['q[29]', 'q[53]', 'q[114]', 'q[136]', 's[29]', 's[114]']`
- Winning objective: `13/2744/480`

Mechanism statement:

The branch evaluates only exact lag-charge continuity features on the retained composite library and its precomputed two-step carrier cones. It does not introduce any family-restricted parameterization beyond the repo's shared Goethals-Seidel lift.

## Checks

- `Williamson`: `pass`. The winning state is not constrained to the symmetric / amicable packet relations characteristic of Williamson-type subfamilies, and the branch never hard-codes them.
- `Turyn`: `pass`. The branch uses only exact lag-delta transport features and never introduces supplementary-sequence identities or multiplication templates.
- `Goethals-Seidel`: `pass`. The repo-wide Goethals-Seidel lift remains the shared evaluation harness only. No branch rule restricts the search to a Goethals-Seidel family subspace.
- `cocyclic`: `pass`. No cocycle coordinates, group generators, or `D_{4t}` constraints appear in the state, candidate generation, or acceptance rule.
- `block_circulant`: `pass`. The improved state has no nontrivial period in any derived channel, so the trajectory does not collapse into a block- or quasi-circulant template.

## Empirical Symmetry Flags

- `q_palindromic`: `False`
- `s_palindromic`: `False`
- `q_prime_involution_fixed`: `False`
- `s_prime_involution_fixed`: `False`
- `q_equals_pm_s`: `False`

## Nontrivial Periods

- `s`: `[]`
- `s_prime`: `[]`
- `qs`: `[]`
- `qs_prime`: `[]`

Overall verdict: no family leakage detected.
