# regional_controllability_seeded_ca

Domains: cellular automata, SAT, control theory

## Topic Context
Use CA controllability results as a pre-screen for any rule family before expensive 668 search. Only rule templates with SAT-certified ability to steer seeds toward low-defect regions survive into the actual search loop.

Mathematical focus:
For a CA rule family f_r and target region R_eps = {s : score(s) <= eps}, solve Reach_r(T, S0, R_eps) via SAT. Choose rules r maximizing a lower bound on reachability to exact or modularly admissible regions while preserving required invariants I(s).

Implementation hypothesis:
Encode bounded-time controllability for small support or defect fields, learn which rule motifs remain controllable under the desired invariants, and restrict later search to those rule families.

## Closest Prior Art
- Regional controllability of cellular automata as a SAT problem (d622c453cb5aa83cdcdd35eb077178d61c7bfcaf)
- A 64-modular Hadamard matrix of order 668 (ajc_v93_p422)
- Applying Computer Algebra Systems with SAT Solvers to the Williamson Conjecture (ac46aa30dbbe83df90f792216d8f31a278170267)

## Implementation Backlog
- Build the prototype scaffold under `experiments/regional_controllability_seeded_ca`.
- Implement the state representation implied by: For a CA rule family f_r and target region R_eps = {s : score(s) <= eps}, solve Reach_r(T, S0, R_eps) via SAT. Choose rules r maximizing a lower bound on reachability to exact or modularly admissible regions while preserving required invariants I(s).
- Test the core loop from the experiment seed: Run reachability certification on smaller solved orders and on slices of the modular 668 seed; correlate reachability scores with downstream search success.
- Keep the novelty guardrail explicit: Prior controllability work is generic CA theory, while this concept uses it as a Hadamard-specific falsification gate tied to exact search regions and concrete seed states.
