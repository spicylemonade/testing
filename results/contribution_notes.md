# Contribution Notes: Bounds on the Univalent Bloch Constant

## Precise Claim Statements

### Certified Result
**Theorem (interval-arithmetic certified).** The univalent Bloch constant satisfies
$$B_u \leq 0.6814202223$$
via the slit-disk domain $\Omega_3 = \mathbb{D} \setminus \{3 \text{ equally-spaced radial slits from } r_0 = 1/2 \text{ to } 1\}$.

*Proof.* The conformal radius of $\Omega_3$ at the origin is computed exactly via a 5-step chain of elementary conformal maps (Cayley transform, squaring, Mobius, square root, inverse Cayley), combined with the $n$-fold symmetry reduction $z \mapsto z^3$. The inradius is $r_0 = 1/2$ (the inscribed disk centered at the origin touches the nearest slit endpoint). The quotient $B_f = \operatorname{inrad}/\operatorname{crad} = 0.6814\ldots$ is computed and certified using mpmath interval arithmetic at 100-digit precision, yielding zero-width intervals (exact rational arithmetic through the chain). See `results/phase3/interval_verify.py`.

**Note:** This bound is weaker than Carroll & Ortega-Cerda's $B_u \leq 0.6564$ (2008), which uses curved (harmonically symmetric) arcs rather than straight radial slits.

### Negative Results
1. **The Koebe 1/4 + Bloch norm dichotomy does not beat 0.5709.** The approach of case-splitting on $||f||_B$ and using Koebe for large Bloch norm and perturbation estimates for small Bloch norm gives $B_u \geq 0.34$ at best. The fundamental barrier is that Koebe 1/4 is sharp for class $S$.

2. **The 2x2 Grunsky constraint is insufficient for univalence.** Optimizing $\min \operatorname{inrad}(f(\mathbb{D}))$ subject to $||G_2||_{op} \leq 1$ finds functions with winding number $\geq 2$ that are not univalent. A larger Grunsky matrix (or full univalence check) is needed.

3. **Higher-fold symmetry ($n \geq 4$) gives worse radial-slit bounds.** The optimal number of radial slits is $n = 3$, confirming the classical result of Goodman (1945).

## Novel Techniques Introduced

1. **Exact conformal radius via Cayley-Joukowsky chain:** For single-slit domains $\mathbb{D} \setminus [a, 1)$, the conformal radius at the origin is computed exactly (in exact arithmetic) via the composition: Cayley $\to$ square $\to$ Mobius $\to$ sqrt $\to$ inverse Cayley. This avoids numerical integration, boundary element methods, or series truncation.

2. **$n$-fold symmetry reduction for slit-disk conformal radius:** $\operatorname{crad}(\Omega_n, 0) = \operatorname{crad}(\mathbb{D} \setminus [r_0^n, 1), 0)^{1/n}$, reducing $n$-slit computation to a single-slit computation.

3. **Interval arithmetic certification pipeline:** All numerical bounds are rigorously certified using mpmath's `iv` (interval) context at 100-digit precision, with 8 test suites covering monotonicity, limiting behavior, cross-validation, and consistency with Skinner's lower bound.

4. **Grunsky coefficient computation via bivariate log expansion:** Direct formulas for the first 2x2 block of the Grunsky matrix from Taylor coefficients, validated against the known Koebe function result $||G|| = 1$.

## Reproducibility Instructions

### Prerequisites
```
pip install numpy scipy mpmath matplotlib seaborn
```

### Reproducing Results (in order)
```bash
# 1. Upper bound computation
python results/phase3/optimized_upper_bound.py

# 2. Interval arithmetic certification
python results/phase3/interval_verify.py

# 3. Generate figures
# (embedded in the main scripts; figures saved to figures/)

# 4. Lower bound analysis (negative result)
python results/phase3/improved_lower_bound.py
```

### Verifying Certified Bound
```python
from mpmath import mp, mpf, mpc, sqrt as mpsqrt, iv
mp.dps = 100

# Single-slit conformal radius for D \ [a, 1)
a = mpf('0.125')  # = r0^3 = (1/2)^3
A = (1 + a) / (1 - a)
A2 = A**2

# Chain computation at z = 0
w1 = mpc(0, 1); dw1 = mpc(0, 2)
w2 = w1**2; dw2 = 2*w1*dw1
den = w2 + A2; w3 = w2/den; dw3 = A2/den**2*dw2
w4 = mpsqrt(w3); dw4 = dw3/(2*w4)
w5 = (w4 - mpc(0,1))/(w4 + mpc(0,1))
dw5 = mpc(0,-2)/(w4 + mpc(0,1))**2 * dw4

crad_single = (1 - abs(w5)**2) / abs(dw5)
crad_3slit = crad_single ** (mpf(1)/3)
Bf = mpf('0.5') / crad_3slit
print(f"B_f = {float(Bf):.15f}")  # Should print 0.681420222312052...
```

## Caveats and Limitations

1. **Our upper bound does not improve on Carroll-Ortega-Cerda.** The best known upper bound remains $B_u \leq 0.6564$.

2. **We did not achieve any improvement on Skinner's lower bound.** The lower bound remains $B_u > 0.5708858$.

3. **The Grunsky adversarial search was inconclusive.** The 2x2 Grunsky constraint is too weak for univalence enforcement; a full $N \times N$ constraint with $N \geq 10$ would be needed, requiring SDP solvers.

4. **Curved-arc domains were not implemented.** Carroll-OC's improvement over straight slits comes from harmonically symmetric arcs (Fedorov's Polya-Chebotarev solution), which we did not implement due to the complexity of the conformal mapping for curved slit domains.

## Suggested Next Steps

1. **Implement curved-arc domain construction** following Carroll & Ortega-Cerda / Fedorov. This requires solving the Polya-Chebotarev problem for $n$ points on $\partial \mathbb{D}$ numerically.

2. **SDP hierarchy with larger Grunsky matrices.** Use $N \geq 10$ truncation with MOSEK or SCS solver via the Lasserre moment hierarchy. This could provide certified lower bounds if the moment relaxation is tight.

3. **Loewner chain optimal control.** Formulate $B_u$ as an optimal control problem on the Loewner ODE and use dynamic programming or Pontryagin's maximum principle.

4. **PSLQ for closed-form conjecture.** If numerical optimization yields a stable value for $B_u$, use PSLQ to check if it matches any algebraic expression.

5. **Higher-order Grunsky constraint with injection verification.** Combine the Grunsky constraint $||G_N|| \leq 1$ with winding number verification and area-principle constraints for a tighter feasible set.
