# ConceptEvolve Steering Notes

**Date:** 2026-03-03  
**Source topic:** "create a minimal gravity sim"  
**Concepts generated:** 12  
**Walk paths:** 22  

## Steering Directions

### Direction 1: Symplectic Integrator Zoo with Energy Dashboard (PRIORITIZED)

**Description:** Build a collection of integrators (Euler, Verlet, Leapfrog, optionally Yoshida 4th-order) with rigorous energy conservation monitoring at every timestep. The energy drift dashboard makes the invisible (conservation properties) visible and serves as the primary correctness metric throughout the project.

**Rubric items informed:** item_006, item_007, item_011, item_012, item_017

**Rationale for prioritization:** This direction is the backbone of the rubric. Every phase depends on having correct, well-characterized integrators. The walk paths `[symplectic_leapfrog_integrator, verlet_position_integration, energy_drift_monitor]` and `[symplectic_leapfrog_integrator, adaptive_timestep_control, energy_drift_monitor]` confirm that the integrator-energy pipeline is the highest-connectivity subgraph in the concept tree. Starting here maximizes downstream reuse and enables meaningful comparisons in Phase 4 experiments.

### Direction 2: Barnes-Hut Spatial Hierarchy + Performance Scaling

**Description:** Implement the Barnes-Hut quadtree algorithm as the primary optimization beyond O(N^2). Focus on correctness (force accuracy vs theta parameter) and demonstrable scaling improvement. This is the classical approach and the most well-characterized in the literature.

**Rubric items informed:** item_009, item_013, item_018, item_021

**Rationale:** The walk path `[barnes_hut_spatial_hierarchy, gpu_compute_shader_parallelism, verlet_position_integration, energy_drift_monitor]` shows Barnes-Hut as a gateway node connecting performance optimization to integration and monitoring. It has the highest fanout in the concept tree adjacency graph, meaning it unlocks the most downstream exploration paths.

### Direction 3: Adaptive Timestep Control with Energy Feedback

**Description:** Use closest-approach distance or maximum acceleration as the adaptive timestep criterion, with energy drift as the feedback signal. This connects the integration (Direction 1) and spatial hierarchy (Direction 2) via the walk path `[adaptive_timestep_control, energy_drift_monitor]`.

**Rubric items informed:** item_015, item_016, item_017

**Rationale:** Adaptive timestepping is necessary for physical correctness in close encounters (which also trigger collisions). The concept tree shows `adaptive_timestep_control` directly linked to `energy_drift_monitor`, confirming that energy conservation is the natural quality signal for timestep adaptation. This is the bridge between accuracy and performance that makes the solar system and collapse scenarios (items 019, 020) viable.

## Priority Ranking

1. **Symplectic Integrator Zoo** — Foundation for everything; highest concept-tree connectivity
2. **Barnes-Hut Spatial Hierarchy** — Primary performance unlock; highest fanout node
3. **Adaptive Timestep Control** — Bridge between accuracy and performance; enables physical scenarios

## Deferred Directions

The following concept-tree directions are intellectually interesting but out of scope for the "minimal" gravity sim rubric:
- GPU compute shader parallelism (WebGPU) — would require a different platform entirely
- GNN/physics-informed neural approaches — research novelty but unnecessary for rubric
- Emergent gravity from swarm rules — scientifically fascinating but tangential
- Fast multipole expansion — overkill for N<2000 regime the rubric targets
