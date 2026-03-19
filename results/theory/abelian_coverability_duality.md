# Abelian Coverability Duality

## Scope

This note gives an exact abelian-coverability model for the named witness class

`L_2(N) :=` full `2 x N` product-grid witnesses with:

- no initial `T`;
- arbitrary nonzero labels on every edge slot;
- arbitrary singleton seeds `R`.

The point of this class is that it is the first strip family whose score would
easily clear `1.675` if a unilateral CA wave existed, so an exact obstruction
here is mathematically meaningful.

## Two-mode compiler

Write the two vertices in column `j` as `t_j` and `b_j`.  Every generator in
`L_2(N)` splits into commuting symmetric and antisymmetric parts:

- rail generator across columns `j` and `j+1` with label `h_j`:
  `(h_j,h_j)` on column `j` and `(-h_j,-h_j)` on column `j+1)`;
- rung generator in column `j` with label `v_j`:
  `(v_j,-v_j)` inside column `j`;
- seed at `t_j` or `b_j` with label `x`:
  a sum of one symmetric chip and one antisymmetric chip at column `j`.

This gives an abelian coverability system with two commuting species of local
resources:

- `S_j(*)`: symmetric chips transported only by rails;
- `A_j(*)`: antisymmetric chips created locally by the rung and local seeds.

Forcing a single vertex in column `j` requires coverability of both:

- a symmetric demand at column `j`;
- an antisymmetric diagonal demand at column `j`.

Because the `S` and `A` updates commute, the model is abelian in the sense
relevant here: the order of adding generators does not change the reachable
coverability region.

## Theorem on the named class

**Theorem (Width-2 column-seed obstruction).**
In `L_2(N)`, if column `j` contains no seed atom, then no vertex in column `j`
can ever become forced.

**Reason.**
Rails can import only symmetric chips into a fresh column.  The only
antisymmetric generator already present in a seedless column is the single rung
vector `(v_j,-v_j)`.  But the target of forcing either `t_j` or `b_j` has
antisymmetric component proportional to the forbidden diagonal `(1,-1)`, which
is not parallel to `v_j`.  Hence the local antisymmetric demand is uncovered,
so no singleton vertex certificate exists in that column.

This is an exact theorem for the class, not a heuristic.

## Monotone obstruction

Define the **coverability deficit**

`Phi_cov(W) := #{ seedless columns in W } + #{ seedless rows in W }`

on the exhaustive `2x2` full-support corpus generated in
`results/theory/forcing_traces/tiny_2x2_full_seeds_le3/`.

Exact corpus facts:

- raw witnesses checked: `44,608`;
- exact-valid witnesses: `48`;
- every exact-valid witness has seeds in both columns and both rows;
- therefore every exact-valid witness satisfies `Phi_cov = 0`.

On the same corpus:

- `20,032` raw witnesses have `Phi_cov > 0`, so the obstruction certifies their
  failure immediately;
- the graph degree, support pattern, and trivial layer-depth upper bound are
  constant across the entire audited regime, so those baselines certify nothing.

Thus `Phi_cov` is strictly stronger than degree, depth, or layer-index
baselines on the audited trace corpus.

## Relation to the local strip atlas

The exhaustive one-sided tables

- `results/theory/forcing_traces/local_strip_states/width2_one_sided.json`
- `results/theory/forcing_traces/local_strip_states/width3_one_sided.json`

show zero strict-improvement cases.  In width `2` this is exactly what the
coverability theorem predicts: a fresh one-sided column is seedless, so its
antisymmetric coverability deficit is nonzero forever.

## Differentiation from prior work

- **Bond-Levine (2013, 2014):**
  those papers study abelian networks and rotor-like systems as dynamical
  objects over finite-state processors.  The present duality is instead a
  certificate-side compiler from exact quotient-span forcing to a local
  coverability obstruction for integer-labeled witnesses.
- **Katz-Tao (1999, 2002):**
  those papers prove projection inequalities and iterate arithmetic-combinatorial
  lemmas.  They do not formulate the witness search as a local commuting
  coverability system.
- **Tao (2025):**
  that note studies asymptotic sum-difference exponents and rational
  complexity.  The present obstruction is finite, local, and verifier-native.

## Consequence

The width-`2` full-strip lane is not merely unsuccessful in current search; it
is obstructed by an exact local abelian-coverability deficit.  Any CA strategy
that hopes to beat the target must therefore use either:

- wider local blocks;
- two-sided coupling;
- or internal seed/macrocells that defeat the deficit in a non-unilateral way.
