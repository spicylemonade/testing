# ConceptEvolve Delta Tracking

## Commands Executed

| Phase | Command | Topic/Seed | Output |
|-------|---------|------------|--------|
| Phase 1 | `evolve` | "Tightening bounds on γ₂ for binary alphabet via computational optimization, stochastic particle processes, and information-theoretic methods" | 12 concepts, 17 edges, 5 bridge chains, 5 steering directions |
| Phase 3 | `probe` | Same topic | 5 new steering directions (RSOS calibration, DFA roughness exponent, bit-parallel certificate evaluator, Bhattacharjee-Seno data collapse, population dynamics) |
| Phase 4 | `reframe` | Phase 3 failure analysis: "no approach improved on SOTA bounds" | 11 reframings generated |

## Concept Cards Implemented

### Card #009: finite_size_scaling_extrapolation
- **Implementation hypothesis:** "Use Richardson extrapolation on eigenvalue sequences to accelerate convergence"
- **Result:** Implemented in `results/novel/particle_process.py` and `results/novel/scaled_upper_bound.py`
- **Outcome:** KPZ 3-parameter fit gives γ₂ ≈ 0.8132 ± 0.0002 (successful estimation, not a rigorous bound). Richardson extrapolation on strip eigenvalues failed due to absorbing state (all γ_s = 1.0).
- **Delta:** Concept partially validated — finite-size scaling works for MC estimates but strip eigenvalue sequence is trivial.

### Card #008: lp_relaxation_dual_bounds  
- **Implementation hypothesis:** "Extend the feasible triplet method with machine-learning-guided selection of promising triplets"
- **Result:** Implemented in `results/novel/neural_certificate.py`
- **Outcome:** Failed. Gradient optimization on simplified buffer model never achieved certificate feasibility. The ML-guided approach requires the full Lueker state space (4^h) to produce valid bounds.
- **Delta:** Concept invalidated for simplified state spaces. Remains viable if applied to the full DFA state space with more sophisticated optimization (e.g., population dynamics, as suggested by Phase 3 probe).

## Steering Directions Acted On

### Phase 1 Steering
1. **GPU multi-spin MC + KPZ scaling** → Implemented (CPU, not GPU). C-accelerated MC with KPZ extrapolation. **Result:** γ₂ ≈ 0.813.
2. **Frog dynamics extension** → Implemented. Searched periods 2-7, best word "100110" with γ ≈ 0.800. **Result:** Valid lower bound but weaker than SOTA.
3. **OT relaxation hierarchy** → Not implemented (deprioritized after Phase 3 failures showed simpler approaches already struggling).

### Phase 3 Probe Steering
4. **Bit-parallel certificate evaluator** → Partially implemented in `lcs_fast.c` (bit-parallel LCS function). Not applied to certificate search.
5. **Population dynamics for certificate search** → Not implemented (would require full Lueker state space).

## Gap Analysis

| Metric | Start of Research | End of Research | Delta |
|--------|-------------------|-----------------|-------|
| Best rigorous lower bound | 0.792665992 (H2024) | 0.792665992 | +0.000 |
| Best rigorous upper bound | 0.826280 (L2009) | 0.826280 | +0.000 |
| Gap width | 0.033614 | 0.033614 | 0.000 |
| Best non-rigorous estimate | 0.8119 (B2001) | 0.8132 ± 0.0002 | +0.001 |
| Concepts explored | 0 | 12 | +12 |
| Missing links identified | 0 | 5 | +5 |
