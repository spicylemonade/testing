# Interleaved Entropy Streams for DEFLATE

## Context

Fabian Giesen's "Interleaved entropy coders" (2014) describes a general technique for interleaving multiple entropy coder instances to achieve ILP. Oodle's format is designed from the ground up with multiple streams. The challenge for DEFLATE is that the format has only a single stream.

## The Virtual Interleaving Insight

By combining sync-point discovery (concept 002) with multi-stream ILP (concept 001), we can create "virtual" interleaved streams from a standard DEFLATE bitstream:

1. Find the compressed block's total bit length (or estimate it)
2. Divide into N segments of roughly equal bit length
3. Find sync points at each segment boundary
4. Initialize N independent bit-buffer states at these sync points
5. Decode round-robin from all N streams

The output comes in N separate buffers, ordered correctly because we decode segment 0 first in round-robin, then segment 1, etc.

## Key Difference from Real Multi-Stream

Real multi-stream formats (Oodle, Zstandard) encode streams independently with known boundaries. Virtual interleaving:
- Has sync-finding overhead (~30-60 bits per sync point)
- May have unequal segment lengths
- Requires knowing or estimating total block size
- Cannot be done until the Huffman table is parsed

## Implementation Backlog

- [ ] Implement N-way virtual stream creation
- [ ] Benchmark 2-way, 3-way, 4-way interleaving on Silesia corpus
- [ ] Measure sync-finding overhead as % of total decode time
- [ ] Determine optimal N for different CPU microarchitectures
- [ ] Handle end-of-block markers within segments
- [ ] Profile register pressure for N streams on x86-64
