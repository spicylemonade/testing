# Parallel Bit Stream Structural Indexing

## Topic Context

The fundamental bottleneck in CSV parsing is the byte-by-byte scan for structural characters: commas (field delimiters), double-quotes (field quoting), and newlines (row terminators). Traditional parsers use a finite state machine (FSM) that processes one byte per iteration, resulting in throughput limited by branch prediction quality and serial dependency chains.

**Parallel bit stream structural indexing** replaces this with a SIMD-parallel approach: load 32-64 bytes at once into SIMD registers, compare against each structural character simultaneously, and produce bitmasks where each bit indicates the presence of that character at the corresponding input position. This technique was pioneered by Robert Cameron (2008) for XML/UTF-8 processing and brought to mainstream attention by Langdale & Lemire's simdjson (2019).

For CSV, the approach is actually simpler than for JSON because CSV has fewer structural characters (3-4 vs. ~8 for JSON) and a simpler grammar. The key challenge unique to CSV is handling quoted fields with embedded delimiters and newlines, which requires determining "in-string" regions — addressed by the companion CLMUL quote-pairing concept.

## Key Insight

A single SIMD comparison instruction (e.g., `_mm256_cmpeq_epi8`) processes 32 bytes simultaneously, and the result is collapsed into a 32-bit bitmask with `_mm256_movemask_epi8`. This means we identify all comma positions in a 32-byte chunk with 2 instructions (~0.0625 instructions per byte), compared to a scalar approach requiring 1+ instructions per byte.

## Implementation Backlog

- [ ] Implement AVX2 structural classifier (32 bytes/iteration)
- [ ] Implement AVX-512 structural classifier (64 bytes/iteration)
- [ ] Implement ARM NEON structural classifier (16 bytes/iteration)
- [ ] Benchmark raw classification throughput (bytes/sec, instructions/byte)
- [ ] Integrate with CLMUL quote pairing for complete structural index
- [ ] Produce flat offset arrays from bitmasks (using TZCNT + BLSR iteration)
- [ ] Handle tail bytes (< SIMD width) with scalar fallback
- [ ] Test on real-world CSV datasets (NYC Taxi, TPC-H, Kaggle datasets)
- [ ] Compare throughput against scalar FSM parser, Rust csv crate, libcsv
