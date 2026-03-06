# Phase 3 Concept Synthesis

## Probe Status

- Required probe command was executed on the question `Can reversibility-triggered close-encounter microsteps and offline calibration improve trust without drifting into a TRACE or JANUS clone?`
- The automated probe sub-agent timed out twice at the built-in 480 second limit, so a direct recovery synthesis was written to `results/concept_evolve/probe_result.json` to keep Phase 3 moving.

## Revisited Walk Paths

### Determinism Path

- `differentiable_softening_calibration -> forward_reverse_verification_loop -> event_sparse_far_field -> epicycle_patch_streaming -> angular_sweep_encounter_queue`
- Why it matters: the useful part is the front half - offline preset fitting plus round-trip diagnostics - while the back half is now treated as optional performance spillover.

### Close-Encounter Path

- `encounter_reversible_substeps -> forward_reverse_verification_loop -> event_sparse_far_field -> epicycle_patch_streaming -> angular_sweep_encounter_queue`
- Why it matters: this is the clearest route from rare-event scheduling to a falsifiable trust metric for near collisions and slingshots.

### Unit-Safety / Scale-Honesty Path

- `resolution_coupled_softening -> trajectory_mass_inference -> constraint_projected_kepler -> differentiable_softening_calibration -> forward_reverse_verification_loop`
- Why it matters: the tree does not contain a pure H3 node, so the best proxy is the path that turns representation scale, fitted parameters, and invariant projection into explicit honesty controls.

## Branch Decisions

- Promoted branch: `angular_sweep_encounter_queue + encounter_reversible_substeps + forward_reverse_verification_loop + differentiable_softening_calibration`
  - Rationale: this is the narrowest branch that is still novel, testable, and clearly different from both generic toy simulators and mature REBOUND integrator work.

- Held branch: `constraint_projected_kepler + resolution_coupled_softening`
  - Rationale: keep as a secondary stabilizer and honesty layer, but only promote if it improves trust without turning bad physics into cosmetically stable motion.

- Retired branch: `neighbor_tree_gravity + event_sparse_far_field + epicycle_patch_streaming`
  - Rationale: it is interesting, but it drifts toward large-N or streaming-architecture novelty and weakens the small-N audited-kernel claim.

## Hypothesis Selection

- `H1` remains champion.
- `H2` remains the live backup if encounter evidence undermines H1.
- `H3` remains held and will be implemented only as supporting scenario-safety infrastructure.
