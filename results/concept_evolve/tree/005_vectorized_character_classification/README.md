# Vectorized Character Classification

## Topic Context

CSV parsing requires classifying every input byte into one of a small number of categories: comma, quote, newline, carriage return, or other. Traditional parsers use switch/if-else chains, which generate branch instructions that the CPU's branch predictor must handle. On mixed-content CSV data, these branches mispredirect frequently.

The PSHUFB (packed shuffle bytes) instruction provides a 16-entry lookup table in a single SIMD register. By splitting each byte into high and low nibbles and performing two lookups, we can classify all bytes in a 16-byte chunk with 3 instructions: 2 shuffles + 1 AND. This is ~0.19 instructions per byte vs. ~1-3 for scalar.

## Key Insight

The CSV structural alphabet is tiny (4 characters). A perfect hash function implemented via nibble-split PSHUFB lookup can classify the entire 256-byte input space with zero collisions in just 3 SIMD instructions per 16 bytes.

## Implementation Backlog

- [ ] Design LUT entries for CSV structural characters (0x2C, 0x22, 0x0A, 0x0D)
- [ ] Implement PSHUFB classification for SSE4.2
- [ ] Implement VPSHUFB classification for AVX2
- [ ] Implement TBL/TBX classification for ARM NEON
- [ ] Handle configurable delimiters (tab, semicolon, pipe)
- [ ] Extract per-class bitmasks from classification results
- [ ] Benchmark against scalar classification loop
- [ ] Measure branch misprediction elimination via perf counters
