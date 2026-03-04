# CLMUL Quote Pairing

## Topic Context

In RFC 4180 CSV, double-quote characters delimit fields that may contain commas, newlines, or other quotes. Determining whether a given comma or newline is a real delimiter or is inside a quoted field requires tracking the open/close state of quotes -- traditionally a sequential operation with O(N) serial dependency.

The CLMUL (carry-less multiplication) instruction, originally designed for AES-GCM and CRC computation in Galois fields, can be repurposed to compute cumulative XOR (prefix parity) across a bitmask in a single instruction. Since quote regions are defined by pairs of quote characters, the parity of quotes seen so far tells us whether we are inside a quoted region (odd parity = inside, even parity = outside).

This is the most critical cross-domain transfer in the entire design: a cryptographic hardware instruction enables branchless text parsing.

## Key Insight

`CLMUL(Q, 0xFFFF...FFFF)` computes the "running XOR" of bitmask Q. Bit i of the result equals the XOR of bits 0 through i of Q. This is exactly the "am I inside quotes?" predicate. A single instruction replaces what would otherwise be a 64-iteration serial loop.

## Implementation Backlog

- [ ] Implement CLMUL-based in_string computation for x86 (PCLMULQDQ)
- [ ] Implement PMULL-based in_string computation for ARM64
- [ ] Handle carry propagation between 64-byte blocks
- [ ] Implement scalar fallback using running-XOR loop
- [ ] Test all RFC 4180 edge cases: embedded commas, embedded newlines, escaped quotes (""), empty quoted fields
- [ ] Benchmark: CLMUL vs. scalar state machine for quote tracking
- [ ] Profile on files with 0%, 25%, 50%, 100% quoted fields
- [ ] Integrate with structural indexer to produce masked delimiter bitmasks
