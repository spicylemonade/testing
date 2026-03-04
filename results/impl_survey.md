# Survey of High-Performance DEFLATE Decompression Implementations

## Overview

This document surveys the leading high-performance DEFLATE decompression implementations,
analyzing their optimization techniques, SIMD usage, table designs, and measured throughput.
The goal is to identify the state of the art and the key techniques responsible for
performance gains over the reference zlib implementation.

---

## 1. zlib (reference baseline)

| Property | Details |
|----------|---------|
| **Language** | C |
| **Repository** | https://github.com/madler/zlib |
| **License** | zlib license |
| **Decompression strategy** | Two-level table-based Huffman decode |
| **SIMD usage** | None in original zlib |
| **Table sizes** | 9-bit primary table (512 entries), secondary tables for longer codes |
| **Bit buffer** | Conditional refill, platform-dependent width (32 or 64 bits) |
| **LZ77 copy** | Byte-at-a-time for overlapping, memcpy for non-overlapping |
| **Throughput** | ~250-400 MB/s on modern x86-64 (single core) |

### Key Characteristics
- The reference implementation prioritizes correctness and portability over performance.
- `inflate_fast()` is the inner loop hot path, using a 9-bit primary table.
- Conditional bit-buffer refill (`if (bits < 15) { ... }`) causes branch overhead.
- No SIMD instructions used anywhere in decompression.
- LZ77 copy in `inflate_fast()` uses `do { *out++ = *from++; } while (...)` pattern.

### Performance Limiters
- Branch mispredictions on bit-buffer refill and symbol type dispatch
- No multi-symbol decode capability
- Suboptimal LZ77 copy for large non-overlapping matches
- 32-bit bit buffer on some platforms limits throughput

---

## 2. zlib-ng

| Property | Details |
|----------|---------|
| **Language** | C |
| **Repository** | https://github.com/zlib-ng/zlib-ng |
| **License** | zlib license |
| **Decompression strategy** | Two-level table-based Huffman, optimized inflate_fast |
| **SIMD usage** | SSE2, SSSE3, SSE4.2, AVX2 (CRC32, Adler32, longest match) |
| **Table sizes** | 9-bit primary table with 2-symbol entries in some paths |
| **Bit buffer** | 64-bit bit buffer with semi-branchless refill |
| **LZ77 copy** | chunked_memcpy with SIMD for >=16 byte copies |
| **Throughput** | ~500-800 MB/s on modern x86-64 (single core) |

### Key Optimizations
1. **64-bit bit buffer**: Reduces refill frequency (can hold 57+ valid bits)
2. **Optimized inflate_fast**: Restructured inner loop with fewer branches
3. **SIMD CRC32/Adler32**: Uses PCLMULQDQ for CRC32, SSSE3 for Adler32
4. **chunked_memcpy**: Uses SSE2/AVX2 128/256-bit stores for LZ77 copies
5. **Architecture detection**: Runtime dispatch to best SIMD code path
6. **Improved table build**: Faster Huffman table construction

### Decompression Strategy Detail
- Primary table: 9-bit lookup (512 entries × 32 bits = 2KB)
- Each entry encodes: symbol value (16 bits) + consumed bits (8 bits) + flags (8 bits)
- Secondary tables for codes > 9 bits: variable size, indexed by remaining bits
- For codes ≤ 9 bits: single table lookup per symbol
- For codes > 9 bits: two table lookups per symbol

### Performance Characteristics
- ~1.5-2× faster than original zlib for decompression
- Main bottleneck remains serial Huffman decode in the inner loop
- CRC32 computation offloaded to hardware (CRC32 instruction or PCLMULQDQ)
- SIMD primarily benefits checksum and LZ77 copy, not Huffman decode itself

---

## 3. libdeflate

| Property | Details |
|----------|---------|
| **Language** | C |
| **Repository** | https://github.com/ebiggers/libdeflate |
| **License** | MIT |
| **Decompression strategy** | Multi-symbol decode tables (up to 4 symbols per lookup) |
| **SIMD usage** | SSE2, BMI2 for bit extraction; AVX2 for some paths |
| **Table sizes** | Configurable; primary table up to 11 bits (8KB), decodes 1-4 symbols |
| **Bit buffer** | 64-bit with unconditional refill from unaligned 64-bit loads |
| **LZ77 copy** | Branchless fixed-size copies (always copy 32 bytes, even if shorter) |
| **Throughput** | ~800-1500 MB/s on modern x86-64 (single core) |

### Key Optimizations
1. **Multi-symbol decode tables**: The key innovation. For short codes (≤11 bits),
   precompute tables that decode up to 4 consecutive literal symbols in a single lookup.
   Table entry format: `[sym1|sym2|sym3|sym4|total_bits|num_symbols]`
   
2. **Unconditional bit-buffer refill**: Load 8 bytes from input pointer on every
   iteration, shift into bit buffer. No conditional branch for refill check.
   ```c
   bitbuf |= get_unaligned_le64(in_next) << bitsleft;
   ```

3. **Branchless LZ77 copy**: Always copy a fixed 32-byte chunk from the back-reference
   source, even for short matches. The output pointer advances by the actual match length.
   This avoids branching on match length.

4. **Near-end-of-buffer fallback**: The fast path reads up to 8 bytes ahead of the
   current position. A "careful" slow path handles the last ~32 bytes of each block.

5. **Whole-buffer API**: Unlike zlib's streaming interface, libdeflate operates on
   the entire compressed/decompressed buffer at once, eliminating state management overhead.

### Multi-Symbol Decode Detail
The decode table maps 11 input bits to a decode result:
- For entries where all decoded symbols are literals (0-255):
  - Entry encodes up to 4 literal bytes + total bits consumed
  - Fast path: write 4 bytes to output, advance bit buffer by total_bits
- For entries containing a length/distance code:
  - Entry encodes the first symbol + bits consumed for just that symbol
  - Decoder falls back to single-symbol path for the back-reference

This approach is highly effective because ~70-90% of decoded symbols in typical
workloads are literals, so the multi-symbol fast path is taken most of the time.

### Performance Characteristics
- 2-3× faster than zlib, ~1.5-2× faster than zlib-ng for decompression
- Multi-symbol decode is the primary contributor to the speedup
- Whole-buffer API avoids per-call overhead of zlib's streaming interface
- The unconditional refill eliminates ~1 branch per symbol (saves ~2 cycles/symbol)

---

## 4. Intel ISA-L (Intelligent Storage Acceleration Library)

| Property | Details |
|----------|---------|
| **Language** | C + x86 assembly (NASM) |
| **Repository** | https://github.com/intel/isa-l |
| **License** | BSD-3 |
| **Decompression strategy** | Two-level table Huffman decode, semi-dynamic compression tables |
| **SIMD usage** | SSE4.2, AVX2, AVX-512 for compression; mostly scalar inflate |
| **Table sizes** | 10-bit primary lookup table |
| **Bit buffer** | 64-bit with efficient refill |
| **LZ77 copy** | Optimized with rep movsb or SIMD copies |
| **Throughput** | ~600-1000 MB/s on modern x86-64 (single core) |

### Key Optimizations
1. **Assembly inner loops**: Critical decompression paths hand-written in NASM assembly
2. **Semi-dynamic compression**: Novel compression table type between static and dynamic
   that offers near-dynamic compression ratio with near-static decompression speed
3. **Optimized inflate**: Larger primary table (10 bits) to reduce secondary lookups
4. **Efficient checksum**: Hardware CRC32C instruction integration

### Semi-Dynamic Compression Innovation
ISA-L introduces "semi-dynamic" Huffman tables:
- Pre-defined set of Huffman tables (not per-block dynamic, not RFC-fixed static)
- Encoder selects best table from pre-computed set based on block statistics
- Decompressor can use pre-built lookup tables for these known table configurations
- Result: compression ratio close to dynamic, decompression speed close to static

### Performance Characteristics
- Faster than zlib but generally slower than libdeflate for single-core decompression
- SIMD primarily benefits compression side (hash matching, table construction)
- Inflate performance competitive with zlib-ng, slightly behind libdeflate
- Assembly implementation ensures minimal overhead but limits portability

---

## 5. Chromium zlib fork

| Property | Details |
|----------|---------|
| **Language** | C |
| **Repository** | https://chromium.googlesource.com/chromium/src/+/HEAD/third_party/zlib/ |
| **License** | zlib license |
| **Decompression strategy** | Modified zlib inflate_fast with SIMD enhancements |
| **SIMD usage** | SSE4.2, SSSE3, NEON (ARM), CRC32 hardware instructions |
| **Table sizes** | Same as zlib (9-bit primary) |
| **Bit buffer** | 64-bit on 64-bit platforms |
| **LZ77 copy** | SIMD-accelerated copies using 128-bit loads/stores |
| **Throughput** | ~400-700 MB/s on modern x86-64 (single core) |

### Key Optimizations
1. **SIMD Adler32**: SSSE3-accelerated Adler32 computation (significant for gzip)
2. **SIMD CRC32**: PCLMULQDQ-based CRC32 computation
3. **Improved inflate_fast**: Backport of some zlib-ng optimizations
4. **NEON support**: ARM SIMD optimizations for mobile/ARM platforms
5. **Whole-buffer variants**: Some paths optimized for known buffer sizes

### Performance Characteristics
- Primary focus is web-content decompression (HTML, JS, CSS)
- Optimizations target real Chrome workloads (many small DEFLATE streams)
- ~1.3-1.7× improvement over reference zlib
- Less aggressive than libdeflate (maintains zlib API compatibility)

---

## 6. Cloudflare zlib fork

| Property | Details |
|----------|---------|
| **Language** | C |
| **Repository** | https://github.com/cloudflare/zlib |
| **License** | zlib license |
| **Decompression strategy** | Modified zlib with AVX2-accelerated longest match |
| **SIMD usage** | AVX2 (primarily for compression), SSE4.2 for CRC32 |
| **Table sizes** | Standard zlib 9-bit primary |
| **Bit buffer** | Standard zlib approach |
| **LZ77 copy** | Minor improvements over standard zlib |
| **Throughput** | ~350-600 MB/s on modern x86-64 (decompression, single core) |

### Key Optimizations
1. **AVX2 longest match**: SIMD-accelerated string matching for compression
2. **PCLMULQDQ CRC32**: Hardware-accelerated CRC32
3. **Improved Adler32**: SIMD computation of Adler32 checksum
4. **Minor inflate improvements**: Some branch reduction in inflate path

### Performance Characteristics
- Primary focus is compression speed (server-side gzip for HTTP responses)
- Decompression improvements are modest compared to libdeflate/zlib-ng
- Maintains full zlib API compatibility
- Optimized for Cloudflare's specific workload (HTTP content compression)

---

## 7. zune-inflate (Rust)

| Property | Details |
|----------|---------|
| **Language** | Rust |
| **Repository** | https://github.com/image-rs/zune-inflate |
| **License** | MIT/Apache-2.0 |
| **Decompression strategy** | Table-based Huffman, branchless optimizations |
| **SIMD usage** | Minimal direct SIMD; benefits from Rust's auto-vectorization |
| **Table sizes** | 9-10 bit primary tables |
| **Bit buffer** | 64-bit with efficient management |
| **LZ77 copy** | Rust's copy_within/copy_from_slice |
| **Throughput** | ~400-700 MB/s on modern x86-64 (single core) |

### Key Optimizations
1. **Memory safety**: No undefined behavior by construction (Rust's ownership model)
2. **Branchless table lookups**: Exploits Rust's conditional move patterns
3. **Bounds-check elision**: Careful coding to enable compiler bounds-check removal
4. **Zero-copy integration**: Designed for image decoding pipelines (PNG)

### Performance Characteristics
- Competitive with Chromium zlib fork for decompression
- Safety guarantees without significant performance penalty
- Primary use case is PNG/image decoding (whole-buffer decompression)
- Slower than libdeflate due to lack of multi-symbol decode

---

## 8. Starflate (C++23)

| Property | Details |
|----------|---------|
| **Language** | C++23 |
| **Repository** | https://github.com/garymm/starflate |
| **License** | MIT |
| **Decompression strategy** | Table-based Huffman with modern C++ |
| **SIMD usage** | None currently; focus on correctness and modern API |
| **Table sizes** | Configurable primary table |
| **Bit buffer** | Modern C++ bitstream reader using std::span |
| **LZ77 copy** | Standard library algorithms |
| **Throughput** | ~200-400 MB/s (correctness-focused, not performance-tuned) |

### Key Characteristics
- Uses C++23 features (std::expected, std::span, constexpr, concepts)
- Focus on clean, modern, correct implementation
- Serves as a reference/educational implementation
- Not yet performance-competitive with C implementations

---

## Comparative Summary

| Implementation | Language | Huffman Strategy | SIMD | Multi-Symbol | Throughput (MB/s) | vs zlib |
|---------------|----------|-----------------|------|-------------|-------------------|---------|
| zlib | C | 2-level table, 9-bit | None | No | 250-400 | 1.0× |
| Cloudflare zlib | C | 2-level table, 9-bit | SSE4.2 CRC | No | 350-600 | 1.3-1.5× |
| Chromium zlib | C | 2-level table, 9-bit | SSE4.2/SSSE3 | No | 400-700 | 1.5-1.7× |
| zlib-ng | C | 2-level table, 9-bit | SSE2/AVX2 | Limited | 500-800 | 1.8-2.0× |
| ISA-L | C+asm | 2-level table, 10-bit | SSE4.2/AVX2 | No | 600-1000 | 2.0-2.5× |
| zune-inflate | Rust | Table-based | Auto-vec | No | 400-700 | 1.5-1.7× |
| libdeflate | C | Multi-symbol, 11-bit | SSE2/BMI2 | **Yes (4-sym)** | 800-1500 | 3.0-3.8× |
| Starflate | C++23 | Table-based | None | No | 200-400 | 0.8-1.0× |

---

## Key Takeaways for Optimization

### 1. Multi-Symbol Decode is the Biggest Win
libdeflate's multi-symbol decode tables are the single most impactful optimization,
providing ~2× improvement over implementations that use equivalent bit-buffer management
but single-symbol decode. This directly addresses the serial Huffman dependency by
decoding multiple consecutive literals in a single table lookup.

### 2. Unconditional Bit-Buffer Refill Eliminates Branches
Loading 8 bytes unconditionally (instead of conditionally checking if refill is needed)
removes one branch per symbol and enables the CPU's branch predictor to focus on the
symbol-type dispatch (literal vs length code).

### 3. Branchless LZ77 Copy Reduces Mispredictions
Always copying a fixed chunk (32 bytes) regardless of actual match length avoids
branching on match length. The extra bytes written are overwritten by subsequent output.
This is safe because the output buffer must have sufficient overrun space.

### 4. Whole-Buffer API Avoids State Management
Operating on complete buffers eliminates per-call overhead of streaming interfaces
and enables the decoder to use larger temporary buffers and make assumptions about
data availability.

### 5. SIMD Benefits are Concentrated in Checksums and Copies
For decompression, SIMD provides the most benefit in:
- CRC32/Adler32 computation (offloading the checksum bottleneck)
- LZ77 wide copies (128/256-bit stores for non-overlapping matches)
- SIMD has NOT been successfully applied to the Huffman decode loop itself in
  any production single-stream decoder

### 6. Table Size vs Cache Pressure Tradeoff
- 9-bit primary: 2KB (fits comfortably in L1)
- 11-bit primary: 8KB (still fits in L1, enables multi-symbol decode)
- 13-bit primary: 32KB (fills L1, may cause pressure with other working set)
- The sweet spot appears to be 10-11 bits for the primary table

### 7. Remaining Bottleneck: Serial Huffman Dependency
Even in the best implementation (libdeflate), the fundamental serial dependency
remains: each symbol's decode depends on the previous symbol to determine bit offset.
Multi-symbol decode mitigates this for runs of literals but back-references still
introduce serial steps (length + extra + distance + extra = 4 sequential decodes).

---

## Gap to 2× Over zlib-ng Target

Current state of the art (libdeflate) achieves ~1.5-2× over zlib-ng.
To reach ≥2× over zlib-ng (which is itself ~1.8-2× over zlib), we need:
- Total speedup of ~3.6-4× over reference zlib
- This requires going beyond libdeflate's current techniques

Promising directions beyond existing implementations:
1. **Wider multi-symbol tables** (decode 6-8 symbols for literal runs)
2. **SIMD-assisted literal extraction** (when literal run detected, use SIMD to
   bulk-extract from bitstream)
3. **Better back-reference handling** (single-lookup length+distance decode)
4. **Bitstream format exploitation** (use properties of canonical Huffman codes
   for faster table construction per dynamic block)

---

*Survey compiled 2026-03-04. Throughput numbers are approximate ranges from published
benchmarks and may vary with CPU model, workload, and compiler.*
