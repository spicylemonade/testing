# autocorrelation_debt_pushdown

Domains: formal languages, additive combinatorics, Hadamard search

## Topic Context
Treat 'cellar automata' literally as a stack-like automaton over run-length or convolution tokens for the length-167 obstruction. The automaton stores unresolved autocorrelation debt and only expands prefixes that still admit completion under global weight, parity, and symmetry constraints.

Mathematical focus:
Let x in {0,1}^{167} with sum_i x_i = 80 and target cyclic convolution c_x(k) = sum_i x_i x_{i+k} = tau_k. Parse x as a token word w; a visibly pushdown automaton state tracks (position, weight, local debt) and a stack of deferred multiscale deficits Delta_I(k). Accept exactly those prefixes that remain extendable to c_x = tau.

Implementation hypothesis:
Tokenize candidate supports or 4-block prefixes, hand-design or learn stack transitions from solved smaller orders, and use the automaton as a prefix filter before any exact SAT or CAS step.

## Closest Prior Art
- Convolution numbers: the cyclic case (af20a0b3ccef66fad2a0a1e9f11011eb99194784)
- Applying Computer Algebra Systems with SAT Solvers to the Williamson Conjecture (ac46aa30dbbe83df90f792216d8f31a278170267)
- Williamson type Hadamard matrices with circulant components (e517b186e1edfb3a865cb4eabbdd4e0f8570d2a3)

## Implementation Backlog
- Build the prototype scaffold under `experiments/autocorrelation_debt_pushdown`.
- Implement the state representation implied by: Let x in {0,1}^{167} with sum_i x_i = 80 and target cyclic convolution c_x(k) = sum_i x_i x_{i+k} = tau_k. Parse x as a token word w; a visibly pushdown automaton state tracks (position, weight, local debt) and a stack of deferred multiscale deficits Delta_I(k). Accept exactly those prefixes that remain extendable to c_x = tau.
- Test the core loop from the experiment seed: Benchmark rejection rate on random prefixes versus retention of known valid smaller witnesses, then use the accepted frontier as input to a focused search on the 167/80 target.
- Keep the novelty guardrail explicit: The contribution is not a rewrapped SAT solver: the pushdown model operates before clause expansion and uses explicit deferred debt, which classical exact encodings usually do not expose as a stateful search object.
