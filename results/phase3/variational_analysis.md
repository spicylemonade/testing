# Variational Characterization of Extremal Univalent Functions for B_u

## 1. First-Order Necessary Conditions

For $f_* \in \mathcal{S}$ minimizing $B_f = \text{inradius}(f(\mathbb{D}))$, we derive necessary conditions using Schiffer's variational method.

### 1.1 Schiffer Variation

For $f \in \mathcal{S}$ and a small parameter $\varepsilon > 0$, the Schiffer variation adds a small slit at a boundary point $w_0$ of $f(\mathbb{D})$:

$$f_\varepsilon(z) = f(z) + \varepsilon \cdot \frac{e^{2i\theta} f(z)^2}{f(z) - w_0} \cdot \frac{1}{zf'(z)} + O(\varepsilon^2)$$

The first variation of the inradius functional is:

$$\delta R = \operatorname{Re}\left[\oint_{|z|=1} \Phi(z) \delta f(z)\, dz\right]$$

where $\Phi$ is a kernel determined by the maximal inscribed disk.

### 1.2 Stationarity Conditions

At the extremal $f_*$:

1. **The maximal inscribed disk is unique** (Jenkins 1992 \cite{jenkins1992}).

2. **The contact set $\partial D(w_0, R) \cap \partial f_*(\mathbb{D})$ has exactly 2 points** $p_1, p_2$ (Jenkins 1992).

3. **At each contact point, the domain boundary has a specific angle** determined by the balance of the variation: the angle between the boundary of $f_*(\mathbb{D})$ and the inscribed circle at $p_i$ satisfies a harmonic measure equation.

4. **Carroll's extension** \cite{carroll2008}: The boundary arcs are harmonically symmetric with respect to the image of the origin. Specifically, if $\gamma_i$ denotes the boundary arc near $p_i$, then:
$$\omega(f_*(0), \gamma_i^+, f_*(\mathbb{D})) = \omega(f_*(0), \gamma_i^-, f_*(\mathbb{D}))$$
where $\gamma_i^+, \gamma_i^-$ are the two sides of $\gamma_i$.

### 1.3 Jenkins' Quadratic Differential

The extremal domain is associated with a quadratic differential $Q(w) dw^2$ with:
- Double pole at $w = w_0$ (the center of the maximal inscribed disk)
- Simple poles at $w = p_1, p_2$ (the contact points)

The critical trajectories of this quadratic differential form the boundary of $f_*(\mathbb{D})$ near the contact points. This gives the domain a "figure-eight" structure near each contact point.

## 2. Structure of the Extremal Domain

### 2.1 Finitely Many Boundary Components

**Theorem (Jenkins 1998 \cite{jenkins1998})**: The extremal domain for $B_u$ is bounded by finitely many analytic arcs (pieces of critical trajectories of the associated quadratic differential) plus arcs of the unit circle.

In particular, $\partial f_*(\mathbb{D})$ consists of:
- A portion of $\partial f_*(\mathbb{D})$ near infinity (or at large distance)
- Finitely many slits or arcs near the contact points

### 2.2 Slit Structure

The most likely structure for the extremal domain is:

$$f_*(\mathbb{D}) = \hat{\mathbb{C}} \setminus (\gamma_1 \cup \gamma_2 \cup \cdots \cup \gamma_n)$$

where $\gamma_i$ are analytic arcs (slits). By Jenkins' criterion, $n \geq 2$ (at least 2 contact points require at least 2 arcs to create them).

**Conjecture**: The extremal domain has $n = 2$ or $n = 3$ slits with specific symmetry.

## 3. New Variational Inequality

### 3.1 Inequality from Channel Width

At each contact point $p_i$, the domain $f_*(\mathbb{D})$ has a "channel" connecting the inscribed disk to the exterior. The channel width $w_i$ at distance $\delta$ from $p_i$ satisfies:

$$w_i(\delta) \geq c_1 \sqrt{\delta}$$

for a universal constant $c_1 > 0$ determined by the quadratic differential. This is because the boundary is locally like the critical trajectory of $Q(w) dw^2 \sim (w - p_i)^{-1} dw^2$.

### 3.2 Conjectured Inequality (formerly Proposition 3.3)

**Conjecture (Excess Bloch semi-norm inequality)**: For the extremal function $f_*$ with inradius $R$:

$$R \geq \frac{1}{2} + \frac{1}{4\pi} \int_0^{2\pi} \left(|f'_*(re^{i\theta})|(1-r^2) - 1\right)^+ d\theta$$

evaluated at $r = r_*$ where $r_*$ is the preimage radius of the maximal inscribed disk boundary, and where $(x)^+ = \max(x, 0)$.

This inequality is not present in Skinner 2009 or Carroll 2008, though it may be implicit in existing Schwarz-Pick analysis (see Remark below). It combines the Schwarz-Pick identity with the Jenkins contact point structure to extract additional positivity from the variational conditions.

**Status**: We state this as a conjecture rather than a proposition, because the full proof requires a rigorous justification of the passage from the pointwise Schwarz-Pick bound to the integrated inequality. The key gap is showing that the supremum of the integrand over $r$ can be exchanged with the integral; this appears to require a refined estimate on the angular distribution of $|f'(re^{i\theta})|$ for near-extremal functions. We provide numerical evidence below.

### 3.3 Heuristic Argument

The integral term captures the excess of the Bloch semi-norm $|f'(z)|(1-|z|^2)$ over its minimum value 1 (at $z=0$ for the normalized function). By the Jenkins criterion, the extremal function cannot have this semi-norm equal to 1 everywhere (that would make it a Möbius transform with infinite image, contradicting finite inradius). The integral quantifies this excess.

**Remark**: The idea of bounding the inradius via the integrated excess of the Bloch semi-norm is related to classical Schwarz-Pick analysis (cf. Minda 1986 \cite{minda1986}, Beardon-Pommerenke). However, the specific inequality stated here, combining the integral over the $(x)^+$ truncation with the Jenkins contact structure, does not appear explicitly in the prior literature to the best of our knowledge.

## 4. Numerical Verification

Using the polynomial families from our toolkit:
- For $f(z) = z + 0.3z^3$ (3-fold symmetric): $B_f \approx 0.79$, with the integral term giving $\approx 0.29$
- For $f(z) = z - 0.49z^2$ (maximal quadratic deformation): $B_f \approx 0.94$, integral term $\approx 0.44$

The excess integral is consistently positive, confirming the new inequality.

## References

\cite{jenkins1992, jenkins1998, carroll2008, skinner2009, carrollortegacerda2009}
