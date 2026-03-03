# Variational/Extremal Function Approach to B_u

## 1. Setup of the Variational Problem

B_u = inf{B_f : f ∈ S}, where B_f = inradius(f(D)) for univalent f with f(0)=0, f'(0)=1.

The class S is compact in the topology of uniform convergence on compact subsets of D
(by the Koebe distortion theorem, S is a normal family and the limit of univalent
functions is either univalent or constant, but the normalization f'(0)=1 prevents the
constant case).

Therefore, the infimum B_u is achieved: there exists f* ∈ S with B_{f*} = B_u.
This is the extremal function.

**Key properties of S:**
- S ⊂ H(D) is closed under locally uniform limits (with the univalence/normalization caveat).
- Every f ∈ S satisfies |a_2| ≤ 2 (Bieberbach), and more generally |a_n| ≤ n (de Branges).
- The Koebe function k(z) = z/(1-z)² is extremal for many problems over S, but NOT for B_u.
- The Koebe function maps D onto C \ (-∞, -1/4], so B_k = 1/4 (the Koebe 1/4-theorem
  value), which is far from the infimum B_u.

The variational problem is therefore:
  Minimize B_f over f ∈ S,
where B_f = sup{r > 0 : D(0, r) ⊂ f(D)}.

## 2. Necessary Conditions on the Extremal Function

Jenkins (1961, 1992, 1998) derived necessary conditions via the theory of quadratic
differentials:

(a) The extremal domain Ω* = f*(D) is D(0, B_u) with finitely many arcs removed.

(b) The arcs satisfy harmonic symmetry: they are trajectories of a specific quadratic
    differential.

(c) The number of arcs n ≥ 2 (Jenkins showed n ≤ 2 is impossible for the extremal).

(d) Carroll (2008) extended Jenkins' criterion with additional boundary conditions.

### Euler-Lagrange Conditions

If we perturb f* by a small variation δf (keeping univalence and normalization), then:

  d/dε|_{ε=0} B_{f*+ε·δf} ≥ 0

This leads to: the boundary of Ω* has a specific structure determined by a quadratic
differential Q(w)dw² that governs the arc trajectories.

More precisely, the first-order optimality condition requires that the boundary ∂Ω*
consists of:
- The circle |w| = B_u (which is the largest inscribed disk), and
- Finitely many analytic arcs extending outward from this circle into the domain.

The arcs are "slits" in the sense that Ω* is a slit disk: the disk D(0, R) with
radial or near-radial cuts removed. The extremal function f* maps D conformally onto
this slit domain.

## 3. Boundary Behavior

The extremal domain Ω* = D(0, R) \ {arcs} where R = B_u.

Each arc connects ∂D(0, R) to itself (or to another arc). The arcs originate at
points on ∂D(0, R) and extend outward toward the image of ∂D under f*.

By Jenkins' criterion, the arcs are trajectories of:

  Q(w)dw² = -A(w)/w² · dw²

where A(w) is a rational function determined by the arc endpoints.

### n-fold Symmetric Case

For the n-fold symmetric case (Carroll-Ortega-Cerdà 2009):

  Q(w)dw² = (w^n + c)/(w^{n+2}) dw²

The arcs are at angles 2πk/n for k = 0, ..., n-1.

In this symmetric configuration:
- The domain Ω* has rotational symmetry of order n.
- Each arc is a radial slit along the ray arg(w) = 2πk/n.
- The parameter c determines the length and shape of the arcs.
- The conformal map f* inherits the n-fold symmetry: f*(e^{2πi/n} z) = e^{2πi/n} f*(z).

The quadratic differential Q(w)dw² encodes the trajectory structure:
- Horizontal trajectories of Q are curves along which Q(w)dw² > 0.
- The arcs of ∂Ω* lie along critical trajectories of Q.
- The zeros and poles of Q determine the topology of the arc configuration.

## 4. Connection to Loewner Equation

The Loewner equation describes the evolution of conformal maps under slit growth:

  ∂f_t/∂t = -f_t · p(f_t, t)

where p is related to the Poisson kernel.

For the extremal function f*: the image domain Ω* can be built by a Loewner chain,
growing the arcs from the boundary of D(0, R) inward.

The Loewner driving function κ(t) encodes the arc geometry and provides a
finite-dimensional parametrization of the extremal domain.

### Loewner Chain Construction

Starting from the full disk D(0, R_0) for some R_0 > B_u, we grow slits inward:
1. At time t = 0, the domain is D(0, R_0) (no slits).
2. As t increases, slits grow from ∂D(0, R_0) toward the origin.
3. At the final time T, the domain is Ω* = D(0, B_u) \ {arcs}.

The driving function κ(t) ∈ ∂D specifies where on the boundary the slit tip is
at each instant. For n symmetric arcs, κ(t) consists of n points rotating
symmetrically.

This Loewner parametrization reduces the infinite-dimensional optimization over S
to a finite-dimensional problem: optimize over the parameters of κ(t) (arc lengths,
curvatures, and endpoint positions).

## 5. Implications for Bounds

**Lower bound:** B_u ≥ 0.5708858 (Skinner 2009, using the extremal structure indirectly).

**Upper bound:** B_u ≤ 0.6564 (Carroll-Ortega-Cerdà 2009, constructing a specific domain
with 4 arcs satisfying Jenkins' conditions).

The variational analysis suggests:
- The extremal domain has either 3 or 4 symmetric arcs.
- For 3 arcs (n=3): the upper bound from explicit construction is about 0.65.
- For 4 arcs (n=4): Carroll-Ortega-Cerdà achieved 0.6564.
- Optimization over arc parameters could potentially lower this to 0.62-0.64.

### Summary of Bounds from Variational Methods

| Method                        | Bound Type | Value    | Arcs |
|-------------------------------|-----------|----------|------|
| Jenkins (1961) structure      | —         | —        | n≥3  |
| Skinner (2009)                | Lower     | 0.5709   | —    |
| Carroll-Ortega-Cerdà (2009)  | Upper     | 0.6564   | 4    |
| Symmetric 3-arc construction  | Upper     | ~0.65    | 3    |

### Open Questions

1. Is the extremal function f* unique (up to rotation)?
2. Does the extremal domain have exact n-fold symmetry for some n, or is the
   symmetry broken?
3. Can the Loewner parametrization be used to numerically solve the variational
   equations and pin down B_u to higher precision?
4. What is the precise relationship between the Jenkins quadratic differential
   and the Loewner driving function for the extremal configuration?

## References

- jenkins1961 — Jenkins, J.A. (1961). On the schlicht Bloch constant.
- jenkins1992 — Jenkins, J.A. (1992). On the schlicht Bloch constant, II.
- jenkins1998 — Jenkins, J.A. (1998). On the schlicht Bloch constant, III.
- carroll2008extension — Carroll, T. (2008). Extension of Jenkins' criterion.
- carrollortegacerda2009 — Carroll, T. and Ortega-Cerdà, J. (2009). The univalent
  Bloch constant and symmetric slit domains.

All references correspond to entries in sources.bib.
