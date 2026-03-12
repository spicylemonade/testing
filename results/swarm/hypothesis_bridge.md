# Cross-Domain Bridge Hypotheses

Inspected `results/research_context.md` and `results/literature/gap_frontier.md` first. `results/swarm/director_brief.md` was absent, and no ConceptEvolve artifacts were present in the repository. Local computation on the first 20,000 terms suggests `R(x) := #{n : T(1,n) <= x}` and `C(x) := #{n : T(n,1) <= x}` are both close to `2x/log x`, while the observed row-1 gap record has already reached `19`, so the bounded-gap conjecture currently looks more likely false than true.

## 1. Greedy Extremal Multiplicative-Basis Hypothesis

- **Title:** Canonical Near-Minimal Multiplicative Basis via Greedy Mex Coupling
- **Closest prior art:** Multiplicative bases of order `2` and the Erdős multiplication-table problem.
- **Why it is different:** Existing work studies how small a multiplicative basis can be or how many distinct products appear. Here the novelty is the deterministic `mex` coupling: the table is not an arbitrary basis but a canonically generated one, and the bridge claim is that this greedy rule forces a specific near-extremal regime rather than merely some sparse covering set.
- **Falsifiable prediction:** If `A = {T(1,n)}` and `B = {T(n,1)}`, then `R(x) ~ 2x/log x` and `C(x) ~ 2x/log x`, and the row-1 difference sequence is unbounded. More sharply, record row gaps should occur at locations where the local product-coverage multiplicity from `A(x)B(x)` is unusually high, so the same local obstruction explains both the near-minimal density and the large gap.
- **Required experiments:** Generate at least `10^6` terms with incremental product coverage; estimate `R(x)log x/(2x)` and `C(x)log x/(2x)` over logarithmic windows; for each new record row gap, log local coverage multiplicities and compare them against synthetic near-minimal multiplicative bases. Reject this bridge if the counting law looks right but record gaps do not line up with any extremal-coverage witness.

## 2. T-Specific Buchstab/Kinetic Frontier Hypothesis

- **Title:** The Mex Frontier Has a Buchstab-Type Scaling Fixed Point
- **Closest prior art:** Buchstab-style rough-number asymptotics and Smoluchowski-type kinetic fixed points.
- **Why it is different:** This is not the generic statement that `A` or `B` look like rough numbers. The claim is that the `mex` evolution induces its own nonlinear frontier operator on uncovered integers, and only after rescaling does that operator land in the same universality class as Buchstab/kinetic equations. The table-specific object is the frontier dynamics, not the eventual asymptotic shape alone.
- **Falsifiable prediction:** On logarithmic scales, the uncovered-frontier profile converges to a stable shape. Consequently, `R(x) = C(x) = (2 + o(1))x/log x`, and the mean row-1 gap near index `n` is `(1/2 + o(1)) log n`. If successive dyadic windows fail to approach a common rescaled profile, or if the mean-gap-to-`log n` ratio drifts without stabilization, this hypothesis should be discarded.
- **Required experiments:** Measure uncovered-frontier statistics on dyadic windows; fit a nonlinear renewal or delay equation directly to the observed frontier; track the mean row gap, upper gap quantiles, and `R(x)` against the predicted scaling law. Reject quickly if no scale-stable profile emerges.

## 3. Divisor-Lattice Twin-Front Hypothesis

- **Title:** Row and Column Are Coupled Fronts in a Deterministic Divisor-Lattice Growth Model
- **Closest prior art:** First-passage percolation / Eden-type growth models and exploration processes on divisor graphs.
- **Why it is different:** A standard symbolic-dynamics or `B`-free framing is too derivative here. The sharper bridge is to deterministic front propagation: `A` and `B` are two advancing fronts, while product-covered integers form the explored interior of a growth process on the divisibility lattice. That creates a coupled two-front geometry absent from fixed forbidden-divisor models.
- **Falsifiable prediction:** The row and column stay near-twins even while row gaps diverge: `T(n,1) - T(1,n) = O(log n)` in maximum and has prefix-average growth at most polylogarithmic, while record row gaps correlate with spikes in divisor richness or local collision multiplicity. Thus unbounded row gaps come from frontier trapping, not from row/column decoupling.
- **Required experiments:** Log `T(n,1) - T(1,n)`, row-gap records, divisor counts `tau(m)`, and local collision multiplicities around each record gap; test whether record gaps concentrate near unusually divisor-rich zones; compare the observed statistics with a deterministic growth surrogate on the divisor graph. Reject this bridge if row/column offsets scale comparably to the row-gap records themselves.
