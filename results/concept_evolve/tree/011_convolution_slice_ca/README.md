# convolution_slice_ca

Domains: signal processing, additive combinatorics, cellular automata

## Topic Context
Represent the 167/80 search state as a field of local convolution contributions instead of raw support bits. Each site stores how much it over- or under-contributes to nearby cyclic shifts, and a conservative CA routes this debt around the cycle with local swaps.

Mathematical focus:
For a support x subset Z_167, define contribution tensor A_i(k) = x_i x_{i+k} and slice debts delta(k) = sum_i A_i(k) - tau_k. Maintain local liabilities ell_i(K) = sum_{k in K} w_k (A_i(k) - tau_k/167), then choose local swaps minimizing nearby ell_i while conserving |x|.

Implementation hypothesis:
Maintain incremental convolution tables so each local swap updates only a small liability neighborhood, then use either deterministic CA rules or a CA-guided beam search over liabilities.

## Closest Prior Art
- Convolution numbers: the cyclic case (af20a0b3ccef66fad2a0a1e9f11011eb99194784)
- Density classification performance and ergodicity of the Gacs-Kurdyumov-Levin cellular automaton model IV (41ce7a3f00efd1be36d2d864667ce6b159168c91)
- Quantum computing formulation of some classical Hadamard matrix searching methods and its implementation on a quantum computer (1fd50d1147b7684686e533886b44a9e92ac2e807)

## Implementation Backlog
- Build the prototype scaffold under `experiments/convolution_slice_ca`.
- Implement the state representation implied by: For a support x subset Z_167, define contribution tensor A_i(k) = x_i x_{i+k} and slice debts delta(k) = sum_i A_i(k) - tau_k. Maintain local liabilities ell_i(K) = sum_{k in K} w_k (A_i(k) - tau_k/167), then choose local swaps minimizing nearby ell_i while conserving |x|.
- Test the core loop from the experiment seed: Compare liability-driven swaps, plain random local moves, and direct recomputation on smaller cyclic test cases and then on the exact 167/80 target.
- Keep the novelty guardrail explicit: The cyclic reduction in prior work is global. This concept localizes that obstruction into per-site liabilities suitable for conservative CA dynamics.
