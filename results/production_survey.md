# Production Base64 Decoder Survey

**Date:** 2026-03-04  
**Item:** item_006

## 1. OpenSSL EVP_DecodeBlock

| Property | Value |
|----------|-------|
| **Source** | `crypto/evp/encode.c` |
| **Strategy** | Scalar (byte-by-byte), with AVX2 encode added Dec 2025 \cite{nuon2025openssl} |
| **Decode SIMD** | None (issue #29739 open for AVX decode optimization) |
| **Throughput** | ~0.4-0.6 GB/s (scalar, Skylake-class) |
| **Validation** | Full: rejects invalid characters, validates padding |
| **Streaming** | Yes, via BIO_f_base64() filter chain |
| **Line handling** | Handles MIME-style line breaks (76-char lines + CRLF) |

**Analysis:** OpenSSL's decoder is among the most widely deployed (every HTTPS connection potentially uses it for certificate handling). It remains fully scalar for decoding as of early 2026. Nick Nuon added AVX2 encoding in December 2025, but the decode path is still awaiting SIMD optimization. The BIO layer adds overhead for streaming but provides clean API composition. This represents the archetypal "production scalar" baseline we aim to exceed by 5x+.

## 2. glibc / musl Base64

| Property | Value |
|----------|-------|
| **Source** | Not in glibc core; typically via `libresolv` or application-level |
| **Strategy** | Scalar lookup table |
| **Decode SIMD** | None |
| **Throughput** | ~0.3-0.5 GB/s (lookup table dependent on cache behavior) |
| **Validation** | Basic: rejects characters not in decode table |
| **Streaming** | No built-in streaming API |

**Analysis:** Standard C libraries do not typically include a base64 API in their public interface. Applications using glibc typically use a simple scalar implementation (often copied from BSD or written ad-hoc). musl does not include base64 either. The de facto "glibc base64" is whatever scalar implementation the application links. Performance is typical of scalar approaches: ~0.3-0.5 GB/s, bounded by the lookup table cache behavior and branch mispredictions for validation.

## 3. Chromium Base64 (Blink/modp_b64)

| Property | Value |
|----------|-------|
| **Source** | `base/base64.cc`, uses `modp_b64` (modified) |
| **Strategy** | Scalar with 32-bit word tricks; recently integrated simdutf for some paths |
| **Decode SIMD** | Partial: simdutf integration in progress for WebSocket/fetch paths |
| **Throughput** | ~0.5-0.8 GB/s (scalar modp), ~3-6 GB/s via simdutf paths |
| **Validation** | Full: strict RFC 4648 compliance |
| **Streaming** | Limited: primarily one-shot decode |

**Analysis:** Chromium historically used `modp_b64`, a clever scalar implementation that processes 4 bytes at a time using 32-bit arithmetic and a precomputed 256-entry decode table. This achieves ~0.5-0.8 GB/s — better than naive scalar but still far from SIMD. Recent Chromium versions have begun integrating simdutf for performance-critical paths, but the transition is incremental. The `modp_b64` approach processes the 4-char groups in parallel at the word level but does not use SIMD vector instructions.

## 4. Node.js Base64 (via simdutf)

| Property | Value |
|----------|-------|
| **Source** | `src/base64.h`, delegates to simdutf \cite{simdutf_lib} |
| **Strategy** | SIMD via simdutf: AVX2, AVX-512, NEON with runtime dispatch |
| **Decode SIMD** | Full: highest available ISA selected at startup |
| **Throughput** | ~3-5 GB/s (AVX2), ~8-12 GB/s (AVX-512 VBMI), ~2-3 GB/s (NEON) |
| **Validation** | Full: strict validation with error reporting |
| **Streaming** | Via Buffer.from(chunk, 'base64') in chunks |

**Analysis:** Node.js represents the state-of-the-art for production SIMD Base64. By delegating to simdutf, it gets the best available SIMD implementation on each platform. On x86-64 with AVX-512 VBMI (Ice Lake+), decode throughput approaches memory bandwidth. On AVX2 (Haswell+), ~3-5 GB/s is typical. On ARM NEON (Graviton), ~2-3 GB/s. This is our primary benchmark comparison target. Any improvement must be measured against simdutf's numbers.

## 5. Go Standard Library encoding/base64

| Property | Value |
|----------|-------|
| **Source** | `encoding/base64/base64.go` |
| **Strategy** | Scalar: byte-by-byte with 256-byte decode table |
| **Decode SIMD** | None (Go does not expose SIMD intrinsics in standard library) |
| **Throughput** | ~0.5-0.8 GB/s (varies by Go version and target) |
| **Validation** | Full: RFC 4648 compliant, strict validation |
| **Streaming** | Yes: `base64.NewDecoder(enc, reader)` wraps `io.Reader` |

**Analysis:** Go's base64 decoder is a well-written scalar implementation with a clean streaming API. It processes 4 input bytes at a time using the decode table. Performance is typical of optimized scalar code (~0.5-0.8 GB/s). Go's lack of portable SIMD intrinsics means the standard library cannot use SIMD without assembly code, which the Go team has been reluctant to add for base64. Third-party Go packages (e.g., `base64x` from bytedance) use assembly for SIMD paths.

## 6. Additional Implementations

### Python base64 module
- **Strategy:** Pure Python (calls C for the actual decode in CPython)
- **Throughput:** ~0.1-0.2 GB/s (Python overhead dominates)
- **Note:** CPython's `binascii.a2b_base64()` is a simple C scalar loop

### Rust base64 crate (v0.22)
- **Strategy:** Scalar with SWAR (Sub-Word Parallelism) tricks
- **Throughput:** ~0.8-1.2 GB/s  
- **Note:** No SIMD; the vb64 crate \cite{young2023vb64} provides SIMD alternative

### Java java.util.Base64
- **Strategy:** Scalar with minor optimizations; JIT may auto-vectorize simple patterns
- **Throughput:** ~0.4-0.7 GB/s (depends on JIT warm-up and platform)

## Performance Gap Summary

| Implementation | Strategy | Throughput (GB/s) | vs Scalar Baseline |
|---------------|----------|------------------|--------------------|
| OpenSSL (decode) | Scalar | ~0.4-0.6 | 1.0x (baseline) |
| glibc-style | Scalar | ~0.3-0.5 | 0.8x |
| Chromium modp_b64 | Scalar+SWAR | ~0.5-0.8 | 1.3x |
| Go stdlib | Scalar | ~0.5-0.8 | 1.3x |
| Rust base64 crate | Scalar+SWAR | ~0.8-1.2 | 2.0x |
| **simdutf (AVX2)** | **SIMD** | **~3-5** | **~7x** |
| **simdutf (AVX-512 VBMI)** | **SIMD** | **~8-12** | **~18x** |
| **simdutf (NEON)** | **SIMD** | **~2-3** | **~5x** |
| Turbo-Base64 (AVX-512) | SIMD | ~10-15 (claimed) | ~25x |

**Key findings:**

1. **The scalar-to-SIMD gap is enormous:** 7x for AVX2, 18x+ for AVX-512 VBMI \cite{mula2018avx2base64, mula2020avx512base64}.

2. **Most production software still uses scalar:** OpenSSL, Go, Python, Java, Chromium (partially), and most application code use scalar decoders. Only Node.js (via simdutf) and a few specialized libraries use SIMD.

3. **The 5x target is already achieved by existing SIMD implementations** against scalar baselines. The research question is whether we can improve on the existing SIMD implementations (simdutf, fastbase64) — not just scalar ones.

4. **Real opportunity:** Against widely-deployed scalar implementations (OpenSSL, Go), 5x+ is easily achievable with AVX2 alone. Against simdutf (the best SIMD baseline), improvements of 10-30% may be possible through better pipelining, GFNI exploitation, or SVE optimization (which simdutf does not yet fully optimize for).

5. **ARM is underserved:** simdutf's NEON path achieves ~5x over scalar, but SVE support is minimal. This is the strongest opportunity for novel contribution.
