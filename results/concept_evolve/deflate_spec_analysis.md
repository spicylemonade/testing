# DEFLATE Specification Deep-Dive and Bottleneck Decomposition

## 1. RFC 1951: DEFLATE Compressed Data Format Anatomy

### 1.1 Overview

DEFLATE (RFC 1951, Deutsch 1996) compresses data using a combination of **LZ77** (sliding-window dictionary matching) and **Huffman coding**. A compressed stream consists of a series of **blocks**, each independently choosing its compression strategy.

### 1.2 Block Types

Each block begins with 3 header bits:
- **BFINAL** (1 bit): Set on the last block
- **BTYPE** (2 bits): Block type
  - `00`: Stored (no compression) — raw data with LEN/NLEN header
  - `01`: Fixed Huffman codes — pre-defined Huffman tables
  - `10`: Dynamic Huffman codes — custom tables transmitted in-band
  - `11`: Reserved (error)

### 1.3 Literal/Length/Distance Alphabet

The compressed data stream consists of interleaved elements from two alphabets:

**Literal/Length alphabet** (0–285):
- 0–255: Literal byte values
- 256: End-of-block marker
- 257–285: Length codes (3–258 bytes), some with 0–5 extra bits

**Distance alphabet** (0–29):
- Distance codes (1–32768 bytes back), with 0–13 extra bits

A decoded element is either:
1. A **literal byte** (value 0–255) → written directly to output
2. A **<length, distance> pair** (LZ77 match) → copy `length` bytes from `distance` bytes back in the output

### 1.4 Huffman Table Encoding

DEFLATE uses **canonical Huffman codes**: given code lengths, the actual codes are deterministically computed using a simple algorithm (sort by length, assign consecutive values within each length).

For **dynamic blocks (BTYPE=10)**, the Huffman tables are themselves compressed:
1. HLIT (5 bits): # of literal/length codes - 257
2. HDIST (5 bits): # of distance codes - 1
3. HCLEN (4 bits): # of code-length codes - 4
4. Code lengths for a "meta-Huffman" alphabet (transmitted in a specific permuted order: 16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15)
5. Huffman-coded code lengths for literal/length and distance alphabets
   - Code 16: Repeat previous 3–6 times
   - Code 17: Repeat 0 for 3–10 times
   - Code 18: Repeat 0 for 11–138 times

### 1.5 Bit Packing

- Data elements packed LSB-first within bytes
- Huffman codes packed MSB-first (bit-reversed relative to other data)
- Blocks do not align to byte boundaries (except stored blocks, which pad to next byte)

### 1.6 LZ77 Constraints

- Maximum back-reference distance: 32,768 bytes (32KB sliding window)
- Maximum match length: 258 bytes
- Back-references can cross block boundaries
- Overlapping copies are valid (distance < length), used for run-length encoding

---

## 2. RFC 1950: zlib Wrapper

The zlib format wraps DEFLATE with a minimal header and checksum:

```
+---+---+=====================+---+---+---+---+
|CMF|FLG|...DEFLATE data...   |    ADLER32    |
+---+---+=====================+---+---+---+---+
```

- **CMF** byte: CM (4 bits, =8 for DEFLATE) + CINFO (4 bits, log2(window) - 8)
- **FLG** byte: FCHECK (5 bits), FDICT (1 bit), FLEVEL (2 bits)
- CMF*256 + FLG must be divisible by 31
- Optional 4-byte DICTID if FDICT is set
- **ADLER-32** checksum (4 bytes, big-endian) over uncompressed data
  - s1 = sum of bytes mod 65521; s2 = sum of s1 values mod 65521
  - Faster than CRC-32; can be vectorized with SIMD

---

## 3. RFC 1952: gzip Wrapper

The gzip format wraps DEFLATE with a richer header:

```
+---+---+---+---+---+---+---+---+---+---+
|ID1|ID2|CM |FLG|     MTIME     |XFL|OS |
+---+---+---+---+---+---+---+---+---+---+
```

- **ID1=0x1F, ID2=0x8B**: Magic bytes
- **CM=8**: DEFLATE compression method
- **FLG**: Bitfield for FTEXT, FHCRC, FEXTRA, FNAME, FCOMMENT
- Optional: extra field (XLEN + data), filename, comment, header CRC16
- Trailer: **CRC-32** (4 bytes) + **ISIZE** (4 bytes, original size mod 2^32)

Key difference from zlib: gzip uses CRC-32 (not ADLER-32) and supports file metadata.

---

## 4. Computational Bottlenecks in DEFLATE Decompression

### Bottleneck 1: Huffman Decode (Table Lookup) — ~35-45% of cycles

**Description:** Each symbol requires a table lookup indexed by the next N bits from the bit stream. For an 11-bit table, this is a 2048-entry or 4096-entry table (depending on entry size).

**Cycle cost:** The critical path per symbol is:
- Extract peek bits from bit buffer: 1 cycle (shift/mask)
- Table lookup: 4-5 cycles (L1D cache load latency; Skylake=4, Zen4/Golden Cove=5)
- Bit buffer update (shift by code length): 1 cycle
- **Total: 6-7 cycles per symbol on the critical path**

Per Fabian Giesen's analysis of Oodle Data 6-stream Huffman decoders (2023): with a 4-instruction decode step using BMI2 (ANDN, MOVZX, SHRX, MOV), the measured throughput is ~1.83 cycles/symbol on Skylake with 6 interleaved streams, vs. ~2.79 cycles/symbol with 3 streams. Single-stream decoders are bottlenecked at ~7 cycles/symbol by the serial dependency chain.

Per cbloom's measurements (2015): single-stream table-based Huffman decode achieves 325-415 MB/s depending on technique, with "ANS-style" state-based decode being fastest at 415 MB/s.

**Why it's a bottleneck:** In DEFLATE, Huffman decode is purely sequential — you must decode symbol N to know where symbol N+1 starts. This serial dependency chain is the fundamental throughput limiter.

### Bottleneck 2: LZ77 Copy (Back-Reference Resolution) — ~20-30% of cycles

**Description:** When a <length, distance> pair is decoded, the decompressor must copy `length` bytes from `distance` bytes back in the output buffer.

**Cycle cost:**
- Short copies (3-8 bytes): 2-4 cycles via register-width load/store
- Medium copies (9-128 bytes): 5-15 cycles via rep movsb or SIMD memcpy
- Long copies (129-258 bytes): 10-30+ cycles
- **Overlapping copies (distance < length):** Cannot use wide loads; must emit byte-by-byte. Worst case: distance=1 (run-length), 258 cycles for 258-byte copy.
- Cache-cold copies (distance > L1 size): Additional 10-20 cycles for L2/L3 access

Per Intel ISA-L documentation and libdeflate benchmarks: LZ77 copy accounts for 20-30% of total decompression time on typical data. On highly compressible data (many long matches), it can dominate.

**Why it's a bottleneck:** Variable-length copies with unpredictable distances cause irregular memory access patterns. Short overlapping copies prevent vectorization. Large distances cause cache misses.

### Bottleneck 3: Bit-Stream Parsing (Bit Buffer Management) — ~15-20% of cycles

**Description:** DEFLATE's variable-length codes require maintaining a bit buffer, refilling it from the input stream, and extracting variable numbers of bits for Huffman codes and extra bits.

**Cycle cost:**
- Bit buffer refill: 3-5 cycles (load + byte swap + OR + shift)
- Extra bits extraction (length/distance): 2-3 cycles per extraction
- Per Giesen (2023): the refill critical path is 9-12 cycles per refill, done once per ~5 symbols with 6-stream interleaving

**Key overhead sources:**
- Byte swap for big-endian bit packing within little-endian memory: ~2 cycles (Intel BSWAP)
- Unaligned memory access for refill: 0-1 extra cycles on modern x86
- Tracking consumed bits: 1-2 instructions per symbol

**Why it's a bottleneck:** The bit buffer update is on the serial dependency chain with Huffman decode. Each symbol consumed changes the bit position, which must be known before the next peek.

### Bottleneck 4: Branch Misprediction — ~10-15% of cycles

**Description:** The inner decompression loop has several unpredictable branches:

1. **Literal vs. match decision:** After decoding a lit/len symbol, the decoder branches on whether the value is < 256 (literal), == 256 (end of block), or > 256 (match). On typical data, ~60-70% of symbols are literals, but the pattern is data-dependent and hard to predict.

2. **Extra bits presence:** Length codes 265-284 and distance codes 4-29 require extra bits. The number of extra bits varies.

3. **Block type dispatch:** At block boundaries, branch on BTYPE.

4. **Bit buffer refill condition:** Check whether the bit buffer needs refilling.

**Cycle cost:**
- Each branch misprediction: ~15-20 cycles (Skylake pipeline depth)
- Measured misprediction rates: 5-15% in zlib's inflate hot loop (data-dependent)
- Per Intel VTune profiles of zlib: branch mispredictions account for 10-15% of total cycles

libdeflate reduces this significantly using branchless techniques: conditional moves for literal/match dispatch, and fixed-structure decode loops that avoid most data-dependent branches.

**Why it's a bottleneck:** Even at 5% misprediction rate, with ~2 branches per symbol and 15-cycle penalty, the effective overhead is 0.05 × 2 × 15 = 1.5 cycles/symbol — significant when the decode itself is only 6-7 cycles.

### Bottleneck 5: Memory Bandwidth and Cache Pressure — ~5-10% of cycles

**Description:** Decompression touches three memory regions:
1. **Input buffer** (compressed data): Sequential read, ~0.5 bytes/symbol average
2. **Output buffer** (decompressed data): Sequential write, 1 byte/symbol for literals
3. **Decode tables**: Random read, 2-4 bytes/symbol, ideally L1-resident
4. **Sliding window** (for LZ77 copies): Random read, distance-dependent

**Cycle cost:**
- L1D hit: 4-5 cycles
- L2 hit: ~12 cycles (Skylake), ~12 cycles (Zen4)
- L3 hit: ~40 cycles (Skylake), ~40 cycles (Zen4)
- DRAM: ~200+ cycles

- Decode table (2KB-4KB for 11-bit table): Fits in L1D, ~0 extra cycles
- Decode table (32KB+ for multi-symbol): Spills to L2, +8-15 cycles/access
- LZ77 copy with distance > 32KB sliding window: Mostly L1-resident for short distances; L2/L3 for distances > ~16KB

**Theoretical bandwidth limit:** At 4 bytes/cycle DDR5 bandwidth and ~1.5 bytes read + 1 byte written per symbol, memory bandwidth is not the bottleneck for single-threaded decompression (~20 GB/s available vs. ~3 GB/s typical throughput). However, for multi-threaded parallel decompression with 8+ threads, memory bandwidth becomes a factor.

**Why it's a bottleneck:** While not the primary bottleneck for single-thread, cache pressure from LZ77 copies with large distances creates stalls. For parallel decompression, memory bandwidth becomes the ceiling.

### Bottleneck 6: Dynamic Huffman Table Construction — ~2-5% of total time

**Description:** For each dynamic block, the decompressor must:
1. Parse the code-length Huffman table (19 symbols max)
2. Decode code lengths for literal/length alphabet (up to 286 symbols)
3. Decode code lengths for distance alphabet (up to 30 symbols)
4. Build decode tables for both alphabets

**Cycle cost:**
- Parsing + building: ~1000-3000 cycles per block
- Amortized over a typical block of ~10K-100K symbols: 0.01-0.3 cycles/symbol
- Per Giesen (2023): table building is a measurable fraction of total Huffman decode time in Oodle Data, even with optimized builders

**Why it's a bottleneck:** Generally minor, but becomes significant for streams with many small blocks or when table building is not optimized. Also matters for latency-sensitive applications (small file decompression).

### Bottleneck 7: Checksum Computation (CRC-32 / ADLER-32) — ~3-8% of cycles

**Description:** gzip requires CRC-32 over uncompressed data; zlib requires ADLER-32.

**Cycle cost:**
- Scalar CRC-32: ~1 cycle/byte with lookup table, ~0.5 cycles/byte with PCLMULQDQ
- SIMD CRC-32 (using carryless multiply): ~0.1 cycles/byte with 256-byte chunks
- ADLER-32: ~0.3 cycles/byte scalar, ~0.05 cycles/byte with SIMD (NEON/SSE)
- Effectively free on modern hardware with SIMD, but a measurable tax without it

---

## 5. Summary: Cycle Budget per Symbol

| Bottleneck | Est. cycles/symbol | % of total | Amenable to SIMD? | Amenable to parallelism? |
|---|---|---|---|---|
| Huffman decode (table lookup) | 6-7 (serial), 1.3-1.8 (6-stream) | 35-45% | Indirect (multi-stream ILP) | Yes (multi-stream) |
| LZ77 copy | 1-3 (amortized) | 20-30% | Yes (wide memcpy) | Limited (cross-block deps) |
| Bit-stream parsing | 1-2 | 15-20% | Indirect (branchless refill) | Yes (multi-stream) |
| Branch misprediction | 0.5-1.5 | 10-15% | Yes (branchless, CMOV) | N/A |
| Memory/cache | 0.5-1 | 5-10% | Prefetch | Yes (more bandwidth) |
| Table construction | 0.01-0.3 | 2-5% | Limited | Per-block parallel |
| Checksum (CRC-32/ADLER-32) | 0.05-0.3 | 3-8% | Yes (PCLMULQDQ, NEON) | Yes (chunked) |

**Total estimated:** ~10-15 cycles/symbol single-stream zlib; ~4-6 cycles/symbol optimized (libdeflate-class); ~1.5-2 cycles/symbol with multi-stream Huffman (Oodle Data 6-stream).

**Key insight for 2-5x speedup over zlib:** The ~3x gap between zlib (~300-500 MB/s) and libdeflate (~1-2 GB/s) comes from branchless techniques, larger decode tables, and optimized LZ77 copy. The additional ~2x from libdeflate to Oodle-class (~3 GB/s Huffman-only) comes from multi-stream entropy coding. Combining both approaches (optimized single-thread + parallel blocks for the LZ77 layer) is the path to 2-5x over zlib.

---

## References

- RFC 1951: Deutsch, P. "DEFLATE Compressed Data Format Specification version 1.3" (May 1996)
- RFC 1950: Deutsch, P. and Gailly, J-L. "ZLIB Compressed Data Format Specification version 3.3" (May 1996)
- RFC 1952: Deutsch, P. "GZIP file format specification version 4.3" (May 1996)
- Giesen, F. "Entropy decoding in Oodle Data: x86-64 6-stream Huffman decoders" (Oct 2023)
- Giesen, F. "Entropy decoding in Oodle Data: x86-64 3-stream Huffman decoders" (Sep 2022)
- Bloom, C. "Huffman Performance" (Oct 2015)
- Collet, Y. "Smaller and faster data compression with Zstandard" (Meta Engineering, Aug 2016)
