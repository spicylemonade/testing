# defect_transport_mod64_lift

Domains: combinatorial design, cellular automata, statistical physics

## Topic Context
Start from Eliahou's 64-modular order-668 matrix rather than from random +/-1 matrices. Encode each nonzero off-diagonal Gram entry as a defect particle on a row-pair graph and let a cellular automaton move, merge, and annihilate defects while an exact verifier stays outside the CA loop.

Mathematical focus:
Given H in {+1,-1}^{668 x 668}, define D_ij = <H_i, H_j> for i != j. Initialize from a sparse-defect seed H^(0) and apply local balanced flips U_f so that H^(t+1) = U_f(H^(t)) while E(H) = sum_{i<j} |D_ij| or sum_{i<j} D_ij^2 decreases and block invariants are preserved.

Implementation hypothesis:
Reconstruct the published 64-modular seed, build a defect graph over row pairs, and implement local row-block sign swaps that preserve balance. Use CA rules to route defect mass toward cancellation and compare against greedy and annealed updates on the same neighborhood.

## Closest Prior Art
- A 64-modular Hadamard matrix of order 668 (ajc_v93_p422)
- Finding a Hadamard Matrix by Simulated Annealing of Spin-Vectors (b01723f49ef6134f64d4675cc9a0d747eb29350b)
- Cellular-automaton decoders for topological quantum memories (e5378f63f33009c7d64c0940c6b819057ba2e295)

## Implementation Backlog
- Build the prototype scaffold under `experiments/defect_transport_mod64_lift`.
- Implement the state representation implied by: Given H in {+1,-1}^{668 x 668}, define D_ij = <H_i, H_j> for i != j. Initialize from a sparse-defect seed H^(0) and apply local balanced flips U_f so that H^(t+1) = U_f(H^(t)) while E(H) = sum_{i<j} |D_ij| or sum_{i<j} D_ij^2 decreases and block invariants are preserved.
- Test the core loop from the experiment seed: Validate on smaller exact Hadamards with injected defects, then start from the 668 modular seed and measure defect count, defect energy, and exact-certificate frequency after fixed update budgets.
- Keep the novelty guardrail explicit: Prior Hadamard heuristics optimize directly in matrix or sequence coordinates, while prior CA decoders repair stabilizer syndromes. This concept combines the two only at the sparse residual-defect stage exposed by the best current 668 construction.
