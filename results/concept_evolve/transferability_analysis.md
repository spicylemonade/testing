# Transferability Analysis — Fast CSV Parsing via SIMD and Speculative Field Detection

**Item:** item_025 | **Date:** 2026-03-04

## 1. Most Valuable Concept-Tree Path

The path **001 → 006 → 002 → 003** (SIMD structural indexing → branchless FSM → CLMUL quote pairing → speculative prediction) proved most valuable. Concept 001 extracts bitmasks, 006 converts the FSM to branchless arithmetic, 002 resolves quote parity via PCLMUL in O(1) per 64-byte block, and 003 exploits the structural index for speculative materialization. This path eliminated 18.75× branch mispredictions, driving 3.8–10× throughput gain.

## 2. Applications to Other Formats

**TSV:** Direct transfer — replace comma (0x2C) with tab (0x09) in SIMD cmpeq. Quote-pairing and two-phase architecture unchanged.

**JSON Lines:** Structural characters expand to `{ } [ ] , : "`. PSHUFB nibble-classification handles 8 classes in the same pipeline. PCLMUL quote pairing transfers directly. This is simdjson's architecture, confirming bidirectional transfer.

**Log files (Apache/nginx):** Structural chars are space and brackets `[ ]` plus `"`. SIMD classification applies with a 4-class LUT. Row-length prediction (concept 003) is effective due to low length variance (CV < 0.10).

**FASTA/FASTQ:** Record boundaries marked by `>` or `@`/`+`, identified via the same bitmask pipeline. Sparse structural index suits density-adaptive dispatch.

## 3. ISA-Specific vs. Portable

**ISA-specific (x86-64):** AVX2 `vpcmpeqb` + `vpmovmskb` for bitmask extraction; `PCLMULQDQ` for prefix-XOR quote pairing.

**Portable:** Two-phase architecture, speculative prediction, structural index concept, and Phase 2 algorithms are ISA-independent (concepts 003, 004, 010, 012, 013, 014).

**ARM NEON:** Classification transfers via `TBL`. NEON's `PMULL` requires two operations per 128-bit register, halving quote-pairing throughput. SVE2 improves this. Estimated NEON port: 60–75% of AVX2 Phase 1 throughput.

## 4. Ranked Next Research Directions

| Priority | Impact | Effort | Direction |
|----------|--------|--------|-----------|
| 1 | High | Medium | **Parallelized Phase 2** — consumes 31.2% of parse time; partition structural index across cores |
| 2 | High | High | **ARM NEON port** — PMULL emulation of PCLMUL is the key challenge |
| 3 | Medium | Low | **Multi-template predictor** — H2 from concept 013; improve utf8_heavy byte-accuracy from 70% to >90% |
| 4 | Medium | Medium | **Draft-and-verify parsing** — from probe; verify only near quotes; wins at <30% quote density |
| 5 | Low | Low | **Prefetch hints Phase 1→2** — PREFETCHNTA for complex fields; 20–40% Phase 2 gain on large files |
