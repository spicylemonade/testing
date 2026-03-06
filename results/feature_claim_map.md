# Feature To Claim Map

- `invariant_tracking`
  - Claim: `results/problem_statement.md` states that the contribution adds audit surfaces ordinary toy simulators omit, including energy, angular momentum, and center-of-mass drift.
  - Output path: scenario diagnostics in `results/baseline/*.json` and `results/audit/*_audit.json`.

- `timestep_halving_convergence`
  - Claim: `results/problem_statement.md` states that timestep-halving behavior must be measured rather than assumed.
  - Output path: `results/audit/*_audit.json` under the `convergence` key.

- `reproducibility_hooks`
  - Claim: `results/problem_statement.md` states that the same scenario bundle must be replayable across runtimes with documented tolerance envelopes.
  - Output path: `trajectory_fingerprint`, `terminal_state_fingerprint`, and `roundtrip` metadata in every audit result.

- `scenario_level_benchmark_metadata`
  - Claim: `results/problem_statement.md` states that the benchmark pack is part of the contribution, not supporting material.
  - Output path: `metadata`, `expected_metrics`, and `benchmark_tags` in every baseline and audit artifact.
