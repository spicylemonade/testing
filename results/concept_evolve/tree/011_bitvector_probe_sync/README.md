# Bitvector Probe Synchronization

## Context

The sync-point discovery algorithm (concept 002) processes probes sequentially, advancing one at a time. This is efficient in terms of total work but has a serial dependency chain. By representing the set of reachable bit positions as a bitvector, we can use hardware-accelerated bit manipulation (POPCNT, CTZ, LZCNT) to process many positions simultaneously.

## Algorithm

```
bitvector_sync(data, start, huffman_table):
  V = bitvector of size max_scan_length, all zeros
  // Initialize: mark first 15 positions as potential starts
  V[0..14] = all 1s
  
  for i = 0 to max_scan_length:
    if V[i] == 1:
      len = huffman_decode_length(data, start + i, huffman_table)
      V[i + len] = 1
    
    // Check convergence in trailing 15-bit window
    window = V[(i-14)..(i+1)]
    if popcount(window) == 1:
      return start + i  // sync point found
  
  return SYNC_NOT_FOUND
```

## Advantages Over Iterative Approach

1. Can be vectorized: process 64 bit positions per word
2. Natural representation for parallel probe tracking
3. POPCNT hardware instruction makes convergence check O(1)
4. Memory access pattern is sequential (cache-friendly)

## Caveats

- Requires more memory than the iterative approach (bitvector vs 15-bit bitmask)
- For typical convergence distances (~50 bits), the iterative approach may be simpler
- Main benefit is for massively parallel sync finding (multiple sync points simultaneously)

## Implementation Backlog

- [ ] Implement bitvector sync finder
- [ ] Benchmark vs iterative sync finder (dougallj's method)
- [ ] Test with SIMD-widened bitvector operations (process 256 bits with AVX2)
- [ ] Measure L1 cache impact of bitvector allocation
- [ ] Handle multiple simultaneous sync-point searches
