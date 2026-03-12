# Hypothesis Negative Space

Current exclusions are clear from the stored evidence. Do **not** recycle raw-witness
compression, prime-support causality, Ford-style divisor-window density, Beatty-style
polish, or pseudo-robustness from axis-swap variants. The next useful hypotheses have
to attack what the current package ignored, failed to test, or could not scale.

## 1. Modular Obstruction Lift

Direction: treat long first-row gaps as a possible residue-class locking phenomenon,
not as a prime-gap effect and not as a generic local product-density effect.
Hypothesis: if the difference sequence is unbounded, the scalable mechanism is a family
of moduli `q` for which the evolving border sets `R_n mod q` and `C_n mod q` fall into
persistent residue patterns whose product classes force long covered blocks before the
next `mex`.

Why this is negative-space:
- Current H1/H2 artifacts explain finished gaps locally after the fact, but they do
  not test whether record timing is driven by congruence structure upstream.
- Composite-only late records already rule out any story that needs skipped primes.

Fast test:
- Log `R_n mod q` and `C_n mod q` for `q <= 200` at record gaps and matched non-record
  windows.
- Search for moduli whose occupancy vectors remain deviant across scales.
- Re-run the same scan under one real admissibility perturbation; if the signal
  disappears instantly, it is not a viable obstruction family.

Angle to avoid: prime-support redux, residue heatmaps without a persistent modulus
family, or any argument that only restates local witness coverage in modular language.

## 2. Complementary Linearization Of The Paired-`mex` Backbone

Direction: separate the two-step border selection law from the multiplicative interior.
Hypothesis: boundedness, if true, is more likely to come from a low-memory
complementary backbone for `(r_n, c_n)` plus correction terms `Delta^R_n, Delta^C_n`
than from raw witness certificates. The hard question becomes whether those correction
terms stay bounded, structured, or sparse near new records.

Why this is negative-space:
- Prior work mostly treats the border sequences as outputs of product coverage.
- The current package has not directly modeled the paired-`mex` skeleton before the
  interior products are updated.

Fast test:
- Fit a low-order complementary model to `(r_n, c_n)` on an initial window.
- Compute the correction terms on a held-out window and around each late record gap.
- Check whether correction spikes have bounded memory or a stable numeration pattern,
  or whether they grow with the records themselves.

Angle to avoid: Beatty or almost-Beatty storytelling, uniform periodicity claims, or
one-dimensional prime-gap analogies. The point is the paired-`mex` correction process,
not a cosmetic reframing of the border sequences.

## 3. Mesoscopic Divisor-Profile Drift

Direction: stop demanding exact witness compression and instead model coarse arithmetic
state variables that can scale. Hypothesis: record-gap growth is governed by a drift in
bucketed divisor profiles such as smoothness, witness multiplicity, and
balanced-factor share. A fluid-limit model could distinguish a genuinely bounded local
gap regime from slow divergence that only looks bounded on current horizons.

Why this is negative-space:
- Exact witness and hypergraph data are informative but too heterogeneous to extrapolate
  directly.
- The late corpus already shows directional drift: tiny-factor explanations weaken
  while balanced-factor share increases.

Fast test:
- Bucket uncovered or skipped values by divisor-profile features at checkpoints such as
  `10^5`, `3 x 10^5`, and `10^6`.
- Fit bucket-level drift laws and forecast later record-gap statistics.
- Compare those forecasts against matched non-record windows and size-matched surrogate
  product sets/hypergraphs so the model does not collapse into Ford-style overlap.

Angle to avoid: uncalibrated curve fitting on record gaps alone, generic
divisor-density heuristics, or any scaling story that lacks surrogate controls.
