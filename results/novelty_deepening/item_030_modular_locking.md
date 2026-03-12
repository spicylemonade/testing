# Item 030: Modular-Locking Audit

## Admissibility Perturbation

The audit uses a genuine coverage-rule change: `coprime_only`, where a product `r * c` counts only when `gcd(r, c) = 1`.

## Baseline Residue Scan

- Searched all modulus families `q <= 200` on the held-out composite-only record windows and their matched controls.
- Best baseline modulus by held-out AUROC: `q = 2` with AUROC `0.526`.

## Perturbation Checkpoints

- At checkpoint `100000`, the perturbation's largest row/column occupancy gap occurs at `q = 178` with L1 gap `0.055`.
- At checkpoint `300000`, the perturbation's largest row/column occupancy gap occurs at `q = 194` with L1 gap `0.030`.
- At checkpoint `1000000`, the perturbation's largest row/column occupancy gap occurs at `q = 195` with L1 gap `0.017`.

## Comparator Ceiling

- Anchor/backbone comparator from Item 026: AUROC `0.922`.
- Hypergraph comparator currently available from Item 029: surrogate-failure rate `1.000`.

A small-`q` modular feature would need to beat the anchor comparator by `20%`, which is impossible here because the anchor baseline is already close to the AUROC ceiling. The residue features are also step-level quantities, so they are constant across the matched controls drawn from the same frontier state and cannot express the within-step geometry that the anchor score captures.

## Conclusion

The small-`q` modular-locking direction fails. The residue occupancies are cheap to measure and survive the perturbation only as coarse background state; they do not form a window-level mechanism and cannot outperform the anchor geometry already present in the matched corpus.
