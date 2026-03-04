# Zero-Copy Field Extraction

## Topic Context

The most expensive operation in CSV parsing (after structural detection) is copying field data into output buffers. For string columns, this involves memcpy of every field. For a 1GB CSV with average 20-byte fields, that's ~50M memcpy operations totaling 1GB of data movement.

Zero-copy extraction eliminates this by storing (offset, length) pairs that point directly into the memory-mapped input file. Only the ~5-10% of fields that require unescaping (containing `""`) need actual copying.

## Key Insight

In real-world CSV files, the vast majority of fields are either unquoted or quoted-but-simple (no embedded quotes). Only fields with `""` escape sequences need mutation. By deferring materialization and returning references, we save 90%+ of memory copy operations.

## Implementation Backlog

- [ ] Implement mmap-based file reader with proper alignment
- [ ] Design (offset, length, needs_unescape) index tuple format
- [ ] Implement zero-copy string field as Arrow StringArray with direct buffer references
- [ ] Implement escape buffer for fields requiring `""` -> `"` conversion
- [ ] Detect needs_unescape during Phase 1 (check for `""` within quoted fields)
- [ ] Handle streaming mode (non-mmap): use double-buffered read with pinned pages
- [ ] Benchmark memory savings and throughput improvement
- [ ] Test interaction with Arrow C Data Interface for Python/R consumers
- [ ] Handle edge case: field spans buffer boundary in streaming mode
