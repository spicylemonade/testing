# Minimal Gravitational N-Body Simulation

A pedagogical gravitational N-body simulator in Python + NumPy, implementing brute-force
and Barnes-Hut force calculation, symplectic integration (leapfrog, Yoshida 4th-order),
adaptive time-stepping, and conservation monitoring.

## Installation

Requires Python 3.10+ and the following packages:

```bash
pip install numpy matplotlib seaborn scipy pytest pytest-cov
```

No additional build steps are needed. The code is pure Python with NumPy.

## Project Structure

| Module | Description |
|--------|-------------|
| `src/bodies.py` | `System` dataclass (SoA layout), initial condition generators: `kepler_orbit()`, `circular_ring()`, `plummer_sphere()` |
| `src/forces.py` | Brute-force O(N²) gravitational force with Plummer softening: loop-based and vectorized variants |
| `src/forces_optimized.py` | Symmetric pair force computation (Newton's 3rd law, upper-triangle) |
| `src/tree.py` | 2D Barnes-Hut quadtree: `build_tree()`, `compute_forces_tree()` with configurable theta |
| `src/integrators.py` | `euler_step()`, `leapfrog_step()`, `yoshida4_step()`, `adaptive_leapfrog()` |
| `src/metrics.py` | `kinetic_energy()`, `potential_energy()`, `total_energy()`, `total_momentum()`, `angular_momentum()`, `virial_ratio()` |
| `tests/` | 57 unit tests across 6 test files |
| `experiments/` | Experiment scripts: Kepler validation, adaptive dt, scaling/energy/Plummer/theta experiments |
| `figures/` | Publication-grade plots (PNG 300 DPI + PDF) |
| `results/` | Analysis documents, experiment data (JSON), and the [project report](results/report.md) |

## Usage

### Programmatic Example: Two-Body Kepler Orbit

```python
import numpy as np
from src.bodies import kepler_orbit
from src.forces import compute_forces_vectorized
from src.integrators import leapfrog_step
from src.metrics import total_energy

# Create a two-body system: eccentricity 0.5, semi-major axis 1.0
system = kepler_orbit(e=0.5, a=1.0)

# Integration parameters
G = 1.0
eps = 1e-4          # Plummer softening
dt = 0.001          # Time step
n_steps = 10000

# Record initial energy
E0 = total_energy(system, G, eps)

# Integrate with leapfrog
for _ in range(n_steps):
    system = leapfrog_step(system, compute_forces_vectorized, dt, G, eps)

# Check energy conservation
E_final = total_energy(system, G, eps)
print(f"Relative energy error: {abs((E_final - E0) / E0):.2e}")
```

### Using Barnes-Hut for Larger Systems

```python
from src.bodies import plummer_sphere
from src.tree import compute_forces_tree
from src.integrators import leapfrog_step

# N=500 Plummer sphere
system = plummer_sphere(N=500, seed=42)

# Barnes-Hut force with theta=0.5
def bh_force(pos, mass, G, eps):
    return compute_forces_tree(pos, mass, G, eps, theta=0.5)

# Integrate
for _ in range(100):
    system = leapfrog_step(system, bh_force, dt=0.01, G=1.0, eps=0.05)
```

### Using Yoshida 4th-Order Integrator

```python
from src.integrators import yoshida4_step

# Same setup as above, but with 4th-order accuracy
for _ in range(n_steps):
    system = yoshida4_step(system, compute_forces_vectorized, dt, G, eps)
```

### Running Experiments

```bash
# Kepler orbit validation
python experiments/kepler_validation.py

# Adaptive time-stepping demo
python experiments/adaptive_dt.py

# Full experiment suite (scaling, energy conservation, Plummer, theta sweep)
python experiments/run_all.py
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

## Key Results

- **Kepler validation**: |ΔE/E| = 2.63×10⁻⁷ over 10 orbital periods (leapfrog)
- **Convergence rates**: Leapfrog O(dt²), Yoshida4 O(dt⁴) — verified exactly
- **Adaptive dt**: 247,000× improvement for e=0.95 orbit vs fixed dt
- **Barnes-Hut**: θ≈0.5 gives ~10× speedup at 2-3% force error (N=1000)
- **Plummer relaxation**: 0.75% energy drift over 20 dynamical times, virial ratio → 1.0

See the full [project report](results/report.md) for detailed analysis and figures.

## References

See [`sources.bib`](sources.bib) for the complete bibliography (26 entries). Key references:

- Barnes & Hut (1986). A hierarchical O(N log N) force-calculation algorithm. *Nature*.
- Yoshida (1990). Construction of higher order symplectic integrators. *Physics Letters A*.
- Verlet (1967). Computer experiments on classical fluids. *Physical Review*.
- Rein & Liu (2012). REBOUND: An open-source multi-purpose N-body code. *A&A*.
- Springel (2005). The cosmological simulation code GADGET-2. *MNRAS*.

## License

Research/educational project.
