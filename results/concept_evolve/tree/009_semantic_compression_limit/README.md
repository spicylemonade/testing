# semantic_compression_limit

## Context
Treats valid R(5,5) graphs as an ensemble of meaning-preserving messages under a distortion metric. We study the phase diagram of this semantic compression space. A first-order phase transition from lossy to lossless compression defines the strict upper bound.

## Domains
Information Theory, Cognitive Neuroscience, Statistical Mechanics

## Math
Rate-distortion R(D) = \min I(X; \hat{X}) subject to E[d(X,\hat{X})] \le D. As N increases, the required rate R(0) exceeds the Shannon capacity of the edge channel.

## Analogies
Like trying to ZIP compress a file of pure noise. A valid Ramsey graph looks like pseudo-random noise, but is actually highly constrained. At R(5,5), the required constraint density exceeds the information capacity.

## Implementation Backlog
- Implement the Replica Symmetric (RS) equations for the semantic compression Hamiltonian. Solve the saddle-point equations numerically. Identify the critical system size N where the replica symmetry breaking phase boundary hits D=0.
- Solve the RS equations for the R(4,4) problem using the framework from Can (2025). The predicted first-order transition line should intersect the D=0 axis exactly at N=18.
