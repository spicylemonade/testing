# Graph Neural Particle Dynamics

## Topic Context

Graph Neural Networks have emerged as powerful tools for learning physical simulations directly from data. For particle systems like gravity, each particle becomes a node, and pairwise interactions become edges in a dynamically constructed graph. The GNN learns the interaction function (which is Newton's law of gravity) from trajectory data.

Recent advances include subequivariant GNNs that handle broken symmetries (gravity breaks full rotational symmetry by defining a preferred "down" direction), multi-scale architectures that mirror the hierarchical structure of Barnes-Hut trees, and physics-informed training losses that improve generalization.

### Key Ideas
- Dynamic interaction graph construction via radius cutoff or k-nearest neighbors
- Message passing learns pairwise force functions from data
- Equivariance constraints reduce data requirements
- Hierarchical multi-scale message passing improves long-range interactions

### Cross-Domain Connections
- Barnes-Hut as handcrafted multi-scale message passing
- Molecular dynamics force fields as hand-designed GNNs
- Social network dynamics as learned influence propagation

## Implementation Backlog

- [ ] Generate training data from classical 3-body integrator
- [ ] Build GNN with 2 message-passing layers
- [ ] Train on acceleration prediction
- [ ] Evaluate autoregressive rollout stability
- [ ] Test generalization to unseen particle counts
- [ ] Add Hamiltonian inductive bias (predict energy, derive forces)
- [ ] Implement subequivariant message passing for gravity
- [ ] Compare with classical integrator accuracy and speed
