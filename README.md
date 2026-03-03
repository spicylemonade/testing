# N-Body Gravity Simulator

A minimal yet comprehensive N-body gravitational simulator written in Python, implementing multiple numerical integration schemes, Barnes-Hut tree-based force approximation, adaptive timestepping, and collision handling. This project was developed as an AI-guided research exploration, systematically working through a 25-item rubric covering literature review, concept evolution, implementation, experimentation, and documentation.

The simulator is designed for educational and research use, emphasizing physical correctness (symplectic integration, energy conservation) over raw performance, while still demonstrating algorithmic scaling improvements from O(N^2) direct summation to O(N log N) Barnes-Hut approximation.

## Installation

**Requirements:** Python 3.8+ with the following packages:

```
numpy
matplotlib
seaborn
pytest        # for running tests
```

Install dependencies:

```bash
pip install numpy matplotlib seaborn pytest
```

No additional compilation or build steps are needed. The entire simulator runs as pure Python with NumPy vectorization.

## Usage

### Running a Simulation

The main entry point is `src/gravity_sim.py`, which provides a full CLI:

```bash
# Basic Euler integration, 50 bodies, 1000 steps
python src/gravity_sim.py --N 50 --steps 1000 --dt 0.01 --integrator euler --output results/baseline/

# Leapfrog integrator (recommended for energy conservation)
python src/gravity_sim.py --N 100 --steps 5000 --dt 0.01 --integrator leapfrog --output results/leapfrog/

# Velocity Verlet integrator
python src/gravity_sim.py --N 100 --steps 5000 --dt 0.01 --integrator verlet --output results/verlet/

# Adaptive timestep with leapfrog
python src/gravity_sim.py --N 100 --steps 5000 --dt 0.01 --integrator leapfrog --adaptive --adaptive-eta 0.01 --output results/adaptive/

# Collision detection (merge mode)
python src/gravity_sim.py --N 20 --steps 500 --dt 0.01 --integrator leapfrog --collisions --collision-mode merge --output results/collisions/

# Load a scenario file (e.g., solar system)
python src/gravity_sim.py --scenario scenarios/solar_system.json --steps 50000 --integrator leapfrog --output results/experiments/solar_system/
```

**Key CLI arguments:**

| Argument | Default | Description |
|----------|---------|-------------|
| `--N` | 50 | Number of bodies |
| `--steps` | 1000 | Number of timesteps |
| `--dt` | 0.01 | Timestep size |
| `--integrator` | euler | Integration method: `euler`, `verlet`, or `leapfrog` |
| `--G` | 1.0 | Gravitational constant |
| `--softening` | 0.1 | Gravitational softening parameter |
| `--seed` | 42 | Random seed for reproducibility |
| `--output` | results/baseline/ | Output directory |
| `--scenario` | None | JSON scenario file path |
| `--collisions` | off | Enable collision detection |
| `--collision-mode` | merge | Collision response: `merge` or `bounce` |
| `--adaptive` | off | Enable adaptive timestepping |
| `--adaptive-eta` | 0.01 | CFL safety factor for adaptive dt |

### Visualization

Generate animations, snapshots, and energy plots from simulation output:

```bash
# Animated GIF
python src/visualize.py results/baseline/ --output figures/animation.gif --fps 30

# Static snapshot
python src/visualize.py results/leapfrog/ --static --output figures/snapshot.png --title "Leapfrog N=100"

# Energy drift plot
python src/visualize.py results/baseline/ --energy --output figures/energy.png
```

### Running Tests

```bash
pytest tests/test_physics.py -v
```

The test suite contains 13 tests covering force symmetry, zero-force edge cases, energy computation, momentum conservation, Keplerian orbit accuracy, and leapfrog energy bounds.

## Directory Structure

```
.
├── src/
│   ├── gravity_sim.py      # Core simulator: integrators, forces, energy, collisions, CLI
│   ├── barneshut.py         # Barnes-Hut quadtree for O(N log N) force approximation
│   └── visualize.py         # Matplotlib-based visualization: animations, snapshots, plots
├── tests/
│   └── test_physics.py      # 13 physics correctness tests
├── scenarios/
│   └── solar_system.json    # Inner solar system (Sun + Mercury, Venus, Earth, Mars)
├── results/
│   ├── baseline/            # Euler integrator baseline (N=50, 1000 steps)
│   ├── verlet/              # Velocity Verlet results
│   ├── leapfrog/            # Leapfrog results (10000 steps, 0.006% drift)
│   ├── barneshut/           # Barnes-Hut performance benchmarks
│   ├── adaptive/            # Adaptive timestep results and comparison
│   ├── collisions/          # Collision detection logs (19 events)
│   ├── experiments/         # Systematic experiments: integrator sweep, scaling, theta sweep
│   │   ├── integrator_accuracy.csv
│   │   ├── scaling.csv
│   │   ├── theta_sweep.csv
│   │   ├── solar_system/
│   │   ├── collapse/
│   │   └── solar_system_validation.md
│   ├── findings.md          # 2077-word synthesis of all experimental results
│   ├── concept_evolve/      # ConceptEvolve artifacts: concept cards, walk paths, summaries
│   └── final_checklist.md   # Final verification checklist
├── figures/                 # Publication-grade figures (PNG 300 DPI + PDF)
│   ├── baseline_scaling.png     # O(N^2) verification
│   ├── integrator_comparison.png # Energy drift vs dt for 3 integrators
│   ├── scaling_comparison.png   # Direct vs Barnes-Hut scaling
│   ├── solar_system_orbits.png  # Orbital traces
│   ├── collapse_sequence.png    # Gravitational collapse time series
│   └── theta_tradeoff.png      # Barnes-Hut theta accuracy-speed curve
├── sources.bib              # 22 BibTeX entries
├── research_rubric.json     # 25-item research rubric with status tracking
└── README.md                # This file
```

## Key Findings

The full experimental analysis is documented in [`results/findings.md`](results/findings.md). Highlights:

**Integrator comparison.** Symplectic integrators (Velocity Verlet, Leapfrog) are approximately 40,000x better than forward Euler for energy conservation at identical computational cost (one force evaluation per step). Leapfrog with dt=0.01 maintains 0.006% energy drift over 10,000 steps, while Euler diverges to >100% drift. Both symplectic methods exhibit O(dt^2) convergence, consistent with theoretical predictions.

**Barnes-Hut scaling.** The Barnes-Hut quadtree implementation achieves the expected O(N log N) algorithmic complexity (fitted exponent 1.34 vs 1.67 for direct summation). However, pure Python tree traversal overhead means the crossover point where Barnes-Hut outperforms NumPy-vectorized direct summation is at approximately N=5,000. For smaller N, the vectorized O(N^2) approach dominates due to constant-factor advantages.

**Physical validation.** The solar system model reproduces inner planet orbital periods within 2.1% of known values (Mercury 2.1%, Venus 0.3%, Earth and Mars < 0.1%). A gravitational collapse scenario matches the analytical free-fall timescale within 6%, consistent with Binney & Tremaine's prediction.

**Adaptive timestepping.** A CFL-based adaptive timestep criterion reduces total force evaluations by 50% compared to fixed timestep, while maintaining 0.003% energy conservation over 10,000 effective steps.

**Collision handling.** Inelastic merging correctly handles 19 collision events among 20 bodies in a confined scenario, reducing the system to a single merged body while conserving momentum.

## References

The project draws on 22 academic sources documented in [`sources.bib`](sources.bib), including foundational works by Aarseth (2003), Barnes & Hut (1986), Verlet (1967), and Binney & Tremaine (2008). See [`results/findings.md`](results/findings.md) for inline citations and quantitative comparisons against published results.

## Concept Evolution

This project used the ConceptEvolve framework to systematically explore the design space. Starting from 12 seed concepts, the exploration generated 22 walk paths across classical simulation, neural/learned, and adaptive optimization clusters. Five concepts were adopted (Barnes-Hut, Leapfrog, Verlet, Adaptive Timestep, Energy Monitor), five were deferred as out of scope (FMM, GPU, GNN, PINN, hybrid), and two were discarded as inapplicable (Boids, Swarm). The full concept tree summary is in [`results/concept_evolve/tree/final_summary.md`](results/concept_evolve/tree/final_summary.md).
