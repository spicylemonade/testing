# Streaming Validation Automaton for Base64

## Context

Base64 decoders must validate that input characters belong to the valid alphabet and that padding ('=') appears only at the end with correct placement. Naive validation checks each character individually with branches, but simdjson demonstrated that UTF-8 validation can be expressed as a SIMD-parallel DFA over byte classifications.

For Base64, the validation DFA is simpler than UTF-8 (fewer states, no multi-byte sequences), but the security implications are significant: non-canonical Base64 can lead to log mismatches, DoS attacks, and signature bypasses (Chatzigiannis & Chalkias, 2022).

## Key Insight

Base64 validation can be decomposed into two orthogonal checks: (1) character validity (each byte is in the Base64 alphabet or '='), and (2) structural validity (padding placement and count). Check (1) is embarrassingly parallel and already embedded in the PSHUFB lookup. Check (2) only needs to examine the last 4 bytes of the input. By accumulating error flags via OR-reduction and deferring the check to the end, the hot loop has zero validation overhead.

## Implementation Backlog

- [ ] Implement OR-accumulating error flag in the main decode loop
- [ ] Add end-of-stream padding validation (check last 4 bytes)
- [ ] Test RFC 4648 canonical enforcement (reject non-canonical padding)
- [ ] Benchmark validation overhead vs no-validation decode
- [ ] Test adversarial inputs (all-invalid, sparse errors, boundary errors)
- [ ] Implement detailed error reporting (byte position of first error) for diagnostic mode
