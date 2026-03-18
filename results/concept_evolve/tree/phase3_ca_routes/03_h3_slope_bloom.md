# H3 Slope Bloom

Status: reserve

## Prerequisites

- `results/phase3_h1_program.md`
- `results/phase3_h3_hedge.md`
- `results/phase2_benchmark_signoff.md`
- `results/literature/prior_art_gap.md`

## Dependency Edges

- Shares the same width-2 corridor extractor as H1.
- Changes only the small pre-registered level-dependent label schedule.
- Remains strictly behind H1 and never blocks H1 implementation.

## Required Evidence

- exact extraction with the same corridor grammar and no repair;
- one fixed small label-budget schedule only;
- per-level reporting of exact score, realized nonzero slope count, rational-complexity summary, and periodicity of the interface-to-label map;
- wins over matched bounded-slope and direct no-CA controls on the same geometry.

## Kill Criteria

- realized slope complexity stays `O(1)`;
- label dynamics become quickly periodic without beating the controls;
- the hedge needs broader interfaces, wider rules, or post hoc repair to survive.

## Why It Could Lower Score

- Only if the tiny label schedule escapes the bounded-slope basin while keeping the extractor legal.
- Otherwise it is just a renamed bounded-slope search and must be killed.
