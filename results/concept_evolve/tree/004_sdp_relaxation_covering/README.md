# SDP Relaxation for Covering Radius

## Topic Context

Semidefinite programming (SDP) has revolutionized several areas of mathematics and theoretical physics by providing systematic, convergent hierarchies of bounds. The conformal bootstrap in physics uses similar ideas to bound operator dimensions in conformal field theories.

The Grunsky inequalities provide a necessary and sufficient condition for univalence that can be expressed as a linear matrix inequality (LMI): the Grunsky matrix G must satisfy ||G||_op ≤ 1. This makes the univalence constraint amenable to SDP.

## Mathematical Framework

For f(z) = z + Σ_{n=2}^N a_n z^n, the Grunsky coefficients c_{mn} are defined by:
```
log(f(z) - f(ζ))/(z - ζ) = -Σ_{m,n≥1} c_{mn} z^m ζ^n
```

The Grunsky matrix G_N = (√(mn) c_{mn}) satisfies ||G_N||_op ≤ 1 for univalent f (and equality iff f maps onto a slit domain).

The SDP hierarchy:
- Level N: maximize R subject to:
  - ||G_N|| ≤ 1 (univalence)
  - f(D) ⊃ D(0,R) (covering)
  - f'(0) = 1 (normalization)

## Implementation Backlog

1. **[P0]** Implement Grunsky matrix computation for polynomial f
2. **[P0]** Formulate the SDP in CVXPY/JuMP with MOSEK backend
3. **[P1]** Solve for N=5 and verify against known bounds
4. **[P1]** Scale to N=10,15,20 and track convergence
5. **[P2]** Combine with interval arithmetic (concept 008) for rigorous certification
6. **[P3]** Explore dual SDP for upper bound interpretation
7. **[P3]** Compare convergence rate with Lasserre hierarchy theory
