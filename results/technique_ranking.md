# Technique Ranking for ≥2× Throughput Over zlib-ng

## Methodology

Techniques are ranked by **expected single-core speedup contribution over zlib-ng**,
synthesized from:
- RFC 1951 spec analysis (results/deflate_spec_analysis.md)
- Implementation survey (results/impl_survey.md)
- Literature review (sources.bib)
- ConceptEvolve exploration (results/concept_evolve/)
- Citation graph analysis (results/citation_graph_analysis.md)

All techniques must maintain **full RFC 1951 compatibility** (standard DEFLATE format,
no modifications to the compressed bitstream).

---

## Ranked Techniques

### Rank 1: Multi-Symbol Speculative Decode Tables ⭐ SELECTED FOR PHASE 3

| Property | Details |
|----------|---------|
| **Estimated speedup** | 1.5–2.0× over zlib-ng (additive with other techniques) |
| **Justification** | libdeflate demonstrates 1.5-2× over zlib-ng primarily from this technique. We extend to wider tables (4-6 symbols) for additional gains. In literal-heavy streams (~70-90% of symbols are literals), decoding 4 symbols per table lookup vs 1 provides near-linear speedup for the Huffman decode phase, which accounts for ~50% of total decompression time. |
| **Complexity** | Medium |
| **RFC 1951 compatible** | YES — purely a decode-side optimization |
| **Hardware requirements** | Baseline x86-64 (no SIMD needed; benefits from BMI2 for PDEP/PEXT) |
| **Citations** | \cite{ebiggers2016libdeflate}, \cite{hirschberg1990efficient}, \cite{keller2025tradeoff} |

**Implementation plan:** Precompute decode tables during Huffman table build (per dynamic block).
Table indexed by 11-12 input bits. Each entry encodes up to 4 decoded literal symbols plus
total consumed bits, or a single non-literal symbol with its consumed bits. Table size: ~16-32KB
(fits L1 cache). For back-references, fall back to single-symbol decode.

---

### Rank 2: Unconditional 64-bit Bit-Buffer with Branchless Refill ⭐ SELECTED FOR PHASE 3

| Property | Details |
|----------|---------|
| **Estimated speedup** | 1.15–1.3× over zlib-ng (multiplicative with Rank 1) |
| **Justification** | zlib-ng uses semi-conditional refill. Unconditional refill (always load 8 bytes from input) eliminates one branch per symbol. With ~8-12 cycles/symbol baseline, saving 1-2 cycles/symbol from branch elimination gives 10-20% improvement. libdeflate already uses this; we adopt and optimize further with unaligned 64-bit loads. |
| **Complexity** | Low |
| **RFC 1951 compatible** | YES |
| **Hardware requirements** | x86-64 (unaligned 64-bit loads are fast since Nehalem) |
| **Citations** | \cite{ebiggers2016libdeflate}, \cite{giesen2015interleaved} |

**Implementation plan:** Bit buffer as `uint64_t`. On each decode step:
```c
bitbuf |= load_le64_unaligned(in_ptr) << bits_left;
// After consuming N bits:
bitbuf >>= N; bits_left -= N;
// Periodically advance in_ptr when bits_left drops below threshold
```
The unconditional load is always safe because we ensure 8 bytes of readable padding
after the input buffer.

---

### Rank 3: SIMD-Accelerated LZ77 Back-Reference Copy ⭐ SELECTED FOR PHASE 3

| Property | Details |
|----------|---------|
| **Estimated speedup** | 1.2–1.5× over zlib-ng for back-reference-heavy workloads |
| **Justification** | Back-reference copies account for 20-40% of decompression time on binary/compressed workloads. zlib-ng uses chunked_memcpy but with branching on overlap. Branchless SIMD copy (always copy 32 bytes via AVX2, handle overlap with shuffle-based repetition for small distances) eliminates per-copy branches and maximizes memory bandwidth utilization. |
| **Complexity** | Medium |
| **RFC 1951 compatible** | YES |
| **Hardware requirements** | AVX2 (SSE2 fallback for < 32-byte copies) |
| **Citations** | \cite{sitaridi2016massively}, \cite{ebiggers2016libdeflate}, \cite{zlibng2023} |

**Implementation plan:**
- Distance ≥ 32: single `_mm256_storeu_si256` from source to dest
- Distance 1: `memset` (or SIMD broadcast + store)
- Distance 2-31: SIMD shuffle-based repetition pattern
- Always copy at least 32 bytes; trim output pointer by actual match length
- Zero branches in the copy inner loop

---

### Rank 4: SIMD Literal Run Fast Path

| Property | Details |
|----------|---------|
| **Estimated speedup** | 1.1–1.4× for literal-heavy workloads (text, HTML, JS) |
| **Justification** | When the multi-symbol decode table reports 4 consecutive literals, we can check if the next N entries are also all-literal and enter a SIMD fast path that extracts and writes 32+ literal bytes per iteration without going through the full decode-dispatch loop. |
| **Complexity** | Medium-High |
| **RFC 1951 compatible** | YES |
| **Hardware requirements** | AVX2 |
| **Citations** | \cite{ebiggers2016libdeflate}, \cite{intel2017isal} |

**Implementation plan:** After decoding 4 literals from the multi-symbol table, peek
ahead in the table to check if the next entries are also all-literal. If so, enter
an unrolled loop that decodes 4 symbols per iteration using the multi-symbol table,
writing directly to the output buffer. Exit when a non-literal entry is encountered.

---

### Rank 5: Optimized Huffman Table Build for Dynamic Blocks

| Property | Details |
|----------|---------|
| **Estimated speedup** | 1.05–1.15× (amortized; significant for many small dynamic blocks) |
| **Justification** | Dynamic Huffman blocks require rebuilding decode tables per block. Faster table construction directly reduces per-block overhead. Using canonical Huffman properties, table build can be done in O(alphabet_size) without sorting. Pre-allocating table memory avoids per-block allocation. |
| **Complexity** | Low |
| **RFC 1951 compatible** | YES |
| **Hardware requirements** | Baseline x86-64 |
| **Citations** | \cite{schwartz1964generating}, \cite{ebiggers2016libdeflate} |

---

### Rank 6: Branchless Symbol Type Dispatch

| Property | Details |
|----------|---------|
| **Estimated speedup** | 1.05–1.1× |
| **Justification** | After Huffman decode, the symbol type (literal < 256, EOB = 256, length > 256) requires a branch. Using branchless conditional moves (CMOV) to handle the literal case without branching eliminates ~5% of mispredictions. The literal case dominates (~70-90%) and is highly predictable, but the 10-20% back-reference rate still causes misprediction overhead. |
| **Complexity** | Low |
| **RFC 1951 compatible** | YES |
| **Hardware requirements** | Baseline x86-64 (CMOV) |
| **Citations** | \cite{mytkowicz2014data}, \cite{ebiggers2016libdeflate} |

---

### Rank 7: Sync-Point Based Intra-Block Parallelism

| Property | Details |
|----------|---------|
| **Estimated speedup** | 1.15–1.5× (on blocks > 4KB) |
| **Justification** | Huffman codes self-synchronize after ~20-50 bits when decoding from an arbitrary offset. By finding sync points within a block, we can split the block into 2-4 independently decodable chunks and process them in parallel using separate pipeline stages or SIMD lanes within a single core. |
| **Complexity** | High |
| **RFC 1951 compatible** | YES |
| **Hardware requirements** | AVX2/AVX-512 for effective parallelism |
| **Citations** | \cite{weissenberger2018massively}, \cite{knespel2023rapidgzip}, \cite{liao2024phd} |

**Note:** This is a theoretically powerful technique but has high implementation
complexity and the sync-point finding overhead may negate gains for blocks < 4KB.
Deferred to future work for the Phase 3 prototype.

---

### Rank 8: Transducer Composition Tables (Byte-at-a-Time Decode)

| Property | Details |
|----------|---------|
| **Estimated speedup** | 1.2–1.6× for single-symbol path |
| **Justification** | Instead of decoding bit-by-bit or with variable-bit lookups, precompute a (state × byte) → (new_state, symbols) table that processes 8 input bits per step regardless of code boundaries. This amortizes the per-symbol overhead into per-byte overhead. Table size for typical DEFLATE: ~30KB (fits L1). |
| **Complexity** | High |
| **RFC 1951 compatible** | YES |
| **Hardware requirements** | Baseline x86-64 |
| **Citations** | \cite{mytkowicz2014data}, \cite{keller2025tradeoff} |

**Note:** Requires rebuilding the transducer table per dynamic Huffman block.
Build cost may be prohibitive for small blocks. Best suited for large blocks
or static Huffman. Deferred to evaluation as a secondary technique.

---

### Rank 9: Prefetch-Driven Speculation

| Property | Details |
|----------|---------|
| **Estimated speedup** | 1.05–1.15× |
| **Justification** | Issue software prefetch instructions for likely future table lookup addresses based on the speculative next-symbol offset. If the Huffman table fits in L1, prefetch is unnecessary; but for two-level tables where secondary lookups may miss L1, prefetching the secondary table entry based on the primary lookup result can hide memory latency. |
| **Complexity** | Low |
| **RFC 1951 compatible** | YES |
| **Hardware requirements** | SSE2 (PREFETCHT0 instruction) |
| **Citations** | \cite{goel2024pointcloud}, \cite{intel2017isal} |

---

### Rank 10: Enumerated-State Parallel Prefix FSM

| Property | Details |
|----------|---------|
| **Estimated speedup** | 1.5–3.0× (theoretical; high overhead for practical DEFLATE) |
| **Justification** | Mytkowicz's algorithm can parallelize any FSM by processing all possible states simultaneously. For Huffman with max 15-bit codes, effective state count after convergence drops to ~16-32. With AVX-512, 16-32 states can be processed per lane. However, the overhead of state enumeration and composition is high, and the technique works best for long streams with stable Huffman tables. |
| **Complexity** | Very High |
| **RFC 1951 compatible** | YES |
| **Hardware requirements** | AVX-512 (preferably with VPGATHERDD) |
| **Citations** | \cite{mytkowicz2014data}, \cite{ladner1980parallel} |

**Note:** Extremely promising theoretically but practical implementation requires
AVX-512 and careful engineering. Deferred to future research direction.

---

## Selected Top 3 for Phase 3 Prototyping

| Priority | Technique | Expected Contribution |
|----------|----------|---------------------|
| **P1** | Multi-Symbol Speculative Decode Tables | 1.5–2.0× over zlib-ng |
| **P2** | Unconditional 64-bit Bit-Buffer | 1.15–1.3× multiplicative |
| **P3** | SIMD-Accelerated LZ77 Copy | 1.2–1.5× for back-ref workloads |

### Combined Expected Speedup

Conservative estimate: 1.5 × 1.15 × 1.2 = **2.07× over zlib-ng**
Optimistic estimate: 2.0 × 1.3 × 1.5 = **3.9× over zlib-ng**

The combined approach targets the geometric mean speedup of **≥2.0× over zlib-ng**
across mixed workloads. Additional gains from Rank 4 (literal run fast path) and
Rank 6 (branchless dispatch) will be implemented as secondary optimizations.

---

## Technique Interaction Matrix

| | Multi-Sym | Bit-Buffer | SIMD LZ77 | Literal Run | Table Build | Branchless |
|---|---|---|---|---|---|---|
| **Multi-Symbol** | — | Synergistic | Independent | Synergistic | Dependent | Synergistic |
| **Bit-Buffer** | Synergistic | — | Independent | Synergistic | Independent | Synergistic |
| **SIMD LZ77** | Independent | Independent | — | Independent | Independent | Independent |
| **Literal Run** | Synergistic | Synergistic | Independent | — | Dependent | Synergistic |
| **Table Build** | Dependent | Independent | Independent | Dependent | — | Independent |
| **Branchless** | Synergistic | Synergistic | Independent | Synergistic | Independent | — |

"Synergistic" = techniques amplify each other's gains
"Independent" = gains are multiplicative (no interaction)
"Dependent" = one technique requires or builds on the other

---

*Ranking compiled 2026-03-04. Speedup estimates based on published benchmarks,
microbenchmark analysis from the profiling literature, and first-principles
cycle counting for x86-64 (Zen 4 / Sapphire Rapids microarchitecture).*
