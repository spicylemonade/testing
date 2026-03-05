# Steering Notes for Ramsey R(5,5) Bounds Research

## Overall Selected Bridge Chains
We will turn the following 3 bridge chains from `semantic_bridge.json` into experiments:
1. **Thermodynamic-ML-Information Chain** (gflownet_entropy_collapse -> spin_glass_partition_zeros -> semantic_compression_limit): Uses ML to learn the partition function, analyzed via statistical mechanics, to find the fundamental information-theoretic compression limit of Ramsey graphs.
2. **Quantum-Tensor-Statistical Chain** (quantum_walk_mixing_time -> tensor_network_contraction -> spin_glass_partition_zeros): Simulates a quantum walk using tensor networks to detect the thermodynamic phase transition of the Ramsey spin glass.
3. **Algebraic-Topological-Categorical Chain** (sos_diffusion_geometry -> algebraic_geometry_syzygies -> topological_graph_homology -> categorical_adjunction_obstruction): Relaxes the discrete problem continuously, studies its algebraic invariants, maps them to topological holes, and categorifies the obstruction.

## Steering Direction 1: Quantum Tensor Network Scaling
*   **Concept Card / Implementation Hypothesis:** `tensor_network_contraction` - Map the K5 constraint to a set of rank-4 tensors on an N x N lattice. Use approximate tensor contraction algorithms (like DMRG or TRG) to estimate the norm of the network. A sharp drop to zero indicates the bound.
*   **Relevant Bridge Chain:** Quantum-Tensor-Statistical Chain
*   **Rubric Items Informed:** item_006, item_007, item_011, item_013, item_016

## Steering Direction 2: Thermodynamic Flow Rate Analysis (GFlowNet)
*   **Concept Card / Implementation Hypothesis:** `gflownet_entropy_collapse` - Implement an edge-by-edge graph building GFlowNet. Train it on N=40..44. Measure the converged Z(N) estimate. Use the derivative dlog Z(N) / dN to detect the phase boundary.
*   **Relevant Bridge Chain:** Thermodynamic-ML-Information Chain
*   **Rubric Items Informed:** item_011, item_013, item_014, item_016, item_017, item_019

## Steering Direction 3: Semantic Rate-Distortion Limit
*   **Concept Card / Implementation Hypothesis:** `semantic_compression_limit` - Implement the Replica Symmetric (RS) equations for the semantic compression Hamiltonian. Solve the saddle-point equations numerically. Identify the critical system size N where the replica symmetry breaking phase boundary hits D=0.
*   **Relevant Bridge Chain:** Thermodynamic-ML-Information Chain
*   **Rubric Items Informed:** item_007, item_008, item_012, item_017, item_018, item_021
