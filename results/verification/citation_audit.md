# Citation Audit

## Scope

This audit checks whether the verification writeup can support its claims with both concrete experiment IDs and named papers from `sources.bib`.

Core experiment IDs:

- `control_n5_q0:H1_defect_syndrome_ca_64m`
- `control_n7_q0:H1_defect_syndrome_ca_64m`
- `control_n7_q0:simulated_annealing`
- `order_668_64m:H1_defect_syndrome_ca_64m`
- `order_668_64m:greedy`
- `order_668_64m:simulated_annealing`
- `order_668_64m:tabu`

Core paper keys:

- `eliahou2025_64mod668`
- `tsompanas2017`
- `ghaleb2019`
- `ghaemi2022`
- `leeuwen2000`
- `suksmono2018`
- `suksmono2019`
- `bright2019`

## Supported Claims

- Claim: the active search starts from the published order-668 frontier object rather than an invented seed.
  - Experiment anchors: `order_668_64m:H1_defect_syndrome_ca_64m`, `order_668_64m:greedy`
  - Paper anchor: `eliahou2025_64mod668`
- Claim: H1 is executable on solved controls but fails the first matched frontier kill test.
  - Experiment anchors: `control_n5_q0:H1_defect_syndrome_ca_64m`, `control_n7_q0:H1_defect_syndrome_ca_64m`, `order_668_64m:H1_defect_syndrome_ca_64m`
  - Paper anchor for wording discipline: `tsompanas2017`
- Claim: broad “automata are untried here” language is unsupported.
  - Experiment anchors: `order_668_64m:H1_defect_syndrome_ca_64m`, `order_668_64m:simulated_annealing`
  - Paper anchors: `tsompanas2017`, `ghaleb2019`
- Claim: the false-positive watchlist papers are only rhetorical/noise comparators, not substantive blockers.
  - Experiment anchors: `order_668_64m:H1_defect_syndrome_ca_64m`
  - Paper anchors: `ghaemi2022`, `leeuwen2000`
- Claim: the benchmark contract is narrower than the broader Hadamard-search literature and should not be overclaimed as competitive evidence.
  - Experiment anchors: `control_n7_q0:simulated_annealing`, `order_668_64m:simulated_annealing`, `order_668_64m:tabu`
  - Paper anchors: `suksmono2018`, `suksmono2019`, `bright2019`

## Metadata Risks

- `eliahou2025_64mod668`
  - Strong anchor. Safe to cite directly for the frontier seed and the 64-modular near-solution.
- `tsompanas2017`
  - Use for the narrow CA-for-search comparison only. Do not lean on it for detailed benchmark methodology.
- `ghaleb2019`
  - Keep usage high level. The saved notes already flag a title/abstract mismatch risk.
- `ghaemi2022`
  - Safe only as a documented lexical false positive.
- `leeuwen2000`
  - Safe only as a rhetorical-drift warning.
- `suksmono2018`, `suksmono2019`, `bright2019`
  - Safe as named comparison points for annealing / exact-search literature, but not as direct empirical baselines in this repo.

## Wording Guardrails

- Allowed:
  - “H1 was tested as a seeded CA repair branch on the frontier seed from `eliahou2025_64mod668`.”
  - “The current H1 implementation failed the first matched frontier kill test.”
  - “The branch remains narrower than the generic CA-for-search framing represented by `tsompanas2017`.”
- Not allowed:
  - “Cellular automata are new for Hadamard matrices.”
  - “Automata have not been tried here.”
  - “H1 established a distinct CA repair method for order 668.”
  - “The current benchmark shows competitiveness with `suksmono2018`, `suksmono2019`, or `bright2019`.”

## Decision

The verification pack can be cited safely if it keeps every substantive claim attached to:

- one or more concrete run IDs from the matched control or frontier batches, and
- one or more named papers above with the scope restrictions noted here

The highest-risk citation key remains `ghaleb2019`; keep it as a broad watchlist comparator only.
