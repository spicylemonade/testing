# Hyperbolic Metric Approach to Bounding B_u

## 1. Formulation of B_u in Terms of Hyperbolic Geometry

For a simply connected domain $\Omega \subset \mathbb{C}$ with $\Omega \neq \mathbb{C}$, the
Riemann mapping theorem guarantees a conformal map from the unit disk $\mathbb{D}$ onto
$\Omega$. The domain carries a unique complete conformal metric of constant curvature
$-4$, the **hyperbolic (Poincare) metric**, with density $\lambda_\Omega(w)$. This density
is related to the conformal radius $R(w, \Omega)$ by:

$$
\lambda_\Omega(w) = \frac{1}{R(w, \Omega)}.
$$

The conformal radius admits classical two-sided bounds in terms of the Euclidean
distance to the boundary $d(w, \partial\Omega)$, known as the **Koebe bounds**:

$$
\frac{1}{4\,d(w,\partial\Omega)} \;\le\; \lambda_\Omega(w) \;\le\; \frac{1}{d(w,\partial\Omega)},
$$

or equivalently:

$$
d(w, \partial\Omega) \;\le\; R(w, \Omega) \;\le\; 4\,d(w, \partial\Omega).
$$

These follow directly from the Koebe one-quarter theorem and the Schwarz lemma
applied to the inverse Riemann map.

Now let $f \in S$ (the class of univalent functions on $\mathbb{D}$ normalized by
$f(0) = 0$, $f'(0) = 1$) and set $\Omega = f(\mathbb{D})$. Then:

- The conformal radius at the origin is $R(0, \Omega) = |f'(0)| \cdot R(0, \mathbb{D}) = 1 \cdot 1 = 1$.
- Therefore $\lambda_\Omega(0) = 1$.
- By the Koebe bound: $1/4 \le d(0, \partial\Omega) \le 1$.

The **inradius** of $\Omega$ is defined as

$$
B_f \;=\; \sup_{w \in \Omega}\, d(w, \partial\Omega).
$$

By the Koebe bounds, this satisfies $B_f \ge \sup_w R(w,\Omega)/4$.

Since $f\colon \mathbb{D} \to \Omega$ is conformal, the **Schwarz--Pick lemma** gives the
fundamental transfer identity:

$$
\lambda_\Omega(f(z))\,|f'(z)| \;=\; \lambda_{\mathbb{D}}(z) \;=\; \frac{1}{1-|z|^2}.
$$

Rearranging:

$$
\lambda_\Omega(f(z)) \;=\; \frac{1}{(1-|z|^2)\,|f'(z)|} \;=\; \frac{1}{R(f(z),\Omega)}.
$$

Hence the conformal radius at $f(z)$ is $(1-|z|^2)|f'(z)|$, and the supremum over
all $z \in \mathbb{D}$ yields the **Bloch semi-norm**:

$$
\beta(f) \;=\; \sup_{z \in \mathbb{D}}\, |f'(z)|\,(1-|z|^2) \;=\; \sup_{w \in \Omega}\, R(w, \Omega).
$$

For every $f \in S$ we have $\beta(f) \ge |f'(0)|(1-0) = 1$, and the Koebe bounds
relate the Bloch semi-norm to the inradius:

$$
\frac{\beta(f)}{4} \;\le\; B_f \;\le\; \beta(f) \;\le\; 4\,B_f.
$$


## 2. Lower Bound via Schwarz--Pick

The core argument for the basic lower bound on $B_u$ proceeds as follows.

**Proposition.** For every $f \in S$, we have $B_f \ge 1/4$.

*Proof.* By the chain of inequalities established above:

$$
B_f \;=\; \sup_w d(w, \partial\Omega) \;\ge\; \frac{1}{4}\sup_w R(w, \Omega)
\;=\; \frac{\beta(f)}{4} \;\ge\; \frac{1}{4}.
$$

The first inequality is the Koebe bound; the second uses $\beta(f) \ge 1$.
Taking the infimum over $S$ gives $B_u \ge 1/4$. $\square$

**Sharpness analysis.** Can $\beta(f) = 1$ for some $f \in S$? Yes:

- The **identity map** $f(z) = z$ has $\beta = 1$ and $B_f = 1$.
- The function $f(z) = \tfrac{1}{2}\log\!\bigl(\tfrac{1+z}{1-z}\bigr) = \operatorname{arctanh}(z)$
  maps $\mathbb{D}$ onto the strip $\{w : |\operatorname{Im} w| < \pi/4\}$ (when suitably
  interpreted as a branch). Here $\beta = 1$ and $B_f = \pi/4 \approx 0.7854$.

The question is whether there exists $f \in S$ with $\beta(f) = 1$ and $B_f$ close
to $1/4$. If the Koebe bound were sharp in this setting, we would have
$B_u = 1/4$. However, the Koebe bound loses a factor of 4 pointwise, and for
functions with $\beta = 1$ the geometry of $\Omega$ is constrained enough that $B_f$
cannot approach $1/4$. In fact, the known lower bound for the univalent Bloch
constant is $B_u \ge 0.5705\ldots$ [@bonkmindayanagihara1996], which far exceeds
$1/4 = 0.25$.

The obstruction to achieving $B_f = 1/4$ via the Schwarz--Pick route alone is
that the Koebe bound $d(w,\partial\Omega) \ge R(w,\Omega)/4$ is only sharp at a
single boundary point (the point closest to $w$ along the direction of the Koebe
extremal slit), not uniformly over all of $\Omega$ simultaneously.


## 3. Refined Hyperbolic Bounds

To go beyond the $1/4$ barrier, we exploit the **global geometry** of the
hyperbolic metric on $\Omega$.

### Hyperbolic balls and their Euclidean size

The hyperbolic ball $B_\Omega(0, t) = \{w \in \Omega : d_\Omega(0,w) < t\}$ has a
clean preimage under $f$:

$$
B_\Omega(0, t) \;=\; f\!\bigl(\mathbb{D}(0, \tanh(t/2))\bigr),
$$

since $f$ is an isometry from $(\mathbb{D}, \lambda_{\mathbb{D}})$ to $(\Omega, \lambda_\Omega)$.
Setting $r = \tanh(t/2) \in (0,1)$, the **growth theorem** for $f \in S$ gives:

$$
\frac{r}{(1+r)^2} \;\le\; |f(z)| \;\le\; \frac{r}{(1-r)^2}
\quad\text{for } |z| = r,
$$

so the Euclidean diameter of $B_\Omega(0,t)$ is controlled by distortion estimates.

### Optimizing the location of the inradius center

Let $w^* \in \Omega$ be the **Chebyshev center** (the point achieving
$B_f = d(w^*, \partial\Omega)$), and let $z^* = f^{-1}(w^*)$ with
$|z^*| = \tanh(\rho/2)$ where $\rho = d_\Omega(0, w^*)$ is the hyperbolic
distance from the origin to $w^*$.

Then by the Koebe bound at $w^*$:

$$
B_f \;=\; d(w^*, \partial\Omega) \;\ge\; \frac{R(w^*, \Omega)}{4}
\;=\; \frac{|f'(z^*)|\,(1-|z^*|^2)}{4}.
$$

Setting $s = |z^*|$, the distortion theorem gives $|f'(z^*)| \ge (1-s)/(1+s)^3$,
so:

$$
B_f \;\ge\; \frac{(1-s)(1-s^2)}{4(1+s)^3}
\;=\; \frac{(1-s)^2}{4(1+s)^2}.
$$

Optimizing over $s \in [0,1)$: the right side is maximized at $s = 0$, giving
$B_f \ge 1/4$. This confirms that the Schwarz--Pick approach, combined with
pointwise distortion, cannot improve the $1/4$ bound by optimization over $z^*$
alone. The distortion theorem bounds are too lossy at $|z| > 0$ to help.

### What is needed for improvement

To surpass $1/4$, one must use **global** information about $\Omega$ that the
pointwise Schwarz--Pick and Koebe bounds do not capture. Specifically:

1. **Area bounds.** The area of the largest inscribed disk in $\Omega$ is
   $\pi B_f^2$, while the area of $\Omega$ satisfies
   $\operatorname{Area}(\Omega) = \int_{\mathbb{D}} |f'(z)|^2\,dA(z) \ge \pi$
   (by the area theorem). Combining these with isoperimetric-type inequalities
   on $\Omega$ yields better bounds.

2. **Curvature constraints.** The Gaussian curvature of $\lambda_\Omega$ is
   identically $-4$, which constrains how rapidly $\lambda_\Omega(w)$ can vary.
   The minimum of $\lambda_\Omega$ (equivalently, the maximum of $R(w,\Omega)$)
   cannot be too isolated; the hyperbolic metric must transition smoothly. This
   forces large inscribed disks somewhere in $\Omega$.

3. **Extremal domain geometry.** If $B_f$ is small, $\Omega$ must be "thin"
   everywhere, which conflicts with $\lambda_\Omega(0) = 1$ and the negative
   curvature constraint. Making this conflict quantitative is the content of
   the work of Bonk, Minda, and Yanagihara [@bonkmindayanagihara1996;
   @bonkmindayanagihara1997].


## 4. Comparison with Ahlfors' Method

Ahlfors [@ahlfors1938] introduced the **ultrahyperbolic metric method** to
establish lower bounds for the Bloch constant. His approach constructs a
conformal metric on the range surface (possibly a branched covering of the
plane) with curvature $\le -4$, then applies the Ahlfors--Schwarz lemma to
compare it with the hyperbolic metric of the disk.

For the **general Bloch constant** $B$ (allowing branched coverings), this
method is extremely powerful: Ahlfors obtained $B \ge \sqrt{3}/4 \approx 0.4330$,
later improved by Heins and others.

For the **univalent Bloch constant** $B_u$, however, the covering surface is a
single unbranched sheet (since $f$ is univalent). In this case:

- The ultrahyperbolic metric on $\Omega$ reduces to the ordinary hyperbolic
  metric $\lambda_\Omega$.
- The Ahlfors--Schwarz comparison reduces to the classical Schwarz--Pick lemma.
- No additional leverage is gained from the covering-surface viewpoint.

Consequently, Ahlfors' method applied naively to the univalent case yields only
$B_u \ge 1/4$, exactly the same as the direct Schwarz--Pick argument. The
strength of Ahlfors' approach lies in handling branch points, which are absent
in the univalent setting.

This explains why the best bounds on $B_u$ (such as those of Bonk--Minda--Yanagihara)
rely on different techniques: distortion theorems for Bloch functions, careful
analysis of extremal domains, and area-type estimates, rather than the
ultrahyperbolic metric.


## 5. Numerical Computation

### Summary of bounds obtained

| Method | Lower bound on $B_u$ | Reference |
|--------|---------------------|-----------|
| Koebe one-quarter + Schwarz--Pick | $0.2500$ | Classical |
| Hyperbolic metric optimization (Section 3) | $0.2500$ | This analysis |
| Bonk--Minda--Yanagihara distortion | $0.5705\ldots$ | [@bonkmindayanagihara1996] |
| Conjectured value | $\approx 0.6564\ldots$ | [@bonkmindayanagihara1997] |

The basic hyperbolic metric approach yields $B_u \ge 1/4 = 0.25$. As shown in
Section 3, no amount of optimization within the Schwarz--Pick framework alone
can improve this: the Koebe distortion bounds are sharp pointwise, and their
composition with the hyperbolic transfer identity bottlenecks at $s = 0$.

The substantial improvement to $B_u \ge 0.5705\ldots$ achieved by Bonk, Minda,
and Yanagihara [@bonkmindayanagihara1996] requires ingredients beyond
Schwarz--Pick:

- **Subordination chains** and integral means estimates for Bloch functions.
- **Distortion theorems** specific to the subclass of $S$ with controlled Bloch
  norm, exploiting the interplay between the univalence constraint and the
  Bloch condition.
- **Extremal problem analysis** showing that candidate extremal domains for
  small $B_f$ necessarily have geometric properties (e.g., controlled boundary
  spiraling) that force $B_f$ above $1/4$ by a definite amount.

Their refined distortion estimates for locally univalent Bloch functions
[@bonkmindayanagihara1997] further constrain the geometry of extremal domains
and support the conjecture that $B_u \approx 0.6564$.

### Conclusion

The hyperbolic metric approach provides a clean conceptual framework for
understanding $B_u$: the inradius is controlled by the minimum of the
hyperbolic density, which in turn is governed by the Schwarz--Pick lemma.
However, the approach saturates at $B_u \ge 1/4$ because the Koebe bounds are
only pointwise sharp. Closing the gap between $0.25$ and the true value of
$B_u \approx 0.57$--$0.66$ requires global geometric arguments that go beyond
the local nature of the Schwarz--Pick comparison.


## References

- [@ahlfors1938]: Ahlfors, L.V. "An extension of Schwarz's lemma."
  *Trans. Amer. Math. Soc.* **43** (1938), 359--364.
- [@bonkmindayanagihara1996]: Bonk, M., Minda, D., and Yanagihara, H.
  "Distortion theorems for locally univalent Bloch functions."
  *J. Analyse Math.* **69** (1996), 73--95.
- [@bonkmindayanagihara1997]: Bonk, M., Minda, D., and Yanagihara, H.
  "Distortion theorems for Bloch functions."
  *Pacific J. Math.* **179** (1997), 241--262.
