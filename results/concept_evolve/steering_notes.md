# Steering Notes — Fast CSV Parsing via SIMD and Speculative Field Detection

## Three Concrete Steering Directions

### Direction 1: CLMUL-First SIMD Lexer (PRIORITIZED)
**Summary:** Build the SIMD CSV lexer using PCLMULQDQ (x86) / PMULL (ARM64) carry-less multiplication for quote-state parity computation as the foundational primitive. This technique, derived from simdjson, eliminates the serial byte-by-byte dependency in quote tracking by computing prefix-XOR across a 64-byte chunk in constant time.

**Rubric items informed:** item_006 (RFC 4180 state machine analysis), item_008 (scalar baseline for comparison), item_012 (SIMD classification), item_013 (quote-state automaton), item_015 (integrated pipeline), item_019 (hardware counters showing branch elimination), item_021 (compliance testing).

**Why prioritized:** This is the single technique with the highest impact-to-complexity ratio. It directly addresses the primary bottleneck (serial quote-state tracking) and enables all downstream optimizations (parallelism, speculative prediction, two-phase architecture). Without correct CLMUL-based quote masking, no other SIMD optimization can function on RFC 4180-compliant data with quoted fields. The Sep parser (.NET) and simdcsv (Rust) have proven this approach viable with measured throughputs of 10-21 GB/s.

### Direction 2: Two-Phase Indexing + Columnar Materialization
**Summary:** Separate parsing into Phase 1 (SIMD structural index producing field/row boundary offset arrays) and Phase 2 (field extraction into columnar output buffers). This decoupling enables cache-friendly access patterns and natural integration with Apache Arrow RecordBatch format.

**Rubric items informed:** item_007 (benchmark datasets), item_009 (comparison with arrow-csv/pandas), item_014 (speculative row prediction feeds Phase 2), item_015 (pipeline integration), item_018 (throughput benchmarks), item_020 (speculation analysis), item_024 (architecture in report).

**Why important:** The two-phase split is the architectural backbone that enables the 5x target over pandas. pandas.read_csv performs row-by-row parsing with per-field string allocation; the two-phase approach eliminates both bottlenecks by producing a compact structural index first, then materializing columns contiguously. This also enables the speculation optimization (Direction 3 below) by making row-shape prediction operate on the index rather than raw bytes.

### Direction 3: Speculative Parallel Chunk Processing
**Summary:** Divide the input into large chunks (64KB-1MB) assigned to parallel threads. Each thread speculatively assumes it starts outside a quoted field and scans for the first unambiguous row boundary. Quote-state validation occurs at chunk boundaries after initial parsing.

**Rubric items informed:** item_014 (speculative row prediction), item_016 (parallel design), item_017 (cross-domain analogies), item_020 (speculation accuracy), item_022 (scalability experiment).

**Why third:** Parallelism provides diminishing returns relative to the single-threaded SIMD approach on datasets that fit in L3 cache. The primary bottleneck on modern hardware is memory bandwidth, not core count. However, for files >1GB, parallel processing is essential to saturate memory bandwidth across NUMA nodes. This direction is technically most complex (speculation failure recovery, lock-free output assembly) and depends on Directions 1 and 2 being correct first.

## Priority Ranking

1. **CLMUL-First SIMD Lexer** — Foundation; blocks everything else
2. **Two-Phase Architecture** — Structural enabler for performance and Arrow integration
3. **Speculative Parallelism** — Scaling multiplier; depends on 1 and 2

## Concept Tree Walk Paths of Highest Value

The most informative walk paths from `walk_paths.json`:
- `clmul_quote_pairing -> branchless_state_machine_encoding -> finite_automaton_to_dataflow -> two_phase_parsing_architecture -> cache_friendly_columnar_materialization` — This is the critical path from core SIMD primitive through to output format.
- `entropy_guided_field_width_prediction -> speculative_row_length_prediction -> two_phase_parsing_architecture -> zero_copy_field_extraction` — This connects the novel speculation technique to practical output.
- `adaptive_chunk_sizing -> parallel_bit_stream_structural_indexing -> clmul_quote_pairing -> branchless_state_machine_encoding -> finite_automaton_to_dataflow` — This represents the parallelism path.
