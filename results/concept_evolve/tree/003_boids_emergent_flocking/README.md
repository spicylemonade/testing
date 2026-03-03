# Boids Emergent Flocking

## Topic Context

Craig Reynolds' 1986 Boids algorithm is one of the most celebrated examples of emergent complexity from simple rules. Each boid (bird-oid) follows three local rules: separation, alignment, and cohesion. No central controller exists; the flock self-organizes from purely local interactions.

The deep connection to gravity: the cohesion rule (steer toward center of mass of neighbors) is mathematically identical to a gravity-like attraction. Separation acts as a short-range repulsive force. Together, they create an effective potential remarkably similar to the Lennard-Jones potential used in molecular dynamics.

### Key Ideas
- Emergent complexity from simple local rules
- Three forces: separation (repulsion), alignment (velocity matching), cohesion (attraction)
- Spatial neighbor lookup is the computational bottleneck (same as N-body)
- KD-trees and spatial hashing accelerate neighbor queries

### Cross-Domain Connections
- Gravity simulation (cohesion = gravity, separation = softening)
- Molecular dynamics (Lennard-Jones potential = separation + cohesion)
- Drone swarm control (bio-inspired flocking for UAV coordination)

## Implementation Backlog

- [ ] Implement classic three-rule boids in 2D
- [ ] Add spatial hashing for neighbor lookup
- [ ] Replace cohesion with inverse-square gravity
- [ ] Tune attraction/repulsion weights for stable clusters
- [ ] Compare emergent dynamics with Newtonian N-body
- [ ] Measure cluster statistics (size distribution, lifetime)
- [ ] Add obstacle avoidance rule
- [ ] Visualize with color-coded velocity vectors
