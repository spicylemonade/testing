# Requirements: Minimal Gravity Simulator

**Date:** 2026-03-03  
**Rubric Item:** item_005  

## 1. Target Language and Platform

- **Language:** Python 3.10+
- **Platform:** Linux (development), cross-platform compatible
- **Core dependencies:** NumPy (vectorized computation), SciPy (optional for reference solutions)
- **Visualization:** Matplotlib + Seaborn (publication figures), Matplotlib.animation (animated output)
- **Testing:** pytest

**Rationale:** Python with NumPy provides the best balance of development speed, readability, and adequate performance for the target scale (N <= 2000). The rubric requires Python explicitly (`src/gravity_sim.py`).

## 2. Particle Count Requirements

| Scenario | Minimum N | Target N | Max N |
|---|---|---|---|
| Unit tests | 1-3 | 5 | 10 |
| Baseline benchmarks | 10 | 50-200 | 500 |
| Scaling experiments | 50 | 500-1000 | 2000 |
| Physical scenarios | 4 (solar system) | 200 (collapse) | 500 |

**Minimum supported:** N >= 100 (configurable)
**Design target:** Correct and performant up to N = 2000

## 3. Required Features

### 3.1 Gravitational Attraction
- Newtonian pairwise gravity: F_ij = G * m_i * m_j * (r_j - r_i) / |r_j - r_i|^3
- Gravitational softening: F_ij = G * m_i * m_j * (r_j - r_i) / (|r_j - r_i|^2 + epsilon^2)^{3/2}
- Configurable G, softening epsilon
- 2D simulation (x, y coordinates)

### 3.2 Multiple Integration Methods
- Forward Euler (baseline)
- Velocity Verlet (Stormer-Verlet)
- Leapfrog (kick-drift-kick symplectic)
- Selectable via command-line argument or function parameter

### 3.3 Force Computation Methods
- Direct O(N^2) pairwise summation (baseline)
- Barnes-Hut quadtree O(N log N) approximation (configurable theta)

### 3.4 Collision Detection and Response
- Elastic or inelastic collision modes (configurable)
- Bodies within softening radius merge or bounce
- Collision event logging

### 3.5 Adaptive Timestepping
- Based on minimum pairwise distance or maximum acceleration
- Must maintain energy conservation within tolerance

### 3.6 Energy and Momentum Tracking
- Total energy (kinetic + gravitational potential) at each timestep
- Momentum conservation verification
- Energy drift reporting

### 3.7 Visualization
- 2D scatter plot animation of body positions
- Static multi-panel figures for time series
- Export to GIF and PNG/PDF

## 4. Performance Targets

| Metric | Target | Method |
|---|---|---|
| Interactive animation | > 30 FPS | N=100, any integrator |
| Baseline timestep | < 50 ms | N=100, O(N^2), Euler |
| Barnes-Hut advantage | > 2x faster | N=500, theta=0.5 |
| Energy conservation (leapfrog) | < 0.1% drift | N=50, 10000 steps |
| Scaling | O(N^2) verified | Exponent in [1.8, 2.2] |

## 5. Integration Method Ranking

Methods ranked by complexity vs. accuracy trade-off, informed by the literature:

| Rank | Method | Order | Symplectic | Force Evals/Step | Energy Drift (long-term) | Complexity |
|---|---|---|---|---|---|---|
| 1 | **Leapfrog (KDK)** | 2 | Yes | 1 | Bounded oscillation | Low |
| 2 | **Velocity Verlet** | 2 | Yes | 1 | Bounded oscillation | Low |
| 3 | Forward Euler | 1 | No | 1 | Linear (secular) growth | Minimal |
| 4 | RK4 | 4 | No | 4 | Slow secular growth | Medium |

**Selection rationale:**

Leapfrog and Velocity Verlet are ranked highest because they provide second-order accuracy with symplectic structure at the cost of only one force evaluation per step. As demonstrated by Gladman et al. \cite{gladman1991}, symplectic integrators maintain bounded energy oscillation over arbitrarily long integrations, unlike non-symplectic methods which exhibit secular energy drift.

Forward Euler is included as a pedagogical baseline to demonstrate why symplecticity matters, following the analysis in Marsden and West \cite{marsden2001} showing that variational integrators naturally preserve geometric structure.

RK4 is excluded from implementation scope as it requires 4 force evaluations per step without symplectic properties, making it dominated by leapfrog for gravitational N-body problems. This is consistent with the findings of Chambers and Murison \cite{chambers1999}, who showed that pseudo-high-order symplectic methods outperform classical RK for planetary dynamics.

## 6. Directory Structure

```
src/
  gravity_sim.py       # Core simulation engine (all integrators)
  barneshut.py         # Barnes-Hut quadtree force approximation
  visualize.py         # Matplotlib-based visualization
tests/
  test_physics.py      # Physics correctness tests
scenarios/
  solar_system.json    # Inner solar system scenario
results/
  baseline/            # Euler O(N^2) results
  verlet/              # Velocity Verlet results
  leapfrog/            # Leapfrog results
  barneshut/           # Barnes-Hut results
  adaptive/            # Adaptive timestep results
  collisions/          # Collision scenario results
  experiments/         # Comparative experiments
figures/               # All publication-grade figures
sources.bib            # Bibliography
```

## 7. Deterministic Reproducibility

- All random initial conditions use `numpy.random.seed(42)`
- All outputs are deterministic given the same parameters
- Simulation parameters stored in JSON alongside results

## References

- \cite{gladman1991} Gladman, Duncan, Candy (1991). Symplectic integrators for long-term celestial mechanics.
- \cite{marsden2001} Marsden, West (2001). Discrete mechanics and variational integrators.
- \cite{chambers1999} Chambers, Murison (1999). Pseudo-High-Order Symplectic Integrators.
- \cite{barnes1986} Barnes, Hut (1986). A hierarchical O(N log N) force-calculation algorithm.
- \cite{verlet1967} Verlet (1967). Computer experiments on classical fluids.
