# Code Watchlist

## Immediate Relevance

- `curtisbright/mathcheck2`
  - Role: exact combinatorial search / SAT+CAS verifier.
  - Why it matters: closest reusable reference for certificate-rich structured-family search, especially when later novelty checks ask whether the CA branch has collapsed into an optimizer over a known family.
  - Why not clone first: it is a comparison target, not the current implementation substrate.
- `sagemath/sage`
  - Role: construction database and validation toolkit.
  - Why it matters: useful for checking smaller solved Hadamard orders and cross-validating known constructions before running custom controls.
  - Why not clone first: very large dependency surface; use as a reference/database, not as the first experiment harness.

## CA / NCA Reference Implementations

- `PWhiddy/Growing-Neural-Cellular-Automata-Pytorch`
  - Role: practical differentiable NCA baseline code.
  - Why it matters: useful if the branch later expands from hand-designed CA rules into learned local repair dynamics.
  - Current decision: watch only. H1 remains a hand-coded compressed defect CA for now.
- `shyamsn97/controllable-ncas`
  - Role: goal-guided NCA implementation.
  - Why it matters: strongest off-the-shelf code reference for learned control over self-organizing CA states.
  - Current decision: watch only. It is relevant to a learned follow-up, not to the first seeded kill test.

## State-Of-The-Art Approach Notes

- The highest-value new paper artifact is not a repo but the 2025 frontier paper itself, because it exposes the exact compact seed description: `q : (83, 2, 81, 1)` and the compact run-length encoding for `s`.
- The strongest non-CA exact-search comparators remain SAT+CAS / Williamson-family work rather than generic GitHub heuristics.
- The strongest non-CA heuristic comparators located so far are the Hadamard-specific annealing and QAOA papers, not public production repositories.
- For the current branch, external code is supporting evidence rather than the implementation target. The first implementation should stay small, reproducible, and native to this repo.
