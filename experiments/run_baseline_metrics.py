import numpy as np
import json
import os
import sys

# Add root directory to path to import metrics
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from metrics.spectral_bounds import check_k5_freeness_spectral

def build_paley_graph(q):
    """Constructs the adjacency matrix for a Paley graph of order q.
    q must be a prime where q = 1 mod 4.
    """
    if q % 4 != 1:
        raise ValueError("q must be 1 modulo 4")
        
    A = np.zeros((q, q))
    for i in range(q):
        for j in range(q):
            if i != j:
                # Euler's criterion for quadratic residues
                if pow(int((i - j) % q), int((q - 1) // 2), int(q)) == 1:
                    A[i, j] = 1
    return A

def convert(v):
    if hasattr(v, 'item'):
        return v.item()
    return v

def main():
    results = {}
    
    # 1. Paley 17 - The unique R(4,4) critical graph (K_4-free)
    print("Building Paley(17)...")
    A_17 = build_paley_graph(17)
    res_17 = check_k5_freeness_spectral(A_17)
    
    # Check actual graph properties directly (optional, for validation)
    N_17 = A_17.shape[0]
    
    results['Paley_17'] = {
        'N': N_17,
        'spectral_metrics': {k: convert(v) for k, v in res_17.items()}
    }
    print("Paley(17) results:", res_17)
    
    # 2. Paley 37 - Optional baseline
    print("\nBuilding Paley(37)...")
    A_37 = build_paley_graph(37)
    res_37 = check_k5_freeness_spectral(A_37)
    
    results['Paley_37'] = {
        'N': A_37.shape[0],
        'spectral_metrics': {k: convert(v) for k, v in res_37.items()}
    }
    print("Paley(37) results:", res_37)
    
    # 3. Paley 41 - Known to contain K_5, provides baseline
    print("\nBuilding Paley(41)...")
    A_41 = build_paley_graph(41)
    res_41 = check_k5_freeness_spectral(A_41)
    
    results['Paley_41'] = {
        'N': A_41.shape[0],
        'spectral_metrics': {k: convert(v) for k, v in res_41.items()}
    }
    print("Paley(41) results:", res_41)

    with open("experiments/baseline_results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("\nResults saved to experiments/baseline_results.json")

if __name__ == "__main__":
    main()
