# Director Brief

## Decision

- Champion direction: `H1` self-diagnosing cross-regime integrator orchestration.
- Backup direction: `H2` commodity-hardware deterministic replay with fidelity envelopes.
- Hold `H3` event-aware differentiable gravity simulation in reserve. It has upside, but it is more overlap-sensitive and less well-audited than `H1` or `H2`.

## Why `H1` Wins

- It matches the strongest gap signal in [gap_map.md](/home/archivara/work/repo/results/swarm/gap_map.md): the seam between mature integrators and trustworthy user-facing behavior.
- It avoids the most crowded territory identified in the same file: raw solver speed, another standalone integrator, generic browser claims, and generic educational demos.
- It is easier to falsify cleanly than event-aware differentiable simulation and more novel than a plain implementation exercise. A short feature audit can kill it early if the orchestration, switching, and explanation stack already exists elsewhere.
- It keeps the work framed as a systems and trust contribution for a gravity simulator, which fits the task better than a benchmark-only or visualization-only paper.

## Why `H2` Is The Backup

- `H2` is still a credible systems contribution if `H1` collapses under overlap pressure.
- It has a clear success or failure boundary: deterministic replay under a declared runtime contract plus explicit fidelity envelopes.
- It is less conceptually novel than `H1`, but the validation story is straightforward and the failure modes are easy to expose.

## Blocker

- Three required scout outputs are missing: `results/swarm/hypothesis_bridge.md`, `results/swarm/hypothesis_negative_space.md`, and `results/swarm/falsifier.md`.
- Because those files are absent, the current synthesis leans too heavily on [gap_map.md](/home/archivara/work/repo/results/swarm/gap_map.md) and the noisy literature scaffolding. Treat all novelty claims as provisional until the missing swarm inputs are supplied or regenerated.

## Exact Next Experiment For The Researcher

- Run one closed-set falsification experiment for `H1` rather than another wide search.
- Use exactly three scenarios: a long-horizon secular system, a close-encounter or scattering case, and a high-eccentricity passage.
- Compare a fixed-step symplectic baseline and a hybrid close-encounter baseline against an orchestration policy that can trigger solver or precision escalation.
- Record only four outcomes: invariant drift, missed-or-late encounter detection, intervention timing, and whether the intervention reason is interpretable to the user.
- Kill `H1` immediately if the orchestration policy does not produce materially earlier or more actionable unsafe-state warnings than the baselines.
- Do not promote any result from that experiment into a strong novelty claim until the missing scout outputs above are restored.
