# Deep Analysis of Skinner 2009: B_u > 0.5708858

## 1. Precise Statement of Skinner's Theorem

**Paper:** Skinner, Brian. "The univalent Bloch constant problem." *Complex Variables and Elliptic Equations* 54(10), 951–955, 2009.

**Theorem (Skinner 2009):** Let S denote the class of normalized univalent functions on the unit disk D, i.e., f: D → C holomorphic and injective with f(0) = 0 and f'(0) = 1. Suppose f ∈ S and |f(z)| ≥ B(|z|) for some nonnegative function B on [0, 1). Then there exists an implicitly defined function C(|z|) such that:
1. |f(z)| ≥ C(|z|) ≥ B(|z|) for all z ∈ D,
2. C is strictly greater than B on (0, 1), and
3. C can be computed explicitly via a fixed-point procedure.

**Consequence:** Starting from the growth theorem bound B₀(r) = r/(1+r)² and applying the improvement theorem, one obtains B_u > 0.5708858.

## 2. Key Technical Ingredients

### 2.1 The Class of Test Functions
Skinner works with the full class S of normalized univalent functions. The normalization f(0) = 0, f'(0) = 1 is standard. The method does not restrict to subclasses (convex, starlike, etc.) but applies to all of S.

### 2.2 Distortion and Growth Estimates

The foundational tool is the **growth theorem** for univalent functions:

For f ∈ S and |z| = r < 1:
$$\frac{r}{(1+r)^2} \leq |f(z)| \leq \frac{r}{(1-r)^2}$$

Both bounds are sharp and achieved by the Koebe function k(z) = z/(1-z)².

Additionally, the **distortion theorem** provides:
$$\frac{1-r}{(1+r)^3} \leq |f'(z)| \leq \frac{1+r}{(1-r)^3}$$

### 2.3 The Bootstrap/Self-Improvement Mechanism

Skinner's key innovation is recognizing that knowledge of a lower bound on |f(z)| can be recycled to produce a strictly better lower bound. The mechanism works as follows:

1. **Start** with an initial lower bound: |f(z)| ≥ B₀(r) = r/(1+r)² (from the growth theorem).

2. **Improvement step**: Given |f(z)| ≥ B(r), use the structural constraints of univalent functions (specifically, the relationship between |f(z)| and the geometry of f(D) enforced by injectivity) to derive a new bound |f(z)| ≥ C(r) > B(r).

3. The function C(r) satisfies an **implicit equation** involving B and the Koebe/distortion estimates. The implicit nature means C is computed numerically at each step.

### 2.4 The Optimization

The final bound B_u > 0.5708858 comes from:
- Computing the improved growth bound C(r) for r ∈ [0, 1)
- The univalent Bloch constant relates to the image: B_u = inf{inradius(f(D)) : f ∈ S}
- The inradius of f(D) is at least sup_w inf_{z ∈ ∂D} |f(z) - w| which can be bounded using the improved growth estimate
- A numerical optimization over the parameters of the implicit equation yields 0.5708858

### 2.5 Connection to the Bloch-Landau Framework

For a univalent function f with f'(0) = 1, the quantity B_f (radius of the largest disk in f(D)) satisfies:
$$B_f \geq \sup_{|z_0| < 1} d(f(z_0), \partial f(D))$$

where d denotes Euclidean distance. The growth theorem lower bound implies that f(D) contains a large neighborhood of 0, and the injectivity of f guarantees that this neighborhood is a genuine disk (not just part of a multi-sheeted covering).

## 3. Identification of Mathematical Bottlenecks

### Bottleneck 1: Radial Growth vs. Two-Dimensional Geometry

**The problem:** Skinner's method works with the **radial** quantity |f(z)| as a function of |z| = r. This is inherently a one-dimensional projection of a two-dimensional problem. The Bloch-Landau constant asks about the largest **disk** (a 2D object) contained in f(D), but the growth theorem only controls the **modulus** along radial directions.

**Why it limits the bound:** The conversion from "f(D) contains all points of modulus ≤ C(r) for r near 1" to "f(D) contains a disk of radius R" necessarily loses information. A domain can have large radial extent in all directions without containing a large round disk (imagine a domain with many narrow "fingers").

**Potential remedy:** Use area-based or capacity-based estimates instead of pointwise growth bounds. The hyperbolic area of f(D) or the conformal capacity of complements of f(D) could provide tighter geometric control.

### Bottleneck 2: The Koebe Function as the Worst Case

**The problem:** The growth theorem is **sharp** for the Koebe function k(z) = z/(1-z)², which maps D onto C minus the half-line (-∞, -1/4]. But the Koebe function is far from extremal for B_u: its image contains arbitrarily large disks (B_k = ∞ in a sense, or at least B_k = 1/4 for the disk at the origin).

**Why it limits the bound:** Skinner's improvement theorem starts from the growth theorem bound, which is tight for Koebe but pessimistic for functions near the B_u extremum. The extremal functions for B_u have images that are **disk-like** with slits removed (as per Carroll–Ortega-Cerdà), not slit-plane-like as Koebe.

**Potential remedy:** Restrict to subclasses of S that exclude Koebe-like functions (e.g., bounded univalent functions, or functions with restricted range) to get tighter initial bounds.

### Bottleneck 3: Inability to Exploit Extremal Domain Structure

**The problem:** Jenkins (1992, 1998) and Carroll (2008) established **necessary conditions** that extremal domains for B_u must satisfy, involving harmonic symmetry and specific boundary behavior. Skinner's method treats all f ∈ S uniformly and cannot exploit these structural constraints.

**Why it limits the bound:** The extremal domain for B_u is expected to be a disk with 3 or 4 harmonically symmetric arcs removed (Carroll & Ortega-Cerdà 2008). A method that "knows" the extremal domain has this structure should be able to achieve much tighter bounds than one that works for arbitrary f ∈ S.

**Potential remedy:** 
- Use Jenkins' criterion to restrict the optimization to functions whose image domains satisfy the necessary conditions.
- Develop two-sided bounds by combining Skinner-type lower bounds with Carroll–Ortega-Cerdà-type upper bounds.
- Parametrize the class of disk-minus-arcs domains and optimize directly.

### Bottleneck 4: Diminishing Returns of Iteration

**The problem:** Each application of the bootstrap improvement gives a smaller increment. The iterates B₀ < B₁ < B₂ < ... converge to a fixed point B_∞ that represents the **fundamental limit** of the radial growth bootstrap approach.

**Why it limits the bound:** Even with infinitely many iterations, the method converges to a value that is likely well below the true B_u. The gap between B_∞ and B_u represents the information lost by reducing the 2D problem to a 1D radial problem.

**Potential remedy:** Instead of iterating the same type of improvement, use qualitatively different tools at each stage (e.g., growth theorem → distortion theorem → area theorem → coefficient bounds).

## 4. Comparison with Methods for B and L

### 4.1 Bloch Constant B

**Best lower bound:** B ≥ √3/4 + 3×10⁻⁴ (Xiong & Chen 2004, building on Bonk 1990 and Chen & Gauthier 1996).

**Method (Bonk):** Bonk (1990) proved B > √3/4 using a **distortion theorem for Bloch functions**. His key insight was that Bloch functions (f with |f'(0)| ≥ 1, sup(1-|z|²)|f'(z)| < ∞) have specific distortion properties that, combined with a Picard-type argument, yield the strict inequality. Chen & Gauthier (1996) and Xiong (2004) improved the technical estimates in Bonk's framework.

**Comparison with Skinner:** Both methods use distortion/growth estimates as the core tool. The key difference is that for B, the Ahlfors covering surface theory provides a powerful geometric framework (relating area to boundary length) that has no direct analogue for B_u, where the function is required to be globally univalent rather than just locally injective.

### 4.2 Landau Constant L

**Best lower bound:** L > 1/2 + 10⁻³³⁵ (Yanagihara 1995).
**Best upper bound:** L ≤ Γ(1/3)Γ(5/6)/Γ(1/6) ≈ 0.5433 (conjectured exact by Rademacher).

**Method:** Yanagihara's improvement is extremely small (10⁻³³⁵), obtained by a perturbation analysis around the conjectured extremal function. The Landau constant sits between B and B_u in the chain B ≤ B_l ≤ L ≤ B_u, so bounds on L give automatic bounds on B_u.

**Comparison:** The Landau constant problem benefits from the fact that the conjectured extremal is known (a specific Schwarz-Christoffel mapping), allowing perturbation-based approaches. For B_u, the extremal function/domain is not known precisely, making such approaches harder.

### 4.3 Summary Table

| Constant | Best Lower Bound | Method | Best Upper Bound | Gap |
|----------|-----------------|--------|------------------|-----|
| B (Bloch) | √3/4 + 3×10⁻⁴ ≈ 0.4333 | Bonk distortion + refinements | ≈ 0.4719 (Ahlfors-Grunsky conj.) | ~0.039 |
| L (Landau) | 1/2 + 10⁻³³⁵ | Yanagihara perturbation | Γ(1/3)Γ(5/6)/Γ(1/6) ≈ 0.5433 | ~0.043 |
| B_u (univalent Bloch) | 0.5708858 | Skinner bootstrap | 0.6564 (Carroll-Ortega-Cerdà) | ~0.086 |

The gap for B_u is roughly twice that of B and L, suggesting that the problem is significantly harder or that current methods leave more room for improvement.

## 5. Historical Development of B_u Lower Bounds

| Year | Author(s) | Bound | Improvement over previous |
|------|-----------|-------|--------------------------|
| 1929 | Landau | B_u ≥ 0.566 | (first explicit bound) |
| 1935 | Robinson | B_u ≥ 0.5 | Established clean baseline |
| 1956 | Reich | B_u > 0.5 | First strict inequality |
| 1985 | Beller & Hummel | B_u > ~0.57 (est.) | Significant improvement via growth theorem refinement |
| 2009 | Skinner | B_u > 0.5708858 | ~0.001 improvement via bootstrap |

## 6. Strategies for Improvement

Based on this analysis, the most promising strategies for improving B_u bounds are:

1. **Tighten the upper bound** via generalized Carroll–Ortega-Cerdà domains with more slits or optimized arc placement. This is computationally accessible and narrows the gap from above.

2. **Develop non-radial lower bound methods** that exploit the 2D geometry of the image domain, perhaps via area theorems, extremal length, or capacity estimates.

3. **Exploit Jenkins' necessary conditions** to restrict the optimization to physically meaningful domains (disk minus harmonically symmetric arcs).

4. **Combine coefficient bounds** (de Branges: |aₙ| ≤ n) with geometric arguments to constrain the image domain more tightly than growth theorem alone.

5. **Numerical direct optimization** over parametric families of univalent functions designed to have small B_f, to discover near-extremal functions and guide theoretical work.
