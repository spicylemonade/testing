# LP Relaxation and Dual Bounds for γ₂

## Topic Context

The most successful computational approach to lower-bounding γ₂ is the "feasible triplet" method, developed across several papers and most recently pushed to new records by Heineman et al. (2024). The method is fundamentally an LP dual approach: it constructs explicit dual-feasible solutions that certify lower bounds.

### Current State of the Art
- **Lower bound**: 0.792666 (Heineman et al. 2024, ℓ = 14)
- **Previous lower bound**: 0.788071 (Lueker 2009, ℓ = 12)
- The bound improves roughly 0.001-0.003 per unit increase in ℓ
- Computational cost grows exponentially in ℓ (state space is 4^ℓ)

### Key Innovation in Heineman et al.
- Parallelization across cores
- "Binary feasible triplet" method reducing state space
- Recursive memory reading/writing scheme avoiding RAM bottleneck
- Improved almost all bounds for σ > 2 and d > 2

## Implementation Backlog

1. **Reproduce baseline results** (Priority: HIGH)
   - Implement feasible triplet method for ℓ = 1,...,14
   - Verify published bounds
   - Profile computational bottlenecks

2. **GPU acceleration** (Priority: HIGH)
   - Port inner loop to CUDA
   - State space enumeration on GPU
   - Target ℓ = 15, 16

3. **ML-guided search** (Priority: MEDIUM)
   - Train classifier to predict "promising" triplets
   - Reduce search space by pruning unlikely candidates
   - Potentially reach ℓ = 18-20

4. **SDP hierarchy for upper bounds** (Priority: MEDIUM)
   - Formulate the dual LP as a moment problem
   - Apply Lasserre/SOS hierarchy for upper bounds
   - Compare with Lueker's Markov chain upper bound

5. **Convergence rate analysis** (Priority: HIGH)
   - Fit bound(ℓ) = γ₂ - c/ℓ^α
   - Extrapolate to ℓ → ∞
   - Compare with known γ₂ estimates
