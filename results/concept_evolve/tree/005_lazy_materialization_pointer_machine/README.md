# Lazy Materialization Pointer Machine

## Context

Traditional JSON DOM parsers allocate memory for every value, key, and structural element. simdjson's On-Demand API improved this by deferring value parsing, but still maintains a structural tape that requires a complete first pass. The pointer machine concept pushes laziness further: the parser is a pure state machine that navigates the structural tape without any heap allocation.

## Key Insight

A JSON document accessed through the structural index is equivalent to a "tape" — a flat array of structural character positions. Navigation (entering objects, iterating arrays, skipping values) can be expressed as pointer arithmetic on this tape. No tree construction is needed.

## Cross-Domain Bridges

- **Database late materialization**: only decode column values that survive filter predicates
- **Functional programming thunks**: values exist as unevaluated closures until forced
- **Virtual memory page faults**: accessing an unmapped page triggers just-in-time allocation; accessing an unmaterialized value triggers just-in-time parsing

## Implementation Backlog

1. [ ] Design the pointer machine state struct with minimal footprint
2. [ ] Implement SIMD-accelerated skip_value() over structural tape
3. [ ] Implement zero-allocation field lookup by key (hash-based or sequential)
4. [ ] Build ring-buffer structural index to bound memory usage
5. [ ] Benchmark selective access patterns against simdjson On-Demand
6. [ ] Measure memory allocation difference (target: zero heap allocation)
7. [ ] Integrate with speculative depth tracking (concept 8) for O(log n) skipping
8. [ ] Test streaming mode where structural index is produced incrementally
