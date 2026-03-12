# Tooling Status

Generated: 2026-03-12

## Summary

- `ngspice`: not installed on `PATH`
- Rootless local install attempt: blocked by network/DNS resolution
- `.archivara/concept_evolve.py evolve`: launcher repaired, broad-task run still low-signal
- `.archivara/concept_evolve.py probe`: wrapper runs, child sub-agent fails to return artifacts
- `.archivara/concept_evolve.py reframe`: wrapper runs, child sub-agent fails to return artifacts

## Working Commands

- `python3 .archivara/concept_evolve.py --help`
- `python3 .archivara/semantic_scholar.py --help`
- `python3 .archivara/rubric_tool.py summary`

## Blocking Defects

### 1. `ngspice` missing

- Symptom:
  - `command -v ngspice` returns nothing.
- Attempted unblock:
  - Checked Debian package metadata with `apt-cache policy ngspice`.
  - Attempted rootless local install with:
    - `apt-get download ngspice`
    - `dpkg-deb -x ngspice_*.deb extracted`
- Failure:
  - `Temporary failure resolving 'deb.debian.org'`
- Owner:
  - Environment / network access to Debian package hosts.
- Impact:
  - Real `ngspice` experiment execution is currently blocked.

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

### 3. `concept_evolve.py probe` child failure

- Call site:
  - `python3 .archivara/concept_evolve.py probe "What is the minimum-energy source-inference mechanism that still improves helper-free multi-source cold start under mixed polarity and 1:20 impedance asymmetry?"`
- Failure:
  - Both sub-agent attempts returned `rc=1`.
  - `results/concept_evolve/probe_result.json` was written only as a `parse_error` placeholder.
- Owner:
  - External Codex responses proxy / child-agent connectivity.
- Impact:
  - The structured probe wrapper exists, but it is not currently producing usable child-generated analysis.

### 4. `concept_evolve.py reframe` child failure

- Call site:
  - `python3 .archivara/concept_evolve.py reframe "Do electrical engineering research and discover something new/interesting. nontrivial and important. maybe you design a new circuit and use ng spice or something"`
- Failure:
  - Both sub-agent attempts returned `rc=1`.
  - `results/concept_evolve/reframings.json` was created with an empty `framings` array.
  - Latest run state recorded `turn.failed` with `stream disconnected before completion`.
- Evidence:
  - `results/concept_evolve/reframings.json`
  - `results/concept_evolve/.state/latest_run.json`
- Owner:
  - External Codex responses proxy / child-agent connectivity.

## Practical Conclusion

- The run can continue on literature, concept definition, netlist authoring, and verification packaging.
- Any rubric item that requires actual `ngspice` execution must either be unblocked by obtaining a working binary or be marked as blocked/failed with this note as the environment reference.
