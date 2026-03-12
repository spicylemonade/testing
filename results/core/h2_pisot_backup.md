# H2 Pisot Backup Memo

## Trigger

The H1 screen leaves irrational survivors in the sparse quadratic lane, so the backup was activated instead of being waived.

## Frozen construction used

The same construction was applied to all six test slopes:

- take every second convergent denominator `q_{2k}` of the slope,
- sample `x_k = floor(q_{2k} r)`,
- search only recurrence orders `d <= 4` from the frozen panel on the first 12 samples,
- demand exact holdout survival on the first 20 samples.

This is the convergent/Hankel front-end frozen in `results/baseline/panel_spec.md` and implemented in `results/concept_evolve/tree/005_convergent_hankel_detector/experiment.py`.

## Exact success/failure certificates

| slope | type | fitted recurrence | holdout verdict | certificate artifact |
| --- | --- | --- | --- | --- |
| `phi` | Pisot quadratic | `x_k - 3 x_{k+1} + x_{k+2} = 0` | success on 20 exact samples | `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` |
| `1 + sqrt(2)` | Pisot quadratic | `x_k - 6 x_{k+1} + x_{k+2} = 0` | success on 20 exact samples | `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` |
| plastic constant | Pisot cubic | no order-`<=4` recurrence | failure | `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` |
| `sqrt(2)` | non-Pisot quadratic control | `x_k - 6 x_{k+1} + x_{k+2} = 0` | success on 20 exact samples | `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` |
| Salem quartic root | Salem control | no order-`<=4` recurrence | failure | `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` |
| `e` | transcendental control | no order-`<=4` recurrence | failure | `results/concept_evolve/tree/005_convergent_hankel_detector/results.json` |

## Verdict

The strong H2 statement "Pisot slopes form the first clean irrational positive family" is not supported by the frozen convergent construction.

- It is **too weak** because the non-Pisot quadratic control `sqrt(2)` also survives.
- It is **too strong** because the higher-degree Pisot test case (plastic constant) fails while the quadratic cases survive.
- The revision holdout follow-up removes the strongest nonquadratic sparse anomaly (`salem_quartic / ost_suffix_001`), but the remaining sparse survivors still lack infinite certificates.

The frozen construction therefore leaves a narrow empirical survivor set confined to quadratic slopes, not a proved Pisot or quadratic family boundary.

## Consequence for the main claim

H2 remains useful only as a falsifier lane: it rules out the tempting but unsupported story that higher-degree Pisot numbers generically rescue the problem.

- The only safe positive statements beyond rationals are the four certified `quadratic_convergent_even` identities.
- Any broader sparse narrative remains empirical until intercept controls, prefix-matched nonquadratic controls, and structural certificates for the surviving leaks are added.
