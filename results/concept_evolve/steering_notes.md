# Steering Notes

## Direction 1 - Close-Encounter Trust Spine

- Concept cards to implement:
  - `angular_sweep_encounter_queue`
  - `encounter_reversible_substeps`
  - `forward_reverse_verification_loop`
- Planned bridge-chain experiments:
  - `angular_sweep_encounter_queue -> encounter_reversible_substeps -> forward_reverse_verification_loop -> differentiable_softening_calibration -> trajectory_mass_inference`
  - `constraint_projected_kepler -> resolution_coupled_softening -> neighbor_tree_gravity`
- Why this direction stays narrow:
  - It turns the strongest falsifier branch - close encounters and trust loss - into a measurable control loop instead of a vague UI feature.
- Rubric items informed:
  - `item_011`, `item_012`, `item_016`, `item_017`, `item_019`, `item_020`, `item_022`

## Direction 2 - Resolution-Aware Honesty Layer

- Concept cards to implement:
  - `resolution_coupled_softening`
  - `constraint_projected_kepler`
- Planned bridge-chain experiments:
  - `constraint_projected_kepler -> resolution_coupled_softening -> neighbor_tree_gravity`
  - `neighbor_tree_gravity -> event_sparse_far_field -> epicycle_patch_streaming -> resolution_coupled_softening`
- Why this direction stays novel:
  - It reframes softening and stabilization as representational honesty controls rather than hidden numerical hacks, which directly supports the H1 audit-first claim.
- Rubric items informed:
  - `item_006`, `item_008`, `item_011`, `item_012`, `item_017`, `item_018`, `item_021`, `item_022`

## Direction 3 - Offline Differentiable Preset Discovery

- Concept cards to implement:
  - `differentiable_softening_calibration`
  - `forward_reverse_verification_loop`
- Planned bridge-chain experiments:
  - `angular_sweep_encounter_queue -> encounter_reversible_substeps -> forward_reverse_verification_loop -> differentiable_softening_calibration -> trajectory_mass_inference`
  - `constraint_projected_kepler -> resolution_coupled_softening -> neighbor_tree_gravity`
- Why this direction is worth the complexity:
  - The calibration step can produce named `fast`, `stable`, and `teaching` presets whose ranking is learned from teacher traces rather than hand-tuned by intuition.
- Rubric items informed:
  - `item_009`, `item_012`, `item_017`, `item_018`, `item_019`, `item_021`
