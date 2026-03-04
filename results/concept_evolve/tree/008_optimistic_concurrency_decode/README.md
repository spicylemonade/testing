# Optimistic Concurrency Decode

## Context

Database systems use optimistic concurrency control (OCC) when conflicts are rare: execute transactions without acquiring locks, then validate at commit time. If validation fails (conflict detected), abort and retry. This is efficient when most transactions don't conflict.

## Application to DEFLATE

The "transaction" is decoding a segment of a DEFLATE block. The "conflict" is starting at an incorrect bit offset. Using sync-point discovery (concept 002), we can dramatically reduce the conflict rate - a successfully found sync point guarantees correct decode from that position onward.

## Architecture

```
Thread 0: decode from block_start to estimated_midpoint
Thread 1: find sync point near estimated_midpoint, decode from sync to estimated_end

Merge phase:
  - Thread 0 produces: decoded symbols [0..N1], final bit offset O1
  - Thread 1 produces: decoded symbols [0..N2], starting bit offset S1
  - Validate: O1 == S1? If yes, concatenate. If no, re-decode segment 1.
```

## Key Challenge: LZ77 Dependencies

Even with parallel Huffman decoding, LZ77 back-references in Thread 1's output may reference data decoded by Thread 0. Solutions:
1. Two-pass: Huffman decode in parallel, LZ77 reconstruction serially
2. Speculative LZ77: Thread 1 maintains its own output buffer, cross-references resolved at merge

## Implementation Backlog

- [ ] Implement 2-thread OCC decoder
- [ ] Measure validation success rate across file types
- [ ] Profile thread synchronization overhead
- [ ] Determine minimum block size for net positive benefit
- [ ] Handle edge cases: end-of-block in first half, stored blocks
- [ ] Extend to 4-thread decode for very large blocks
