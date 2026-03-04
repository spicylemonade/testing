# RFC 4648 Base64 Algorithm Analysis

**Date:** 2026-03-04  
**Item:** item_004  
**Primary reference:** \cite{rfc4648}

## 1. The 4-Input-Character to 3-Output-Byte Mapping

Base64 encoding represents binary data using 64 printable ASCII characters. The fundamental unit of operation is:

```
4 Base64 characters (4 x 6 bits = 24 bits) -> 3 output bytes (3 x 8 bits = 24 bits)
```

**Encoding direction (for context):**
```
Input bytes:     [AAAAAAAA] [BBBBBBBB] [CCCCCCCC]
6-bit groups:    [AAAAAA] [AABBBB] [BBBBCC] [CCCCCC]
Base64 indices:     i0       i1       i2       i3
```

**Decoding direction (our focus):**
```
Base64 chars:    c0  c1  c2  c3
6-bit values:    v0  v1  v2  v3  (each in range 0-63)
Output bytes:    [(v0<<2)|(v1>>4)]  [((v1&0xF)<<4)|(v2>>2)]  [((v2&0x3)<<6)|v3]
```

The decode operation for a single 4-character group produces exactly 3 bytes through bit manipulation.

## 2. The 6-Bit Extraction and Recombination Arithmetic

Given four 6-bit values `v0, v1, v2, v3` (each guaranteed to be in `[0, 63]` after valid lookup):

```c
byte0 = (v0 << 2) | (v1 >> 4);    // Top 6 bits from v0, top 2 from v1
byte1 = (v1 << 4) | (v2 >> 2);    // Bottom 4 of v1, top 4 from v2 (masked to low 8 bits)
byte2 = (v2 << 6) | v3;           // Bottom 2 of v2, all 6 from v3 (masked to low 8 bits)
```

**Bit layout (24-bit concatenation):**
```
v0:      [543210--]
v1:      [--5432][10----]
v2:      [----54][3210--]
v3:      [------][543210]
         byte0    byte1    byte2
```

**SIMD optimization insight:** The multiply-add approach \cite{mula2018avx2base64} computes this in 2 instructions:

```
Step 1: PMADDUBSW([v3,v2,v1,v0], [0x01,0x40,0x01,0x40])
  = [v2*64 + v3, v0*64 + v1]  (as 16-bit words)
  = [00ccccccdddddd, 00aaaaaabbbbbb]

Step 2: PMADDWD(result, [0x0001,0x1000])
  = [aaaaaabbbbbbccccccdddddd]  (as 32-bit dword)
```

This is correct because:
- `v0*64 + v1 = (v0 << 6) | v1` (upper 12 bits of 24-bit output)
- `v2*64 + v3 = (v2 << 6) | v3` (lower 12 bits of 24-bit output)
- Combining: `(upper << 12) | lower = (v0 << 18) | (v1 << 12) | (v2 << 6) | v3`

After byte reordering (big-endian to little-endian), this yields the 3 output bytes.

## 3. The Alphabet Lookup

### Standard Base64 alphabet (RFC 4648 Table 1):

| Character range | ASCII range | 6-bit value |
|----------------|-------------|-------------|
| A-Z | 65-90 | 0-25 |
| a-z | 97-122 | 26-51 |
| 0-9 | 48-57 | 52-61 |
| + | 43 | 62 |
| / | 47 | 63 |
| = | 61 | padding |

### Base64url variant (RFC 4648 Section 5):

| Changed chars | ASCII | 6-bit value |
|--------------|-------|-------------|
| - | 45 | 62 (replaces +) |
| _ | 95 | 63 (replaces /) |

### Lookup implementation strategies:

1. **256-byte table (scalar):** `decode_table[char] -> 6-bit value or error`. Simple, fast for scalar, but 256 bytes of L1 cache footprint.

2. **PSHUFB nibble decomposition (SIMD):** Decompose ASCII byte `b` into `hi = b >> 4` and `lo = b & 0xF`. Use PSHUFB with 16-byte LUTs indexed by `hi` to determine the shift/validation per nibble range. Cost: 3 PSHUFB + comparisons.

3. **VPERMB 64-byte table (AVX-512 VBMI):** A single `vpermb` instruction with a 64-byte table containing all 64 decoded values indexed by the 6-bit position. Requires first mapping ASCII to indices 0-63, then the VPERMB lookup.

4. **Range-shift approach:** Classify characters by range comparison and add a per-range constant:
   ```
   if A<=c<=Z: value = c - 65
   if a<=c<=z: value = c - 71  (97 - 26)
   if 0<=c<=9: value = c + 4   (48 -> 52)
   if c=='+': value = 62
   if c=='/': value = 63
   ```

## 4. Padding Rules

RFC 4648 Section 4 specifies padding with `=`:

| Input bytes | Base64 chars | Padding |
|-------------|-------------|---------|
| 3n | 4n | None |
| 3n+1 | 4n+2 + `==` | 2 pad chars |
| 3n+2 | 4n+3 + `=` | 1 pad char |

**Decoding with padding:**
- `XX==` (2 Base64 chars + 2 padding) -> 1 output byte
- `XXX=` (3 Base64 chars + 1 padding) -> 2 output bytes
- `XXXX` (4 Base64 chars, no padding) -> 3 output bytes

**Critical constraint for SIMD:** Padding only appears at the very end of the input stream, never in the middle. This means the main SIMD loop processes only full 4-character groups. Padding handling can be deferred to a scalar epilogue.

**Base64url and optional padding:** RFC 4648 Section 3.2 notes that padding MAY be omitted in some contexts (particularly Base64url for JWT). Decoders should handle both padded and unpadded input.

## 5. Whitespace Handling in MIME Contexts

RFC 2045 (MIME) specifies that Base64-encoded content must have line breaks (CRLF) every 76 characters. RFC 4648 Section 3.1 states:

> Implementations MUST NOT add line feeds to base-encoded data unless the specification referring to this document explicitly directs base encoders to add line feeds.

**For decoders:** Different contexts require different whitespace handling:
- **Strict RFC 4648:** No whitespace allowed; reject on any non-Base64 character.
- **MIME RFC 2045:** Must ignore CRLF sequences within the data.
- **Liberal:** Ignore all whitespace (common in practice).

**SIMD impact:** Whitespace handling introduces a compaction problem. If whitespace characters appear within a SIMD vector, the valid Base64 characters must be "gathered" together before processing. This can be done via:
1. **Pre-scan removal:** Remove whitespace in a separate pass before decoding.
2. **Masked processing:** Use SIMD mask operations to skip whitespace positions.
3. **Assumption of no whitespace:** For bulk binary data (most common case), assume no whitespace and validate.

Our implementation will support strict mode (no whitespace) for the SIMD fast path, with an optional pre-processing step for MIME-style whitespace removal.

## 6. Formal Proof: Decoding is Embarrassingly Parallel

**Theorem:** The decoding of non-overlapping 4-byte Base64 groups is embarrassingly parallel (no data dependencies between groups).

**Proof:**

Let the input be a sequence of Base64 characters: `c_0, c_1, c_2, ..., c_{4n-1}` where `n` is the number of 4-character groups.

Define the decoding function for group `k`:
```
D(k) = decode(c_{4k}, c_{4k+1}, c_{4k+2}, c_{4k+3}) -> (byte_{3k}, byte_{3k+1}, byte_{3k+2})
```

where:
```
byte_{3k}   = (lookup(c_{4k}) << 2) | (lookup(c_{4k+1}) >> 4)
byte_{3k+1} = ((lookup(c_{4k+1}) & 0xF) << 4) | (lookup(c_{4k+2}) >> 2)
byte_{3k+2} = ((lookup(c_{4k+2}) & 0x3) << 6) | lookup(c_{4k+3})
```

**Observation 1:** `D(k)` reads only from indices `{4k, 4k+1, 4k+2, 4k+3}` of the input.

**Observation 2:** `D(k)` writes only to indices `{3k, 3k+1, 3k+2}` of the output.

**Observation 3:** For distinct groups `k != j`:
- Read sets are disjoint: `{4k..4k+3} ∩ {4j..4j+3} = ∅`
- Write sets are disjoint: `{3k..3k+2} ∩ {3j..3j+2} = ∅`
- No read-write overlap between groups

**Observation 4:** The `lookup()` function is a pure function (stateless table lookup) with no side effects.

**Observation 5:** No group's output depends on any other group's input or output.

**Therefore:** By Bernstein's conditions for parallel execution, all `D(k)` for `k = 0, 1, ..., n-1` can execute simultaneously without synchronization. The decoding is embarrassingly parallel with granularity of 4 input bytes / 3 output bytes. **QED.**

**SIMD exploitation:** A W-byte SIMD register can process `W/4` groups simultaneously:
- SSE (128-bit, 16 bytes): 4 groups -> 12 output bytes
- AVX2 (256-bit, 32 bytes): 8 groups -> 24 output bytes
- AVX-512 (512-bit, 64 bytes): 16 groups -> 48 output bytes
- SVE (128-2048 bit): `VL/4` groups -> `3*VL/4` output bytes

## 7. Identification of Sequential Dependencies

While the core decode is embarrassingly parallel, several aspects introduce sequential dependencies:

### 7.1 Validation (Parallelizable with Reduction)

Invalid character detection must cover the entire input. However, this is parallelizable: each SIMD lane independently checks its character and produces an error flag. The flags are then OR-reduced. This is a parallel reduction operation:

```
error_accumulator |= validate_simd(input_block)
// After all blocks:
if (error_accumulator != 0) return ERROR;
```

**Dependency:** Only the final error check is sequential (OR-reduction over blocks). Within a block, validation is fully parallel.

### 7.2 Padding at Stream End

Padding characters (`=`) are only valid at positions `{n-1}` and `{n-1, n-2}` of the input. This requires knowing the total input length. **This is NOT a sequential dependency for streaming** because padding detection only applies to the final 4-character group. The main loop can process all complete 4-character groups without considering padding.

### 7.3 Error Propagation Policy

Two strategies for error handling:
1. **Fail-fast:** Stop on first error. Introduces a branch in the SIMD loop that may cause mispredictions. Performance cost: ~10-15% due to branch overhead.
2. **Accumulate-and-report:** Process entire input, accumulating error flags, report at end. Branchless. Preferred for SIMD.

**Security consideration:** Accumulate-and-report is also preferred for constant-time behavior (timing side channels). The decoder should not reveal the position of an invalid character through timing variations. \cite{chatzigiannis2022malleability}

### 7.4 Output Compaction (4:3 Ratio)

SIMD processing of 32 input bytes produces 24 output bytes. The 24 useful bytes must be stored contiguously, requiring a compaction step. On AVX2, this is done via `vpshufb` + `vpermd` (lane-crossing permute). On AVX-512 VBMI, a single `vpermb` suffices. This compaction is per-block and introduces no inter-block dependency.

### 7.5 Streaming Chunk Boundaries

When decoding a stream in chunks, a 4-character group may be split across chunk boundaries. At most 3 bytes of carry state are needed between chunks. This is the only true sequential dependency in the streaming case.

**Carry state:** `struct { uint8_t buf[3]; uint8_t count; }` — at most 3 leftover bytes from the previous chunk that didn't form a complete 4-byte group.

## Summary of Parallelism Analysis

| Aspect | Parallel? | Granularity | SIMD Strategy |
|--------|-----------|-------------|---------------|
| Alphabet lookup | Yes | Per byte | PSHUFB / VPERMB / VTBL |
| Bit recombination | Yes | Per 4-byte group | PMADDUBSW + PMADDWD |
| Validation | Yes (with reduction) | Per byte + final OR | Compare + accumulate |
| Output compaction | Yes (per block) | Per SIMD block | Shuffle/permute |
| Padding handling | Sequential (end only) | Final group only | Scalar epilogue |
| Streaming carry | Sequential | 0-3 bytes | Carry buffer |
| Error reporting | Sequential (final) | Single check | OR-reduce accumulator |
