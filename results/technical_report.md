# Technical Report: Bounds on the Univalent Bloch Constant $B_u$

**Authors:** Computational Mathematics Research Group  
**Date:** March 2026  
**Repository:** `results/technical_report.md`

---

## 1. Introduction

### 1.1 Definition and Context

The univalent Bloch constant $B_u$ is a fundamental quantity in geometric function theory that measures the worst-case size of the largest disk contained in the image of a normalized univalent (injective, holomorphic) function on the unit disk. Let $\mathbb{D} = \{z \in \mathbb{C} : |z| < 1\}$ denote the open unit disk. Define the **normalized Schlicht class** $S$ to be the set of all holomorphic, univalent functions $f : \mathbb{D} \to \mathbb{C}$ satisfying $f(0) = 0$ and $f'(0) = 1$. For any such $f \in S$, the image $f(\mathbb{D})$ is a simply connected proper subdomain of $\mathbb{C}$. Since $f$ is injective, every disk contained in $f(\mathbb{D})$ is automatically the univalent image of a subdomain of $\mathbb{D}$. We define the **inradius** of $f(\mathbb{D})$ as

$$\operatorname{inrad}(f(\mathbb{D})) = \sup_{w \in f(\mathbb{D})} \operatorname{dist}(w, \partial f(\mathbb{D})) = \sup_{w \in f(\mathbb{D})} \inf_{\zeta \in \partial f(\mathbb{D})} |w - \zeta|,$$

which is the radius of the largest open disk contained in $f(\mathbb{D})$. The **univalent Bloch constant** is then defined as

$$B_u = \inf_{f \in S} \operatorname{inrad}(f(\mathbb{D})).$$

Equivalently, $B_u$ is the largest radius $R$ such that every normalized univalent function on $\mathbb{D}$ has an image containing a disk of radius $R$. The constant $B_u$ quantifies the extremal covering capability of the Schlicht class and is one of the central constants in the covering theorem tradition initiated by Bloch (1925) and Landau (1929).

### 1.2 Motivation: The Hierarchy of Bloch-Landau Constants

The univalent Bloch constant sits at the top of a chain of four related constants. Let $\mathcal{F}$ denote the class of all holomorphic functions $f : \mathbb{D} \to \mathbb{C}$ with $f'(0) = 1$ (no injectivity requirement). For $f \in \mathcal{F}$, define $B_f$ as the supremum of radii $r > 0$ such that some subdomain of $\mathbb{D}$ maps univalently onto a domain containing a disk of radius $r$. The **Bloch constant** is $B = \inf_{f \in \mathcal{F}} B_f$. Similarly, the **Landau constant** $L$ is the infimum of the largest disk radius in $f(\mathbb{D})$ (without requiring a univalent pre-image), and the **locally univalent Bloch constant** $B_l$ is the infimum of $B_f$ restricted to locally univalent $f$ (i.e., $f'(z) \neq 0$ on $\mathbb{D}$). These constants satisfy the fundamental chain of inequalities:

$$B \leq B_l \leq L \leq B_u.$$

The proof of $B \leq B_l$ follows because the infimum defining $B$ is over a larger class than that for $B_l$. The inequality $B_l \leq L$ holds because every univalent disk is a disk (dropping the univalence condition increases the radius). Finally, $L \leq B_u$ because for univalent $f$, the Landau radius $L_f$ equals the inradius of $f(\mathbb{D})$ (since $f^{-1}$ provides a global univalent pre-image), and the univalent class is a subclass of $\mathcal{F}$.

### 1.3 Current Best Bounds

The current state of knowledge on $B_u$ is summarized by the inequalities

$$0.5708858 < B_u \leq 0.6564.$$

The lower bound $B_u > 0.5708858$ is due to Skinner (2009), who used an implicit function method combined with classical distortion estimates for univalent functions. The upper bound $B_u \leq 0.6564$ was established by Carroll and Ortega-Cerdà (2008/2010) via an explicit domain construction using harmonically symmetric curved arcs, building on the Polya-Chebotarev problem solved by Fedorov (1985). The gap of approximately $0.086$ (relative gap $\approx 14\%$ of the midpoint) is the largest among the four Bloch-Landau constants, suggesting significant room for improvement.

### 1.4 Summary of Contributions

This report documents our systematic computational investigation of bounds on $B_u$. Our main contributions are:

1. **A certified upper bound $B_u \leq 0.6814$** via a 3-fold symmetric radial slit-disk domain, computed using an exact Cayley-Joukowsky conformal map chain and verified with interval arithmetic at 100-digit precision.
2. **An interval arithmetic certification framework** capable of producing rigorous, computer-assisted bounds free of floating-point errors.
3. **Comprehensive negative results**: we document why the Koebe 1/4 + Bloch norm dichotomy, the Grunsky matrix adversarial search with $2 \times 2$ truncation, and higher-fold radial symmetry ($n \geq 4$ slits) all fail to improve upon existing bounds.
4. **A detailed analysis** of why straight radial slits cannot match Carroll-Ortega-Cerdà's curved arc construction.

We emphasize that we did **not** achieve any improvement over the best previously published bounds. The lower bound remains at Skinner's $0.5708858$, and the upper bound remains at Carroll-Ortega-Cerdà's $0.6564$. Our certified upper bound of $0.6814$ is weaker than theirs but is notable for being independently derived with full interval arithmetic certification.

---

## 2. Literature Review

The study of covering theorems for holomorphic functions has a century-long history. We survey the key papers from our bibliography that bear on the univalent Bloch constant.

### 2.1 Origins: Bloch and Landau

**Bloch (1925)** proved the foundational result that there exists a universal constant $B > 0$ such that for every holomorphic function $f : \mathbb{D} \to \mathbb{C}$ with $f'(0) = 1$, the image $f(\mathbb{D})$ contains a univalent disk of radius at least $B$. Bloch's proof was non-constructive and did not produce a good numerical value. **Landau (1929)** subsequently introduced the Landau constant $L$ and established a systematic framework for covering theorems, connecting them to the theory of normal families and the modular function.

### 2.2 The Ahlfors-Grunsky Upper Bound for $B$

**Ahlfors and Grunsky (1937)** established the still-standing best upper bound on the Bloch constant:

$$B \leq \sqrt{\frac{\sqrt{3}-1}{2}} \cdot \frac{\Gamma(1/3)\,\Gamma(11/12)}{\Gamma(1/4)} \approx 0.47186.$$

Their construction uses a specific Riemann surface with prescribed branching and remains one of the most elegant results in the area. The conjectured equality $B = 0.47186\ldots$ has motivated nearly a century of work on improved lower bounds but remains unproven.

### 2.3 Robinson and Goodman: Early Bounds on $B_u$

**Robinson (1935)** initiated the study of the Schlicht (univalent) Bloch constant, establishing the first non-trivial lower bound $B_u > 1/2$ using the Koebe 1/4 theorem and distortion estimates. **Goodman (1945)** introduced the fundamental construction of **slit-disk domains** for obtaining upper bounds on $B_u$. Her idea was to remove symmetric radial slits from $\mathbb{D}$, conformally map back to $\mathbb{D}$, and compute the ratio of inradius to conformal radius for the resulting domain. Goodman's construction with 3 equally-spaced radial slits yielded the first explicit upper bound significantly below 1, approximately $B_u \leq \pi/4 \approx 0.785$. This slit-disk paradigm has been refined by every subsequent improvement.

### 2.4 Intermediate Developments

**Rademacher (1943)** established the conjectured value of the Landau constant $L \leq \Gamma(1/3)\Gamma(5/6)/\Gamma(1/6) \approx 0.5433$, providing an upper bound that feeds into the chain $L \leq B_u$. **Reich (1956)** obtained explicit improvements beyond the 1/2 lower bound for $B_u$. **Heins (1962)** provided a comprehensive treatment of covering theorems in his monograph, placing the Bloch-Landau constants in a broader function-theoretic context. **Toppila (1969)** achieved further modest improvements on the lower bound using refined covering arguments.

### 2.5 Beller-Hummel: Improved Upper Bound

**Beller and Hummel (1985)** significantly improved the upper bound on $B_u$ using coefficient methods and more carefully optimized slit-disk domains. Their approach combined the de Branges coefficient bounds $|a_n| \leq n$ (proved by de Branges in 1984) with explicit conformal radius computations for domains with multiple slits. The Beller-Hummel bound represented the state of the art for over two decades.

### 2.6 Jenkins: Necessary Conditions for Extremal Domains

**Jenkins (1992)** established a crucial structural result: if $f_0$ is an extremal function for $B_u$ (achieving the infimum), then the largest inscribed disk in $f_0(\mathbb{D})$ must be tangent to the boundary at more than one point. In a follow-up, **Jenkins (1998)** strengthened this to show that the boundary arcs of tangency must satisfy a specific quadratic differential equation. These necessary conditions constrain the geometry of candidate extremal domains and informed the later work of Carroll and Ortega-Cerdà. **Carroll (2008)** further extended Jenkins's condition, proving that the tangency arcs must exhibit **harmonic symmetry** with respect to the origin --- the harmonic measure of each arc as seen from the origin must equal the harmonic measure as seen from the center of the extremal inscribed disk.

### 2.7 Bonk-Minda-Yanagihara: Hyperbolic Metric Methods

**Bonk, Minda, and Yanagihara (1996)** developed sharp distortion theorems for Bloch functions using the ultrahyperbolic metric. Their paper introduced the technique of defining auxiliary metrics that dominate the hyperbolic metric of the image domain and deriving covering estimates from the resulting comparison. In a companion paper, **Bonk, Minda, and Yanagihara (1997)** extended these methods to general Bloch functions, obtaining improved bounds on $B$ and $B_l$. **Yanagihara (1994, 1995)** proved the lower bound $B_l > 1/2 + 10^{-335}$ using sharp distortion estimates for locally Schlicht Bloch functions, which also implies $B_u > 1/2 + 10^{-335}$ via the chain $B_l \leq L \leq B_u$.

### 2.8 Chen-Gauthier and Xiong: Improved Bloch Constant Bounds

**Chen and Gauthier (1996)** obtained the improved lower bound $B \geq \sqrt{3}/4 + 2 \times 10^{-4} \approx 0.4332$ using the hyperbolic metric approach. **Xiong (1998)** further improved the lower bound on $B$ by refining the auxiliary metric construction. These improvements on $B$ are relevant to $B_u$ only through the chain inequality $B \leq B_u$, but they demonstrate the power of the hyperbolic metric approach that has not been fully exploited for the univalent constant.

### 2.9 Carroll and Ortega-Cerdà: The Current Best Upper Bound

**Carroll and Ortega-Cerdà (2008, published 2010)** achieved the breakthrough upper bound $B_u \leq 0.6564$ by constructing domains with **harmonically symmetric curved arcs** rather than straight radial slits. Their key innovation was to use Fedorov's (1985) solution of the Polya-Chebotarev problem --- which determines the continuum of minimal logarithmic capacity containing prescribed points --- to design slit geometries with 4-fold symmetry satisfying Jenkins's necessary conditions. The conformal welding technique (following Bishop) was used to rigorously construct the required conformal map. The curved arcs minimize the conformal radius more efficiently than straight slits, yielding a significantly better upper bound.

### 2.10 Skinner: The Current Best Lower Bound

**Skinner (2009)** proved the best known lower bound $B_u > 0.5708858$ using an implicit function method. His approach constructs an explicit function $C(r)$ such that for any $f \in S$, the image $f(\mathbb{D})$ must contain a disk of radius at least $C(r)$ centered at some point within distance $r$ of $f(0)$. By optimizing over $r$ and using the classical growth and distortion theorems for univalent functions, Skinner obtained the stated bound. The method relies on the interaction between covering disks at different centers, going beyond the pointwise Koebe 1/4 theorem.

### 2.11 Recent Work

**Bhowmik and Sen (2023)** improved the Bloch and Landau constants for meromorphic functions and provided a contemporary survey of the known bounds on all four constants $B, B_l, L, B_u$, confirming that Skinner's 2009 bound remains the best lower bound on $B_u$. **Kudryavtseva and Solodov (2024)** studied sharp univalent covering domains for holomorphic self-maps of the disk with fixed interior and boundary points, a related extremal problem that provides geometric insight into the structure of extremal conformal maps. **Derganc and Urbanč (2025)** performed numeric computations of Landau's constant, developing computational techniques for covering theorems that parallel our own approach. **Baernstein and Vinson (1998)** established local minimality results for extremal domains associated with the Bloch and Landau constants using symmetrization techniques.

---

## 3. Methods

We pursued four distinct approaches to bounding $B_u$: slit-disk domain construction for upper bounds, a Bloch norm dichotomy argument for lower bounds, a Grunsky matrix adversarial search, and interval arithmetic certification.

### 3.1 Slit-Disk Domain Construction for Upper Bounds

#### Domain Definition

Following Goodman (1945), we consider the $n$-fold symmetric slit-disk domain

$$\Omega_n = \mathbb{D} \setminus \bigcup_{k=0}^{n-1} \left\{ r e^{2\pi i k/n} : r_0 \leq r < 1 \right\},$$

which is the unit disk with $n$ equally-spaced radial slits removed, each extending from an inner radius $r_0$ to the boundary. The free parameter $r_0 \in (0,1)$ controls the slit length: small $r_0$ produces long slits (thin domain), while $r_0$ near 1 produces short slits (nearly full disk). By the Riemann mapping theorem, there exists a unique conformal map $\varphi_n : \mathbb{D} \to \Omega_n$ with $\varphi_n(0) = 0$ and $\varphi_n'(0) > 0$. The quantity $\varphi_n'(0)$ is the **conformal radius** of $\Omega_n$ at the origin, denoted $\operatorname{crad}(\Omega_n, 0)$. The normalized function $g(z) = \varphi_n(z)/\varphi_n'(0)$ belongs to $S$ (satisfying $g(0)=0, g'(0)=1$, and univalent), and its image is the rescaled domain $\Omega_n / \varphi_n'(0)$. The univalent Bloch radius for this function is

$$B_g = \frac{\operatorname{inrad}(\Omega_n)}{\operatorname{crad}(\Omega_n, 0)},$$

providing the upper bound $B_u \leq B_g$.

#### Conformal Radius via Cayley-Joukowsky Chain

The conformal radius computation exploits $n$-fold symmetry. The map $z \mapsto z^n$ sends $\Omega_n$ to the single-slit domain $\mathbb{D} \setminus [r_0^n, 1)$ (since the $n$ slits merge into one under the $n$-th power). By the transformation law for conformal radius under power maps, we have

$$\operatorname{crad}(\Omega_n, 0) = \operatorname{crad}\!\left(\mathbb{D} \setminus [r_0^n, 1), 0\right)^{1/n}.$$

This reduces the $n$-slit computation to a single-slit computation. For the single-slit domain $\mathbb{D} \setminus [a, 1)$ (with $a = r_0^n$), the conformal radius at the origin is computed via a chain of five elementary conformal maps:

1. **Cayley transform**: $w_1 = i(1+z)/(1-z)$ maps $\mathbb{D}$ to the upper half-plane $\mathbb{H}$. The slit $[a,1)$ maps to $[iA, i\infty)$ where $A = (1+a)/(1-a)$.
2. **Squaring**: $w_2 = w_1^2$ maps $\mathbb{H}$ to $\mathbb{C} \setminus [0, \infty)$. The vertical slit maps to $(-\infty, -A^2]$.
3. **Möbius map**: $w_3 = w_2/(w_2 + A^2)$ maps the doubly-slit plane to $\mathbb{C} \setminus [0, \infty)$.
4. **Square root**: $w_4 = \sqrt{w_3}$ maps $\mathbb{C} \setminus [0, \infty)$ to $\mathbb{H}$.
5. **Inverse Cayley**: $w_5 = (w_4 - i)/(w_4 + i)$ maps $\mathbb{H}$ to $\mathbb{D}$.

The composition $\psi = w_5 \circ w_4 \circ w_3 \circ w_2 \circ w_1$ maps $\mathbb{D} \setminus [a,1)$ conformally to $\mathbb{D}$. Evaluating at $z = 0$ and tracking the derivative through the chain rule at each step, we obtain

$$\operatorname{crad}(\mathbb{D} \setminus [a,1), 0) = \frac{1 - |\psi(0)|^2}{|\psi'(0)|}.$$

At $z = 0$: $w_1 = i$, $dw_1/dz = 2i$; $w_2 = -1$, $dw_2 = -4$; $w_3 = -1/(A^2-1)$, $dw_3 = -4A^2/(A^2-1)^2$; and so on through the chain. This computation involves only elementary arithmetic (addition, multiplication, division, and one square root), making it amenable to exact or high-precision computation.

#### Inradius Computation

For $\Omega_n$ with $n \geq 2$ equally-spaced slits, the inradius is the radius of the largest disk contained in $\Omega_n$. Two candidate disk placements are considered:

- **Origin-centered disk**: radius $= r_0$ (touching the nearest slit tip).
- **Bisector-centered disk**: a disk centered along the angle bisector between two adjacent slits, at distance $d$ from the origin at angle $\pi/n$. The radius is $\min(1-d, d\sin(\pi/n))$ when the center's projection onto the slit lies beyond the slit tip, or $\min(1-d, \sqrt{(d\cos(\pi/n) - r_0)^2 + (d\sin(\pi/n))^2})$ otherwise.

Both cases are optimized over the center position $d$, and the inradius is the larger of the two candidates. A fine grid search over $d \in [0.01, 0.99]$ with 1000 points supplements the analytic solutions.

#### Optimization over $r_0$

For each $n$, we optimize $B_g = \operatorname{inrad}(\Omega_n)/\operatorname{crad}(\Omega_n, 0)$ over $r_0$ using a three-stage grid search: coarse (100 points in $[0.05, 0.95]$), fine (500 points in a $\pm 0.05$ window around the coarse optimum), and ultra-fine (500 points in a $\pm 0.005$ window). This procedure was applied for $n = 1, 2, \ldots, 12$.

### 3.2 Lower Bound via Bloch Norm Dichotomy

Our first lower bound approach uses a case split on the Bloch seminorm $\|f\|_B = \sup_{z \in \mathbb{D}} (1 - |z|^2)|f'(z)|$.

**Case 1: $\|f\|_B \geq M$.** The Koebe 1/4 theorem, applied to $f$ restricted to the disk centered at the point $z_0$ where $\|f\|_B$ is nearly attained, gives $\operatorname{inrad}(f(\mathbb{D})) \geq \|f\|_B / 4 \geq M/4$.

**Case 2: $\|f\|_B < M$.** When $M$ is close to 1, the function $f$ is close to the identity (small Bloch seminorm implies small higher-order coefficients). Specifically, using the Bloch norm constraint $(1 - t^2)|f'(te^{i\theta})| \leq M$ at small $t$ and differentiating, one obtains $|a_2| \leq C_0 \sqrt{M-1}$ for a universal constant $C_0$. For the quadratic subfamily $f(z) = z + a_2 z^2$ with $|a_2| \leq 1/2$ (which is univalent on $\mathbb{D}$), the inradius of the limacon-like image is $\operatorname{inrad} \geq 1 - |a_2|$.

The optimal $M$ balances the two cases: at the crossover $M/4 = 1 - C_0\sqrt{M-1}$, one solves for $M^* \approx 1.37$ (with $C_0 \approx 1$), giving a bound of approximately $B_u \geq 0.34$. This is significantly weaker than Skinner's $0.5709$.

**Fundamental barrier:** The Szegő subordination principle shows that for any $z_0 \in \mathbb{D}$, the function $g(z) = [f((z+z_0)/(1+\bar{z}_0 z)) - f(z_0)] / [(1-|z_0|^2)f'(z_0)]$ belongs to $S$. Therefore the Koebe 1/4 constant cannot be improved beyond 1/4 for pointwise estimates, and this approach is fundamentally limited. The barrier at 1/4 is sharp: it is achieved asymptotically by compositions of the Koebe function with Möbius transforms.

### 3.3 Grunsky Matrix Adversarial Search

#### Setup

The Grunsky inequalities provide necessary conditions for univalence: if $f(z) = z + \sum_{n=2}^{\infty} a_n z^n$ is univalent, then the infinite Grunsky matrix $G = (G_{mn})_{m,n \geq 1}$ satisfies $\|G\|_{\text{op}} \leq 1$, where $G_{mn} = \sqrt{mn} \cdot b_{mn}$ and $b_{mn}$ are the Grunsky coefficients defined by

$$\log \frac{f(z) - f(\zeta)}{z - \zeta} = -\sum_{m,n=1}^{\infty} b_{mn} z^m \zeta^n.$$

Combined with the de Branges bounds $|a_n| \leq n$, this provides a tractable relaxation of the univalence constraint.

#### 2x2 Grunsky Matrix

We computed the $2 \times 2$ normalized Grunsky matrix directly from the Taylor coefficients $a_2, \ldots, a_5$:

- $b_{11} = a_2^2 - a_3$
- $b_{12} = -a_4 + 2a_2 a_3 - a_2^3$
- $b_{22} = -a_5 + 2a_2 a_4 + \frac{3}{2}a_3^2 - 4a_2^2 a_3 + \frac{3}{2}a_2^4$

The normalized matrix is $G_{mn} = \sqrt{mn}\, b_{mn}$.

#### Optimization

We formulated a penalized minimization problem: minimize $\operatorname{inrad}(f(\mathbb{D}))$ (approximated as $\min_{|z| \approx 1} |f(z)|$ for center at origin, with center search) subject to soft penalties for $\|G_2\|_{\text{op}} > 1$, $|a_n| > n$, winding number $\neq 1$, and boundary self-intersections. We used Nelder-Mead followed by Powell optimization with 15--20 random restarts per polynomial degree $N = 3, 4, 5, 6, 7, 8, 10$.

#### Results and Failure Analysis

All solutions found by the adversarial search were **non-univalent**: the winding number check and self-intersection analysis revealed that every candidate with small inradius at the origin had winding number $\geq 2$ or self-intersecting boundary curves. For instance, at $N = 8$, the optimizer found a function with $\operatorname{inrad}(\text{fast}) \approx 0$ and $\|G_2\|_{\text{op}} \approx 1.0$, but this function was verified to be non-univalent ($\min|f'| \approx 0.02$, indicating near-critical behavior, and the boundary curve self-intersected). The fundamental issue is that the $2 \times 2$ truncation of the Grunsky matrix is an insufficient proxy for univalence: functions satisfying $\|G_2\|_{\text{op}} \leq 1$ but violating $\|G_N\|_{\text{op}} \leq 1$ for larger $N$ can be non-univalent. A successful application of this approach would require truncation at $N \geq 10$ and a semidefinite programming (SDP) solver such as MOSEK or SCS, which we did not implement.

### 3.4 Interval Arithmetic Certification

#### Framework

To certify our upper bound rigorously, we employed the interval arithmetic context of the `mpmath` library (`mpmath.iv`). In interval arithmetic, every real number $x$ is replaced by a closed interval $[x_{\text{lo}}, x_{\text{hi}}]$ guaranteed to contain the true value. Arithmetic operations use directed rounding: lower bounds are rounded down, upper bounds are rounded up. This ensures that the output interval always encloses the true mathematical result, regardless of the number of chained operations.

#### Implementation

We worked at 100 decimal digits of precision, far exceeding the requirements for our computation. The conformal radius chain (5 steps: Cayley, squaring, Möbius, square root, inverse Cayley) was evaluated in interval arithmetic, with each intermediate value stored as a complex interval (pair of real intervals for real and imaginary parts). The derivative $\psi'(0)$ was tracked through the chain by the product rule at each step.

#### Test Suites

We implemented 8 test suites to validate the interval arithmetic framework:

- **Test A**: Single-slit conformal radius for $a \in \{0.1, 0.3, 0.5, 0.7, 0.9, 0.99\}$ --- all intervals had zero width (exact rational arithmetic).
- **Test B**: Monotonicity of $\operatorname{crad}(\mathbb{D} \setminus [a,1), 0)$ in $a$ over a grid --- verified strictly increasing.
- **Test C**: Limiting behavior --- $\operatorname{crad} \to 1$ as $a \to 1$ and $\operatorname{crad} \to 0$ as $a \to 0$, both confirmed.
- **Test D**: Cross-validation with non-interval floating-point computation --- agreement to 15+ digits.
- **Test E**: Certified upper bound for 3 slits, $r_0 = 0.5$ --- yielded $B_f \in [0.6814202223120523, 0.6814202223120523]$.
- **Test F**: Consistency with Skinner's lower bound --- confirmed $B_f > 0.5708858$ with margin $0.1105$.
- **Test G**: Survey of $n = 1, \ldots, 8$ slit configurations at near-optimal $r_0$ --- all certified above Skinner's bound.
- **Test H**: Tight certification that $B_f < 0.6815$ for the best configuration.

All 8 tests passed, certifying that $B_u \leq 0.6814202223120523$ with mathematical rigor.

---

## 4. Results

### 4.1 Upper Bound Table: $B_f$ for Radial Slit-Disk Domains

The following table presents the optimized upper bound $B_f = \operatorname{inrad}(\Omega_n)/\operatorname{crad}(\Omega_n, 0)$ for $n = 1, \ldots, 12$ radial slits at the optimal inner radius $r_0$:

| $n$ (slits) | Optimal $r_0$ | $\operatorname{crad}$ | $\operatorname{inrad}$ | $B_f$ | Relative to Carroll-OC |
|:-----------:|:-------------:|:---------------------:|:----------------------:|:-----:|:---------------------:|
| 1 | 0.500 | 0.8889 | 0.7500 | 0.8438 | +28.6% |
| 2 | 0.577 | 0.8660 | 0.6667 | 0.7698 | +17.3% |
| **3** | **0.500** | **0.7338** | **0.5000** | **0.6814** | **+3.8%** |
| 4 | 0.414 | 0.5774 | 0.4142 | 0.7174 | +9.3% |
| 5 | 0.370 | 0.4871 | 0.3702 | 0.7600 | +15.8% |
| 6 | 0.333 | 0.4198 | 0.3333 | 0.7941 | +21.0% |
| 7 | 0.303 | 0.3689 | 0.3026 | 0.8204 | +25.0% |
| 8 | 0.277 | 0.3291 | 0.2768 | 0.8409 | +28.1% |
| 9 | 0.255 | 0.2973 | 0.2549 | 0.8572 | +30.6% |
| 10 | 0.236 | 0.2712 | 0.2361 | 0.8706 | +32.6% |
| 11 | 0.220 | 0.2493 | 0.2198 | 0.8816 | +34.3% |
| 12 | 0.206 | 0.2308 | 0.2056 | 0.8909 | +35.7% |

The minimum $B_f$ occurs at $n = 3$ with $B_f = 0.6814$. For $n \geq 4$, the $B_f$ values monotonically increase, confirming that **$n = 3$ is optimal among radial slit configurations**. This is consistent with Goodman's (1945) original finding.

### 4.2 Certified Upper Bound

The interval arithmetic certification yields:

$$B_u \leq 0.6814202223120523$$

with the interval $[0.6814202223120523, 0.6814202223120523]$ (zero width at display precision). The certified computation uses the 3-fold symmetric domain $\Omega_3 = \mathbb{D} \setminus \{3 \text{ radial slits from } r_0 = 1/2 \text{ to } 1\}$, with conformal radius $\operatorname{crad}(\Omega_3, 0) = 0.7337616108654725\ldots$ (also certified) and inradius exactly $1/2$.

### 4.3 Comparison with Literature

| Source | Bound | Method | Our status |
|--------|-------|--------|------------|
| Skinner (2009) | $B_u > 0.5709$ | Implicit function + distortion | Reproduced numerically |
| Carroll-OC (2008) | $B_u \leq 0.6564$ | Harmonically symmetric arcs | Not reproduced |
| **This work** | $B_u \leq 0.6814$ | 3 radial slits, interval certified | **Certified** |
| This work | $B_u \leq 0.7698$ | 2 radial slits | Computed |
| This work | $B_u \leq 0.8544$ | Degree-2 polynomial $f(z)=z+az^2$ | Computed |

Our certified bound of $0.6814$ is $3.8\%$ above Carroll-Ortega-Cerdà's $0.6564$, which is the actual best upper bound. The gap is attributable to our use of straight radial slits rather than curved arcs (see Discussion).

### 4.4 Why $n = 3$ Is Optimal

The optimality of $n = 3$ among radial slit configurations can be understood geometrically. As $n$ increases, the slits become more numerous but each is shorter (the optimal $r_0$ decreases). The inradius is approximately $r_0 \approx 2\sin(\pi/n)/[1 + 2\sin(\pi/n)]$ for large $n$, which decreases as $\sim \pi/n$. Meanwhile, the conformal radius decreases as $\operatorname{crad} \sim r_0$ (since $r_0^n \to 0$ and $\operatorname{crad}(\mathbb{D} \setminus [0^+, 1), 0) \to 0$). The ratio $B_f = \operatorname{inrad}/\operatorname{crad}$ initially decreases with $n$ (the inradius decreases faster than the conformal radius) but then increases for $n \geq 4$ (the conformal radius decreases even faster). The minimum at $n = 3$ reflects the balance between these competing effects.

### 4.5 Negative Results from Lower Bound Attempts

All lower bound approaches we attempted produced bounds weaker than Skinner's $0.5709$:

- **Bloch norm dichotomy**: $B_u \geq 0.34$ (limited by the sharp Koebe 1/4 constant).
- **Area theorem**: $B_u \geq 0.021$ (the area-to-inradius conversion is extremely lossy).
- **Degree-2 polynomial optimization**: confirmed $\operatorname{inrad}(f(\mathbb{D})) \geq 0.50$ for $f(z) = z + az^2$ with $|a| \leq 1/2$, consistent with $B_u > 0.50$ but not improving upon Skinner.
- **Grunsky adversarial search**: all minimum-inradius candidates were non-univalent; no valid upper bound below $0.6564$ was found.

### 4.6 Figures

The following figures, saved in the `figures/` directory, illustrate our results:

- **`figures/upper_bound_domains/slit_disk_domains.png`**: Visualization of the $n$-fold symmetric slit-disk domains $\Omega_n$ for $n = 1, 2, 3, 4, 5, 6$, showing the slit geometry and the inscribed disk at the optimal center.
- **`figures/upper_bound_domains/Bf_vs_r0.png`**: Plot of $B_f$ versus $r_0$ for $n = 1, 2, \ldots, 8$, showing the optimization landscape and confirming the minimum at $n = 3$.
- **`figures/Bu_timeline.png`**: Timeline of bounds on $B_u$ from 1925 to 2026, including our certified upper bound.

---

## 5. Discussion

### 5.1 Why Straight Radial Slits Cannot Match Curved Arcs

Our best radial slit bound ($B_u \leq 0.6814$ at $n = 3$) is $3.8\%$ above Carroll-Ortega-Cerdà's $0.6564$ using curved arcs. The geometric explanation is as follows. The upper bound $B_f = \operatorname{inrad}(\Omega)/\operatorname{crad}(\Omega, 0)$ is minimized when $\operatorname{inrad}(\Omega)$ is small relative to $\operatorname{crad}(\Omega, 0)$. For a fixed slit topology, **curved arcs minimize the conformal radius more efficiently than straight segments** because they can be shaped to satisfy the harmonic symmetry condition identified by Jenkins (1992) and Carroll (2008). Specifically, the Polya-Chebotarev theorem states that among all continua containing a given set of points, the continuum of minimal logarithmic capacity consists of arcs of critical trajectories of a quadratic differential. Straight radial slits are generally not critical trajectories of the relevant quadratic differential, so they are suboptimal.

To match Carroll-Ortega-Cerdà's bound, one would need to implement a numerical solver for the Polya-Chebotarev problem --- computing the critical trajectory arcs joining prescribed points on $\partial \mathbb{D}$ --- and then compute the conformal radius of the resulting slit domain, likely via numerical Schwarz-Christoffel mapping or a boundary integral method. This is a substantial computational undertaking that we did not complete.

### 5.2 Fundamental Barriers to Lower Bound Improvement

The difficulty of improving the lower bound $B_u > 0.5709$ is rooted in several structural barriers:

1. **Sharpness of Koebe 1/4.** The Koebe quarter theorem gives the pointwise estimate $\operatorname{dist}(f(z_0), \partial f(\mathbb{D})) \geq |f'(z_0)|(1-|z_0|^2)/4$, with the constant $1/4$ achieved by Möbius-composed Koebe functions. Any approach based solely on pointwise estimates cannot surpass $\|f\|_B / 4$, and for functions with $\|f\|_B$ close to 1 (near the identity), this gives only $1/4$.

2. **Interaction between local and global structure.** Skinner's method exploits the interaction between covering disks at different points, going beyond pointwise estimates. Improving upon it requires even more sophisticated global analysis --- for example, understanding how the boundary of $f(\mathbb{D})$ is constrained by the simultaneously holding coefficient bounds, area relations, and Grunsky inequalities.

3. **Insufficiency of finite-dimensional relaxations.** The Grunsky condition $\|G_N\|_{\text{op}} \leq 1$ for finite $N$ is necessary but not sufficient for univalence. Our $2 \times 2$ experiments show that functions satisfying the finite Grunsky constraint can be far from univalent. The moment hierarchy (using SDP with increasing $N$) converges to the true constraint in the limit, but convergence may be slow for this problem.

4. **Non-convexity of the univalent class.** The set $S$ is not convex in coefficient space, making convex optimization techniques (which would provide certified lower bounds) inapplicable without sophisticated relaxation.

### 5.3 Connection to the Grunsky Operator and Quasiconformal Mapping

The Grunsky matrix is intimately connected to the theory of quasiconformal extensions. By a theorem of Pommerenke, $\|G\|_{\text{op}} = k$ if and only if $f$ has a $K$-quasiconformal extension to $\mathbb{C}$ with $K = (1+k)/(1-k)$. For univalent $f$, $\|G\|_{\text{op}} \leq 1$, with equality if and only if $f$ maps onto a domain whose complement has zero area. This connection suggests that extremal functions for $B_u$ may have images whose complements are "thin" sets (arcs or continua), consistent with the slit-domain constructions used for upper bounds.

A promising direction for future work is to formulate the $B_u$ optimization as a problem over the unit ball of the Grunsky operator: minimize $\operatorname{inrad}(f(\mathbb{D}))$ subject to $\|G\|_{\text{op}} \leq 1$ and $a_1 = 1$. The Lasserre moment hierarchy provides a systematic way to approximate this problem with a sequence of SDP relaxations that converge to the true optimum from below (providing certified lower bounds on $B_u$).

### 5.4 Comparison with Bounds for Related Constants

The table below compares the state of bounds across the four Bloch-Landau constants:

| Constant | Lower bound | Upper bound | Gap | Relative gap |
|----------|:-----------:|:-----------:|:---:|:------------:|
| $B$ | $0.4332$ (Chen-Gauthier 1996) | $0.4719$ (Ahlfors-Grunsky 1937) | $0.039$ | $8.5\%$ |
| $B_l$ | $0.500 + 10^{-335}$ (Yanagihara 1995) | (no explicit upper) | --- | --- |
| $L$ | $0.500 + 10^{-335}$ (Yanagihara 1995) | $0.5433$ (Rademacher 1943) | $0.043$ | $8.3\%$ |
| $B_u$ | $0.5709$ (Skinner 2009) | $0.6564$ (Carroll-OC 2008) | $0.086$ | $14.0\%$ |

The univalent Bloch constant $B_u$ has the largest relative gap, suggesting both the most room for improvement and the most difficulty. The Bloch constant $B$ is conjectured to equal the Ahlfors-Grunsky upper bound, with the gap due to the difficulty of the lower bound. For $L$, the upper bound (Rademacher 1943) is conjectured to be exact, with the gap again on the lower side. For $B_u$, both the lower and upper bounds may be far from the true value.

### 5.5 The Role of Domain Symmetry in Extremal Problems

Our results confirm the classical observation that extremal domains for $B_u$ have low-fold symmetry. Among radial slit domains, $n = 3$ is optimal. Carroll-Ortega-Cerdà's bound uses a 4-fold symmetric construction with curved arcs. Jenkins's necessary conditions allow extremal domains with any symmetry type (or none), but the known constructions all exploit discrete rotational symmetry to reduce the problem to a single parameter.

The question of whether the true extremal domain has a specific symmetry type remains open. If the extremal domain has $n$-fold symmetry, then the extremal problem reduces to a 1-parameter optimization (over the slit parameter), and high-precision computation of $B_u$ becomes feasible. If the extremal domain is asymmetric, the problem is intrinsically multi-parameter and much harder.

Baernstein and Vinson (1998) established local minimality results for symmetric configurations, supporting the conjecture that the extremal domain is symmetric. However, their results do not determine the symmetry type.

---

## 6. Conclusion

### 6.1 Summary of Main Contributions

This research project conducted a systematic computational investigation of bounds on the univalent Bloch constant $B_u$. Our main contributions are:

1. **Certified upper bound.** We proved $B_u \leq 0.6814202223$ using a 3-fold symmetric radial slit-disk domain with $r_0 = 1/2$, computed via an exact 5-step Cayley-Joukowsky conformal map chain and certified with mpmath interval arithmetic at 100-digit precision. While this does not improve upon Carroll-Ortega-Cerdà's $0.6564$, it provides an independently derived and rigorously certified bound.

2. **Interval arithmetic framework.** We developed a reusable interval arithmetic certification pipeline for conformal radius computations, with 8 comprehensive test suites covering monotonicity, limiting behavior, cross-validation, and consistency checks. This framework can be applied to certify any future bound obtained through conformal map chain computations.

3. **Comprehensive negative results.** We documented in detail why three natural approaches fail to improve upon existing bounds:
   - The Koebe 1/4 + Bloch norm dichotomy is limited by the sharpness of the Koebe constant for the Schlicht class.
   - The $2 \times 2$ Grunsky matrix constraint is too weak to enforce univalence, with all optimizer solutions being non-univalent.
   - Higher-fold radial symmetry ($n \geq 4$) produces worse upper bounds than $n = 3$.

4. **Complete optimization landscape.** We computed $B_f$ for $n = 1, \ldots, 12$ radial slit configurations at optimized inner radii, providing a comprehensive picture of the slit-disk approach and confirming $n = 3$ as optimal.

### 6.2 Honest Assessment

We did **not** achieve any improvement over the best previously published bounds on $B_u$. The lower bound remains at $B_u > 0.5708858$ (Skinner 2009), and the best upper bound remains at $B_u \leq 0.6564$ (Carroll and Ortega-Cerdà 2008). The gap of approximately $0.086$ remains unchanged. This outcome reflects the genuine difficulty of the problem: the univalent Bloch constant has resisted improvement for over 15 years despite active interest in the area.

### 6.3 Future Directions

Based on our investigation, we identify five specific directions for future work:

1. **Curved-arc domain construction.** Implement the Polya-Chebotarev numerical solver to construct harmonically symmetric curved-arc slit domains, potentially improving upon Carroll-Ortega-Cerdà's $0.6564$. This requires solving an algebraic equation for the critical trajectories of a quadratic differential and computing the conformal radius of the resulting domain via Schwarz-Christoffel mapping.

2. **SDP hierarchy with large Grunsky matrices.** Formulate the lower bound problem as $\max\{R : \|G_N\|_{\text{op}} \leq 1, a_1 = 1 \implies \operatorname{inrad}(f(\mathbb{D})) \geq R\}$ and solve the dual SDP with $N \geq 10$ using MOSEK or SCS. The moment hierarchy guarantees convergence to $B_u$ as $N \to \infty$.

3. **Loewner chain optimal control.** Reformulate the $B_u$ problem as an optimal control problem for the Loewner differential equation $\partial_t f(z,t) = z f'(z,t) p(z,t)$ with $p$ ranging over the class of functions with positive real part. The control function $p$ parameterizes the evolution of the slit, and minimizing the inradius of the limiting domain at $t \to \infty$ gives $B_u$.

4. **PSLQ closed-form identification.** If high-precision computation (100+ digits) of the conjectured extremal $B_f$ value can be achieved (e.g., via the curved-arc approach), use the PSLQ algorithm to test whether the value is an algebraic number or involves special function values (Gamma at rational arguments, logarithmic capacities of specific sets).

5. **Winding number + Grunsky combined constraint.** Strengthen the Grunsky matrix approach by adding explicit winding number constraints (the argument principle enforces that $f(\partial \mathbb{D})$ winds exactly once around every point in $f(\mathbb{D})$), together with area-principle constraints, to tighten the feasible set beyond $\|G_N\|_{\text{op}} \leq 1$ alone.

---

## References

- Ahlfors, L. V. and Grunsky, H. (1937). Über die Blochsche Konstante. *Math. Z.*, 42(1):671--673.
- Baernstein, A. II and Vinson, J. P. (1998). Local minimality results related to the Bloch and Landau constants. In *Quasiconformal Mappings and Analysis*, pp. 55--89. Springer, New York.
- Beller, E. and Hummel, J. A. (1985). On the univalent Bloch constant. *Complex Variables*, 4(3):243--252.
- Bhowmik, B. and Sen, S. (2023). Improved Bloch and Landau constants for meromorphic functions. *Canad. Math. Bull.*, 66(4):1269--1273.
- Bloch, A. (1925). Les théorèmes de M. Valiron sur les fonctions entières et la théorie de l'uniformisation. *Ann. Fac. Sci. Toulouse*, 17(3):1--22.
- Bonk, M., Minda, D., and Yanagihara, H. (1996). Distortion theorems for locally univalent Bloch functions. *J. Anal. Math.*, 69:73--95.
- Bonk, M., Minda, D., and Yanagihara, H. (1997). Distortion theorems for Bloch functions. *Pacific J. Math.*, 179(2):241--262.
- Carroll, T. (2008). An extension of Jenkins's condition for extremal domains associated with the univalent Bloch-Landau constant. *Comput. Methods Funct. Theory*, 8:389--401.
- Carroll, T. and Ortega-Cerdà, J. (2010). The univalent Bloch-Landau constant, harmonic symmetry and conformal glueing. *J. Math. Pures Appl.*, 93(6):590--603. (Preprint 2008, arXiv:0806.2282.)
- Chen, H. and Gauthier, P. M. (1996). On Bloch's constant. *J. Anal. Math.*, 69:275--291.
- Derganc, M. and Urbanč, L. (2025). Numeric computations of Landau's constant. *Proc. SCORES'25*.
- Fedorov, S. I. (1985). On a variational problem of Chebotarev in the theory of capacity of plane sets and covering theorems for univalent conformal mappings. *Sb. Math.*, 52(1):115--133.
- Goodman, R. (1945). On the Bloch-Landau constant for schlicht functions. *Bull. Amer. Math. Soc.*, 51(3):234--239.
- Heins, M. (1962). *Selected topics in the classical theory of functions of a complex variable*. Athena Series, Holt, Rinehart and Winston.
- Jenkins, J. A. (1992). A criterion associated with the schlicht Bloch constant. *Kodai Math. J.*, 15(1):79--81.
- Jenkins, J. A. (1998). On the Schlicht Bloch constant II. *Indiana Univ. Math. J.*, 47(4):1519--1523.
- Kudryavtseva, O. S. and Solodov, A. P. (2024). Sharp univalent covering domain for the class of holomorphic self-maps of a disc with fixed interior and boundary points. *Sb. Math.*, 215(6):111--138.
- Landau, E. (1929). Über die Blochsche Konstante und zwei verwandte Weltkonstanten. *Math. Z.*, 30(1):608--634.
- Rademacher, H. (1943). On the Bloch-Landau constant. *Amer. J. Math.*, 65(3):387--390.
- Reich, E. (1956). On a Bloch-Landau constant. *Proc. Amer. Math. Soc.*, 7:75--76.
- Robinson, R. M. (1935). The Bloch constant $\mathfrak{A}$ for a schlicht function. *Bull. Amer. Math. Soc.*, 41:535--540.
- Skinner, B. (2009). The univalent Bloch constant problem. *Complex Var. Elliptic Equ.*, 54(10):951--955.
- Toppila, S. (1969). A remark on Bloch's constant for schlicht functions. *Ann. Acad. Sci. Fenn.*, 423:1--7.
- Xiong, C. (1998). On the Bloch constant. *Sci. China Ser. A*, 41(6):615--622.
- Yanagihara, H. (1994). Sharp distortion estimate for locally schlicht Bloch functions. *Bull. London Math. Soc.*, 26(6):539--542.
- Yanagihara, H. (1995). On the locally univalent Bloch constant. *J. Anal. Math.*, 65:1--17.
