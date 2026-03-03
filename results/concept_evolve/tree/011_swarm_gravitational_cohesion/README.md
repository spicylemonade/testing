# Swarm Gravitational Cohesion

## Topic Context

Can Newtonian gravity emerge from purely local agent rules? This concept explores the boundary between agent-based modeling (artificial life) and fundamental physics. Reynolds' original boids paper noted that cohesion produced "gravity-like" behavior. Taking this seriously, we can ask whether specific local interaction rules recover the inverse-square law as an emergent phenomenon.

This connects to Verlinde's entropic gravity hypothesis (2011), which proposes that gravity itself is an emergent force arising from information-theoretic principles. While speculative in physics, the computational question is concrete: what minimal local rules produce N-body dynamics indistinguishable from Newtonian gravity?

### Key Ideas
- Gravity as emergent from local attraction + repulsion rules
- Agent sensing radius as an analog of gravitational horizon
- Self-organization produces hierarchical structure (clusters, filaments)
- Noise acts as temperature, enabling thermodynamic analogy

### Cross-Domain Connections
- Entropic gravity (Verlinde): gravity as emergent force
- Chemotaxis: aggregation from local gradients
- Economic gravity models: spatial attraction by mass/distance

## Implementation Backlog

- [ ] Implement agent-based model with configurable attraction/repulsion
- [ ] Add Newtonian N-body reference simulation
- [ ] Compute radial density profiles for both
- [ ] Compare velocity dispersion profiles
- [ ] Measure power spectrum of density fluctuations
- [ ] Sweep parameter space: attraction strength, sensing radius, noise
- [ ] Identify parameter regime closest to Newtonian gravity
- [ ] Test whether stable binary orbits emerge from swarm rules
