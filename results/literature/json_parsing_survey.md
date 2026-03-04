# Literature Survey: High-Performance SIMD JSON Parsing

## 1. simdjson Architecture (Core Reference)

### Langdale & Lemire 2019 — "Parsing Gigabytes of JSON per Second" [langdale2019]
**Key contribution**: First standard-compliant JSON parser to process gigabytes per second on a single core using SIMD instructions. Uses a **two-pass architecture**: (1) Stage 1 — structural indexing via SIMD classification of structural characters, string detection via carry-less multiplication prefix-XOR, and UTF-8 validation via lookup tables; (2) Stage 2 — tape generation that converts structural indices into a flat tape representation. Uses 4x fewer instructions than RapidJSON.
**Relevance**: This is the baseline we aim to beat. The two-pass design is the specific architectural limitation we exploit via fusion.

### Keiser & Lemire 2024 — "On-Demand JSON: A Better Way to Parse Documents?" [keiser2024]
**Key contribution**: Designed an On-Demand parsing API that appears like a DOM but is actually a lazy iterator over the structural index tape. Values are materialized only when accessed. Used by Apache Doris, Node.js, Milvus, and Velox.
**Relevance**: Demonstrates that lazy materialization is practical and widely adopted. Our zero-copy arena DOM extends this with SIMD-accelerated skip operations and arena allocation.

## 2. SIMD String Processing & Bit-Parallel Techniques

### Cameron & Lin 2009 — "Architectural Support for SWAR Text Processing" [cameron2009]
**Key contribution**: Introduced the inductive doubling principle for SIMD text processing — building complex character classifiers from simple 2-bit parallel operations that double in width at each step.
**Relevance**: Foundational technique used in simdjson's character classification. Our fused parser builds on this principle.

### Lin et al. 2012 — "Parabix: Boosting the Efficiency of Text Processing" [lin2012]
**Key contribution**: Systematic approach to converting byte-oriented text processing into bit-parallel operations on basis bit streams. Achieved 3-7x speedups on XML parsing.
**Relevance**: Parabix's bit-parallel approach directly influenced simdjson's structural indexing. Our bitwise structural index cascade (CE concept #6) is a refined version.

### Mula & Lemire 2018 — "Faster Base64 Encoding/Decoding Using AVX2" [mula2018]
**Key contribution**: Demonstrated SIMD table lookup (VPSHUFB) techniques for encoding/decoding, achieving 10x speedup. Key insight: VPSHUFB as a 16-entry lookup table for byte-level classification.
**Relevance**: VPSHUFB lookup is the foundation of our branchless state machine (CE concept #7).

### Lemire & Kaser 2016 — "Faster 64-bit Universal Hashing Using Carry-Less Multiplications" [lemire2016]
**Key contribution**: Demonstrated VPCLMULQDQ for efficient prefix operations on bit strings.
**Relevance**: VPCLMULQDQ prefix-XOR is how simdjson tracks string state. Our fused parser inherits this technique.

## 3. Branchless Programming & Data-Parallel Automata

### Mytkowicz et al. 2014 — "Data-Parallel Finite-State Machines" [mytkowicz2014]
**Key contribution**: Showed that finite automata can be executed in parallel by enumerating all possible start states, running the DFA on each partition, and reconciling at boundaries. Achieved near-linear speedup for many real-world automata.
**Relevance**: Direct theoretical foundation for our speculative structural indexing (CE concept #1) and DFA state convergence speculation (CE concept #4). The key insight is that most DFAs converge quickly regardless of starting state.

### Ge et al. 2019 — "Speculative Distributed CSV Data Parsing" [ge2019]
**Key contribution**: Applied speculative parsing to CSV format — guess record boundaries, parse in parallel, fix up on speculation failures. Tested on 11,000+ real-world datasets. Speculation rarely fails for CSV due to syntactic properties.
**Relevance**: Directly validates our speculative approach for JSON. CSV has simpler grammar but JSON's DFA convergence properties (CE concept #4) suggest similar speculation success rates.

## 4. AVX-512 and Advanced SIMD Applications

### HoseinyFarahabady et al. 2025 — "Accelerating Key-Value Data Structures Using AVX-512" [hoseiny2025]
**Key contribution**: Lock-free AVX-512 hash map achieving 4-5x speedup over STL hash maps. Demonstrated viability of AVX-512 as primary processing paradigm rather than supplementary.
**Relevance**: Validates our approach of building the entire parser around AVX-512 intrinsics rather than using SIMD as an optimization layer.

## 5. Speculative Execution in Parsers

### Bonetta & Brantner 2017 — "FAD.js: Fast JSON Data Access Using JIT-based Speculative Optimizations" [bonetta2017]
**Key contribution**: JIT-compiled JSON parser that speculatively assumes structural patterns based on previously seen documents. Falls back to full parsing on misprediction. Achieves 8x speedup over V8's JSON parser.
**Relevance**: Validates speculative prediction for JSON at the application level. Our approach moves speculation down to the SIMD structural indexing level, which is complementary.

## 6. Zero-Copy and On-Demand Designs

### Mühlbauer et al. 2013 — "Instant Loading for Main Memory Databases" [muhlbauer2013]
**Key contribution**: Zero-copy data loading directly from raw input files into columnar database format. Parsing and loading are fused into a single pass.
**Relevance**: Our zero-copy arena DOM is the JSON analog — data stays in the input buffer and is referenced by pointers, never copied until mutation.

### Xie et al. 2019 — "FishStore: Faster Ingestion with Subset Hashing" [xie2019]
**Key contribution**: Concurrent latch-free storage for flexible-schema data with multi-chain hash indexing. Ingest data at orders of magnitude lower cost than alternatives.
**Relevance**: Demonstrates the value of making raw data immediately queryable without full parsing, similar to our on-demand approach.

## 7. GPU-Accelerated Parsing

### Gargary et al. 2025 — "cuJSON: A Highly Parallel JSON Parser for GPUs" [gargary2025]
**Key contribution**: Novel GPU JSON parser with minimal branching and maximal parallelism. Three phases: UTF-8 validation, tokenization, nesting structure recognition. Outperforms simdjson and Pison.
**Relevance**: Demonstrates that minimal-branching parser design (directly paralleling our branchless state machine, CE concept #7) is effective. GPU approach is orthogonal to our CPU SIMD approach.

### Talluri et al. 2025 — "GpJSON: High-performance JSON Data Processing on GPUs" [talluri2025]
**Key contribution**: GPU-accelerated JSON processing built on GraalVM. Parallel structural indexing on GPU.
**Relevance**: Validates parallel structural indexing concept across different hardware platforms.

### Kaczmarski et al. 2022 — "Fast JSON Parser Using Metaprogramming on GPU" [kaczmarski2022]
**Key contribution**: GPU JSON parser optimized via metaprogramming, outperforming simdjson and cuDF. Data-ready for common data frame formats.
**Relevance**: Shows the value of format-specific optimization — our approach similarly optimizes for common JSON shapes.

## 8. Query-Aware Parsing

### Li et al. 2017 — "Mison: A Fast JSON Parser for Data Analytics" [li2017]
**Key contribution**: Introduced structural indices for JSON and projection pushdown into the parser. Converts control flow to data flow, eliminating unpredictable branches. Up to 10x speedup over existing parsers.
**Relevance**: Mison pioneered the structural index concept that simdjson later adopted. Our kernel-fusion parse-query approach (CE concept #9) extends Mison's projection pushdown to arbitrary path queries.

### Jiang et al. 2020 — "Pison: Scalable Structural Index Construction" [jiang2020]
**Key contribution**: Memory-efficient structural index construction with intra-record parallelism. 9.8x speedup over existing structural index construction for bulky records.
**Relevance**: Pison's parallel structural indexing directly validates our speculative depth tracking approach (CE concept #8).

### Jiang & Zhao 2022 — "JSONSki: Streaming Semi-Structured Data with Bit-Parallel Fast-Forwarding" [jiang2022]
**Key contribution**: Bit-parallel fast-forwarding to skip irrelevant regions during streaming JSON queries. Avoids full structural index construction.
**Relevance**: JSONSki's approach is complementary — it skips during streaming, while our fused approach skips during indexing.

### Palkar et al. 2018 — "Sparser: Filter Before You Parse" [palkar2018]
**Key contribution**: Apply SIMD-based raw filters on the bytestream before parsing. RF cascades achieve up to 22x speedup over Mison.
**Relevance**: Demonstrates the massive potential of avoiding unnecessary parsing. Our fused parse-query approach achieves similar benefits but through different mechanisms.

## 9. Competing Parser Implementations

### yyjson [yyjson2024]
Fastest C JSON library (non-SIMD). Achieves ~1106 MB/s read throughput. ANSI C compliance, RFC 8259 strict.

### Glaze [glaze2025]
C++ library achieving 1396 MB/s write, 1200 MB/s read in June 2025 benchmarks. Competitive with simdjson On-Demand.

### RapidJSON [rapidjson2015]
Widely-used C++ JSON library with SAX/DOM APIs and in-situ parsing. Performance reference baseline (~400-600 MB/s).

## 10. UTF-8 Validation

### Keiser & Lemire 2020 — "Validating UTF-8 In Less Than One Instruction Per Byte" [lemire2019utf8]
**Key contribution**: SIMD UTF-8 validation using lookup tables (VPSHUFB) that checks all validation rules simultaneously in a single pass. Less than 1 instruction per byte.
**Relevance**: Directly used in simdjson. Our fused parser integrates this validation into the structural indexing pass, eliminating the need for a separate validation step.

---

## Summary Statistics
- **Total sources surveyed**: 22 papers/resources
- **BibTeX entries in sources.bib**: 22
- **Coverage**: simdjson architecture (2), SIMD string processing (4), branchless techniques (2), AVX-512 (1), speculative parsing (2), zero-copy designs (2), GPU parsing (3), query-aware parsing (4), competing parsers (3), UTF-8 validation (1)
