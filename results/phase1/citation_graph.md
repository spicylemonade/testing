# Citation Graph Mining: Branchless Binary GCD

## Seeds
- Bernstein-Yang 2019 (114 citations)
- Pornin 2020 (18 citations)
- Sreedhar-Horowitz-Torng 2022 (11+4 citations)

## Citation Chain 1: Constant-Time GCD → Side-Channel Attacks → Formal Verification

```
Aldaya & Brumley 2020 "When one vulnerable primitive turns viral"
  → Bos 2014 "Constant time modular inversion"
    → Bernstein & Yang 2019 "Fast constant-time gcd"
      → Hvass, Aranha & Spitters 2023 "High-Assurance Field Inversion" (CSF 2023)
        → O'Connor & Poelstra 2025 "Formal Verification of Safegcd"
```

**Transferable insight**: Security requirements (eliminating side-channel leaks via data-dependent branches) produced the divstep algorithm — the same branchless formulation that eliminates branch mispredictions. The `divstep` inner loop maps to exactly 5 x86 operations: SAR (sign extract), CMOV pair (conditional swap), ADD, SAR (halving). Zero JCC in steady state.

**Informs**: item_012 (branchless inner loop), item_017 (divstep GCD), item_025 (correctness proof)

## Citation Chain 2: SIMD Batch Modular Arithmetic → Vectorized GCD

```
Buhrow et al. 2021 "Parallel modular multiplication using AVX-512"
  → Didier et al. 2024 "Truncated multiplication and batch SIMD AVX512"
    → Cheng et al. 2021 "Batching CSIDH using AVX-512" (TCHES 2021)
      → Aranha et al. 2023 "Faster Constant-time Kronecker Symbol" (CCS 2023)
        → Bernstein-Yang 2019 / Hamburg 2021 "Jacobi symbol using BY"
```

**Transferable insight**: Word-sliced AVX-512 layout enables 8-way parallel divstep processing. Each AVX-512 instruction processes one limb-operation for 8 independent GCD instances simultaneously. Estimated 6-8x throughput gain for batch scenarios.

**Informs**: item_013 (SIMD GCD), item_018 (combined algorithm)

## Citation Chain 3: Hardware GCD → Software Carry Optimization

```
Sreedhar et al. 2022 "Fast XGCD Hardware" (TCHES)
  → Sreedhar et al. 2024 "3.25 GHz XGCD Accelerator" (ESSERC)
    → Ou et al. 2023 "Fast XGCD in Redundant Representation" (TCAS-II)
      → Botrel & El Housni 2023 "Faster Montgomery MSM for SNARKs" (TCHES)
        → Bernstein-Yang 2019 / Pornin 2020 inner loops
```

**Transferable insight**: Hardware designs use redundant signed digit representation to eliminate carry chains (23x over software). Software equivalent: use ADCX/ADOX dual carry chains for matrix×vector step; use k-ary stepping (k=4-5) with lookup table to reduce iterations by 4-5x.

**Informs**: item_011 (256-bit baselines), item_017 (divstep), item_016 (LUT)

## Key Newly Discovered Papers

| Paper | Year | Key Insight | Added to sources.bib? |
|-------|------|-------------|----------------------|
| Aldaya & Brumley 2020 | 2020 | Side-channel attack on branchy binary GCD | No (security focus) |
| Hvass et al. 2023 | 2023 | Automated verified synthesis of branchless field inversion | Yes (future) |
| Cheng et al. 2021 | 2021 | AVX-512 IFMA batched field operations for CSIDH | Yes (future) |
| Ou et al. 2023 | 2023 | Redundant representation XGCD | No (hardware focus) |
| Botrel & El Housni 2023 | 2023 | ADCX/ADOX dual carry chains for Montgomery | Yes (future) |

## Open Intersection (High Value)

**No paper yet combines AVX-512 batch GCD with the Bernstein-Yang jumping technique.** This is the highest-value unexplored research direction for throughput optimization.
