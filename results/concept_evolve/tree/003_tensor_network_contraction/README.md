# tensor_network_contraction

## Context
Formulates the boolean constraints of a valid R(5,5) coloring as a 2D grid tensor network (like a Projected Entangled Pair State - PEPS). Each tensor represents a localized constraint. The global contraction of this network yields the total number of valid Ramsey graphs. The bound R(5,5) is reached when the exact contraction yields a zero norm state.

## Domains
Quantum Information, Computational Complexity, Graph Theory

## Math
|\Psi\rangle = \sum_{G} \delta_{K_5}(G) |G\rangle. The norm \langle \Psi | \Psi \rangle = \text{tTr}(\prod_{i,j} T^{[i,j]}) exactly counts valid graphs. R(5,5) = \min \{N \mid \langle \Psi_N | \Psi_N \rangle = 0\}.

## Analogies
Like tracking the entanglement entropy in a many-body quantum system, where the ground state abruptly changes its topology. Here, the 'norm' is the volume of valid graphs.

## Implementation Backlog
- Map the K5 constraint to a set of rank-4 tensors on an N x N lattice. Use approximate tensor contraction algorithms (like DMRG or TRG) to estimate the norm of the network. A sharp drop to zero indicates the bound.
- Contract the network for R(3,3)=6 and R(4,4)=18. Analyze the contraction time and entanglement scaling with N. Try to extrapolate to N=43 to 48 using finite-size scaling techniques.
