# Mod-9 Preimage Residue Filter

## Topic Context

The mod-9 Preimage Sieve is one of the oldest known optimization for Collatz verification. It exploits the preimage structure of the Collatz map: certain residue classes mod 9 are guaranteed to lie on the trajectory of a smaller integer, so they need not be independently verified.

The key challenge is efficient implementation: computing n mod 9 requires integer division, which is expensive on GPUs. Angeltveit's bitvector approach avoids this by precomputing mod-9 membership as a bit array.

## Cross-Domain Bridges

- **Error-correcting codes**: Syndrome-based decoding identifies correctable errors by residue
- **Signal processing**: Polyphase filter banks decompose by residue modulo decimation factor
- **CRT in cryptography**: Combine mod-p residue information for global inference

## Implementation Backlog

- [ ] Implement naive mod-9 filter (integer division per candidate)
- [ ] Implement bitvector mod-9 filter (precomputed bit arrays)
- [ ] Benchmark both on GPU (CUDA) for 10^12 candidates
- [ ] Test mod-27 and mod-81 extensions
- [ ] Quantify diminishing returns of higher mod-3^k sieves
- [ ] Explore CRT-based combination of mod-9 with other prime moduli
