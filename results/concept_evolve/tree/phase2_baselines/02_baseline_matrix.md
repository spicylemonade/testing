# 02 Baseline Matrix

## Prerequisites

- certificate grammar frozen
- exact score selected as the only primary metric

## Dependency Edges

- depends on: certificate grammar
- depends on: prior-art gap and Tao-2025 barrier notes
- enables: benchmark sign-off
- enables: experiment matrix

## Why This Branch Could Lower Score

- Matched direct no-CA search can reveal whether the grammar contributes more than a search prior.
- Low-height asymmetric `X` baselines can identify arithmetic levers that a CA family might be exploiting indirectly.
- Stage-order, aspect-ratio, isotropic, and randomization rows can expose a robust transfer effect if one exists.

## Why This Branch Could Fail

- A too-weak matrix can confuse best-of-many luck for a real frontier.
- If hidden-complexity accounting is missing, CA state count or extractor size can masquerade as progress.
- If ablations are combined too coarsely, a single control row can miss the real source of the gain.
