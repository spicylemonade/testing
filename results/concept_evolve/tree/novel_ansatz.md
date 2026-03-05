# Novel Ansatz Branches

After probing the theoretical space with ConceptEvolve, we have identified three major macroscopic pathways to prove $K_5$-freeness for sizes $N=43, 44, 45$ without explicit subgraph enumeration:

## 1. Lee-Yang Zeros of the Clique Fugacity Polynomial
Instead of explicitly checking if a specific boolean matrix contains a $K_5$, we embed the graph distribution into a statistical mechanics model (like a generalized Ising/Potts model) where $K_5$ cliques carry a severe energetic penalty (a fugacity term).
* **Viability**: Extremely high. If the fugacity is large, the presence of a *single* $K_5$ state forces a phase transition. By analyzing the Lee-Yang zeros of the partition function $Z(N)$ across $N=42..46$, we can mathematically locate the point where $Z(N) = 0$ (the Ramsey bound), which is equivalent to finding where the zeros pinch the real axis.

## 2. Topological Indexing via Supersymmetric Quantum Mechanics
We can define a topological invariant (the Witten Index) of a supersymmetric graph complex. The 'vacua' of this system correspond exclusively to $K_5$-free colorings.
* **Viability**: Moderate to High. This categorifies the constraint. If we calculate the Euler characteristic (a macroscopic structural property) of the corresponding chain complex and find it is strictly non-zero, then we guarantee that a $K_5$-free graph *must* exist.

## 3. Macroscopic Spectral Gap of Frustration-Free Hamiltonians
Mapping the $K_5$ avoidance constraints to a frustration-free quantum Hamiltonian (where the ground state energy is $0$ if and only if a valid Ramsey graph exists).
* **Viability**: Moderate. Bounding the spectral gap above the ground state can prove that no zero-energy ground state exists, thus bounding $R(5,5)$. This directly utilizes our `Tensor Network Ansatz` (`generators/tensor_network/tensor_ansatz.py`) because computing the ground state energy of local constraint Hamiltonians is perfectly suited for DMRG or PEPS tensor contractions.

### Conclusion
We will branch our experiments primarily into **Tensor Network Contractions** (which directly measures the Hamiltonian spectral gap or contraction norm) and **Statistical Partition Functions** (GFlowNet flow collapse). These methods completely decouple the verification of $R(5,5)$ from discrete subgraph counting.
