# Tool Plan

## Guardrails

- Stay on the two active lines only:
  - `H1_frontier_witness_certificate`
  - `H2_prime_support_fixed_point`
- Do not widen into generic mex, prime-gap, or multiplication-table storytelling unless a blocker forces targeted prior-art clearance.
- Every computational claim must carry proof-oriented artifacts:
  - witness logs for skipped integers in record gaps;
  - recurrence-order validation;
  - compact claim-to-evidence mapping.
- Cap robustness work at two meaningful perturbations. Do not create a variant zoo.

## Role Routing

| Role | Tool routing | Expected output | Budget envelope |
|---|---|---|---|
| Orchestrator | Repo artifacts and shell first. Spawn at most one parallel review round if needed. Use web only for blocker-driven provenance checks. | One-page decision memo that keeps `H1` primary and `H2` backup unless a blocker reverses them. | 2-3 hours human. No broad search budget. |
| Researcher | Existing local scripts, shell, and repository data only. If no correct baseline generator exists, stop and file that exact blocker before building anything else. | One witness-carrying record-gap corpus and two short claim sheets: frontier certificate claim and prime-support claim. | 4-6 hours human plus one bounded benchmark pass. No theorem search and no side explorations. |
| Falsifier | Local artifact review plus targeted attacks on the active claims. No new hypothesis families. | Pass/fail checklist covering prime-free record gaps, brittle single-witness coverage, stale small-horizon claims, and recurrence-order mistakes. | 4-5 hours human. Stop after one decisive failure per claim or three failed rescue attempts. |
| Writer | Work from the claim sheets and falsifier outputs only. No new research. | Compact note organized as `claim -> required evidence -> current status -> blocker`. | 2-3 hours human, 2-3 pages max. |
| Reviewer | Review only the active claims and their evidence package. No reopening of the full search space. | Go/no-go review focused on overclaim, novelty overlap, and missing controls. | 1.5-2 hours human. |
| Citation auditor | Targeted provenance check only. Local notes first, then exact sources if needed. | Source map covering OEIS array/row provenance, bounded-difference statement, Kimberling baseline, and Ford only if divisor-interval language appears. | 1-2 hours human. No bibliography growth beyond blocker-driven sources. |
| Benchmark auditor | Validate one correct baseline, one witness-log format, and at most two ablations. Use shell plus existing helper scripts only. | Benchmark spec with stress metrics: record-gap trajectory, skipped-prime composition, witness multiplicity profile, and row/column offset sanity check. | 3-4 hours human, up to 8 CPU-hours. Reject any run without witness logs or recurrence-order validation. |

## Minimal Sequence

1. Orchestrator locks the claim ladder: `H1` first, `H2` second, `H3` out of scope.
2. Benchmark auditor defines the baseline generator contract, witness-log schema, and two allowed ablations.
3. Researcher and falsifier run in parallel on that contract.
4. Writer, reviewer, and citation auditor engage only if the evidence package clears the falsifier bar.

## Stop Conditions

- Stop immediately if the baseline recurrence implementation cannot be validated.
- Stop the champion line if witness logs do not yield a compact certificate language or obstruction.
- Promote the backup only if prime-support observables explain failures that frontier witnesses do not.
- Do not spend budget on broader literature or extra variants until one active line survives the above filters.
