# Item 028: Border-Ordered Prefix Law

## Definition

For a step-`n` window, define `L_n` to be the smallest `L` such that every value in the window has at least one witness pair whose row factor lies among the last `L` row-border terms and whose column factor lies among the last `L` column-border terms present at step `n`.

This is a genuine border-ordered criterion: it measures how far back one must look in the actual mex-generated border order, not how dense the local product set is in the abstract.

## Counterfamily

The record windows themselves already kill any bounded-prefix explanation.

- Gap `20` at step `27676` has `L_n = 27675`.
- Gap `21` at step `29373` has `L_n = 29372`.
- Gap `25` at step `92320` has `L_n = 92319`.
- Gap `28` at step `247399` has `L_n = 247398`.
- Gap `30` at step `729353` has `L_n = 729352`.

## Proof-Backed Obstruction

The obstruction is the anchor value `c_n` inside each true row gap. Any representation of `c_n` present at step `n` must use the factor `1` on the row side:

1. `c_n` is not in `R_{n-1} C_{n-1}` by definition, because it is the second missing value of that snapshot.
2. A factorization `c_n = r_i c_j` with `j = n` forces `r_i = 1`, since `c_j = c_n` and any larger row factor would exceed `c_n`.
3. A factorization with `j < n` would already place `c_n` in `R_{n-1} C_{n-1}`, impossible.

Therefore the anchor value can only be covered by `1 * c_n`, so any recent-prefix law must look all the way back to the oldest row-border term. In the present definition this gives `L_n = n - 1` on every true record window through `10^6`.

## Consequence

No criterion of the form `L_n <= C log(gap)` can hold on the true record windows. The border-order direction therefore fails for structural reasons before any Ford-style density comparison is even needed.
