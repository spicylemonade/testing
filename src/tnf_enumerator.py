"""Tree Normal Form (TNF) enumerator for n-state, 2-symbol Turing machines.

Implements Brady's algorithm for generating TMs in Tree Normal Form.
TNF avoids redundant machines by only assigning transition rules as they
are first encountered during simulation. This dramatically reduces the
search space while preserving all distinct behaviors.

Convention: TNF-1RB — all machines start with first transition being
"write 1, move Right, go to state B" from state A reading 0.

References:
    - Brady 1964: PhD dissertation on BB(4)
    - bbchallenge Collaboration 2025: BB(5) paper uses TNF enumeration
"""

from __future__ import annotations

import json
import os
from typing import Dict, Generator, List, Optional, Tuple

from src.tm_simulator import HALT_STATE


class TNFEnumerator:
    """Enumerate Turing machines in Tree Normal Form.

    A TM is in TNF if states are numbered in the order they are first
    encountered during simulation from a blank tape. The first transition
    is always fixed: state A, symbol 0 -> write 1, move R, go to state B.
    """

    def __init__(self, num_states: int, num_symbols: int = 2):
        self.num_states = num_states
        self.num_symbols = num_symbols
        self.state_names = [chr(ord("A") + i) for i in range(num_states)]

    def _possible_transitions(self, next_new_state_idx: int) -> List[Tuple[int, str, str]]:
        """Generate all valid transitions for a new (state, symbol) pair.

        The next_state can be:
        - Any state with index < next_new_state_idx (already seen)
        - The state at index next_new_state_idx (first new state)
        - The halt state Z

        For 2-symbol: write can be 0 or 1, direction can be L or R.
        """
        transitions = []
        # Available next states: already-seen states + at most one new state + halt
        max_state_idx = min(next_new_state_idx, self.num_states - 1)
        available_states = [self.state_names[i] for i in range(max_state_idx + 1)] + [HALT_STATE]

        for write in range(self.num_symbols):
            for direction in ["L", "R"]:
                for next_state in available_states:
                    transitions.append((write, direction, next_state))

        return transitions

    def enumerate(self, max_count: Optional[int] = None) -> Generator[str, None, None]:
        """Generate TMs in TNF order as compact notation strings.

        TNF-1RB convention: first transition is always A,0 -> 1,R,B.
        Remaining transitions are filled in order: A1, B0, B1, C0, C1, ...
        Each transition can use states already introduced or introduce the
        next new state.

        Yields compact notation strings.
        """
        n = self.num_states
        # Total transitions: n states * 2 symbols = 2n transitions
        # First transition fixed: A0 -> 1RB
        # Remaining: 2n - 1 transitions to fill

        # Transition slots in order: (A,1), (B,0), (B,1), (C,0), (C,1), ...
        slots = []
        for si in range(n):
            for sym in range(2):
                if si == 0 and sym == 0:
                    continue  # Skip A,0 — it's fixed
                slots.append((si, sym))

        count = 0

        def _recurse(
            slot_idx: int,
            table: list,  # flat: [write, dir_int, next_state_idx] for each (state, sym)
            next_new: int,  # index of next unused state
        ):
            nonlocal count
            if max_count and count >= max_count:
                return

            if slot_idx >= len(slots):
                # All transitions defined — yield this machine
                yield self._table_to_compact(table, n)
                count += 1
                return

            si, sym = slots[slot_idx]

            # If this state hasn't been introduced yet, skip (can't define it)
            if si >= next_new:
                return

            # Enumerate all valid transitions for this slot
            for write in range(2):
                for dir_int in [1, -1]:  # R=1, L=-1
                    # Next state: any already-introduced state, or next_new, or halt (-1)
                    max_ns = min(next_new, n - 1)  # Can introduce at most one new state
                    for ns in range(max_ns + 1):
                        base = (si * 2 + sym) * 3
                        table[base] = write
                        table[base + 1] = dir_int
                        table[base + 2] = ns

                        new_next = next_new
                        if ns == next_new and next_new < n:
                            new_next = next_new + 1

                        yield from _recurse(slot_idx + 1, table, new_next)

                    # Halt state
                    base = (si * 2 + sym) * 3
                    table[base] = write
                    table[base + 1] = dir_int
                    table[base + 2] = -1  # halt

                    yield from _recurse(slot_idx + 1, table, next_new)

        # Initialize table with A,0 -> 1,R,B (fixed first transition)
        table = [0] * (n * 2 * 3)
        table[0] = 1   # write 1
        table[1] = 1   # move R
        table[2] = 1   # next state B (index 1)

        yield from _recurse(0, table, 2)  # next_new=2 since A(0) and B(1) introduced

    def _table_to_compact(self, flat_table: list, n: int) -> str:
        """Convert flat table to compact notation."""
        parts = []
        for si in range(n):
            group = ""
            for sym in range(2):
                base = (si * 2 + sym) * 3
                write = flat_table[base]
                dir_int = flat_table[base + 1]
                ns = flat_table[base + 2]
                direction = "R" if dir_int == 1 else "L"
                if ns < 0:
                    next_state = "Z"
                else:
                    next_state = chr(ord("A") + ns)
                group += f"{write}{direction}{next_state}"
            parts.append(group)
        return "_".join(parts)

    def count_tnf(self, max_count: int = 10**7) -> int:
        """Count TNF machines up to max_count."""
        count = 0
        for _ in self.enumerate(max_count=max_count):
            count += 1
        return count


def enumerate_and_count(num_states: int, max_count: int = 10**7) -> Dict:
    """Enumerate TNF machines and return count + sample."""
    enumerator = TNFEnumerator(num_states)
    count = 0
    first_10 = []

    for notation in enumerator.enumerate(max_count=max_count):
        if count < 10:
            first_10.append(notation)
        count += 1

    return {
        "num_states": num_states,
        "max_count": max_count,
        "tnf_count": count,
        "first_10": first_10,
    }


if __name__ == "__main__":
    print("Counting TNF machines...")

    results = {}
    for n in [2, 3]:
        print(f"  {n}-state: ", end="", flush=True)
        result = enumerate_and_count(n, max_count=10**6)
        print(f"{result['tnf_count']} TNF machines")
        results[f"{n}_state"] = result

    # For 6-state, just generate first 10K
    print(f"  6-state (first 10,000): ", end="", flush=True)
    enumerator = TNFEnumerator(6)
    count = 0
    for _ in enumerator.enumerate(max_count=10000):
        count += 1
    print(f"{count} generated")
    results["6_state_first_10k"] = {"tnf_count": count, "max_count": 10000}

    os.makedirs("results/benchmarks", exist_ok=True)
    with open("results/benchmarks/tnf_counts.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to results/benchmarks/tnf_counts.json")
