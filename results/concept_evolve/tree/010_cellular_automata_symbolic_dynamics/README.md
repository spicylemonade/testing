# Cellular Automata and Symbolic Dynamics

## Topic Context

Tiskin (2023) provided a new perspective on the Chvátal-Sankoff problem by reformulating it in the language of symbolic dynamics and cellular automata (CA). The key ideas:

1. **LCS as a CA**: The dynamic programming computation of LCS can be viewed as a deterministic CA evolving on a 1D lattice. Each cell stores incremental score information. The CA rule is local and deterministic, but the initial condition (the input strings) is random.

2. **Height function**: The LCS length corresponds to the "height" of the CA spacetime diagram. The constant γ₂ is the asymptotic slope of this height function.

3. **Symbolic dynamics**: The set of valid CA configurations forms a subshift, whose topological entropy relates to γ₂.

4. **Transfer matrix**: For finite-width strips, the CA dynamics can be captured by a transfer matrix whose dominant eigenvalue gives exact γ₂ for that width.

## Key Insight from Tiskin (2023)
Tiskin noted an error in his 2022 paper that invalidated some claims about properties of γ₂. The corrected analysis still establishes the CA/particle process framework but the numerical estimates may need revision.

## Implementation Backlog

1. **Implement LCS cellular automaton** (Priority: HIGH)
   - Code the CA rule from Tiskin's description
   - Validate on known LCS examples
   - Visualize spacetime diagrams

2. **Transfer matrix computation** (Priority: HIGH)
   - Derive transfer matrix T_w for width w
   - Compute dominant eigenvalue for w = 1,...,15
   - Extract γ₂(w) sequence

3. **Width extrapolation** (Priority: HIGH)
   - Fit γ₂(w) → γ₂ using scaling ansatz
   - Determine convergence rate (geometric vs algebraic)
   - Compare with Monte Carlo estimates

4. **Topological entropy analysis** (Priority: MEDIUM)
   - Compute topological entropy of the subshift for small widths
   - Relate to γ₂ via Tiskin's formula
   - Check if entropy provides additional constraints
