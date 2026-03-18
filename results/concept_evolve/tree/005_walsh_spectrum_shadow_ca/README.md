# walsh_spectrum_shadow_ca

Domains: cryptography, spectral combinatorics, cellular automata

## Topic Context
Use CA-generated bent or semi-bent Boolean functions as spectral templates for length-167 block candidates. The CA does not try to output an order-668 Hadamard directly; it supplies Walsh-flat shadows that are decoded into candidates likely to survive modular or exact filters.

Mathematical focus:
For a CA rule r and seed s, derive a Boolean function f_{r,s}. Compute Walsh profile W_f(omega) = sum_x (-1)^(f(x) + omega.x). Project spectrally flat signatures through a map Pi into candidate block tuples (a,b,c,d) and score them by autocorrelation debt J(Pi(f)).

Implementation hypothesis:
Search over CA rules already known to yield bent-like functions, define one or more projection maps into 167-length binary blocks, and keep only shadows enriched for modular admissibility.

## Closest Prior Art
- Bent Functions from Cellular Automata (iacr:2020/1272)
- Heuristic Search of (Semi-)Bent Functions based on Cellular Automata (d0ef2d96e201af37ae7bf3535d21a4ac29c6f6b3)
- Convolution numbers: the cyclic case (af20a0b3ccef66fad2a0a1e9f11011eb99194784)

## Implementation Backlog
- Build the prototype scaffold under `experiments/walsh_spectrum_shadow_ca`.
- Implement the state representation implied by: For a CA rule r and seed s, derive a Boolean function f_{r,s}. Compute Walsh profile W_f(omega) = sum_x (-1)^(f(x) + omega.x). Project spectrally flat signatures through a map Pi into candidate block tuples (a,b,c,d) and score them by autocorrelation debt J(Pi(f)).
- Test the core loop from the experiment seed: Measure enrichment against random supports and direct local search on smaller targets before applying the same decoder to 167-length blocks.
- Keep the novelty guardrail explicit: Prior CA-bent papers optimize cryptographic quality in their own right. Here spectral flatness is only a proposal prior and success is judged by Hadamard-specific filters.
