# gram_syndrome_decoder

Domains: quantum error correction, cellular automata, combinatorial optimization

## Topic Context
Reinterpret row-pair inner products as syndromes and borrow decoder architectures from topological quantum memories. An auxiliary CA propagates defect messages across overlapping row neighborhoods, attempting local pairing and cancellation before an exact verifier decides whether the update helped.

Mathematical focus:
Let S = {(i,j) : D_ij != 0} for D_ij = <H_i, H_j>. Build a factor graph whose variables are row bits and whose checks are pairwise orthogonality constraints. A decoder CA maintains messages m_t and selects local flips F_t = psi(m_t, D_t) so that syndrome weight ||D_t||_0 or energy sum D_ij^2 falls.

Implementation hypothesis:
Construct a sparse message graph from block interactions, adapt a local decoder rule to pass defect messages, and test whether message-guided flips outperform direct local repair.

## Closest Prior Art
- Cellular-automaton decoders for topological quantum memories (e5378f63f33009c7d64c0940c6b819057ba2e295)
- A 64-modular Hadamard matrix of order 668 (ajc_v93_p422)
- A Quantum Approximate Optimization Method For Finding Hadamard Matrices (8a06d7ef189e83b6ac474ddbcb623f02a635e286)

## Implementation Backlog
- Build the prototype scaffold under `experiments/gram_syndrome_decoder`.
- Implement the state representation implied by: Let S = {(i,j) : D_ij != 0} for D_ij = <H_i, H_j>. Build a factor graph whose variables are row bits and whose checks are pairwise orthogonality constraints. A decoder CA maintains messages m_t and selects local flips F_t = psi(m_t, D_t) so that syndrome weight ||D_t||_0 or energy sum D_ij^2 falls.
- Test the core loop from the experiment seed: Inject controlled defects into exact smaller Hadamards and measure syndrome collapse speed, then apply the same decoder to modular-seed residuals.
- Keep the novelty guardrail explicit: The target checks are dense orthogonality constraints compressed into a structured factor graph, which is a different object from the sparse stabilizer graphs used in prior decoder work.
