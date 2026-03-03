# Multipole-Neural Hybrid

## Topic Context

Pure neural approaches to physics simulation suffer from accumulating errors during rollout and lack of physical guarantees. Pure classical approaches (Barnes-Hut, FMM) have well-understood error bounds but may require high expansion orders for accuracy. The hybrid approach takes the best of both worlds: use a cheap classical approximation as a backbone and train a neural network to correct the residual error.

This is directly analogous to residual learning in deep learning (ResNets): it's easier to learn a small correction than the full function. The classical backbone provides a strong inductive bias, and the neural correction handles the aspects that are hard to capture with low-order multipoles (e.g., non-spherical mass distributions, close encounters).

### Key Ideas
- Classical force approximation as backbone (strong inductive bias)
- Neural network learns only the residual correction
- Residual is smaller and smoother than the full force, easier to learn
- Generalizes better than pure neural approaches

### Cross-Domain Connections
- ResNets in deep learning (residual learning principle)
- Kalman filtering (prediction + correction)
- Boosting in ML (weak learner + correction)

## Implementation Backlog

- [ ] Implement Barnes-Hut with theta=1.0 as backbone
- [ ] Generate training data: (F_BH, F_direct) pairs
- [ ] Train MLP on force residual
- [ ] Evaluate hybrid accuracy vs pure BH and direct
- [ ] Test generalization to different N
- [ ] Experiment with different input features for the MLP
- [ ] Add local density and velocity dispersion as features
- [ ] Compare training efficiency with pure GNN approach
