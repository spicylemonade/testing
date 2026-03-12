# Item 022 Analysis Package

Date: 2026-03-12
Scope: explain why the H1 champion wins or fails, quantify sensitivity to the required factors, and identify the smallest surviving claim boundary
Status: PASS with a narrowed claim boundary

## Generated Artifacts

- Sensitivity table:
  - `tables/analysis_sensitivity.csv`
- Pairwise factor table:
  - `tables/analysis_pairwise.csv`
- Machine-readable summary:
  - `tables/analysis_summary.json`
- Primary-matrix figure:
  - `figures/h1_startup_sensitivity.svg`
- Falsifier-boundary figure:
  - `figures/h1_falsifier_boundary.svg`

## Why The Champion Does Not Win Broadly

- The primary matrix does not show a startup-correctness advantage:
  - `startup_ok` is tied at `17/24` for champion, fixed, and nonaware
- The dominant limiter in the primary matrix is shared source-model stress, not the arbitration topology:
  - all three designs are `6/6` at `0.1 mV/s`
  - all three designs are `6/6` at `1 mV/s`
  - all three designs fall to `4/6` at `10 mV/s`
  - all three designs fall to `1/6` at `100 mV/s`
- The fixed baseline remains too competitive for a broader H1 story:
  - the champion never improves startup count over fixed in any grouped primary-matrix slice
  - the champion is sometimes faster than fixed, but only on a minority of successful cases and never with a startup-count gain

## Sensitivity Readout

### Ramp Rate

- Ramp rate is the strongest shared driver of outcome in the primary matrix.
- Successful-case median control energy falls sharply as the ramp speeds up:
  - champion: `4.71e-01 J` at `0.1 mV/s`, `3.76e-03 J` at `1 mV/s`, `1.19e-03 J` at `10 mV/s`, `2.49e-06 J` at `100 mV/s`
  - fixed and nonaware follow the same pattern
- Interpretation:
  - startup dwell time dominates control-energy cost across all three designs
  - the primary matrix therefore cannot support a claim that the champion wins simply because its control logic is lighter

### Source Impedance Spread

- The worst grouped regime for every design is the moderate asymmetry slice:
  - ratio `1:5` gives `5/8` startup successes for champion, fixed, and nonaware
- Ratio `1:1` and ratio `1:20` both give `6/8` successes for every design.
- What does separate:
  - at ratio `1:20`, the champion has lower `e_ctrl` than fixed in `8/8` grouped cases and lower `e_ctrl` than nonaware in `7/8`
  - at ratio `1:1`, the champion is faster than fixed in `6/8` cases and faster than nonaware in `5/8`
- Interpretation:
  - impedance spread changes control burden and handoff timing, but not startup correctness in the primary matrix

### Polarity Mix

- Same-polarity cases are only slightly easier than mixed-polarity cases:
  - all three designs are `9/12` on same polarity
  - all three designs are `8/12` on mixed polarity
- Mixed polarity inflates control-energy cost for every design:
  - champion successful-case median `e_ctrl` rises from `7.53e-04 J` in same-polarity cases to `3.83e-02 J` in mixed-polarity cases
  - fixed rises from `6.89e-04 J` to `3.59e-02 J`
  - nonaware rises from `8.56e-04 J` to `3.97e-02 J`
- Interpretation:
  - polarity routing is a real cost center
  - but mixed polarity by itself still does not produce a primary-matrix correctness win for the champion

### Control Overhead

- The champion is usually lower in measured control energy without converting that into general startup wins:
  - lower `e_ctrl` than fixed in `13/24` primary-matrix cases
  - lower `e_ctrl` than nonaware in `22/24` primary-matrix cases
  - better startup count than fixed in `0/24`
  - better startup count than nonaware in `0/24`
- The falsifier suite shows why this matters:
  - `fa_003` gives the champion lower control energy than both baselines, but no startup-correctness advantage
- Interpretation:
  - lower control energy is real, but it is not the surviving headline result
  - the surviving result is narrower and tied to adversarial source interactions, not to control energy alone

### Smallest Condition Set Where The Claim Still Holds

- The smallest evidence-backed condition set is the two-case falsifier subset:
  - `fa_001`
    - same polarity
    - ratio `1:5`
    - `100 mV`
    - `10 mV/s`
    - one-source collapse attack
    - result: champion starts, fixed fails, nonaware starts later with `1.65e-06 J` back-drive
  - `fa_005`
    - mixed polarity
    - ratio `1:1`
    - `300 mV`
    - `10 mV/s`
    - chatter-intended transient stress
    - result: champion and fixed start, nonaware fails with `3.59e-04 J` wrong-way energy
- What does **not** survive as a claim boundary:
  - `fa_002`, `fa_004`, and `fa_006` because the champion does not rescue startup there
  - `fa_003` because it is only a lower-control-energy result without a correctness gain

### Mechanistic Readout

- The RC-ranked packet gate does not change the global startup envelope enough to beat the fixed path broadly.
- It does appear to matter when a nonaware path can connect both sources through a transiently bad branch choice:
  - collapse and mixed-polarity attacks are the only places where the champion avoids wrong-way energy or preserves startup on the narrowed evidence boundary
- This explains the overall pattern:
  - the primary matrix is mostly governed by shared source stress and storage dynamics
  - the falsifier suite is where pre-arbitration source awareness becomes visible

### Conclusion

- The champion fails as a broad startup-interface winner.
- The champion survives as a narrow adversarial-startup result:
  - helper-free pre-arbitration source awareness can avoid some nonaware mixed-source failure modes during collapse and mixed-polarity transients
