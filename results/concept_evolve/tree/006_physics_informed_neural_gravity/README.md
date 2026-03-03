# Physics-Informed Neural Gravity

## Topic Context

Physics-Informed Neural Networks (PINNs) represent a paradigm shift in computational physics: instead of discretizing PDEs on a grid, the solution is parameterized as a neural network, and the PDE is enforced via a physics loss term computed using automatic differentiation. For gravity, the relevant PDE is Poisson's equation: nabla^2 Phi = 4*pi*G*rho.

The PINN Gravity Model (PINN-GM) has gone through three generations. Gen III addresses failure modes including spectral bias (difficulty learning high-frequency features) and training instability. PINNs have been applied to gravity field modeling of asteroids, planetary bodies, and Earth's geoid.

### Key Ideas
- Neural network as continuous potential field representation
- Physics loss via automatic differentiation of Poisson's equation
- Data-efficient: physics constraint acts as strong regularizer
- Compact representation vs spherical harmonics

### Cross-Domain Connections
- Regularization theory (physics loss as structured prior)
- GRINN: PINN for hydrodynamics with self-gravity
- Geoid modeling: PINNs applied to Earth's gravity field

## Implementation Backlog

- [ ] Implement MLP potential representation
- [ ] Compute Laplacian via autograd
- [ ] Implement combined data + physics loss
- [ ] Train on 2D mass distribution
- [ ] Compare with analytical potential for simple shapes
- [ ] Test extrapolation outside training domain
- [ ] Experiment with loss weighting lambda
- [ ] Extend to time-dependent potential (moving masses)
