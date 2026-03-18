#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hadamard_ca.seed import published_frontier_manifest_payload, published_frontier_sequences


SOURCE_EXCERPT = """Fact 3.1. Let q, s in {+/-1}^167 be the binary sequences encoded as follows and starting
with +1:
q : (83, 2, 81, 1)
s : (4)^5(2,1,1)^5(1,5)(4)^4(2,1,1)^6(4)^4(3)(1,2,1)^5(3)(4)^4(3)(1,2,1)^5
Let (A, B, C, D) = (s, s', (sq), (sq)') and H = GS(A, B, C, D). Then (A, B, C, D) is
a 64-modular Golay quadruple of length 167, and H is a 64-modular Hadamard matrix of
order 668.

The 166 coefficients c_i are all 0 with the following 13 exceptions:
c4 c8 c12 c16 c26 c30 c34 c38 c42 c46 c50 c54 c58
-512 384 -256 128 -64 128 -192 256 -320 256 -192 128 -64
"""


def _to_list_dict(sequences: dict[str, object]) -> dict[str, list[int]]:
    return {key: [int(value) for value in seq] for key, seq in sequences.items()}


def main() -> int:
    out_dir = Path("results/frontier/order_668_64m")
    out_dir.mkdir(parents=True, exist_ok=True)

    sequences = published_frontier_sequences()
    manifest = published_frontier_manifest_payload()

    (out_dir / "source_excerpt.txt").write_text(SOURCE_EXCERPT)
    (out_dir / "seed_sequences.json").write_text(
        json.dumps(_to_list_dict(sequences), indent=2)
    )
    (out_dir / "seed_manifest.json").write_text(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
