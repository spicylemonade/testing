# quaternionic_shadow_decoder

Domains: sequence design, quaternionic algebra, cellular automata

## Topic Context
Search in a richer quaternionic perfect-sequence space and only later project to real binary shadows. If quaternionic phases cluster around low-defect real shadows more often than random binary starts do, they become a practical latent space for 668 search.

Mathematical focus:
Sample q in {+1,-1,+i,-i,+j,-j,+k,-k}^{167}. Define shadow maps Pi_alpha(q) in {+1,-1}^{4 x 167} by phase partitioning, score J(Pi_alpha(q)) by autocorrelation or modular defect, and run CA repair R_f on the best shadows.

Implementation hypothesis:
Enumerate or sample small quaternionic perfect sequences, evaluate several shadow maps, keep the maps with the best enrichment, and then push their real shadows through a CA repair loop.

## Closest Prior Art
- Quaternionic Perfect Sequences and Hadamard Matrices (3a6ce978f1717d149e7e4d6d8fe0e6ff857d93b8)
- Perfect Sequences and Arrays over the Unit Quaternions (278d6d8081ada7cb58b965accd65196059cc2ecd)
- A 64-modular Hadamard matrix of order 668 (ajc_v93_p422)

## Implementation Backlog
- Build the prototype scaffold under `experiments/quaternionic_shadow_decoder`.
- Implement the state representation implied by: Sample q in {+1,-1,+i,-i,+j,-j,+k,-k}^{167}. Define shadow maps Pi_alpha(q) in {+1,-1}^{4 x 167} by phase partitioning, score J(Pi_alpha(q)) by autocorrelation or modular defect, and run CA repair R_f on the best shadows.
- Test the core loop from the experiment seed: Compare quality distributions of projected quaternionic shadows and random real seeds on small exact targets and on 32- or 64-modular filters before scaling to length 167.
- Keep the novelty guardrail explicit: Prior quaternionic work stays inside quaternionic sequence families. Here those families only serve as proposal generators for a real-domain search with explicit downstream repair and filtering.
