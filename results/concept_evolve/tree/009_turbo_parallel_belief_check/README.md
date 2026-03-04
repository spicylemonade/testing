# Turbo Parallel Belief Check for Base64 Validation

## Context

In LDPC and Turbo code decoders, belief propagation iteratively refines confidence in each decoded bit by passing messages between variable nodes and check nodes. The key insight is that most bits are decoded correctly in the first pass, and the second pass only needs to fix the few that aren't.

Applied to Base64: the vast majority of inputs are valid. A decode-first, validate-later strategy processes all input optimistically, accumulating error flags without branching. Only if any error was detected does a slower second pass locate the exact error position.

## Key Insight

This is an application of the "optimistic" principle from speculative execution and optimistic concurrency control: assume the common case (valid input), minimize overhead for it, and handle the rare case (invalid input) with a separate slow path. The accumulated error bitmask is the "speculation check" — a zero bitmask confirms the speculation was correct.

## Implementation Backlog

- [ ] Implement error flag accumulation using 64-bit bitmask (1 bit per 64-byte block)
- [ ] Add fast-path check: if bitmask == 0, return success
- [ ] Implement slow-path binary search for error position using _tzcnt_u64
- [ ] Ensure constant-time behavior of the fast path (no timing side-channel for valid inputs)
- [ ] Benchmark overhead of flag accumulation (expected: 1 OR instruction per iteration)
- [ ] Test with adversarial input patterns that maximize error-path cost
