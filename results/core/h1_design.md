# H1 Design

`H1` = Proof-Carrying Symbolic Forcing-Front Cellular Automaton

This is a design document for the verifier-coupled CA lane. It does not claim experimental success; the exact verifier remains absent.

## 1. Lattice / Fiber Layout

Use a stage-indexed fiber layout rather than a flat 2D image-style lattice.

- Vertex fiber:
  - one cell for each vertex `e in d_1 x ... x d_k`
  - stores `R`-seed proposals, `T` membership, and proof-carrying span metadata
- Edge fibers:
  - for each stage `i`, one cell for each prefix key in `d_1 x ... x d_{i-1} x (d_i - 1)`
  - stores the proposed nonzero entry of `f_i`
- Alphabet registry fiber:
  - stores the active finite set `X`
  - all nonzero labels used anywhere must appear here

The fiber layout is chosen so the decoded object is already a legal witness schema. No post hoc graph reconstruction from an arbitrary image is allowed.

## 2. Cell / State Alphabet

Each vertex-fiber cell carries a finite structured state:

- `seed_label`:
  - either `none` or one element of `X`
  - compiles to one singleton-supported element of `R`
- `forced_bit`:
  - whether the cell belongs to `T`
- `proof_tag`:
  - symbolic provenance class for why a local certificate is believed available
- `mask_tag`:
  - whether all currently known off-target support is already inside `T`

Each edge-fiber cell carries:

- `edge_label`:
  - `(0,0)` or one element of `X`
- `legality_tag`:
  - local flag that the key lies in the correct stage range

Each registry cell carries:

- one candidate label of `X`
- an active/inactive bit

## 3. Proof-Carrying Symbolic Fields

The CA is not allowed to carry only geometric or scalar activations. It must carry discrete symbolic fields that are interpretable as witness-relevant proof data.

Minimal required symbolic fields:

- edge-difference provenance:
  - which stage edge could justify adding `x(e_1) - x(e_2)` to the span
- singleton-certificate request:
  - whether the local goal is to isolate `(a,-a)` at one vertex
- mask status:
  - whether all other known support is already inside `T`
- support ownership:
  - ensures each decoded `R` element has exactly one nonzero support site

These fields are only a proposal language until an exact verifier exists, but they constrain the CA away from purely heuristic pattern generation.

## 4. Local Update Constraints

Local updates are allowed only if they preserve direct decodability into a legal witness.

- Edge-fiber updates:
  - may change `edge_label` only to `(0,0)` or an active label in the registry fiber
  - may not create keys outside the legal prefix range of that stage
- Vertex-fiber updates:
  - may activate `seed_label` only if the site remains singleton-supported in the decoded `R`
  - may set `forced_bit = 1` only when the local proof state claims a singleton `(a,-a)` certificate and the mask condition is satisfied
- Registry updates:
  - may activate or deactivate labels in `X`, but the nonzero labels must continue to satisfy `a+b != 0`

Illegal transitions are not repaired. The entire candidate is rejected at decode time.

## 5. Exact Decoder Interface

The decoder is fixed in advance and contains no optimization logic.

Input:

- registry fiber state
- all edge-fiber states
- all vertex-fiber states

Output:

- `X`:
  - active labels from the registry plus `(0,0)`
- `d_1, ..., d_k`:
  - fixed by the evaluation condition, not learned on the fly inside the decoder
- `f_1, ..., f_k`:
  - one entry from each edge-fiber cell with nonzero `edge_label`
- `T`:
  - all vertex cells with `forced_bit = 1`
- `R`:
  - one singleton-supported map for each vertex cell with `seed_label != none`

Reject conditions:

- nonzero label outside active `X`
- any nonzero label with `a+b = 0`
- malformed singleton support in `R`
- duplicate or out-of-range coordinates
- denominator failure in the score

## 6. No-Repair Rule

This lane is valid only if:

- the CA state decodes directly to a legal witness,
- malformed candidates are rejected rather than repaired,
- and all downstream score/forcing checks are exact.

If the decoder has to merge supports, rewrite labels, or infer missing legality conditions, the novelty moves from the CA to the decoder and the lane fails its own standard.

## 7. Why This Design Fits The Literature Constraints

- It uses the product-grid witness representation directly, matching the Katz-Tao target rather than an adjacent proxy.
- It leaves room for proof-aware local structure, which is the only way to avoid generic automated-search overlap.
- It explicitly resists the bounded-slope trap by separating the `X` registry from the local cell alphabet and by requiring rational-complexity sweeps in evaluation.

## 8. Current Limitation

The design is verifier-coupled in form but not yet in execution. Until the exact verifier blocker is removed, this document remains a disciplined architectural proposal rather than a validated search program.
