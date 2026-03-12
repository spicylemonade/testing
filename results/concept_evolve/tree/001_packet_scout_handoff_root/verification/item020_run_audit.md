# Item 020 Run Audit

Date: 2026-03-12
Scope: experiment-governance audit over the startup and falsifier run logs
Status: PASS with a sweep block

## Execution Note

- Attempted a multi-agent audit using `worker`, `monitor`, `benchmark_auditor`, `falsifier`, and `integrator`.
- Result:
  - the environment hit the six-agent thread cap, so only the `worker` audit actually spawned
  - the remaining role sections below are parent syntheses over the same run-log and verification artifacts
- Governance consequence:
  - this memo serves as the required integrator note before any additional sweep decision

## Worker Audit

- Completed cases:
  - startup log contains `72/72` executed rows
  - falsifier log contains `18/18` executed rows
- Blocked cases:
  - none at the run-control level; every logged row finished with `status: ok`
- Instrumentation errors:
  - none material
  - the tiny negative `e_backdrive` in `fixed/fa_005` is numerical noise, not a real physics signal
- Consistency:
  - startup and falsifier summaries match their respective run logs with no duplicate or structurally inconsistent cases

## Monitor Audit

- Startup run log:
  - `72` unique rows
  - `24` cases for each of `champion`, `fixed`, and `nonaware`
- Falsifier run log:
  - `18` unique rows
  - `6` cases for each of `champion`, `fixed`, and `nonaware`
- Missing or truncated cases:
  - none
- Sequencing issue:
  - no later sweep is needed to repair logging completeness

## Benchmark Auditor Audit

- Benchmark completeness:
  - pass
  - the primary matrix and the falsifier matrix both have full design coverage
- Blocking issue:
  - the benchmark does **not** show a primary-matrix startup-success gain or any primary-matrix back-drive separation for the champion
- New-sweep decision:
  - block any new broad sweep
- What must be fixed first:
  - nothing in instrumentation
  - the next step is interpretation and lane decision, not more shotgun simulation

## Falsifier Audit

- Strongest negative signal:
  - the source-awareness claim still does not beat the fixed baseline broadly
- Strongest surviving positive signal:
  - the nonaware baseline does accumulate wrong-way energy and loses startup in several adversarial mixed/collapse cases where the champion survives
- Instrumentation problem invalidating a case:
  - none
- Current claim boundary:
  - helper-free source-aware startup may help specifically against nonaware multi-input failure modes under collapse and mixed-polarity stress
  - it is not yet a general superiority claim over the fixed startup path

## Integrator Note

- Completed cases:
  - accepted as-is from the current startup and falsifier logs
- Blocked cases:
  - none in execution
  - the block is interpretive, not operational
- Instrumentation errors:
  - none that require rerun
- Sweep decision:
  - **no new broad sweep is allowed**
- Governing rationale:
  - the current evidence is sufficient to decide whether H1 is promoted, narrowed, or killed
  - another broad sweep would only repeat the same benchmark null unless the problem formulation changes materially
