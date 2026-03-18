# H2 Gate

## Purpose

`H2_lag_space_ca_167` activates only if `H1_defect_syndrome_ca_64m` fails for principled locality reasons rather than weak implementation, unfair benchmarking, or missing controls.

This gate keeps H2 as a backup representation experiment, not as a default escape hatch.

## What Counts As A Principled H1 Locality Failure

H1 is allowed to open the H2 gate only if the evidence says the current q/s packet-locality premise is wrong on the canonical seed.

Qualifying evidence includes:

1. **Frozen local neighborhood**
   - `results/concept_evolve/probe_result.json` indicates that the current single-bit q/s packet basis has no improving one-packet or two-packet moves on the canonical seed.
   - A matched verification pass does not overturn that diagnosis.

2. **Diffusion-versus-paralysis bifurcation**
   - `results/branches/H1_frontier_micro_smoke.json` shows support diffusion under weaker spill control.
   - `results/branches/H1_frontier_sensitivity_probe.json` shows that stronger spill control keeps H1 pinned to the seed objective.
   - If matched frontier runs preserve that split, H1 has failed as a locality model rather than as a mere parameter choice.

3. **No frontier advantage under matched controls**
   - On the canonical seed and the locked benchmark contract, H1 shows no exact-hit advantage and no stable near-exact advantage over `greedy`, `tabu`, `simulated_annealing`, and `stochastic_hillclimb`.
   - The failure persists after a small, documented H1 sensitivity sweep inside the approved budget envelope.

4. **Locality metrics break**
   - Any H1 variant that looks competitive only after widening its sensed lag neighborhood, effectively scanning most packets each step, or relying mostly on exact per-packet global pressure should be treated as locality failure, not as H1 success.

## What Does Not Open H2

The following do **not** justify activating H2:

- H1 code bugs, crashes, or seed-loading mistakes
- missing matched baselines or broken accounting
- failure on toy controls alone
- a single bad H1 config with no sensitivity check
- apparent H1 weakness caused by an unfair budget, unfair restart policy, or broken exactness reporting

Those are implementation or benchmarking failures and must be fixed before any branch pivot.

## Family-Leakage Audit Required Before H2 Starts

H2 is only defensible if its lag-space state remains meaningfully different from search over known structured families.

Before any substantial H2 build-out, answer these checks explicitly:

1. **Williamson leakage**
   - Does the lag-space state or reconstruction enforce Williamson-type symmetry, supplementary-sequence constraints, or equivalent amicability conditions?

2. **Turyn leakage**
   - Does the coordinate system reduce to a Turyn or supplementary-sequence parameterization with a new move policy layered on top?

3. **Goethals-Seidel leakage**
   - Does H2 merely optimize over a pre-imposed Goethals-Seidel family description instead of using lag defects as the operative state?

4. **Cocyclic leakage**
   - For `668 = 4 * 167`, does the lag-space branch collapse into cocyclic or transposed-Ito style coordinates already known to be tightly constrained?

5. **Block-circulant leakage**
   - Are block-circulant, circulant, quasi-circulant, or compression constraints silently reintroduced to make the branch workable?

If the honest answer to any of these is "yes," then H2 is not a new CA branch. It must be relabeled as an optimizer over a known family.

## Activation Rule

Open H2 only if all of the following are true:

1. H1 is implemented, executable, and benchmarked fairly under `results/verification/benchmark_spec.md` and `results/verification/benchmark_gate.md`.
2. H1 fails on the canonical frontier seed for locality reasons, not because the implementation or benchmark scaffold was weak.
3. The H2 family-leakage audit above is completed and does not collapse H2 into Williamson, Turyn, Goethals-Seidel, cocyclic, or block-circulant search.
4. H2 remains in the same exactness-first evaluation regime: exact-hit rate is primary, near-exact improvements are diagnostic only.

If any of those conditions is missing, keep H2 closed.
