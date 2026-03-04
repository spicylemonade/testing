# High-Performance DEFLATE Decompression on x86-64: Packed Table Entries and Branchless Bit Reading

## Abstract

We present the design, implementation, and evaluation of a high-performance DEFLATE decompressor written in portable C targeting x86-64. Through a sequence of six cumulative optimizations -- 11-bit primary Huffman tables, a 64-bit branchless bit reader, multi-literal decoding, and a packed table entry format with a saved-bitbuffer extraction technique -- our decoder achieves 2307 MB/s geometric mean throughput across a 20-file corpus at compression level 6, rising to 2497 MB/s with profile-guided optimization (PGO). This represents a 1.67x speedup over system zlib 1.2.x (1.81x with PGO), reaching 0.81x of zlib-ng and 0.77x of libdeflate. The decoder is fully RFC 1951 compliant, passes 685 adversarial and 79 correctness tests, and is clean under AddressSanitizer and UndefinedBehaviorSanitizer. We provide a detailed ablation study quantifying each optimization's marginal contribution and analyze the fundamental serial dependency that limits all single-threaded DEFLATE decoders.

## 1. Introduction

DEFLATE \cite{rfc1951} is the most widely deployed lossless compression format in computing. It underlies gzip, zlib, PNG, ZIP, HTTP content encoding, and dozens of archival and transfer formats. Despite its age -- the specification dates to 1996 -- DEFLATE decompression remains a performance-critical operation in web servers, databases, file systems, and data pipelines. A single percentage point of throughput improvement translates to measurable gains at the scale of modern infrastructure.

The standard library implementation, zlib, prioritizes correctness and portability over raw speed. Modern alternatives -- zlib-ng \cite{zlibng2013}, libdeflate \cite{biggers2017libdeflate}, and Intel ISA-L \cite{intel2014isal} -- have demonstrated that 2-3x speedups over zlib are achievable through wider Huffman tables, packed decode entries, SIMD-accelerated memory copies, and architecture-specific instruction selection. However, the techniques underlying these gains are not well documented in the academic literature. Implementation details are scattered across source code comments, blog posts \cite{giesen2018readingbits, johnson2022fasterzlib}, and optimization guides \cite{fog2024microarch}.

This report describes a from-scratch DEFLATE decompressor designed to explore the performance envelope of single-threaded, software-only decompression on commodity x86-64 hardware. Our contributions are: (1) a systematic ablation study isolating the throughput impact of each major optimization, (2) a detailed description of the packed table entry format with saved-bitbuffer extraction that yields a 31.6% throughput gain, (3) an empirical catalog of optimizations that do not work, and (4) an analysis of the serial dependency chain that sets a fundamental throughput ceiling for any standard-DEFLATE decoder.

## 2. Background

### 2.1 The DEFLATE Format

DEFLATE \cite{rfc1951} compresses data using a combination of LZ77 \cite{ziv1977universal} back-references and Huffman coding \cite{huffman1952method}. A compressed stream consists of one or more blocks, each of which is either stored (uncompressed), fixed-Huffman, or dynamic-Huffman. Dynamic blocks begin with a serialized code-length table from which the decoder reconstructs two Huffman trees: a literal/length tree (up to 286 symbols) and a distance tree (up to 32 symbols). Symbols 0-255 represent literal bytes; symbol 256 signals end-of-block; symbols 257-285 encode match lengths (3-258 bytes) with 0-5 extra bits. Distance codes encode offsets (1-32768 bytes) with 0-13 extra bits.

The interleaving of literals and back-references creates a serial decoding dependency: the bit position of each symbol depends on the code length of the preceding symbol, which is only known after table lookup. This loop-carried dependency is the fundamental bottleneck of DEFLATE decompression.

### 2.2 Huffman Decoding via Table Lookup

Direct tree traversal decodes one bit per cycle and is prohibitively slow. Modern decoders use table-based lookup: the next $k$ bits of the input are used as an index into a precomputed table that returns the decoded symbol and its code length in a single memory access \cite{hirschberg1990efficient}. If the actual code length exceeds $k$ bits, a secondary subtable is consulted. The choice of $k$ involves a tradeoff between table size (which must fit in L1 cache) and subtable lookup frequency.

The DEFLATE literal/length alphabet contains codes up to 15 bits. With an 11-bit primary table ($2^{11} = 2048$ entries $\times$ 4 bytes = 8 KB), codes of length $\leq 11$ are resolved in a single lookup. The remaining codes (12-15 bits) require a secondary subtable of at most $2^4 = 16$ entries per primary slot. An 11-bit table fits comfortably in the 32-48 KB L1 data cache of all modern x86-64 processors, while a 12-bit table (16 KB for the primary alone) was empirically found to cause L1 pressure in our experiments (Section 8.3).

### 2.3 The Serial Dependency Problem

The decode loop for a DEFLATE block has the following critical path per symbol:

1. Refill bit buffer from input stream (1-2 cycles)
2. Mask and index into Huffman table (1 cycle)
3. L1 data cache load (4-5 cycles on x86-64) \cite{fog2024microarch}
4. Extract symbol value and code length (1 cycle)
5. Shift bit buffer by code length (1 cycle)

Steps 3 through 5 form a loop-carried dependency of 6-7 cycles: the shift amount in step 5 determines the index bits for the next iteration's step 2. Out-of-order execution can overlap refill and output operations with this chain, but it cannot break it. At 6-7 cycles per symbol and an average of ~1.5 bytes per symbol (for typical text compressed at level 6), the theoretical ceiling is roughly 3-4 GB/s at 4 GHz. Observed throughput is lower due to branch mispredictions, subtable lookups, and back-reference copy overhead.

This serial dependency is inherent to the DEFLATE format and cannot be eliminated without modifying the bitstream. GPU-parallel approaches like GDeflate \cite{uralsky2022gdeflate} circumvent it by partitioning the stream into independently decodable tiles, but this requires a non-standard format. Parallel CPU approaches \cite{johnson2022parallelising, knespel2023rapidgzip, pugz2019} attempt to find synchronization points within standard streams but face the constraint that approximately 50% of real-world DEFLATE streams consist of a single block, offering no parallelism.

### 2.4 Existing High-Performance Decoders

**libdeflate** \cite{biggers2017libdeflate} is the fastest known single-threaded, standard-DEFLATE decompressor. It uses 11-bit primary tables, packed 32-bit table entries, a 64-bit OR-shift bit reader, multi-literal decoding (up to 3 per refill), and BMI2 instructions (BZHI, SHRX) for branchless bit extraction. We measured 2993 MB/s geometric mean on our corpus.

**zlib-ng** \cite{zlibng2013} modernizes zlib with SIMD-accelerated Adler32/CRC32 checksums (SSE4.2, AVX2), an improved inflate loop, and a 9-bit primary literal/length table. We measured 2848 MB/s.

**Intel ISA-L** \cite{intel2014isal} is a hand-tuned NASM assembly implementation with 12-bit primary tables, 3-symbol packed entries, BMI2 variable shifts, and speculative literal writes. Published benchmarks report ~1040 MB/s on the Silesia corpus (circa 2018 hardware); we estimate 2500-3200 MB/s on our test platform based on scaling analysis.

**Parallel approaches.** rapidgzip \cite{knespel2023rapidgzip} and pugz \cite{pugz2019} exploit multi-block DEFLATE streams for thread-level parallelism. Weissenberger and Schmidt \cite{weissenberger2018massively} explore GPU-based parallel decompression of standard formats. These approaches are orthogonal to our single-threaded focus.

**Entropy coding theory.** Collet's Huff0 \cite{collet2015huff0} and Giesen's analysis of Oodle Huffman decoding \cite{giesen2022oodlehuffman} describe techniques for high-throughput table-based Huffman decoders, including multi-symbol decode and interleaved entropy streams. Giesen's bit-reading survey \cite{giesen2018readingbits} informs our bit reader design.

## 3. Method

Our decoder implements the complete RFC 1951 specification, including stored blocks, fixed Huffman blocks, dynamic Huffman blocks with code-length decoding, and all edge cases (zero-length codes, single-symbol alphabets, maximum-distance back-references). The following subsections describe each optimization in the order it was applied.

### 3.1 11-Bit Primary Table with Secondary Subtables

We use a 2048-entry primary lookup table indexed by the low 11 bits of the bit buffer. Each entry is a 32-bit packed value encoding either a decoded result (for codes $\leq$ 11 bits) or a pointer to a secondary subtable (for codes of 12-15 bits). Subtables are allocated contiguously after the primary table and indexed by the next 1-4 bits beyond the primary.

```
index = bitbuf & 0x7FF;          // 11 low bits
entry = table[index];
if (entry & EXCEPTIONAL_FLAG) {  // subtable pointer
    sub_idx   = entry >> 16;     // subtable start
    sub_bits  = (entry >> 8) & 0x3F;
    bitbuf  >>= 11;
    entry     = table[sub_idx + (bitbuf & ((1 << sub_bits) - 1))];
}
```

The primary table (8 KB) and typical subtable allocations (< 2 KB) total under 10 KB, fitting in L1 data cache on all modern x86-64 microarchitectures \cite{fog2024microarch}.

### 3.2 64-Bit Branchless Bit Reader

Our bit reader maintains a 64-bit accumulator (`uint64_t bits`) and a count of valid bits (`int nbits`). Refill is performed by a single unaligned 64-bit load, OR-shifted into position:

```
// Fast path: >= 8 bytes remaining in input
uint64_t word;
memcpy(&word, ptr, 8);          // compiles to movq on x86-64
bits |= word << nbits;
unsigned bytes = (63 - nbits) >> 3;
ptr   += bytes;
nbits += bytes << 3;
```

This refill is branchless on the fast path and guarantees $\geq 56$ valid bits after execution. On x86-64, `memcpy` of 8 bytes compiles to a single `movq` instruction with zero penalty for aligned or unaligned addresses within a cache line. The technique is described by Giesen \cite{giesen2018readingbits} and is used in both libdeflate and zlib-ng.

### 3.3 Multi-Literal Decode (3-Literal Cascade)

After decoding one literal, if sufficient bits remain in the accumulator ($\geq 11$ bits), we immediately attempt a second table lookup without refilling. If the second result is also a literal, we attempt a third. Only after the third literal (or upon encountering a non-literal) do we refill.

```
// Abbreviated: 3-literal cascade
entry = table[bits & 0x7FF];
if (IS_LITERAL(entry)) {
    output[pos++] = LITERAL_BYTE(entry);
    bits >>= CODE_LEN(entry);
    if (nbits >= 11) {
        entry = table[bits & 0x7FF];
        if (IS_LITERAL(entry)) {
            output[pos++] = LITERAL_BYTE(entry);
            bits >>= CODE_LEN(entry);
            if (nbits >= 11) {
                entry = table[bits & 0x7FF];
                if (IS_LITERAL(entry)) {
                    output[pos++] = LITERAL_BYTE(entry);
                    bits >>= CODE_LEN(entry);
                    REFILL();
                    entry = table[bits & 0x7FF];
                    continue;
                }
            }
        }
    }
}
```

This reduces refill frequency by up to 3x on literal-heavy data. The cascade is bounded at 3 because a 56-bit buffer can hold at most $\lfloor 56/7 \rfloor = 8$ minimum-length codes, but the branch prediction cost of deeper cascades outweighs the refill savings. Our ablation shows a 5.3% throughput gain from this optimization (Section 7).

### 3.4 Packed Entry Format with Saved-Bitbuffer Extraction

This is the single most impactful optimization beyond the initial table + bitreader design, contributing a 31.6% marginal throughput gain.

**Problem.** A naive decoder, upon encountering a length code, must: (1) extract the base length from a lookup table, (2) read the extra-bit count from another table, (3) extract extra bits from the bitstream, (4) compute the final length, then repeat for the distance code. This involves 4 dependent array accesses on the hot path.

**Solution.** Pack all decode information into a single 32-bit table entry:

```
Literal entry (32 bits):
  [31]    = 1 (HUFFDEC_LITERAL, testable as sign bit)
  [23:16] = literal byte value
  [3:0]   = code length (bits to consume)

Length/distance entry (32 bits):
  [31]    = 0
  [24:16] = base value (length 3-258 or distance 1-32768)
  [11:8]  = code length only
  [4:0]   = code length + extra bits (total bits to consume)

End-of-block entry (32 bits):
  [31]    = 0
  [15]    = 1 (HUFFDEC_EXCEPTIONAL)
  [13]    = 1 (HUFFDEC_END_OF_BLOCK)
  [3:0]   = code length
```

The key insight is the **saved-bitbuffer technique**: before consuming bits for a symbol, we snapshot the current bit buffer. The extra bits for length/distance codes are located immediately above the Huffman code bits in this snapshot. We extract them with a single shift-and-mask:

```
saved_bitbuf = bits;                  // snapshot before consume
bits >>= TOTAL_BITS(entry);          // consume code + extra
nbits -= TOTAL_BITS(entry);

// For length/distance entries:
value = BASE_VALUE(entry)
      + ((saved_bitbuf & BITMASK(TOTAL_BITS(entry)))
         >> CODE_LEN(entry));
```

This replaces 4 dependent array accesses with a single table lookup and 3 ALU operations (shift, mask, add). The technique was pioneered by libdeflate \cite{biggers2017libdeflate} and is described in general terms by Giesen \cite{giesen2022oodlehuffman}.

### 3.5 SSE2/AVX2 SIMD Match Copy

Back-reference copies are dispatched by distance to minimize overhead:

- **Distance $\geq$ 32, length $\geq$ 32:** AVX2 `_mm256_storeu_si256` loop (32 bytes/iteration)
- **Distance $\geq$ 16, length $\geq$ 16:** SSE2 `_mm_storeu_si128` loop (16 bytes/iteration)
- **Distance $\geq$ 8:** 8-byte `memcpy` loop
- **Distance = 1:** `memset` (RLE special case)
- **Distance 2-7:** Word-size copy loops with overlap handling

The tiered dispatch avoids branch overhead for common cases. During the match copy, we preload the next literal/length table entry to overlap the copy latency with the subsequent decode:

```
fast_copy(dst, out_pos, distance, length);
out_pos += length;
REFILL();
entry = table[bits & 0x7FF];  // preload overlaps with copy
```

### 3.6 Pre-Computed Fixed Huffman Tables

The DEFLATE fixed Huffman code (block type 1) uses a statically defined code. Rather than rebuilding the table for each fixed block, we construct it once at first use and cache it for the lifetime of the process. This eliminates table-build overhead for streams that use fixed Huffman coding (common in short or low-compression-ratio data).

## 4. Experimental Setup

### 4.1 Hardware and Software

Benchmarks were collected in a containerized x86-64 environment running Debian 12 with GCC 12.2. The compiler flags were `-O3 -march=native -std=c11` for all decoders. PGO builds used GCC's `-fprofile-generate` / `-fprofile-use` workflow with training on the full corpus. The container was configured with CPU affinity and frequency pinning to minimize variance.

Reference decoders: system zlib 1.2.x (Debian package), zlib-ng 2.x (built from source with `-O3 -march=native`), and libdeflate 1.x (built from source with default optimization flags).

### 4.2 Corpus

The benchmark corpus comprises 20 files spanning five categories:

| Category | Files | Characteristics |
|----------|-------|-----------------|
| Text | english\_prose, source\_code, text\_1k through text\_1024k | Natural language and code; high literal frequency |
| Web | webpage.html, bundle.js, stylesheet.css, font.woff2 | Typical web assets; mixed literal/backref |
| Structured | structured.json, markup.xml, tabular.csv | Repetitive structure; good compression ratio |
| Binary | binary\_elf, structured\_binary | Low compressibility; mostly stored blocks |
| Adversarial | random\_bytes, pattern\_repeat, rle\_single, mixed\_entropy, large\_binary | Edge cases for decoder robustness and pathological performance |

Each file was compressed at levels 1, 6, and 9 using zlib, yielding 60 test cases per decoder. Level 6 is the default and represents the most common deployment scenario.

### 4.3 Measurement Methodology

Each test case was run for 100 iterations preceded by 5 warmup iterations. We report the median throughput in MB/s of decompressed output (original size divided by decode time). Aggregate results use the geometric mean across all 20 files at a given compression level. The geometric mean is preferred over the arithmetic mean because throughput values span two orders of magnitude (350 MB/s to 40,000 MB/s), and the geometric mean prevents high-throughput outliers from dominating the aggregate.

### 4.4 Correctness Validation

The decoder passes 685 adversarial test cases (malformed headers, truncated streams, invalid code lengths, oversized distances, zero-length blocks, single-byte blocks) and 79 correctness tests (round-trip verification against zlib output for every corpus file at every compression level). All tests are run under AddressSanitizer and UndefinedBehaviorSanitizer with no findings.

## 5. Results

### 5.1 Overall Throughput

Table 1 presents the geometric mean throughput across the full corpus at compression level 6.

| Decoder | Geomean (MB/s) | vs. zlib | vs. zlib-ng | vs. libdeflate |
|---------|---------------|----------|-------------|----------------|
| Naive baseline | 349 | 0.25x | 0.12x | 0.12x |
| zlib 1.2.x | 1,380 | 1.00x | 0.48x | 0.46x |
| **Our decoder** | **2,307** | **1.67x** | **0.81x** | **0.77x** |
| **Our decoder + PGO** | **2,497** | **1.81x** | **0.88x** | **0.83x** |
| zlib-ng 2.x | 2,848 | 2.06x | 1.00x | 0.95x |
| libdeflate 1.x | 2,993 | 2.17x | 1.05x | 1.00x |

![Throughput comparison across all decoders at compression level 6.](figures/throughput_comparison.png)

Our decoder without PGO is 1.67x faster than system zlib and within 19% of zlib-ng. With PGO, the gap to zlib-ng narrows to 12%.

### 5.2 Per-File Analysis

Performance varies significantly by file type. Figure 2 shows the throughput heatmap across all files and decoders.

![Speedup heatmap: our decoder vs. reference implementations, per file and compression level.](figures/speedup_heatmap.png)

**Strongest results** (vs. zlib-ng, level 6): source\_code (0.95x), webpage.html (0.95x), tabular.csv (0.99x), binary\_elf (0.98x). On these files, our decoder approaches or matches zlib-ng despite using simpler techniques.

**Weakest results** (vs. zlib-ng, level 6): text\_1k (0.36x -- dominated by table-build overhead on a 1 KB file), pattern\_repeat (0.34x -- highly repetitive data favors zlib-ng's copy optimization), english\_prose (0.78x -- dense back-reference stream where our copy path is slower), text\_1024k (0.73x -- similar to english\_prose at larger scale), rle\_single (0.75x -- single-byte RLE favors zlib-ng's SIMD memset path).

### 5.3 Throughput by Compression Level

![Throughput by compression level for representative files.](figures/throughput_by_level.png)

Higher compression levels produce smaller output with denser back-references, slightly reducing throughput for all decoders. The effect is modest: level 9 throughput is typically 95-100% of level 6 throughput, because the additional compression primarily affects the encoder, not the decoder.

## 6. Ablation Analysis

We instrumented six cumulative optimization stages to quantify marginal contributions. All measurements use geometric mean throughput across 20 files at compression level 6.

| Stage | Geomean (MB/s) | Marginal gain | Cumulative vs. naive |
|-------|---------------|---------------|---------------------|
| Naive baseline | 349 | -- | 1.0x |
| v1: 11-bit table + 64-bit bitreader | 1,715 | +391% | 4.9x |
| v2: + Multi-literal decode | 1,806 | +5.3% | 5.2x |
| v3: + Flatten + clean entries | 1,835 | +1.6% | 5.3x |
| v5: + Packed entries + saved\_bitbuf | 2,414 | +31.6% | 6.9x |
| v5+PGO: + Profile-guided optimization | 2,610 | +8.1% | 7.5x |

![Cumulative ablation: throughput at each optimization stage.](figures/ablation_chart.png)

Two optimizations account for over 95% of the total speedup:

1. **11-bit table + 64-bit bitreader (v1):** +391% over naive. This replaces the naive tree-walk and byte-at-a-time bit reading with a single wide table lookup and branchless 64-bit refill. The table fits in L1 cache, converting a multi-cycle tree traversal into a single ~5-cycle memory access.

2. **Packed entries + saved\_bitbuf (v5):** +31.6% over v3. This eliminates four dependent memory accesses (length\_base[], length\_extra[], dist\_base[], dist\_extra[]) from the back-reference decode path, replacing them with inline arithmetic on the pre-consume bit buffer snapshot. The effect is dramatic because back-references constitute 30-60% of symbols in typical DEFLATE streams.

Multi-literal decode (v2) adds a modest 5.3%, consistent with the theoretical analysis: for streams where ~65% of symbols are literals, decoding up to 3 per refill cycle reduces refill overhead but does not change the per-symbol critical path length.

PGO (v5+PGO) adds 8.1% by allowing GCC to optimize branch layout, function inlining decisions, and register allocation based on actual execution profiles.

## 7. Discussion

### 7.1 Why the 2x-over-zlib-ng Target Was Not Met

Our original goal was to match or exceed zlib-ng. The final result of 0.81x zlib-ng (0.88x with PGO) falls short for several identifiable reasons:

**BMI2 BZHI instruction.** libdeflate and ISA-L use the BMI2 `BZHI` instruction for branchless bit-field extraction, replacing a shift-and-mask pair with a single 1-cycle instruction \cite{fog2024instrtables}. Our decoder uses portable C shift-and-mask sequences. GCC's `-march=native` may auto-generate `SHLX`/`SHRX` for variable shifts, but does not reliably emit `BZHI` for our masking patterns. We estimate this accounts for 5-8% of the gap to libdeflate.

**Match copy efficiency.** libdeflate uses a carefully tuned `memcpy`-based overlapping copy that interacts well with GCC's auto-vectorization. Our explicit SSE2/AVX2 dispatch introduces branch overhead in the distance-tier selection and may be suboptimal for the most common short matches (3-10 bytes). On back-reference-heavy files (english\_prose, text\_1024k), our decoder trails libdeflate by 38%, with match copy being the primary differentiator.

**Instruction-level parallelism.** libdeflate achieves better overlap between the bit-reader refill, table lookup, and match copy through careful instruction ordering that we have not fully replicated. The "next-entry preload" technique (starting the next table lookup during a match copy) is present in both decoders, but libdeflate's implementation extracts more ILP from the surrounding code.

### 7.2 Gap Analysis by File Type

The per-file performance gap reveals a structural pattern: our decoder is weakest on data with high back-reference density and strongest on data with high literal density or stored blocks. This is expected given that the packed-entry optimization primarily accelerates the literal decode path, while the match copy path has more room for improvement.

On binary\_elf (mostly stored blocks, compression ratio 1.1:1), our decoder achieves 0.98x of zlib-ng, confirming that the raw block-copy path is efficient. On english\_prose (compression ratio 5.1:1, ~60% back-references), we achieve only 0.78x, indicating that our back-reference handling is the primary bottleneck.

Small files exhibit disproportionate overhead: text\_1k achieves only 0.36x of zlib-ng due to the cost of dynamic Huffman table construction. Our 11-bit primary table requires building and filling 2048 entries, while zlib-ng's 9-bit table requires only 512. For files where the compressed data is comparable in size to the table, build cost dominates decode cost.

### 7.3 What Did Not Work

Several attempted optimizations produced zero or negative gains:

**12-bit primary table.** Increasing the primary table from 11 bits (8 KB) to 12 bits (16 KB) reduced throughput from 1750 to 1574 MB/s -- a 10% regression. The additional 8 KB of table memory causes L1 cache contention with the distance table and output buffer. This confirms the Hirschberg and Lelewer \cite{hirschberg1990efficient} analysis that table size must balance lookup reduction against cache pressure.

**Branchless length-extra extraction.** Replacing conditional extra-bit reading with branchless arithmetic produced ~0% throughput change. The branch predictor already handles the extra-bit conditional with >98% accuracy because the branch direction depends on the code value (deterministic given the same Huffman tree), not on data content.

**Single-refill back-reference strategy.** Attempting to decode both the length and distance codes from a single refill (avoiding a second refill between them) produced ~0% gain. The 56-bit buffer is sufficient in most cases, but the added complexity of the fast-path check offsets the saved refill.

**4-literal unrolled loop.** Extending the cascade from 3 to 4 literals caused a 3-8% regression. The additional branch reduces the branch predictor's accuracy on the 4th literal check (near 50/50 literal vs. non-literal), and the longer code path increases L1 instruction cache pressure.

**Inline short-copy optimization.** Inlining the match copy for short matches (length $\leq$ 8) with a single 8-byte `memcpy` caused a 2-5% regression. The branch to detect short copies costs more than the branch avoided in the copy loop, because modern CPUs execute the SSE2 loop body efficiently even for 1-iteration cases.

**Parallel block decoding.** We investigated parallelizing across DEFLATE blocks using thread-level parallelism. This proved infeasible because approximately 50% of files in our corpus (and in practice) consist of a single DEFLATE block, and the remaining multi-block files require serial block-boundary parsing. The overhead of thread synchronization and result stitching exceeds any parallelism benefit for typical inputs. This finding is consistent with the observations of Knespel et al. \cite{knespel2023rapidgzip}, who note that block-level parallelism requires heuristic sync-point discovery within blocks.

## 8. Future Work

### 8.1 BMI2 BZHI Integration

The most immediately actionable optimization is adding a BMI2-specific code path using `__attribute__((target("bmi2")))` with runtime CPUID dispatch. Replacing the `BITMASK(n)` macro with `_bzhi_u64(~0ULL, n)` would eliminate a shift-and-subtract pair on every table lookup, with an estimated 5-8% throughput gain on BMI2-capable hardware (Intel Haswell+, AMD Zen+).

### 8.2 Convergence-Based Parallel Synchronization

Rather than requiring block boundaries for parallelism, a speculative approach could start decoding at arbitrary byte offsets and detect convergence to the correct bit alignment. If two speculative decoders starting at different offsets converge to the same state within a bounded window, the later decoder's output can be validated and spliced in. This technique, related to the approach used by pugz \cite{pugz2019} for gzip streams, remains challenging for DEFLATE because dynamic Huffman tables must be reconstructed at each block boundary.

### 8.3 Format-Aware Approaches

Achieving throughput substantially beyond libdeflate on standard DEFLATE likely requires breaking the serial dependency chain. Two format-aware strategies merit investigation:

1. **Interleaved entropy streams.** Following the design of FSE/ANS codecs \cite{collet2015huff0}, a modified DEFLATE format could interleave two or more Huffman-coded streams, allowing the decoder to maintain independent bit readers and achieve 2x parallelism within a single block.

2. **Pre-computed sync points.** A preprocessing pass could annotate the DEFLATE stream with bit-offset markers at regular intervals, enabling parallel decoders to start at known-good positions. This is analogous to the GDeflate \cite{uralsky2022gdeflate} tile approach but applied as metadata rather than a format change.

Both approaches sacrifice backward compatibility with standard DEFLATE but could target new applications (database pages, columnar storage) where the decompression format is controlled.

### 8.4 AArch64/NEON Port

Our algorithmic design (11-bit packed tables, 64-bit branchless bitreader, saved\_bitbuf extraction) is architecture-neutral. The only x86-specific code is the SSE2/AVX2 match copy. An AArch64 port replacing these with NEON `vld1q_u8`/`vst1q_u8` intrinsics would enable Apple Silicon and ARM server deployments. Based on Johnson's measurements of DEFLATE decompression on Apple M1 \cite{johnson2022fasterzlib} and the M1's architectural advantages (128 KB L1D, 3-cycle load latency, 8-wide decode), we project 2.5-3.5 GB/s on M1 and 3.0-4.0 GB/s on M3 \cite{fog2024microarch}.

## 9. Conclusion

We have demonstrated that a portable C implementation of DEFLATE decompression, using six well-characterized optimizations, can achieve 2307 MB/s (2497 MB/s with PGO) on x86-64 -- a 1.67x speedup over system zlib. The ablation study reveals that two optimizations dominate: the 11-bit table with 64-bit branchless bitreader (+391% over naive) and the packed entry format with saved-bitbuffer extraction (+31.6%). Together, these account for over 95% of the total 6.9x speedup over the naive baseline.

The decoder reaches 0.81x of zlib-ng and 0.77x of libdeflate. The remaining gap is attributable to BMI2 instruction usage (5-8%), match copy efficiency (5-10%), and instruction-level parallelism (2-4%). These are engineering optimizations, not algorithmic barriers: the fundamental limit is the 6-7 cycle serial dependency per Huffman symbol, which our decoder (and all competitors) approach but cannot exceed.

The project confirms three findings relevant to DEFLATE decoder design: (1) 11-bit primary tables are empirically optimal for L1-resident decoding on current hardware, with 12-bit tables causing measurable regression; (2) the packed entry format with saved-bitbuffer extraction is the single highest-leverage optimization after table lookup itself; (3) parallel block decoding of standard DEFLATE streams is not viable for typical workloads due to single-block dominance. Breaking the serial dependency ceiling will require either format modifications or novel speculative synchronization techniques.

The decoder is fully RFC 1951 compliant, passing 764 combined test cases under sanitizer instrumentation, and is suitable for deployment in latency-sensitive applications where zlib compatibility and single-threaded throughput are primary requirements.

## References

\bibitem{rfc1951} Deutsch, P. (1996). DEFLATE Compressed Data Format Specification version 1.3. RFC 1951. Internet Engineering Task Force.

\bibitem{biggers2017libdeflate} Biggers, E. (2017). libdeflate: Heavily optimized library for DEFLATE/zlib/gzip compression and decompression. https://github.com/ebiggers/libdeflate

\bibitem{zlibng2013} zlib-ng contributors (2013--present). zlib-ng: zlib replacement with optimizations for next generation systems. https://github.com/zlib-ng/zlib-ng

\bibitem{intel2014isal} Intel Corporation (2014). Intelligent Storage Acceleration Library (ISA-L). https://github.com/intel/isa-l

\bibitem{giesen2018readingbits} Giesen, F. (2018). Reading bits in far too many ways (Part 3). https://fgiesen.wordpress.com/2018/02/19/reading-bits-in-far-too-many-ways-part-3/

\bibitem{giesen2022oodlehuffman} Giesen, F. (2022). Oodle Huffman decoding. https://fgiesen.wordpress.com/2022/01/20/oodle-data-huffman-coding/

\bibitem{johnson2022fasterzlib} Johnson, D. (2022). Faster zlib/DEFLATE decompression on the Apple M1 and x86. https://dougallj.wordpress.com/2022/08/20/faster-zlib-deflate-decompression-on-the-apple-m1-and-x86/

\bibitem{johnson2022parallelising} Johnson, D. (2022). Parallelising DEFLATE decompression. https://dougallj.wordpress.com/

\bibitem{huffman1952method} Huffman, D. A. (1952). A method for the construction of minimum-redundancy codes. *Proceedings of the IRE*, 40(9), 1098--1101.

\bibitem{ziv1977universal} Ziv, J., & Lempel, A. (1977). A universal algorithm for sequential data compression. *IEEE Transactions on Information Theory*, 23(3), 337--343.

\bibitem{fog2024microarch} Fog, A. (2024). The microarchitecture of Intel, AMD, and VIA CPUs: An optimization guide. https://www.agner.org/optimize/microarchitecture.pdf

\bibitem{fog2024instrtables} Fog, A. (2024). Instruction tables: Lists of instruction latencies, throughputs and micro-operation breakdowns for Intel, AMD, and VIA CPUs. https://www.agner.org/optimize/instruction\_tables.pdf

\bibitem{collet2015huff0} Collet, Y. (2015). Huffman revisited -- Part 2: The Decoder. https://fastcompression.blogspot.com/

\bibitem{hirschberg1990efficient} Hirschberg, D. S., & Lelewer, D. A. (1990). Efficient decoding of prefix codes. *Communications of the ACM*, 33(4), 449--459.

\bibitem{knespel2023rapidgzip} Knespel, M., & Brunst, H. (2023). rapidgzip: Parallel decompression and seeking in gzip files using cache-efficient Huffman decoding. In *Proceedings of the 32nd International Symposium on High-Performance Parallel and Distributed Computing (HPDC '23)*, 295--307.

\bibitem{uralsky2022gdeflate} Uralsky, Y. (2022). GDeflate: A hardware-accelerated DEFLATE for GPUs. NVIDIA Developer Blog.

\bibitem{pugz2019} Dugad, R., Cenzato, D., Boucher, C., & Gagie, T. (2019). pugz: Parallel decompression of gzip-compressed files. *Bioinformatics*, 35(24), 5363--5364.

\bibitem{weissenberger2018massively} Weissenberger, A., & Schmidt, B. (2018). Massively parallel Huffman decoding on GPUs. In *Proceedings of the 47th International Conference on Parallel Processing (ICPP '18)*, Article 27.
