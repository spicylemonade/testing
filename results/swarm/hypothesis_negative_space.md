# Hypothesis Negative Space: Hadamard 668 After the Flat-CA No-Go

## Context

- `results/literature/gap_frontier.md` is effectively empty, so the next frontier has to come from the repo's own failed-branch evidence rather than another broad survey.
- `H1` support-space CA and `H2` flat defect-transport CA are already retired under matched baselines. Spending more budget on those families would be derivative.
- The phrase `cellar automata` is too unstable to carry novelty on its own. The only defensible use here is a literal memory-bearing automaton over structured Hadamard search states, not another homogeneous cellular rule.

## Families To Avoid Repeating

- Raw support-space CA or density-classifier repairs on weight-`80` subsets of `Z_167`.
- Flat modular-seed defect transport, CA-annealer hybrids, or other `H2` restarts with the same information channel.
- Generic `GS` / `Williamson` / `SDS` / `SAT+CAS` / annealing packaging with an automata label on top.
- Reservoir or neural-CA variants that are farther from the exact `167/80` obstruction than the reserve branches already in the repo.

## 1. Canonical-Path Cellar Automaton With Deferred Autocorrelation Debt

- Gap attacked:
  Prior work sharpens order `668` to the exact `167/80` cyclic obstruction, but search procedures still mostly act on raw bits, static clauses, or family parameters instead of a canonical orbit word with explicit deferred debt.
- Core idea:
  Canonicalize each weight-`80` support in `Z_167` to its unique orbit representative, encode it as run-length or path tokens, and let a pushdown-style automaton track `(position, used weight, parity debt, local debt)` plus a stack of multiscale autocorrelation deficits.
- Why this is negative-space:
  The search object stops being "a score on a raw support" and becomes "an auditable prefix with a completion certificate." That is materially different from the retired local CA loops.
- First discriminator:
  Keep every known smaller same-template witness alive, reject most random prefixes by mid-depth, and beat a matched non-automaton prefix search that uses the same canonicalization and the same exact-completion oracle.
- Derivative overlap to watch:
  Canonicalization alone can look strong. If the gain comes only from symmetry quotienting or compression, this collapses into ordinary branch-and-bound.
- Angle to avoid:
  Do not sell static prefix pruning or `SAT+CAS` preprocessing as `cellar automata`. The stack state has to add information that the comparator does not already have.

## 2. Proof-Carrying Cellar Frontier With Online Exact-Feedback Motifs

- Gap attacked:
  Exact Hadamard searches usually treat failed completions as terminal verdicts. They do not recycle those failures into reusable local transition guards for later frontier growth.
- Core idea:
  Wrap Direction 1 around a small exact completion oracle. When a frontier state fails, convert the failure into short forbidden motifs, stack-transition vetoes, or weighted penalties that update later automaton transitions online.
- Why this is negative-space:
  It tests an adaptive exact-feedback loop that the repo has not executed and that standard exact-search work usually leaves implicit inside static encodings.
- First discriminator:
  On solved same-template controls, show fewer oracle calls at fixed witness retention than the static pushdown filter.
- Derivative overlap to watch:
  If conflicts stay global, nonlocal, or unreusable, this is only `SAT+CAS` with extra plumbing.
- Angle to avoid:
  Do not count clause learning by itself as the method. The contribution only survives if exact feedback becomes short, reusable automaton-state updates.

## 3. Hierarchical Defect-Memory Decoder On The `64`-Modular `668` Seed

- Gap attacked:
  The seed-side line already has a strong near-solution, but the repo only tested flat local defect transport there, and that tied the matched non-CA baseline. What remains untested is multiscale memory on the seed's sparse defect pattern.
- Core idea:
  Build a coarse-to-fine defect pyramid on the published `64`-modular order-`668` seed. Each level stores deferred defect mass for one block scale, passes repair requests downward, and proposes only those local flips that support cross-scale cancellations. Require a small-order controllability check before any real `668` run.
- Why this is negative-space:
  The state is no longer "current row flips plus local score." It is a hierarchy of defect syndromes with explicit memory, which is the missing ingredient in the retired `H2` branch.
- First discriminator:
  On injected-defect exact Hadamards and smaller modular controls, beat flat greedy and flat CA under the same neighborhood and move budget. Only then spend any budget on whether the real seed can improve beyond modulus `64` or reduce defect count.
- Derivative overlap to watch:
  If the hierarchy adds no benefit beyond seed privilege or merely reweights the same flip schedule, this is just `H2` rebranding.
- Angle to avoid:
  Do not rerun flat defect transport, CA-annealer hybrids, or unfair start-cold baselines. No credit without same-seed, same-neighborhood fairness and an ablation showing the hierarchy matters.

## Recommended Order

1. Start with Direction 1. It is the cleanest literal reading of `cellar automata` and the sharpest test against the exact `167/80` obstruction.
2. Promote Direction 2 only if Direction 1 keeps positive controls but still pays too much exact-oracle cost.
3. Touch Direction 3 only if the team still wants a seed-side branch after the repo's flat `H2` no-go.

## Not Selected Now

- `learned_prefix_automaton` stays on hold until Direction 1 exists as a clean teacher. Right now the transfer-risk story is too weak.
- `convolution_slice_ca` stays secondary reserve only. It is still one step away from relabeling the failed `H1` search space.
- `density_classifier_support_repair`, `defect_transport_mod64_lift`, `ising_ca_hybrid_annealer`, and `reservoir_defect_readout` stay retired.

## Kill Rules

- Kill any branch whose advantage disappears against a matched comparator on the same representation.
- Kill any branch that cannot keep same-template positive controls alive.
- Kill any branch that drifts back into `GS` / `Williamson` / `SAT+CAS` packaging or generic local search with automata branding.
- Kill any branch that reports only heuristic score improvement rather than exact witness retention, exact completability, or verified modulus lift.
