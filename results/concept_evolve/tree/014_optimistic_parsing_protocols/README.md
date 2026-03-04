# Optimistic Parsing Protocols

## Cross-Domain Connection

Optimistic concurrency control (OCC) in databases and optimistic replication in distributed systems share a core assumption with speculative CSV parsing: conflict is rare, so it is cheaper to proceed optimistically and fix errors after the fact than to prevent them up front. This concept node transfers three specific mechanisms from these domains to parallel CSV chunk parsing.

**OCC Validation Phases to Chunk-Boundary Resolution.** The Kung-Robinson OCC protocol divides a transaction into read, validate, and commit phases. In parallel CSV parsing, splitting a file into chunks creates potential "conflicts" at boundaries where a row spans two chunks. The pessimistic approach pre-scans the entire file for newlines (acquiring "locks" on row boundaries). The optimistic approach lets each worker parse its chunk independently (read phase), then validates boundary consistency with its neighbors (validate phase), and merges any split rows (commit phase). Since the probability of a boundary falling mid-row is avg_row_length/chunk_size (typically <0.01%), the optimistic path almost always succeeds without correction.

**Distributed Anti-Entropy to Async Chunk Merging.** Dynamo-style anti-entropy protocols reconcile divergent replicas asynchronously. Applied to CSV parsing, each chunk worker produces a (suffix, complete_rows, prefix) triple. A lightweight merge function concatenates adjacent suffix-prefix pairs to form complete rows. This is associative, enabling out-of-order chunk completion without a global barrier, which is critical for NUMA-aware parsing where different memory domains complete at different rates.

**Protocol Dissector Confidence Scoring to Delimiter Detection.** Network analyzers track per-flow protocol confidence, switching dissectors when confidence drops. A CSV parser can similarly track schema confidence (field count consistency) to detect embedded comments, delimiter changes, or malformed regions inline, rather than requiring a separate dialect-detection pre-pass.

## Proposed Transfers

H4 targets the primary latency bottleneck (sequential pre-scan). H5 enables scalability to many-core systems. H6 improves robustness to real-world CSV messiness. All three are falsifiable via controlled benchmarks.

## Implementation Backlog

- [ ] Implement optimistic chunk splitter (split at byte offsets without newline alignment)
- [ ] Implement boundary validation and merge protocol between adjacent chunks
- [ ] Implement CRDT-style suffix-prefix merge for out-of-order chunk completion
- [ ] Implement confidence-scored delimiter tracking with fallback
- [ ] Benchmark optimistic vs. pessimistic splitting on 1-10GB files with 2-16 threads
- [ ] Measure merge overhead as fraction of total parse time
