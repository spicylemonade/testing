# Final Research Brief

Date: 2026-03-12
Scope: final validated H1 brief after the ablation reruns, metric repair, citation cleanup, and robustness study
Status: PASS for a narrowed falsification/simplification result

## Writer (`writer`)

- Core question:
  - in a helper-free weak multi-source cold-start model, is explicit pre-handoff source ranking actually necessary once packetized isolation is already present
- Closest prior-work family:
  - weak-source startup papers such as `goppert2016startup70mv`, `das2017selfstarter`, `quintero2019cmosstartup`, and `coustans2019coldstart60mv`
  - adaptive dual-source and bipolar-input papers such as `tang2018dualsource`, `cao2019bipolarinput`, and `kuai2022dualpolarityjssc`
  - multi-input interface papers such as `alhawari2016multisourcepmu`, `alghisi2017batteryless`, `wang2023serialstack`, `chen2024collaborative`, `weng2024osece`, and `li2022multiinputplatform`
- Implemented design family:
  - `champion`: RC-ranked packet gate
  - `source_blind`: packet gate with the same isolation scaffold but no source awareness
  - `time_constant_ranked`: dual-window fast/slow source-aware selector with lighter control current
- Validated result:
  - the primary 24-case matrix is tied at `17/24` startup successes for all five designs
  - `source_blind` is the empirical leader on the 10-case falsifier suite at `10/10`
  - `time_constant_ranked` is `9/10` and reduces median successful-case pre-handoff control energy to `1.11852e-13 J`
  - the original RC-ranked design is only `8/10`, so the initial mechanism thesis is falsified

## Reviewer (`reviewer`)

- The paper should not claim that the RC-ranked design won.
- The paper should show the null primary matrix first.
- The paper should make the ablation logic explicit:
  - if blind packet gating beats source-aware ranking, then source awareness is not the causal ingredient
- The fixed startup path remains competitive and should be presented honestly.

## Citation Auditor (`citation_auditor`)

- The active citation spine is now real and recovered:
  - `tang2018dualsource`
  - `cao2019bipolarinput`
  - `kuai2022dualpolarityjssc`
  - `alhawari2016multisourcepmu`
  - `alghisi2017batteryless`
  - `wang2023serialstack`
  - `chen2024collaborative`
  - `weng2024osece`
  - `li2022multiinputplatform`
  - `gogolou2025multisourcereview`
- Blocked wording remains blocked:
  - `first`
  - `novel`
  - `best`
  - literature-performance superiority claims

## Benchmark Auditor (`benchmark_auditor`)

- Benchmark integrity now passes for the narrowed manuscript:
  - same-family ablation executed
  - lower-overhead control executed
  - real chatter, unequal-`VOC`, and leak-path falsifiers executed
  - robustness intervals reported
- The benchmark does not clear the original superiority story.
- The benchmark does clear a falsification story.

## Integrator (`integrator`)

- Final integrated verdict:
  - H1 is not promoted as originally framed
  - H1 is not killed
  - H1 is reportable as a negative-result and simplification paper
- Allowed final claim:
  - in the executed helper-free weak-source model, packetized pre-handoff isolation is the load-bearing ingredient, while explicit source ranking is falsified by a blind packet-gate ablation that matches the primary matrix and improves adversarial startup outcomes
- Open kill conditions:
  - a reproduced literature-faithful comparator shows the same helper-free packet-gated boundary already exists
  - a stronger local control eclipses both `source_blind` and `time_constant_ranked` under the same evidence contract
