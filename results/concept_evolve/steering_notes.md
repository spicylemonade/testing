# ConceptEvolve Steering Notes

## Three Concrete Steering Directions

### Direction 1: Fused Single-Pass SIMD Parser with Speculative Structural Indexing
**Concept Cards**: #1 (speculative_structural_indexing), #2 (fused_tokenize_validate_pass), #6 (bitwise_structural_index_cascade)
**Implementation Hypothesis to Implement**:
- Card #2: Process 64 bytes per iteration with a single zmm register load. In the same iteration: (1) compare bytes against structural chars via vpcmpeqb + vpternlog, (2) check for backslash-quote sequences, (3) validate UTF-8 via vpshufb lookup, (4) track string state via prefix-xor on quote bits (vpclmulqdq). All four operations use independent register sets.
- Card #6: Implement the complete bitwise cascade: Load(64B) -> 3 comparisons -> 2 bitwise ops -> 1 clmul -> 1 AND -> 1 popcount-prefix = ~12 instructions for 64 bytes.

**Bridge Chains Used**:
- `speculation_pipeline`: formal language theory → CPU architecture → SIMD algorithms → information theory → digital logic
- `fusion_pipeline`: GPU computing → digital logic → database systems → streaming algorithms

**Rubric Items**: item_012, item_013, item_015, item_016

### Direction 2: Zero-Copy Arena DOM with VBMI2 Compress/Expand and Gather-Scatter Token Routing
**Concept Cards**: #3 (vbmi2_compress_expand_parsing), #5 (lazy_materialization_pointer_machine), #12 (simd_gather_scatter_token_routing)
**Implementation Hypothesis to Implement**:
- Card #3: Use VPCOMPRESSB to extract structural bytes into dense buffer. Simultaneously use kmov to store corresponding positions. For string extraction, use VPCOMPRESSB with inverted mask.
- Card #12: Load 16 structural index entries into a zmm register. Use VPGATHERDQ to load first 8 bytes at each position. Classify via VPSHUFB lookup on first byte. Scatter results to columnar output using VPSCATTERDQ.

**Bridge Chains Used**:
- `laziness_pipeline`: functional programming → CPU microarchitecture → SIMD architecture → ISA design
- `branchless_pipeline`: cryptography → GPU computing → compiler optimization → ISA design

**Rubric Items**: item_014, item_020

### Direction 3: Predictive Structural Classifier via DFA State Convergence + Branchless State Machine
**Concept Cards**: #4 (dfa_state_convergence_speculation), #7 (branch_free_state_machine), #11 (runahead_prefetch_parsing)
**Implementation Hypothesis to Implement**:
- Card #4: Pre-compute the JSON DFA convergence table. For each (state, byte_sequence) pair of length 4, store whether all starting states converge. At runtime, check first 4 bytes at speculation boundaries.
- Card #7: Precompute 8 VPSHUFB tables (one per input byte equivalence class). Classify each input byte into class using cascaded comparison (3 instructions). Use class to select table register, then VPSHUFB with current state vector.

**Bridge Chains Used**:
- `parallelism_pipeline`: parallel algorithms → GPU computing → CPU architecture → formal language theory
- `branchless_pipeline`: cryptography → GPU computing → compiler optimization → ISA design

**Rubric Items**: item_013, item_017

## Concept Cards Selected for Direct Implementation
1. **Card #2** (fused_tokenize_validate_pass) - implementation_hypothesis for the core fused parser
2. **Card #3** (vbmi2_compress_expand_parsing) - implementation_hypothesis for VPCOMPRESSB token extraction
3. **Card #7** (branch_free_state_machine) - implementation_hypothesis for branchless state transitions
4. **Card #4** (dfa_state_convergence_speculation) - implementation_hypothesis for convergence table

## Bridge Chains Selected for Experimental Testing
1. **speculation_pipeline** - Test whether DFA convergence enables practical speculative parallel parsing for JSON
2. **fusion_pipeline** - Test whether GPU-style kernel fusion reduces memory bandwidth pressure in CPU SIMD parsing
3. **laziness_pipeline** - Test whether functional-programming-style lazy materialization with SIMD prefetch beats eager DOM construction
