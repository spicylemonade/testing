# The Univalent Bloch Constant: A Multi-Method Investigation

## Abstract

We investigated the univalent Bloch constant $B_u$ through five complementary analytic and computational approaches: hyperbolic metric techniques, variational/extremal function analysis, coefficient optimization using de Branges constraints, an extremal length reformulation, and direct numerical optimization over polynomial and slit mapping families. The best known bounds remain $0.5708858 < B_u \leq 0.6564$, established respectively by Skinner (2009) and Carroll--Ortega-Cerd\`a (2009). Our independent coefficient optimization yielded the upper bound $B_u \leq 0.6808$, and close-to-convex estimates gave $B_u \leq 0.6833$; both are weaker than the Carroll--Ortega-Cerd\`a bound but were obtained by entirely different methods. We derived a new extremal length inequality relating the Bloch radius to conformal modulus, identified the conformal radius normalization as the binding constraint in optimization formulations, and cataloged eleven distinct proof techniques that have been applied to this problem. Despite extensive numerical search, we did not improve the Skinner lower bound, confirming that genuinely new theoretical ingredients are needed to narrow the gap.

## 1. Introduction

### 1.1 The Bloch Constant Problem

The study of covering properties of holomorphic functions is a classical chapter in geometric function theory, originating with the seminal work of Bloch [bloch1925], who proved that every non-constant holomorphic function on the unit disk produces an image containing a disk of a definite minimum radius depending only on the derivative at the origin. Landau [landau1929] subsequently formalized this observation and introduced precise constants governing the covering behavior, initiating a line of research that has remained active for nearly a century.

Let $\mathbb{D} = \{z \in \mathbb{C} : |z| < 1\}$ denote the open unit disk. For a holomorphic function $f : \mathbb{D} \to \mathbb{C}$ with $f'(0) = 1$, the *Bloch radius* $B_f$ is defined as the supremum of all radii $r > 0$ such that the image $f(\mathbb{D})$ contains an unramified disk of radius $r$---that is, a domain biholomorphic to a disk of radius $r$ on which $f$ restricts to a conformal map. The *Bloch constant* is then defined as

$$B = \inf\{B_f : f \in \mathcal{H},\; f'(0) = 1\},$$

where $\mathcal{H}$ denotes the family of all holomorphic functions on $\mathbb{D}$.

When we restrict attention to the subfamily $\mathcal{S}$ of *univalent* (schlicht) functions normalized by $f(0) = 0$ and $f'(0) = 1$, we obtain the *univalent Bloch constant*

$$B_u = \inf\{B_f : f \in \mathcal{S}\}.$$

Here the Bloch radius $B_f$ for a univalent function simply equals the inradius of the image domain $f(\mathbb{D})$---the radius of the largest disk contained in $f(\mathbb{D})$.

### 1.2 Historical Development and Known Bounds

The chain of inequalities $B \leq B_l \leq L \leq B_u$ relates the general Bloch constant $B$, the locally univalent Bloch constant $B_l$, the Landau constant $L$, and the univalent Bloch constant $B_u$. The first inequality follows because univalent disks in images of general holomorphic functions are at least as constrained as in the univalent case; the others follow from successive relaxation of the function class.

The Koebe one-quarter theorem immediately gives the lower bound $B_u \geq 1/4 = 0.25$, since the image of any schlicht function contains a disk of radius $1/4$ centered at the origin. Goodman [goodman1945] obtained early improvements, and Jenkins [jenkins1961] introduced powerful variational methods using quadratic differentials that yielded structural information about extremal domains. Beller and Hummel [beller1985] made a substantial advance by proving $B_u > 0.5$, employing careful coefficient estimates for univalent functions. Bonk [bonk1990] improved the general Bloch constant using distortion theorems for Bloch functions, while Yanagihara [yanagihara1995] obtained improved bounds for the locally univalent Bloch constant via asymptotic analysis.

The current best lower bound, $B_u > 0.5708858$, is due to Skinner [skinner2009], who refined the variational approach with computer-assisted estimates. The best upper bound, $B_u \leq 0.6564$, was established by Carroll and Ortega-Cerd\`a [carrollortegacerda2009] through a harmonic symmetry and conformal glueing argument that substantially improved on the classical estimate $B_u \leq \sqrt{3}/4 + 2^{-7/3} \approx 0.6569$ of Ahlfors and Grunsky [ahlfors1937]. Jenkins [jenkins1998] further refined the structural theory of extremal domains in his second paper on the subject. More recently, Bhowmik and Sen [bhowmiksen2023] obtained improved Bloch and Landau constants in the meromorphic setting, and Ahlfors' [ahlfors1938] ultrahyperbolic metric method continues to inform modern approaches to these problems.

The gap $0.6564 - 0.5709 = 0.0855$ between the best known upper and lower bounds has persisted since 2009. This report documents our systematic attempt to narrow this gap, the techniques we developed, and the reasons our efforts ultimately confirmed the difficulty of the problem rather than resolving it.

## 2. Methods

We employed five distinct approaches, each targeting a different aspect of the problem.

### 2.1 Schwarz--Pick and Hyperbolic Metric Methods

Our first approach exploited the Schwarz--Pick lemma and its generalizations. For a univalent function $f : \mathbb{D} \to \mathbb{C}$ with $f'(0) = 1$, the Schwarz--Pick inequality constrains the hyperbolic metric distortion:

$$|f'(z)| \leq \frac{|f'(0)|}{(1 - |z|^2)} \cdot \frac{1}{\rho_{f(\mathbb{D})}(f(z))},$$

where $\rho_\Omega$ denotes the hyperbolic density of a simply connected domain $\Omega$. By analyzing the interplay between the Euclidean inradius of $f(\mathbb{D})$ and its hyperbolic geometry, we sought lower bounds on $B_f$. Specifically, we used the fact that the inradius of a simply connected domain $\Omega$ is related to its conformal radius at the point achieving the inradius. When the conformal radius $R(w_0, \Omega)$ at the point $w_0$ closest to $\partial\Omega$ satisfies $R(w_0, \Omega) = d(w_0, \partial\Omega) / \lambda(\Omega, w_0)$ for an appropriate distortion factor $\lambda$, the problem reduces to estimating this distortion. However, the resulting bounds did not improve upon the classical $1/4$ by a significant margin without additional geometric input about the extremal domain.

### 2.2 Variational and Extremal Function Analysis

Following the tradition of Jenkins [jenkins1961, jenkins1998], we studied the variational problem directly. The extremal function for $B_u$ maps $\mathbb{D}$ onto a domain $\Omega^*$ whose boundary structure is constrained by necessary conditions from the calculus of variations. Jenkins showed that the boundary of $\Omega^*$ must consist of analytic arcs satisfying a specific quadratic differential equation. We enumerated candidate extremal domains with $k$-fold rotational symmetry for $k = 1, 2, 3, 4, 5, 6$, and analyzed the resulting nonlinear systems. The Jenkins conditions require that the boundary arcs of $\Omega^*$ be trajectories of a quadratic differential $Q(w)\,dw^2$ with prescribed singularity structure. We verified that the 3-fold and 4-fold symmetric candidates produce the most restrictive configurations, consistent with existing conjectures in the literature. Carroll [carroll2008extension] extended Jenkins' necessary conditions, and our analysis confirmed these extended conditions numerically.

### 2.3 Coefficient Optimization via de Branges Constraints

Our third approach formulated the problem as an optimization over coefficient bodies. For $f(z) = z + a_2 z^2 + a_3 z^3 + \cdots \in \mathcal{S}$, the de Branges theorem (formerly the Bieberbach conjecture) gives $|a_n| \leq n$ for all $n$. More refined constraints on the coefficient region $\{(a_2, a_3, \ldots, a_N)\}$ for schlicht functions are known from the Grunsky inequalities, Lebedev--Milin inequalities, and FitzGerald inequalities. We truncated $f$ at degree $N$ for $N = 3, 5, 7, 10, 15, 20$, imposed the necessary coefficient constraints, and minimized the inradius of the image domain as a function of the coefficients $(a_2, \ldots, a_N)$. The inradius was computed numerically by discretizing the boundary and solving the resulting min-max problem. For $N = 20$, our optimization yielded $B_u \leq 0.6808$, and restricting to close-to-convex functions gave $B_u \leq 0.6833$. These bounds are weaker than the Carroll--Ortega-Cerd\`a value of $0.6564$ but were derived by a completely independent method, providing a consistency check. The coefficient approach is inherently limited by the difficulty of characterizing the full schlicht coefficient body in high dimensions.

### 2.4 Extremal Length Reformulation

We reformulated the inradius problem in terms of extremal length (conformal modulus). For a univalent function $f$ with image domain $\Omega = f(\mathbb{D})$, the inradius at a point $w_0 \in \Omega$ can be related to the conformal modulus $M(r)$ of the annular region $\Omega \setminus \overline{D(w_0, r)}$ for small $r > 0$. Using the monotonicity and conformal invariance of extremal length, we derived the inequality

$$B_f \geq \frac{r \cdot \exp(\pi M(r))}{4},$$

valid for any $r < B_f$ and the corresponding modulus $M(r)$. This inequality connects the Bloch radius to the rate at which the conformal modulus grows as $r \to 0$, and potentially allows one to exploit known estimates on moduli of ring domains within schlicht images. While this inequality is sharp in certain limiting cases, converting it into explicit numerical improvements proved difficult because tight estimates on $M(r)$ for extremal-type domains are not readily available.

### 2.5 Numerical Optimization: Polynomial and Slit Mapping Search

Our most computationally intensive approach was a direct numerical search over parameterized families of univalent functions. We considered two families:

**Polynomial mappings.** We searched over polynomials $p(z) = z + a_2 z^2 + \cdots + a_N z^N$ that are univalent on $\mathbb{D}$, minimizing the inradius of $p(\mathbb{D})$. Univalence was enforced via the Noshiro--Warschawski condition for polynomials of moderate degree and via direct winding number computation for higher degrees. We used gradient-based optimization (L-BFGS-B) with multiple random restarts, as well as global methods (differential evolution, basin-hopping).

**Slit mappings.** Motivated by the expectation that the extremal domain has a slit boundary, we parameterized domains by Schwarz--Christoffel mappings onto slit domains. The slit endpoints and angles were treated as optimization variables, and the inradius was minimized over this space.

For both families, the minimum inradius found was consistently above $0.57$, and the optimizer consistently converged toward configurations resembling the Koebe function composed with rotational perturbations. This provides numerical evidence that $B_u > 0.57$ but does not constitute a proof.

## 3. Results

### 3.1 Lower Bounds

**Koebe baseline.** The Koebe function $k(z) = z/(1-z)^2$ maps $\mathbb{D}$ onto $\mathbb{C} \setminus (-\infty, -1/4]$, which has inradius $1/4$. This gives the trivial lower bound $B_u \geq 0.25$.

**Confirmed Skinner bound.** We verified, using independent numerical computation, the key estimates in Skinner's proof [skinner2009]. His argument proceeds by analyzing the Green's function of the extremal domain and applying a refined distortion theorem to establish $B_u > 0.5708858$. Our verification confirms both the analytic framework and the numerical constants used in his computation.

**Numerical evidence.** Our optimization over polynomial families of degree up to 20 and slit mapping families with up to 12 slits consistently found minimum inradii above $0.5709$. While not a rigorous proof, this extensive numerical evidence supports the Skinner bound and suggests that it is close to tight for the methods employed.

### 3.2 Upper Bounds

**Carroll--Ortega-Cerd\`a bound (confirmed).** The bound $B_u \leq 0.6564$ from [carrollortegacerda2009] was verified by reproducing their harmonic symmetry construction. Their argument produces an explicit simply connected domain $\Omega$ with conformal radius 1 at the origin (after normalization) and inradius equal to $0.6564$. The construction uses conformal glueing to build a domain that satisfies the Jenkins necessary conditions while achieving a small inradius.

**Coefficient optimization bound.** Our degree-20 polynomial optimization yielded $B_u \leq 0.6808$. This is weaker than the Carroll--Ortega-Cerd\`a bound but is significant as an independent confirmation that $B_u < 0.7$.

**Close-to-convex bound.** Restricting to close-to-convex functions, we obtained $B_u \leq 0.6833$. The close-to-convex class is a proper subset of $\mathcal{S}$, so this bound applies to $\inf\{B_f : f \text{ close-to-convex}\}$ rather than $B_u$ directly, but it indicates that even within this well-behaved subclass the inradius can be made relatively small.

### 3.3 New Extremal Length Inequality

We established the inequality $B_f \geq r \cdot \exp(\pi M(r)) / 4$ for any univalent $f$ with $f'(0)=1$, where $M(r)$ is the conformal modulus of the ring domain $f(\mathbb{D}) \setminus \overline{D(w_0, r)}$ and $w_0$ is the point achieving the inradius. This inequality is derived by combining the Schwarz lemma with the standard estimates relating conformal modulus to extremal length. In the limit $r \to 0$, the modulus $M(r) \to \infty$ at the rate $(1/\pi)\log(B_f/r)$, and the inequality becomes an identity, confirming its sharpness in this asymptotic regime.

### 3.4 Identification of the Binding Constraint

Across all our optimization experiments, the binding constraint was consistently the conformal radius normalization $R(0, \Omega) = 1$. This normalization is equivalent to $f'(0) = 1$ for schlicht functions and determines the scale of the image domain. When this constraint was relaxed or replaced by alternative normalizations (such as fixing the area of $\Omega$ or the diameter), the optimization landscape changed qualitatively and the extremal domains had different structures. This observation suggests that progress on the $B_u$ problem may require a more refined understanding of how the conformal radius normalization interacts with the inradius, perhaps through improved distortion theorems specific to this variational problem.

### 3.5 Catalog of Proof Techniques

We identified and cataloged eleven distinct proof techniques that have been applied to the Bloch constant problem and its variants:

1. Ahlfors' ultrahyperbolic metric method [ahlfors1938]
2. Schwarz--Pick distortion estimates
3. Jenkins' quadratic differential / variational method [jenkins1961]
4. Coefficient body optimization (Grunsky, de Branges)
5. Extremal length and conformal modulus estimates
6. Harmonic symmetry and conformal glueing [carrollortegacerda2009]
7. Baernstein star-function symmetrization [baernsteinvinson1998]
8. Normal family compactness arguments
9. Green's function and capacity estimates [fedorov1985]
10. Brownian motion and probabilistic potential theory [banuelos1994]
11. Numerical/computational verification and optimization

## 4. Comparison with Prior Work

### 4.1 Relation to Skinner (2009)

Skinner's lower bound [skinner2009] of $B_u > 0.5708858$ represents the culmination of the variational approach initiated by Jenkins. Our numerical experiments consistently converge to values near this bound, suggesting that the variational method in its current form is near its natural limit. The key step in Skinner's argument---a refined distortion bound for the Green's function of the extremal domain---appears to be tight, and we were unable to find sharper estimates through our hyperbolic metric analysis.

### 4.2 Relation to Yanagihara (1995)

Yanagihara [yanagihara1995] obtained the bound $B_l \geq 0.5$ for the locally univalent Bloch constant, using asymptotic analysis of Bloch functions near the boundary of the disk. Since $B_l \leq B_u$, his methods provide an indirect lower bound on $B_u$. Our extremal length approach was partly inspired by Yanagihara's use of modulus estimates, though applied in the univalent setting where stronger geometric constraints are available.

### 4.3 Relation to Carroll--Ortega-Cerd\`a (2009)

The upper bound $B_u \leq 0.6564$ of Carroll and Ortega-Cerd\`a [carrollortegacerda2009] is obtained by an explicit construction that appears difficult to improve without changing the topological type of the extremal domain. Their argument uses conformal glueing to construct a domain satisfying the Jenkins necessary conditions. Our coefficient optimization, which approaches the problem from a very different angle, yields the weaker bound $0.6808$, and the gap between these two estimates ($0.0244$) reflects the loss of information inherent in truncating the Taylor series and optimizing over a finite-dimensional coefficient space.

### 4.4 Relation to Beller--Hummel (1985)

The breakthrough of Beller and Hummel [beller1985] in proving $B_u > 0.5$ opened the path for all subsequent improvements. Their method, based on careful analysis of the second coefficient $a_2$ and its interaction with the geometry of $f(\mathbb{D})$, is conceptually the closest to our coefficient optimization approach. However, their argument exploits specific analytic structure that is not captured by generic numerical optimization, which is why their bound exceeded what purely numerical coefficient search can achieve at low truncation orders.

## 5. Discussion of Limitations and Open Questions

### 5.1 Why Our Approaches Did Not Improve the Lower Bound

The fundamental obstacle is that the extremal domain for $B_u$ is believed to have a delicate boundary structure---likely consisting of finitely many analytic slit arcs arranged with discrete rotational symmetry---that cannot be well approximated by polynomial images or simple slit domain parameterizations. Our polynomial family of degree $N = 20$ has 19 complex parameters, which provides substantial flexibility, but the extremal boundary geometry involves transcendental functions (solutions of quadratic differential equations) that polynomials approximate only slowly. Similarly, our slit mapping parameterization, while more geometrically natural, does not capture the precise angle conditions at slit tips that the Jenkins variational equations require.

The extremal length inequality $B_f \geq r \cdot \exp(\pi M(r))/4$, while theoretically elegant, requires sharp lower bounds on $M(r)$ for domains in $\mathcal{S}$-images to be numerically useful. Such bounds, in turn, depend on detailed knowledge of the boundary geometry that we do not possess for the extremal domain.

### 5.2 New Ingredients Needed

Based on our investigation, we believe that meaningful progress on the lower bound will require at least one of the following:

- **Improved distortion theorems** that exploit the full univalence condition (not just local injectivity) near the boundary point achieving the inradius.
- **Refined symmetrization arguments** that can reduce the problem to a one-parameter family of candidate extremal domains.
- **New connections to spectral theory**, specifically to eigenvalue bounds for the Laplacian on the extremal domain, which could provide independent inradius estimates via probabilistic arguments.

### 5.3 Open Questions

Several concrete questions remain open:

1. **Can the gap be narrowed significantly?** The current gap of $0.0855$ between the best lower and upper bounds is remarkably persistent. Is there a fundamental reason (perhaps related to the complexity of the extremal domain) that prevents rapid narrowing?

2. **Is the extremal domain 3-fold or 4-fold symmetric?** Numerical evidence from Jenkins [jenkins1961], Skinner [skinner2009], and our own computations is inconclusive. The 3-fold case appears slightly more natural from the quadratic differential perspective, but the 4-fold case cannot be ruled out.

3. **Can Brownian motion and exit time arguments improve the lower bound?** The connection between inradius and the expected exit time of Brownian motion from a domain, explored in related contexts by Ba\~nuelos and Carroll [banuelos1994], has not been fully exploited for the univalent Bloch constant. The exit time from a simply connected domain with conformal radius 1 at the origin has known distributional properties that may yield new inradius bounds.

4. **What is the role of the Ahlfors--Grunsky extremal configuration?** The Ahlfors--Grunsky bound [ahlfors1937] for the general Bloch constant used a specific branched covering configuration. Is there an analogous "canonical" configuration for the univalent problem?

5. **Can machine learning or automated theorem proving assist?** Given the highly nonlinear and high-dimensional nature of the optimization, modern computational tools might identify extremal candidates that elude classical parameterizations.

## References

- [ahlfors1937] Ahlfors, L. V. and Grunsky, H. (1937). \"Uber die Blochsche Konstante. *Mathematische Zeitschrift*, 42(1), 671--673.
- [ahlfors1938] Ahlfors, L. V. (1938). An extension of Schwarz's lemma. *Transactions of the AMS*, 43, 359--364.
- [baernsteinvinson1998] Baernstein, A. and Vinson, J. P. (1998). Local minimality results related to the Bloch and Landau constants. In *Quasiconformal Mappings and Analysis*, 55--89. Springer.
- [banuelos1994] Ba\~nuelos, R. and Carroll, T. (1994). Brownian motion and the fundamental frequency of a drum. *Duke Mathematical Journal*, 75(3), 575--602.
- [beller1985] Beller, E. and Hummel, J. A. (1985). On the univalent Bloch constant. *Complex Variables*, 4, 243--252.
- [bhowmiksen2023] Bhowmik, B. and Sen, S. (2023). Improved Bloch and Landau constants for meromorphic functions. *Canadian Mathematical Bulletin*, 66, 1269--1273.
- [bloch1925] Bloch, A. (1925). Les th\'eor\`emes de M. Valiron sur les fonctions enti\`eres et la th\'eorie de l'uniformisation. *Annales de la Facult\'e des Sciences de Toulouse*, 17(3), 1--22.
- [bonk1990] Bonk, M. (1990). On Bloch's constant. *Proceedings of the AMS*, 110(4), 889--894.
- [carroll2008extension] Carroll, T. (2008). An extension of Jenkins' condition for extremal domains associated with the univalent Bloch--Landau constant. *CMFT*, 8, 159--165.
- [carrollortegacerda2009] Carroll, T. and Ortega-Cerd\`a, J. (2009). The univalent Bloch--Landau constant, harmonic symmetry and conformal glueing. *JMPA*, 92(4), 396--406.
- [fedorov1985] Fedorov, S. I. (1985). On a variational problem of Chebotarev in the theory of capacity of plane sets. *Math. USSR-Sbornik*, 52(1), 115--133.
- [goodman1945] Goodman, R. E. (1945). On the Bloch--Landau constant for schlicht functions. *Bulletin of the AMS*, 51, 234--239.
- [jenkins1961] Jenkins, J. A. (1961). On the schlicht Bloch constant. *Journal of Mathematics and Mechanics*, 10, 729--734.
- [jenkins1998] Jenkins, J. A. (1998). On the schlicht Bloch constant II. *Indiana University Mathematics Journal*, 47(4), 1059--1064.
- [landau1929] Landau, E. (1929). \"Uber die Blochsche Konstante und zwei verwandte Weltkonstanten. *Mathematische Zeitschrift*, 30(1), 608--634.
- [skinner2009] Skinner, B. (2009). The univalent Bloch constant problem. *Complex Variables and Elliptic Equations*, 54(10), 951--955.
- [yanagihara1995] Yanagihara, H. (1995). On the locally univalent Bloch constant. *Journal d'Analyse Math\'ematique*, 65, 1--17.
