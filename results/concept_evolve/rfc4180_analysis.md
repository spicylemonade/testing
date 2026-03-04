# RFC 4180 CSV Grammar Analysis

## 1. Complete Grammar Rules (ABNF)

From RFC 4180 (Shafranovich, 2005), the grammar in ABNF notation:

```abnf
file        = [header CRLF] record *(CRLF record) [CRLF]
header      = name *(COMMA name)
record      = field *(COMMA field)
name        = field
field       = (escaped / non-escaped)
escaped     = DQUOTE *(TEXTDATA / COMMA / CR / LF / 2DQUOTE) DQUOTE
non-escaped = *TEXTDATA
COMMA       = %x2C           ; ,
CR          = %x0D           ; \r
CRLF        = CR LF          ; \r\n
DQUOTE      = %x22           ; "
LF          = %x0A           ; \n
TEXTDATA    = %x20-21 / %x23-2B / %x2D-7E
              ; printable ASCII excluding DQUOTE and COMMA
2DQUOTE     = DQUOTE DQUOTE  ; escaped quote ""
```

**Practical extensions** (widely accepted beyond strict RFC):
- LF-only line endings (Unix) in addition to CRLF (Windows)
- UTF-8 content beyond ASCII (TEXTDATA extended to valid UTF-8 byte sequences)
- BOM (byte order mark, `%xEF.BB.BF`) at file start
- Trailing newline after last record (optional)

## 2. Structural Character Classes

There are exactly **4 structural character classes** in CSV:

| Character | Hex   | ASCII | Role | SIMD Bitmask Name |
|-----------|-------|-------|------|--------------------|
| COMMA     | 0x2C  | `,`   | Field separator | `comma_bits` |
| DQUOTE    | 0x22  | `"`   | Quote delimiter (paired) | `quote_bits` |
| CR        | 0x0D  | `\r`  | Part of CRLF line ending | `cr_bits` |
| LF        | 0x0A  | `\n`  | Line ending (LF or part of CRLF) | `lf_bits` |

All other bytes are **content bytes** (TEXTDATA or UTF-8 continuation bytes).

### Low-Nibble Analysis for SIMD Classification

Each structural character's low nibble (`byte & 0x0F`):

| Character | Full Byte | Low Nibble | High Nibble |
|-----------|-----------|------------|-------------|
| LF        | 0x0A      | 0x0A       | 0x00        |
| CR        | 0x0D      | 0x0D       | 0x00        |
| DQUOTE    | 0x22      | 0x02       | 0x02        |
| COMMA     | 0x2C      | 0x0C       | 0x02        |

**Critical observation**: CR (0x0D) and COMMA (0x2C) share low nibble 0x0C and 0x0D respectively — they are **distinct** in the low nibble. All four structural characters have **unique low nibbles** (0x0A, 0x0D, 0x02, 0x0C), enabling single-PSHUFB classification.

However, other ASCII characters share these low nibbles:
- `*` (0x2A) shares low nibble 0x0A with LF
- `-` (0x2D) shares low nibble 0x0D with CR
- `B` (0x42), `R` (0x52), `b` (0x62), `r` (0x72) share low nibble 0x02 with DQUOTE
- `<` (0x3C), `L` (0x4C), `\` (0x5C), `l` (0x6C), `|` (0x7C) share low nibble 0x0C with COMMA

**Resolution**: After PSHUFB lookup, AND with a comparison mask (`cmpeq` against original byte) to eliminate false positives. This is the standard simdjson two-step: `classify_low_nibble(byte) AND (byte == expected_byte)`.

## 3. Full State Machine

### States

| State | ID | Description |
|-------|----|-------------|
| `FIELD_START` | 0 | Beginning of a field (after record start or comma) |
| `UNQUOTED_FIELD` | 1 | Inside an unquoted field, consuming TEXTDATA |
| `QUOTED_FIELD` | 2 | Inside a quoted field (between opening and closing DQUOTE) |
| `QUOTE_IN_QUOTED` | 3 | Seen a DQUOTE while in QUOTED_FIELD (might be escape or close) |
| `RECORD_END` | 4 | End of record (after LF or CRLF); ready for next record |
| `CR_SEEN` | 5 | Seen CR; expecting LF for CRLF or treating CR alone as line ending |

### Transition Table

```
Current State    | Input     | Next State       | Action
-----------------+-----------+------------------+----------------------------
FIELD_START      | DQUOTE    | QUOTED_FIELD     | Mark field as quoted
FIELD_START      | COMMA     | FIELD_START      | Emit empty field
FIELD_START      | CR        | CR_SEEN          | Emit empty field, pending EOL
FIELD_START      | LF        | RECORD_END       | Emit empty field, emit record
FIELD_START      | TEXTDATA  | UNQUOTED_FIELD   | Start accumulating field content
-----------------+-----------+------------------+----------------------------
UNQUOTED_FIELD   | COMMA     | FIELD_START      | Emit field
UNQUOTED_FIELD   | CR        | CR_SEEN          | Emit field, pending EOL
UNQUOTED_FIELD   | LF        | RECORD_END       | Emit field, emit record
UNQUOTED_FIELD   | TEXTDATA  | UNQUOTED_FIELD   | Continue accumulating
UNQUOTED_FIELD   | DQUOTE    | ERROR            | Quote in unquoted field (strict)
-----------------+-----------+------------------+----------------------------
QUOTED_FIELD     | DQUOTE    | QUOTE_IN_QUOTED  | Potential close-quote or escape
QUOTED_FIELD     | COMMA     | QUOTED_FIELD     | Content (not structural)
QUOTED_FIELD     | CR        | QUOTED_FIELD     | Content (embedded newline)
QUOTED_FIELD     | LF        | QUOTED_FIELD     | Content (embedded newline)
QUOTED_FIELD     | TEXTDATA  | QUOTED_FIELD     | Content
-----------------+-----------+------------------+----------------------------
QUOTE_IN_QUOTED  | DQUOTE    | QUOTED_FIELD     | Escaped quote (2DQUOTE); emit "
QUOTE_IN_QUOTED  | COMMA     | FIELD_START      | Close quote, emit field
QUOTE_IN_QUOTED  | CR        | CR_SEEN          | Close quote, emit field, pending EOL
QUOTE_IN_QUOTED  | LF        | RECORD_END       | Close quote, emit field, emit record
QUOTE_IN_QUOTED  | TEXTDATA  | ERROR            | Invalid character after close quote
-----------------+-----------+------------------+----------------------------
CR_SEEN          | LF        | RECORD_END       | Complete CRLF, emit record
CR_SEEN          | other     | depends          | Treat CR as line ending, reprocess byte
-----------------+-----------+------------------+----------------------------
RECORD_END       | DQUOTE    | QUOTED_FIELD     | Start new quoted field in new record
RECORD_END       | COMMA     | FIELD_START      | Empty first field in new record
RECORD_END       | TEXTDATA  | UNQUOTED_FIELD   | Start new unquoted field in new record
RECORD_END       | LF        | RECORD_END       | Empty record (consecutive newlines)
RECORD_END       | EOF       | DONE             | Parsing complete
```

### State Transition Count
- Total states: 6 (including CR_SEEN)
- Transitions: 25 (including error transitions)
- In the hot path (excluding error/EOF): ~20 transitions

## 4. Ambiguous Transitions Requiring Lookahead

### Ambiguity 1: DQUOTE in QUOTE_IN_QUOTED (1-character lookahead)
**The critical ambiguity.** When the parser is in `QUOTE_IN_QUOTED` and sees another DQUOTE, it means escaped quote (`""`). When it sees any other character, the previous DQUOTE was the closing quote. This is a **1-character lookahead** ambiguity.

**SIMD impact**: This is exactly what CLMUL/prefix-XOR resolves. Adjacent quote pairs (`""`) appear as two 1-bits in the quote bitmask. After CLMUL (prefix XOR), they produce a zero-length "inside" region, effectively canceling out. The CLMUL approach handles this correctly without explicit lookahead.

**Detail**: Given a sequence `"ab""cd"`, the quote bitmask is `10001001` (positions of `"`). After prefix-XOR via CLMUL:
```
Quote positions:  1 0 0 0 1 0 0 1 0 0 1
Prefix XOR:       1 1 1 1 0 0 0 1 1 1 0
                  ^inside-q^   ^inside^
```
The doubled quotes correctly cancel the inside-quote region for exactly one position.

### Ambiguity 2: CR followed by LF vs. CR alone (1-character lookahead)
When the parser sees CR, it cannot immediately determine if this is a CRLF pair or a standalone CR. It must look ahead 1 byte.

**SIMD impact**: Create a `crlf_bits` mask by detecting `(cr_bits >> 1) AND lf_bits` — positions where CR is immediately followed by LF. Non-CRLF CRs are `cr_bits AND NOT (crlf_bits << 1)`. This is purely bitwise with no branches.

### Ambiguity 3: Start of field — quoted vs. unquoted (1-character lookahead)
In `FIELD_START`, the first character determines whether the field is quoted or unquoted. This is resolved immediately by the first byte.

**SIMD impact**: After masking structural characters with the quote-parity mask, the first byte after each field-start position (after comma or newline) determines quoting. In the two-phase architecture, Phase 1 simply marks all structural positions; Phase 2 interprets them.

### Summary of Lookahead Requirements
- Maximum lookahead: **1 character** (no deeper lookahead needed)
- All ambiguities are resolvable with bitwise operations on the structural bitmasks
- **No ambiguity requires backtracking** — the grammar is LL(1)

## 5. How Embedded Newlines Break Naive Line-Splitting Parallelism

### The Core Problem

A naive parallel parser strategy:
1. Split file into N chunks at byte boundaries
2. Scan forward in each chunk to find the first newline (LF)
3. Start parsing from the byte after that newline

**This fails for CSV because newlines can appear inside quoted fields:**

```csv
name,description,value
"Alice","She said,
""hello world""",42
"Bob","Normal field",99
```

If a chunk boundary falls within the quoted field `"She said,\n""hello world"""`, the naive scanner will find the embedded `\n` and incorrectly treat it as a record boundary. The parser will then:
- Start mid-field, producing garbage
- Miscount fields (wrong number of commas per record)
- Potentially produce incorrect data silently (no error detected)

### Quantifying the Problem

The probability of hitting an embedded newline depends on:
- **p_quote**: fraction of fields that are quoted (typically 0-30%)
- **p_newline**: probability a quoted field contains an embedded newline (typically 0-5%)
- **chunk_size**: size of each parallel chunk
- **avg_row_length**: average bytes per record

For a file with 10% quoted fields containing 2% embedded newlines, with 64KB chunks and 100-byte average rows, the probability of a chunk boundary falling inside a quoted field with an embedded newline is approximately:

```
P(bad_split) ≈ p_quote × p_newline × (avg_quoted_field_length / chunk_size)
             ≈ 0.10 × 0.02 × (50 / 65536)
             ≈ 0.0000015 (very rare per chunk)
```

But across a 10GB file with ~150,000 chunks, the expected number of bad splits is:
```
E(bad_splits) ≈ 150000 × 0.0000015 ≈ 0.23
```

This means roughly 1 in 4 large-file parses will have a bad split. **This is too frequent to ignore.**

### Resolution Strategies

**Strategy A: Speculative parsing with validation (Ge et al., SIGMOD 2019)**
- Each chunk speculatively assumes it starts outside a quoted field
- After parsing, validate: if the first record's field count doesn't match the expected count, re-parse with opposite quote-state assumption
- Speculation success rate: >99.9% on real-world data (11,000 datasets tested)

**Strategy B: Pre-scan quote parity**
- Single-threaded pre-scan: compute quote count (even/odd) at each chunk boundary using SIMD popcount on the quote bitmask
- O(n/64) work for n-byte file (scanning 1 bit per 64 bytes)
- Then distribute chunks to threads with correct initial quote-state

**Strategy C: CLMUL global prefix-XOR**
- Compute the full quote-parity vector using CLMUL across the entire file in one pass
- This is a single-threaded O(n/64) operation that produces an n-bit vector
- Each chunk then knows its exact initial quote-state from this vector
- **This is our preferred approach**: it integrates naturally with the SIMD structural indexing pipeline

### Impact on Architecture

The embedded newline problem fundamentally shapes our parallel architecture:
1. **Phase 1 must be single-threaded** (or use Strategy B/C for pre-scan)
2. Phase 1 produces the global quote-parity mask, identifying true record boundaries
3. Only **Phase 2 (field extraction/materialization)** can be trivially parallelized, because it operates on the structural index where record boundaries are already resolved
4. For files small enough to fit in L3 cache (<30MB), single-threaded Phase 1 is fast enough that parallelism provides marginal benefit
5. For large files (>1GB), the pre-scan overhead of Strategy B/C is amortized over the parallel Phase 2 speedup
