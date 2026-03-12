# Verification Summary

## Status Label

**still unresolved**

## Justification

The current package settles the computational baseline, not the mathematics.

- The validated million-step run extends the record-gap trajectory from the old `21`
  horizon to new records `25`, `28`, and `30`.
- The `column_immediate` perturbation reaches `31`, so the package clearly does not
  support any small bounded-difference narrative.
- But every experiment remains finite-horizon. No theorem in the repo upgrades those
  records into an unboundedness proof, and no witness invariant upgrades them into a
  global upper bound.
- The active mechanism claims also weaken rather than strengthen:
  - the original H1 mechanism claim is rejected; only a narrowed hypergraph-rescue
    question remains open;
  - H2 is killed as non-explanatory.

Therefore the honest synthesis is neither `boundedness supported` nor `boundedness
refuted`, but `still unresolved`.

## Minimum Remaining Blockers

- A horizon-independent invariant or certificate extracted from the witness/hypergraph
  data that would imply a genuine global bound, or rule one out.
- A proof bridge from the measured observables to asymptotic behavior; finite record-gap
  growth alone is not enough.
- A decisive compression result on the full witness hypergraphs, if the narrowed
  hypergraph-rescue question is to remain open at all.

## Overclaim Boundary

The package may claim stronger validated evidence and stronger negative mechanism
results. It may **not** claim a proof or disproof of boundedness from the current
artifacts.

## Sources

See `results/verification/claim_source_matrix.md` and `sources.bib`.
