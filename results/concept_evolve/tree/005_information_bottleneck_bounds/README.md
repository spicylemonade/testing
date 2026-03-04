# Information-Theoretic Bounds on γ₂

## Topic Context

Information theory provides several angles of attack on the Chvátal-Sankoff constant:

1. **Kolmogorov complexity upper bounds**: The LCS between strings a and b bounds the conditional complexity K(a|b). For random strings, this yields γ₂ ≤ 1 - H_min/n where H_min is related to the minimum description length gap.

2. **Markov chain upper bounds** (Lueker 2003): Model the LCS computation as a Markov chain on a state space encoding partial alignment information. The stationary distribution of an order-k Markov chain gives an upper bound that tightens with k.

3. **Concentration via entropy method**: The Efron-Stein inequality and logarithmic Sobolev inequalities give exponential concentration of LCS around its mean, with Var[LCS] = O(n).

4. **Deletion channel capacity**: γ₂ is related to the capacity of the binary deletion channel, providing a coding-theoretic interpretation.

## Current Best Bounds
- Upper: 0.826280 (Lueker 2003, Markov chain method)
- Lower: 0.792666 (Heineman et al. 2024, feasible triplet method)

## Implementation Backlog

1. **Reproduce Lueker upper bound** (Priority: HIGH)
   - Implement order-k Markov chain analysis
   - Verify 0.826280 for the reported k value
   - Extend to higher k if computationally feasible

2. **Information bottleneck formulation** (Priority: MEDIUM)
   - Formulate γ₂ as mutual information optimization
   - Implement Blahut-Arimoto for numerical solution
   - Compare with direct Markov chain bounds

3. **Deletion channel connection** (Priority: MEDIUM)
   - Map known deletion channel capacity bounds to γ₂ constraints
   - Check if recent capacity results improve γ₂ bounds
   - Explore polarization-based approaches

4. **Improved concentration bounds** (Priority: LOW)
   - Apply modified logarithmic Sobolev inequality
   - Bound Var[LCS] more tightly than O(n)
   - Use for improved confidence intervals in Monte Carlo estimation
