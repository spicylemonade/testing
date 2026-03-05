# Fractional Ramsey Theory

## Concept
Fractional Ramsey Theory relaxes the discrete boolean requirement of edge coloring into a continuous probability distribution of colors. Instead of a single graph avoiding $K_5$, we assign weights to all graphs on $N$ vertices avoiding $K_5$, such that the marginal probability of any edge being red or blue is bounded.

## Analogical Connection
This acts similarly to the fractional relaxation of linear programming in combinatorial optimization. By solving the continuous problem, we can find continuous bounds, which then might be rounded using randomized techniques or Lovász Local Lemma.

## Next Steps
- Implement fractional LP formulations for $N=42..46$.
- Check if the continuous bound is strictly less than 46.
