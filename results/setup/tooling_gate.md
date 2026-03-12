# Tooling Gate

- Date: `2026-03-12`
- Scope: Phase 2 `item_007`

## Status Summary

- `ngspice`
  - `command -v ngspice` still returns no global path.
  - A reproducible user-space install is now available through `./tools/setup_ngspice_local.sh`.
  - `./tools/ngspice-local -v` executes the extracted local binary successfully.
- `.archivara/concept_evolve.py`
  - `python3 .archivara/concept_evolve.py --help` works.
  - `evolve` launcher mismatch was repaired earlier in this run.
  - The mandatory broad-task `evolve` command launches but remains low-signal; the focused H1 workaround is documented in `results/concept_evolve/tooling_blockers.md`.
  - `probe` and `reframe` launch, but their useful output still depends on external Codex child reliability; exact call sites are tracked in `results/setup/tooling_status.md`.
- Shell/package environment
  - `sudo` is unavailable.
  - Current user is `uid=1000(archivara)`.
  - Root package-manager install is blocked, but outbound HTTPS works for direct artifact download.

## Exact Commands And Outcomes

### `ngspice` availability

```bash
command -v ngspice
```

- Outcome: no binary found on `PATH`.

```bash
apt-cache policy ngspice
```

- Outcome: candidate available: `39.3+ds-1`.

### Root-level install attempt

```bash
apt-get update && apt-get install -y ngspice
```

- Outcome:
  - `E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)`
  - `E: Unable to lock directory /var/lib/apt/lists/`
- Interpretation:
  - Package-manager install requires privileges not available in this environment.

### Privilege check

```bash
sudo -n true
```

- Outcome:
  - `sudo: command not found`
- Interpretation:
  - No privilege-escalation path is available from the shell.

### User-space install path

```bash
./tools/setup_ngspice_local.sh
```

- Outcome:
  - Downloads `ngspice_39.3+ds-1_amd64.deb` directly from the Debian mirror over HTTPS.
  - Extracts the package under `.tools/ngspice/extracted/`.
  - Verifies the local binary by printing the `ngspice-39` banner.

```bash
./tools/ngspice-local -v
```

- Outcome:
  - Local extracted `ngspice` binary executes successfully from the repo wrapper.

## Blockers And Owners

- Blocker: no root package-manager access.
  - Owner: environment / runner
- Blocker: `concept_evolve` child reliability still depends on the external responses proxy and pre-existing artifact semantics.
  - Owner: helper wrapper plus external Codex child runtime
- Researcher-side mitigation:
  - Use the local `ngspice` wrapper for baseline and champion experiments.
  - Keep `concept_evolve` failures documented and use focused local equivalents when a helper subcommand does not converge cleanly.

## Working Commands

```bash
./tools/setup_ngspice_local.sh
./tools/ngspice-local -v
python3 .archivara/concept_evolve.py --help
python3 .archivara/rubric_tool.py summary
```

These commands are sufficient to begin netlist authoring and `ngspice` execution without root access.
