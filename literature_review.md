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

## Design Choice for This Project

For a minimal gravity simulation, we implement:
1. **Direct summation** as the baseline (exact reference)
2. **Barnes-Hut quadtree** as the primary approximate method (good balance of complexity and accuracy)
3. Both loop-based and NumPy-vectorized versions of direct summation for performance comparison
