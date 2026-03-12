# H2 Pisot Backup Memo

## Trigger

The H1 screen leaves irrational survivors in the quadratic lane, so the backup was activated instead of being waived.

## Frozen construction used

The same construction was applied to all six test slopes:

- take every second convergent denominator `q_{2k}` of the slope,
- sample `x_k = floor(q_{2k} r)`,
- recover an exact recurrence from the first 12 samples,
- demand exact holdout survival on the first 20 samples.

This is the convergent/Hankel front-end frozen in `results/baseline/panel_spec.md` and implemented in `results/concept_evolve/tree/005_convergent_hankel_detector/experiment.py`.

## Exact success/failure certificates

| slope | type | fitted recurrence | holdout verdict | certificate artifact |
| --- | --- | --- | --- | --- |
| `phi` | Pisot quadratic | `x_k - 3 x_{k+1} + x_{k+2} = 0` | success on 20 exact samples | `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` |
| `1 + sqrt(2)` | Pisot quadratic | `x_k - 6 x_{k+1} + x_{k+2} = 0` | success on 20 exact samples | `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` |
| plastic constant | Pisot cubic | order-6 prefix relation | fails exactly at holdout window 6 | `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` |
| `sqrt(2)` | non-Pisot quadratic control | `x_k - 6 x_{k+1} + x_{k+2} = 0` | success on 20 exact samples | `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` |
| Salem quartic root | Salem control | order-6 prefix relation | fails exactly at holdout window 6 | `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` |
| `e` | transcendental control | order-6 prefix relation | fails exactly at holdout window 6 | `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` |

## Verdict

The strong H2 statement "Pisot slopes form the first clean irrational positive family" is not supported by the frozen convergent construction.

- It is **too weak** because the non-Pisot quadratic control `sqrt(2)` also survives.
- It is **too strong** because the higher-degree Pisot test case (plastic constant) fails while the quadratic cases survive.

The evidence therefore points to a **periodic-continued-fraction / quadratic mechanism**, not a broad Pisot mechanism, at least for this frozen construction.

## Consequence for the main claim

H2 remains useful only as a narrow falsifier lane: it helped rule out the tempting but unsupported narrative that higher-degree Pisot numbers generically rescue the problem. Any remaining positive story beyond rationals should now be phrased as a quadratic periodic-CF phenomenon unless the separate beta-endpoint experiment produces a new exact survivor.
