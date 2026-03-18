# mols_to_sds_transducer

Domains: combinatorial design, cellular automata, incidence geometry

## Topic Context
Treat CA-generated orthogonal Latin squares and orthogonal arrays as high-regularity incidence patterns, then transduce them into candidate supplementary difference-set style block supports. The claim is not that Latin squares solve 668 directly, but that their incidence regularity might seed nontrivial candidate families outside obvious circulant traps.

Mathematical focus:
Given CA-generated Latin squares L1, L2, build incidence tensors T_{a,b}(i,j) = 1[(L1(i,j), L2(i,j)) = (a,b)]. Search transductions Phi(T) -> (S1,S2,S3,S4) subset Z_167 such that sum_t 1_{S_t} * 1_{-S_t} approximates target SDS counts or modular Golay filters.

Implementation hypothesis:
Generate small OLS or OA objects from linear CA, learn symbolic projections into subset tuples, and test whether those tuples land closer to known Hadamard filters than random subsets do.

## Closest Prior Art
- Constructing Orthogonal Latin Squares from Linear Cellular Automata (1abe43406189b39ff3064f2882467c2ae2a549c8)
- Combinatorial Designs and Cellular Automata: A Survey (44871e8b22b10f05e8ff1eaec72e3fe125c83c50)
- Convolution numbers: the cyclic case (af20a0b3ccef66fad2a0a1e9f11011eb99194784)

## Implementation Backlog
- Build the prototype scaffold under `experiments/mols_to_sds_transducer`.
- Implement the state representation implied by: Given CA-generated Latin squares L1, L2, build incidence tensors T_{a,b}(i,j) = 1[(L1(i,j), L2(i,j)) = (a,b)]. Search transductions Phi(T) -> (S1,S2,S3,S4) subset Z_167 such that sum_t 1_{S_t} * 1_{-S_t} approximates target SDS counts or modular Golay filters.
- Test the core loop from the experiment seed: Use small primes with known Goethals-Seidel or SDS witnesses as positive controls, then inspect whether the transducer still produces enriched seeds at p = 167.
- Keep the novelty guardrail explicit: Prior design papers stop inside OLS or OA families. This concept only counts as success if the incidence structure translates into better 167-length witness candidates.
