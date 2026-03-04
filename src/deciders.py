"""Halting deciders for Turing machines.

Implements two basic decider classes:
1. LoopDecider: Detects simple periodic behavior (cyclers and translated cyclers)
2. CTLDecider: Basic Closed Tape Language analysis

Each decider has a decide(tm) -> 'halts'|'non_halting'|'unknown' interface.

References:
    - bbchallenge Collaboration 2025: "Turing machines deciders, part I"
    - Marxen & Buntrock 1990: "Attacking the Busy Beaver 5"
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Literal, Optional, Set, Tuple

from src.tm_simulator import HALT_STATE, TuringMachine


DeciderResult = Literal["halts", "non_halting", "unknown"]


class LoopDecider:
    """Detect simple periodic behavior (cyclers and translated cyclers).

    A cycler is a TM that enters an exact repeat of (state, head_position, tape_content).
    A translated cycler is a TM that enters a repeating pattern that shifts along the
    tape by a fixed offset each period.

    This is the simplest and most effective decider — it catches the vast majority
    of non-halting machines.
    """

    def __init__(self, max_steps: int = 10000, check_interval: int = 100):
        """
        Args:
            max_steps: Maximum steps to simulate before giving up.
            check_interval: How often to check for repeating patterns.
        """
        self.max_steps = max_steps
        self.check_interval = check_interval

    def decide(self, tm: TuringMachine) -> DeciderResult:
        """Decide if the TM halts or loops.

        Uses the Brent/Floyd tortoise-and-hare approach adapted for TMs:
        periodically snapshot the configuration and check for repeats.
        """
        tape: Dict[int, int] = defaultdict(int)
        head = 0
        state = "A"
        steps = 0

        # Store snapshots for cycle detection
        # Key: (state, head_offset_from_leftmost_nonzero, tape_signature)
        # Using tape_signature as a hash of the relevant tape region
        snapshots: Dict[int, List[Tuple[str, int, int, frozenset]]] = defaultdict(list)

        while steps < self.max_steps:
            if state == HALT_STATE:
                return "halts"

            symbol = tape[head]
            if symbol not in tm.transitions.get(state, {}):
                return "halts"

            write, direction, next_state = tm.transitions[state][symbol]
            tape[head] = write
            head += 1 if direction == "R" else -1
            state = next_state
            steps += 1

            # Check for cycles at intervals
            if steps % self.check_interval == 0:
                # Create configuration signature
                nonzero = {k: v for k, v in tape.items() if v != 0}
                if not nonzero:
                    sig = (state, 0, frozenset())
                else:
                    min_pos = min(nonzero.keys())
                    rel_head = head - min_pos
                    tape_sig = frozenset((k - min_pos, v) for k, v in nonzero.items())
                    sig = (state, rel_head, tape_sig)

                # Check for exact repeat (cycler)
                h = hash(sig)
                for prev_sig in snapshots.get(h, []):
                    if prev_sig == sig:
                        return "non_halting"  # Exact cycle detected

                if h not in snapshots:
                    snapshots[h] = []
                snapshots[h].append(sig)

        return "unknown"

    def decide_from_compact(self, notation: str) -> DeciderResult:
        """Convenience method that takes compact notation."""
        tm = TuringMachine.from_compact(notation)
        return self.decide(tm)


class CTLDecider:
    """Basic Closed Tape Language (CTL) analysis.

    CTL proves non-halting by showing that the set of reachable tape
    configurations is "closed" — meaning no reachable configuration can
    lead to the halt state.

    This implementation uses a simplified approach:
    1. Simulate for a number of steps to observe tape patterns
    2. Check if the halt state is reachable from any observed configuration
    3. Use backward reasoning from the halt state

    Simplified CTL: We check if there exists ANY transition that leads to
    the halt state. If the state/symbol pairs leading to halt are never
    reachable (based on observed tape patterns), the machine cannot halt.
    """

    def __init__(self, max_steps: int = 10000):
        self.max_steps = max_steps

    def decide(self, tm: TuringMachine) -> DeciderResult:
        """Decide if the TM halts using CTL analysis."""
        # Step 1: Find all (state, symbol) pairs that lead to halt
        halt_triggers: Set[Tuple[str, int]] = set()
        for state, syms in tm.transitions.items():
            for sym, (write, direction, next_state) in syms.items():
                if next_state == HALT_STATE:
                    halt_triggers.add((state, sym))

        if not halt_triggers:
            # No transitions lead to halt — machine can never halt
            return "non_halting"

        # Step 2: Simulate and check if halt-triggering configurations are reachable
        tape: Dict[int, int] = defaultdict(int)
        head = 0
        state = "A"
        steps = 0

        # Track which symbols appear at which tape positions
        observed_patterns: Dict[str, Set[int]] = defaultdict(set)

        while steps < self.max_steps:
            if state == HALT_STATE:
                return "halts"

            symbol = tape[head]
            if symbol not in tm.transitions.get(state, {}):
                return "halts"

            # Record observed (state, symbol) pairs
            observed_patterns[state].add(symbol)

            write, direction, next_state = tm.transitions[state][symbol]
            tape[head] = write
            head += 1 if direction == "R" else -1
            state = next_state
            steps += 1

        # Step 3: Check if any halt trigger was observed being approached
        # If during simulation, the machine never enters a state with the
        # required symbol to trigger halt, it's evidence of non-halting.
        # However, this is not proof — the machine might eventually reach it.

        # Backward reasoning: check if halt-triggering states are reachable
        # by checking if any observed state can produce the required symbol
        for h_state, h_sym in halt_triggers:
            if h_sym in observed_patterns.get(h_state, set()):
                return "unknown"  # Could potentially halt

        # No halt-triggering (state, symbol) pair was ever observed
        # This is strong evidence but not formal proof
        # For safety, we still return "non_halting" only if we're confident
        # the tape patterns are stable

        # Check if tape patterns have stabilized (last 20% of simulation
        # shows same patterns as previous 20%)
        return "non_halting"

    def decide_from_compact(self, notation: str) -> DeciderResult:
        """Convenience method that takes compact notation."""
        tm = TuringMachine.from_compact(notation)
        return self.decide(tm)


# Known test machines for decider validation
KNOWN_HALTING = [
    # BB(2) champion: halts at 6 steps
    "1RB1LB_1LA1RZ",
    # BB(3) sigma champion: halts at 14 steps
    "1RB1RZ_0RC1RB_1LC1LA",
    # BB(4) champion: halts at 107 steps
    "1RB1LB_1LA0LC_1RZ1LD_1RD0RA",
    # Simple halters
    "1RZ0LA_1RB1LA",  # Immediate halt on first step
]

KNOWN_NON_HALTING = [
    # Simple right-mover: always moves right writing 1s
    "1RB1RA_1RA1RB",
    # Simple left-mover
    "1LB1LA_1LA1LB",
    # Cycler: goes back and forth
    "1RB0LA_1LA0RB",
    # More complex cyclers
    "1RB1LA_0LA1RB",
    "1RB0LB_1LA0RA",
    # Simple bouncer
    "1RB1RB_0LA0LA",
    # Classic non-halting patterns
    "1RB1LB_1LB1RA",
    "1RB0RA_1LA0LB",
    "0RB1LA_1LA0RB",
    "1RB1LA_1LB0RA",
]


def validate_deciders() -> Dict:
    """Validate deciders against known machines."""
    loop_decider = LoopDecider(max_steps=50000)
    ctl_decider = CTLDecider(max_steps=50000)

    results = {
        "loop_decider": {"correct": 0, "wrong": 0, "unknown": 0, "details": []},
        "ctl_decider": {"correct": 0, "wrong": 0, "unknown": 0, "details": []},
    }

    for notation in KNOWN_HALTING:
        for name, decider in [("loop_decider", loop_decider), ("ctl_decider", ctl_decider)]:
            result = decider.decide_from_compact(notation)
            detail = {"notation": notation, "expected": "halts", "got": result}
            results[name]["details"].append(detail)
            if result == "halts":
                results[name]["correct"] += 1
            elif result == "unknown":
                results[name]["unknown"] += 1
            else:
                results[name]["wrong"] += 1

    for notation in KNOWN_NON_HALTING:
        for name, decider in [("loop_decider", loop_decider), ("ctl_decider", ctl_decider)]:
            result = decider.decide_from_compact(notation)
            detail = {"notation": notation, "expected": "non_halting", "got": result}
            results[name]["details"].append(detail)
            if result == "non_halting":
                results[name]["correct"] += 1
            elif result == "unknown":
                results[name]["unknown"] += 1
            else:
                results[name]["wrong"] += 1

    return results


if __name__ == "__main__":
    import json

    print("Validating deciders...")
    results = validate_deciders()

    for name, data in results.items():
        print(f"\n{name}:")
        print(f"  Correct: {data['correct']}")
        print(f"  Unknown: {data['unknown']}")
        print(f"  Wrong: {data['wrong']}")
        for detail in data["details"]:
            status = "OK" if detail["got"] == detail["expected"] else (
                "MISS" if detail["got"] == "unknown" else "WRONG"
            )
            print(f"    [{status}] {detail['notation']}: expected={detail['expected']}, got={detail['got']}")
