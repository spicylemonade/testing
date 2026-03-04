# Theoretical Performance Ceiling for JSON Parsing on Modern Hardware

## 1. Memory Bandwidth Ceiling

### DRAM Bandwidth
- **DDR5-4800 dual channel**: ~77 GB/s theoretical, ~60 GB/s practical (stream triad)
- **DDR5-5600 dual channel**: ~89 GB/s theoretical, ~70 GB/s practical
- **Single-core achievable**: ~20-30 GB/s (limited by memory controller and prefetch)

### Cache Bandwidth
- **L1D cache**: ~500 GB/s (64 bytes/cycle at 4 GHz, ~128 bytes/cycle load bandwidth)
- **L2 cache**: ~200 GB/s (64 bytes/cycle at 4 GHz)
- **L3 cache**: ~80-120 GB/s (varies with associativity and access pattern)

**Implication**: For files fitting in L2 cache (<1 MB), the parser can achieve up to 200 GB/s throughput if compute-bound. For large files exceeding L3 (>30 MB), DRAM bandwidth of ~25 GB/s becomes the ceiling.

## 2. SIMD Throughput Ceiling

### AVX-512 at 64 bytes/iteration
- **Clock rate**: ~3.5-4.0 GHz (sustained with AVX-512 on Sapphire Rapids)
  - Note: Ice Lake AVX-512 does NOT downlock. Zen 4 implements as 2x256-bit, no downclock.
- **Instructions per iteration**: ~12 (for structural index cascade per CE concept #6)
- **Bytes per cycle**: 64 / 12 = 5.33 bytes/instruction, but multiple instructions execute per cycle
- **With IPC ~4**: 64 bytes per 3 cycles = ~21 bytes/cycle
- **Throughput**: 21 * 4.0 GHz = **~84 GB/s** (structural indexing only, L1-resident)

### AVX2 at 32 bytes/iteration
- **Instructions per iteration**: ~12 (same count, narrower registers)
- **With IPC ~4**: 32 bytes per 3 cycles = ~10.7 bytes/cycle
- **Throughput**: 10.7 * 4.5 GHz = **~48 GB/s** (structural indexing only, L1-resident)

**Implication**: Pure structural indexing is NOT the bottleneck — it runs at 48-84 GB/s in cache. The bottleneck is Stage 2 (tape generation) and number/string parsing.

## 3. Instruction Throughput Limits (μops Analysis)

### simdjson Stage 1 per 64-byte block (approximate)
| Operation | μops | Port | Latency |
|---|---|---|---|
| vmovdqu64 (load) | 1 | p2/p3 | 5 |
| vpcmpeqb x3 (classify) | 3 | p0/p1 | 1 |
| vpternlogq (combine) | 1 | p0/p1 | 1 |
| vpshufb x2 (nibble lookup) | 2 | p5 | 1 |
| vpandq (mask) | 1 | p0/p1/p5 | 1 |
| vpclmulqdq (prefix-XOR) | 1 | p5 | 6 |
| kmovq + tzcnt loop | ~5 | mixed | varies |
| **Total** | **~14** | | |

At IPC 4 and 4.0 GHz: 14/4 = 3.5 cycles per 64 bytes = **18.3 bytes/cycle = 73 GB/s**

### simdjson Stage 2 per structural character (approximate)
- ~15-30 instructions per structural character (type switch, validation, tape write)
- At ~1 structural char per 8-10 bytes: ~2-3 instructions/byte
- At IPC 2 (branch-heavy): 4.0 GHz / 2.5 = **1.6 GB/s**

**This is why Stage 2 is the bottleneck!** Stage 1 runs at ~73 GB/s, Stage 2 at ~1.6 GB/s. The combined throughput is limited by Stage 2.

## 4. Branch Misprediction Overhead Model

### JSON's Inherent Unpredictability
JSON has ~8 distinct token types at each structural position: `{`, `}`, `[`, `]`, string, number, true/false/null. A branch predictor achieves:
- **Static prediction**: ~50% accuracy (always predict most common type)
- **2-bit saturating counter**: ~65-75% accuracy (biased toward strings/objects)
- **Neural/TAGE predictor**: ~80-85% accuracy (learns structural patterns)

### Cost Model
- Branch misprediction penalty: ~15 cycles (Intel Skylake/Ice Lake)
- Structural characters per 1000 bytes: ~50-100 (typical JSON)
- At 15% misprediction rate: 0.15 × 75 × 15 = **169 wasted cycles per 1000 bytes**
- At 4 GHz: 169 / 4000 = 0.042 μs per 1000 bytes → overhead of **~24 GB/s cap**

### Branchless Alternative
Eliminating all branches in Stage 2 (via table-driven state machine, CE concept #7) removes this ceiling entirely. Cost becomes pure instruction throughput.

## 5. Amdahl's Law Analysis

### Fraction of simdjson's Work
Based on profiling data and published analysis:

| Component | % of Total Time | Parallelizable? |
|---|---|---|
| Stage 1: Structural indexing | 25-35% | Yes (SIMD, per-block) |
| Stage 2: Tape generation | 40-50% | Partially (type switches sequential) |
| Number parsing | 10-20% | Yes (independent per number) |
| String validation/copy | 5-15% | Yes (independent per string) |
| Memory allocation | 2-5% | No |

### Maximum Speedup via Fusion
If we fuse Stage 1 and Stage 2 (eliminating the second pass):
- **Data passes**: 2 → 1 (saves ~30% of memory bandwidth)
- **Cache pollution**: eliminated (intermediates stay in registers)
- **Stage 2 overhead**: reduced by eliminating structural index buffer reads

Theoretical speedup from fusion alone: **1.3-1.5x** (reducing data movement)

### Maximum Speedup via Branchless + Fusion
If we also make Stage 2 branchless:
- Branch misprediction overhead: eliminated (saves ~169 cycles/1000 bytes)
- Combined with fusion: **1.5-2.0x** theoretical speedup

### Maximum Speedup via Speculation + Fusion + Branchless
If we additionally parallelize across chunks with speculation:
- Parallelism factor P = 4-8 (limited by core count and cache sharing)
- Speculation overhead: ~5% re-run rate
- Combined theoretical speedup: **2.0-3.0x** (for large files, limited by memory bandwidth)

## 6. Concrete Numeric Predictions

### Target Throughput (single-core, Sapphire Rapids with AVX-512)

| File | simdjson Baseline | Our Predicted | Speedup | Limiting Factor |
|---|---|---|---|---|
| twitter.json (632 KB) | 3.5 GB/s | 5.0-6.0 GB/s | 1.5-1.7x | L2 cache resident; compute-bound → fusion helps |
| citm_catalog.json (1.7 MB) | 2.7 GB/s | 4.5-5.5 GB/s | 1.7-2.0x | High structural density → branchless helps most |
| canada.json (2.3 MB) | 1.1 GB/s | 1.4-1.6 GB/s | 1.3-1.5x | Float parsing dominates; fusion has minimal impact |
| github_events.json (65 KB) | 1.9 GB/s | 2.5-3.5 GB/s | 1.3-1.8x | L1 resident; per-document overhead matters |
| Large synthetic (100 MB) | 2.0 GB/s | 3.5-5.0 GB/s | 1.8-2.5x | Memory-bandwidth limited → single-pass most valuable |

### Confidence Assessment
- **High confidence** in 1.3-1.5x speedup from fusion alone (well-understood data movement savings)
- **Medium confidence** in 1.5-2.0x from fusion + branchless (depends on actual branch misprediction rates)
- **Low confidence** in >2.0x from full speculation pipeline (speculation overhead may exceed savings for small files)

### Summary: The Path to Beating simdjson
1. **Fusion** (merging two passes into one): ~1.3-1.5x — almost guaranteed
2. **Branchless state machine**: ~1.1-1.3x additional — likely achievable
3. **VBMI2 compress/expand**: ~1.05-1.15x additional — ISA-dependent
4. **Zero-copy arena DOM**: ~1.05-1.1x additional — reduces allocation overhead
5. **Combined**: ~1.5-2.5x — our target range

The critical insight: no single optimization beats simdjson. Victory requires a **stack of orthogonal improvements**, each contributing a modest factor, that multiply together.
