# Witness Taxonomy

This node audits whether the skipped values in record gaps can be compressed into a
small reusable family of witness types.

The active baseline evidence points the other way: late record gaps are dominated by
singleton witnesses, the tiny-factor share decays with scale, and the only clearly
endogenous motif is the single `1 * previous_column_term` marker inside the gap.
