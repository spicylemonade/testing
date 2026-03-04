# Repository Analysis: SIMD-Accelerated Base64 Decoding

**Date:** 2026-03-04  
**Item:** item_001

## Existing Modules

### 1. Archivara Tooling (`.archivara/`)

| File | Purpose |
|------|---------|
| `concept_evolve.py` | Cross-domain concept-tree exploration engine. Launches OpenCode sub-agents to research topics, generate concept cards, build semantic bridges, and produce steering directions. Commands: `evolve`, `probe`, `reframe`, `walk`. Outputs to `results/concept_evolve/`. |
| `semantic_scholar.py` | Semantic Scholar API wrapper for literature graph traversal. Supports `search`, `citations`, `references`, `recommend`, `graph`, and `bibtex` commands. Uses exponential backoff for API resilience. |
| `opencode.json` | OpenCode configuration: defines agents (orchestrator, researcher, writer, reviewer, concept_worker) with per-agent tool permissions. Model: `anthropic/claude-opus-4-6`. |
| `logs/` | Runtime log directory for agent operations. |

### 2. OpenCode Agent System (`.opencode/`)

| Component | Purpose |
|-----------|---------|
| `agents/` | Agent definitions referenced by `opencode.json` |
| `tools/` | Custom tool wrappers (semantic_scholar, concept_evolve) |
| `package.json` | Node.js dependencies for OpenCode runtime |
| `node_modules/` | Installed dependencies |

### 3. Interconnections

```
opencode.json
    |
    +-- orchestrator agent (planning) -> generates research_rubric.json
    +-- researcher agent (this agent) -> executes rubric items
    +-- writer agent -> synthesizes findings
    +-- reviewer agent -> quality checks
    |
    +-- concept_evolve.py (tool) -> spawns sub-agents for concept exploration
    |       |
    |       +-- writes: results/concept_evolve/{concept_cards,semantic_bridge,...}.json
    |       +-- writes: results/concept_evolve/tree/NNN_slug/{concept.json,README.md}
    |
    +-- semantic_scholar.py (tool) -> literature graph queries
            |
            +-- writes: results/literature_graph.json, sources.bib entries
```

### 4. Output Directories (initially empty)

| Directory | Purpose |
|-----------|---------|
| `results/` | All research data outputs (JSON, CSV, markdown reports) |
| `figures/` | Publication-quality plots (PNG 300 DPI + PDF) |

## Proposed Directory Layout for Research Codebase

```
repo/
├── .archivara/                    # Existing tooling (unchanged)
├── .opencode/                     # Existing agent config (unchanged)
├── src/                           # Source code for all implementations
│   ├── scalar/                    # RFC 4648-compliant scalar baseline
│   │   └── base64_scalar.c
│   ├── avx2/                      # AVX2 optimized decoder
│   │   ├── base64_avx2.c
│   │   └── DESIGN.md
│   ├── avx512/                    # AVX-512 (VBMI + BW fallback) decoder
│   │   └── base64_avx512.c
│   ├── neon/                      # ARM NEON decoder
│   │   └── base64_neon.c
│   ├── sve/                       # ARM SVE/SVE2 decoder (VLA)
│   │   └── base64_sve.c
│   ├── streaming/                 # Stateful streaming decoder + ISA dispatcher
│   │   └── base64_stream.c
│   ├── common/                    # Shared headers, lookup tables, error codes
│   │   ├── base64.h               # Public API
│   │   ├── base64_common.h        # Internal shared definitions
│   │   └── cpu_detect.h           # CPUID/HWCAP runtime detection
│   └── concepts/                  # Concept modules from ConceptEvolve
├── benchmarks/                    # Benchmarking framework
│   ├── CMakeLists.txt
│   ├── bench_main.c               # Benchmark harness
│   ├── README.md                  # Measurement methodology + setup
│   └── payloads/                  # Pre-generated test payloads
├── tests/                         # Test suites
│   ├── test_scalar.c              # Scalar decoder tests
│   ├── test_vectors.h             # Shared test vectors (100+)
│   └── test_all.c                 # Cross-implementation correctness
├── docs/                          # Design documents
├── results/                       # Research outputs
│   ├── repo_analysis.md           # This document
│   ├── literature_review.md
│   ├── base64_algorithm_analysis.md
│   ├── production_survey.md
│   ├── baselines/                 # External baseline benchmark data
│   ├── experiments/               # Full experimental results
│   ├── profiling/                 # perf stat/record analysis
│   └── concept_evolve/            # ConceptEvolve artifacts
│       ├── tree/                  # Concept card folders
│       ├── steering_notes.md
│       └── *.json                 # Evolve/probe/reframe outputs
├── figures/                       # Publication-quality figures
│   └── generate_plots.py
├── scripts/                       # Setup and utility scripts
│   └── setup_research_tools.sh
├── sources.bib                    # BibTeX bibliography (15+ entries)
├── CMakeLists.txt                 # Top-level build system
├── research_rubric.json           # Research progress tracking
└── README.md                      # Project overview
```

## Build System Plan

- **CMake** as primary build system (supports cross-compilation, ISA flag management)
- Compile flags: `-O3 -march=native` for native benchmarks; explicit `-mavx2`, `-mavx512bw`, `-mavx512vbmi` for per-ISA builds
- ARM cross-compile with `-march=armv8.2-a+sve` for SVE targets
- Test framework: custom minimal or Unity C test framework
- Benchmark framework: custom with rdtsc/cntvct cycle counters + `clock_gettime`

## Hardware Requirements

- **x86-64:** Minimum AVX2 (Haswell+), ideally Ice Lake/Sapphire Rapids for AVX-512 VBMI
- **ARM64:** Minimum ARMv8.0 NEON, ideally ARMv8.2+ SVE (Graviton3, A64FX, or QEMU SVE emulation)

## Next Steps

1. Run ConceptEvolve `evolve` for topic exploration (mandatory before completing item_001)
2. Literature search (item_002)
3. Build sources.bib (item_003)
4. Deep RFC 4648 algorithm analysis (item_004)
