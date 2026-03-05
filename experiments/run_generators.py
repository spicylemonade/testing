import numpy as np
import sys
import os
import json
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generators.twisted_algebraic import TwistedAlgebraicGenerator
from generators.tensor_network.tensor_ansatz import TensorNetworkAnsatz
from metrics.analytic_pruning import SpectralPruner

def execute_generators():
    print("--- Phase 4: Executing Novel Generators on Target Space (N=42..44) ---")
    
    # 1. Algebraic Candidates Generator
    pruner = SpectralPruner(tolerance_threshold=6.6)
    
    results = {}
    
    for N in [42, 43, 44]:
        start_time = time.time()
        print(f"\n[N={N}] Generating Twisted Algebraic Candidates...")
        generator = TwistedAlgebraicGenerator(N=N)
        
        # Generate 100 randomized twisted candidates
        batch = [generator.generate_candidate(num_twists=np.random.randint(5, 25)) for _ in range(100)]
        
        # Prune via spectral invariants
        viable = pruner.evaluate_batch(batch)
        elapsed = time.time() - start_time
        print(f"[N={N}] Kept {len(viable)} / 100 viable candidates (Threshold: {pruner.tolerance_threshold}). Time: {elapsed:.2f}s")
        
        if viable:
            best_candidate = viable[0]
            print(f"[N={N}] Best Spectral Max Bound (theta): {best_candidate['max_bound']:.4f}")
            results[f"algebraic_N{N}"] = {
                "density": float(np.mean(best_candidate['matrix'])),
                "max_spectral_bound": float(best_candidate['max_bound']),
                "viable_count": len(viable)
            }
            
        # 2. Tensor Network Structural Info
        print(f"[N={N}] Building exact Tensor Network constraint space...")
        tn = TensorNetworkAnsatz(N=N)
        topology = tn.define_network_topology()
        print(f"[N={N}] Tensor Network initialized: {topology['num_spins']} edges (physical spins), {topology['num_tensors']} K_5 constraint tensors.")
        
        results[f"tensor_N{N}"] = {
            "num_spins": topology['num_spins'],
            "num_tensors": topology['num_tensors']
        }
        
    with open("experiments/generator_logs.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("\nLogs and structural constraints saved to experiments/generator_logs.json")

if __name__ == "__main__":
    execute_generators()
