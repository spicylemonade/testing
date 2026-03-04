# Deep-Dive Mathematical Formulation: The Univalent Bloch Constant

## 1. Definitions

### 1.1 The Class $\mathcal{F}$

Let $\mathbb{D} = \{z \in \mathbb{C} : |z| < 1\}$ denote the open unit disk. Define $\mathcal{F}$ to be the class of all holomorphic functions $f : \mathbb{D} \to \mathbb{C}$ normalized by $f'(0) = 1$. Note that the normalization $f(0) = 0$ is not required; the condition is solely on the derivative at the origin. This class encompasses all holomorphic functions on $\mathbb{D}$ whose derivative has modulus 1 at the origin, and is equivalent (up to a translation) to the requirement $|f'(0)| = 1$ used in many references.

### 1.2 The Bloch Radius $B_f$

For any $f \in \mathcal{F}$, define $B_f$ to be the supremum of radii $r > 0$ such that there exists a domain $U \subset \mathbb{D}$ on which $f$ is injective (univalent) and $f(U)$ contains a disk of radius $r$. More precisely:
$$
B_f = \sup\{r > 0 : \exists\, w_0 \in \mathbb{C},\, U \subset \mathbb{D} \text{ open, such that } f|_U \text{ is injective and } D(w_0, r) \subset f(U)\}.
$$
This is the radius of the largest univalent disk in the image $f(\mathbb{D})$, where "univalent disk" means a disk that is the injective image of some subdomain of $\mathbb{D}$.

### 1.3 The Bloch Constant $B$

The **Bloch constant** is defined as:
$$
B := \inf_{f \in \mathcal{F}} B_f.
$$
Bloch's theorem guarantees $B > 0$. The best known bounds are:
$$
\frac{\sqrt{3}}{4} + 2 \times 10^{-4} \leq B \leq \sqrt{\frac{\sqrt{3}-1}{2}} \cdot \frac{\Gamma(1/3)\,\Gamma(11/12)}{\Gamma(1/4)} \approx 0.47186.
$$
The lower bound is due to Chen and Gauthier (1996); the upper bound to Ahlfors and Grunsky (1937). The Ahlfors-Grunsky upper bound is conjectured to be the true value.

### 1.4 The Landau Constant $L$

For $f \in \mathcal{F}$, let $L_f$ denote the supremum of radii $r > 0$ such that $f(\mathbb{D})$ contains a disk of radius $r$ (without requiring the disk to be a univalent image). The **Landau constant** is:
$$
L := \inf_{f \in \mathcal{F}} L_f.
$$
The best known bounds are:
$$
\frac{1}{2} + 10^{-335} < L \leq \frac{\Gamma(1/3)\,\Gamma(5/6)}{\Gamma(1/6)} \approx 0.5433.
$$
The lower bound $L > 1/2 + 10^{-335}$ is due to Yanagihara (1995). The upper bound (Rademacher 1943) is conjectured to be the exact value.

### 1.5 The Locally Univalent Bloch Constant $B_l$

Restrict $\mathcal{F}$ to functions that are locally univalent (i.e., $f'(z) \neq 0$ for all $z \in \mathbb{D}$). For such $f$, let $B_{l,f}$ be the Bloch radius as defined above. The **locally univalent Bloch constant** is:
$$
B_l := \inf\{B_{l,f} : f \in \mathcal{F},\, f'(z) \neq 0\ \forall z \in \mathbb{D}\}.
$$
By Yanagihara (1995), $B_l > 1/2 + 10^{-335}$.

### 1.6 The Univalent Bloch Constant $B_u$

Restrict $\mathcal{F}$ to functions that are globally univalent (injective) on $\mathbb{D}$, i.e., the Schlicht class $\mathcal{S}$ (with normalization $f'(0) = 1$ but not requiring $f(0) = 0$). For such $f$, define $B_f$ as above, where we now seek the largest disk $D(w_0, r) \subset f(\mathbb{D})$. (Since $f$ is already univalent on all of $\mathbb{D}$, any disk in $f(\mathbb{D})$ is automatically a univalent disk.) The **univalent Bloch constant** is:
$$
B_u := \inf\{B_f : f \in \mathcal{F},\, f \text{ is univalent on } \mathbb{D}\}.
$$
The best known bounds are $B_u > 0.5708858$ (Skinner 2009) and $B_u \leq 1$ (trivially, from $f(z) = z$). Carroll and Ortega-Cerda (2008) obtained the non-trivial upper bound $B_u \leq 0.6564$.

## 2. The Chain of Inequalities: $B \leq B_l \leq L \leq B_u$

### 2.1 $B \leq B_l$

**Proof sketch:** The infimum defining $B$ is taken over all $f \in \mathcal{F}$, while $B_l$ restricts to locally univalent $f$. Since locally univalent functions form a subset of $\mathcal{F}$, we have $B_l \geq B$. For the reverse direction: every function in $\mathcal{F}$ has $B_f \geq B$, and since the infimum can potentially be approached more closely using functions with critical points, we get $B \leq B_l$.

More precisely: the class over which $B$ is the infimum is larger than the class for $B_l$. An infimum over a larger set is always less than or equal to the infimum over a subset. Hence $B \leq B_l$.

### 2.2 $B_l \leq L$

**Proof sketch:** For a locally univalent function $f \in \mathcal{F}$ with $f'(z) \neq 0$ on $\mathbb{D}$, the Bloch radius $B_f$ measures the largest univalent disk in $f(\mathbb{D})$. But $L_f$ (the Landau radius) is the largest disk contained in $f(\mathbb{D})$ without requiring univalence. Since every univalent disk in $f(\mathbb{D})$ is in particular a disk in $f(\mathbb{D})$, we have $B_f \leq L_f$ for each locally univalent $f$. Taking infima over all locally univalent $f \in \mathcal{F}$:
$$
B_l = \inf B_f \leq \inf L_f.
$$
Moreover, the Landau constant $L$ is the infimum of $L_f$ over all $f \in \mathcal{F}$ (not just locally univalent). The infimum over the larger class could be smaller, but in fact for any $f \in \mathcal{F}$, the largest disk in $f(\mathbb{D})$ is at least $L$, so $B_l \leq L$.

### 2.3 $L \leq B_u$

**Proof sketch:** The Landau constant $L$ is the infimum of $L_f$ over all $f \in \mathcal{F}$, where $L_f$ is the radius of the largest disk in $f(\mathbb{D})$. When $f$ is univalent, $f(\mathbb{D})$ is a simply connected domain and $f : \mathbb{D} \to f(\mathbb{D})$ is a conformal equivalence. For univalent $f$, every disk in $f(\mathbb{D})$ is automatically a univalent disk (since $f^{-1}$ provides the local inverse), so $L_f = B_f$ for univalent $f$.

Since $L$ is the infimum over all $f \in \mathcal{F}$ and $B_u$ is the infimum over the subset of univalent $f$, we would expect $L \leq B_u$ if the larger class has smaller infimum. Indeed, since univalent functions form a subclass of $\mathcal{F}$:
$$
L = \inf_{f \in \mathcal{F}} L_f \leq \inf_{\substack{f \in \mathcal{F} \\ f \text{ univalent}}} L_f = \inf_{\substack{f \in \mathcal{F} \\ f \text{ univalent}}} B_f = B_u.
$$

## 3. Koebe 1/4 Theorem and the Bound $B_u \geq 1/4$

The Koebe quarter theorem states: if $f$ is univalent on $\mathbb{D}$ with $f(0) = 0$ and $f'(0) = 1$ (the normalized Schlicht class $S$), then $f(\mathbb{D}) \supset D(0, 1/4)$. The disk of radius 1/4 centered at the origin is contained in the image.

For a general univalent $f \in \mathcal{F}$ (with $f'(0) = 1$ but $f(0)$ arbitrary), consider $g(z) = f(z) - f(0)$, which is in $S$. Then $g(\mathbb{D}) \supset D(0, 1/4)$, so $f(\mathbb{D}) \supset D(f(0), 1/4)$. Since $f$ is univalent, $D(f(0), 1/4) \subset f(\mathbb{D})$ is a univalent disk. Hence $B_f \geq 1/4$ for all univalent $f \in \mathcal{F}$, giving $B_u \geq 1/4$.

The Koebe 1/4 constant is sharp for the Koebe function $k(z) = z/(1-z)^2$, which maps $\mathbb{D}$ onto $\mathbb{C} \setminus (-\infty, -1/4]$. The largest inscribed disk centered at the origin has radius 1/4, so $B_k = 1/4$ (this is close to the infimum but not exactly it, since the inradius of the image with respect to $w = 0$ is 1/4, but the overall inradius is larger since the disk can be placed at other centers).

However, $B_u$ is much larger than 1/4 because we optimize over all center points. For the Koebe function, the image $\mathbb{C} \setminus (-\infty, -1/4]$ contains arbitrarily large disks (by moving the center far from the slit), so $B_k = \infty$. The infimum $B_u$ is therefore not achieved by the Koebe function.

## 4. Goodman's 1945 Extremal Domain Construction

Ruth Goodman (1945) introduced a fundamental construction for obtaining upper bounds on $B_u$. Her idea was to consider specific simply connected domains $\Omega$ that are "nearly extremal" for the univalent Bloch constant.

**Construction:** Start with the unit disk $\mathbb{D}$ and remove a finite number of radial slits emanating from the boundary toward the interior. Specifically, consider the domain:
$$
\Omega = \mathbb{D} \setminus \bigcup_{k=1}^{n} S_k
$$
where each $S_k$ is a radial segment $S_k = \{r e^{i\theta_k} : r_k \leq r < 1\}$ for some inner radius $r_k \in (0,1)$ and angle $\theta_k$.

The conformal map $f : \mathbb{D} \to \Omega$ with $f(0) = 0$, $f'(0) > 0$ has a specific value of $f'(0)$, and after normalization to $f'(0) = 1$, the image becomes $\tilde{\Omega} = \Omega / f'(0)$. The univalent Bloch radius $B_f$ equals the inradius of $\tilde{\Omega}$ (the radius of the largest inscribed disk):
$$
B_f = \text{inrad}(\tilde{\Omega}) = \sup_{w \in \tilde{\Omega}} \text{dist}(w, \partial \tilde{\Omega}).
$$

Goodman specifically considered **symmetrically placed slits**: $n$ slits at equally spaced angles $\theta_k = 2\pi k/n$, all of the same inner radius $r_k = r$. By symmetry, the inradius of such a domain can be computed explicitly (or with high precision numerically), giving an upper bound $B_u \leq B_f$.

Goodman's original computation used $n = 3$ slits and obtained the bound $B_u \leq 0.6564$ (approximately). Her key insight was that the slits reduce the inradius of the conformally normalized domain, and that domains closer to the boundary of the Schlicht class tend to have smaller inradii.

## 5. Jenkins's Necessary Condition for Extremal Domains

James Jenkins (1992, 1998) established necessary conditions that any extremal domain for the univalent Bloch constant must satisfy.

**Jenkins's Criterion (1992):** If $f_0$ is an extremal univalent function for $B_u$ (i.e., $B_{f_0} = B_u$), then the extremal domain $\Omega_0 = f_0(\mathbb{D})$ must have the property that the largest inscribed disk in $\Omega_0$ touches the boundary $\partial \Omega_0$ at more than one point. More precisely, the inscribed disk of radius $B_u$ must be tangent to $\partial \Omega_0$ along arcs (not just isolated points).

**Jenkins's Extended Condition (1998):** In "On the Schlicht Bloch Constant II," Jenkins proved a stronger structural result. The boundary of the extremal domain $\Omega_0$ near the touching arcs must satisfy a specific differential equation related to quadratic differentials. Specifically, the boundary arcs where the extremal inscribed disk touches $\partial \Omega_0$ must be trajectories of a quadratic differential $Q(w)\,dw^2$ that arises from the variational problem.

**Carroll's Extension (2008):** Tom Carroll extended Jenkins's condition, showing that in an extremal domain for $B_u$, the arcs where the boundary of the maximal inscribed disk meets $\partial \Omega_0$ must exhibit **harmonic symmetry** with respect to the origin. This means that the arcs are invariant under a specific harmonic measure condition: the harmonic measure of each arc as seen from the origin must equal the harmonic measure as seen from the center of the extremal inscribed disk.

This condition severely constrains the geometry of candidate extremal domains. Carroll and Ortega-Cerda (2008) exploited this constraint to show that Goodman-type domains with harmonically symmetric arc removal from the disk yield the best known upper bounds.

## 6. The Carroll-Ortega-Cerda Upper Bound

Carroll and Ortega-Cerda (2008) obtained the best known non-trivial upper bound:
$$
B_u \leq 0.6564.
$$
Their construction modifies Goodman's approach:

1. Start with $\mathbb{D}$ and remove arcs (not straight radial slits) from the boundary.
2. The arcs are chosen to be **harmonically symmetric** with respect to the origin: the domain $\Omega = \mathbb{D} \setminus \bigcup \gamma_k$ is such that each arc $\gamma_k$ has equal harmonic measure as seen from $z = 0$ and from the point that becomes the center of the extremal inscribed disk.
3. They used Fedorov's explicit solution of the Polya-Chebotarev problem for four symmetrically placed points to compute the conformal radius of the resulting domain.
4. The optimal configuration uses 3-fold symmetric arc removal (4 total arcs in the symmetric arrangement) and yields the bound $B_u \leq 0.6564$.

The existence of such domains was established using conformal welding techniques (following Bishop 2007).

## 7. Skinner's Lower Bound Method

Brian Skinner (2009) proved the best known lower bound $B_u > 0.5708858$. His method uses:

1. **Distortion estimates for univalent functions:** For $f \in S$ (normalized Schlicht class), sharp distortion theorems give pointwise bounds on $|f(z)|$ and $|f'(z)|$.
2. **Implicit function argument:** Skinner constructs an implicit function $C(r)$ such that for any univalent $f$ with $f'(0) = 1$, the image $f(\mathbb{D})$ must contain a disk of radius at least $C(r)$ centered at some point of distance $\leq r$ from $f(0)$.
3. **Optimization:** The lower bound $B_u > 0.5708858$ comes from optimizing $C(r)$ over the radius parameter $r$.

The method relies on the classical growth theorem for univalent functions: $|z|/(1+|z|)^2 \leq |f(z)| \leq |z|/(1-|z|)^2$ and the distortion theorem $|f'(z)| \geq (1-|z|)/(1+|z|)^3$.

## 8. Summary of Known Bounds

| Constant | Lower Bound | Upper Bound | Gap |
|----------|------------|------------|-----|
| $B$ (Bloch) | $\sqrt{3}/4 + 2\times 10^{-4} \approx 0.4332$ | $\approx 0.47186$ (Ahlfors-Grunsky) | $\approx 0.039$ |
| $B_l$ (locally univalent Bloch) | $1/2 + 10^{-335}$ | Unknown explicit bound | Unknown |
| $L$ (Landau) | $1/2 + 10^{-335}$ | $\Gamma(1/3)\Gamma(5/6)/\Gamma(1/6) \approx 0.5433$ | $\approx 0.043$ |
| $B_u$ (univalent Bloch) | $0.5708858$ (Skinner 2009) | $0.6564$ (Carroll-Ortega-Cerda 2008) | $\approx 0.086$ |

The gap for $B_u$ is notably the largest among these constants, suggesting significant room for improvement in both directions. The chain $B \leq B_l \leq L \leq B_u$ provides structural constraints: any improvement to the lower bound on $L$ immediately improves the lower bound on $B_u$ (though $B_u$ is known to be substantially larger than $L$).

## 9. Key Techniques for Potential Improvement

### 9.1 For Lower Bounds
- **Coefficient constraints:** The de Branges theorem (formerly Bieberbach conjecture) gives $|a_n| \leq n$ for $f(z) = z + a_2 z^2 + \cdots$ in $S$. Combined with growth/distortion theorems, this provides stronger estimates than used by Skinner.
- **Grunsky inequalities:** The Grunsky matrix $G_N$ of a univalent function satisfies $\|G_N\|_{\text{op}} \leq 1$, providing an infinite hierarchy of constraints that can be encoded as semidefinite programs.
- **Hyperbolic metric methods:** The Schwarz-Pick lemma and its generalizations provide covering theorems via comparison of the hyperbolic metric of $f(\mathbb{D})$ with that of $\mathbb{D}$.

### 9.2 For Upper Bounds
- **Domain optimization:** Searching over larger families of slit-disk domains (varying number of slits, asymmetric configurations, non-radial slits).
- **Logarithmic capacity connection:** The inradius of a simply connected domain is related to its logarithmic capacity via the conformal radius. The Polya-Chebotarev problem minimizes logarithmic capacity over continua containing prescribed points.
- **Variational methods:** Schiffer's variational method provides necessary conditions for extremal domains, which can be used to constrain the search space.

This formulation provides the mathematical foundation for all subsequent computational and analytical work in this research project.
