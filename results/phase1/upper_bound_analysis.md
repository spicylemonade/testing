# Upper Bound Analysis for the Univalent Bloch Constant B_u

---

## 1. Goodman's Original Domain Construction (1945)

### Background

The **univalent Bloch constant** B_u is the largest number such that the image of the unit disk under any conformal map f (with f(0) = 0, f'(0) = 1) must contain a disk of radius B_u. To find an **upper bound** on B_u, one constructs a specific univalent function whose image fails to contain any large disk.

### Ruth Goodman's Construction

Ruth E. Goodman ("On the Bloch-Landau constant for schlicht functions," *Bull. Amer. Math. Soc.* 51, 1945, pp. 234–239) introduced the first non-trivial domain construction yielding an upper bound for B_u.

**The Goodman Domain**: Consider a disk of some radius R from which three symmetric radial slits are removed. Specifically:

1. Start with the disk D(0, R) = {w : |w| < R}.
2. Remove three radial line segments placed at 120° angles:
   - L_1 from r_0 to R along the positive real axis
   - L_2 from r_0·e^{2πi/3} to R·e^{2πi/3}
   - L_3 from r_0·e^{4πi/3} to R·e^{4πi/3}

where r_0 is chosen to optimize the bound.

3. The resulting domain Ω = D(0, R) \ (L_1 ∪ L_2 ∪ L_3) is simply connected.

4. By the Riemann mapping theorem, there exists a unique conformal map f : **D** → Ω with f(0) = 0, f'(0) > 0.

5. After normalization to f'(0) = 1, the domain f(**D**) = Ω / f'(0) has an inradius that can be computed.

### The Threefold Symmetry Principle

The three slits create a domain with **threefold rotational symmetry** (C_3 symmetry). This is not accidental—it reflects the geometric intuition that the worst domain for the covering problem distributes its boundary features symmetrically.

**Why threefold?** The inradius of a domain is the supremum of radii of inscribed disks. In a domain with three symmetric slits, the largest inscribed disk fits between two adjacent slits. The three-fold arrangement minimizes the inradius relative to the conformal radius, as it equally constrains inscribed disks in all directions.

### Goodman's Result

Goodman showed that the optimal choice of slit parameters gives:

> **B_u ≤ 0.6565...**

(approximate value; the exact value depends on the optimization over slit length and starting radius).

### Limitations of Goodman's Domain

1. **Straight radial slits**: The boundary arcs are line segments, which is geometrically rigid. There is no reason the extremal domain should have straight boundaries.
2. **No variational optimality**: The domain was constructed by explicit choice, not by solving a variational problem. Jenkins' later work showed that extremal domains must satisfy specific boundary conditions (tangency with extremal disks) that Goodman's domain does not respect.
3. **Slit endpoints in the interior**: The inner endpoints of the slits create artificial singularities that may not be present in the true extremal domain.

---

## 2. Carroll & Ortega-Cerdà's Harmonic Symmetry Modification (2009)

### Reference

T. Carroll and J. Ortega-Cerdà, "The univalent Bloch-Landau constant, harmonic symmetry and conformal glueing," *J. Math. Pures Appl.* 92 (2009), no. 4, pp. 396–406. (arXiv: 0806.2282)

### Key Innovation: Harmonic Symmetry

Carroll and Ortega-Cerdà modified Goodman's domain by replacing the straight radial slits with **curved arcs** satisfying the condition of **harmonic symmetry**.

**Definition (Harmonic Symmetry)**: An arc γ in a domain D is *harmonically symmetric with respect to a point z_0 ∈ D* if, for the harmonic measure ω(z_0, ·, D), the measure is equally distributed on the two sides of the arc. Equivalently, the harmonic measure of γ as seen from z_0 in the domain D \ γ is equal from both sides.

More precisely, if D is a simply connected domain containing z_0, and γ is an arc of ∂D, then γ is harmonically symmetric in D with respect to z_0 if:
- Viewing γ from z_0, the harmonic measure of the "left" and "right" sides of the boundary arc are balanced in a specific sense related to the conformal map to the disk.

### The Modified Domain

The Carroll-Ortega-Cerdà domain takes the form:

> **Ω = D(0, R) \ (γ_1 ∪ γ_2 ∪ γ_3)**

where:
- D(0, R) is a disk of radius R
- γ_1, γ_2, γ_3 are three arcs placed at 120° angles
- Each arc γ_j lies on a circle (not a straight line) and is **harmonically symmetric in Ω with respect to the origin**

The key insight from Carroll's earlier work (2008) was that **extremal domains for B_u must satisfy the harmonic symmetry condition** on each boundary arc that touches an extremal disk. By building this condition directly into the domain construction, they obtain a domain closer to the actual extremal domain.

### Conformal Welding Technique

The existence of domains with the required harmonic symmetry property is established using **conformal welding** (also called conformal glueing):

1. Specify the desired harmonic measure distribution on the boundary.
2. Use conformal welding theory to prove that a Jordan domain with this boundary structure exists.
3. The welding homeomorphism φ : S¹ → S¹ determines the domain via the Riemann map.

The conformal welding approach is non-constructive (existence, not explicit formula), but the resulting domain can be approximated numerically.

### Connection to Fedorov's Work

The numerical computation of the domain parameters exploits Fedorov's explicit solution of the Pólya-Chebotarev problem for four symmetrically placed points (see Section 3 below). The removed arcs are configured so that their endpoints form a symmetric point configuration for which Fedorov's formulas apply.

### The Improved Upper Bound

Carroll and Ortega-Cerdà obtained:

> **B_u ≤ 0.6563937...**

which is a small but definite improvement over Goodman's bound. The precise value is computed as:

> B_u ≤ U, where U is determined by the equation involving the capacity of the extremal continuum from Fedorov's solution.

The improvement arises because:
1. The harmonic symmetry condition is a necessary condition for extremality.
2. Curved arcs satisfying this condition distribute the boundary measure more efficiently than straight slits.
3. Fedorov's explicit capacity formulas allow exact computation.

---

## 3. The Pólya-Chebotarev / Fedorov Connection

### The Pólya-Chebotarev Problem

**Problem (Pólya, 1929; suggested by Chebotarev)**: Given a finite set of points E = {a_1, ..., a_n} ⊂ **C**, find the continuum K ⊃ E of minimal logarithmic capacity.

**Theorem (Laurentiev, 1934)**: The extremal continuum exists, is unique, and has the following properties:
1. Every point of **C** belongs to either the extremal domain Ω = **C** \ K or to K.
2. The boundary K consists of finitely many simple arcs of analytic curves.
3. The points a_i are endpoints of distinct arcs.
4. If k arcs emanate from a point of K, adjacent arcs form angles of 2π/k.
5. The arcs are trajectories of a specific quadratic differential.

### Fedorov's Explicit Solution (1985)

**Reference**: S. I. Fedorov, "On a variational problem of Chebotarev in the theory of capacity of plane sets and covering theorems for univalent conformal mappings," *Math. USSR-Sb.* 52 (1985), no. 1, pp. 115–133.

Fedorov solved the Pólya-Chebotarev problem explicitly in the case of **four symmetrically placed points**: E = {a, ia, -a, -ia} (or more generally, four points with fourfold symmetry, or specific configurations with threefold symmetry).

**Key results**:

1. **Extremal continuum structure**: For four points at the vertices of a square, the extremal continuum consists of arcs connecting the points through the center, forming a cross-like structure. The exact shape involves elliptic integrals.

2. **Capacity formula**: The logarithmic capacity of the extremal continuum is expressed in terms of:
   - Elliptic integrals K(k) and K'(k)
   - The modulus k determined by the geometric configuration
   - Explicit algebraic relations among the parameters

3. **Differential equation**: The conformal mapping from the unit disk to the complement of the extremal continuum satisfies:

   > [zf'(z)/f(z)]² = C · ∏(f(z) - a_i) / ∏(f(z) - b_j)

   where the b_j are accessory parameters and C is determined by normalization.

### Application to the Bloch Constant

The connection to the univalent Bloch constant arises as follows:

1. **Domain construction**: Start with a disk of radius R and remove arcs to create a simply connected domain Ω.
2. **Endpoints of arcs**: The inner endpoints of the removed arcs form a finite point set E.
3. **Optimization**: The capacity of the continuum formed by the arcs determines (via conformal mapping) the relationship between R and the normalization f'(0) = 1.
4. **Fedorov's formulas**: For three symmetric arcs (related to the four-point problem by symmetry), the capacity can be computed explicitly.

The extremal continuum from the Pólya-Chebotarev problem gives the **most efficient** boundary for the removed arcs, in the sense that it minimizes the "cost" (in terms of conformal capacity) of creating the slits. This is why Fedorov's result leads to the best upper bound.

### The Ortega-Cerdà & Pridhnani Numerical Implementation

Ortega-Cerdà and Pridhnani ("The Pólya-Tchebotaröv problem," *Contemporary Mathematics* 505, 2010, pp. 153–170) described a numerical implementation of the Pólya-Chebotarev solution that can handle general point configurations. This allows computation of optimal continua and their capacities for any finite point set, enabling systematic numerical optimization of upper bound domains.

---

## 4. Current Best Upper Bound Value for B_u

### Summary of Upper Bounds

| Year | Author(s) | Upper Bound | Method |
|------|-----------|-------------|--------|
| 1935 | Robinson | B_u ≤ ~0.75 | Koebe function estimate |
| 1945 | Goodman | B_u ≤ 0.6565... | Three-slit disk domain |
| 2009 | Carroll & Ortega-Cerdà | **B_u ≤ 0.6564...** | Harmonic symmetric arcs + Fedorov |

The precise current best upper bound from Carroll-Ortega-Cerdà:

> **B_u ≤ 0.6563937...**

Note: The improvement from Goodman's bound is small (in the fourth decimal place). This suggests that Goodman's straight-slit construction was already close to optimal among three-slit domains, and the harmonic symmetry condition provides a fine-tuning rather than a qualitative change.

### The Current Gap

Combining with Skinner's lower bound:

> **0.5708858 < B_u ≤ 0.6563937...**

The gap is approximately **0.0855**, or about **13%** of the midpoint estimate.

### Comparison with Related Constants

For context:
- **Bloch constant B**: 0.4332... ≤ B ≤ 0.4719... (gap ~0.039)
- **Landau constant L**: 0.5 < L ≤ 0.5433... 
- **Univalent Bloch constant B_u**: 0.5709... ≤ B_u ≤ 0.6564...

The gap for B_u is proportionally larger than for B, suggesting more room for improvement.

---

## 5. Analysis: Are Tighter Upper Bounds Achievable?

### 5.1. Evidence That the Current Upper Bound Is Not Sharp

Several lines of evidence suggest B_u < 0.6564:

1. **Jenkins' criterion not fully satisfied**: The Carroll-Ortega-Cerdà domain satisfies the harmonic symmetry condition (a necessary condition for extremality) but does not necessarily satisfy all conditions from Jenkins' theory. In particular, the tangency conditions between the domain boundary and extremal disks may not be fully optimal.

2. **Fixed number of arcs**: The domain uses exactly three removed arcs (threefold symmetry). The true extremal domain might have:
   - More than three boundary components
   - A different symmetry order
   - Arcs of different shapes than those arising from the four-point Pólya-Chebotarev solution

3. **Non-optimal arc placement**: The arcs are placed symmetrically, but the angular positions and radial depths are optimized within a restricted parameter family. A more general parameterization might yield a better bound.

### 5.2. Potential Approaches for Tighter Upper Bounds

#### Approach A: Higher-Order Symmetry Domains

Replace threefold symmetry with N-fold symmetry for N = 4, 5, 6, ... and compare inradii. For each N, construct the optimal N-slit domain satisfying harmonic symmetry and compute B_f.

**Analysis**: As N → ∞, the N-slit domain approaches a nearly circular boundary, and B_f → R (the conformal radius). For the normalized map, this gives B_f → 1/4 (Koebe), which is worse. So there is likely an optimal N, and the question is whether N = 3 is already optimal.

#### Approach B: Non-Symmetric Domains

Relax the symmetry assumption and search over asymmetric domains. This vastly increases the parameter space but could reveal that the extremal domain is not perfectly symmetric.

**Caveat**: By Jenkins' theory, the extremal domain is expected to have the same symmetry as its extremal disk configuration. If there are three extremal disks equally spaced, threefold symmetry is natural.

#### Approach C: Conformal Welding Optimization

Use the conformal welding framework more aggressively:
1. Parameterize the welding homeomorphism φ by a finite-dimensional family (e.g., Fourier coefficients).
2. For each φ, compute the resulting domain, its conformal map, and its inradius.
3. Minimize the inradius over the parameter space.

This is computationally intensive but could find domains with smaller inradii than the Carroll-Ortega-Cerdà construction.

#### Approach D: Variational Method with Multiple Extremal Disks

Consider domains with k extremal disks (k = 2, 3, 4, ...) and solve the variational problem exactly for each k.

For k = 3 (three extremal disks at 120°):
- The domain boundary consists of arcs connecting the extremal disk boundaries.
- The variational equations (Euler-Lagrange conditions from Jenkins' theory) determine the arc shapes.
- The resulting system can be solved numerically with high precision.

This approach directly targets the extremal domain rather than constructing ad hoc domains.

### 5.3. Theoretical Barriers to Closing the Gap

1. **Lack of conjecture**: Unlike the Bloch constant B (where the Ahlfors-Grunsky conjecture gives a precise target), there is no widely accepted conjecture for the exact value of B_u. Without a target, it is difficult to know when the bounds are close to sharp.

2. **Computational complexity**: The extremal domain for B_u is defined by a free boundary problem that couples:
   - The conformal map f
   - The location and size of extremal disks
   - The boundary geometry (harmonic symmetry conditions)
   
   This coupled system has no known closed-form solution, making analytical progress difficult.

3. **Non-computable aspects**: Rettinger (2008) studied the computability of Bloch's constant, showing it is computable but that the rate of convergence of computational schemes is unknown. Similar issues may apply to B_u.

### 5.4. Most Promising Direction

The most promising approach for a tighter upper bound is:

**Direct numerical solution of the variational problem with threefold symmetry.**

Specifically:
1. Assume the extremal domain has threefold symmetry with three extremal disks of radius r centered at points w_1, w_2, w_3 = w_1·e^{2πi/3}, w_1·e^{4πi/3}.
2. The boundary ∂D_f consists of arcs connecting the extremal disk boundaries.
3. Each arc satisfies the harmonic symmetry condition (Carroll 2008).
4. The conformal map f : **D** → D_f satisfies f(0) = 0, f'(0) = 1.
5. Minimize r over all valid configurations (w_1, arc shapes).

This is a finite-dimensional optimization problem (essentially optimizing over |w_1| and the arc shape parameter), which can be solved numerically to high precision. The result would give a much tighter upper bound and might effectively determine B_u to several decimal places.

---

## 6. Connections to Broader Mathematical Framework

### 6.1. Brownian Motion and Expected Lifetime

The univalent Bloch constant is related to the **maximal expected lifetime of Brownian motion** on simply connected domains of inner radius 1. Specifically, if τ_Ω denotes the first exit time of Brownian motion from Ω started at a point z_0 where d_Ω(z_0) is maximized, then:

> E[τ_Ω] is bounded above by a function of B_u

This probabilistic interpretation was emphasized by Bañuelos and Carroll (Duke Math. J. 75, 1994) and provides an alternative approach to bounding B_u.

### 6.2. Principal Eigenvalue of the Laplacian

The first Dirichlet eigenvalue λ_1(Ω) of the Laplacian on a simply connected domain Ω satisfies:

> λ_1(Ω) · R_Ω² ≥ c

where R_Ω is the inradius and c is a universal constant related to B_u. Improvements in B_u directly translate to improvements in eigenvalue estimates.

### 6.3. Hyperbolic Metric

The constant B_u is closely related to the infimum of the hyperbolic density σ_Ω(z_0) over simply connected domains Ω, where z_0 is a point achieving the inradius. The relationship is:

> σ_Ω(z_0) · d_Ω(z_0) ≥ 1/2 (classical)

with the optimal constant being determined by B_u.

---

## 7. Summary and Outlook

### Current State

| Bound | Value | Source |
|-------|-------|--------|
| Best lower bound | B_u > 0.5708858 | Skinner (2009) |
| Best upper bound | B_u ≤ 0.6563937 | Carroll & Ortega-Cerdà (2009) |
| Gap | ~0.0855 | |

### Key Open Questions

1. **What is the exact value of B_u?** There is no known conjecture.
2. **Does the extremal domain have threefold symmetry?** Strongly expected but not proven.
3. **How many extremal disks does the extremal domain have?** Expected: three, by analogy with related problems.
4. **Can the lower bound be significantly improved?** The current method (Skinner) seems far from optimal; approaches using Jenkins-Carroll theory could yield substantial improvements.
5. **Is B_u algebraic or transcendental?** Likely transcendental (involves elliptic integrals), but unknown.

### Assessment of Tightening Prospects

- **Upper bound tightening**: Achievable but likely to yield only small improvements (0.001–0.01) since the current construction already incorporates the main structural features of extremal domains.
- **Lower bound tightening**: More promising, with potential for improvements of 0.01–0.05 or more, since the current method is relatively crude.
- **Closing the gap**: Would require a fundamentally new approach, likely involving direct numerical computation of the extremal domain coupled with rigorous error bounds.

The univalent Bloch constant remains one of the most interesting open problems in geometric function theory, connecting conformal mapping, potential theory, extremal problems, and probability.
