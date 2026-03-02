# GRADIENT_DESCENT_DUALITY

The deep structural isomorphism between gravitational dynamics and optimization. A body falling in a potential field IS gradient descent. Adding kinetic energy (momentum) IS momentum-SGD. This duality makes a gravity sim a physical optimizer and vice versa.

## Mathematical Formalization

Gravitational: a = -nabla Phi(x), v' = v + a*dt, x' = x + v*dt.  SGD+momentum: g = nabla L(theta), v' = mu*v - lr*g, theta' = theta + v'.  Isomorphism: Phi <-> L, x <-> theta, v <-> momentum_buffer, dt <-> lr, G*m <-> 1.

## Analogical Connections

- Orbiting body <-> momentum-SGD oscillating around a minimum without converging
- Gravitational capture <-> convergence (losing kinetic energy to reach a bound state)
- Escape velocity <-> learning rate explosion (too much kinetic energy to stay bound)
- Lagrange points <-> saddle points in loss landscape (unstable equilibria)

## Implementation Hypothesis

Implement a 'GravityOptimizer' that uses the same leapfrog code to minimize an arbitrary scalar field. Show it finding the minimum of Rosenbrock's function. Conversely, visualize SGD trajectories as 'orbits' in loss space.

## Experiment Seed

Use the gravity sim engine to minimize f(x,y) = (1-x)^2 + 100(y-x^2)^2 (Rosenbrock). Add damping (friction) to convert orbits into convergence. Compare trajectory with standard Adam optimizer.
