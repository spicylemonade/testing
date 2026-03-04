# Literature Review: SIMD-Accelerated Base64 Decoding

**Date:** 2026-03-04  
**Item:** item_002

## 1. Mula & Lemire, "Faster Base64 Encoding and Decoding Using AVX2 Instructions" (2017/2018)

**Type:** Peer-reviewed paper  
**Venue:** ACM Transactions on the Web (TWEB), Vol. 12, 2018  
**ArXiv:** 1704.00605  
**DOI:** 10.1145/3132709  
**Citation key:** `mula2018avx2base64`

**Summary:** The foundational work on SIMD-accelerated Base64 codecs. Demonstrates ~7x decode and ~10x encode speedup over scalar implementations using AVX2 (256-bit) SIMD instructions on Intel processors. The key algorithmic innovations:

1. **PSHUFB-based nibble lookup:** Decomposes the 256-entry ASCII-to-6-bit lookup table into operations on 4-bit nibbles using three `vpshufb` instructions plus comparisons. This "bitmask" approach processes 32 input bytes per iteration.
2. **Multiply-add packing:** Uses `vpmaddubsw` + `vpmaddwd` to pack four 6-bit values into three output bytes in just 2 instructions, replacing the 9-instruction shift/mask/or sequence.
3. **Integrated validation:** Invalid characters are detected as part of the lookup by checking that the result of the nibble lookup is non-zero, adding minimal overhead.

**Key results:** 7x faster decode than Chrome's scalar base64, 10x faster encode. AVX2 decode throughput: ~2.5-3.5 GB/s on Skylake-era hardware (vs ~0.4-0.5 GB/s scalar).

**Relevance:** This is the baseline SIMD approach we must match or exceed. The PSHUFB-bitmask lookup and multiply-add packing are the algorithmic foundations for all subsequent work.

---

## 2. Mula & Lemire, "Base64 Encoding and Decoding at Almost the Speed of a Memory Copy" (2019/2020)

**Type:** Peer-reviewed paper  
**Venue:** Software: Practice and Experience, Vol. 50(2), 2020  
**ArXiv:** 1910.05109  
**DOI:** 10.1002/spe.2777  
**Citation key:** `mula2020avx512base64`

**Summary:** Extends the AVX2 work to AVX-512, specifically exploiting AVX-512 VBMI instructions (`vpermb`, `vpmultishiftqb`) available on Ice Lake and later processors. Key innovations:

1. **VPERMB single-instruction lookup:** Replaces the 3-PSHUFB nibble decomposition with a single `vpermb` against a 64-byte lookup table. Since VPERMB can index into all 64 bytes of a ZMM register, the entire Base64 alphabet (64 characters) maps directly.
2. **VPMULTISHIFTQB packing:** Uses the multishift instruction to extract 6-bit fields and pack them in a single instruction, further reducing the instruction count.
3. **Near-memcpy throughput:** For payloads exceeding L1 cache (>32KB), encode/decode throughput approaches `memcpy` speed because the bottleneck shifts from computation to memory bandwidth.

**Key results:** 0.11 cycles/byte for decode on Cannon Lake, approaching the 0.06 cycles/byte of memcpy. 2-3x fewer instructions than the AVX2 version. The key finding is that AVX-512 VBMI reduces the decode pipeline from ~12 instructions to ~6 per 64-byte block.

**Relevance:** Establishes the theoretical performance ceiling for x86-64 SIMD base64. Our implementation must benchmark against these numbers directly.

---

## 3. Wojciech Mula's base64simd Repository & 0x80.pl Articles

**Type:** Open-source research code + technical blog  
**URL:** https://github.com/WojciechMula/base64simd  
**Blog:** http://0x80.pl/articles/index.html#base64-algorithm-new  
**Citation key:** `mula_base64simd`

**Summary:** Comprehensive collection of SIMD Base64 implementations covering:
- **SSE (128-bit):** Initial proof-of-concept with `pshufb`-based lookup
- **AVX2 (256-bit):** Multiple algorithm variants (lookup, packing, range-based validation)
- **AVX-512F:** 512-bit version using only Foundation instructions
- **AVX-512BW:** Byte/word granularity operations for improved throughput
- **AVX-512VBMI:** The `vpermb`-based single-instruction lookup (highest performance)
- **ARM NEON (128-bit):** Port using `vtbl`/`vtbx` for lookup, `vmull` for packing

The repository also includes the `base64-avx512` companion repo (https://github.com/WojciechMula/base64-avx512) with the code for the 2019 paper.

**Relevance:** Primary reference implementation for all ISA-specific approaches. The NEON implementation provides the starting point for our ARM work.

---

## 4. Turbo-Base64 (powturbo)

**Type:** Open-source library  
**URL:** https://github.com/powturbo/Turbo-Base64  
**License:** GPL-3.0  
**Citation key:** `powturbo_turbobase64`

**Summary:** Claims to be the "Fastest Base64 SIMD" implementation, supporting SSE, AVX2, AVX-512, NEON, and Altivec. Claims to be "faster than memcpy." Uses aggressive optimization techniques including:
- Lookup-free decode using arithmetic operations
- Platform-specific assembly optimizations
- Encode path that uses non-temporal stores for large payloads
- Multi-platform SIMD support including PowerPC Altivec

**Key claims:** Exceeds memcpy throughput for some configurations (likely due to non-temporal stores for writes while memcpy does cached stores). Provides both encoding and decoding.

**Relevance:** Important competitive baseline. However, the GPL-3.0 license limits adoption in production software. The "faster than memcpy" claim needs careful verification (may depend on non-temporal store behavior and cache configuration).

---

## 5. simdutf Library

**Type:** Production open-source library  
**URL:** https://github.com/simdutf/simdutf  
**License:** Apache-2.0 / MIT  
**Citation key:** `simdutf_lib`

**Summary:** The successor to fastbase64, maintained by Lemire and collaborators. Provides Unicode validation/transcoding AND Base64 encoding/decoding with comprehensive SIMD support. Used in production by:
- Node.js (primary base64 implementation)
- WebKit/Safari
- Ladybird browser
- Chromium
- Cloudflare Workers
- Bun runtime

Supports: SSE2, AVX2, NEON, AVX-512, RISC-V Vector Extension, LoongArch64, POWER.

**Key features:**
- Runtime ISA detection and dispatch
- Handles both standard Base64 and Base64url
- Full validation with error reporting
- Streaming-compatible API

**Relevance:** The gold standard for production deployment. This is our primary comparison target. Any new implementation must demonstrate measurable improvement over simdutf's current best to be worthwhile.

---

## 6. vb64: Rust SIMD Base64 Codecs

**Type:** Open-source Rust crate  
**URL:** https://github.com/mcy/vb64  
**Crate:** https://crates.io/crates/vb64  
**Blog post:** https://mcyoung.xyz/2023/11/27/simd-base64/  
**Author:** Miguel Young de la Sota  
**Citation key:** `young2023vb64`

**Summary:** A from-scratch SIMD Base64 implementation in Rust using `std::simd` (portable SIMD). The accompanying blog post "Designing a SIMD Algorithm from Scratch" is an excellent pedagogical resource explaining SIMD algorithm design methodology. Key insights:

- **Portable SIMD approach:** Uses Rust's `std::simd` for architecture-independent vectorization
- **Performance:** 2x-2.5x faster decode than the `base64` Rust crate on Zen 2 with AVX2
- **Design philosophy:** Thinks about SIMD as circuit design rather than loop optimization

**Relevance:** Demonstrates that the Mula/Lemire approach can be ported to portable SIMD abstractions. The blog post provides valuable insight into the thought process of SIMD algorithm design. However, performance is lower than handwritten intrinsics approaches.

---

## 7. Vogel's base64sve and base64rvv

**Type:** Research prototypes  
**URLs:**
- ARM SVE: https://github.com/vogma/base64sve
- RISC-V RVV: https://github.com/vogma/base64rvv  
**Author:** Marco Vogel  
**Citation key:** `vogel2024base64sve`, `vogel2024base64rvv`

**Summary:** Vectorized Base64 implementations for ARM SVE and RISC-V RVV (Vector Extension). The SVE implementation uses:
- SVE `svtbl` for table-based lookup
- SVE predicated loads/stores for variable-length processing
- CMake build system supporting cross-compilation

The RVV implementation targets the RISC-V vector extension with similar algorithmic approach adapted to RVV's register grouping model.

**Relevance:** The only known SVE Base64 implementation. However, it's a research prototype (1 star, minimal documentation). Our SVE implementation should build on and significantly improve upon this work, adding full validation, streaming support, and production-quality error handling.

---

## 8. aklomp/base64: Streaming SIMD Base64 in C99

**Type:** Production open-source library  
**URL:** https://github.com/aklomp/base64  
**Stars:** 931  
**License:** BSD-2-Clause  
**Citation key:** `klomp_base64`

**Summary:** A well-maintained C99 library providing streaming Base64 encode/decode with SIMD acceleration. Supports SSE4.1, SSE4.2, AVX, AVX2, AVX-512, and NEON. Notable for its streaming API design:
- `base64_stream_encode_init()` / `base64_stream_encode()` / `base64_stream_encode_final()`
- Chunk-based processing with carry state between calls
- Runtime SIMD detection

**Relevance:** The best existing model for streaming Base64 API design. Our streaming decoder (item_016) should study this API carefully. However, the library predates VBMI-era optimizations and may not include the most recent algorithmic improvements.

---

## 9. Nick Nuon's OpenSSL SIMD Base64 Contribution (2025/2026)

**Type:** Production contribution to OpenSSL  
**URLs:**
- Blog: https://nicknuon.substack.com/p/improving-openssl-making-base64-encoding
- PR: https://github.com/openssl/openssl/pull/29178
- Issue: https://github.com/openssl/openssl/issues/29739
- Commit: 3a69b1902892883d81c41747b2230c5168511026  
**Author:** Nick Nuon (advised by Daniel Lemire)  
**Citation key:** `nuon2025openssl`

**Summary:** Added AVX2 SIMD base64 encoding to OpenSSL (December 2025), with 3x-4x speedup over the scalar implementation. This is significant because OpenSSL is one of the most widely-deployed cryptographic libraries. Key details:
- AVX2 encoding path (`enc_b64_avx2.c`)
- Improved scalar path (`enc_b64_scalar.c`)
- Integration with OpenSSL's EVP/BIO layer
- Follow-up issue (#29739) for AVX-based decoding optimization

**Relevance:** Demonstrates that even in 2025-2026, major production libraries still have scalar base64 decoders. The decoding optimization is still open (issue #29739), confirming the ongoing gap between research and production. OpenSSL's complex codebase constraints (reviewed by Belyavskiy and Dale) illustrate the engineering challenges of integrating SIMD into production crypto libraries.

---

## 10. RFC 4648: "The Base16, Base32, and Base64 Data Encodings" (Josefsson, 2006)

**Type:** IETF RFC (Internet Standard)  
**URL:** https://www.rfc-editor.org/rfc/rfc4648  
**Author:** Simon Josefsson  
**Date:** October 2006  
**Citation key:** `rfc4648`

**Summary:** The authoritative specification for Base64 encoding. Defines:
- Standard Base64 alphabet: A-Z (0-25), a-z (26-51), 0-9 (52-61), + (62), / (63)
- Base64url variant: replaces + with - and / with _ (URL-safe)
- Padding: = characters to align output to 4-character groups
- Line-feed handling for MIME (RFC 2045) compatibility

**Relevance:** The specification our implementation must conform to. All test vectors derive from this RFC. Critical details include the padding behavior (both `=` and `==` are valid) and the requirement to reject invalid characters.

---

## 11. Additional References

### simdjson (Langdale & Lemire, 2019)
**Citation key:** `langdale2019simdjson`  
Parsing Gigabytes of JSON per Second. VLDB Journal 28(6), 2019. Relevant for SIMD shuffle techniques (classification via PSHUFB) that transfer directly to Base64 character classification.

### gfoidl/Base64 (.NET SIMD)
**URL:** https://github.com/gfoidl/Base64  
**Citation key:** `gfoidl_base64`  
.NET implementation with SIMD support (SSE, AVX2) for both standard Base64 and Base64url. Demonstrates SIMD Base64 in managed-language ecosystems.

### Chatzigiannis & Chalkias, "Base64 Malleability in Practice" (2022)
**Citation key:** `chatzigiannis2022malleability`  
**DOI:** 10.1145/3488932.3527284  
Documents security issues with non-canonical Base64 encoding/decoding across implementations. Highlights the importance of strict validation — directly relevant to our fused validation requirement.

### Intel 64 and IA-32 Architectures Software Developer's Manual
**Citation key:** `intel_sdm`  
Primary reference for AVX2, AVX-512, and GFNI instruction timing and behavior. Volume 2 (Instruction Set Reference) for intrinsics mapping.

### ARM Architecture Reference Manual for A-profile architecture
**Citation key:** `arm_arm`  
Primary reference for NEON and SVE/SVE2 instruction details, encoding, and timing.

---

## Summary Table

| # | Source | Type | ISA | Key Contribution |
|---|--------|------|-----|-----------------|
| 1 | Mula & Lemire 2018 | Paper | AVX2 | 7x decode speedup via PSHUFB + PMADDUBSW |
| 2 | Mula & Lemire 2020 | Paper | AVX-512 VBMI | Near-memcpy via VPERMB + VPMULTISHIFTQB |
| 3 | base64simd repo | Code | All x86+NEON | Reference implementations for every ISA tier |
| 4 | Turbo-Base64 | Library | All | Claims fastest; GPL-3.0 limits adoption |
| 5 | simdutf | Library | All | Production standard; used in Node.js, Chrome |
| 6 | vb64 | Crate | Portable | Rust std::simd; pedagogical blog post |
| 7 | base64sve/rvv | Prototype | SVE, RVV | Only known SVE/RVV implementations |
| 8 | aklomp/base64 | Library | x86+NEON | Best streaming API design model |
| 9 | Nuon/OpenSSL | Contribution | AVX2 | 3-4x encode speedup in OpenSSL (2025) |
| 10 | RFC 4648 | Standard | N/A | Authoritative specification |
| 11 | simdjson et al. | Papers+libs | Various | Related SIMD techniques |
