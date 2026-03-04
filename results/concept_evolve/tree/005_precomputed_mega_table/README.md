# Precomputed Mega Table (Multi-Symbol Decode)

## Context

Standard Huffman decoding uses a table indexed by the next k bits of the bitstream, returning (symbol, code_length). Multi-symbol tables extend this: for a k-bit peek, if two consecutive symbols both have short codes (len1 + len2 <= k), encode both symbols in a single table entry.

Yann Collet explored this concept in "Huffman revisited, Part 4: Multi-bytes decoding" and measured 20-40% improvements for 2-symbol decode tables.

## Cache Size Tradeoff

- k=10: 1024 entries * 4B = 4KB (very cache-friendly, but few 2-symbol hits)
- k=11: 2048 entries * 4B = 8KB (Oodle's choice, good balance)
- k=12: 4096 entries * 4B = 16KB (fits L1, more 2-symbol opportunities)
- k=13: 8192 entries * 4B = 32KB (approaches L1 size limit)
- k=15: 32768 entries * 4B = 128KB (exceeds L1, terrible cache behavior)

## Entry Format

For a 32-bit entry: `[sym2:8][sym1:8][total_len:6][count:2][extra:8]`
- count=1: only one symbol decoded (sym2 unused)
- count=2: two literals decoded
- count=0: length/distance code (requires different handling)

## Implementation Backlog

- [ ] Implement 2-symbol table builder
- [ ] Measure probability of 2-symbol decode by k-value and file type
- [ ] Benchmark table build time vs standard table build
- [ ] Profile decode loop with 2-symbol table on Silesia corpus
- [ ] Explore 3-symbol table (useful for k=15 with very short codes)
- [ ] Test interaction with multi-stream ILP (concept 001)
