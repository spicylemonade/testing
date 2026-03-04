# DEFLATE Specification Analysis (RFC 1951)

## Purpose

This document provides a deep technical analysis of the DEFLATE compressed data format
(RFC 1951) with a specific focus on identifying the serial dependencies that limit
decompression throughput. Understanding these dependencies is essential for designing
optimizations that break or reduce the serial bottleneck.

---

## 1. Overview of DEFLATE

DEFLATE combines two compression techniques:
1. **LZ77** — sliding-window dictionary compression (back-references to previously seen data)
2. **Huffman coding** — variable-length prefix codes for entropy encoding

A DEFLATE stream consists of a series of **blocks**, each independently Huffman-coded
but sharing the same LZ77 sliding window (up to 32 KB).

### Byte and Bit Ordering

- Multi-byte integers: **little-endian** (least-significant byte first)
- Bit packing: data elements packed starting from **least-significant bit** of each byte
- Huffman codes: packed starting from **most-significant bit** of the code
  (i.e., they are bit-reversed relative to other data elements)

This asymmetry between Huffman code bit ordering and data element bit ordering
is a key implementation detail that affects bit-buffer design.

---

## 2. Block Types and Headers

Every DEFLATE block begins with a 3-bit header:

```
+--------+--------+
| BFINAL | BTYPE  |
| 1 bit  | 2 bits |
+--------+--------+
```

- **BFINAL** (1 bit): Set to 1 if this is the last block in the stream.
- **BTYPE** (2 bits): Block type:
  - `00` = Stored (no compression)
  - `01` = Static Huffman codes (fixed, predefined)
  - `10` = Dynamic Huffman codes (per-block custom)
  - `11` = Reserved (error)

### 2.1 Stored Blocks (BTYPE=00)

```
+--+--+--+--+==============================+
|  LEN  |NLEN|    LEN bytes literal data    |
+--+--+--+--+==============================+
  2 bytes  2 bytes
```

- Any remaining bits in the current byte are **discarded** (byte-aligned).
- LEN: number of literal data bytes (0–65535).
- NLEN: one's complement of LEN (for integrity checking).
- Data: raw literal bytes, no encoding.

**Serial dependency impact**: None within the literal data. The only overhead
is header parsing. This block type is trivially parallelizable.

### 2.2 Static Huffman Blocks (BTYPE=01)

Use predefined (fixed) Huffman codes — no code tables transmitted in the stream.

**Literal/Length alphabet** (0–287):

| Value Range | Bit Length | Code Range              |
|-------------|------------|-------------------------|
| 0–143       | 8 bits     | 00110000–10111111       |
| 144–255     | 9 bits     | 110010000–111111111     |
| 256–279     | 7 bits     | 0000000–0010111         |
| 280–287     | 8 bits     | 11000000–11000111       |

**Distance alphabet** (0–31): All use 5 bits (uniform), plus extra bits per table.

**Serial dependency impact**: Fixed code lengths mean decoders can use a single
precomputed lookup table. Symbol bit-lengths are known a priori (7, 8, or 9 bits
for lit/len; 5 bits for distance), which enables more aggressive speculative decoding.

### 2.3 Dynamic Huffman Blocks (BTYPE=10)

The block header transmits custom Huffman tables:

```
+------+-------+--------+
| HLIT | HDIST | HCLEN  |   (5 + 5 + 4 = 14 bits)
+------+-------+--------+

Followed by:
  (HCLEN + 4) × 3 bits: code lengths for the code-length alphabet
  HLIT + 257 code lengths: literal/length alphabet (Huffman-encoded)
  HDIST + 1 code lengths: distance alphabet (Huffman-encoded)
```

#### Code-Length Alphabet

The code-length alphabet (0–18) is itself Huffman-encoded:
- 0–15: Literal code lengths
- 16: Repeat previous code length 3–6 times (2 extra bits)
- 17: Repeat zero 3–10 times (3 extra bits)
- 18: Repeat zero 11–138 times (7 extra bits)

The code-length codes are transmitted in a specific permutation order:
`16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15`

This ordering prioritizes the most commonly used code lengths to minimize overhead.

**Serial dependency impact**: Dynamic header parsing is inherently serial
(each code-length symbol depends on the previous to locate the next in the bitstream).
However, this overhead is amortized over the entire block, so block size matters.

---

## 3. Huffman Code Construction Algorithm

DEFLATE uses **canonical Huffman codes** with the following constraints:
1. Codes of the same bit length have lexicographically consecutive values
2. Shorter codes precede longer codes lexicographically
3. Maximum code length: 15 bits (lit/len and distance) or 7 bits (code-length alphabet)

### Construction Algorithm (from code lengths):

```
Step 1: Count codes per length
    bl_count[N] = number of codes with length N, for N >= 1

Step 2: Compute base codes
    code = 0
    bl_count[0] = 0
    for bits = 1 to MAX_BITS:
        code = (code + bl_count[bits-1]) << 1
        next_code[bits] = code

Step 3: Assign codes
    for n = 0 to max_code:
        len = tree[n].Len
        if len != 0:
            tree[n].Code = next_code[len]
            next_code[len]++
```

### Decode Table Construction

For decompression, the canonical structure enables efficient table-based decoding:

**Single-level table** (e.g., 9-bit lookup):
- Index: next N bits from the bitstream
- Value: decoded symbol + consumed bit count
- For codes longer than N bits: use a secondary table (two-level lookup)

**Key property**: Because codes are canonical, the table can be constructed in O(alphabet_size)
time, which is important since dynamic blocks require rebuilding tables per block.

---

## 4. The Serial Dependency Chain

This is the **core bottleneck** for DEFLATE decompression throughput.

### The Fundamental Problem

```
Bitstream: |...symbol_N bits...|...symbol_N+1 bits...|...symbol_N+2 bits...|
           ^                    ^                      ^
           |                    |                      |
           known                UNKNOWN until          UNKNOWN until
           start position       symbol_N decoded       symbol_N+1 decoded
```

Each Huffman symbol in the DEFLATE bitstream has a **variable number of bits**.
The start position of symbol N+1 is:

    start(N+1) = start(N) + bitlength(symbol_N) + extra_bits(symbol_N)

Where:
- `bitlength(symbol_N)` depends on which symbol was decoded (1–15 bits for lit/len)
- `extra_bits(symbol_N)` depends on the symbol value:
  - Literals (0–255): 0 extra bits
  - End-of-block (256): 0 extra bits
  - Length codes (257–285): 0–5 extra bits (length) + 5–13 bits (distance code + extra)
  - Total consumed bits per back-reference: length_code + length_extra + dist_code + dist_extra

### Dependency Chain Diagram

```
Symbol N:      [Huffman lookup] → symbol value → consumed bits
                                                      |
                                                      v
Symbol N+1:    bit_offset += consumed_bits → [Huffman lookup] → symbol value
                                                                      |
                                                                      v
Symbol N+2:    bit_offset += consumed_bits → [Huffman lookup] → ...
```

**Critical path per symbol** (for a table-based decoder):
1. Shift/mask bit buffer to extract next N bits (1 cycle, depends on bit_offset)
2. Table lookup (L1 cache hit: ~4 cycles latency)
3. Determine consumed bits from table entry (0 cycles, in same load)
4. Update bit_offset (1 cycle, ADD)
5. Branch on symbol type: literal vs length code vs EOB (1 cycle + misprediction penalty)

**Minimum cycles per symbol**: ~6-7 cycles on modern x86-64 (assuming L1 hits,
no branch mispredictions). With mispredictions (~10-20% of symbols are back-refs):
~8-12 cycles per symbol average.

### Back-Reference Dependency (LZ77)

Back-references create an additional serial dependency in the **output stream**:

```
Output position P:
  if literal: output[P] = symbol_value (independent of previous output)
  if back-ref: output[P..P+len] = output[P-dist..P-dist+len]
               (depends on output[P-dist] which may itself be a recent back-ref)
```

When distance < length (overlapping copy), each output byte depends on a
recently written byte, creating a **true data dependency** that cannot be
trivially parallelized.

---

## 5. LZ77 Length/Distance Encoding

### Length Codes (literal/length alphabet values 257–285)

| Code | Extra Bits | Length(s) | Code | Extra Bits | Length(s)  |
|------|-----------|-----------|------|-----------|------------|
| 257  | 0         | 3         | 271  | 2         | 27-30      |
| 258  | 0         | 4         | 272  | 2         | 31-34      |
| 259  | 0         | 5         | 273  | 3         | 35-42      |
| 260  | 0         | 6         | 274  | 3         | 43-50      |
| 261  | 0         | 7         | 275  | 3         | 51-58      |
| 262  | 0         | 8         | 276  | 3         | 59-66      |
| 263  | 0         | 9         | 277  | 4         | 67-82      |
| 264  | 0         | 10        | 278  | 4         | 83-98      |
| 265  | 1         | 11-12     | 279  | 4         | 99-114     |
| 266  | 1         | 13-14     | 280  | 4         | 115-130    |
| 267  | 1         | 15-16     | 281  | 5         | 131-162    |
| 268  | 1         | 17-18     | 282  | 5         | 163-194    |
| 269  | 2         | 19-22     | 283  | 5         | 195-226    |
| 270  | 2         | 23-26     | 284  | 5         | 227-257    |
|      |           |           | 285  | 0         | 258        |

### Distance Codes (0–29)

| Code | Extra Bits | Distance    | Code | Extra Bits | Distance        |
|------|-----------|-------------|------|-----------|-----------------|
| 0    | 0         | 1           | 15   | 6         | 193-256         |
| 1    | 0         | 2           | 16   | 7         | 257-384         |
| 2    | 0         | 3           | 17   | 7         | 385-512         |
| 3    | 0         | 4           | 18   | 8         | 513-768         |
| 4    | 1         | 5-6         | 19   | 8         | 769-1024        |
| 5    | 1         | 7-8         | 20   | 9         | 1025-1536       |
| 6    | 2         | 9-12        | 21   | 9         | 1537-2048       |
| 7    | 2         | 13-16       | 22   | 10        | 2049-3072       |
| 8    | 3         | 17-24       | 23   | 10        | 3073-4096       |
| 9    | 3         | 25-32       | 24   | 11        | 4097-6144       |
| 10   | 4         | 33-48       | 25   | 11        | 6145-8192       |
| 11   | 4         | 49-64       | 26   | 12        | 8193-12288      |
| 12   | 5         | 65-96       | 27   | 12        | 12289-16384     |
| 13   | 5         | 97-128      | 28   | 13        | 16385-24576     |
| 14   | 6         | 129-192     | 29   | 13        | 24577-32768     |

### Bits Consumed Per Back-Reference

Total bits per back-reference = length_code_bits + length_extra_bits + distance_code_bits + distance_extra_bits

- **Minimum**: 7 (lit/len) + 0 (extra) + variable_dist_code + 0 = ~12 bits (short match, close distance)
- **Maximum**: 15 (lit/len) + 5 (extra) + 15 (dist) + 13 (extra) = 48 bits (long match, far distance)
- **Typical**: ~20-30 bits for a back-reference

This variability exacerbates the serial dependency: the decoder cannot know
how many total bits a back-reference will consume until it has decoded both
the length code (with its extra bits) and the distance code (with its extra bits).

---

## 6. End-of-Block Sentinel

- Symbol 256 in the literal/length alphabet signals end of block.
- Always present at the end of compressed blocks (BTYPE=01 and BTYPE=10).
- After EOB, the decoder reads the next block's 3-bit header (BFINAL + BTYPE).
- For stored blocks (BTYPE=00), remaining bits in the current byte are discarded.

**Serial dependency impact**: Block boundaries are unpredictable from the bitstream alone.
The EOB symbol must be decoded to know where the next block starts. This prevents
parallel decoding of blocks unless block boundaries are pre-scanned.

---

## 7. Summary of Serial Dependencies

### Primary Serial Dependencies (Throughput Limiters)

| Dependency | Description | Severity |
|-----------|-------------|----------|
| **Huffman bit-length chain** | Each symbol's start depends on previous symbol's length | **Critical** |
| **Back-reference resolution** | Length+distance extra bits consume variable additional bits | **High** |
| **LZ77 output dependency** | Overlapping copies depend on recently written data | **Medium** |
| **Block boundary detection** | EOB must be decoded to find next block | **Medium** |
| **Dynamic header parsing** | Code-length decoding is serial | **Low** (amortized) |

### Secondary Dependencies (Optimization Inhibitors)

| Dependency | Description | Impact |
|-----------|-------------|--------|
| **Bit-buffer refill** | Conditional refill adds branch per symbol | Branch misprediction |
| **Symbol type dispatch** | Literal vs length vs EOB branch | Branch misprediction |
| **Table size vs cache** | Larger tables = more coverage but more L1 misses | Cache pressure |
| **Bit-reversal** | Huffman code bit order ≠ data element bit order | Extra ALU ops |

---

## 8. Opportunities for Breaking Serial Dependencies

### 8.1 Speculative Multi-Symbol Decode

Since the most common symbols (literals) have known bit lengths in typical
dynamic Huffman trees (7–9 bits), we can precompute decode tables that
speculatively decode **multiple symbols** assuming they are all short:

```
Table entry for N input bits:
  [symbol_1, symbol_2, symbol_3, ..., total_bits_consumed, num_symbols_decoded]
```

If all decoded symbols are literals (the common case), the speculation succeeds
and we advance by total_bits_consumed. If any symbol is a length code or exceeds
the table, we fall back to single-symbol decoding.

**Potential speedup**: 2–4× for literal-heavy streams (text, HTML, JS).

### 8.2 Branchless Bit-Buffer Management

Replace conditional refill:
```c
// Traditional (branchy):
if (bits_remaining < NEEDED) { refill(); }

// Branchless (always refill):
bitbuffer |= (uint64_t)(*(uint64_t*)input_ptr) << bits_remaining;
// Consume: shift right by consumed, advance input_ptr periodically
```

### 8.3 SIMD Literal Run Acceleration

When consecutive literals are detected, use SIMD to bulk-extract and write them:
- AVX2: process 32 literal bytes per iteration
- Requires detecting "literal run" stretches in the decode table

### 8.4 Precomputed Block Boundary Scan

Pre-scan the bitstream to identify block boundaries (by decoding just the
Huffman headers and counting symbols, without producing output), then decode
blocks in parallel. This is a two-pass approach with limited applicability.

### 8.5 Optimized LZ77 Copy

- Use wide SIMD copies (32 bytes at a time) for non-overlapping back-references
- Use shuffle-based repetition for small-distance overlapping copies (e.g., distance=1 → memset)

---

## 9. Critical Constants and Limits

| Parameter | Value | Notes |
|-----------|-------|-------|
| Max code length (lit/len, dist) | 15 bits | Affects table size |
| Max code length (code-length) | 7 bits | For dynamic header |
| Literal alphabet size | 256 | Symbols 0–255 |
| Lit/len alphabet size | 286 | Symbols 0–285 (286–287 unused) |
| Distance alphabet size | 30 | Symbols 0–29 (30–31 unused) |
| Code-length alphabet size | 19 | Symbols 0–18 |
| Max match length | 258 bytes | Code 285 |
| Min match length | 3 bytes | Code 257 |
| Max back-reference distance | 32,768 bytes | 32 KB sliding window |
| Max stored block size | 65,535 bytes | Limited by 16-bit LEN |
| Max extra bits (length) | 5 | Code 281–284 |
| Max extra bits (distance) | 13 | Codes 28–29 |

---

## 10. Bit Packing Detail and Decoder State Machine

### Decoder State Machine

```
State: BLOCK_HEADER
  → Read BFINAL (1 bit), BTYPE (2 bits)
  → If BTYPE=00: → STORED_BLOCK
  → If BTYPE=01: → STATIC_HUFFMAN (use fixed tables)
  → If BTYPE=10: → DYNAMIC_HEADER
  → If BTYPE=11: → ERROR

State: STORED_BLOCK
  → Align to byte boundary
  → Read LEN (16 bits), NLEN (16 bits)
  → Copy LEN bytes verbatim
  → If BFINAL: → DONE, else → BLOCK_HEADER

State: DYNAMIC_HEADER
  → Read HLIT (5), HDIST (5), HCLEN (4)
  → Read (HCLEN+4)×3 bits → code-length code lengths
  → Build code-length Huffman table
  → Decode HLIT+257 lit/len code lengths
  → Decode HDIST+1 distance code lengths
  → Build lit/len and distance Huffman tables
  → → COMPRESSED_DATA

State: COMPRESSED_DATA (also entered from STATIC_HUFFMAN)
  → Loop:
    → Decode lit/len symbol from bitstream
    → If symbol < 256: output literal byte
    → If symbol = 256: EOB → if BFINAL: DONE, else BLOCK_HEADER
    → If symbol > 256: decode length extra bits, decode distance, decode dist extra bits
      → Copy from output buffer (LZ77 back-reference)
```

### Bit Buffer Typical Implementation

```
uint64_t bitbuffer;    // Holds up to 64 bits
int      bits_left;    // Number of valid bits in buffer
uint8_t *input_ptr;    // Next byte to read from input

// Refill (unconditional, loads 8 bytes):
bitbuffer |= load_le64(input_ptr) << bits_left;
// (input_ptr advanced separately when bits_left drops below threshold)

// Extract N bits:
value = bitbuffer & ((1 << N) - 1);
bitbuffer >>= N;
bits_left -= N;

// Huffman decode (table-based):
entry = table[bitbuffer & TABLE_MASK];
symbol = entry >> 4;         // or similar encoding
nbits  = entry & 0xF;
bitbuffer >>= nbits;
bits_left -= nbits;
```

---

*Analysis based on RFC 1951 (Deutsch, May 1996). Total lines: ~250+.*
*Serial dependency analysis informed by study of zlib, libdeflate, and zlib-ng source code.*
