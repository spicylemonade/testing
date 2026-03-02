# ConceptEvolve Steering Notes

**Generated**: 2026-03-02  
**Seed**: "create minimal gravity simulation"  
**Concept folders**: 7 (force_computation, numerical_integration, particle_data_structures, spatial_trees, visualization, validation_benchmarks, conservation_laws)

---

## 3 Concrete Steering Directions

### Direction 1: Symplectic-First Design
**Description**: Build all components around energy conservation guarantees by using symplectic integrators from the start.

**Rubric items informed**: item_008 (integrators), item_009 (conservation metrics), item_010 (Kepler validation), item_013 (Yoshida), item_017 (integrator comparison)

**Rationale**: Energy conservation is the single most important quality metric for gravitational N-body simulation. Symplectic methods guarantee bounded energy oscillation rather than secular drift. Building around this property from day one means every subsequent test and benchmark produces meaningful results.

### Direction 2: Vectorized Brute-Force as Ground Truth
**Description**: Implement a fully vectorized numpy O(N^2) force computation as the accuracy baseline before implementing tree codes.

**Rubric items informed**: item_007 (brute force), item_012 (Barnes-Hut), item_016 (scaling benchmark), item_018 (theta sweep)

**Rationale**: Barnes-Hut and other approximate methods require a ground truth to validate against. Direct summation with numpy broadcasting provides exact forces (within softening) and establishes the accuracy floor.

### Direction 3: Benchmark-Driven Development
**Description**: Implement standard test problems (Kepler, figure-eight, Plummer) before optimization work.

**Rubric items informed**: item_010 (Kepler validation), item_015 (initial conditions), item_019 (figure-eight test), item_020 (adaptive test)

**Rationale**: Having validated benchmarks early enables regression testing. Each optimization (Barnes-Hut, Yoshida, adaptive timestep) can be immediately tested against known-correct behavior.

---

## Priority

**Direction 1 (Symplectic-First) is prioritized** because:
1. It directly addresses the core scientific concern: accuracy of physical simulation
2. It enables meaningful interpretation of all subsequent experiments
3. It's validated by the literature: Hairer et al. (2006) [hairer2006] prove that symplectic methods are essential for long-term Hamiltonian dynamics
4. The rubric's most stringent acceptance criteria all involve energy conservation bounds

Directions 2 and 3 are natural consequences of Direction 1 -- once we commit to symplectic integration, we need ground-truth forces (Direction 2) and benchmark problems (Direction 3) to validate the conservation properties.

---

## Concept Tree Walk Paths

The most productive walk path through the concept tree for implementation order:

```
particle_data_structures -> force_computation -> numerical_integration -> conservation_laws -> validation_benchmarks -> visualization
```

This path follows the natural data flow of the simulation: data structures hold state, forces compute accelerations, integrators advance time, conservation laws validate, benchmarks test, visualization presents.
