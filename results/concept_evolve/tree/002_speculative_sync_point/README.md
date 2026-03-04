# Speculative Sync Point Discovery

## Context

The fundamental challenge in parallelizing Huffman decoding is that each symbol's position depends on the length of all preceding symbols. You cannot decode symbol N without first decoding symbols 1..N-1. This is the "embarrassingly sequential" nature of variable-length prefix codes.

dougallj discovered a practical method: start decoding from max_code_length (15 for DEFLATE) consecutive bit offsets simultaneously. One of these must be a valid symbol boundary. As the probes advance through the bitstream, they converge to the same positions (like rivers joining). The first position where only one probe remains is a guaranteed synchronization point.

## Algorithm

```
find_sync_after(data, offset):
  probes = (1 << MAX_CODE_LENGTH) - 1  // 15 active probes
  while probes != 1:
    size = decode_length(data, offset)
    offset += 1
    probes >>= 1
    probes |= 1 << (size - 1)
    offset += ctz(probes)
    probes >>= ctz(probes)
  return offset
```

## Key Properties

- Guaranteed to find a sync point (provable from prefix code properties)
- Expected convergence within ~50 bits for typical DEFLATE data
- Cost: decode ~15-30 symbols at the sync-finding position
- Independent of block size - works for any position within a block

## Implementation Backlog

- [ ] Implement sync-point finder for DEFLATE Huffman tables
- [ ] Measure convergence distance distribution across diverse file types
- [ ] Profile the overhead: sync-finding time vs parallel decode benefit
- [ ] Determine minimum block size where sync-finding is amortized
- [ ] Handle edge cases: end-of-block markers, stored blocks, fixed Huffman blocks
- [ ] Implement the backwards variant for finding the first sync point at/after a given position
- [ ] Verify correctness exhaustively on adversarial inputs
