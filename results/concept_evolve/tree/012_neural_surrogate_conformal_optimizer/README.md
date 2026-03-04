# 012: Neural Surrogate Conformal Optimizer

## Topic Context

Physics-informed neural networks (PINNs) can learn conformal maps by enforcing the Cauchy-Riemann equations as part of the loss function. Once trained, the neural surrogate provides a differentiable approximation to the conformal map, enabling gradient-based optimization of the Bloch radius.

This approach bridges machine learning and classical complex analysis: the neural network explores the vast space of univalent functions, while the Bloch radius objective guides the search toward extremal configurations.

## Key Technical Components

- **Complex-valued neural networks**: Split architecture (separate real/imaginary) or holomorphic activation functions
- **PINN loss**: Cauchy-Riemann residual + boundary conditions + univalence regularization
- **Domain parameterization**: B-spline or Fourier series description of boundary
- **Automatic differentiation**: For computing f'(z) and gradients of B_f

## Implementation Backlog

1. [ ] Implement complex-valued neural network in PyTorch
2. [ ] Design PINN loss: Cauchy-Riemann + boundary + univalence
3. [ ] Train on known case: conformal map from disk to strip
4. [ ] Verify accuracy against analytical solution
5. [ ] Parameterize domain boundaries with B-splines (10-20 control points)
6. [ ] Implement Bloch radius computation from neural map
7. [ ] Set up end-to-end differentiable optimization: domain params -> NN -> B_f
8. [ ] Run optimizer, compare discovered domains with known candidates
9. [ ] Analyze convergence and generalization across domain families
