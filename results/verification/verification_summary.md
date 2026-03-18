# Verification Summary

## Decision

Next action: `pivot to H2`.

## Basis

- Control validity:
  - `control_n5_q0:H1_defect_syndrome_ca_64m`
  - `control_n7_q0:H1_defect_syndrome_ca_64m`
  - These runs show H1 is executable under the shared harness and is not being retired for a trivial coding failure.
- Frontier kill test:
  - `order_668_64m:H1_defect_syndrome_ca_64m`
  - `order_668_64m:greedy`
  - `order_668_64m:simulated_annealing`
  - `order_668_64m:tabu`
  - `order_668_64m:stochastic_hillclimb`
  - No method reaches exactness, H1 never beats the seed objective from `eliahou2025_64mod668`, and H1 fails the support-plus-magnitude continuation gate.
- Novelty and citation discipline:
  - `tsompanas2017` keeps the CA claim narrow.
  - `ghaleb2019`, `ghaemi2022`, and `leeuwen2000` remain watchlist comparators only.
  - The current H1 result does not justify calling the branch a new CA repair method for order `668`.

## What This Means

- `continue H1`: rejected for the current single-packet q/s branch.
- `pivot to H2`: accepted, because the failure signature is consistent with a locality / actuator-basis mismatch already flagged in `results/concept_evolve/probe_result.json` and summarized in the verification pack.
- `stop H3`: remains in force; H3 stays closed while H2 is the next gated branch.

## Exactness Status

- Exact order-668 Hadamard matrix found in this run: `no`
- Exact frontier improvement over the published seed from `eliahou2025_64mod668`: `no`

## Required Guardrail

Opening H2 does not mean broad expansion. The next pass should first satisfy the H2 family-leakage audit against known structured families before spending frontier budget.
