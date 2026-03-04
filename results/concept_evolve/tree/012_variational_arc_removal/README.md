# Variational Arc Removal

## Topic Context

The upper bound on B_u comes from constructing specific simply connected domains with small covering radius. The standard approach is to start with a disk and remove arcs (slits). Each arc removal reduces the covering radius.

The Hadamard variational formula gives the rate of change of the conformal radius under small perturbations of the domain boundary. This provides the gradient information needed for optimization.

## Variational Framework

Model the arc removal as a continuous process:
- Time t ∈ [0,1] parameterizes the "amount" of boundary removed
- At each time, choose where to place the next infinitesimal slit
- The conformal radius R(t) decreases
- The goal: find the removal path that reaches the smallest R(1)

This is an optimal control problem where:
- State: the domain D_t (or its conformal map)
- Control: the position and direction of the next arc
- Cost: the final covering radius R(1)

## Connection to Other Concepts

- Concept 001: The variational process should converge to harmonically symmetric configurations
- Concept 003: Arc removal is a discrete Loewner chain; the energy of removal relates to Loewner energy
- Concept 006: OT provides a distance metric between successive domains

## Implementation Backlog

1. **[P0]** Implement Hadamard variation formula for disk minus slits
2. **[P1]** Implement greedy arc removal algorithm
3. **[P2]** Compare with known extremal configurations
4. **[P3]** Study the continuous limit (PDE for optimal removal)
5. **[P3]** Prove convergence to harmonically symmetric configurations
