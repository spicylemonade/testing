# resolution_coupled_softening

## Context
Choose gravitational softening from the simulator's actual resolution - pixel footprint, patch size, or local cell width - instead of pretending one epsilon works at every zoom level. This borrows anti-aliasing and mesh-resolution logic from graphics and FEM so a minimal simulator degrades honestly when representation gets coarse.

## Domains
- computer_graphics
- geophysics
- astrophysics

## Mathematical Formalization
eps_i = max(eps_phys, k_screen * s_px(i), k_cell * h_cell(i)); a_i = sum_j G m_j r_ij / (||r_ij||^2 + eps_ij^2)^(3/2), with eps_ij = max(eps_i, eps_j)

## Closest Prior Art
- REBOUND: An open-source multi-purpose N-body code for collisional dynamics (`5240c4a18da2b6dcae3fbfa633c01bee1670d0a0`)
- Efficient parallel finite-element methods for planetary gravitation: DtN and multipole expansions (`973aaba20de052e555f2721ee9b1c47ddff95fef`)
- Momentum-conserving self-gravity in the phantom smoothed particle hydrodynamics code. Parallel dual tree traversal for the symmetric fast multipole method (`e30e52bdbc59b0847e73cd4141831bf1ce285a5b`)

## Novelty
The novelty is to bind the smoothing scale to representational limits rather than only to physical heuristics or density estimates.

## Differentiation
Adaptive softening in self-gravity codes is usually motivated by particle density or kernel support. Here the driver is what the simulator can honestly resolve and display, which is a different control signal.

## Experiment Seed
Run the same scene across repeated zoom-in and zoom-out cycles; compare stability, aliasing, and conservation metrics for fixed epsilon versus scale-aware epsilon.

## Implementation Backlog
1. Measure pixel, world, and cell scale per body.
2. Bind epsilon to the current representation scale.
3. Add an overlay showing effective epsilon.
4. Sweep zoom levels and compare artifact rates.
5. Separate pedagogical presets from physically faithful presets.

## Planned Paths
- `results/concept_evolve/tree/009_resolution_coupled_softening/concept.json`
- `results/concept_evolve/tree/009_resolution_coupled_softening/README.md`
- `results/concept_evolve/tree/009_resolution_coupled_softening/literature.json`
- `prototypes/minigrav/force/resolution_softening.py`
- `prototypes/minigrav/ui/softening_overlay.py`
