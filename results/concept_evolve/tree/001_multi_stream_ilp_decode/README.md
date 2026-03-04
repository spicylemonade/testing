# Multi-Stream ILP Decode

## Context

DEFLATE decompression's core bottleneck is the serial Huffman table lookup chain. Each symbol decode requires: peek at bits -> table load (5 cycles on Skylake) -> shift bit buffer (1 cycle) -> update bit count (1 cycle). This ~7-cycle chain means a single-stream decoder is severely underutilizing modern superscalar CPUs that can issue 4+ instructions per cycle.

The key insight from Fabian Giesen (RAD/Oodle) and others is that by maintaining multiple independent bit-buffer states and round-robin decoding from each, we fill the otherwise-idle execution slots with useful work from other streams.

## Key References

- Fabian Giesen, "Entropy decoding in Oodle Data: x86-64 3-stream Huffman decoders" (2022)
- Fabian Giesen, "Interleaved entropy coders" (arXiv:1402.3392, 2014)
- dougallj, "Faster zlib/DEFLATE decompression on the Apple M1 and x86" (2022)

## Critical Insight for DEFLATE

Unlike Oodle (which designs its format for multi-stream), DEFLATE has a single bitstream. The bridge to multi-stream ILP requires either:
1. Sync-point discovery (concept 002) to find valid decode positions within the stream
2. A two-pass architecture where the first pass identifies decode positions

## Implementation Backlog

- [ ] Implement 3-stream Huffman decode loop with hand-tuned x86-64 assembly
- [ ] Implement sync-point finding for stream splitting
- [ ] Benchmark stream count (2, 3, 4, 6) vs throughput on Skylake and Zen3
- [ ] Profile register pressure: 3 registers per stream * 6 streams = 18, exceeds 16 GPRs
- [ ] Investigate using XMM registers for additional bit-buffer state storage
- [ ] Measure impact of L1 cache pressure from multiple simultaneous table lookups
- [ ] Compare against libdeflate and ISA-L baseline numbers
- [ ] Test on ARM64 (Apple M1) with NEON-based implementation
