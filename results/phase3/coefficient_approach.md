# Coefficient Bounds Approach to the Bloch–Landau Constant

## (a) Express B_f in terms of Taylor coefficients

For $f(z) = z + a_2 z^2 + a_3 z^3 + \cdots \in S$ (the class of normalized univalent functions on $\mathbb{D}$):

- $f(\mathbb{D})$ is the image domain, with boundary $\partial f(\mathbb{D})$ given (in a limit sense) by $f(\partial\mathbb{D})$.
- The **inradius** is $B_f = \sup_{w \in f(\mathbb{D})} d(w,\, \partial f(\mathbb{D}))$.

**Boundary parametrization.** On $|z| = 1$ (limit $r \to 1^-$):

$$
w(t) = e^{it} + a_2 e^{2it} + a_3 e^{3it} + \cdots
$$

**Distance from the origin to the boundary:**

$$
d(0,\, \partial f(\mathbb{D})) = \min_t |f(e^{it})| \geq \frac{1}{4}
$$

by the Koebe 1/4-theorem. A crude triangle-inequality bound gives:

$$
d(0,\, \partial f(\mathbb{D})) \geq 1 - |a_2| - |a_3| - \cdots
$$

**Area of $f(\mathbb{D})$:**

$$
\text{Area}(f(\mathbb{D})) = \pi \sum_{n=1}^{\infty} n|a_n|^2 \geq \pi
$$

since $a_1 = 1$. This is a consequence of the area theorem and provides a lower bound on the "size" of the image domain.

---

## (b) De Branges bounds (formerly the Bieberbach conjecture)

By the de Branges theorem (1985):

$$
|a_n| \leq n \quad \text{for all } n \geq 2.
$$

Equality holds if and only if $f$ is a rotation of the Koebe function $k(z) = z/(1-z)^2$.

**Truncated polynomial model.** Fix $N$ and consider:

$$
f(z) = z + \sum_{n=2}^{N} a_n z^n
$$

The constraint set is:
- $|a_n| \leq n$ for each $n = 2, \ldots, N$ (de Branges bounds),
- $f$ is univalent on $\mathbb{D}$ (this is the hard constraint).

The de Branges bounds define a compact convex polytope in coefficient space, but univalence carves out a complicated subset.

---

## (c) Optimization formulation

For truncated polynomials $f(z) = z + \sum_{n=2}^{N} a_n z^n$ with real coefficients:

**Objective:** Minimize $B_f$ (the inradius of $f(\mathbb{D})$).

**Constraints:**
1. $|a_n| \leq n$ for all $n = 2, \ldots, N$ (coefficient bounds).
2. $f$ univalent on $\mathbb{D}$. Sufficient conditions include:
   - **Starlike condition:** $\sum_{k=2}^{N} k|a_k| \leq 1$ (very restrictive but guarantees starlikeness, hence univalence).
   - **Critical point condition:** $f'(z) \neq 0$ for all $|z| < 1$, verified by checking that no root of the polynomial $f'(z) = 1 + \sum_{n=2}^{N} n a_n z^{n-1}$ lies inside $\mathbb{D}$.
3. $f'(0) = 1$ (automatic from the normalization $a_1 = 1$).

**Numerical approach:**
- Use `scipy.optimize.differential_evolution` with bounds $a_n \in [-n, n]$.
- Penalize non-univalent functions heavily in the objective.
- Approximate $B_f$ by boundary sampling: evaluate $f(re^{it})$ for $r = 0.999$ and $t \in [0, 2\pi]$ with ~5000 points, then compute the maximum inscribed disk radius.

---

## (d) Numerical bound and comparison

**Known results:**
| Source | Bound |
|--------|-------|
| Skinner (1994) | $B_f \leq 0.5708858$ |
| Carroll & Ortega-Cerda (2009) | $B_f \leq 0.6564$ |
| Koebe function | $B_{\text{Koebe}} = 1/4 = 0.25$ (minimum inradius) |

**This approach:** The coefficient optimization yields a numerical upper bound $B_u$ on the maximum inradius achievable within the truncated polynomial class. As $N$ increases, the bound should approach the true supremum over $S$.

Key observations:
- For small $N$, the truncation severely limits the function class, and $B_u$ will underestimate the true value.
- The starlike sufficient condition is too restrictive; the critical-point method captures more of the univalent class.
- As $N \to \infty$, the truncated polynomials are dense in $S$ (in the topology of locally uniform convergence), so the bounds should converge.

**Results** are reported in `coefficient_results.json` after running the optimization script `coefficient_optimization.py`.
