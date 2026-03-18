# Novelty Report

## Scope

This report evaluates the post-frontier novelty status of the active CA branch against concrete experiment IDs and named papers in `sources.bib`.

Primary experiment IDs:

- `control_n5_q0:H1_defect_syndrome_ca_64m`
- `control_n7_q0:H1_defect_syndrome_ca_64m`
- `order_668_64m:H1_defect_syndrome_ca_64m`
- `order_668_64m:greedy`
- `order_668_64m:simulated_annealing`
- `order_668_64m:stochastic_hillclimb`
- `order_668_64m:tabu`

Primary paper keys and titles:

- `eliahou2025_64mod668` :: *A 64-Modular Hadamard Matrix of Order 668*
- `tsompanas2017` :: *Cellular Automata Applications in Shortest Path Problem*
- `ghaleb2019` :: *Learning Automata-Based Solutions to the Single Elevator Problem*
- `ghaemi2022` :: *On the possibility of oscillating in the Ebola virus dynamics and investigating the effect of the lifetime of T lymphocytes*
- `leeuwen2000` :: *Engineering Societies in the Agents World*

## Findings

### 1. H1 survived as an executable branch, not as a defended frontier method

- `control_n5_q0:H1_defect_syndrome_ca_64m` and `control_n7_q0:H1_defect_syndrome_ca_64m` both reach exactness under the matched control contract, so the branch is not being retired for a trivial implementation failure.
- `order_668_64m:H1_defect_syndrome_ca_64m` does not improve the canonical seed from `eliahou2025_64mod668`. Its best objective remains support `13`, `l1 = 2880`, `max_abs = 512`, and all three restart terminals diffuse support above the seed support.

### 2. The closest real novelty pressure remains CA-as-search prior art, not the lexical false positives

- `tsompanas2017` remains the strongest method-shape warning because it is genuine CA-for-search prior art.
- After the first frontier kill test, H1 no longer supports a strong claim of being a distinct CA repair method. Without a frontier advantage, the branch collapses toward “local repair heuristic on a seeded Hadamard object” rather than “new CA repair method for Hadamard 668.”
- `ghaleb2019`, `ghaemi2022`, and `leeuwen2000` remain language-discipline or rhetorical warnings only. None threatens novelty on state representation, objective, or certification style.

### 3. The frontier anchor remains the dominant novelty constraint

- `eliahou2025_64mod668` provides the actual order-668 frontier seed and defect profile.
- The only defensible downstream claim was always narrow: seeded CA repair on top of that frontier object.
- `order_668_64m:H1_defect_syndrome_ca_64m` fails to earn even that narrow claim as an active method result because `order_668_64m:greedy` and `order_668_64m:simulated_annealing` preserve the seed support while H1 does not hold the required support-plus-magnitude advantage.

## Branch-Level Verdict

- `H1_defect_syndrome_ca_64m`
  - Status: retired as an active frontier branch after the first matched kill test.
  - Honest claim: tested seeded-CA hypothesis, not demonstrated CA repair method.
- `H2_lag_space_ca_167`
  - Status: eligible to open next because the current failure signature is consistent with locality / actuator-basis mismatch rather than missing controls.
  - Constraint: still requires the family-leakage audit already described in `results/branches/H2_gate.md`.
- `H3_spacetime_row_emission_ca`
  - Status: remains closed.
  - Reason: direct CA-construction overlap risk remains high, and H1 failure does not justify widening into H3.

## Decision

The current work remains materially different from the named papers only as a completed falsification step:

- it tested a seeded CA repair program on the recovered frontier object from `eliahou2025_64mod668`
- it benchmarked that branch against matched non-CA controls
- it showed that the current H1 branch does not justify a stronger novelty claim after the first frontier batch

Next verification action: `pivot to H2`, not `continue H1`.
