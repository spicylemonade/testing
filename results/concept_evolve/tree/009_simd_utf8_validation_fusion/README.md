# SIMD UTF-8 Validation Fusion

## Topic Context

CSV files increasingly contain UTF-8 encoded text (international names, addresses, product descriptions). Validating UTF-8 correctness is important for data quality but adds a separate pass over the data. By fusing UTF-8 validation into the structural character detection pass, we get validation "for free" since both operations process the same bytes.

## Key Insight

All CSV structural characters (comma 0x2C, quote 0x22, LF 0x0A, CR 0x0D) are ASCII (< 0x80). In valid UTF-8, bytes >= 0x80 are either leading bytes or continuation bytes and can never be misinterpreted as structural characters. This means structural detection and UTF-8 validation are naturally complementary operations on the same data.

## Implementation Backlog

- [ ] Implement SIMD UTF-8 validation using high-bit detection and continuation byte checking
- [ ] Fuse into classify stage: reuse loaded SIMD registers for both delimiter and UTF-8 checks
- [ ] Report byte-precise positions of UTF-8 validation errors
- [ ] Benchmark fused vs. separate passes on ASCII and multi-byte-heavy CSV
- [ ] Test with intentionally malformed UTF-8 to verify error detection
- [ ] Optional: support UTF-8 -> UTF-16 transcoding fusion for Windows consumers
