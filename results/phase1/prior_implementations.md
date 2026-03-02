# Survey of Prior Open-Source N-Body / Gravity Simulation Implementations

**Rubric Item**: item_005  
**Date**: 2026-03-02  

---

## 1. Introduction

This document surveys five major open-source N-body and gravitational dynamics codebases, ranging from production cosmological simulation engines to educational Python implementations. The goal is to extract design patterns, algorithmic choices, and performance lessons that inform the architecture of our minimal Python gravity simulator.

For each repository we document: the language and build ecosystem, the algorithms implemented, measured or reported performance characteristics, and concrete lessons for our project. We conclude with a cross-cutting comparison table and a list of additional papers that should be added to `sources.bib`.

---

## 2. Repository Surveys

### 2.1 REBOUND

| Attribute | Detail |
|-----------|--------|
| **Repository** | [hannorein/rebound](https://github.com/hannorein/rebound) |
| **Language** | C core with Python bindings (ctypes) |
| **License** | GPL-3.0 |
| **Primary Authors** | Hanno Rein, Shangfei Liu, Daniel Spiegel, and contributors |
| **Key Papers** | Rein & Liu (2012) [rein2012], Rein & Spiegel (2014) [rein2014], Rein & Tamayo (2015) [rein2015whfast] |

#### Algorithms

REBOUND is a modular N-body code designed primarily for planetary dynamics and small-N gravitational systems. It provides a pluggable integrator architecture where the force computation and time-stepping are cleanly separated. Available integrators include:

- **IAS15**: 15th-order implicit Gauss-Radau integrator with adaptive timestep control. Achieves machine-precision energy conservation over 10^9 orbits. Based on the Everhart (1985) scheme with a novel adaptive step-size controller.
- **WHFast**: A fast implementation of the Wisdom-Holman symplectic mapping (Wisdom & Holman, 1991). Second-order symplectic, optimized for near-Keplerian systems (e.g., planetary systems around a dominant central mass). Includes 11th-order symplectic correctors for enhanced accuracy.
- **Leapfrog**: Standard second-order kick-drift-kick (KDK) Stormer-Verlet integrator.
- **SEI**: Shearing-sheet integrator for local disk dynamics.
- **MERCURIUS**: Hybrid symplectic integrator that switches between WHFast for long-range and IAS15 for close encounters, following the MERCURY approach of Chambers (1999).

Force computation is direct O(N^2) pairwise summation. REBOUND does not implement tree codes or FMM -- it targets problems where N is small (planetary systems, debris disks) and accuracy per interaction matters more than asymptotic scaling.

#### Performance Characteristics

- IAS15 requires ~8 function evaluations per step but achieves Brouwer's law error growth (random walk at machine precision).
- WHFast is ~10x faster than IAS15 for near-Keplerian problems due to fixed-step symplecticity and the Kepler solver shortcut.
- Leapfrog is the cheapest per step (1 force evaluation) but only second-order accurate.
- The C core with Python ctypes bindings achieves near-native speed while maintaining a clean Python API. Typical overhead for the Python layer is <1% for N > 10.
- Collision detection is O(N^2) via direct search or O(N log N) via spatial hashing.
- Reported performance: ~10^6 timesteps/second for a 10-body planetary system on a single core (IAS15).

#### Key Lessons for Our Simulator

1. **Modular integrator interface**: REBOUND's clean separation between force computation and time integration is a design pattern we should adopt. Each integrator implements a common interface (`step(dt)`) operating on a shared particle state.
2. **Softening as a parameter, not hardcoded**: REBOUND allows per-simulation softening length, defaulting to zero for point-mass dynamics.
3. **Energy tracking built-in**: REBOUND computes total energy and angular momentum as first-class diagnostics, not afterthoughts. We should build conservation metrics into our simulation loop from the start.
4. **Python/C boundary via ctypes**: Demonstrates that a Python-facing API with C internals is highly effective. For our pure-Python simulator, NumPy vectorization serves the analogous role.
5. **Benchmark suite**: REBOUND ships with example scripts for Kepler orbits, resonance chains, and the outer solar system, providing validated reference solutions.

---

### 2.2 GADGET-2 / GADGET-4

| Attribute | Detail |
|-----------|--------|
| **Repository** | [GADGET-4 on GitLab](https://gitlab.mpcdf.mpg.de/vspringe/gadget4) (GADGET-2 originally distributed from MPA Garching) |
| **Language** | C (GADGET-2), C++ (GADGET-4) |
| **License** | GPL-2.0 (GADGET-2), GPL-3.0 (GADGET-4) |
| **Primary Author** | Volker Springel |
| **Key Papers** | Springel et al. (2001) [springel2001], Springel (2005) [springel2005], Springel et al. (2021) [springel2021gadget4] |

#### Algorithms

GADGET (GAlaxies with Dark matter and Gas intEracTion) is one of the most influential codes in computational cosmology. It employs a TreePM hybrid algorithm:

- **Tree component**: Barnes-Hut octree for short-range gravitational forces. Uses monopole and quadrupole moments for multipole acceptance. The opening criterion is a combination of geometric (Barnes-Hut theta) and relative cell-opening criteria.
- **PM (Particle-Mesh) component**: Long-range forces computed via FFT on a regular mesh. The gravitational potential is solved in Fourier space using the Green's function, then differentiated for forces. This handles the smooth, long-wavelength component of gravity efficiently.
- **TreePM split**: A force-splitting function separates gravity into short-range (tree) and long-range (PM) components at a scale set by the mesh resolution. This gives O(N log N) total complexity with excellent accuracy.
- **SPH**: Smoothed Particle Hydrodynamics for gas dynamics (GADGET is a combined gravity + hydro code).
- **Time integration**: Second-order leapfrog (KDK) with individual block timesteps. Particles are assigned timesteps that are powers of two of the smallest step, enabling efficient hierarchical timestepping.

GADGET-4 (Springel et al., 2021) extends this with FMM capabilities, improved load balancing, and support for on-the-fly group finding and lightcone construction.

#### Performance Characteristics

- GADGET-2 was used for the Millennium Simulation (Springel et al., 2005): 10^10 particles on 512 processors. This remains one of the landmark simulations in cosmology.
- TreePM achieves force accuracy of ~0.1-1% depending on the opening angle and PM mesh resolution.
- Excellent parallel scaling via domain decomposition with Peano-Hilbert space-filling curve. Demonstrated scaling to >10,000 MPI ranks.
- Individual block timesteps provide ~10x speedup over global timesteps for clustered systems (where dense regions require small dt while voids can use large dt).
- Memory footprint: ~100-200 bytes per particle depending on configuration.

#### Key Lessons for Our Simulator

1. **Force splitting is powerful**: Even for our minimal simulator, the concept of splitting forces into near-field (exact) and far-field (approximate) components is instructive. We could implement a simplified version where brute-force handles nearby particles and a coarser approximation handles distant ones.
2. **Individual timesteps**: While complex to implement symplectically, the concept of giving different particles different timesteps based on their local dynamical time is essential for efficiency in clustered systems.
3. **Domain decomposition via space-filling curves**: The Peano-Hilbert curve provides excellent spatial locality for cache performance even on a single core. For our Barnes-Hut implementation, Morton ordering (Z-curve) of particles before tree construction would improve cache coherence.
4. **Opening criterion matters**: GADGET's relative cell-opening criterion (which considers the particle-cell distance relative to the cell's internal structure) is more robust than the simple geometric criterion s/d < theta.
5. **Block timestep hierarchy**: Powers-of-two timestep levels are simple to implement and allow efficient synchronization. Worth considering for an advanced version of our simulator.

---

### 2.3 PKDGRAV3 / ChaNGa

| Attribute | Detail |
|-----------|--------|
| **Repository** | [PKDGRAV3](https://bitbucket.org/dpotter/pkdgrav3) and [ChaNGa](https://github.com/N-BodyShop/changa) |
| **Language** | C (PKDGRAV3), C++ with Charm++ (ChaNGa) |
| **License** | Various open-source licenses |
| **Primary Authors** | Joachim Stadel, Douglas Potter (PKDGRAV3); Tom Quinn, Filippo Gioachin (ChaNGa) |
| **Key Papers** | Potter, Stadel & Teyssier (2017) [potter2017], Stadel (2001) [stadel2001], Jetley et al. (2008) [jetley2008] |

#### Algorithms

PKDGRAV3 represents the state of the art in large-scale gravitational N-body computation:

- **Fast Multipole Method (FMM)**: Full FMM with multipole-to-local (M2L) translations up to hexadecapole order (p=4). This achieves O(N) complexity for uniform distributions, though practical performance depends on the particle distribution.
- **Tree structure**: K-D tree (binary spatial partition) rather than octree. K-D trees provide better load balancing for non-uniform distributions and are simpler to construct.
- **Individual timesteps**: Fully adaptive individual timesteps with multistepping. Each particle evolves on its own timescale.
- **Periodic boundaries**: Ewald summation for periodic boundary conditions, essential for cosmological simulations.
- **Dual tree traversal**: Both source and sink trees are traversed simultaneously, enabling efficient interaction lists and better cache utilization.

ChaNGa (Charm N-body GrAvity) is a related code from the N-Body Shop group that uses the Charm++ parallel runtime for dynamic load balancing. It implements Barnes-Hut with hexadecapole corrections and SPH.

#### Performance Characteristics

- PKDGRAV3 achieved the first-ever trillion-particle (2 x 10^12) cosmological simulation, running on the Piz Daint supercomputer (Potter et al., 2017).
- FMM provides ~5x speedup over Barnes-Hut for N > 10^6 at comparable accuracy.
- Dual tree traversal reduces tree walk time by ~30% compared to standard particle-cell traversal.
- K-D tree construction is O(N log N) and highly cache-efficient due to binary splitting.
- ChaNGa demonstrates excellent scaling to 128K+ cores using Charm++ over-decomposition and dynamic load balancing.
- PKDGRAV3 reports ~10^5 particle-steps per second per core for cosmological simulations.

#### Key Lessons for Our Simulator

1. **K-D tree vs. octree/quadtree**: For 2D simulations, a binary K-D tree may be simpler and more efficient than a quadtree. It splits one axis at a time, giving a balanced tree by construction when splitting at the median. Worth considering as an alternative to our planned quadtree.
2. **Multipole order matters**: Even going from monopole (center-of-mass) to quadrupole gives significant accuracy improvement. Our Barnes-Hut implementation should track at least the quadrupole moment per node.
3. **Dual tree traversal**: An advanced optimization where we traverse both the "source" tree (containing mass) and "sink" tree (containing evaluation points) simultaneously. Beyond our scope but conceptually important.
4. **FMM as the theoretical optimum**: O(N) complexity is the gold standard. Understanding why FMM achieves this (systematic M2L translations that avoid redundant work) helps us appreciate what Barnes-Hut's O(N log N) is "paying" for.
5. **Memory layout**: PKDGRAV3 uses structure-of-arrays (SoA) layout for particle data, which is more cache-friendly for vectorized operations. Our NumPy arrays naturally provide this.

---

### 2.4 Educational Python N-Body Simulators

| Attribute | Detail |
|-----------|--------|
| **Repositories** | [pmocz/nbody-python](https://github.com/pmocz/nbody-python), [pynbody/pynbody](https://github.com/pynbody/pynbody), [vpython nbody examples](https://github.com/vpython/vpython-jupyter), various "nbody" repos on GitHub |
| **Language** | Python (NumPy) |
| **License** | Various (MIT, BSD, GPL) |
| **Primary Authors** | Philip Mocz (Princeton), various educational authors |
| **Key References** | Mocz (2020) [mocz2020] blog post series, various course materials |

#### Algorithms

The Python N-body ecosystem comprises dozens of educational and prototype implementations. Common patterns across these codebases include:

- **Brute-force O(N^2) with NumPy vectorization**: The most common approach. Particle positions stored as (N, 2) or (N, 3) arrays. Pairwise distances computed via broadcasting: `dx = x[:, None, :] - x[None, :, :]`, giving an (N, N, d) displacement tensor. Forces accumulated via `np.sum` over the source axis.
- **Leapfrog integration**: Nearly all educational codes use the KDK leapfrog, often implemented in ~20 lines of Python.
- **Plummer softening**: Universal use of epsilon softening to prevent singularities.
- **Matplotlib animation**: Real-time visualization via `matplotlib.animation.FuncAnimation` or frame-by-frame saving.

Notable specific implementations:

1. **pmocz/nbody-python** (Philip Mocz): Clean 100-line implementation of brute-force N-body with leapfrog. Uses vectorized NumPy throughout. Includes energy conservation tracking. Excellent pedagogical reference.
2. **pynbody**: Analysis and visualization library for N-body simulation outputs (not a simulator itself, but relevant for post-processing patterns). Reads GADGET, TIPSY, and other formats.
3. **Various course implementations**: Stanford CS 205, Princeton AST 204, and MIT 8.962 all have published N-body assignments with reference solutions in Python.

#### Performance Characteristics

- Pure NumPy brute-force: ~1 second for N=1000 per timestep on modern hardware (single core). The N^2 scaling is clear: N=2000 takes ~4 seconds.
- NumPy broadcasting creates an O(N^2) memory intermediate (the pairwise displacement tensor), limiting practical N to ~5000-10,000 before memory becomes an issue.
- With Numba JIT compilation, brute-force Python approaches within 5-10x of C performance for N < 10,000.
- Matplotlib real-time animation limits frame rate to ~10-30 fps depending on N and rendering complexity.

#### Key Lessons for Our Simulator

1. **NumPy broadcasting is the key pattern**: The `x[:, None, :] - x[None, :, :]` idiom for computing all pairwise displacements is the core vectorization trick. We should use this for our brute-force implementation.
2. **Avoid Python loops over particles**: Even a single explicit loop over N particles (for force accumulation) destroys performance. Everything must be vectorized or delegated to NumPy/SciPy.
3. **Memory-performance tradeoff**: The O(N^2) memory for the pairwise tensor is acceptable for N < ~5000 but becomes the bottleneck before compute does. For larger N, chunked computation or Barnes-Hut is needed.
4. **Simplicity aids correctness**: The 100-line implementations are trivially verifiable against analytical solutions. Starting with the simplest possible correct code and adding complexity incrementally is the right approach.
5. **Visualization as debugging tool**: Real-time plotting of orbits and energy evolution catches bugs faster than unit tests alone. We should integrate matplotlib visualization from the earliest stages.
6. **Softening parameter sensitivity**: Educational repos consistently demonstrate that too-small epsilon causes energy blowup while too-large epsilon distorts orbits. A value of epsilon ~ 0.01 * characteristic_length is a common default.

---

### 2.5 galpy

| Attribute | Detail |
|-----------|--------|
| **Repository** | [jobovy/galpy](https://github.com/jobovy/galpy) |
| **Language** | Python with C extensions |
| **License** | BSD-3-Clause |
| **Primary Author** | Jo Bovy (University of Toronto) |
| **Key Paper** | Bovy (2015) [bovy2015] |

#### Algorithms

galpy is a Python library for galactic dynamics, providing a comprehensive toolkit for orbit integration, potential evaluation, and distribution function computation. Unlike the other codes surveyed, galpy focuses on orbits in fixed or semi-analytic potentials rather than self-consistent N-body simulation:

- **Potential library**: Extensive collection of analytic gravitational potentials including Miyamoto-Nagai disk, NFW halo, logarithmic halo, Hernquist profile, power-law, and many more. Potentials can be combined additively.
- **Orbit integration**: Multiple integrators available:
  - Leapfrog (symplectic, 2nd-order)
  - 4th-order symplectic (Yoshida-type)
  - `dop853`: 8th-order Dormand-Prince (via SciPy)
  - `odeint`: LSODA adaptive integrator (via SciPy)
- **Action-angle coordinates**: Computation of actions (J_R, J_phi, J_z), angles, and frequencies using the Staeckel approximation, adiabatic approximation, or numerical orbit integration.
- **Distribution functions**: Quasi-isothermal, Dehnen, Shu, and other distribution functions for modeling stellar populations.
- **Coordinate transformations**: Full support for galactocentric, heliocentric, and observational coordinate systems.

While galpy is not an N-body code, it provides excellent reference implementations of orbit integration in gravitational potentials and validated test cases.

#### Performance Characteristics

- Orbit integration in analytic potentials is extremely fast: ~10^6 timesteps/second for a single orbit in a combined disk+halo potential.
- C extensions accelerate potential evaluation by 10-100x over pure Python for complex multi-component potentials.
- Action-angle computation via Staeckel approximation: ~10^4 orbits/second.
- The code is well-optimized for vectorized evaluation of potentials at many points simultaneously (useful for force evaluation on particle arrays).
- Full test suite with >90% coverage, including comparison against known analytical solutions (Kepler, harmonic oscillator, Henon-Heiles).

#### Key Lessons for Our Simulator

1. **Analytic potentials as test oracles**: galpy's library of exact gravitational potentials provides reference solutions for testing our force computation. A particle orbiting in a known potential (e.g., Kepler, Plummer) should conserve energy to the integrator's expected order.
2. **Integrator comparison methodology**: galpy provides direct comparison between symplectic (leapfrog, Yoshida) and non-symplectic (Dormand-Prince, LSODA) integrators on the same problems, demonstrating the long-term advantage of symplecticity. We should replicate this comparison.
3. **Unit system design**: galpy uses "natural units" (velocities in km/s, distances in kpc, masses in solar masses) with explicit unit conversion. For our simulator, adopting G=1 natural units simplifies the code and avoids floating-point range issues.
4. **API design pattern**: galpy's `Orbit` class with methods like `.integrate()`, `.E()`, `.L()`, `.plot()` provides a clean interface model. Our `Simulation` class should offer similar convenience methods.
5. **Testing against known solutions**: galpy validates integrators against the Kepler problem, harmonic oscillator, and other exactly solvable systems. We should adopt the same validation hierarchy: Kepler (2-body), circular orbit stability, and figure-eight (3-body).

---

## 3. Cross-Cutting Comparison

### 3.1 Algorithm and Complexity Summary

| Code | Force Algorithm | Complexity | Integrators | Target N |
|------|----------------|------------|-------------|----------|
| REBOUND | Direct (pairwise) | O(N^2) | IAS15, WHFast, Leapfrog, SEI, MERCURIUS | 2 -- 10^4 |
| GADGET-2/4 | TreePM hybrid | O(N log N) | Leapfrog (KDK) with individual block timesteps | 10^6 -- 10^10 |
| PKDGRAV3 | FMM + tree | O(N) | Leapfrog with individual timesteps | 10^8 -- 10^12 |
| Python nbody | Direct (vectorized) | O(N^2) | Leapfrog | 10 -- 10^3 |
| galpy | Analytic potentials | O(1) per particle | Leapfrog, Yoshida, DOP853, LSODA | N/A (single orbits) |

### 3.2 Language and Architecture Comparison

| Code | Core Language | Python API | Parallelism | Build System |
|------|--------------|------------|-------------|-------------|
| REBOUND | C | ctypes bindings | OpenMP (limited) | Makefile / pip |
| GADGET-2/4 | C / C++ | None (standalone) | MPI + OpenMP | Makefile / CMake |
| PKDGRAV3 | C | None | MPI + pthreads | CMake |
| ChaNGa | C++ | None | Charm++ | Charm++ build |
| Python nbody | Python | Native | None (single-thread) | pip / script |
| galpy | Python + C ext | Native | OpenMP (C extensions) | pip / setup.py |

### 3.3 Design Philosophy Spectrum

These codes span a clear design philosophy spectrum from **accuracy-first** to **scale-first**:

```
Accuracy-first                                        Scale-first
    |                                                      |
  REBOUND ---- galpy ---- Python nbody ---- GADGET ---- PKDGRAV3
  (IAS15:      (analytic   (pedagogical     (TreePM      (FMM:
   machine     potentials:  clarity)         hybrid:      O(N),
   precision)  exact)                        O(N log N))  10^12)
```

Our minimal simulator sits in the middle: we need pedagogical clarity (like Python nbody codes) with correct physics (like REBOUND) and the option to scale to moderate N (like GADGET's tree approach, simplified).

---

## 4. Architectural Patterns to Adopt

### 4.1 From REBOUND: Modular Integrator Interface

```python
class Integrator(ABC):
    @abstractmethod
    def step(self, system: ParticleSystem, dt: float) -> None:
        """Advance system by one timestep."""
        ...

class Leapfrog(Integrator):
    def step(self, system, dt): ...

class Yoshida4(Integrator):
    def step(self, system, dt): ...
```

### 4.2 From GADGET: Force Computation Abstraction

```python
class ForceComputation(ABC):
    @abstractmethod
    def compute(self, positions: np.ndarray, masses: np.ndarray) -> np.ndarray:
        """Return accelerations array of shape (N, 2)."""
        ...

class BruteForce(ForceComputation):
    def compute(self, positions, masses): ...

class BarnesHut(ForceComputation):
    def __init__(self, theta: float = 0.5): ...
    def compute(self, positions, masses): ...
```

### 4.3 From galpy: Conservation Diagnostics

```python
class Diagnostics:
    def kinetic_energy(self, system) -> float: ...
    def potential_energy(self, system) -> float: ...
    def total_energy(self, system) -> float: ...
    def angular_momentum(self, system) -> float: ...
    def relative_energy_error(self, system, E0: float) -> float: ...
```

### 4.4 From Educational Codes: NumPy Vectorization

```python
# Core brute-force pattern (from pmocz style)
dx = positions[:, np.newaxis, :] - positions[np.newaxis, :, :]  # (N, N, 2)
r2 = np.sum(dx**2, axis=-1) + epsilon**2                        # (N, N)
inv_r3 = r2**(-1.5)                                              # (N, N)
acc = G * np.sum(masses[np.newaxis, :, np.newaxis] * dx * inv_r3[:, :, np.newaxis], axis=1)
```

---

## 5. Common Pitfalls Identified Across Implementations

1. **Forgetting Newton's third law**: Several educational codes compute F_ij and F_ji independently, wasting half the computation. Symmetric force evaluation halves the work and exactly conserves linear momentum.

2. **Self-interaction in vectorized code**: When computing pairwise forces via broadcasting, the diagonal (i=i) terms produce NaN or infinity without softening. Must either mask the diagonal or ensure softening prevents division by zero.

3. **Energy computation timing**: Energy must be evaluated at synchronized times (positions and velocities at the same time). In leapfrog, velocities are offset by dt/2; energy evaluation requires a half-kick to synchronize.

4. **Floating-point accumulation order**: Summing N forces in different orders gives different floating-point results. For reproducibility, particle ordering should be deterministic (sorted by index or spatial curve).

5. **Softening and conservation**: Plummer softening modifies the potential, so the "conserved" energy includes the softened potential. Comparing softened and unsoftened energies is invalid.

---

## 6. Additional References for sources.bib

The following papers are referenced by the surveyed repositories and should be added to our bibliography:

### 6.1 Code Papers

| Citation Key | Authors | Year | Title | Relevance |
|-------------|---------|------|-------|-----------|
| `rein2015whfast` | Rein & Tamayo | 2015 | WHFast: A fast and accurate implementation of the Wisdom-Holman integrator | REBOUND's symplectic integrator |
| `springel2001` | Springel, Yoshida, White | 2001 | GADGET: A code for collisionless and gasdynamical cosmological simulations | Original GADGET paper |
| `springel2021gadget4` | Springel et al. | 2021 | Simulating cosmic structure formation with the GADGET-4 code | GADGET-4 methods paper |
| `stadel2001` | Stadel | 2001 | Cosmological N-body simulations and their analysis (PhD thesis) | PKDGRAV methods and K-D tree design |
| `jetley2008` | Jetley et al. | 2008 | Massively parallel cosmological simulations with ChaNGa | ChaNGa code paper |
| `bovy2015` | Bovy | 2015 | galpy: A Python library for galactic dynamics | galpy code paper |
| `chambers1999` | Chambers | 1999 | A hybrid symplectic integrator (MERCURY) | Hybrid integrator method used in REBOUND's MERCURIUS |
| `everhart1985` | Everhart | 1985 | An efficient integrator using Gauss-Radau spacings | Basis for IAS15 |

### 6.2 Method Papers

| Citation Key | Authors | Year | Title | Relevance |
|-------------|---------|------|-------|-----------|
| `dehnen2002` | Dehnen | 2002 | A hierarchical O(N) force calculation algorithm | Improved tree algorithm with mutual interactions |
| `dehnen2011` | Dehnen & Read | 2011 | N-body simulations of gravitational dynamics | Review article covering all major methods |
| `springel2010` | Springel | 2010 | E pur si muove: Galilean-invariant cosmological SPH | Advanced SPH methods |
| `hernquist1987` | Hernquist & Katz | 1987 | TreeSPH: A unification of SPH with the tree algorithm | Foundational tree+hydro combination |
| `salmon1994` | Salmon & Warren | 1994 | Skeletons from the treecode closet | Error analysis of tree codes, improved opening criteria |

### 6.3 Recommended BibTeX Entries

```bibtex
@article{rein2015whfast,
  title={WHFast: A Fast and Accurate Implementation of the Wisdom-Holman Integrator},
  author={Hanno Rein and Daniel Tamayo},
  year={2015},
  journal={Monthly Notices of the Royal Astronomical Society},
  volume={452},
  number={1},
  pages={376--388},
  doi={10.1093/mnras/stv1257},
}

@article{springel2021gadget4,
  title={Simulating Cosmic Structure Formation with the GADGET-4 Code},
  author={Volker Springel and Ruediger Pakmor and Oliver Zier and Martin Reinecke},
  year={2021},
  journal={Monthly Notices of the Royal Astronomical Society},
  volume={506},
  number={2},
  pages={2871--2949},
  doi={10.1093/mnras/stab1855},
}

@article{bovy2015,
  title={galpy: A Python Library for Galactic Dynamics},
  author={Jo Bovy},
  year={2015},
  journal={The Astrophysical Journal Supplement Series},
  volume={216},
  number={2},
  pages={29},
  doi={10.1088/0067-0049/216/2/29},
}

@phdthesis{stadel2001,
  title={Cosmological N-body Simulations and their Analysis},
  author={Joachim G. Stadel},
  year={2001},
  school={University of Washington},
}

@inproceedings{jetley2008,
  title={Massively Parallel Cosmological Simulations with ChaNGa},
  author={Pritish Jetley and Filippo Gioachin and Celso Mendes and Laxmikant V. Kale and Thomas R. Quinn},
  year={2008},
  booktitle={Proceedings of the IEEE International Parallel and Distributed Processing Symposium},
  doi={10.1109/IPDPS.2008.4536319},
}

@article{chambers1999,
  title={A Hybrid Symplectic Integrator that Permits Close Encounters between Massive Bodies},
  author={John E. Chambers},
  year={1999},
  journal={Monthly Notices of the Royal Astronomical Society},
  volume={304},
  number={4},
  pages={793--799},
  doi={10.1046/j.1365-8711.1999.02379.x},
}

@inproceedings{everhart1985,
  title={An Efficient Integrator that Uses Gauss-Radau Spacings},
  author={Edgar Everhart},
  year={1985},
  booktitle={Dynamics of Comets: Their Origin and Evolution},
  pages={185--202},
  publisher={Reidel},
  doi={10.1007/978-94-009-5400-7_17},
}

@article{dehnen2011,
  title={N-body Simulations of Gravitational Dynamics},
  author={Walter Dehnen and Justin I. Read},
  year={2011},
  journal={European Physical Journal Plus},
  volume={126},
  pages={55},
  doi={10.1140/epjp/i2011-11055-3},
}

@article{salmon1994,
  title={Skeletons from the Treecode Closet},
  author={John K. Salmon and Michael S. Warren},
  year={1994},
  journal={Journal of Computational Physics},
  volume={111},
  number={1},
  pages={136--155},
  doi={10.1006/jcph.1994.1050},
}
```

---

## 7. Synthesis: Design Decisions for Our Simulator

Based on this survey, the following design decisions are justified:

### 7.1 Force Computation Strategy

| Decision | Rationale | Source |
|----------|-----------|-------|
| Start with brute-force O(N^2) | All surveyed codes include direct summation as baseline; NumPy vectorization makes it practical for N < 5000 | REBOUND, Python nbody |
| Add Barnes-Hut quadtree | O(N log N) is necessary for N > 1000; quadtree is simpler than K-D tree for 2D | GADGET, PKDGRAV3 |
| Use Plummer softening | Universal across all implementations; physically motivated | All surveyed codes |
| Track quadrupole moments | Significant accuracy improvement for modest implementation cost | PKDGRAV3, GADGET |

### 7.2 Integration Strategy

| Decision | Rationale | Source |
|----------|-----------|-------|
| Leapfrog as default | Used by every surveyed code; minimal implementation, symplectic | All surveyed codes |
| Yoshida 4th-order as upgrade | 100x accuracy improvement for 3x cost; composition method is elegant | galpy, REBOUND |
| Fixed global timestep | Individual timesteps add massive complexity; fixed dt is sufficient for our N range | Simplification of GADGET pattern |
| Energy synchronization at output | Leapfrog half-step sync required for correct energy evaluation | REBOUND, educational codes |

### 7.3 Software Architecture

| Decision | Rationale | Source |
|----------|-----------|-------|
| Abstract integrator interface | REBOUND's modular design enables clean comparison between methods | REBOUND |
| Abstract force computation interface | GADGET's separation enables swapping brute-force for tree code | GADGET |
| Built-in conservation diagnostics | Every production code tracks energy as first-class diagnostic | REBOUND, galpy |
| NumPy arrays as core data structure | SoA layout is cache-friendly and enables vectorized operations | Python nbody, galpy |
| G=1 natural units | Simplifies code, avoids floating-point range issues | galpy |

---

## 8. Summary

This survey of five open-source N-body implementations reveals a clear progression from simple educational codes to production cosmological engines. The key insight is that all of them share the same fundamental building blocks -- pairwise gravity, symplectic integration, and energy diagnostics -- differing primarily in how they optimize these components for scale.

Our minimal Python gravity simulator should:
1. Implement the shared fundamentals correctly (brute-force + leapfrog)
2. Adopt the modular architecture patterns from REBOUND and GADGET
3. Include conservation diagnostics from the start (not as an afterthought)
4. Use NumPy vectorization as our primary performance tool
5. Add Barnes-Hut as the scaling solution, targeting N ~ 1000-10,000
6. Validate against known solutions (Kepler, figure-eight) following galpy's methodology

The 10 additional bibliography entries identified in Section 6 should be added to `sources.bib` to complete our literature foundation.

---

## 9. References

All citations refer to entries in `/sources.bib`. New entries proposed in Section 6.3 should be appended to that file.

- [rein2012] Rein & Liu, 2012 -- REBOUND code paper
- [rein2014] Rein & Spiegel, 2014 -- IAS15 integrator
- [springel2005] Springel, 2005 -- GADGET-2 code paper
- [potter2017] Potter, Stadel & Teyssier, 2017 -- PKDGRAV3
- [barnes1986] Barnes & Hut, 1986 -- Tree algorithm
- [greengard1987] Greengard & Rokhlin, 1987 -- FMM
- [yoshida1990] Yoshida, 1990 -- 4th-order symplectic
- [wisdom1991] Wisdom & Holman, 1991 -- Symplectic maps
- [hairer2006] Hairer et al., 2006 -- Geometric numerical integration
- [bovy2015] Bovy, 2015 -- galpy (proposed addition)
- [rein2015whfast] Rein & Tamayo, 2015 -- WHFast (proposed addition)
- [springel2021gadget4] Springel et al., 2021 -- GADGET-4 (proposed addition)
- [dehnen2011] Dehnen & Read, 2011 -- N-body review (proposed addition)
- [chambers1999] Chambers, 1999 -- MERCURY hybrid integrator (proposed addition)
- [everhart1985] Everhart, 1985 -- Gauss-Radau integrator (proposed addition)
