# Novelty Collapse Audit

Prepared for rubric `item_014`.

## Narrow claim that survives

The only claim that survives review is narrow and negative:

- this repo implemented Hadamard-specific CA search branches tied to the exact `167/80` cyclic obstruction and the published `64`-modular order-`668` seed;
- those branches were evaluated against matched same-representation non-CA baselines;
- the implemented CA rules did not outperform those baselines.

Anything broader collapses into existing prior art or into unsupported optimism.

## Named watchlist audit

### Cellular Automata Applications in Shortest Path Problem (2017)

- Pass on differentiation.
- The current work is not a generic shortest-path or routing application.
- Constraint on wording: do not claim novelty for `CA optimization` in the abstract.

### Learning Automata-Based Solutions to the Single Elevator Problem (2019)

- Pass on differentiation.
- Overlap is lexical only.
- Constraint on wording: do not describe the method as a generic optimization controller.

### On the possibility of oscillating in the Ebola virus dynamics... (2022)

- Pass on differentiation.
- The paper is a lexical false positive caused by the initial seed query.
- Constraint on wording: keep biomedical CA simulation completely out of the methodological frame.

### Engineering Societies in the Agents World (2000)

- Pass on differentiation.
- It is not substantive prior art for this branch.
- Constraint on wording: avoid drifting into agent-society or generic multi-agent novelty language.

## Exact Hadamard and structured-search anchors

### Constantine and Constantine (2025)

- Pass on differentiation in scope, fail as a positive-contribution claim.
- The repo did not restate the cyclic reduction, but it also did not produce a better solver for the exact obstruction than matched direct search.

### Eliahou (2025)

- Pass on differentiation in scope, fail as a positive-contribution claim.
- The repo did not claim a new modular construction, but the CA repair layer failed to improve the published seed beyond the matched non-CA baseline.

### Bright, Kotsireas, and Ganesh (2018)

- Guardrail only.
- The reserve symbolic branches risk collapsing into SAT+CAS-style exact filtering unless they prove a distinct proposal mechanism before clause-level pruning.

### Williamson / Goethals-Seidel family literature

- Guardrail only.
- Any branch that exposes family parameters instead of local support- or defect-space dynamics should be retired as a reformulation, not promoted as a new method.

## CA-side anchors

### CA design and bent-function literature

- Pass on narrow differentiation, fail on any broad novelty claim.
- CA has already been used for combinatorial-design and cryptographic search objects adjacent to Hadamard structure.
- The repo can only claim novelty at the level of the specific order-`668` obstruction or seed, not at the level of `CA meets Hadamard-like objects`.

### CA controllability and decoder literature

- Guardrail only.
- These sources justify reachability and local-repair concerns, but they do not license a success claim for Hadamard search.

## Branch-by-branch collapse call

- `H1`: novel enough to test, not novel enough to keep once it loses to matched direct search.
- `H2`: collapses into a local-search wrapper because it ties the matched baseline on the decisive `668` attempt.
- Literal `cellar` / pushdown branch: materially different from `H1/H2`, but still vulnerable to collapse into ordinary prefix pruning unless it proves stateful deferred-debt behavior that static exact encodings do not already provide.

## Final wording constraints

- Do say:
  - `we tested a CA-style search program on the exact 167/80 obstruction and the published mod-64 seed`;
  - `the matched baselines beat or tied the CA rules`;
  - `any next attempt requires a materially different representation`.
- Do not say:
  - `cellular automata for Hadamard search is untried`;
  - `the repo discovered a promising CA route to order 668`;
  - `the literal cellar reading is already a validated new method`.
