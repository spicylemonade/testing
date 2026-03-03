# Experiment Protocol (Preregistered)

## Objective

Evaluate baseline, symplectic, and Barnes-Hut methods under a controlled matrix that is reproducible and directly aligned with thresholds in `results/repo_analysis/problem_statement.md`.

## Methods under test

1. `baseline` (explicit Euler + direct O(N^2) force)
2. `symplectic` (fixed-step symplectic Euler + direct O(N^2) force)
3. `barnes_hut` (explicit Euler + Barnes-Hut approximation; `theta=0.8`, `leaf_size=8`, `bh_min_n=64`)

## Scenarios

1. **Two-body analytic proxy** (`scenario=two_body`, `N=2`)
2. **Three-body chaotic** (`scenario=three_body`, `N=3`)
3. **Random N-body** (`scenario=random`, `N in {64, 256, 512, 1024}`)

## Sweep variables

- `dt` values: `{0.002, 0.001, 0.0008}`
- Seeds: `{42, 43, 44, 45, 46}` (fixed preregistered set)
- Softening:
  - two-body: `1e-4`
  - three-body/random-N: `1e-3`

## Step/horizon policy

- Two-body and three-body use a fixed physical horizon with steps adjusted by `dt`.
- Random N-body uses practical high-N step counts to keep runtime bounded while preserving comparable short-horizon dynamics:
  - `N=64`: steps `{120, 240, 300}` for `dt {0.002, 0.001, 0.0008}`
  - `N=256`: steps `{24, 48, 60}`
  - `N=512`: steps `{8, 16, 20}`
  - `N=1024`: steps `{4, 8, 10}`

## Stopping criteria

Stop a run when the first criterion is met:

1. Planned step budget reached.
2. Non-finite state (`NaN`/`Inf`) detected.
3. Wall-clock runtime exceeds 30 minutes for a single run.

## Metric computation rules

- Max energy drift %: `100 * max_t |E(t)-E(0)| / |E(0)|`
- Max angular momentum drift %: `100 * max_t ||L(t)-L(0)|| / ||L(0)||`
- Center-of-mass drift: `||COM_final - COM_0||`
- Runtime per step: wall-clock runtime divided by executed steps.
- Throughput: executed steps per second.
- Two-body orbit error: RMS position error normalized by initial orbital radius.
- Barnes-Hut error metric: final-position RMS error % relative to direct-force baseline with matched seed/config.

## Reporting policy

- Report per-run raw metrics and aggregated medians across seeds.
- Use no seed replacement and no outlier deletion.
- Keep command/config hash, commit hash, and environment metadata per run in manifest files.
