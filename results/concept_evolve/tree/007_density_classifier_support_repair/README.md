# density_classifier_support_repair

Domains: cellular automata, statistical mechanics, additive combinatorics

## Topic Context
Adapt Gacs-Kurdyumov-Levin style density classification to the weight-80 support vector underlying the 167/80 obstruction. A conservative CA moves occupied sites along the cycle based on neighborhood-majority and convolution-debt signals, maintaining total weight while smoothing harmful local patterns.

Mathematical focus:
Let x_t in {0,1}^{167} with sum_i x_i = 80. For each site i compute local density rho_i and debt gradients g_i(k) = c_{x_t}(k) - tau_k over nearby shifts. Update with a particle-conserving rule x_{t+1} = F(x_t, rho, g) that swaps 10/01 pairs instead of flipping occupancy.

Implementation hypothesis:
Implement conservative GKL-like swaps with optional multi-radius debt sensors and compare them against plain hill-climbing on the same weight-preserving neighborhood.

## Closest Prior Art
- Density classification performance and ergodicity of the Gacs-Kurdyumov-Levin cellular automaton model IV (41ce7a3f00efd1be36d2d864667ce6b159168c91)
- Convolution numbers: the cyclic case (af20a0b3ccef66fad2a0a1e9f11011eb99194784)
- Regional controllability of cellular automata as a SAT problem (d622c453cb5aa83cdcdd35eb077178d61c7bfcaf)

## Implementation Backlog
- Build the prototype scaffold under `experiments/density_classifier_support_repair`.
- Implement the state representation implied by: Let x_t in {0,1}^{167} with sum_i x_i = 80. For each site i compute local density rho_i and debt gradients g_i(k) = c_{x_t}(k) - tau_k over nearby shifts. Update with a particle-conserving rule x_{t+1} = F(x_t, rho, g) that swaps 10/01 pairs instead of flipping occupancy.
- Test the core loop from the experiment seed: Start from random weight-80 supports, transduced design seeds, and projections of modular blocks; track exact target distance and distinct orbit coverage.
- Keep the novelty guardrail explicit: Standard density-classification CA solve a one-bit aggregate task. This version is constrained by a full convolution signature and an exact weight budget.
