# simdjson Architecture Analysis and Performance Ceilings

## 1. Two-Pass Design

### Stage 1: Structural Indexing (Branch-Free, SIMD-Heavy)
Processes 64 bytes per iteration in a nearly branch-free pipeline:
1. **UTF-8 validation** — vectorized algorithm via Keiser-Willets VPSHUFB lookup tables
2. **Odd-length backslash detection** — identifies escape characters via bit manipulation
3. **Quote-pair detection** — filters escaped quotes, then prefix-XOR via `VPCLMULQDQ` produces 64-bit in-string mask
4. **Structural/whitespace classification** — dual `VPSHUFB` lookups (low nibble + high nibble), AND'd together
5. **Pseudo-structural detection** — bitwise ops identify value-start characters
6. **Bits-to-indexes** — `tzcnt` + shift loop converts bitmask to array of 32-bit integer positions

Output: flat array of integer indexes pointing to every position Stage 2 must examine.

### Stage 2: Tape Generation (Branchy, Sequential)
Goto-based automaton with a stack that:
- Validates structural character sequence is legal JSON
- Validates and converts atoms (numbers, strings, booleans, null)
- Constructs flat tape: 64-bit records with type in top 8 bits, payload in lower 56 bits

**Key insight from Langdale**: "It is Stage 2 that needs to be made parallel and/or regular, not Stage 1!"

## 2. SIMD Character Classification via VPSHUFB

The `VPSHUFB` instruction serves as a 16-entry lookup table. simdjson uses a **two-lookup split**:
```
a = VPSHUFB(table_lo, input AND 0x0F)  // classify by low nibble
b = VPSHUFB(table_hi, input >> 4)       // classify by high nibble
result = a AND b                         // intersection = final class
```
Each table entry is a bitset of character properties. This classifies all 64 input bytes with ~6 SIMD instructions, zero branches.

## 3. Quote/Escape Tracking via VPCLMULQDQ

Parallel prefix-XOR scan: multiply quote bitmask by all-ones constant. Low 64 bits give the in-string mask.
```cpp
quote_mask = _mm_clmulepi64_si128(quote_bits, 0xFF, 0);
quote_mask ^= prev_iter_inside_quote;  // carry from previous block
```
Latency: 6 cycles on Skylake (reciprocal throughput: 1 cycle). simdjson hides latency by scheduling other work between CLMUL and first consumer.

## 4. On-Demand API vs DOM API Performance

| Task (twitter.json) | On-Demand (GiB/s) | DOM (GiB/s) | Speedup |
|---|---|---|---|
| json2msgpack (full) | 2.3-2.5 | 1.7-1.8 | 1.4x |
| partial tweets | 4.8-5.2 | 2.9-3.1 | 1.7x |
| find tweet (single) | 8.0-8.7 | 3.1-3.3 | 2.6x |
| **Geometric mean** | **3.3-3.6** | **1.9-2.1** | **~1.7x** |

On-Demand uses ~60% of instructions of DOM, ~70% faster overall.

## 5. Known Bottlenecks

1. **Floating-point parsing**: canada.json drops to ~1.1 GB/s due to decimal-to-binary conversion cost
2. **String-heavy documents**: validation and unescaping is expensive
3. **Stage 2 branch mispredictions**: goto-based automaton with type switches — primary bottleneck
4. **Memory allocation for large files**: First-time allocation costs ~1.4 GB/s overhead
5. **Bits-to-indexes**: Sequential `tzcnt` + shift loop for converting structural bitmask to positions
6. **PCLMULQDQ latency**: 6 cycles on Skylake; requires careful scheduling

## 6. Specific Throughput Numbers

### Skylake i7-6700 (3.4 GHz, GCC, DOM)
| File | Size | simdjson | RapidJSON | sajson |
|---|---|---|---|---|
| twitter.json | 632 KB | ~2.2 GB/s | ~0.7 GB/s | ~0.9 GB/s |
| github_events.json | 65 KB | ~1.9 GB/s | ~0.6 GB/s | ~0.7 GB/s |
| canada.json | 2.3 MB | ~1.1 GB/s | ~0.4 GB/s | ~0.6 GB/s |
| citm_catalog.json | 1.7 MB | ~2.7 GB/s | ~0.9 GB/s | ~1.1 GB/s |

### Sapphire Rapids / Ice Lake (AVX-512, On-Demand)
- twitter.json: ~3.5 GB/s
- Selective queries: up to 8.7 GB/s

### Key Optimization Target
Stage 2 (tape generation) consumes **40-60%** of total parsing time. Fusing Stage 1 and Stage 2 into a single pass eliminates the second data traversal and the intermediate structural index buffer, reducing memory bandwidth pressure by ~50%.
