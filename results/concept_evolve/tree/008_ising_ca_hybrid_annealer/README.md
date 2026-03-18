# ising_ca_hybrid_annealer

Domains: statistical physics, quantum optimization, cellular automata

## Topic Context
Keep the proven Hadamard energy functions from SA, SQA, and QAOA literature, but replace uninformed proposal moves with CA-generated balanced neighborhoods. The CA becomes a structured move generator inside a global energy search instead of pretending to be a full solver by itself.

Mathematical focus:
Use E(H) = sum_{i<j} <H_i,H_j>^2 or a structured block analogue E(z). Let q_f(z'|z) be a proposal kernel induced by a local CA rule f over neighborhoods N(i); keep the same acceptance scheme as Metropolis, SQA, or QAOA-style mixers while q_f preserves balance and symmetry.

Implementation hypothesis:
Implement a shared energy and verifier, then compare random proposals versus CA proposals under identical SA, SQA-style, and QAOA-inspired acceptance logic.

## Closest Prior Art
- Finding a Hadamard Matrix by Simulated Annealing of Spin-Vectors (b01723f49ef6134f64d4675cc9a0d747eb29350b)
- Finding a Hadamard Matrix by Simulated Quantum Annealing (d98246df005a52ff9a5e99b6c5f548c1def1ba12)
- A Quantum Approximate Optimization Method For Finding Hadamard Matrices (8a06d7ef189e83b6ac474ddbcb623f02a635e286)

## Implementation Backlog
- Build the prototype scaffold under `experiments/ising_ca_hybrid_annealer`.
- Implement the state representation implied by: Use E(H) = sum_{i<j} <H_i,H_j>^2 or a structured block analogue E(z). Let q_f(z'|z) be a proposal kernel induced by a local CA rule f over neighborhoods N(i); keep the same acceptance scheme as Metropolis, SQA, or QAOA-style mixers while q_f preserves balance and symmetry.
- Test the core loop from the experiment seed: Use solved smaller orders first, then modular-seed lift tasks and 167-slice tasks to measure acceptance efficiency and eventual certificate rate.
- Keep the novelty guardrail explicit: Prior annealing and QAOA papers change the optimizer. This concept asks whether CA proposals improve the same objective under matched acceptance dynamics.
