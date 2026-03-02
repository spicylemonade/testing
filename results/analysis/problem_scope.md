# Problem Scope: Minimal Gravity Simulation

**Date**: 2026-03-02  
**Item**: item_002

## 1. Dimensionality

**Choice: 2D with extensibility to 3D**

We implement in 2D (d=2) for clarity and visualization, with the data structures supporting
arbitrary dimensionality via numpy array shapes `(N, d)`. All physics equations are
dimension-agnostic: `F = -G*m1*m2*(r_j - r_i) / (|r_ij|^2 + eps^2)^(3/2)` works for any d.
The Barnes-Hut tree uses a quadtree for 2D.

**Justification**: 2D allows direct trajectory visualization, simpler tree construction, and
faster experiments while preserving all the algorithmic structure of the 3D case. REBOUND
(Rein & Liu, 2012) supports both 2D and 3D with the same integrator core.

## 2. Particle Count Range

**Target: N=2 to N=5000**

| Regime | N | Use Case |
|--------|---|----------|
| Two-body | 2 | Kepler validation, analytical comparison |
| Few-body | 3-10 | Chaotic dynamics, figure-eight choreography |
| Moderate | 50-500 | Plummer sphere relaxation |
| Large | 1000-5000 | Scaling experiments, Barnes-Hut crossover |

Brute-force O(N^2) is viable up to ~1000 bodies. Barnes-Hut O(N log N) is needed for N > 1000.
GADGET-2 (Springel, 2005) targets N=10^6-10^10 with TreePM; our minimal sim targets the
pedagogical range where algorithmic transitions are visible.

## 3. Gravitational Softening Strategy

**Choice: Plummer softening**

$$F_{ij} = -G \cdot m_i \cdot m_j \cdot \frac{r_j - r_i}{(|r_{ij}|^2 + \epsilon^2)^{3/2}}$$

$$\Phi(r) = -\frac{G \cdot m}{\sqrt{r^2 + \epsilon^2}}$$

The Plummer softening parameter epsilon controls the resolution scale:
- `epsilon = 0` recovers pure Newtonian gravity (singular at r=0)
- `epsilon > 0` regularizes close encounters, making forces finite everywhere
- Recommended: `epsilon ~ 0.01 * mean_interparticle_distance`

**Alternatives considered**:
- Spline softening (used in GADGET-2): more accurate transition but more complex
- No softening: requires regularization techniques for close encounters

**Justification**: Plummer softening is the simplest, most widely used approach. It preserves
the Newtonian 1/r^2 behavior for r >> epsilon while preventing numerical divergence.

## 4. Boundary Conditions

**Choice: Open (vacuum) boundaries**

No periodic boundaries. Particles can escape to infinity. This is the natural choice for:
- Stellar dynamics / cluster simulations
- Pedagogical gravity demonstrations
- Orbit mechanics

**Justification**: Periodic boundaries (used in cosmological simulations like GADGET-2) require
Ewald summation and add significant complexity. Our minimal sim focuses on isolated systems.

## 5. Target Conservation Properties

| Property | Formula | Target Precision |
|----------|---------|-----------------|
| Total energy | E = K + W = Σ½mv² + Σ_{i<j} Φ(r_ij) | |dE/E| < 10^-6 per orbit (leapfrog) |
| Linear momentum | P = Σ m_i v_i | Conserved to machine precision (~10^-15) |
| Angular momentum | L = Σ m_i (r_i × v_i) | Conserved to machine precision (~10^-15) |

Momentum and angular momentum conservation follow from Newton's third law (equal and opposite
forces) and are exact for any consistent force computation. Energy conservation depends on the
integrator: symplectic integrators bound the energy error rather than accumulating secular drift.

## 6. Time-Step Strategy

**Three-tier approach**:

1. **Fixed time-step** (baseline): dt constant throughout simulation
   - Simple, predictable, symplectic
   - Inefficient for eccentric orbits (dt must resolve periapsis)

2. **Global adaptive**: dt = eta * min_i(|v_i|/|a_i|)
   - Automatically resolves close encounters
   - Breaks strict symplecticity

3. **Per-particle block time-steps** (stretch goal): particles on power-of-2 dt schedules
   - Used by GADGET-2 and REBOUND for mixed dynamical timescales
   - Most complex to implement correctly

## 7. Language and Framework Choice

**Choice: Python 3 with NumPy**

| Criterion | Python+NumPy | C/C++ | Julia |
|-----------|-------------|-------|-------|
| Development speed | Excellent | Poor | Good |
| Vectorized performance | Good (via numpy) | Excellent | Excellent |
| Visualization | Excellent (matplotlib) | Poor | Moderate |
| Testing ecosystem | Excellent (pytest) | Moderate | Moderate |
| Accessibility | Excellent | Poor | Moderate |

**Dependencies**:
- `numpy`: vectorized array operations, linear algebra
- `scipy`: special functions, spatial data structures (cKDTree for reference)
- `matplotlib` + `seaborn`: publication-grade plotting
- `pytest` + `pytest-cov`: testing and coverage

**Justification**: Python is the standard for pedagogical scientific computing. NumPy
broadcasting eliminates the need for explicit loops in force computation, giving near-C
performance for vectorized operations. This matches the "minimal" philosophy: minimal code,
maximum clarity, publishable plots.

## 8. Comparison with Existing N-Body Codes

### REBOUND (Rein & Liu, 2012)
- **Language**: C with Python wrapper
- **Integrators**: Leapfrog, WHFast, IAS15, SEI, Mercurius
- **Force methods**: Direct summation, Barnes-Hut tree
- **Key feature**: WHFast uses Wisdom-Holman mapping for planetary systems
- **Our difference**: We focus on the pure N-body problem without Keplerian splitting

### GADGET-2 (Springel, 2005)
- **Language**: C with MPI parallelism
- **Integrators**: Quasi-symplectic leapfrog with individual time-steps
- **Force methods**: Barnes-Hut tree, TreePM hybrid, direct summation
- **Key feature**: Cosmological SPH, Ewald summation for periodic boundaries
- **Our difference**: We omit hydrodynamics, periodicity, and parallelism

### Nbody6 (Aarseth, 2003)
- **Language**: Fortran
- **Integrators**: 4th-order Hermite with Ahmad-Cohen neighbor scheme
- **Force methods**: Direct summation with neighbor lists, regularization
- **Key feature**: KS and chain regularization for close encounters
- **Our difference**: We use softening instead of regularization; focus on tree methods

## 9. Design Principles (from Steering Directions)

Per the ConceptEvolve steering notes:

1. **Symplectic-first**: All integrators preserve the symplectic structure (SD1)
2. **Vectorized SoA layout**: Flat numpy arrays, no Python objects in hot path (SD2)
3. **Hierarchical force path**: Brute-force -> Newton's-third -> Barnes-Hut (SD3)

## References

- Barnes, J. & Hut, P. (1986). A hierarchical O(N log N) force-calculation algorithm. Nature.
- Rein, H. & Liu, S. (2012). REBOUND: An open-source multi-purpose N-body code. A&A.
- Springel, V. (2005). The cosmological simulation code GADGET-2. MNRAS.
- Yoshida, H. (1990). Construction of higher order symplectic integrators. Phys. Lett. A.
- Aarseth, S. (2003). Gravitational N-Body Simulations. Cambridge University Press.
