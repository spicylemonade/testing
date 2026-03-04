# Interval Arithmetic Certification

## Topic Context

Validated numerics (interval arithmetic, computer-assisted proofs) have been used to settle several longstanding mathematical problems: Hales' proof of the Kepler conjecture, Tucker's proof of the Lorenz attractor, and various results in PDE theory.

For the Bloch constant, Rettinger (2008) studied the computability of B from the perspective of computable analysis. The key question is: can we use interval arithmetic to convert numerical bounds on B_u into rigorous proofs?

## Certification Strategy

1. **Represent** the candidate extremal function f with interval Taylor coefficients
2. **Verify univalence**: compute interval enclosure of Grunsky matrix norm; if ||G||_op ≤ 1 rigorously, f is univalent
3. **Verify covering**: compute interval enclosure of f on |z|=1; verify winding number around w for |w|=R
4. **Certify**: if both pass, then B_u ≥ R is a machine-checkable theorem

## Implementation Backlog

1. **[P0]** Set up interval arithmetic framework (Julia/MATLAB)
2. **[P0]** Implement interval Grunsky matrix computation
3. **[P1]** Implement interval winding number computation
4. **[P1]** Test on known examples (Koebe function)
5. **[P2]** Apply to Skinner's candidate for R = 0.5709
6. **[P3]** Combine with SDP (concept 004) for systematic certified bounds
