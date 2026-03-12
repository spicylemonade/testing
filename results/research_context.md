# Research Context

- Stage: `phase_1_inventory_and_lane_freeze`
- Date: `2026-03-12`
- Researcher lane status: active
- Champion lane: `H1_multisource_cold_start`
- Backup lane: `H2_cryo_support_blocks`
- Reserve lane: `H3_dynamic_source_impedance`

## Repo Reality

- The repository is mostly research scaffolding. `README.md` is only `# testing` and does not constrain the technical direction.
- `TASK_orchestrator.md` is absent. The effective handoff is carried by `research_rubric.json`, `results/swarm/director_brief.md`, `results/swarm/hypotheses.json`, `results/swarm/tool_plan.md`, and `results/swarm/falsifier.md`.
- `results/verification/` exists as a directory but started this run empty. No novelty, benchmark, citation, or summary reports were present at handoff.
- The saved literature watchlist and seed snapshot are polluted by the original vague query and must be repaired rather than trusted.

## Module Inventory

### Repo Root

- `README.md`
  - Placeholder only. No research, tooling, or artifact guidance.
- `research_rubric.json`
  - Canonical execution contract for this run: 5 phases, 26 items, H1-centered validation gates, and explicit multi-agent checkpoints.
- `TASK_orchestrator.md`
  - Missing. Treat the swarm artifacts plus rubric as the orchestrator handoff.
- `TASK_researcher_attempt_1.md`
  - Present as a previous attempt log, but the rubric and swarm artifacts are more authoritative.

### Helper Scripts

- `.archivara/semantic_scholar.py`
  - Cached Semantic Scholar client with `search`, `citations`, `references`, `recommend`, `graph`, and `bibtex`.
  - Writes canonical search memory to `results/literature/semantic_scholar_manifest.json`.
  - Primary mechanism for focused literature expansion without restarting the search from zero.
- `.archivara/concept_evolve.py`
  - Required structured exploration tool for concept-tree generation and iteration.
  - `probe`, `reframe`, and `iterate` already use operation fingerprints, run-state logging, and watched artifacts.
  - Blocking defect discovered on entry: the original `evolve()` path called `_run_sub_agent()` with only `prompt` and `name`, omitting the required `command`, `fingerprint`, `topic`, and `watched_paths` arguments. That launcher mismatch would have raised a `TypeError` before any concept artifacts were produced.
  - Current run action: repaired the `evolve()` launcher contract and constrained child prompts to avoid recursive child-agent spawning.
  - Mandatory execution result on `2026-03-12`: the repaired `evolve` path launched successfully, but the first broad-task run produced no concept artifacts after several minutes and drifted across off-lane queries (oscillator synchronization, cryogenic blocks, generic cross-domain searches). Use a focused equivalent path for `item_006` and record the workaround in `results/concept_evolve/tooling_blockers.md`.
- `.archivara/rubric_tool.py`
  - Added in this run to make rubric state changes reproducible instead of hand-editing a 26-item JSON file.

### Research Context

- `results/research_context.md`
  - Human-readable execution log, inventory, and frozen working plan.
- `results/research_context.json`
  - Machine-readable snapshot of current stage, git state, literature counts, and rubric summary.

### Literature Artifacts

- `results/literature/literature_snapshot.json`
  - Preserved seed snapshot from the vague initial query; currently off-target and requires a focused H1 extension, not replacement.
- `results/literature/prior_art_watchlist.md`
  - Contains mostly false-neighbor papers from the seed query and must be explicitly differentiated rather than treated as topical prior art.
- `results/literature/prior_art_gap.md`
  - Running novelty ledger. Already records the oscillator-interleaving pivot; still needs dated H1 differentiation entries.
- `results/literature/novelty_guard.json`
  - Stores the polluted seed-watchlist guardrails and reminder questions.
- `results/literature/semantic_scholar_manifest.json`
  - Canonical memory of prior searches. Must be reused before widening queries.
- `results/literature/gap_frontier.md` and `results/literature/gap_frontier.json`
  - Frontier scaffold; currently thin and not sufficient by itself.
- `results/literature/literature_graph.json`
  - Saved Semantic Scholar graph from earlier exploration; useful for reuse but not yet focused on H1.
- `results/literature/gap_probe_*.json`
  - Earlier scouting probes behind the swarm shortlist.

### Swarm Artifacts

- `results/swarm/director_brief.md`
  - Highest-authority lane selection memo for the researcher: H1 champion, H2 backup, H3 reserve, plus the exact first experiment.
- `results/swarm/hypotheses.json`
  - Structured lane definitions, novelty claims, closest prior art, evidence plans, and lane-specific budget envelopes.
- `results/swarm/tool_plan.md`
  - Routing, lane budgets, kill rules, and role responsibilities for the run.
- `results/swarm/falsifier.md`
  - Adversarial constraints, benchmark traps, and weak-claim invalidators.
- `results/swarm/gap_map.md`
  - Explains why H1 is the most simulation-ready and why several decoy directions were deprioritized.
- Missing traceability artifacts:
  - `results/swarm/hypothesis_bridge.md`
  - `results/swarm/hypothesis_negative_space.md`

### Verification Artifacts

- `results/verification/*`
  - Directory exists but started empty. This run must create:
    - `novelty_report.md`
    - `benchmark_report.md`
    - `citation_audit.md`
    - `verification_summary.md`

## Artifact Data Flow

1. The original vague task string polluted the initial Semantic Scholar seed search, which then polluted `literature_snapshot.json`, `prior_art_watchlist.md`, and `novelty_guard.json`.
2. The swarm pass repaired the high-level direction using `gap_map.md`, `director_brief.md`, `hypotheses.json`, and `tool_plan.md`, selecting H1 as the active lane and explicitly deprioritizing the crowded/hype-prone branches.
3. The researcher phase must now:
   - repair the literature snapshot with targeted H1 evidence,
   - build `sources.bib`,
   - run `concept_evolve` on the now-frozen context,
   - choose a champion concept folder under `results/concept_evolve/tree/`,
   - implement baseline and champion netlists,
   - run bounded `ngspice` experiments,
   - and only then write verification artifacts under `results/verification/`.
4. `results/literature/semantic_scholar_manifest.json` is the anti-forgetting mechanism and should be treated as the memory of already-searched papers.

## Frozen Working Plan

### Lane Freeze

- Champion: `H1_multisource_cold_start`
  - Title: `Source-Adaptive Cold Start for Weak Multi-Source Harvesters Under Ultra-Slow Ramps`
- Backup: `H2_cryo_support_blocks`
  - Title: `Cryogenic Low-Frequency-Noise-Resilient Bias, Reference, Comparator, and ADC Support Blocks Below 10 K`
- Reserve: `H3_dynamic_source_impedance`
  - Title: `Dynamic-Source-Impedance-Aware Harvest Interfaces for Self-Powered Sensors`

### First Experiment To Preserve Verbatim In Spirit

- Run one go/kill `ngspice` cold-start matrix covering source voltages `20/50/100/300 mV`, ramp rates `0.1/1/10/100 mV/s`, impedance ratios `1:1/1:5/1:20`, and mixed-polarity cases.
- Report `startup success`, `time-to-handoff`, `back-drive loss`, and `startup-control energy`.
- Benchmark against two strong baselines:
  - a fixed startup path
  - a non-source-aware multi-input startup/arbitration path

### Global Governance And Budget

- Global governance rule: do not re-run broad searches. Spend literature budget only on blocker-driven or direct-overlap questions.
- Global blocker: `results/swarm/hypothesis_bridge.md` and `results/swarm/hypothesis_negative_space.md` are missing, so the H1 claim matrix must repair that traceability gap before heavy execution.
- Phase A budget: `~40 hours` total to decide whether H1 survives direct-overlap checking and one first `ngspice` evidence matrix.
- Phase B budget: `~24 hours` total only if H1 survives but stalls, or if H1 is killed after the prior-art gate.
- Phase C budget: `~16 hours` total only if H1 is killed and H2 is blocked on models.

### H1 Budget Envelope

- Literature gate: `1 focused pass, <=12 papers, no broad re-search`
- Simulation gate: `1 topology family, <=24 startup cases, 2 strong baselines`
- Promotion rule: `Promote if it survives the prior-art kill check and shows a clean startup-correctness advantage under mixed-source stress cases.`
- Kill rule: `Kill if novelty collapses to existing helper-free multi-source cold start, or if anti-backdrive/arbitration overhead dominates.`

### H2 Kill Rules

- `Kill if no credible cryogenic model path exists.`
- `Kill if the concept fails under widened low-frequency-noise, mismatch, and threshold-shift assumptions.`

### H3 Kill Rules

- `Kill if the 2025 variable-impedance overlap collapses the novelty margin.`
- `Kill if a simple hysteretic baseline matches the result once probe overhead is counted.`

## Phase 2 Bindings

- Tooling gate cleared:
  - repo-local `ngspice` is available through `./tools/setup_ngspice_local.sh` and `./tools/ngspice-local`.
- Canonical H1 implementation root:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root`
- Folder contract for all later H1 artifacts:
  - use `dependency_map.md` in the champion root as the source of truth for shared subcircuits, baselines, manifests, tables, and lane-local verification outputs.

## Phase 3 Selection Freeze

- Active H1 architecture:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/champion/packet_scout_handoff/variant_01_rc_ranked_packet_gate/rc_ranked_packet_gate.cir`
- Kill-ready H1 fallback:
  - `results/concept_evolve/tree/002_dual_bucket_polarity_split_bootstrap`
- Support-only H1 branches:
  - `003_time_constant_ranked_arbiter`
  - `005_tokenized_uvlo_handoff_gate`
- Branches retired from the architecture race:
  - `004_reverse_leakage_vote_or`
  - `006_comparatorless_current_probe_bootstrap`
- Rationale:
  - the packet-scout RC-ranked branch is the only active path that keeps the claim on helper-free, pre-arbitration source scouting
  - the dual-bucket branch is the only fallback that still opens a materially different mixed-polarity failure regime
  - `003` stays as the benchmark-line source-awareness control and `005` stays as a support block only if later adversarial cases expose chatter
  - `004` and `006` are no longer credible enough to keep in the active architecture race

## Immediate Execution Priorities

1. Run the mandatory `concept_evolve evolve` command against the user task, now that the launcher mismatch is repaired and the active lane is frozen.
2. Repair the literature snapshot around H1 with targeted Semantic Scholar traversals and narrow web checks.
3. Create `sources.bib` and keep it current.
4. Gate `ngspice` availability and concept-evolve command viability before baseline implementation.
