# Literature Review: N-Body Gravitational Simulation Methods

## 1. Direct Summation (Brute Force) — O(N²)

The most straightforward approach computes gravitational force on each particle by summing contributions from all other particles. For N particles, this requires N(N-1)/2 pairwise interactions per timestep.

**Key reference:** Aarseth (2003) "Gravitational N-Body Simulations" — the definitive reference for direct N-body methods. Aarseth's NBODY series (NBODY1-7) pioneered regularization techniques for close encounters and individual timesteps.

**Complexity:** O(N²) per timestep
**Pros:** Exact (to machine precision), simple to implement, handles close encounters naturally
**Cons:** Prohibitively expensive for N > 10⁴, no approximation error
**Best for:** Small N (star clusters), collisional systems where close encounters matter

## 2. Barnes-Hut Tree Algorithm — O(N log N)

Barnes & Hut (1986) introduced a hierarchical octree (3D) / quadtree (2D) decomposition. Distant groups of particles are approximated as single point masses when the opening angle θ = s/d < threshold, where s is cell width and d is distance to cell center of mass.

**Key reference:** Barnes, J. & Hut, P. (1986) "A hierarchical O(N log N) force-calculation algorithm." Nature, 324, 446-449.

**Complexity:** O(N log N) per timestep
**θ parameter:** Controls accuracy vs. speed tradeoff. θ=0 degenerates to direct summation. Typical values: 0.3-0.7.
**Pros:** Dramatic speedup over direct summation, relatively simple to implement, good for moderately concentrated distributions
**Cons:** Does not conserve momentum exactly, accuracy depends on θ, tree construction overhead
**Best for:** N ~ 10³–10⁶, collisionless systems (galaxies)

## 3. Fast Multipole Method (FMM) — O(N)

Greengard & Rokhlin (1987) achieved linear O(N) complexity by using multipole and local (Taylor) expansions. Far-field effects are computed via cell-cell interactions with controlled error bounds.

**Key reference:** Greengard, L. & Rokhlin, V. (1987) "A fast algorithm for particle simulations." J. Comput. Phys., 73, 325-348.

**Complexity:** O(N) per timestep (for fixed precision)
**Pros:** Asymptotically optimal, controlled error bounds, rigorous mathematical foundation
**Cons:** More complex to implement, higher constant factor for small N, level-by-level nature less efficient for concentrated distributions
**Best for:** Very large N (>10⁶), uniform or mildly clustered distributions

## 4. Dehnen's Hybrid Algorithm — O(N)

Dehnen (2002) combined advantages of Barnes-Hut (specific low-precision expansions) with FMM (cell-cell interactions) to produce a practical O(N) algorithm for astrophysics. Implemented as falcON.

**Key reference:** Dehnen, W. (2002) "A Hierarchical O(N) Force Calculation Algorithm." J. Comput. Phys., 179, 27-42.

**Complexity:** O(N) empirically for N > 10⁴
**Pros:** Fastest in practice for astrophysical problems, conserves momentum, less sensitive to concentration
**Cons:** Complex implementation, optimized for softened gravity

## 5. GADGET-2: Production N-Body Code

Springel (2005) developed GADGET-2, a massively parallel TreeSPH code combining Barnes-Hut tree gravity with smoothed particle hydrodynamics. Widely used for cosmological simulations.

**Key reference:** Springel, V. (2005) "The cosmological simulation code GADGET-2." MNRAS, 364, 1105-1134.

## Complexity Comparison

| Method | Time Complexity | Space Complexity | Accuracy |
|--------|---------------|-----------------|----------|
| Direct Summation | O(N²) | O(N) | Exact |
| Barnes-Hut | O(N log N) | O(N) | Approximate (θ-dependent) |
| FMM | O(N) | O(N) | Approximate (p-dependent) |
| Dehnen | O(N) | O(N) | Approximate |

---

# Numerical Integration Schemes for Orbital Mechanics

## 6. Forward Euler — 1st Order

The simplest explicit integrator: x(t+dt) = x(t) + v(t)*dt, v(t+dt) = v(t) + a(t)*dt.

**Order:** 1st order — error O(dt)
**Symplectic:** No
**Energy conservation:** Poor — energy drifts secularly (typically grows), making it unsuitable for long integrations
**Use case:** Educational baseline; demonstrates why higher-order methods are needed

## 7. Leapfrog / Velocity-Verlet / Størmer-Verlet — 2nd Order

The leapfrog method staggers position and velocity updates. The velocity-Verlet variant computes both at the same timestep:
1. v(t + dt/2) = v(t) + a(t)*dt/2  (half kick)
2. x(t + dt) = x(t) + v(t + dt/2)*dt  (drift)
3. a(t + dt) = F(x(t + dt))/m  (force evaluation)
4. v(t + dt) = v(t + dt/2) + a(t + dt)*dt/2  (half kick)

**Key references:**
- Verlet, L. (1967) "Computer Experiments on Classical Fluids." Phys. Rev., 159, 98.
- Hairer, Lubich & Wanner (2006) "Geometric Numerical Integration" — comprehensive treatment of symplectic methods.

**Order:** 2nd order — error O(dt²)
**Symplectic:** Yes — preserves phase-space volume
**Energy conservation:** Excellent — energy oscillates around true value with bounded error O(dt²), no secular drift
**Time-reversible:** Yes
**Use case:** Workhorse integrator for N-body simulations. Best balance of simplicity, accuracy, and conservation.

## 8. Classical Runge-Kutta (RK4) — 4th Order

The standard 4th-order Runge-Kutta method uses 4 force evaluations per step to achieve 4th-order accuracy.

**Order:** 4th order — error O(dt⁴)
**Symplectic:** No
**Energy conservation:** Better short-term accuracy than leapfrog, but energy drifts secularly over long integrations
**Use case:** General-purpose ODE integration; not ideal for Hamiltonian systems due to lack of symplecticity

## 9. Yoshida 4th-Order Symplectic — 4th Order

Yoshida (1990) showed how to compose 2nd-order symplectic integrators (leapfrog) with specific coefficients to obtain higher-order symplectic methods. The 4th-order scheme uses 3 leapfrog sub-steps with coefficients:
- c₁ = c₄ = 1/(2(2-2^{1/3}))
- c₂ = c₃ = (1-2^{1/3})/(2(2-2^{1/3}))
- d₁ = d₃ = 1/(2-2^{1/3})
- d₂ = -2^{1/3}/(2-2^{1/3})

**Key references:**
- Yoshida, H. (1990) "Construction of higher order symplectic integrators." Phys. Lett. A, 150, 262-268.
- Forest, E. & Ruth, R.D. (1990) "Fourth-order symplectic integration." Physica D, 43, 105-117.

**Order:** 4th order — error O(dt⁴)
**Symplectic:** Yes
**Energy conservation:** Excellent — energy error bounded O(dt⁴), no secular drift. ~100x better than leapfrog at same step count.
**Cost:** 3 force evaluations per step (vs 1 for leapfrog)
**Use case:** High-precision orbital mechanics where long-term conservation matters

## Integrator Comparison

| Method | Order | Symplectic | Force Evals/Step | Energy Drift |
|--------|-------|-----------|-----------------|-------------|
| Forward Euler | 1 | No | 1 | Secular (grows) |
| Leapfrog/Verlet | 2 | Yes | 1 | Bounded O(dt²) |
| RK4 | 4 | No | 4 | Secular (slow) |
| Yoshida 4th | 4 | Yes | 3 | Bounded O(dt⁴) |

## Design Choice for This Project

**Force algorithms:** We implement direct summation (exact baseline), NumPy-vectorized direct summation (performance), and Barnes-Hut quadtree (approximate, scalable).

**Integrators:** We implement forward Euler (baseline), velocity-Verlet/leapfrog (workhorse), and Yoshida 4th-order (high-precision). This covers 1st, 2nd, and 4th order, both symplectic and non-symplectic.
