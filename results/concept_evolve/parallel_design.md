# Parallel Chunk Processing Design for SIMD CSV Parser

## 1. Chunk Boundary Selection Strategy

Split the input into chunks of **64KB** (configurable), aligned to SIMD block boundaries (64 bytes).

**Strategy**: Split on 64KB boundaries. Each chunk starts at `chunk_id * chunk_size`. Speculatively assume **even quote parity** at each chunk boundary (i.e., the chunk starts outside a quoted field).

**Rationale** (citing Ge et al., SIGMOD 2019 \cite{ge2019speculative}):
- In their analysis of 11,000+ real-world CSV datasets, >99.9% of speculative chunk boundaries correctly start outside quoted fields
- This is because quoted fields with embedded newlines are rare (~2% of rows in typical data) and the probability of a chunk boundary falling inside such a field is proportional to `quoted_field_length / chunk_size`, which is typically < 0.001

**Chunk structure**:
```
Input:  [====Chunk 0====][====Chunk 1====][====Chunk 2====]...
Offset:  0              64K             128K             192K

Each chunk contains:
- start_offset: byte position in file
- end_offset: byte position of chunk end
- speculated_quote_state: 0 (even parity, outside quotes)
```

## 2. Validation/Correction Protocol When Speculation Fails

After each thread completes Phase 1 on its chunk:

1. **Local validation**: Check if the first structural boundary (comma or newline) found in the chunk produces a valid record. Specifically:
   - Count fields in the first detected record
   - Compare against the header field count (if known) or against adjacent chunks' field counts
   - If mismatch: speculation failed

2. **Correction on failure**:
   - Re-parse the chunk with opposite quote-state assumption (odd parity)
   - If the chunk boundary falls inside a quoted field, the correct parse will find no structural characters until the closing quote, then produce valid records
   - Mark the corrected parse as authoritative

3. **Boundary reconciliation**:
   - The last partial record of chunk K may continue into chunk K+1
   - Thread K+1 records the offset of its first complete record start
   - During assembly, stitch the partial record from chunk K with the prefix of chunk K+1

**Failure detection cost**: O(1) per chunk — just check first record's field count.
**Correction cost**: O(chunk_size) but triggered <0.1% of the time.

## 3. Work-Stealing Thread Pool Architecture

```
                   ┌─────────────────┐
                   │   Main Thread    │
                   │  (File mmap +   │
                   │   chunk setup)   │
                   └────────┬────────┘
                            │ submit chunks
                   ┌────────▼────────┐
                   │   Thread Pool    │
                   │  (N = CPU cores) │
                   └────────┬────────┘
          ┌─────────┬───────┼───────┬─────────┐
     ┌────▼───┐┌────▼───┐┌──▼────┐┌─▼──────┐
     │Thread 0││Thread 1││Thread 2││Thread 3│  ...
     │Chunk 0 ││Chunk 1 ││Chunk 2 ││Chunk 3 │
     │Phase 1 ││Phase 1 ││Phase 1 ││Phase 1 │
     └────┬───┘└────┬───┘└────┬───┘└────┬───┘
          │         │         │         │
     ┌────▼───┐┌────▼───┐┌────▼───┐┌────▼───┐
     │ Local  ││ Local  ││ Local  ││ Local  │
     │ Index  ││ Index  ││ Index  ││ Index  │
     └────┬───┘└────┬───┘└────┬───┘└────┬───┘
          └─────┬───┴─────┬───┴─────┬───┘
                │   Barrier + Validate  │
                └──────────┬────────────┘
                           │ merge indices
                   ┌───────▼──────────┐
                   │  Global Sorted   │
                   │  Structural Index│
                   └───────┬──────────┘
                           │ Phase 2 (parallel columns)
                   ┌───────▼──────────┐
                   │   Output Rows    │
                   └──────────────────┘
```

**Work stealing**: Use a shared atomic counter for chunk assignment. Each thread atomically increments `next_chunk` to claim work:
```c
while ((chunk_id = atomic_fetch_add(&next_chunk, 1)) < n_chunks) {
    process_chunk(chunk_id);
}
```

No explicit work-stealing queue needed — the atomic counter provides load balancing naturally (chunks are equal-sized, so thread imbalance is minimal).

## 4. Lock-Free Output Assembly Maintaining Row Order

**Strategy**: Each thread writes its local structural index to a pre-allocated region of the global index. No locks required.

```
Global field_offsets:   [=== Thread 0 ===][=== Thread 1 ===][=== Thread 2 ===]
                        ^                 ^                 ^
                   pre_allocated     pre_allocated     pre_allocated
                   (estimated size)  (estimated size)  (estimated size)
```

**Row ordering**:
1. Each thread tags its structural index entries with the chunk_id
2. Post-merge: indices are already spatially ordered because chunk_id corresponds to file position
3. Boundary stitching: merge the last partial record of chunk K with the prefix of chunk K+1
4. Use prefix-sum on per-chunk record counts to compute global row numbers

**Lock-free guarantee**: Each thread writes to its own pre-allocated buffer region. The merge step is a single-threaded scan over chunk boundaries (O(n_chunks), negligible cost).

## Correctness Tests

Implemented a 2-thread correctness test on embedded_newlines.csv:
- Split file at midpoint
- Thread 0 processes first half with even quote parity
- Thread 1 processes second half with speculative even parity
- Validate: merged result matches single-threaded parse
- Test passes for our benchmark datasets

## References

- \cite{ge2019speculative} — Ge et al., "Speculative Distributed CSV Data Parsing for Big Data Analytics", SIGMOD 2019. Establishes speculation success rate >99.9% on 11,000+ datasets.
- \cite{barenghi2015parallel} — Barenghi et al., "Parallel Parsing Made Practical", Science of Computer Programming 2015. Theory of speculative parallel parsing with operator-precedence grammars; applicable to CSV via regular grammar simplification.
