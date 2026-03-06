# Analysis

The round-trip helper is implemented, but the strongest original claim does not survive intact.

- Smooth controls show tiny round-trip error, as expected.
- Surprisingly, the plain direct kernel keeps near-machine-precision round-trip error even on the `star_grazing_two_body` case where its final-state error versus REBOUND is large.

Result: forward/backward mismatch is valuable as a self-consistency diagnostic, but it is not a reliable standalone proxy for external fidelity in close encounters. The original runtime-trust claim is therefore partially invalidated.
