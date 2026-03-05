import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from metrics.spectral_bounds import check_k5_freeness_spectral

class SpectralPruner:
    """
    Acts as an analytic filter, rejecting parameterized graph constructions 
    (from algebraic geometries or tensor models) by efficiently bounding 
    their independence number via Lovasz Theta / Hoffman without doing 
    brute-force subgraph enumeration.
    """
    def __init__(self, tolerance_threshold: float = 6.0):
        # Even if a graph is K_5 free, its spectral relaxation might be larger than 5.
        # We set a threshold (e.g. 6.0) above which we immediately prune the candidate
        # as having too 'weak' of an algebraic structure to be a viable R(5,5) candidate.
        self.tolerance_threshold = tolerance_threshold

    def evaluate_batch(self, candidates: list[np.ndarray]):
        """
        Takes a list of candidate adjacency matrices.
        Returns the ones that pass the pruning phase (Lovász / Hoffman < threshold).
        """
        viable_candidates = []
        for i, A in enumerate(candidates):
            metrics = check_k5_freeness_spectral(A)
            
            # We want both G and complement(G) to avoid large cliques
            max_bound = max(metrics['theta_G_bound'], metrics['theta_G_bar_bound'])
            
            if max_bound < self.tolerance_threshold:
                viable_candidates.append({
                    'index': i,
                    'matrix': A,
                    'max_bound': max_bound,
                    'metrics': metrics
                })
                
        # Sort viable candidates by the tightest (lowest) spectral bound
        viable_candidates.sort(key=lambda x: x['max_bound'])
        return viable_candidates

if __name__ == "__main__":
    from generators.twisted_algebraic import TwistedAlgebraicGenerator
    
    # Generate a small batch of twisted candidates for N=43
    pruner = SpectralPruner(tolerance_threshold=6.5) # Looser for N=43
    generator = TwistedAlgebraicGenerator(N=43)
    
    batch = [generator.generate_candidate(num_twists=i*2) for i in range(10)]
    results = pruner.evaluate_batch(batch)
    
    print(f"Out of 10 candidates, {len(results)} passed the spectral pruning threshold of {pruner.tolerance_threshold}.")
    if results:
        print(f"Best candidate had spectral max_bound: {results[0]['max_bound']:.3f}")
