# Phase 4 Experiment Matrix

This file freezes the exact extracted-score experiment table for the active H1 pilot before any result is treated as evidence.

## Common Reporting Rules

- Every row reports exact legal certificate score `(m+r)/(n-t)` after exact verifier confirmation, or a documented verification failure.
- No row may substitute fill time, closure count, occupancy, decoder success rate, or any other surrogate for exact score.
- Every matched comparison must keep fixed:
  - geometry,
  - `X`,
  - symmetry quotient,
  - verifier,
  - grammar-size budget,
  - optimizer/search budget,
  - and canonicalization policy.

## H1 Core Rows

1. `H1_L1_exact`
   - Frozen width-2 corridor grammar at level 1.
   - Report: exact score, `m`, `r`, `n`, `t`, `|Sigma_active|`, grammar description length, and whether extraction was legal with no repair.

2. `H1_L2_exact`
   - Same grammar, same `X`, same extractor, level 2.
   - Report: exact score and the transfer delta relative to `H1_L1_exact`.

3. `H1_transfer_gate`
   - Derived row comparing `S_1` and `S_2`.
   - Pivot trigger fires if `S_2 >= S_1` or if level-2 extraction needs bespoke repair.

## Matched Baselines

4. `baseline_no_ca_same_geometry`
   - Direct no-CA certificate search on the same extracted geometry and the same fixed `X`.

5. `baseline_low_height_asymmetric_X`
   - Same geometry with low-height asymmetric `X` sweeps under the same search budget.

6. `baseline_bounded_slope`
   - Same geometry restricted to bounded-many-slope / low-rational-complexity families.

7. `baseline_slowly_growing_X`
   - Same geometry with controlled `X`-growth outside active H1, reported only as a matched control frontier.

8. `baseline_isotropic`
   - Remove oriented transport / anisotropy while matching edge density and budget.

9. `baseline_random_label`
   - Randomize labels while preserving geometry, edge count, and `|X|`.

## Required Perturbations And Ablations

10. `ablation_stage_order`
    - Reorder the recursive stage or substitution expansion while keeping the same local grammar.

11. `ablation_aspect_ratio`
    - Perturb corridor width / aspect ratio within the same route family.

12. `ablation_boundary_seed_removal`
    - Remove or thin the boundary-band seeds from the same candidate family.

13. `ablation_randomize_R`
    - Keep `G` and `X`, randomize singleton seed placement.

14. `ablation_randomize_T`
    - Keep `G` and `X`, randomize initial solved set of the same size.

15. `ablation_randomize_X`
    - Keep `G`, randomize nonzero labels subject to the same coordinate-height budget.

16. `ablation_exact_elimination_replacement`
    - Replace any local screening or CA rollout with exact elimination on the same candidate family.

17. `ablation_freeze_X_scale_n`
    - Scale the geometry while freezing `X`.

## Optional Diagnostic Rows

- `diag_zero_forcing_screen`
  - Auxiliary zero-forcing-style structural screen from the reframe pass; not a substitute for exact verification.

- `diag_structural_observability_screen`
  - Auxiliary observability-style screen from the reframe pass; not a substitute for exact verification.

## Decision Rule

- H1 is relevant only if the exact extracted frontier beats the matched no-CA and bounded-slope baselines in or near the `1.70` neighborhood before any claim about the `1.675` target is entertained.
- If not, document the no-go cleanly and evaluate the H1-to-H2 pivot against the pre-registered trigger.
