# sat_user_propagator_ca

Domains: SAT/SMT, computer algebra, cellular automata

## Topic Context
Couple a CA proposal engine with SAT+CAS user propagators that learn forbidden local motifs. Unsat cores from the exact layer are translated back into penalties on CA neighborhoods, closing the loop between symbolic proof and local dynamics.

Mathematical focus:
Let z_t be compressed block tokens and z_{t+1} = f(z_t) be a CA update. An exact verifier V(z) returns extendable or a conflict core C; learn local penalties lambda_C so later updates minimize E_local(z) + sum_C lambda_C * 1[C subset z].

Implementation hypothesis:
Build a compressed tokenization of block states, integrate a user-propagator SAT solver, and feed extracted unsat motifs back into CA rule weights or rejection masks.

## Closest Prior Art
- Applying Computer Algebra Systems with SAT Solvers to the Williamson Conjecture (ac46aa30dbbe83df90f792216d8f31a278170267)
- Enumeration of Complex Golay Pairs via Programmatic SAT (909616c0a3c4d05d30f4090785f4d87d6248109b)
- A SAT+CAS Approach to Finding Good Matrices: New Examples and Counterexamples (f0da7cd59959010936975efce768a87cfa190c00)

## Implementation Backlog
- Build the prototype scaffold under `experiments/sat_user_propagator_ca`.
- Implement the state representation implied by: Let z_t be compressed block tokens and z_{t+1} = f(z_t) be a CA update. An exact verifier V(z) returns extendable or a conflict core C; learn local penalties lambda_C so later updates minimize E_local(z) + sum_C lambda_C * 1[C subset z].
- Test the core loop from the experiment seed: Recover known Williamson or good-matrix instances, then measure whether learned motifs improve throughput on the 167-length obstruction or on modular-seed refinement.
- Keep the novelty guardrail explicit: Standard SAT+CAS work uses fixed encodings and static pruning. This concept turns exact conflicts into online updates of a local proposal process.
