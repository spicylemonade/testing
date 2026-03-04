# Optimal Transport Formulation for LCS Bounds

## Topic Context

Optimal transport (OT) provides a natural framework for sequence alignment problems. The LCS alignment between strings a and b can be viewed as an optimal partial coupling between the character positions, subject to a monotonicity constraint. This perspective connects LCS to the rich OT theory including Kantorovich duality, Sinkhorn algorithms, and Gromov-Wasserstein distances.

The key advantage: OT relaxations provide systematic upper bounds on the LCS (and thus γ₂). The Kantorovich dual gives a certificate-based bound that can be optimized over dual variables.

## Formulation

Given random binary strings a, b of length n:
- **Primal**: LCS = max {|π| : π is a monotone partial matching between positions}
- **OT relaxation**: Drop monotonicity → max partial matching = min(#{0s in a} + #{0s in b}, #{1s in a} + #{1s in b}) ≈ n/2 (too loose)
- **Structured OT**: Add partial monotonicity constraints (e.g., no crossing within windows of size w) for a hierarchy of bounds

## Implementation Backlog

1. **LP formulation of LCS** (Priority: HIGH)
   - Write LCS as integer LP with monotonicity constraints
   - Solve LP relaxation for small n
   - Evaluate tightness of relaxation gap

2. **Sinkhorn with monotonicity** (Priority: MEDIUM)
   - Add entropic regularization to the OT formulation
   - Impose monotonicity via Lagrangian penalties
   - Solve iteratively for moderate n

3. **Gromov-Wasserstein approach** (Priority: MEDIUM)
   - Model order preservation as internal structure
   - Use Fused GW distance to capture both character matching and positional structure

4. **Hierarchy of relaxations** (Priority: LOW)
   - Define window-w monotonicity constraints
   - Solve for w = 1, 2, 5, 10, n
   - Track bound tightening as w increases
