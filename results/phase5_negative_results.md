# Negative Results And Pivot Log

Date: 2026-03-18

## H1 Macrocell Substitution

- Status: killed
- Pivot / kill reason:
  - exact one-seed obstruction
  - no initial solved vertices
  - exact verification fails before any level-1 versus level-2 score comparison
- Falsifier criterion fired:
  - the route never produced a genuine second-label bootstrap start and never reached a real transfer test

## H2 Target-Direction Abelian

- Status: killed
- Pivot / kill reason:
  - activated only after H1 failure
  - invariant package added no screening value beyond raw support size, rank, and target-solvable counts on the same family IDs
- Falsifier criterion fired:
  - “abelian” language was only a relabeling of direct arithmetic descriptors

## Direct Corridor Residual

- Status: survives only as a finite-size control
- Best exact scores:
  - `2.0` on `2 x 4`
  - `2.0` on `2 x 6`
  - `29/14` on exploratory `2 x 8`
- Failure mode:
  - boundary-sensitive
  - not robust under `R` / `T` perturbation
  - not scale-stable under frozen `X`
  - still in the tiny fixed-`X` corridor regime highlighted by the bounded-slope / rational-complexity warning literature

## H3 Slope Bloom

- Status: not activated
- Reason:
  - kept as reserve only
  - the current run already delivered a clean finite-size negative result for H1 and H2 without evidence that widening to H3 would meet the novelty or benchmark bars
