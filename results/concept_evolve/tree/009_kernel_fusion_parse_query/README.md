# Kernel Fusion: Parse + Query

## Context

Current JSON processing follows a two-phase approach: (1) parse/index the entire document, (2) evaluate queries on the parsed representation. Even simdjson's On-Demand API fully indexes the document before any query evaluation. For large documents where queries are selective, most of the indexing work is wasted.

## Key Insight

If the query is known at parse time, the parser can skip irrelevant subtrees *during* structural indexing, not after. This is the JSON equivalent of predicate pushdown in databases: push the query filter into the scan operator. The skip is nearly free because depth tracking (needed for skipping) is already a component of structural indexing.

## Cross-Domain Bridges

- **Database predicate pushdown**: push filter predicates below joins and into the scan operator
- **GPU kernel fusion**: combine multiple GPU kernels into one to eliminate intermediate memory traffic
- **Streaming algorithms**: process data in a single pass to minimize memory requirements

## Implementation Backlog

1. [ ] Design query automaton that matches JSON path expressions
2. [ ] Integrate query automaton with structural indexer
3. [ ] Implement subtree skipping during indexing via depth tracking
4. [ ] Build JSONPath query compiler that produces the query automaton
5. [ ] Benchmark on large real-world JSON with selective queries
6. [ ] Compare bytes processed vs. full-index approach
7. [ ] Profile cache and memory bandwidth reduction
8. [ ] Test with multi-field queries and nested path expressions
9. [ ] Measure overhead of query automaton when all fields match (worst case)
