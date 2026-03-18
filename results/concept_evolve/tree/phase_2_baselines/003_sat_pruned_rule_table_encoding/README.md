# SAT-Pruned Rule-Table Encoding

Status: secondary candidate

## Source Inspiration

- `results/concept_evolve/tree/009_sat_pruned_local_rule_synthesis/concept.json`
- `results/concept_evolve/tree/010_egraph_linear_span_rewriting/concept.json`

## Encoding

Represent a candidate by a local rule table plus a small periodic-orbit or short-horizon spacetime block, with SAT or symbolic pruning used to enforce witness legality early. This is less biologically CA-like, but it yields a tightly specified parameterization that non-CA baselines can also search.

## Why It Survives

- It is compatible with the exact-witness mindset because legality is baked into the parameterization rather than added by repair.
- It supplies a clean decoder-matched comparator against the champion CA lane.

## Why It Is Not Promoted

- It is more of a formal-methods search parameterization than a natural CA state encoding.
- It is useful for baseline parity and search-space pruning, but not the clearest champion representation for the main story.
