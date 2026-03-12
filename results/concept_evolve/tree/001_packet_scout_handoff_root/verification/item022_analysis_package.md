# Item 022 Analysis Package

Date: 2026-03-12
Scope: explain why the H1 packet-gated family survives, why the RC-ranked champion fails as the final headline, and what the smallest defensible claim boundary is after the new evidence pack
Status: PASS with a falsification-centered claim boundary

## Generated Artifacts

- Sensitivity table:
  - `tables/analysis_sensitivity.csv`
- Pairwise factor table:
  - `tables/analysis_pairwise.csv`
- Same-family ablation table:
  - `tables/ablation_pairwise.csv`
- Ablation summary:
  - `tables/ablation_summary.json`
- Robustness summary:
  - `tables/robustness_summary.json`
- Machine-readable analysis summary:
  - `tables/analysis_summary.json`
- Figures:
  - `figures/h1_primary_matrix_heatmap.pdf`
  - `figures/h1_falsifier_boundary.pdf`
  - `figures/h1_metric_accounting.pdf`
  - `figures/h1_ablation_tradeoff.pdf`
  - `figures/h1_robustness_ci.pdf`

## 1. Why The RC-Ranked Champion Does Not Win Broadly

- The primary startup matrix is a five-way tie at `17/24` startup successes.
- Grouped counts by polarity, impedance ratio, and ramp rate are identical across all five designs.
- The dominant limiter in the primary matrix is therefore shared source stress and storage dynamics, not the selector law.

## 2. What The Executed Ablations Actually Show

- `source_blind` is not a weak control. It is the strongest deterministic design in the expanded falsifier suite.
- The startup-matrix equality between `champion` and `source_blind` means explicit ranking buys no startup-envelope advantage in the measured operating region.
- The falsifier gaps make the point sharper:
  - `fa_002` and `fa_006` are won by `source_blind` and lost by the RC-ranked champion
  - the RC-ranked champion wins no case that `source_blind` loses
- The correct mechanistic conclusion is:
  - packet-gated isolation matters
  - explicit RC-based branch ranking does not survive the ablation screen

## 3. Why `time_constant_ranked` Still Matters

- `time_constant_ranked` keeps `17/24` startup-matrix success and `9/10` falsifier success.
- Its successful-case pre-handoff control-energy median is `1.11852e-13 J`, versus `2.37717e-13 J` for the RC-ranked champion.
- That `52.9%` reduction is large enough to matter, but it does not restore the RC-ranked design as the headline result.
- The right interpretation is that if one still wants a source-aware control within the packet-gated family, the time-constant implementation is the only version that remains competitive.

## 4. Metric-Contract Repair Changed The Energy Story For The Better

- The shared measurement hooks now stop `e_ctrl` and `e_backdrive` at first handoff rather than integrating across the full transient by default.
- This removes the failure-window bias that previously distorted the control-energy narrative.
- The result is cleaner:
  - the RC-ranked champion and `source_blind` share the same successful-case median pre-handoff control energy
  - `time_constant_ranked` is clearly lower
  - the remaining energy claims can be tied directly to effective control conductance rather than to artifact-heavy full-window integration

## 5. The Smallest Defensible Claim Boundary

- The final claim boundary is not the old two-case subset `{fa_001, fa_005}` anymore.
- The stronger and more honest boundary is:
  - packet-gated isolation beats the nonaware join topology under collapse, mixed-polarity conflict, and leak-path stress
  - explicit RC ranking is unnecessary inside that packet-gated family
- Load-bearing cases:
  - `fa_001`: fixed path fails; packet-gated family survives
  - `fa_005`: nonaware fails; packet-gated family survives
  - `fa_009` and `fa_010`: nonaware fails leak-path stress while the packet-gated family survives
  - `fa_002` and `fa_006`: `source_blind` survives cases that the RC-ranked champion does not

## 6. Robustness Readout

- `fa_001` stays the sharpest fixed-baseline separator under variation.
- `fa_005` stays the sharpest nonaware separator under variation.
- `fa_004` confirms that the repaired chatter case now produces the intended fall/rise2 events, although all designs still start under sampled variation.
- `sm_015` confirms that the primary-matrix null remains a null under sampled perturbation.

## Conclusion

- The H1 lane no longer supports a champion-design paper.
- It does support a stronger paper than the old narrowed story:
  - a falsification result showing that minimal packet gating preserves the adversarial boundary, explicit source ranking is unnecessary, and a lower-overhead time-constant control is the only source-aware variant worth keeping.
