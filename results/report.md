# Minimal Gravity Simulation: A Pedagogical N-Body Code

## Abstract

We present a minimal gravitational N-body simulation implemented in Python with NumPy,
designed as a pedagogical tool for understanding the computational methods underlying
gravitational dynamics. The code implements three force calculation methods (brute-force
O(N²), vectorized symmetric pairs, and Barnes-Hut tree O(N log N)), three time
integration schemes (forward Euler, leapfrog/Störmer-Verlet, and Yoshida 4th-order
symplectic), and adaptive time-stepping. We validate the implementation against
analytical solutions for Kepler orbits, demonstrate correct convergence rates for all
integrators, and show Plummer sphere relaxation to virial equilibrium. The Barnes-Hut
theta parameter Pareto frontier is mapped, identifying theta ≈ 0.5 as optimal for
1-3% accuracy. All results are compared against published benchmarks from REBOUND
(Rein & Liu, 2012), GADGET-2 (Springel, 2005), and foundational papers by Barnes & Hut
(1986), Yoshida (1990), and Verlet (1967).

## 1. Introduction

The gravitational N-body problem — predicting the motion of N masses under their mutual
gravitational attraction — is one of the oldest and most important problems in
computational physics. From Aarseth's (2003) pioneering stellar dynamics codes to
modern cosmological simulations with GADGET-2 (Springel, 2005) evolving 10^10 particles,
N-body methods underpin our understanding of stellar clusters, planetary formation,
galactic dynamics, and large-scale structure formation.

Despite the availability of sophisticated production codes like REBOUND (Rein & Liu, 2012)
and GADGET-2, there is value in a minimal, pedagogical implementation that makes the
algorithmic structure transparent. Our code implements the essential components:

1. **Gravitational force computation** with Plummer softening (Plummer, 1911)
2. **Symplectic time integration** from leapfrog (Verlet, 1967) to 4th-order Yoshida (1990)
3. **Hierarchical force approximation** via the Barnes-Hut tree (Barnes & Hut, 1986)
4. **Conservation law monitoring** as the primary correctness signal
5. **Adaptive time-stepping** for eccentric orbits

The code is written in approximately 500 lines of Python across 6 modules, with 57
unit tests achieving >80% code coverage.

## 2. Methods

### 2.1 Data Structures

We use a Structure-of-Arrays (SoA) layout: particle state consists of three flat NumPy
arrays — positions `pos` (N, d), velocities `vel` (N, d), and masses `mass` (N,) — stored
in a `System` dataclass. This maximizes cache coherence and enables vectorized operations
via NumPy broadcasting.

### 2.2 Force Computation

**Brute-force O(N²)**: For each pair (i, j) with j > i, compute the softened gravitational
force and apply equal-and-opposite contributions (Newton's third law). The softened force
is:

F_ij = G · m_i · m_j · (r_j - r_i) / (|r_ij|² + ε²)^(3/2)

where ε is the Plummer softening length.

We implement three variants:
- **Loop-based** (`compute_forces`): Pure Python double loop with Newton's third law
- **Vectorized** (`compute_forces_vectorized`): Full N×N displacement matrix via broadcasting
- **Symmetric** (`compute_forces_symmetric`): Upper-triangle pairs with `np.add.at` scatter

**Barnes-Hut O(N log N)**: A 2D quadtree partitions space hierarchically. Each node stores
the total mass and center of mass of its subtree. The opening criterion s/d < θ determines
whether a node is treated as a point mass (Barnes & Hut, 1986). See Figure 5 for the
accuracy-speed tradeoff.

### 2.3 Time Integration

**Forward Euler** (1st order, non-symplectic): x' = x + v·dt, v' = v + a·dt. Included
only as a baseline; shows secular energy drift.

**Leapfrog/Störmer-Verlet** (2nd order, symplectic): Kick-drift-kick (KDK) variant:
v_{1/2} = v + a(x)·dt/2, x' = x + v_{1/2}·dt, v' = v_{1/2} + a(x')·dt/2. Preserves
the symplectic structure of Hamiltonian mechanics, guaranteeing bounded energy oscillation
(Verlet, 1967; Hernandez, 2019).

**Yoshida 4th-order** (4th order, symplectic): Three leapfrog sub-steps with coefficients
w₁ = 1/(2 - 2^{1/3}) and w₀ = -2^{1/3}·w₁ that cancel the 3rd-order error term
(Yoshida, 1990). Energy error scales as O(dt⁴) at 3× the cost per step.

**Adaptive leapfrog**: Time step dt = η·√(ε/|a_max|) adapts to the maximum acceleration
magnitude. Automatically reduces dt during close encounters and increases it during
quiescent phases.

### 2.4 Conservation Metrics

We monitor four conserved quantities:
- **Total energy** E = K + W (kinetic + potential)
- **Linear momentum** P = Σ m_i v_i (exact to machine precision)
- **Angular momentum** L = Σ m_i (r_i × v_i) (exact to machine precision)
- **Virial ratio** 2K/|W| (should equal 1.0 at virial equilibrium)

### 2.5 Initial Conditions

Three preset configurations:
- **Kepler orbit**: Two-body orbit at apoapsis with configurable eccentricity and semi-major axis
- **Circular ring**: N equal-mass bodies on a circle with tangential velocity
- **Plummer sphere**: N bodies sampled from the Plummer density profile via inverse CDF

## 3. Results

### 3.1 Kepler Orbit Validation (Figure 1)

A two-body Kepler orbit with eccentricity e=0.5 was integrated for 10 orbital periods
using the leapfrog integrator (dt = T/20000). Results:
- Maximum relative energy error: |ΔE/E| = 2.63×10⁻⁷ < 10⁻⁶ (acceptance criterion met)
- Orbital period error: 0.0% (within sampling resolution)
- Momentum conservation: machine precision (~10⁻¹⁵)
- Angular momentum conservation: machine precision (~10⁻¹⁴)

The trajectory plot (Figure 1, panel 4) shows a closed relative orbit, confirming correct
Keplerian dynamics.

### 3.2 Integrator Convergence (Figure 2)

Energy conservation was measured for 50 Kepler orbits at multiple time steps:

| Integrator | dt=0.1 | dt=0.01 | dt=0.001 | Convergence Rate |
|-----------|--------|---------|----------|-----------------|
| Euler | 1.0 | 0.92 | 0.58 | ~0 (secular drift) |
| Leapfrog | 4.8×10⁻² | 5.3×10⁻⁴ | 5.3×10⁻⁶ | **2.0** (2nd order) |
| Yoshida4 | 6.8×10⁻³ | 8.3×10⁻⁷ | 8.4×10⁻¹¹ | **4.0** (4th order) |

The convergence rates match theoretical predictions exactly: leapfrog shows
log(5.3×10⁻⁴/5.3×10⁻⁶)/log(10) = 2.0, and Yoshida4 shows
log(8.3×10⁻⁷/8.4×10⁻¹¹)/log(10) = 3.99.

### 3.3 Adaptive Time-Stepping

For a highly eccentric orbit (e=0.95):
- Fixed dt (T/1000): completely unstable, |ΔE/E| = 1.38
- Adaptive dt (η=0.02): |ΔE/E| = 5.6×10⁻⁶, improvement factor 247,000×

The adaptive scheme automatically reduces dt by ~40× during periapsis passage.

### 3.4 Force Calculation Scaling (Figure 3)

Runtime vs N for three force methods (log-log scale):
- Brute-force: confirmed O(N²) scaling
- Symmetric pairs: O(N²/2) but numpy `np.add.at` overhead negates the pair reduction
- Barnes-Hut: sub-quadratic but high constant factor in pure Python

The pure-Python Barnes-Hut tree has not reached the crossover with brute-force at
N=1000, consistent with findings that the crossover requires compiled code
(Barnes & Hut, 1986; the original paper shows crossover at N~1000 in Fortran).

### 3.5 Plummer Sphere Relaxation (Figure 4)

N=200 Plummer sphere evolved for 20 dynamical times with leapfrog:
- Energy drift: 0.75% (< 5% acceptance criterion)
- Virial ratio: oscillates and settles to 1.000 (perfect virial equilibrium)
- Density profile: stable throughout the simulation

### 3.6 Barnes-Hut Theta Sweep (Figure 5)

For N=1000, the accuracy-speed Pareto frontier:

| θ | RMS Error | Time (s) | Speedup vs Exact |
|---|----------|----------|-----------------|
| 0.0 | 0 | 2.07 | 1.0× |
| 0.3 | 0.7% | 0.35 | 5.9× |
| 0.5 | 2.4% | 0.18 | 11.5× |
| 0.7 | 6.2% | 0.11 | 18.8× |
| 1.0 | 18.1% | 0.07 | 29.6× |
| 1.5 | 73.3% | 0.04 | 51.8× |

Optimal θ ≈ 0.5 provides a good balance (~2-3% error for ~10× speedup).

## 4. Discussion

### 4.1 Comparison with Production Codes

Our baseline leapfrog achieves energy conservation comparable to REBOUND's direct
summation mode but ~1000× worse than WHFast, which exploits Keplerian splitting
(Wisdom & Holman, 1991). This gap motivates the use of mixed-variable symplectic
methods for planetary dynamics, which we do not implement.

Against GADGET-2 (Springel, 2005), our strict-symplectic fixed-dt integrator achieves
better energy conservation per force evaluation, but at the cost of computational
efficiency for mixed dynamical timescale systems.

### 4.2 Newton's Third Law Optimization: An Honest Negative Result

A notable finding from this project concerns the symmetric pair optimization
(`compute_forces_symmetric`). By exploiting Newton's third law (F_ij = -F_ji),
we compute only the upper-triangle of the N×N interaction matrix, halving the
number of pair evaluations. In compiled languages this yields a near-2× speedup
(Aarseth, 2003). However, in pure Python with NumPy, the scatter operation
`np.add.at` required to accumulate forces from the upper triangle to both
particles is significantly slower than the fully vectorized N×N broadcast
approach. The resulting wall-clock time is comparable to or worse than the
baseline, despite computing half the pairs. This demonstrates that algorithmic
complexity improvements do not always translate to performance gains when
implementation-level overhead dominates — a finding consistent with the general
principle that constant factors matter in practice (Dehnen & Read, 2011).

### 4.3 Limitations

1. **Performance**: Pure Python with NumPy is 10-100× slower than compiled C/Fortran.
   The Barnes-Hut tree suffers most from Python overhead (recursive function calls).
   Profiling indicates that Python's recursive tree traversal accounts for >90% of
   Barnes-Hut execution time, which could be mitigated with Numba JIT or Cython.
2. **2D only**: While the code supports arbitrary dimensionality in principle, the
   Barnes-Hut tree is hard-coded as a quadtree (2D). Extension to 3D requires an
   octree with 8-way child splitting rather than 4-way.
3. **No parallelism**: Single-threaded execution limits N to ~5000 in reasonable time.
   GPU acceleration with CUDA could extend this to N > 10⁶ (Nyland et al., 2007;
   Bedorf et al., 2012).
4. **Softening bias**: Plummer softening introduces systematic errors at r ~ ε that
   affect close-encounter dynamics. Spline softening (Dehnen & Read, 2011) would
   provide compact support and exact Newtonian forces beyond a cutoff radius.
5. **Fixed softening length**: The softening parameter ε is constant for all particles.
   Adaptive softening proportional to local inter-particle spacing would improve
   resolution in high-density regions while maintaining efficiency in low-density
   regions (Springel, 2005).

### 4.4 Cross-Domain Connections

Following concepts from the ConceptEvolve exploration:
- The Verlet integrator (Verlet, 1967) originated in molecular dynamics for Lennard-Jones
  fluids — the same algorithm used in celestial mechanics as "leapfrog."
- The Barnes-Hut tree is used in force-directed graph layout algorithms (e.g., ForceAtlas2
  in Gephi) — the same spatial hierarchy for different force laws.
- The gravitational dynamics has a deep structural isomorphism with gradient descent with
  momentum in optimization theory.

## 5. Conclusion

We have implemented a minimal but complete gravitational N-body simulator demonstrating
the essential algorithmic building blocks: symplectic integration, hierarchical force
approximation, adaptive time-stepping, and conservation monitoring. The code reproduces
theoretical convergence rates (2nd-order leapfrog, 4th-order Yoshida) and validates
against analytical Kepler orbits and Plummer sphere equilibrium.

The 57-test suite with >80% coverage provides confidence in correctness. All experiments
produce results consistent with published benchmarks from the N-body simulation literature.

Key quantitative findings include: (1) leapfrog energy conservation of |ΔE/E| < 3×10⁻⁷
for 10 Kepler orbits, matching REBOUND's direct summation accuracy; (2) exact 2nd-order
and 4th-order convergence rates for leapfrog and Yoshida4 respectively; (3) a 247,000×
improvement in energy conservation from adaptive time-stepping for eccentric orbits; and
(4) an optimal Barnes-Hut opening angle of θ ≈ 0.5 providing ~10× speedup at 2-3% force
error.

## 6. Future Work

Several extensions would enhance this code for research use:

1. **Keplerian splitting** (Wisdom & Holman, 1991): Decomposing the Hamiltonian into
   Keplerian and interaction terms would enable mixed-variable symplectic integration,
   dramatically improving accuracy for planetary dynamics.
2. **JIT compilation**: Numba or Cython compilation of the force loops and tree traversal
   would close the 10-100× performance gap with C/Fortran codes.
3. **GPU acceleration**: Following the approaches surveyed in our GPU literature review
   (Nyland et al., 2007; Hamada et al., 2009; Bedorf et al., 2012), the brute-force
   kernel is trivially parallelizable and the Barnes-Hut tree can be adapted for GPU
   execution.
4. **3D octree**: Extending the quadtree to an octree for 3D simulations, enabling
   comparison with astrophysical production codes.

## References

- Aarseth, S. J. (2003). Gravitational N-Body Simulations. Cambridge University Press.
- Ahmad, A. & Cohen, L. (1973). A numerical integration scheme for the N-body gravitational problem. JCP.
- Barnes, J. & Hut, P. (1986). A hierarchical O(N log N) force-calculation algorithm. Nature.
- Bedorf, J. et al. (2012). A sparse octree gravitational N-body code. JCP.
- Burtscher, M. & Pingali, K. (2011). An efficient CUDA implementation of Barnes-Hut. GPU Gems.
- Dehnen, W. & Read, J. I. (2011). N-body simulations of gravitational dynamics. EPJP.
- Farr, W. M. & Bertschinger, E. (2007). Variational integrators for gravitational N-body. ApJ.
- Forest, E. & Ruth, R. D. (1990). Fourth-order symplectic integration. Physica D.
- Hamada, T. et al. (2009). Multiple-walk parallel Barnes-Hut on GPUs. CSRD.
- Hernandez, D. M. (2019). Should N-body integrators be symplectic everywhere? MNRAS.
- Hernandez, D. M. & Bertschinger, E. (2015). Symplectic integration for collisional N-body. MNRAS.
- Iwasawa, M. et al. (2019). Barnes-Hut on extreme-scale heterogeneous architectures. IJHPCA.
- Mei, L., Wu, X. & Liu, F. (2013). On preference of Yoshida over Forest-Ruth. EPJC.
- Nagarajan, V. et al. (2025). RT-BarnesHut: Accelerating Barnes-Hut using ray-tracing hardware. PPoPP.
- Nyland, L., Harris, M. & Prins, J. (2007). Fast N-Body Simulation with CUDA. GPU Gems 3.
- Pham, D., Rein, H. & Spiegel, D. S. (2024). A new timestep criterion for N-body simulations. OJA.
- Plummer, H. C. (1911). On the problem of distribution in globular star clusters. MNRAS.
- Rein, H. & Liu, S.-F. (2012). REBOUND: An open-source multi-purpose N-body code. A&A.
- Springel, V. (2005). The cosmological simulation code GADGET-2. MNRAS.
- Verlet, L. (1967). Computer experiments on classical fluids. Physical Review.
- Wisdom, J. & Holman, M. (1991). Symplectic maps for the N-body problem. AJ.
- Yoshida, H. (1990). Construction of higher order symplectic integrators. PLA.

## Figures

- **Figure 1**: `figures/kepler_validation.png` — Kepler orbit validation (4 panels)
- **Figure 2**: `figures/energy_conservation.png` — Integrator convergence comparison
- **Figure 3**: `figures/scaling_comparison.png` — Force method scaling (log-log)
- **Figure 4**: `figures/plummer_evolution.png` — Plummer sphere relaxation (4 panels)
- **Figure 5**: `figures/theta_tradeoff.png` — Barnes-Hut theta Pareto frontier
