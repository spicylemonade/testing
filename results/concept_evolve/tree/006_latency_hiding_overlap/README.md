# Latency Hiding Through Decode/Copy Overlap

## Context

In a standard DEFLATE decode loop, the sequence is: decode Huffman symbol -> if match, execute LZ77 copy -> decode next symbol. The LZ77 copy involves memory loads and stores that can have significant latency, especially for cache-missing long-distance references. Meanwhile, the Huffman decode involves table lookups and bit manipulation.

On out-of-order CPUs, if we initiate the next iteration's Huffman table lookup before the current LZ77 copy completes, the CPU can overlap these independent operations. The key insight from dougallj is that the bit-buffer refill and table lookup for the next symbol are independent of the LZ77 copy's memory operations.

## Implementation Strategy

```
loop:
  // Current iteration: we have 'entry' from table lookup
  if (entry is match):
    initiate_lz77_copy(length, distance)  // issues loads/stores
    // IMMEDIATELY begin next iteration's setup:
    refill_bitbuffer()
    next_entry = table[bitbuf & MASK]  // overlaps with copy
  else:
    emit_literal(entry)
    refill_bitbuffer()
    next_entry = table[bitbuf & MASK]
  entry = next_entry
  goto loop
```

## Implementation Backlog

- [ ] Restructure zlib-ng decode loop for overlap
- [ ] Profile with VTune to verify actual overlap on Skylake
- [ ] Measure impact on files with many short matches vs few long matches
- [ ] Quantify branch mispredict overhead from the literal/match check
- [ ] Test interaction with multi-stream ILP approach
