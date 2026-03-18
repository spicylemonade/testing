# H3 Gate

`H3_spacetime_row_emission_ca` stays reserve-only. It is more exposed to prior CA-construction overlap than H1 or H2 and should not consume serious budget unless the earlier branches fail for representation reasons.

## Activation Rule

Do not open H3 unless both of these are true:

1. H1 fails for principled locality reasons rather than weak implementation.
2. H2 is either not opened because of immediate family leakage, or H2 also fails for representation reasons rather than simple tuning debt.

If H1 or H2 still look like viable branches under the locked benchmark rules, keep H3 closed.

## Tight Exploratory Budget

If H3 opens, the budget is intentionally small:

1. One short exploratory pass only.
2. Radius limited to a narrow family such as radius-`1` or radius-`2`.
3. No broad Wolfram-style rule-table sweeps.
4. No large random search over rule/seed pairs.
5. No claim of a live branch unless H3 first shows frontier-relevant behavior on a sharply reduced pilot.

H3 is allowed only enough budget to test whether the idea is structurally mismatched, not enough budget to become a sprawling separate program.

## Required Overlap Check Before Any Build-Out

Before writing substantial H3 code or running a serious sweep, explicitly check overlap against the direct CA-construction literature already noted in the repo:

1. **Linear bipermutive CA constructions**
   - If the useful rules are linear, bipermutive, or finite-field constructive in the usual way, H3 has likely collapsed into known CA-construction territory.

2. **CA-derived bent-function / Hadamard-adjacent pipelines**
   - If the route goes through bent functions, mutually unbiased bases, orthogonal arrays, or orthogonal Latin-square constructions, relabel the branch as prior-art overlap rather than as a new order-668 direction.

3. **Compact rule-table generative search**
   - If H3 is just brute-force or black-box search over a large local rule table, stop. The branch is only defensible if the rule family is tiny and the order-668 relevance is explicit.

4. **Power-of-two or prime-power constructive bias**
   - If the rules only reproduce the power-of-two / prime-power regimes where prior CA constructions are already strongest, H3 is mismatched to the `167` prime core behind order `668`.

## Immediate Stop Conditions

Stop H3 immediately if any of the following happens:

1. The first useful rules are linear or bipermutive in a way already covered by the known CA-construction literature.
2. The search requires enumerating many rules or seeds to get any Hadamard-adjacent behavior.
3. The branch cannot even imitate the qualitative defect profile of the recovered 64-modular order-668 seed.
4. The branch drifts into a construction story for other orders or other regimes instead of the real order-668 bottleneck.

## Decision Rule

- `keep H3 closed`: default.
- `open H3 briefly`: only after H1 and H2 fail for representation reasons and the overlap check above stays clean.
- `stop H3`: immediately if it starts looking like direct CA-construction prior art or wide brute-force rule search.

## Evidence Artifacts To Check First

- `results/swarm/hypotheses.json`
- `results/swarm/falsifier.md`
- `results/swarm/hypothesis_negative_space.md`
- `results/swarm/hypothesis_bridge.md`
- `results/literature/code_watchlist.md`
- `results/literature/prior_art_gap.md`
