# Baseline Profiling Report

## Methodology

Since `perf` is not available on this machine, profiling was conducted via two methods:

1. **gprof**: GCC's built-in sampling profiler (`-pg` flag, compiled at `-O2`).
   Provides function-level time attribution via statistical sampling.

2. **Instrumented profiler** (`bench/profile.c`): Manual `clock_gettime` instrumentation
   inserted at phase boundaries in a copy of the naive decoder. Note: timing overhead
   from frequent `clock_gettime` calls inflates total time by ~2x, but relative ratios
   between phases are informative.

All measurements on: x86-64, GCC 12.2, Debian 12.

## Hardware

```
CPU: See /proc/cpuinfo (containerized environment)
Memory: Sufficient for all working sets
No CPU frequency pinning available (containerized)
```

## gprof Results (naive decoder, english_prose.txt L6, 1000 iterations)

| Function         | % Time | Self (s) | Calls/iter | Description |
|-----------------|--------|----------|------------|-------------|
| huff_decode     | 37.5%  | 0.26     | 45,311     | Huffman symbol decode (table lookup + bit consume) |
| build_huff_table| 31.7%  | 0.22     | 34,513     | Build Huffman lookup table (15-bit flat array) |
| fd_inflate      | 28.0%  | 0.19     | 1          | Main decode loop (LZ77 copy, bit reading, control) |

**Key insight**: Table building at 31.7% is disproportionately expensive because:
- We use 15-bit tables (32,768 entries each) for both litlen and distance
- Each block requires clearing + filling two 32K-entry tables
- build_huff_table iterates over the full table size for clearing

## Instrumented Profiler Results

### english_prose.txt (L6, 262KB → 50KB, ratio 19.7%)
```
Throughput:      40.2 MB/s (naive), vs 1483 MB/s (zlib-ng) → 37x gap
Symbols/iter:    23,465
Literals:        7.5% of symbols
Back-references: 92.5% (avg length 12.0)
Bit refills:     3.4 per symbol

Phase breakdown (excluding timing overhead):
  Huffman decode:  38%
  Extra bit reads: 33%
  LZ77 copy:       20%
  Table build:      5%  (low because only 2 blocks)
  Other:            4%
```

### source_code.c (L6, 262KB → 23KB, ratio 9.1%)
```
Throughput:      80.2 MB/s (naive), vs 2650 MB/s (zlib-ng) → 33x gap
Symbols/iter:    17,812
Literals:        46.7% of symbols
Back-references: 53.2% (avg length 26.8)
Bit refills:     2.6 per symbol

Phase breakdown:
  Huffman decode:  39%
  Extra bit reads: 30%
  LZ77 copy:       16%
  Table build:      6%
  Other:            9%
```

### text_1024k.txt (L6, 1024KB → 173KB, ratio 16.9%)
```
Throughput:      47.1 MB/s (naive), vs 1744 MB/s (zlib-ng) → 37x gap
Symbols/iter:    77,811
Literals:        3.8% of symbols (mostly back-references)
Back-references: 96.2% (avg length 14.0)
Bit refills:     3.7 per symbol

Phase breakdown:
  Huffman decode:  38%
  Extra bit reads: 33%
  LZ77 copy:       22%
  Table build:      3%
  Other:            4%
```

## Optimization Target Analysis

### Where time is spent (naive decoder)

| Phase | % of Hot Path | Optimization Opportunity |
|-------|---------------|--------------------------|
| Huffman decode (table lookup + branch) | 38% | Multi-symbol decode (2-3 symbols per lookup), smaller table → better cache |
| Bit reader (refill + extract) | 33% | Branchless 64-bit refill, overlap refill with lookup (dougallj technique) |
| LZ77 copy | 20% | SIMD word-at-a-time copy (SSE2/AVX2), unrolled for common lengths |
| Table build | 5-32% | Smaller tables (11-bit primary), fast clearing, table caching |
| Control/branch | 4% | Branchless literal/length dispatch |

### Why the naive decoder is 37x slower than zlib-ng

1. **15-bit flat tables** — 32K entries × 4 bytes = 128KB per table, blows L1 cache (32KB).
   zlib-ng uses 9-bit (512 entries), libdeflate uses 11-bit (2048 entries).

2. **Byte-at-a-time bit refill** — refills one byte at a time when needed.
   Best implementations use 64-bit word reads, branchless.

3. **Single-symbol decode** — one symbol per table lookup.
   libdeflate decodes up to 3 symbols per primary table access.

4. **Byte-by-byte LZ77 copy** — `for (i=0; i<len; i++) dst[out_pos++] = dst[src_pos++]`.
   Should use `memcpy` / SIMD for non-overlapping copies (distance >= length).

5. **No inlining** — all functions are separate, preventing compiler optimization.

6. **Redundant refills** — 3.4 refills per symbol vs. theoretical minimum of ~1.

### Estimated impact of each optimization

| Optimization | Expected Speedup | Priority |
|-------------|-------------------|----------|
| 11-bit primary table (smaller, cacheable) | 3-5x | P0 (critical) |
| 64-bit branchless bit reader | 2-3x | P0 |
| Multi-symbol decode | 1.3-2x | P1 |
| SIMD LZ77 copy | 1.2-1.5x | P1 |
| Table build caching | 1.1-1.3x (small blocks) | P2 |
| Branchless dispatch | 1.05-1.1x | P2 |

### Comparison: naive vs. zlib-ng vs. libdeflate (100-iteration median, MB/s)

| File | Naive | zlib | zlib-ng | libdeflate | zlib-ng/naive |
|------|-------|------|---------|------------|---------------|
| english_prose L6 | 269 | 469 | 1,483 | 1,825 | 5.5x |
| source_code L6 | 974 | 1,416 | 2,650 | 3,433 | 2.7x |
| text_1024k L6 | 338 | 555 | 1,744 | 2,150 | 5.2x |
| structured.json L6 | 390 | 690 | 1,888 | 2,207 | 4.8x |
| webpage.html L6 | 1,216 | 2,377 | 3,851 | 4,874 | 3.2x |
| mixed_entropy L6 | 320 | 817 | 2,433 | 3,020 | 7.6x |
| tabular.csv L6 | 179 | 349 | 569 | 689 | 3.2x |

### Geometric mean throughput (all 60 files, 100 iterations)

| Decoder | Geomean MB/s | vs. zlib |
|---------|-------------|----------|
| naive | 353 | 0.25x |
| zlib (system) | 1,415 | 1.00x |
| zlib-ng | 2,862 | 2.02x |
| libdeflate | 2,987 | 2.11x |

### Path to 2x over zlib-ng (target: ~5,724 MB/s)

This is very aggressive — 92% faster than the current best (libdeflate at 2,987 MB/s).
More realistically, we should aim to match or exceed libdeflate first, then pursue
novel techniques for additional gains:

1. **Phase 1** (match libdeflate, ~3000 MB/s): 11-bit table, branchless bit reader,
   word-at-a-time copy, multi-symbol decode
2. **Phase 2** (exceed libdeflate, ~3500-4000 MB/s): dougallj zero-refill-latency,
   AVX2 copy, optimized table build
3. **Phase 3** (approach 2x target): Speculative multi-symbol decode,
   parallel block detection, ILP exploitation

## Conclusion

The naive decoder's primary bottleneck is the Huffman decode loop (38% of hot path),
amplified by cache-busting 15-bit tables (128KB each) and byte-at-a-time bit reading.
Reducing table size from 15→11 bits alone should give ~3-5x speedup by fitting tables
in L1 cache. Combined with branchless bit reading and multi-symbol decode, matching
libdeflate's ~3000 MB/s is achievable. Exceeding it requires novel techniques from
the concept tree (dougallj bit reader, speculative decode, ILP exploitation).
