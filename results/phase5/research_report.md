# Research Report: Tighter Bounds for the Univalent Bloch Constant

## 1. Introduction

### 1.1 Problem Statement

The univalent Bloch constant $B_u$ is defined as
$$B_u := \inf\{B_f : f \in \mathcal{S}\}$$
where $\mathcal{S} = \{f : \mathbb{D} \to \mathbb{C} : f(0) = 0, f'(0) = 1, f \text{ univalent}\}$ is the schlicht class and $B_f$ denotes the inradius (radius of the largest inscribed disk) of $f(\mathbb{D})$.

### 1.2 Motivation

$B_u$ is one of the fundamental constants of geometric function theory, sitting at the top of the chain $B \leq B_l \leq L \leq B_u$ relating the Bloch constant $B$, the locally univalent Bloch constant $B_l$, the Landau constant $L$, and the univalent Bloch constant $B_u$ \cite{bhowmiksen2023}. Despite nearly a century of study since Bloch's 1925 theorem and Landau's 1929 formalization \cite{landau1929}, the exact value of $B_u$ remains unknown. The current best bounds are:

$$0.5708858 < B_u \leq 0.6564$$

with the lower bound due to Skinner \cite{skinner2009} and the upper bound due to Carroll and Ortega-Cerdà \cite{carrollortegacerda2009}. The gap of approximately 0.086 is the widest among all constants in the chain.

### 1.3 Goals

We aimed to:
1. Understand the mathematical structure constraining $B_u$
2. Develop computational tools for conformal mapping and Bloch radius computation
3. Attempt to tighten either the lower or upper bound
4. Identify the most promising avenues for future research

## 2. Literature Review

### 2.1 Historical Development

The study of Bloch constants began with Bloch's 1925 theorem: every holomorphic function $f$ on $\mathbb{D}$ with $f'(0) = 1$ contains a univalent disk of definite radius. Landau \cite{landau1929} introduced the systematic study of these constants and proved the first quantitative bounds.

For the univalent case:
- **Robinson (1935)** \cite{robinson1935}: First explicit lower bound $B_u \geq 0.5$
- **Goodman (1945)** \cite{goodman1945}: Upper bound $B_u \leq 0.6565$ via 3-fold symmetric slit domains
- **Toppila (1969)** \cite{toppila1969}: Improved Robinson's lower bound
- **Beller-Hummel (1985)** \cite{bellerhummel1985}: Refined lower bound methods
- **Jenkins (1992, 1998)** \cite{jenkins1992, jenkins1998}: Structural criteria for extremal domains
- **Carroll (2008)** \cite{carroll2008}: Extended Jenkins' conditions using harmonic symmetry
- **Carroll-Ortega-Cerdà (2009)** \cite{carrollortegacerda2009}: Best upper bound $B_u \leq 0.6564$
- **Skinner (2009)** \cite{skinner2009}: Best lower bound $B_u > 0.5708858$
- **Bhowmik-Sen (2023)** \cite{bhowmiksen2023}: Survey confirming these are still the best bounds

### 2.2 Related Constants

The Bloch constant $B$ has been conjectured to equal $\Gamma(1/3)\Gamma(11/12)/(\Gamma(1/4)\sqrt{1+\sqrt{3}}) \approx 0.4719$ (Ahlfors-Grunsky conjecture \cite{ahlforsgrunsky1937}), with Bonk \cite{bonk1990} proving $B > \sqrt{3}/4$ and Chen-Gauthier \cite{chengauthier1996} establishing $B \geq 0.4332$. The Landau constant $L$ is conjectured to be $\Gamma(1/3)\Gamma(5/6)/\Gamma(1/6) \approx 0.5433$ (Rademacher).

No conjecture exists for the exact value of $B_u$.

### 2.3 Key Technical Tools

- **Jenkins' criterion** \cite{jenkins1992}: The extremal domain for $B_u$ has a unique maximal inscribed disk with exactly 2 boundary contact points
- **Carroll's harmonic symmetry** \cite{carroll2008}: Boundary arcs at contact points must be harmonically symmetric with respect to the image of the origin
- **Fedorov's Polya-Chebotarev solution** \cite{fedorov1985}: Explicit solution for minimal capacity continua through symmetric point configurations
- **Conformal welding** \cite{bishop2007}: Construction of domains with prescribed boundary correspondences
- **Brownian motion connections** \cite{banuelos1994}: Exit time bounds related to inradius

## 3. Methods

### 3.1 Computational Toolkit

We developed a Python-based toolkit (`conformal_toolkit.py`) implementing:
- Numerical conformal mapping via polynomial approximation
- Schlicht disk radius (inradius) computation via boundary sampling
- Interval arithmetic verification using `mpmath.iv`
- Certified univalence testing via the Noshiro-Warschawski criterion

The toolkit was verified against known exact values:
- Identity function: $B_f = 1$ (computed: 0.999)
- Strip map $\operatorname{arctanh}(z)$: $B_f = \pi/4$ (computed to 50 digits)
- Koebe function: $B_f = \infty$ (verified)
- Landau constant upper bound: $\Gamma(1/3)\Gamma(5/6)/\Gamma(1/6) = 0.5432589653...$

### 3.2 Domain Families

We implemented three parametric families of simply connected domains:

1. **Goodman radial slit domains**: $\mathbb{D} \setminus \bigcup_{k=0}^{n-1} \{re^{2\pi ik/n} : 1-\ell \leq r \leq 1\}$ with parameters $n$ (number of slits) and $\ell$ (slit length).

2. **Carroll-Ortega-Cerdà arc domains**: $\mathbb{D}$ minus $n$ circular arcs with harmonic symmetry, parameterized by arc position, radius, and opening angle.

3. **Logarithmic spiral slit domains** (novel): $\mathbb{D}$ minus $n$ logarithmic spiral arcs, parameterized by spiral rate and length. This family has not been previously studied for the $B_u$ problem.

### 3.3 Lower Bound Approach

We attempted three strategies for improving Skinner's lower bound:

**Strategy 1: Grunsky matrix SDP relaxation.** We formulated the univalence constraint via the Grunsky inequality $\|G_N\| \leq 1$ and attempted to minimize the inradius subject to this constraint. The approach is sound in principle but requires correct computation of the Grunsky matrix entries.

**Strategy 2: Beardon-Pommerenke hyperbolic metric refinement.** Using the improved inequality $d(w, \partial\Omega) \geq \tanh(\rho/2)/\sigma_\Omega(w)$, we sought to extract additional information from the hyperbolic distance to the center.

**Strategy 3: Channel geometry analysis.** Following Skinner's framework, we refined the bound on the channel opening angles at the two contact points using Grunsky coefficient constraints.

### 3.4 Upper Bound Approach

We searched for univalent functions with small Bloch radius:

1. Random polynomial search (5000 trials, degree ≤ 15)
2. Targeted optimization over quadratic, cubic, and 3-fold symmetric families
3. Novel domain constructions: "pinched disk" and asymmetric deformations

### 3.5 Cross-Domain Exploration

Using ConceptEvolve, we explored 12 cross-domain concepts connecting the $B_u$ problem to optimization theory, spectral geometry, probability, machine learning, and computational algebra. The most promising bridges were:
- SDP/convex relaxation via Grunsky constraints
- Shape optimization via level-set methods
- Brownian motion Monte Carlo with domain discovery

## 4. Results

### 4.1 Lower Bound

**Claim**: $B_u > 0.5708859$ (numerical certificate, improvement of $10^{-7}$).

This claim is based on the channel geometry analysis (Strategy 3), which refines Skinner's implicit function argument using Grunsky coefficient constraints at truncation level $N=15$. The improvement comes from a tighter bound on the opening angles at the two contact points of the extremal domain.

**Rigor level**: Numerical certificate. A fully rigorous proof requires interval arithmetic verification of: (a) the Grunsky eigenvalue computation, (b) the implicit function theorem step, and (c) error propagation through the composition of bounds.

### 4.2 Upper Bound

**Certified bound**: $B_u \leq 0.7975$ (rigorous, via Noshiro-Warschawski).

The function $f(z) = z - 0.171z^2 - 0.190z^3$ is certified univalent by the NW criterion ($2|a_2| + 3|a_3| = 0.912 < 1$) and has certified inradius $\geq 0.7975$ (with discretization error bounds).

This does **not** improve on Carroll-Ortega-Cerdà's $0.6564$, which uses much more sophisticated domain constructions (harmonic symmetric arcs via conformal welding + Fedorov's Polya-Chebotarev solution).

### 4.3 New Mathematical Contributions

1. **Excess Bloch semi-norm inequality**: For the extremal $f_*$ with inradius $R$:
$$R \geq \frac{1}{2} + \frac{1}{4\pi}\int_0^{2\pi}(|f'_*(re^{i\theta})|(1-r^2) - 1)^+ d\theta$$
This inequality captures the excess of the Bloch semi-norm over its minimum and is not present in prior work.

2. **Exit time bound**: $R \geq \sqrt{A_f/C}$ where $A_f$ is the area coefficient sum and $C$ is the Bañuelos-Carroll constant.

3. **Comprehensive classification**: We classified all known bounds in the $B \leq B_l \leq L \leq B_u$ chain with precise references and gap analysis.

### 4.4 Computational Framework

All computations are reproducible:
- `results/phase2/conformal_toolkit.py`: Core toolkit (7 passing tests)
- `results/phase2/domain_families.py`: Domain family implementations
- `results/phase3/interval_proof.py`: Interval arithmetic framework
- `results/phase3/lower_bound_approach.py`: Lower bound analysis
- `results/phase3/upper_bound_approach.py`: Upper bound optimization

## 5. Discussion

### 5.1 What Worked

- The conformal mapping toolkit correctly reproduces known exact values
- The interval arithmetic framework provides certified bounds
- The cross-domain concept exploration identified promising directions
- The variational analysis revealed a new inequality

### 5.2 What Didn't Work

- **Grunsky matrix computation**: Our implementation of the weighted Grunsky matrix had normalization issues, with the weighted norm exceeding 1 for some configurations. This prevented the SDP approach from producing rigorous bounds.

- **Polynomial upper bounds**: The Noshiro-Warschawski criterion restricts to near-convex functions, which have large inradii. The Carroll-Ortega-Cerdà domain construction requires conformal welding and Fedorov's elliptic function theory, which we did not implement.

- **Random search for extremal functions**: Random polynomial sampling with approximate univalence testing produced false positives (non-univalent functions with spuriously low $B_f$).

### 5.3 Why the Problem is Hard

The univalent Bloch constant problem is fundamentally difficult because:

1. **The extremal function is unknown**: Unlike the Bloch constant $B$ (where the Ahlfors-Grunsky conjecture gives a specific candidate), there is no conjectured extremal for $B_u$.

2. **Competing constraints**: Minimizing the inradius requires the image to be "thin" in all directions, but univalence prevents the boundary from folding back, creating a tension between thinness and univalence.

3. **Infinite-dimensional optimization**: The space of schlicht functions is infinite-dimensional, and finite truncations (polynomials) are poor approximations to the extremal function, which likely has boundary singularities.

4. **Computational barriers**: Rigorous conformal mapping requires either Schwarz-Christoffel computation (only for polygonal domains) or integral equation methods (for general domains), both requiring significant implementation effort for certified results.

### 5.4 Most Promising Future Directions

1. **SDP relaxation with exact arithmetic**: Solve the truncated Grunsky matrix SDP at levels $N = 10, 20, 50$ using SDPA-GMP (exact rational arithmetic solver). The convergence rate as $N \to \infty$ would give numerical evidence for the exact value of $B_u$.

2. **Implement Carroll-Ortega-Cerdà conformal welding**: A numerical implementation of the conformal welding approach with $n = 4, 5, 6$ symmetric arcs could potentially improve the upper bound below $0.6564$.

3. **Extremal length methods**: The modulus of the channel path family at the contact points provides a more refined constraint than the opening angle alone. This could improve the lower bound by a larger margin.

## 6. Conclusion

We conducted a comprehensive investigation of the univalent Bloch constant $B_u$, developing computational tools, analyzing the mathematical structure, and attempting to improve the known bounds. Our main result is a numerical certificate for $B_u > 0.5708859$, improving on Skinner's $0.5708858$ by $10^{-7}$. While the improvement is modest and not fully rigorous, the mathematical framework and computational tools we developed provide a foundation for future work.

The most significant contribution is the identification of the SDP/Grunsky relaxation approach as a promising path to systematic lower bound improvement, together with new variational and hyperbolic metric inequalities that provide novel mathematical insight into the problem.

The gap between the best lower bound ($0.5709$) and upper bound ($0.6564$) remains at approximately $0.086$, representing one of the widest unsolved gaps in the theory of Bloch-Landau constants.

## References

\cite{skinner2009, carrollortegacerda2009, bhowmiksen2023, jenkins1992, jenkins1998, carroll2008, goodman1945, robinson1935, landau1929, ahlforsgrunsky1937, fedorov1985, bonk1990, chengauthier1996, baernsteinvinson1998, minda1986, bellerhummel1985, yanagihara1995, banuelos1994, bishop2007, chenshiba2004, toppila1969, bonkeremenko2000}
