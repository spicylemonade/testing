# Problem Scope: Minimal Gravity Simulator

**Rubric Item**: item_004  
**Date**: 2026-03-02  
**Status**: Complete  

---

## 1. Introduction

This document defines the scope, constraints, and requirements for a minimal gravitational
N-body simulator. The simulator targets pedagogical clarity and algorithmic exploration over
astrophysical realism: the goal is to implement, validate, and benchmark the core algorithms
of gravitational dynamics in a self-contained Python codebase. All design decisions below are
informed by the literature review (`results/phase1/literature_review.md`) and the concept tree
generated via ConceptEvolve (`results/concept_evolve/tree/`).

The implementation follows the concept-tree path:

```
particle_data_structures -> force_computation -> numerical_integration
    -> conservation_laws -> validation_benchmarks -> visualization
```

This path was identified during the ConceptEvolve walk phase (see
`results/concept_evolve/tree/walk_paths.json`, paths 2 and 3) as the primary dependency chain
for a minimal viable simulator. Each node in the path corresponds to a concept folder in the
tree:

| Step | Concept Node             | Tree Folder                                  |
|------|--------------------------|----------------------------------------------|
| 1    | `particle_data_structures` | `003_particle-data-structures/`             |
| 2    | `force_computation`        | `001_force-computation/`                    |
| 3    | `numerical_integration`    | `002_numerical-integration/`                |
| 4    | `conservation_laws`        | `007_conservation-laws/`                    |
| 5    | `validation_benchmarks`    | `006_validation-benchmarks/`                |
| 6    | `visualization`            | `005_visualization/`                        |

An auxiliary branch via `spatial_trees` (`004_spatial-trees/`) feeds into `force_computation`
when the Barnes-Hut algorithm is enabled.

---

## 2. Dimensionality Choice: 2D

### 2.1 Decision

The simulator operates in **two spatial dimensions** (2D). All positions, velocities, and
accelerations are represented as 2-component vectors.

### 2.2 Justification

Three independent considerations support the 2D choice:

**Visualization simplicity.** 2D simulations map directly to screen coordinates. No projection,
camera model, or depth-sorting is required. This eliminates an entire class of implementation
complexity and keeps the visualization pipeline (matplotlib scatter/line plots) trivial to
implement and debug. The concept node `visualization` (`005_visualization/`) identifies direct
2D rendering as the lowest-friction path to visual validation.

**Computational cost reduction.** Every vector operation — distance computation, force
accumulation, position update — operates on 2 components instead of 3. For the brute-force
$O(N^2)$ algorithm, this reduces the inner-loop constant factor by roughly 33%. More
importantly, memory layout for Structure-of-Arrays (SoA) representations is more cache-friendly
with fewer components per particle.

**Algorithmic equivalence.** The N-body algorithms central to this project — brute-force
direct summation and the Barnes-Hut tree method — are structurally identical in 2D and 3D. The
only changes are dimensional: quadtrees replace octrees, 2D distance replaces 3D distance, and
angular momentum becomes a scalar instead of a vector. The algorithmic complexity classes,
convergence properties, and error characteristics are preserved.

### 2.3 Literature Support

**Barnes & Hut (1986)** [barnes1986] introduced their hierarchical tree algorithm using an
octree spatial decomposition in 3D. The 2D specialization uses a quadtree — each internal node
subdivides space into four quadrants rather than eight octants. The multipole acceptance
criterion ($s/d < \theta$, where $s$ is node width and $d$ is distance to center of mass) is
identical in both cases. The algorithm's $O(N \log N)$ complexity is dimension-independent;
only the branching factor of the tree changes (4 vs. 8), which affects constants but not
asymptotic scaling.

**Pfalzner & Gibbon (1996)** [pfalzner1996] provide a systematic analysis of tree methods in
*Many-Body Tree Methods in Physics*, explicitly treating both 2D and 3D formulations. Their
error analysis demonstrates that force approximation accuracy as a function of the opening
angle $\theta$ follows the same power-law behavior in 2D and 3D. The complexity class
$O(N \log N)$ for tree construction and force evaluation holds in both dimensionalities, with
the 2D case producing slightly shallower trees (due to the lower branching factor) and
correspondingly smaller constant factors. Their treatment confirms that 2D simulations capture
the full algorithmic character of the N-body problem without loss of generality for the
questions this project investigates.

### 2.4 What 2D Does Not Capture

For transparency, the following aspects are lost in the 2D restriction:

- **3D orbital mechanics**: Inclination, longitude of ascending node, and argument of
  perihelion have no 2D analogue. Orbital elements reduce from 6 to 4.
- **Vector angular momentum**: In 3D, $\mathbf{L} = \mathbf{r} \times \mathbf{v}$ is a
  3-vector. In 2D, $L = x v_y - y v_x$ is a scalar (the $z$-component of the cross product).
  Conservation is still meaningful but less structurally rich.
- **Astrophysical realism**: Real stellar systems, galaxies, and planetary systems are
  inherently 3D. The 2D simulator makes no claim to physical fidelity for such systems.

None of these limitations affect the project's core goals of algorithm implementation,
validation, and benchmarking.

---

## 3. Target Body Count Range

### 3.1 Overall Range

The simulator must support body counts from **N = 2** through **N = 1000+**:

| Range       | Purpose                           | Algorithm          | Mode         |
|-------------|-----------------------------------|--------------------|--------------|
| N = 2       | Kepler orbit validation           | Brute-force        | Real-time    |
| N = 3–10    | Few-body dynamics, chaos onset    | Brute-force        | Real-time    |
| N = 10–100  | Cluster dynamics, energy drift    | Brute-force        | Real-time    |
| N = 100–500 | Scaling transition zone           | Both               | Benchmarking |
| N = 500–1000+ | Barnes-Hut scaling tests       | Barnes-Hut         | Benchmarking |

### 3.2 Primary Focus: N = 2–100 (Real-Time)

The primary interactive use case targets N = 2 to N = 100 bodies running in real-time
(defined as $\geq$ 30 integration steps per second with force evaluation as the bottleneck).
At N = 100, brute-force requires $\binom{100}{2} = 4950$ pairwise force evaluations per step,
well within the capability of vectorized NumPy on modern hardware.

### 3.3 Secondary Focus: N = 100–1000 (Benchmarking)

The benchmarking suite measures wall-clock time per integration step as a function of N for
both brute-force and Barnes-Hut algorithms. The crossover point — where Barnes-Hut's
$O(N \log N)$ overtakes brute-force's $O(N^2)$ despite higher constant factors — is expected
near N = 200–500 depending on the opening angle $\theta$ and implementation details. Runs at
N = 1000 confirm asymptotic scaling.

### 3.4 Upper Bound

No hard upper bound is imposed, but the simulator is not designed for N > 10,000. At that
scale, memory layout optimizations (cache-oblivious algorithms), GPU offloading, and
parallelism become necessary — all outside the minimal scope.

---

## 4. Force Model

### 4.1 Newtonian Gravity with Plummer Softening

The gravitational force on body $i$ due to body $j$ is:

$$\mathbf{F}_{ij} = \frac{G \, m_i \, m_j \, \mathbf{r}_{ij}}{(|\mathbf{r}_{ij}|^2 + \epsilon^2)^{3/2}}$$

where:

- $\mathbf{r}_{ij} = \mathbf{r}_j - \mathbf{r}_i$ is the displacement vector from body $i$
  to body $j$
- $|\mathbf{r}_{ij}|$ is the Euclidean distance in 2D
- $G$ is the gravitational constant (configurable, default: 1.0 in simulation units)
- $m_i, m_j$ are the body masses
- $\epsilon$ is the Plummer softening length (configurable, default: 0.01)

### 4.2 Softening Rationale

The Plummer softening parameter $\epsilon$ serves two purposes:

1. **Singularity avoidance**: The bare Newtonian potential $\propto 1/r$ diverges as
   $r \to 0$. In discrete N-body systems without regularization, close encounters produce
   arbitrarily large forces that destabilize the integrator. The softened denominator
   $(r^2 + \epsilon^2)^{3/2}$ caps the maximum force at $F_{\max} \approx G m_i m_j /
   (2\epsilon^2)$ (achieved at $r = \epsilon / \sqrt{2}$).

2. **Effective smoothing**: Plummer softening replaces each point mass with a Plummer sphere
   of characteristic radius $\epsilon$. This is physically motivated: real stellar systems
   have finite extent, and the softening mimics the effect of unresolved substructure.

The softening length should satisfy $\epsilon \ll L$ (where $L$ is the typical inter-particle
separation) to avoid suppressing genuine gravitational interactions, while being large enough
to prevent numerical overflow. A value of $\epsilon \approx 0.01 L$ is typical.

### 4.3 Configurable Parameters

| Parameter | Symbol     | Default | Units           | Notes                               |
|-----------|------------|---------|-----------------|-------------------------------------|
| Gravitational constant | $G$ | 1.0 | sim units   | Set to 1 for dimensionless runs     |
| Softening length | $\epsilon$ | 0.01 | length units | Scale relative to system size       |
| Opening angle | $\theta$   | 0.5   | dimensionless   | Barnes-Hut only; 0 = exact          |

### 4.4 Total Force on a Body

The net force on body $i$ is the superposition of all pairwise interactions:

$$\mathbf{F}_i = \sum_{j \neq i} \mathbf{F}_{ij}$$

The corresponding acceleration is $\mathbf{a}_i = \mathbf{F}_i / m_i$. Newton's third law
guarantees $\mathbf{F}_{ij} = -\mathbf{F}_{ji}$, which the brute-force implementation
exploits to halve the number of force evaluations (computing each pair once and applying
equal-and-opposite forces).

---

## 5. Conservation Properties

### 5.1 Conserved Quantities

For an isolated N-body system under Newtonian gravity with no external forces and no
dissipation, the following quantities are exactly conserved in continuous time:

**Total energy** (kinetic + potential):

$$E = T + V = \sum_i \frac{1}{2} m_i |\mathbf{v}_i|^2 + \sum_{i < j} \frac{-G \, m_i \, m_j}{(|\mathbf{r}_{ij}|^2 + \epsilon^2)^{1/2}}$$

Note: the potential uses the softened distance, consistent with the force model. This ensures
the force is the exact negative gradient of the potential, which is required for the system to
be Hamiltonian.

**Linear momentum**:

$$\mathbf{p} = \sum_i m_i \mathbf{v}_i$$

Conservation follows from Newton's third law. In practice, linear momentum is preserved to
machine precision by symmetric force accumulation.

**Angular momentum** (scalar in 2D):

$$L = \sum_i m_i (x_i \, v_{y,i} - y_i \, v_{x,i})$$

This is the $z$-component of $\sum_i m_i (\mathbf{r}_i \times \mathbf{v}_i)$ and is the only
non-trivial component in 2D. Conservation follows from the central nature of the gravitational
force (forces along the line connecting two bodies produce zero net torque).

### 5.2 Numerical Conservation and Symplectic Integrators

Discrete time-stepping introduces numerical error in all conserved quantities. The choice of
integrator determines the character of this error:

- **Non-symplectic methods** (e.g., RK4): Energy drifts secularly. Over long integrations,
  the accumulated error grows without bound ($\Delta E \propto t$ or worse).
- **Symplectic methods** (e.g., Leapfrog/Verlet, Yoshida): Energy error is bounded and
  oscillatory. A symplectic integrator exactly preserves a shadow Hamiltonian
  $\tilde{H} = H + O(\Delta t^p)$, where $p$ is the integrator order. The physical energy
  oscillates around the true value with amplitude $O(\Delta t^p)$ but no secular drift.

The simulator uses symplectic integrators (Leapfrog as baseline, Yoshida 4th-order as upgrade)
to ensure bounded energy error. This is a core requirement, not an optimization — secular
energy drift would invalidate long-duration simulations entirely.

### 5.3 Conservation Monitoring

Every integration step, the simulator computes and records:

| Quantity                | Symbol   | Expected Error (Leapfrog) | Expected Error (Yoshida) |
|-------------------------|----------|---------------------------|--------------------------|
| Total energy            | $E$      | $O(\Delta t^2)$ bounded   | $O(\Delta t^4)$ bounded  |
| Linear momentum (x)     | $p_x$   | Machine precision          | Machine precision         |
| Linear momentum (y)     | $p_y$   | Machine precision          | Machine precision         |
| Angular momentum        | $L$     | $O(\Delta t^2)$ bounded    | $O(\Delta t^4)$ bounded  |

Relative energy error $|\Delta E / E_0|$ is the primary diagnostic. Acceptable thresholds:

- Leapfrog at $\Delta t = 0.01$: $|\Delta E / E_0| < 10^{-4}$ over 1000 orbits
- Yoshida at $\Delta t = 0.01$: $|\Delta E / E_0| < 10^{-8}$ over 1000 orbits

---

## 6. Performance Targets

### 6.1 Real-Time Operation (N $\leq$ 100)

The simulator must sustain at least **30 integration steps per second** (equivalent to 30 fps
for animated visualization) using brute-force force computation for up to N = 100 bodies. This
translates to a per-step wall-clock budget of approximately 33 ms, allocated as:

| Phase                | Budget   | Notes                                      |
|----------------------|----------|--------------------------------------------|
| Force computation    | 20 ms    | Dominant cost: $O(N^2)$ pairwise forces    |
| Integration step     | 2 ms     | Leapfrog kick-drift-kick                   |
| Conservation check   | 1 ms     | Energy, momentum, angular momentum sums    |
| Visualization update | 10 ms    | matplotlib blitting or frame buffer update  |

At N = 100, brute-force computes 4,950 pairwise interactions. With vectorized NumPy, each
interaction requires ~5 floating-point operations (displacement, distance, softened force,
accumulation), totaling ~25,000 FLOPs — trivially within budget on any modern CPU.

### 6.2 Benchmarking Mode (N = 100–1000+)

In benchmarking mode, visualization is disabled. The target is to measure raw computational
throughput:

- **Brute-force**: Expected to hit the 33 ms wall-clock limit around N = 300–500 (depending
  on hardware and vectorization efficiency).
- **Barnes-Hut**: Expected to sustain 33 ms per step up to N = 1000–3000 with $\theta = 0.5$.

The benchmarking suite records:

- Wall-clock time per step as a function of N
- Scaling exponent (linear regression of $\log t$ vs. $\log N$)
- Force accuracy (RMS relative error vs. direct summation) for Barnes-Hut at various $\theta$

### 6.3 Non-Goals

The following are explicitly out of scope for performance:

- GPU acceleration (concept node `spatial_trees` notes this as a future direction)
- Multi-threading or multiprocessing
- SIMD intrinsics or Cython/Numba JIT compilation
- Adaptive time-stepping (constant $\Delta t$ only in initial implementation)

---

## 7. Output Format Specification

### 7.1 Structured Results: JSON

Configuration, metadata, and summary statistics are stored as JSON files:

```json
{
  "simulation": {
    "n_bodies": 100,
    "dt": 0.01,
    "n_steps": 10000,
    "integrator": "leapfrog",
    "force_method": "brute_force",
    "G": 1.0,
    "epsilon": 0.01
  },
  "initial_conditions": {
    "generator": "random_cluster",
    "seed": 42
  },
  "conservation": {
    "energy_relative_error_max": 1.2e-5,
    "energy_relative_error_mean": 3.4e-6,
    "momentum_drift": [1.1e-16, 2.3e-16],
    "angular_momentum_relative_error_max": 8.7e-6
  }
}
```

### 7.2 Bulk Trajectory Data: NumPy Arrays

Trajectory data (positions, velocities, accelerations at each timestep) is stored as NumPy
`.npy` files for efficiency:

| File                   | Shape               | Dtype    | Description                      |
|------------------------|---------------------|----------|----------------------------------|
| `positions.npy`        | `(n_steps, N, 2)`   | float64  | Position vectors at each step    |
| `velocities.npy`       | `(n_steps, N, 2)`   | float64  | Velocity vectors at each step    |
| `energies.npy`         | `(n_steps,)`         | float64  | Total energy at each step        |
| `momenta.npy`          | `(n_steps, 2)`       | float64  | Total linear momentum (x, y)    |
| `angular_momentum.npy` | `(n_steps,)`         | float64  | Total angular momentum (scalar) |

Files exceeding 100 MB are tracked via Git LFS (`.gitattributes` already configured for
`*.npy` files — see `results/phase1/repo_analysis.md` Section 5).

### 7.3 Visualization: Matplotlib Figures

All plots are saved in dual format:

- **PNG at 300 DPI** for quick inspection and documentation embedding
- **PDF** for publication-quality vector graphics

Standard figure set:

| Figure                       | Description                                       |
|------------------------------|---------------------------------------------------|
| `orbit_traces.png/pdf`       | Particle trajectories over full simulation         |
| `energy_conservation.png/pdf`| Relative energy error vs. time                     |
| `momentum_conservation.png/pdf` | Linear and angular momentum drift vs. time     |
| `scaling_benchmark.png/pdf`  | Wall-clock time vs. N for brute-force and BH       |
| `force_accuracy.png/pdf`     | Barnes-Hut RMS force error vs. $\theta$            |

Figures are written to the `figures/` directory at the repository root.

---

## 8. Concept Tree Integration

The implementation plan directly maps to the ConceptEvolve tree
(`results/concept_evolve/tree/index.json`):

### 8.1 Implementation Dependency Graph

```
  particle_data_structures (003)
            |
            v
    force_computation (001) <--- spatial_trees (004)
            |
            v
  numerical_integration (002)
            |
            v
    conservation_laws (007)
            |
            v
  validation_benchmarks (006)
            |
            v
      visualization (005)
```

### 8.2 Concept-to-Module Mapping

| Concept Node               | Source Module(s)            | Key Deliverable                    |
|----------------------------|-----------------------------|------------------------------------|
| `particle_data_structures` | `src/bodies.py`             | Body dataclass, System container   |
| `force_computation`        | `src/forces/brute_force.py` | $O(N^2)$ pairwise gravity          |
| `spatial_trees`            | `src/forces/barnes_hut.py`  | Quadtree + BH force evaluation     |
| `numerical_integration`    | `src/integrators.py`        | Leapfrog, Yoshida 4th-order        |
| `conservation_laws`        | `src/diagnostics.py`        | Energy, momentum, angular momentum |
| `validation_benchmarks`    | `benchmarks/`, `tests/`     | Kepler test, scaling plots         |
| `visualization`            | `src/visualization.py`      | Orbit plots, conservation plots    |

### 8.3 Walk Path Alignment

The concept tree walk paths (`results/concept_evolve/tree/walk_paths.json`) confirm this
ordering. The primary implementation path aligns with walk path index 1:

```
force_computation -> numerical_integration -> conservation_laws -> validation_benchmarks
```

Extended with the data structures prerequisite and visualization endpoint, this gives the
full pipeline specified in Section 1.

---

## 9. Summary of Scope Decisions

| Decision                  | Choice                          | Key Rationale                         |
|---------------------------|---------------------------------|---------------------------------------|
| Dimensionality            | 2D                              | Simpler viz; same algorithm classes   |
| Body count                | N = 2 to 1000+                  | Validation through scaling tests      |
| Force model               | Newtonian + Plummer softening   | Physical + numerically stable         |
| Integrators               | Leapfrog (2nd), Yoshida (4th)   | Symplectic: bounded energy error      |
| Conservation monitoring   | E, p, L every step              | Primary correctness diagnostic        |
| Real-time target          | $\geq$ 30 steps/s for N $\leq$ 100 | Interactive exploration          |
| Scaling target            | N = 1000 with Barnes-Hut        | Demonstrate $O(N \log N)$             |
| Output: config/stats      | JSON                            | Human-readable, structured            |
| Output: trajectories      | NumPy `.npy`                    | Efficient binary, large-array native  |
| Output: figures           | PNG 300 DPI + PDF               | Inspection + publication quality      |
| Language                  | Python (NumPy, matplotlib)      | Rapid development, ecosystem support  |

---

## 10. References

- [barnes1986] Barnes, J. & Hut, P. (1986). "A hierarchical O(N log N) force-calculation
  algorithm." *Nature*, 324(6096), 446–449.
- [pfalzner1996] Pfalzner, S. & Gibbon, P. (1996). *Many-Body Tree Methods in Physics*.
  Cambridge University Press.
- [aarseth2003] Aarseth, S.J. (2003). *Gravitational N-Body Simulations*. Cambridge
  University Press.
- [hairer2006] Hairer, E., Lubich, C. & Wanner, G. (2006). *Geometric Numerical Integration*.
  Springer.

Full BibTeX entries are maintained in `sources.bib` at the repository root.
