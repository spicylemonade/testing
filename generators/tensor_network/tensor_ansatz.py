import numpy as np
import itertools

class TensorNetworkAnsatz:
    """
    Formulates the exact search for a (5,5)-Ramsey graph as a Tensor Network contraction problem.
    Instead of explicitly building graphs or using continuous relaxations (SDPs), this ansatz
    embeds the discrete boolean constraint exactly into a local tensor structure.
    
    Ansatz:
    1. Every possible edge `e` between N vertices is a physical spin index `s_e` in {-1, 1}.
    2. Every possible K_5 subgraph is a rank-10 constraint tensor `T`.
    3. `T(s_1, ..., s_10) = 0` if all 10 spins are +1 (a red K_5) or all are -1 (a blue K_5).
       Otherwise, `T = 1`.
    
    The contraction of this network over all edges and all K_5 subsets yields the exact partition 
    function Z(N) of valid Ramsey graphs.
    """
    def __init__(self, N: int):
        self.N = N
        self.num_edges = N * (N - 1) // 2

    def build_local_constraint_tensor(self):
        """
        Builds the localized rank-10 tensor ensuring a single K_5 is free of monocromatic cliques.
        Dimension: 2 x 2 x ... x 2 (10 times)
        """
        # A tensor with 10 physical legs, each of dimension 2 (boolean edge state)
        T = np.ones((2,) * 10, dtype=np.float32)
        
        # Red K_5: all 10 edges are 0
        T[tuple([0]*10)] = 0.0
        # Blue K_5: all 10 edges are 1
        T[tuple([1]*10)] = 0.0
        
        return T

    def define_network_topology(self):
        """
        Maps which physical edge indices connect to which constraint tensors.
        Returns a list mapping each K_5 to its 10 edge indices.
        """
        edges = list(itertools.combinations(range(self.N), 2))
        edge_to_idx = {e: i for i, e in enumerate(edges)}
        
        k5_constraints = []
        for subset in itertools.combinations(range(self.N), 5):
            subset_edges = list(itertools.combinations(subset, 2))
            indices = [edge_to_idx[e] for e in subset_edges]
            k5_constraints.append(indices)
            
        return {
            'num_spins': self.num_edges,
            'num_tensors': len(k5_constraints),
            'tensor_connections': k5_constraints
        }

if __name__ == "__main__":
    ansatz = TensorNetworkAnsatz(5)
    T = ansatz.build_local_constraint_tensor()
    topology = ansatz.define_network_topology()
    print(f"For N=5: Network has {topology['num_spins']} spins and {topology['num_tensors']} constraint tensors.")
    print(f"Norm of local constraint tensor: {np.linalg.norm(T)}")
