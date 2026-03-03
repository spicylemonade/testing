# Extremal Length and the Univalent Bloch Constant

## 1. Reformulation of B_u in Terms of Extremal Length

### Background on Extremal Length

The **extremal length** (or modulus) of a family of curves Γ in a domain Ω is defined as:

$$\lambda(\Gamma) = \sup_\rho \frac{L(\rho, \Gamma)^2}{A(\rho, \Omega)}$$

where the supremum is over all non-negative Borel measurable functions ρ (metrics), L(ρ, Γ) = inf_{γ ∈ Γ} ∫_γ ρ |dz|, and A(ρ, Ω) = ∫∫_Ω ρ^2 dA.

Extremal length is a conformal invariant: if f: Ω₁ → Ω₂ is conformal and Γ₁ maps to Γ₂ under f, then λ(Γ₁) = λ(Γ₂).

### Connection to Inradius

For a simply connected domain Ω and a point w₀ ∈ Ω, the **inradius at w₀** is d(w₀, ∂Ω). The largest inscribed disk at w₀ has radius d(w₀, ∂Ω).

The extremal length of the family of curves separating w₀ from ∂Ω in an annular region relates to the conformal modulus of that annulus:

**Lemma:** Let Ω be simply connected with w₀ ∈ Ω. Let R = d(w₀, ∂Ω) (inradius at w₀). For 0 < r < R, let Γ(r, R) be the family of curves in D(w₀, R) \ D̄(w₀, r) separating the two boundary components. Then:

$$\lambda(\Gamma(r, R)) = \frac{1}{2\pi} \log(R/r)$$

This is the standard modulus of an annulus.

### Reformulation of B_f

For f ∈ S with Ω = f(D):

$$B_f = \sup_{w₀ ∈ Ω} d(w₀, ∂Ω)$$

The conformal radius R(w₀, Ω) = |f'(f^{-1}(w₀))| · (1 - |f^{-1}(w₀)|²).

By the Koebe bounds: B_f ≤ R(w₀*, Ω) ≤ 4 · B_f where w₀* is the Chebyshev center.

In terms of extremal length: B_f is characterized by the fact that for all w₀ ∈ Ω and all r < B_f, the family of curves separating D(w₀, r) from ∂Ω has positive extremal length.

More precisely: let Γ_w₀ be the family of curves in Ω connecting ∂D(w₀, r) to ∂Ω. The modulus of this family is:

$$\text{mod}(\Gamma_{w₀}) = \frac{1}{2\pi} \log\frac{R(w₀, Ω)}{r}$$

for r < R(w₀, Ω)/4 (where the annular region is conformally equivalent to a genuine annulus).

## 2. Bounds via Modulus Estimates

### Curve Family Approach

Consider the following curve family in the image domain Ω = f(D):

Let Γ_rad be the family of radial curves from the origin to ∂Ω. Each curve γ_θ traces the image of the radius [0, e^{iθ}) under f.

The length of γ_θ in the Euclidean metric is:
$$L(γ_θ) = \int_0^1 |f'(re^{iθ})| dr$$

By the distortion theorem: |f'(re^{iθ})| ≥ (1-r)/(1+r)³.
So L(γ_θ) ≥ ∫₀¹ (1-r)/(1+r)³ dr = 1/4.

This means every radial curve in Ω has length at least 1/4, confirming d(0, ∂Ω) ≥ 1/4.

### Conjugate Extremal Length

The conjugate family Γ* consists of curves separating 0 from ∂Ω.

By the duality λ(Γ) · λ(Γ*) = 1 for ring domains, we get:

If we can bound λ(Γ_rad) from above, we get a bound on λ(Γ*) from below, which in turn bounds the conformal modulus of the ring separating 0 from ∂Ω.

For f ∈ S:
$$\text{Area}(f(D)) = \pi \sum_{n=1}^∞ n|a_n|^2 \geq \pi$$

The extremal length of the radial curves satisfies:
$$\lambda(\Gamma_\text{rad}) \leq \frac{\text{Area}(Ω)}{L_\text{min}^2}$$

Wait, this goes the wrong way. We need:
$$\lambda(\Gamma_\text{rad}) = \sup_\rho \frac{(\inf_γ \int_γ ρ)^2}{\int\int ρ^2}$$

Using ρ = 1/|f'(z)| (pullback of Euclidean metric):
- L_min = inf_θ ∫₀¹ 1 dr = 1 (in the z-plane, the radii have unit Euclidean length)
- A = ∫∫_D 1/|f'|² dA (in the z-plane)

By the distortion theorem: |f'(z)| ≤ (1+r)/(1-r)³ for |z| = r.
So 1/|f'|² ≥ (1-r)⁶/(1+r)² and A ≥ ∫₀¹ 2πr(1-r)⁶/(1+r)² dr.

This gives a bound on the extremal length of radial curves in the z-plane, which by conformal invariance equals the extremal length of the corresponding curves in Ω.

### Modulus of the Ring Domain

For the ring Ω \ D̄(w₀, r) (where D(w₀, r) ⊂ Ω):
The modulus M = (1/2π) log(R(w₀, Ω)/r).

For the Chebyshev center w₀*: R(w₀*, Ω) = |f'(z*)|·(1-|z*|²) and r can be taken up to d(w₀*, ∂Ω) = B_f.

Since B_f ≤ R(w₀*, Ω), the modulus M ≤ (1/2π) log(R(w₀*, Ω)/B_f) ≤ (1/2π) log 4 (by Koebe).

This shows that the conformal modulus is bounded, but doesn't directly give a new bound on B_u.

## 3. Comparison with Ahlfors' Covering Surface Method

Ahlfors (1938) used covering surfaces to bound the Bloch constant B. His method works as follows:

1. Consider f: D → C as a (possibly branched) covering surface over C.
2. Define an "island" as a simply connected region in C covered by a univalent branch of f.
3. Count the number and size of islands using area/perimeter estimates.
4. The largest island gives a disk of radius ≥ B_f.

For univalent f (no branching), the image f(D) is itself the single "island." The covering surface analysis reduces to the study of a single simply connected domain, losing the powerful multi-sheet area comparison that drives Ahlfors' bound for B.

In the extremal length framework:
- Ahlfors' method uses the area/length comparison: Area ≥ L² / λ (from extremal length definition)
- For branched coverings, the total area (counting multiplicity) is large, while the boundary curves have bounded length, forcing large islands
- For univalent maps, the area is at most π (if the image is contained in D), and the extremal length argument gives back the Koebe bound

## 4. New Inequality: Connecting B_u to a Computable Quantity

**Proposition:** For f ∈ S with Ω = f(D), let M(r) denote the conformal modulus of the ring domain Ω \ D̄(0, r) for 0 < r < d(0, ∂Ω). Then:

$$B_f \geq r \cdot e^{2\pi M(r)}$$

*Proof sketch:* The ring Ω \ D̄(0, r) contains a round annulus of modulus M(r). By the Grötzsch modulus theorem, the conformal radius at any point of Ω \ D̄(0, r) is at least r · e^{2πM(r)} / C for a universal constant C. Since B_f is the maximum inscribed disk radius in Ω:
B_f ≥ d(w₀, ∂Ω) for the point w₀ in the "thickest" part of the ring.

More precisely: consider the conformal map g: A(1, e^{2πM(r)}) → Ω \ D̄(0, r), where A(1, R) = {1 < |z| < R} is the standard annulus. The map g extends the identity on the inner boundary |z| = 1 (rescaled by r). By the Koebe bounds for ring domains (Grötzsch distortion theorem), the image of the midline |z| = e^{πM(r)} has Euclidean distance at least r·e^{πM(r)}/4 from both boundary components.

Hence: B_f ≥ r · e^{πM(r)} / 4.

This is a new inequality connecting B_u to the conformal modulus of a specific ring domain, which is a computable geometric quantity.

**Numerical evaluation:** For f = identity (Ω = D):
- d(0, ∂D) = 1, R(0, D) = 1.
- For r = 0.1: M(0.1) = (1/2π) log(1/0.1) = log(10)/(2π) ≈ 0.366.
- Bound: 0.1 · e^{π · 0.366} / 4 = 0.1 · e^{1.15} / 4 ≈ 0.079. (Much weaker than B_f = 1.)

The bound is not tight because the Grötzsch distortion is being applied to the full ring, which is wasteful. The bound improves when r is closer to B_f (i.e., when we already know a good lower bound on d(0, ∂Ω)).

## 5. Assessment

The extremal length approach provides an elegant reformulation of B_u in terms of conformal moduli but does not immediately yield bounds competitive with Skinner's 0.5708858. The main value is:

1. **Structural insight:** The duality between radial and separating curve families illuminates why the Koebe 1/4 bound is hard to improve.
2. **New inequality:** The modulus-inradius bound B_f ≥ r · e^{πM(r)}/4 connects B_u to a computable quantity, albeit with a loose constant.
3. **Framework for improvement:** Replacing the crude Grötzsch distortion with domain-specific estimates (using the known structure of the extremal domain from Jenkins) could tighten the bound.

### References

- [ahlfors1938] Ahlfors, L.V. An extension of Schwarz's lemma. Trans. AMS 43, 359-364, 1938.
- [jenkins1961] Jenkins, J.A. On the schlicht Bloch constant. J. Math. Mech. 10, 729-734, 1961.
- [jenkins1998] Jenkins, J.A. On the schlicht Bloch constant II. Indiana Univ. Math. J. 47(4), 1059-1064, 1998.
- [fedorov1985] Fedorov, S.I. On a variational problem of Chebotarev. Math. USSR-Sb. 52(1), 115-133, 1985.
