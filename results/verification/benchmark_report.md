# Benchmark Report

Date: 2026-03-12
Verification phase: post_deepen
Scope: controls, baselines, ablations, and evaluation weaknesses in `001_packet_scout_handoff_root`
Status: PASS only for a narrow post-repair same-family DEEPEN observation; BLOCK for a publication-quality benchmark package

## High-Level Verdict

- The only cleanly post-repair benchmark slice is the DEEPEN near-tie suite. Inside that slice, `confidence_gated` matches `source_blind` on static same-polarity near ties, improves median `t_handoff` by `0.30882 s` on the six late-arrival same-polarity near ties, and still loses to `time_constant_ranked`.
- The broader startup/falsifier package is not yet benchmark-complete enough for publication-quality claims. The current artifact set still mixes metric contracts, fragments the key internal baselines across separate tables, and lacks the controls needed to isolate the claimed mechanism.

## Blocking Gaps

### 1. The main comparison pack does not yet demonstrate a full rerun under the repaired metric contract

- `item028_metric_control_repair.md` changes the contract to explicit `n_handoff` timing plus `startup_ok = (vstore_final >= V_HANDOFF) * (handoff_seen_final >= 0.5)`.
- `deepen_results.csv` and `deepen_near_tie_runlog.jsonl` carry the repaired fields for every row: `handoff_seen_v` and `t_store_proxy_s` are populated in `40/40` rows.
- `startup_runlog.jsonl` has `120` rows, but `handoff_seen_v` is blank in `120/120`, and `startup_summary.json` was last updated at `2026-03-12T10:09:32Z`, before the repair note.
- `falsifier_runlog.jsonl` has `50` rows, but `handoff_seen_v` is populated only for the `10` `source_blind` rows and blank for the other `40`.
- Benchmark consequence:
  - the package currently mixes pre-repair and post-repair evidence
  - the `17/24` startup tie and much of the deterministic falsifier table are not on the same visible measurement contract as the DEEPEN suite
- Falsifiable next test:
  - rerun the full `24`-case startup matrix and full `10`-case falsifier suite for all five designs with the repaired hooks
  - if any success count, same-family ranking, or decisive separator flips, replace the old matrix narrative instead of averaging old and new evidence together

### 2. The main comparison surface still omits key internal baselines and the active DEEPEN lane

- `benchmark_comparison.csv` and `benchmark_summary.json` only compare `champion` against `fixed` and `nonaware`.
- The current startup tables already expose stronger internal comparators:
  - `startup_summary.json` reports `time_constant_ranked` at `18.3911 s` median successful `t_handoff` and `1.11852e-13 J` median successful `e_ctrl`, versus `champion` at `18.5461 s` and `2.37717e-13 J`
  - `startup_summary.json` also shows `source_blind` tied with the rest at `17/24` successes on the current primary matrix
- The DEEPEN lane is also fragmented away from the main ablation bundle:
  - `analysis_summary.json` and `ablation_summary.json` stop at `champion`, `fixed`, `nonaware`, `source_blind`, and `time_constant_ranked`
  - `confidence_gated` and `blind_packet_merge` only appear in the separate DEEPEN artifacts
- Benchmark consequence:
  - the strongest same-family challengers are not presented on one comparison surface
  - the current lane can only be understood by manually stitching together `startup_*`, `analysis_*`, and `deepen_*` artifacts
- Falsifiable next test:
  - publish one unified comparator table on matched cases that includes `fixed`, `nonaware`, `source_blind`, `time_constant_ranked`, `blind_packet_merge`, and `confidence_gated`
  - if `time_constant_ranked` remains faster and lower-overhead on the matched slice, write the result as a frontier/tradeoff paper rather than a new champion benchmark

### 3. There is still no executed literature-faithful comparator

- `claim_matrix.md`, `verification_summary.md`, and `final_research_brief.md` all keep literature-performance claims blocked.
- The executed comparisons are internal only: `fixed`, `nonaware`, `source_blind`, `time_constant_ranked`, and `blind_packet_merge`.
- Benchmark consequence:
  - the repo can support an internal same-family frontier only
  - it still cannot support "better than prior art", "closest literature family beaten", or strong novelty-through-performance language
- Falsifiable next test:
  - implement one literature-faithful proxy from the recovered multi-input self-powered interface family under the same `source_pair_models.inc` and `VCTRL_MON` accounting
  - if that comparator matches the late-arrival gain or the speed/backdrive frontier, kill any external-superiority sentence

### 4. The primary matrix is a 24-point screen, not a factor-complete heterogeneous-source benchmark

- The frozen source contract exposes `4` voltage levels, `4` ramp levels, `3` impedance ratios, and `2` polarities, i.e. `96` possible cells.
- `startup_matrix_manifest.json` executes `24` aliased points, leaving `72` cross-combinations unsampled.
- `source_pair_models.inc` still uses one global `RAMP_MVPS`, and the primary matrix mostly keeps `VOC_A = VOC_B`.
- Benchmark consequence:
  - the primary matrix is a screening set, not a field map
  - broad "heterogeneous weak-source startup" language is under-supported
- Falsifiable next test:
  - either run the missing cross-combinations or rewrite the paper to call this a 24-point screen explicitly
  - add independent per-source ramps and more than the current two unequal-`VOC` falsifier cases before claiming heterogeneous-source generality

### 5. The DEEPEN positive result is missing the control that would separate "confidence" from "just wait longer"

- The surviving DEEPEN win is `confidence_gated` versus `source_blind` on six late-arrival same-polarity near ties: median `t_handoff` gain `+0.30882 s`.
- `deepen_near_tie_manifest.json` omits `fixed` and `nonaware`, so even that late-arrival improvement is benchmarked only inside the packet family.
- No executed control holds packet isolation fixed while replacing the confidence logic with a simple fixed holdoff, delayed handoff, or matched extra latency/energy budget.
- Benchmark consequence:
  - the current data shows a same-family improvement, but not yet the causal reason for it
  - a reviewer can still argue that the gain comes from waiting rather than from evidence-driven commitment
- Falsifiable next test:
  - add a `source_blind + fixed_commit_delay` control with matched pre-handoff energy accounting
  - if it reproduces the late-arrival gain without the confidence node, kill the confidence-specific mechanism claim

### 6. A simple physical reverse-isolation baseline and scout-removal ablations are still missing

- The decisive control frontier compares `blind_packet_merge`, `confidence_gated`, and `source_blind`.
- There is still no low-overhead reverse-current-blocking / back-to-back isolation baseline under the same hooks.
- `source_blind_packet_gate` and `blind_packet_merge_gate` are not minimal controls:
  - both keep `EOBS_*`, `RSCOUT_*`, `CSCOUT_*`, and `BCTRL_SCOUT`
  - there is no executed no-scout blind packet control and no executed no-scout merge control
- Benchmark consequence:
  - the package does not yet show that packet gating is the minimal or necessary way to get the measured speed/backdrive trade
  - it also does not isolate whether the scout apparatus matters once isolation/merge behavior is fixed
- Falsifiable next test:
  - implement one simple reverse-blocking baseline under the same `VCTRL_MON` contract
  - run no-scout versions of the blind packet gate and merged control
  - if either closes the frontier, collapse the packet/scout headline to a generic isolation result

### 7. Error analysis is incomplete on both failure modes and DEEPEN uncertainty

- `startup_results.csv` and `falsifier_results.csv` encode failures as `startup_ok = 0.0` with blank `t_handoff*` fields while `status = ok` and `return_code = 0`, but there is no failure-class column or companion failure table.
- The same hard startup corners recur without explanation: the current startup package fails the same seven cases across all designs (`sm_003`, `sm_004`, `sm_008`, `sm_013`, `sm_014`, `sm_017`, `sm_021`).
- The deterministic falsifier failures also differ by attack class, but `falsifier_summary.json` reduces them to counts instead of causes.
- The DEEPEN slice still has no uncertainty intervals:
  - `deepen_summary.json` reports medians over `12` core cases plus `4` decisive control runs
  - `robustness_summary.json` covers only `fa_001`, `fa_004`, `fa_005`, and `sm_015`; it does not cover any DEEPEN late-arrival case
- Benchmark consequence:
  - the package does not yet explain why the boundaries occur
  - the reported `0.30882 s` late-arrival gain and the control-frontier backdrive separation are still point-estimate stories
- Falsifiable next test:
  - add a failure taxonomy such as `no_handoff`, `store_only`, `fall_rise2`, `late_commit`, and `wrong_way_loss`
  - run robustness on all six late DEEPEN cases and the four decisive control cases across `confidence_gated`, `source_blind`, `time_constant_ranked`, and `blind_packet_merge`
  - if the gain interval crosses zero, demote the late-arrival advantage to anecdotal

### 8. Stress-test coverage is still too narrow for publication-quality generalization

- `robustness_summary.json` covers only four case IDs with `24` samples each: `fa_001`, `fa_004`, `fa_005`, and `sm_015`.
- That leaves `7/10` falsifier attacks and `23/24` startup cases without perturbation coverage, including the champion's nominal deterministic falsifier failures `fa_002` and `fa_006`.
- The DEEPEN manifest is same-polarity only, `ratio_b_to_a` in `{1, 3}`, `VOC` pairs in `{100/101, 100/103, 100/105}`, and delay in `{0, 4}`.
- There is no mixed-polarity near-tie DEEPEN, no late-arrival opposite-polarity separator, and no repeated-collapse / stale-state restart suite after first handoff.
- Benchmark consequence:
  - the safe claim remains confined to same-polarity temporal separability inside the abstract two-source model
- Falsifiable next test:
  - add mixed-polarity late-arrival near ties, independent per-source ramp laws, and repeated-collapse restart cases with a fixed scrub baseline
  - if the confidence controller loses there or a simple scrub baseline matches it, keep only the current narrow same-polarity claim

## Consistency Problems To Repair Before Submission

### 9. Several verification notes are stale or contradicted by the current machine-readable tables

- `item018_benchmark_note.md` still documents a `24`-case / `3`-design primary benchmark.
- `item019_falsifier_note.md` still documents `6` falsifier cases and `3` designs.
- `item020_run_audit.md` still says the startup log has `72` rows and the falsifier log has `18` rows, but the current run logs have `120` and `50`.
- `claim_matrix.md` still centers the old `variant_01_rc_ranked_packet_gate`, while `verification_summary.md`, `final_research_brief.md`, and the DEEPEN artifacts frame the final paper around `confidence_gated`.
- `item021_decision_memo.md` and `item022_analysis_package.md` still say `source_blind` is `10/10` and the strongest deterministic falsifier design.
- The current repaired falsifier table says otherwise:
  - `champion`: `8/10`
  - `fixed`: `7/10`
  - `nonaware`: `5/10`
  - `source_blind`: `5/10`
  - `time_constant_ranked`: `9/10`
- `falsifier_cases.json` currently lists `"designs": ["source_blind"]`, while `falsifier_runlog.jsonl` and `falsifier_summary.json` show five designs.
- `startup_summary.json` labels the suite `startup_matrix_v2`, while `startup_matrix_manifest.json` still says `startup_matrix_v1`.
- Benchmark consequence:
  - the current same-family interpretation is not synchronized
  - readers cannot tell whether the paper is about the old RC-ranked champion, packet-gated falsification, or the final confidence-gated lane
- Falsifiable next test:
  - regenerate the manifests and every downstream note from the current tables
  - do not submit until every quoted count matches the machine-readable summary

### 10. Backdrive reporting is thresholded and still model-limited

- `tools/run_h1_falsifier.py` counts `nonzero_backdrive_cases` only when `e_backdrive_j > 1e-12`.
- The deterministic falsifier table still contains positive backdrive values below that threshold, e.g. `nonaware/fa_005 = 3.33373e-14 J` and `nonaware/fa_008 = 2.57416e-14 J`, so "zero nonzero cases" means "below the reporting threshold", not exact zero.
- `ablation_summary.json` also reports a nonzero `nonaware` falsifier median `e_backdrive_j = 2.356385e-17` despite the summary count staying at zero.
- The primary matrix reports `0.0` backdrive in all `120/120` rows, while `startup_cells.inc` and `source_pair_models.inc` still use idealized routing and a simplified two-source model.
- Benchmark consequence:
  - anti-backdrive should be written as an internal model frontier, not as a device-faithful physical result
- Falsifiable next test:
  - state the threshold explicitly and rerun the decisive controls under a parasitic sweep or a more physical reverse-isolation baseline
  - if the zero-backdrive separation collapses, remove the stronger anti-backdrive wording

### 11. The final DEEPEN lane still lacks a fully audited and reproducible publication bundle

- `item020_run_audit.md` audits the startup and falsifier logs only; it does not audit the DEEPEN run that now carries the final positive claim.
- The DEEPEN runlog does exist and is complete:
  - `deepen_near_tie_runlog.jsonl` contains `40` rows
  - all `40/40` rows have `status = ok`
  - the run covers `12` cases and `4` designs
- The figure bundle referenced by the notes is not reproducible from the tracked tree:
  - `item030_deepen_matrix.md` names `figures/h1_deepen_confidence_tradeoff.svg`
  - `deepen_summary.json` names `figures/h1_deepen_confidence_tradeoff.pdf`
  - no `figures/` directory or tracked `h1_*.(pdf|svg)` artifact exists under `results/concept_evolve/tree/001_packet_scout_handoff_root`
- The claimed "pre-registered gate" against `source_blind` is explicit in `results/research_context.md` and then in the DEEPEN results note, but it is not frozen in a separate pre-run verification artifact inside the lane directory.
- Benchmark consequence:
  - the final lane is interesting, but its governance and artifact bundle are still thinner than the older startup/falsifier pack
  - that is not yet publication-grade for a benchmark-centered paper
- Falsifiable next test:
  - add a DEEPEN audit memo parallel to `item020_run_audit.md`
  - export the actual DEEPEN figure files into a tracked location and make every note point to the same filename
  - freeze the gate condition in a pre-run lane artifact rather than only in post-hoc result text

## Bottom Line

- Safe now:
  - only the fully post-repair same-family DEEPEN statement
  - `confidence_gated` helps on same-polarity late-arrival near ties relative to `source_blind`, abstains on static near ties, and does not beat `time_constant_ranked`
- Not safe now:
  - any unified benchmark story that mixes the old startup/falsifier matrices with the post-repair DEEPEN suite
  - any literature-performance claim
  - any broad heterogeneous-source or best-overall selector claim
