# Conformal Welding Bootstrap

## Topic Context

Conformal welding is the inverse problem: given a homeomorphism h: S^1 → S^1, find conformal maps f_+: D → Ω_+ and f_-: D* → Ω_- such that Ω_+ ∪ Ω_- = C and f_+ = f_- ∘ h on S^1. The existence was proved by various authors; uniqueness holds up to Möbius transformations.

The "bootstrap" methodology from conformal field theory (Rattazzi-Rychkov-Tonni-Vichi) has revolutionized the study of CFTs by using semidefinite programming to bound physical quantities from consistency conditions. We propose an analogous approach for the Bloch constant.

## Bootstrap Strategy

1. Parameterize welding homeomorphisms h by Fourier coefficients
2. The condition that f_- is univalent with f_-'(0) = 1 constrains the Fourier coefficients
3. The condition that f_+(D*) ⊃ C \ D(0, R) (complement of a disk) is a covering constraint
4. Both conditions can be expressed as positivity/semidefiniteness conditions on matrices built from the Fourier coefficients
5. SDP feasibility determines whether a given R is achievable
6. Binary search on R gives bounds on B_u

## Implementation Backlog

1. **[P0]** Implement welding from Fourier data using iterative methods
2. **[P1]** Formulate positivity constraints on welding coefficients
3. **[P2]** Set up SDP feasibility problem in CVXPY
4. **[P3]** Binary search for tightest upper bound
5. **[P3]** Compare with Carroll-Ortega-Cerdà's 0.6564
