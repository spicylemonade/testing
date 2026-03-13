# Hypothesis Bridge

These three candidates stay inside the current budget envelope: each is surprising at the method bridge level, but each can be killed quickly by transfer, witness-safety, or anti-derivative checks already defined in the repo.

## 1. Contrastive Motif Enrichment Atlas

Title: Contrastive motif enrichment for failed `42 -> 43` extensions in `R(5,5)`.

Closest prior art: Ge et al. 2022 on Exoo's lower bound, Lehavi 2024 on one-vertex extension / counterexample checking, and the current repo-local obstruction-atlas line. The overlap risk is that this collapses into plain recurrence counting over failed extension witnesses.

Why it is different: The bridge import is from biological-network motif mining plus design-of-experiments controls. The claim is not that some obstruction core appears often; it is that a small set of canonical motifs is differentially enriched in failed extensions relative to witness-safe local neighborhoods and seed-diversified null families. If that enrichment transfers across parent families, the object is stronger than an OVE catalog and less lineage-sensitive than an Exoo-only atlas.

Falsifiable prediction: After canonicalization and frozen provenance labels, a top-`k` enriched motif set will cover at least 30 percent of failed orbit-distinct extensions across at least 3 non-isomorphic parent families, retain at least 50 percent of that coverage on the decisive anti-Exoo holdout, and cause zero deletions of known `42`- or `43`-vertex witnesses when promoted to filters.

Required experiments: Materialize `frontier_parent`, `extension_case`, and `failure_witness` records for at least 3 parent families; define a witness-safe / seed-diversified null comparison set; measure raw versus canonical motif enrichment; run leave-one-parent-out, family-balance, and witness-safety audits; reject the direction immediately if enrichment vanishes off the main lineage.

## 2. Orbit-Quotient Ramsey Abstract Interpreter

Title: A sound abstract-interpretation layer for partial Ramsey colorings.

Closest prior art: the necessary-condition and filter logic in the `R(5,5) <= 46` and Gauthier upper-bound line, together with the repo's planned witness-safe filter bank. The overlap risk is that this becomes ad hoc pruning with a static-analysis label attached.

Why it is different: The bridge import is from abstract interpretation and static analysis, not from another SAT or LP engine. The reusable object would be a monotone abstract state over orbit-labeled neighborhood signatures, together with sound refinement operators. That is stronger than a bag of filters because the state space, transfer functions, and refinement order can be audited for soundness and potentially replayed as proof-side lemmas.

Falsifiable prediction: An abstract domain richer than trivial degree and neighborhood screens will prune a measurable fraction of impossible extension cases or exact branches on held-out families while deleting zero known witnesses; if the gain disappears when representation, decomposition, and proof logging are held fixed and only the abstract layer is removed, the hypothesis is dead.

Required experiments: Define the abstract state, concretization map, and refinement rules; prove monotonicity or exhaustively audit soundness on the saved witness set; benchmark against trivial degree / neighborhood filters under matched compute; run held-out-family transfer and raw-versus-refined ablations; try to replay at least one promoted abstract state as a checker-visible proof stub.

## 3. Rare-Tail Phase Separation Of Uncovered Failures

Title: Rare-event tail discovery for secondary obstruction families.

Closest prior art: Exoo-style and Aija'am-style heuristic search, Ge et al. 2022 low-defect near-miss analysis, and the repo's held `defect_ensemble_rare_event_bridge`. The overlap risk is optimizer theater: better search trajectories without a new Ramsey object.

Why it is different: The bridge import is from statistical physics and rare-event analysis, but the objective is not to find better witnesses. The only claim is that, after the first atlas pass, the uncovered failure tail may contain a compact secondary obstruction family that ordinary recurrence counting misses. Rare-event sampling is therefore a diagnostic probe for hidden structure, not a standalone lower-bound method.

Falsifiable prediction: Once the dominant atlas cores are removed, targeted rare-event sampling plus local-signature clustering will reveal a secondary canonical family explaining at least 20 percent of the remaining failures across at least 2 non-Exoo-like parent families; if the tail stays diffuse, family-specific, or fails witness-safety / transfer checks, record `rare_core_tail` and kill the direction.

Required experiments: Run the first atlas pass and quantify the uncovered tail; sample low-coverage regions from diversified, not just Exoo-like, seeds; canonicalize and cluster the new failures by local signature; run anti-Exoo transfer, family-balance, and witness-safety audits on the secondary family; compare against equalized non-rare-event sampling so any gain cannot be explained as "more search."
