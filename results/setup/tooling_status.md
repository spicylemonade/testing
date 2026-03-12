# Tooling Status

Generated: 2026-03-12

## Summary

- `ngspice`: not installed on `PATH`, but available through `./tools/ngspice-local`
- Rootless local install path: working via direct Debian package download plus `dpkg-deb -x`
- `.archivara/concept_evolve.py evolve`: launcher repaired, broad-task run still low-signal
- `.archivara/concept_evolve.py probe`: launches, but reliable artifact production is still not guaranteed
- `.archivara/concept_evolve.py reframe`: launches, but existing-artifact retry semantics still make the output quality check manual

## Working Commands

- `./tools/setup_ngspice_local.sh`
- `./tools/ngspice-local -v`
- `python3 .archivara/concept_evolve.py --help`
- `python3 .archivara/semantic_scholar.py --help`
- `python3 .archivara/rubric_tool.py summary`

## Remaining Defects

### 1. Global `ngspice` package install unavailable

- Symptom:
  - `command -v ngspice` returns nothing.
- Attempted unblock:
  - Checked Debian package metadata with `apt-cache policy ngspice`.
  - Root install attempt:
    - `apt-get update && apt-get install -y ngspice`
  - Working user-space fallback:
    - `./tools/setup_ngspice_local.sh`
    - `./tools/ngspice-local -v`
- Result:
  - Root install is blocked by privilege limits.
  - User-space `ngspice` execution is unblocked for this repo.
- Owner:
  - Environment for system-wide install, researcher for repo-local wrapper.
- Impact:
  - No impact on planned repo-local experiments.

### 2. `concept_evolve.py evolve` artifact drift

- Call site:
  - `python3 .archivara/concept_evolve.py evolve "Do electrical engineering research and discover something new/interesting. nontrivial and important. maybe you design a new circuit and use ng spice or something"`
- Pre-run defect:
  - Original `evolve()` launcher mismatch in `.archivara/concept_evolve.py` omitted required `_run_sub_agent()` parameters.
- Current state after repair:
  - The launcher no longer crashes.
  - The broad-task run still produced no target artifacts and drifted across off-lane queries.
- Evidence:
  - `results/concept_evolve/tooling_blockers.md`
  - `results/concept_evolve/.state/latest_run.json`

### 3. `concept_evolve.py probe` reliability gap

- Call site:
  - `python3 .archivara/concept_evolve.py probe "biggest blocker in helper-free source-aware cold start under mixed-polarity weak sources"`
- Observed problem:
  - The wrapper launches child work, but if `results/concept_evolve/probe_result.json` already exists, success still requires a semantic delta (`steering_directions`) that is not guaranteed by the child.
  - The current run has retried because the saved artifact remained a stale parse-error placeholder.
- Owner:
  - Helper wrapper semantics plus external Codex child runtime.
- Impact:
  - Probe output must be manually validated before it is treated as a research input.

### 4. `concept_evolve.py reframe` reliability gap

- Call site:
  - `python3 .archivara/concept_evolve.py reframe "Do electrical engineering research and discover something new/interesting. nontrivial and important. maybe you design a new circuit and use ng spice or something"`
- Observed problem:
  - The wrapper launches and can complete a child attempt, but existing artifact reuse means an empty prior `framings` array still requires a manual quality check before reuse.
  - The current run is useful as an execution check, not yet as a trusted reframing artifact.
- Evidence:
  - `results/concept_evolve/reframings.json`
  - `results/concept_evolve/.state/reframe_latest.json`
- Owner:
  - Helper wrapper semantics plus external Codex child runtime.

## Practical Conclusion

- The run can proceed with netlist authoring, baseline implementation, and actual repo-local `ngspice` execution through `./tools/ngspice-local`.
- `concept_evolve` helper output beyond `--help` and the repaired `evolve` path still requires human validation, so later phases should treat those artifacts as advisory until checked.
