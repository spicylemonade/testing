# High-Performance DEFLATE Implementation Survey

## 1. zlib (madler/zlib) — The Reference Implementation

**Repository:** https://github.com/madler/zlib
**Authors:** Jean-Loup Gailly, Mark Adler
**Language:** C
**License:** zlib license

### Key Optimization Techniques
- Straightforward table-based Huffman decode (9-bit primary table + secondary overflow)
- Scalar LZ77 copy with byte-by-byte fallback for overlapping copies
- CRC-32 computed via 4KB lookup table
- Adler-32 with delayed modulo (every 5552 bytes)
- Minimal platform-specific optimization; portable C code

### Reported Throughput
- **Decompression:** ~300-500 MB/s on modern x86-64 (Silesia corpus, varies by data)
- **Compression (level 6):** ~35-40 MB/s
- Benchmark source: TurboBench (zlib-ng/zlib-ng#1486), Ryzen 6600HS

### Target Platforms
- Universal: Every platform with a C compiler. Ships in virtually every OS.

### Limitations
- No SIMD utilization for decompression
- Branch-heavy inner loop (literal vs. match dispatch)
- No vectorized CRC-32 or Adler-32
- Single-threaded, strictly sequential

---

## 2. zlib-ng

**Repository:** https://github.com/zlib-ng/zlib-ng
**Authors:** Dead2 (Hans Kristian Rosbach) et al.
**Language:** C
**License:** zlib license

### Key Optimization Techniques
- **SIMD CRC-32:** PCLMULQDQ-based CRC-32 (x86), ARM CRC instructions, Chorba CRC32 for pre-PCLMUL CPUs
- **SIMD Adler-32:** SSE2/SSSE3/AVX2/AVX-512/NEON vectorized accumulation
- **Vectorized slide hash:** AVX2/SSE2/NEON parallel hash table update for compression
- **Optimized longest_match:** SIMD-assisted string comparison
- **Improved inflate:** Some loop restructuring, unrolled copy paths
- **ABI-compatible:** Drop-in replacement for zlib (zlib-compat mode) or native API (zlib-ng mode)
- **Chorba CRC32:** Major improvement for pre-PCLMUL CPUs (added in v2.3.x)

### Reported Throughput
- **Decompression:** ~600-735 MB/s on x86-64 (Silesia, Ryzen 6600HS, TurboBench)
- **Compression (level 6):** ~90-120 MB/s (1.5-2x over zlib)
- zlib-rs (Rust port) aims for performance parity with zlib-ng
- Source: https://github.com/zlib-ng/zlib-ng/issues/1486, https://tweedegolf.nl/en/blog/134/current-zlib-rs-performance

### Target Platforms
- x86/x86-64 (SSE2/SSSE3/SSE4.2/AVX2/AVX-512), ARM (NEON, CRC), s390x, POWER, RISC-V

---

## 3. libdeflate

**Repository:** https://github.com/ebiggers/libdeflate
**Authors:** Eric Biggers
**Language:** C
**License:** MIT

### Key Optimization Techniques
- **Optimized Huffman decode:** Larger decode tables (up to 11-bit), single-level lookup for most codes, reducing branches
- **Branchless literal/match dispatch:** Reduces branch misprediction in hot decode loop
- **Vectorized LZ77 copy:** Uses wide loads/stores for non-overlapping copies
- **Whole-buffer API:** Operates on complete buffers (not streaming), enabling better optimization
- **SIMD CRC-32:** PCLMULQDQ (x86), ARM CRC, folding optimization
- **SIMD Adler-32:** Vectorized accumulation
- **Optimized table construction:** Fast Huffman table builder
- **Platform-specific codepaths:** Separate optimized paths for x86-64, ARM64, generic

### Reported Throughput
- **Decompression:** ~1000-1133 MB/s on x86-64 (Silesia, Ryzen 6600HS, libdeflate 12 setting)
- **Compression:** 7.5-185 MB/s depending on level (level 3: 185 MB/s, level 12: 7.5 MB/s)
- Per aras-p benchmark (OpenEXR): "reaches 2GB/s speed" for EXR decompression
- Source: https://github.com/zlib-ng/zlib-ng/issues/1486, https://aras-p.info/blog/2021/08/09/EXR-libdeflate-is-great/

### Target Platforms
- x86/x86-64, ARM/ARM64, generic (portable C fallback)

### Limitations
- Non-streaming API only (whole buffer required)
- No parallel decompression
- Not a drop-in zlib replacement (different API)

---

## 4. Intel ISA-L (igzip)

**Repository:** https://github.com/intel/isa-l
**Authors:** Intel
**Language:** C + x86 Assembly (NASM)
**License:** BSD-3-Clause

### Key Optimization Techniques
- **Hand-written x86 assembly** for critical decompression paths
- **AVX2/AVX-512 string matching** for compression
- **Optimized Huffman decode:** Assembly-level tuned table lookup with prefetching
- **Vectorized CRC-32:** Multiple folding techniques with PCLMULQDQ
- **Multi-buffer API:** Process multiple streams concurrently for compression
- **Optimized for Intel architectures** but works on AMD x86 and has ARM assembly

### Reported Throughput
- **Decompression:** ~1000-2200+ MB/s on x86-64 (benchmark-dependent)
- Per mxmlnkn (HN): "ISA-L/igzip is more than twice(!) as fast as libdeflate" for decompression of some workloads
- Per ebiggers: "latest version of libdeflate is slightly faster than ISA-L" (as of Aug 2023)
- Results vary significantly by workload and measurement method
- Source: https://news.ycombinator.com/item?id=37270722, Intel tuning guide (686422)

### Target Platforms
- x86-64 (SSE/AVX2/AVX-512), ARM64 (partial assembly support)

### Limitations
- Heavy x86 assembly makes porting difficult
- Primarily optimized for Intel microarchitectures (may be suboptimal on AMD Zen)
- No parallel decompression of single streams

---

## 5. Chromium zlib (zlib-chromium)

**Repository:** https://chromium.googlesource.com/chromium/src/+/refs/heads/main/third_party/zlib/
**Authors:** Google Chromium team, Adenilson Cavalcanti (ARM)
**Language:** C

### Key Optimization Techniques
- **ARM NEON inflate optimizations:** Chunk SIMD for LZ77 copy, 64-bit reads
- **SIMD CRC-32 and Adler-32:** Platform-specific vectorization
- **Optimized for both x86 and ARM:** Dual-platform focus (desktop + mobile)
- **PNG-specific optimizations:** Integrated with Chromium's PNG decoder
- Incorporates patches from multiple contributors (Intel, ARM, Cloudflare)

### Reported Throughput
- **Decompression (ARM):** 1.7-2.0x faster than stock zlib on ARM NEON
- **Decompression (x86):** Comparable to zlib-ng for most workloads
- Per dougallj (2022): using zlib-cloudflare as base, achieved 1.51x speedup over cloudflare on M1, 2.1x over Apple system zlib (282-380 MB/s compressed throughput on M1)
- Source: https://www.phoronix.com/news/Faster-Zlib-ARM-NEON, https://dougallj.wordpress.com/2022/08/20/faster-zlib-deflate-decompression-on-the-apple-m1-and-x86/

### Target Platforms
- x86-64, ARM/ARM64 (NEON), ChromeOS, Android

---

## 6. Cloudflare zlib

**Repository:** https://github.com/cloudflare/zlib
**Authors:** Cloudflare (Vlad Krasnov et al.)
**Language:** C
**License:** zlib license (fork of madler/zlib)

### Key Optimization Techniques
- **64-bit read for bit buffer:** Eliminates multiple byte reads in inflate hot loop
- **SIMD chunk copy:** Vectorized LZ77 copies using SSE2/NEON
- **ARM NEON port** of inflate improvements
- **Optimized longest_match** using SIMD string comparison
- **Drop-in zlib replacement** (ABI-compatible fork)
- Focused on server workloads (HTTP content-encoding)

### Reported Throughput
- **Decompression:** ~1.3-1.6x faster than stock zlib
- Per AWS benchmark (2021): decompression improved by 30-60% over stock zlib across Silesia corpus
- Per dougallj: 186-276 MB/s compressed throughput on M1 (Silesia), used as base for further optimization
- Source: https://aws.amazon.com/blogs/opensource/improving-zlib-cloudflare-and-comparing-performance-with-other-zlib-forks/

### Target Platforms
- x86-64, ARM64 (Linux server focus)

### Limitations
- Not as aggressively optimized as libdeflate or ISA-L
- Fork maintenance can lag behind upstream zlib

---

## 7. pugz and rapidgzip (Parallel DEFLATE)

**pugz Repository:** https://github.com/Piezoid/pugz
**rapidgzip Repository:** https://github.com/mxmlnkn/rapidgzip
**Authors:** Nayuki (pugz), Maximilian Knespel (rapidgzip)
**Language:** C++ (pugz), C++/Python (rapidgzip)
**License:** MIT (pugz), Apache-2.0/MIT (rapidgzip)

### Key Optimization Techniques

#### pugz
- **Parallel DEFLATE decompression** by discovering block boundaries speculatively
- **Probabilistic sync-point detection:** Scans compressed bitstream for valid Huffman table headers
- **Speculative decode + validation:** Each thread starts decoding from a candidate boundary, validates by checking consistency
- **Restriction:** Original pugz requires decompressed data to contain only byte values 9-126 (ASCII text)
- Paper: "pugz: Parallel decompression of gzipped text files" (PPoPP 2019)

#### rapidgzip
- **Generalized parallel gzip decompression** — removes pugz's ASCII-only restriction
- **Cache-based architecture:** Handles incorrect speculative decode results safely
- **Parallelized prefetcher:** Speculatively decodes blocks ahead
- **Random access:** Builds an index for seeking within gzip files
- **ISA-L integration:** Uses ISA-L for per-block decompression, boosting per-thread throughput
- Paper: "Rapidgzip: Parallel Decompression and Seeking in Gzip Files Using Cache Prefetching" (SC 2023)

### Reported Throughput
- **pugz:** ~1.5-2 GB/s on 8 threads for ASCII text
- **rapidgzip:** Up to 10 GB/s with many threads (>20 GB/s if index pre-built)
- Per mxmlnkn: "55x over gzip with 128 cores, 5.6 GB/s on Silesia"
- Single-thread throughput is ~equal to underlying inflate implementation used
- Source: https://github.com/mxmlnkn/rapidgzip, SC 2023 paper, HN discussion

### Target Platforms
- x86-64, multi-core systems (Linux focus)

### Limitations
- pugz: ASCII text only
- rapidgzip: Overhead for small files; best for large (>100MB) gzip files
- Cannot parallelize a single DEFLATE block; only inter-block parallelism

---

## 8. Additional Notable Implementations

### dougallj's zlib optimizations (2022)
- Focused on Apple M1 / ARM optimization
- Achieved 1.51x over zlib-cloudflare on M1 for decompression
- Demonstrated 2.1x over Apple's system zlib
- URL: https://dougallj.wordpress.com/2022/08/20/faster-zlib-deflate-decompression-on-the-apple-m1-and-x86/

### Blend2D High-Performance PNG Codec (2025)
- Claims fastest PNG decode of any C/C++ library
- Custom DEFLATE decompression optimized for PNG's specific patterns
- URL: https://blend2d.com/blog/png-image-codec.html

### zlib-rs (Tweede Golf, 2024)
- Rust reimplementation targeting zlib-ng performance parity
- Memory-safe drop-in replacement for libz.so
- URL: https://tweedegolf.nl/en/blog/134/current-zlib-rs-performance

---

## Summary Comparison Table

| Implementation | Decompress (MB/s) | vs. zlib | Key Advantage | API | Parallel |
|---|---|---|---|---|---|
| zlib (reference) | 300-500 | 1.0x | Universal compatibility | Streaming | No |
| zlib-ng | 600-735 | 1.5-2.0x | Drop-in replacement, SIMD checksums | zlib-compat | No |
| Cloudflare zlib | 400-650 | 1.3-1.6x | Drop-in, server-optimized | zlib-compat | No |
| Chromium zlib | 500-700 | 1.4-1.8x | ARM NEON optimized | zlib-compat | No |
| libdeflate | 1000-1133 | 2.0-3.0x | Best single-thread, branchless | Whole-buffer | No |
| Intel ISA-L | 1000-2200 | 2.5-4.0x | Hand-tuned x86 assembly | Custom | No |
| pugz | 1500-2000 | 4-5x | Parallel, speculative | Custom | Yes (text) |
| rapidgzip | up to 10000+ | 20-55x | Parallel, general, indexed | Custom | Yes |

*Note: Throughput numbers are approximate and depend on data, CPU, compiler, and measurement methodology. Silesia corpus on modern x86-64 (Zen3/4 or Skylake-class) unless otherwise noted.*

---

## Key Observations

1. **Single-thread ceiling:** libdeflate and ISA-L represent the practical single-thread ceiling at ~1-2 GB/s. Further gains require parallelism or fundamentally different approaches.

2. **The 2-5x target over zlib:** Already achieved by libdeflate (~2-3x) and ISA-L (~2.5-4x) on a single thread. To exceed these, either multi-threading or novel algorithmic techniques are needed.

3. **Parallelism is the multiplier:** rapidgzip demonstrates that parallel decompression can achieve 10-55x over single-threaded zlib, but requires multi-core and works best on large files.

4. **Branch elimination is the key single-thread technique:** libdeflate's main advantage over zlib-ng and zlib-cloudflare comes from branchless literal/match dispatch and optimized table lookup.

5. **Multi-stream Huffman (Oodle approach):** Not used by any open DEFLATE implementation, but achieves ~1.83 cycles/symbol (3+ GB/s single-thread) for Huffman-only decode. Could be adapted with format-aware batching.

6. **ARM is underserved:** Most aggressive optimizations target x86-64. ARM NEON optimizations exist (Chromium, Cloudflare) but lag behind x86 performance.
