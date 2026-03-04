# ConceptEvolve Steering Notes

## Three Concrete Steering Directions

### Direction 1: OEIS A284668 New Term Computation (PRIORITIZED)
**Description:** Compute new terms of OEIS sequence A284668 (number below 10^n with highest Collatz stopping time). The sequence has limited known terms. Computing a new term (e.g., a(19) or beyond a(18)) would be a concrete, verifiable, tweetable new record.

**Rubric items informed:** item_006, item_007, item_008, item_011, item_012, item_015, item_016, item_017, item_021, item_022, item_023

**Why prioritized:** This direction produces a single, unambiguous "new record" number that anyone can verify with a 5-line Python script. It's the most hype-worthy outcome: "We computed the Nth term of this OEIS sequence that no one has computed before." The verification is trivially deterministic. It also exercises all our implementation modules (sieve, shortcuts, parallel computation) in service of a concrete goal.

### Direction 2: Entropy-Guided Binary Template Sieve for Delay Records
**Description:** Use Shannon entropy of parity sequences to create a discriminative sieve that targets high-delay candidates. Combine information-theoretic trajectory analysis with modular arithmetic sieves to achieve ~1000x speedup over brute force.

**Rubric items informed:** item_005, item_008, item_011, item_013, item_014, item_016

**Rationale:** This is the novel algorithmic contribution. If >90% of known delay records fall within the top 0.1% of the entropy ranking of residue classes, this would be a publishable algorithmic innovation beyond just a new number.

### Direction 3: Extreme Value Theory Analysis of Delay Record Gaps
**Description:** Fit GEV/Generalized Pareto distributions to the 147 known delay record gap ratios. Predict where the next delay record should appear with confidence intervals.

**Rubric items informed:** item_002, item_013, item_014, item_019, item_020

**Rationale:** This adds mathematical depth and predictive power to complement the computational search. It connects Collatz computation to well-understood statistical theory and produces publishable figures.

## Priority Ranking
1. **Direction 1** (OEIS new term) - primary goal, determines success/failure of the project
2. **Direction 2** (entropy sieve) - novel technique enabling Direction 1 
3. **Direction 3** (EVT analysis) - adds depth to the paper/analysis
