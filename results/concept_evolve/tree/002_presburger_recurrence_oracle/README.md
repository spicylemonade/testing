# Presburger Recurrence Oracle

## Topic context
Automatic theorem provers already decide rich theories of Sturmian and Beatty structures in special cases. This card repackages the special numbers problem as a family of first-order search and decision tasks so that conjectures about exact recurrence orders can be machine-generated rather than hand-guessed.

This concept targets the problem of characterizing real numbers r for which the Beatty sequence floor(n*r) contains a homogeneous linearly recurrent subsequence.

## Mathematical sketch
In a structure M_r extending (N,+,<) with a predicate or function for floor(n*r), express formulas of the form: there exist d, c_0,...,c_d, and an increasing selector n_k such that y_k = floor(r*n_k) and sum_{i=0}^d c_i*y_{k+i} = 0. For quadratic r, use an Ostrowski-synchronized presentation; for tame axiomatized Beatty expansions, use the model-complete presentations when available.

## Cross-domain analogies
- Use a theorem prover as a wind tunnel for recurrence templates.
- Turn a subsequence classification question into a satisfiability landscape.
- Treat recurrence certificates as machine-checkable proofs rather than hand-constructed examples.

## Novel move
The novelty is the workflow: decidable Beatty theories become an experimental oracle for the subsequence problem, not just a source of ambient structure theorems.

## Why this is not just a reimplementation
Prior logic papers prove decidability of whole structures. This card uses that decidability to enumerate, accept, and reject candidate recurrence patterns in the specific Beatty subsequence problem.

## Implementation backlog
1. Translate the mathematical sketch into a concrete prototype: Generate formulas for fixed d, coefficient tuples, and selector schemas, then feed them to Walnut or Pecan on decidable Beatty or Sturmian presentations. Cache UNSAT templates to build a forbidden-pattern atlas and SAT templates to recover explicit examples.
2. Run the first experiment: Run the oracle first on the golden ratio and silver ratio, then compare with a transcendental-axiomatized Beatty case. The expected output is a template table separating easy rational or quadratic cases from apparently structureless ones.
3. Compare the observed patterns against the closest prior art and record where the new bridge adds information.

## Literature anchors
- Decidability for Sturmian words (9db8fdff7bca15077834c62d6051340e5e06180b, 2021, Annual Conference for Computer Science Logic): Core result showing first-order decidability for Sturmian words over Presburger arithmetic.
- Ostrowski-automatic sequences: Theory and applications (60d51405e92dd39f0836d04dbbe88f5904b094b3, 2021, Theoretical Computer Science): Gives addition and automata tools in Ostrowski numeration.
- Expansions of the group of integers by Beatty sequences (71157b4e3492593ee91953f91f660c81f13b388c, 2020, Annals of Pure and Applied Logic): Supplies quantifier-elimination style context for Beatty predicates over integers.
- Model-completeness and decidability of the additive structure of integers expanded with a function for a Beatty sequence (e2ab0ff0760958d37dcde2ddb5292d9784a74f0b, 2021, Annals of Pure and Applied Logic): Shows that some Beatty-function expansions admit complete recursive theories.

