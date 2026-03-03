# Cross-Domain Concept Bridges for Branchless Binary GCD

## Bridge 1: Hardware Pipeline Design → Software Instruction Scheduling

**Domains**: VLSI/ASIC design ↔ x86 microarchitectural optimization

**Connection**: Sreedhar et al. (2022) showed that Stein's subtraction-based algorithm maps better to hardware pipelines than Euclid's division-based approach, yielding 8x speedup in ASIC. The same principle applies to software: the binary GCD inner loop is essentially a "software pipeline" where each iteration produces one new value through a chain of dependent operations. The hardware concept of "register forwarding" maps to breaking the CPU dependency chain by reordering operations (TZCNT before ABS).

**Actionable insight**: Design the inner loop as if it were a single-cycle combinational logic block in hardware. Minimize the longest combinational path (= critical dependency chain in software). The Algorithmica TZCNT-before-ABS optimization is exactly this: shortening the combinational critical path.

**Informs**: item_005 (bottleneck analysis), item_012 (branchless inner loop)

## Bridge 2: Cryptographic Constant-Time Programming → Zero-Branch GCD

**Domains**: Side-channel attack mitigation ↔ Performance optimization

**Connection**: The cryptographic community (Bernstein-Yang 2019, Pornin 2020, Bos 2014) has spent years eliminating all data-dependent branches from GCD/modular-inversion algorithms, not for performance but for security. Their techniques — CMOV for conditional swap, fixed iteration counts, predicated operations — directly solve our performance problem. The divstep algorithm specifically provides a template for a GCD loop with zero data-dependent branches.

**Actionable insight**: The Bernstein-Yang divstep can be adapted for plain GCD (not modular inversion) by tracking only the GCD value, not cofactors. This reduces register pressure and instruction count per iteration. The tradeoff is 2n-1 fixed iterations vs ~0.7n variable iterations — but each fixed iteration is cheaper (no branch misprediction) and perfectly predictable.

**Informs**: item_017 (divstep GCD), item_015 (speculative approach)

## Bridge 3: SIMD Data Parallelism → Batch GCD Throughput

**Domains**: GPU/SIMD computing ↔ Integer arithmetic algorithms

**Connection**: While single-pair GCD latency is bounded by the dependency chain, throughput can be multiplied by processing independent pairs in parallel. This is analogous to how GPUs achieve high throughput on inherently serial algorithms by running thousands of instances simultaneously. AVX2 provides 4x 64-bit lanes; AVX-512 provides 8x. The main obstacle — no SIMD TZCNT — can be solved using the same techniques used in SIMD string processing: isolate the lowest set bit via v & (-v), then use LZCNT (which has a SIMD version via VPLZCNTD in AVX-512CD) or a VPSHUFB nibble lookup table.

**Actionable insight**: Implement batch GCD as an "embarrassingly parallel" SIMD kernel. Use vpblendvd (AVX2) or k-masks (AVX-512) as SIMD equivalents of scalar CMOV. For TZCNT emulation: bit_position = 63 - lzcnt(v & (-v)).

**Informs**: item_013 (SIMD GCD), item_018 (combined algorithm)
