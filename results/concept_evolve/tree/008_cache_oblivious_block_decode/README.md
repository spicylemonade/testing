# Cache-Oblivious Block Decode

## Context

For large inputs (>64KB), the Base64 decoder's performance becomes memory-bound rather than compute-bound. The input is read sequentially and the output is written sequentially, but the 4:3 size ratio means the input and output pointers advance at different rates, potentially causing cache conflicts.

Cache-oblivious algorithms avoid tuning block sizes to specific cache sizes by using recursive or self-similar access patterns that are optimal for any cache configuration. For streaming transforms like Base64 decode, the key insight is to process blocks small enough that both input and output fit in the lowest cache level.

## Key Insight

A 3072-byte input block decodes to 2304 output bytes. Together (5376 bytes) they fit comfortably in a 32KB L1d cache. By processing in these blocks and prefetching the next block, we ensure nearly all loads and stores hit L1, even when the total input is much larger than any cache level.

## Implementation Backlog

- [ ] Implement blocked decode with 3072-byte chunks
- [ ] Add software prefetch (_mm_prefetch) for next input block during current block processing
- [ ] Measure L1/L2/L3 miss rates at various input sizes using perf
- [ ] Compare against simple linear streaming decode
- [ ] Test interaction with downstream consumer (e.g., simulated JSON parser reading output)
- [ ] Explore adaptive block sizing based on runtime cache detection (optional, defeats cache-oblivious philosophy)
