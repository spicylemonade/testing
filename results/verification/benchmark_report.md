# Benchmark Report

Date: 2026-03-12
Scope: review the H1 startup matrix, falsifier matrix, baseline strength, and run-governance results
Status: BLOCK on any broad performance claim

## Reviewed Scope

- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/benchmark_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/benchmark_comparison.csv`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/falsifier_summary.json`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/tables/analysis_sensitivity.csv`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item018_benchmark_note.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item019_falsifier_note.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item020_run_audit.md`
- `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item022_analysis_package.md`

## Result

- The benchmark artifact integrity passes:
  - full design coverage exists for the startup and falsifier matrices
  - no material instrumentation error requires rerun
- The benchmark claim gate blocks broad promotion:
  - primary-matrix startup success is tied at `17/24` for all three designs
  - primary-matrix back-drive separation is `0` for every design
  - the fixed baseline remains as competitive as the champion on the primary matrix

## What Actually Survives

- The surviving benchmark boundary is narrow:
  - the champion helps mainly against the nonaware baseline in adversarial collapse and mixed-polarity cases
- The surviving condition set is the two-case subset:
  - `fa_001`
  - `fa_005`

## What Is Blocked

- Any claim of broad superiority over the fixed startup path
- Any claim that the primary matrix proves source-aware startup correctness in general
- Any new broad sweep launched to rescue the blocked claim

## Next Required Action

- Use the benchmark only to support the narrowed adversarial-startup story.
- Do not run another broad sweep unless the problem formulation changes materially.
