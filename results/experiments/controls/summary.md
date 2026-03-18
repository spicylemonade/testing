# Control Experiment Summary

Matched control batch over two deterministic q0-flip seeds (`n=5` and `n=7`) with shared budget `80`, restart count `3`, and RNG seed `17`.

Method-level results:

- `H1_defect_syndrome_ca_64m`: exact-hit rate `1.00`, median defect reduction `2.5`, variance `0.25`
- `greedy`: exact-hit rate `1.00`, median defect reduction `2.5`, variance `0.25`
- `simulated_annealing`: exact-hit rate `0.50`, median defect reduction `2.0`, variance `0.00`
- `stochastic_hillclimb`: exact-hit rate `0.50`, median defect reduction `2.0`, variance `0.00`
- `tabu`: exact-hit rate `1.00`, median defect reduction `2.5`, variance `0.25`

Per-run results:

- `control_n5_q0:H1_defect_syndrome_ca_64m`: exact_hit `True`, reduction `2`, terminal support `0`, max defect `0`, evaluations `10`
- `control_n5_q0:greedy`: exact_hit `True`, reduction `2`, terminal support `0`, max defect `0`, evaluations `34`
- `control_n5_q0:simulated_annealing`: exact_hit `True`, reduction `2`, terminal support `0`, max defect `0`, evaluations `46`
- `control_n5_q0:stochastic_hillclimb`: exact_hit `True`, reduction `2`, terminal support `0`, max defect `0`, evaluations `18`
- `control_n5_q0:tabu`: exact_hit `True`, reduction `2`, terminal support `0`, max defect `0`, evaluations `80`
- `control_n7_q0:H1_defect_syndrome_ca_64m`: exact_hit `True`, reduction `3`, terminal support `0`, max defect `0`, evaluations `15`
- `control_n7_q0:greedy`: exact_hit `True`, reduction `3`, terminal support `0`, max defect `0`, evaluations `74`
- `control_n7_q0:simulated_annealing`: exact_hit `False`, reduction `2`, terminal support `1`, max defect `4`, evaluations `80`
- `control_n7_q0:stochastic_hillclimb`: exact_hit `False`, reduction `2`, terminal support `1`, max defect `4`, evaluations `31`
- `control_n7_q0:tabu`: exact_hit `True`, reduction `3`, terminal support `0`, max defect `0`, evaluations `74`
