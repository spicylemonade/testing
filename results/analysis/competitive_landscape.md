# Competitive Landscape: High-Performance JSON Parsers

## CPU-Based Parsers (Single-Core)

| Parser | Language | Peak Throughput (GB/s) | SIMD ISA | Approach | Year | Key Differentiator |
|---|---|---|---|---|---|---|
| **simdjson** | C++ | 3.5 (AVX-512 On-Demand) | AVX-512/AVX2/NEON/POWER | Two-stage: structural index + tape/On-Demand | 2026 (v4.3) | First GB/s-class validating parser. Gold standard. |
| **yyjson** | C (ANSI C89) | 1.8 (insitu, EPYC 7R32) | None (scalar, ILP) | Full DOM, linked-list nodes | 2025 (v0.12) | Fastest portable parser, no SIMD, pure C89 |
| **Glaze** | C++20 | 1.4 (write), 1.2 (read) | None (compile-time) | Compile-time struct reflection | 2026 (v4.2) | Fastest struct roundtrip, zero-overhead reflection |
| **sajson** | C++11 | 1.2 (EPYC 7R32) | None | Single-allocation DOM | 2019 | Entire parse tree in one allocation |
| **RapidJSON** | C++ | 0.8 (insitu) | None | Recursive descent, SAX/DOM | 2016 (v1.1) | Widely deployed reference implementation |
| **sonic (Go)** | Go | ~1.0 (AVX2 JIT) | AVX2 (JIT), NEON | JIT-compiled (de)serializer | 2026 | No codegen needed, ByteDance-scale production |
| **sonic-rs** | Rust | 1.0-1.5 (AVX2) | AVX2/SSE4.2/NEON | On-demand + SIMD fast-forward | 2026 | Rust + serde compat, JSONSki-inspired |
| **simd-json (Rust)** | Rust | 1.5-2.5 (AVX2) | AVX2/SSE4.2/NEON | simdjson port (two-stage) | 2025 | Idiomatic Rust, full serde support |

## Research / Query-Oriented Parsers

| Parser | Language | Throughput | Approach | Year | Differentiator |
|---|---|---|---|---|---|
| **Mison** | C++ | 2-4 GB/s (index only) | Structural index + projection pushdown | 2017 | Pioneered structural indexing for JSON |
| **Pison** | C++ | 1.5-2 GB/s (parallel) | Parallel structural index construction | 2020 | Multi-core intra-record parallelism |
| **JSONSki** | C++ | 2-5 GB/s (queries) | Bit-parallel fast-forwarding, streaming | 2022 | ASPLOS Best Paper; 4x faster than simdjson for selective queries |
| **Sparser** | C++ | Up to 22x Mison | SIMD raw filtering before parse | 2018 | Filter-before-parse paradigm |

## GPU-Based Parsers

| Parser | Platform | Throughput | Approach | Year | Differentiator |
|---|---|---|---|---|---|
| **cuJSON** | CUDA | Multi-GB/s | 3-phase GPU parallel, minimal branching | 2025 | First end-to-end GPU parser; outperforms cuDF |
| **GpJSON** | GraalVM/CUDA | 2.9x over CPU | GPU structural indexing + in-situ querying | 2025 | Polyglot (JS/Python), GPU structural index |

## Performance Frontier Summary

The current state-of-the-art for single-core CPU JSON parsing:
- **Full DOM parsing**: ~3.5 GB/s (simdjson AVX-512 On-Demand on Sapphire Rapids)
- **Selective queries**: ~5-8 GB/s (JSONSki, simdjson On-Demand for single-field lookups)
- **Structural indexing only**: ~4-6 GB/s (Mison/Pison approach)

**Our target**: A fused single-pass parser achieving 5-7 GB/s for full DOM parsing, representing 1.5-2x speedup over simdjson.
