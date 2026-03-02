# GRAPH_LAYOUT_ISOMORPHISM

Force-directed graph layout algorithms (Fruchterman-Reingold, ForceAtlas2) ARE N-body simulations with modified force laws. A gravity sim with repulsive short-range forces and attractive edge-spring forces becomes a graph visualization engine.

## Mathematical Formalization

ForceAtlas2: F_repulsive(i,j) = k_r * m_i * m_j / |r_ij|^2 (Coulomb repulsion).  F_attractive(i,j) = k_a * |r_ij| for (i,j) in E (Hooke spring).  This is gravity with sign-flipped short-range + edge-only long-range.

## Analogical Connections

- Barnes-Hut for gravity <-> Barnes-Hut in Gephi's ForceAtlas2 (same algorithm, different domain)
- Gravitational collapse <-> graph clustering (dense subgraphs attract each other)
- Escape velocity <-> graph disconnection (weakly connected nodes drift away)

## Implementation Hypothesis

Modify compute_forces() to accept a force_law parameter. Add 'repulsive_gravity' and 'spring_attraction' laws. Feed an adjacency list. Reuse the entire simulation loop. ~40 lines of glue code.

## Experiment Seed

Load a small social network (Zachary's karate club, 34 nodes) and lay it out using the gravity sim engine with repulsive + spring forces. Compare layout quality with NetworkX's spring_layout.
