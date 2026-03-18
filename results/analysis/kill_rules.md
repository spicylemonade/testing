# Registered Gates

Prepared for rubric `item_009`.

## H1 gates

- Promotion status: active.
- Success metrics:
  - exact-hit rate on `control_4x79`,
  - closest-target distance on `target_167_weight_80`,
  - unique-orbit coverage,
  - wall-clock cost.
- Kill rules:
  - kill `H1` if `direct_greedy` matches or beats `parallel_gain_ca` on the exact same 167/80 support space under the same step budget,
  - kill `H1` if the CA cannot recover the solved 79-control from perturbed solution seeds at a rate that justifies further budget,
  - kill `H1` if its observed advantage reduces to representation leakage rather than reachability.

## H2 gates

- Promotion status: dormant until `H1` fails.
- Success metrics:
  - exact repair on the structured `n=9` lift ladder,
  - reached two-adic modulus on the 668 seed attempt,
  - defect count,
  - max defect magnitude.
- Kill rules:
  - kill `H2` if it cannot solve the structured `n=9` lift ladder under the same neighborhood and budget as `direct_greedy`,
  - kill `H2` if it cannot restore or improve the published 668 seed beyond the matched non-CA baseline,
  - kill `H2` if the active update rule relies on a different variable family than the baseline on the 668 seed.

## H3 gates

- Promotion status: reserve only.
- Success metrics:
  - none until explicitly promoted by a later memo.
- Kill rules:
  - kill `H3` immediately if a compressed-state branch does not beat the same-representation non-CA comparator,
  - kill `H3` if it collapses into a SAT+CAS or branch-and-bound presentation with no new reachability result,
  - do not promote `H3` before `H1` and `H2` are both closed.
