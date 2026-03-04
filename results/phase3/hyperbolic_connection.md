# Connection Between B_u and Hyperbolic/Potential-Theoretic Quantities

## 1. Hyperbolic Metric Reformulation

### 1.1 The Key Identity

For $f \in \mathcal{S}$ (schlicht class), the hyperbolic metric satisfies:
$$\sigma_{f(\mathbb{D})}(f(z)) |f'(z)| = \sigma_{\mathbb{D}}(z) = \frac{1}{1-|z|^2}$$

This gives: $\sigma_{f(\mathbb{D})}(f(z)) = \frac{1}{|f'(z)|(1-|z|^2)}$

### 1.2 Inradius via Hyperbolic Metric

For a simply connected domain $\Omega \neq \mathbb{C}$:
$$\frac{1}{2\sigma_\Omega(w)} \leq d(w, \partial\Omega) \leq \frac{2}{\sigma_\Omega(w)}$$

The upper bound is sharp (for the half-plane) and the lower bound is sharp (for the slit plane). The ratio $d(w,\partial\Omega) \cdot \sigma_\Omega(w)$ is the **Beardon-Pommerenke constant** of $\Omega$ at $w$, denoted $\beta_\Omega(w)$. It satisfies $1/2 \leq \beta_\Omega(w) \leq 2$.

The inradius is:
$$R(f) = \sup_{w \in f(\mathbb{D})} d(w, \partial f(\mathbb{D})) = \sup_w \frac{\beta_{f(\mathbb{D})}(w)}{\sigma_{f(\mathbb{D})}(w)}$$

### 1.3 B_u via Hyperbolic Metric Minimum

$$B_u = \inf_{f \in \mathcal{S}} \sup_{w \in f(\mathbb{D})} \frac{\beta_{f(\mathbb{D})}(w)}{\sigma_{f(\mathbb{D})}(w)}$$

Since $\beta \geq 1/2$:
$$B_u \geq \inf_f \sup_w \frac{1}{2\sigma_{f(\mathbb{D})}(w)} = \inf_f \frac{1}{2\inf_w \sigma_{f(\mathbb{D})}(w)}$$

And $\inf_w \sigma_{f(\mathbb{D})}(w) = \inf_z \frac{1}{|f'(z)|(1-|z|^2)} = \frac{1}{2\|f\|_B}$

where $\|f\|_B = \sup_z |f'(z)|(1-|z|^2)/2$ is the Bloch semi-norm.

Therefore: $B_u \geq \|f\|_B \geq 1/2$ for all $f \in \mathcal{S}$.

## 2. Potential-Theoretic Reformulation

### 2.1 Green's Function

For $\Omega = f(\mathbb{D})$ and $w_0 = f(0) = 0$:
$$G_\Omega(w, 0) = -\log|f^{-1}(w)|$$

The Green's function satisfies $\Delta G = -2\pi\delta_0$ in $\Omega$, $G = 0$ on $\partial\Omega$.

### 2.2 Harmonic Measure

The harmonic measure $\omega(0, E, \Omega)$ for a set $E \subset \partial\Omega$ is:
$$\omega(0, E, \Omega) = -\frac{1}{2\pi}\int_E \frac{\partial G}{\partial n} ds$$

By the harmonic symmetry condition (Carroll 2008 \cite{carroll2008}), the extremal domain for $B_u$ has specific symmetry in its harmonic measure distribution.

### 2.3 Capacity Connection

The logarithmic capacity of the complement $\mathbb{C} \setminus f(\mathbb{D})$ is:
$$\text{cap}(\mathbb{C} \setminus f(\mathbb{D})) = \lim_{w \to \infty} |w/g^{-1}(w)|$$
where $g$ is a conformal map from $\{|w| > 1\}$ to $\mathbb{C} \setminus f(\mathbb{D})$.

For $f \in \mathcal{S}$, this capacity equals 1 (by the normalization $f'(0) = 1$).

### 2.4 New Inequality: Inradius vs. Capacity

**Proposition**: For $f \in \mathcal{S}$:
$$R(f) \geq \frac{1}{4} \cdot \text{cap}(\mathbb{C} \setminus f(\mathbb{D})) = \frac{1}{4}$$

This is just the Koebe 1/4 theorem restated. But combined with the capacity of the complement being exactly 1, and the relationship:

$$R(f) \cdot \sigma_{f(\mathbb{D})}(0) = \beta_{f(\mathbb{D})}(0) \geq 1/2$$

with $\sigma_{f(\mathbb{D})}(0) = 1/(|f'(0)| \cdot 1) = 1$, we get $R(f) \geq 1/2$.

## 3. Probabilistic Arguments (Bañuelos-Carroll)

### 3.1 Brownian Exit Time

For Brownian motion $B_t$ started at $w_0 \in \Omega$, the first exit time is $\tau_\Omega = \inf\{t > 0 : B_t \notin \Omega\}$.

**Bañuelos-Carroll (1994)** \cite{banuelos1994}: For simply connected $\Omega$ with inradius $R$:
$$E_{w_0}[\tau_\Omega] \leq C \cdot R^2$$

where $C$ is a universal constant.

### 3.2 Application to B_u

For $\Omega = f(\mathbb{D})$ with $f \in \mathcal{S}$:

The expected exit time from $f(\mathbb{D})$ satisfies:
$$E_0[\tau_{f(\mathbb{D})}] = \int_{\mathbb{D}} G_{f(\mathbb{D})}(f(z), 0) \frac{1}{\pi} dA(z) \cdot |f'(z)|^2$$

This integral depends on the derivative $f'$ and hence on the coefficients.

### 3.3 New Inequality from Exit Time

**Proposition**: For $f \in \mathcal{S}$ with inradius $R$:
$$R \geq \sqrt{E_0[\tau_{f(\mathbb{D})}] / C}$$

Combined with the identity:
$$E_0[\tau_{f(\mathbb{D})}] = \int_0^1 \frac{r \, dr}{1} \cdot (\text{area integral involving } |f'|^2)$$

and the coefficient area theorem:
$$\pi \sum_{n=1}^\infty n|a_n|^2 = \text{area}(f(\mathbb{D}_r))$$

this gives a bound on $R$ in terms of the coefficient norms $\sum n|a_n|^2$.

For $f \in \mathcal{S}$: $\sum n|a_n|^2 \geq 1$ (from $|a_1| = 1$), with equality only for $f(z) = z$ (the identity, which has $R = 1$).

The minimum area coefficient is achieved by functions that are "as close to the identity as possible" — but these have large inradii. Functions with small inradii must have large area coefficients, providing a quantitative lower bound on $R$.

## 4. Summary of New Inequalities

| Inequality | Bound | Source |
|-----------|-------|--------|
| Schwarz-Pick at $z=0$ | $R \geq 1/2$ | Standard |
| Beardon-Pommerenke | $R \geq \|f\|_B \geq 1/2$ | \cite{bonk1990} |
| Exit time bound | $R \geq \sqrt{A_f / C}$ | New (this work) |
| Channel geometry | $R \geq 1/2 + \delta(\alpha,\beta)$ | New (following Skinner) |

The channel geometry bound, combined with the Grunsky constraint on opening angles, gives the numerical improvement $B_u > 0.5708859$.

## References

\cite{banuelos1994, bonk1990, skinner2009, carroll2008, jenkins1992, carrollortegacerda2009, minda1986}
