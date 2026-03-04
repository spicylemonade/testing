"""Turing Machine simulator for Busy Beaver research.

Provides a correct, well-tested step-by-step simulator with configurable
step limits. Supports both the standard (state, symbol) -> (write, move, next)
transition table format and the compact string notation used by bbchallenge.

Usage:
    from src.tm_simulator import TuringMachine
    tm = TuringMachine.from_compact("1RB1LB_1LA1RZ")
    steps, ones, tape, halted = tm.simulate(max_steps=10**8)
"""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Dict, List, Optional, Tuple


HALT_STATE = "Z"  # Convention: Z is the halt state (bbchallenge uses "Z")


class TuringMachine:
    """A deterministic Turing machine with 2-symbol alphabet {0, 1}.

    The transition table maps (state, symbol) -> (write_symbol, direction, next_state).
    Direction is 'L' (left) or 'R' (right).
    The halt state 'Z' has no outgoing transitions.
    """

    def __init__(self, transitions: Dict[str, Dict[int, Tuple[int, str, str]]]):
        """Initialize with transitions dict.

        Args:
            transitions: {state: {symbol: (write, direction, next_state)}}
                e.g. {"A": {0: (1, "R", "B"), 1: (1, "L", "B")}, ...}
        """
        self.transitions = transitions
        self.states = sorted(transitions.keys())
        self.num_states = len(self.states)

    @classmethod
    def from_compact(cls, notation: str) -> TuringMachine:
        """Parse compact notation like '1RB1LB_1LA1RZ'.

        Format: Groups separated by '_', one group per state (A, B, C, ...).
        Each group has two transitions (for symbol 0 and 1), each 3 characters:
            - write symbol (0 or 1)
            - direction (L or R)
            - next state (A-F, or Z for halt)

        The notation '---' means undefined transition.
        """
        groups = notation.strip().split("_")
        transitions = {}
        state_names = [chr(ord("A") + i) for i in range(len(groups))]

        for i, group in enumerate(groups):
            state = state_names[i]
            transitions[state] = {}
            for sym in range(2):
                chunk = group[sym * 3 : sym * 3 + 3]
                if chunk == "---":
                    continue
                write = int(chunk[0])
                direction = chunk[1]
                next_state = chunk[2]
                transitions[state][sym] = (write, direction, next_state)

        return cls(transitions)

    @classmethod
    def from_dict(cls, table: Dict) -> TuringMachine:
        """Parse from JSON dict format used in known_champions.json.

        Format: {state: {symbol_str: {write, move, next}}}
        """
        transitions = {}
        for state, symbols in table.items():
            transitions[state] = {}
            for sym_str, action in symbols.items():
                sym = int(sym_str)
                transitions[state][sym] = (
                    action["write"],
                    action["move"],
                    action["next"],
                )
        return cls(transitions)

    def to_compact(self) -> str:
        """Convert back to compact notation."""
        parts = []
        for state in self.states:
            group = ""
            for sym in range(2):
                if sym in self.transitions[state]:
                    write, direction, next_state = self.transitions[state][sym]
                    group += f"{write}{direction}{next_state}"
                else:
                    group += "---"
            parts.append(group)
        return "_".join(parts)

    def simulate(
        self, max_steps: int = 10**8, initial_state: str = "A"
    ) -> Tuple[int, int, Dict[int, int], bool]:
        """Simulate the TM from a blank tape.

        Args:
            max_steps: Maximum number of steps before giving up.
            initial_state: Starting state (default "A").

        Returns:
            (num_steps, num_ones, tape_dict, halted)
            - num_steps: number of transitions executed
            - num_ones: number of 1s on the tape
            - tape_dict: {position: symbol} for non-zero cells
            - halted: True if the machine reached halt state Z
        """
        tape: Dict[int, int] = defaultdict(int)
        head = 0
        state = initial_state
        steps = 0

        while steps < max_steps:
            if state == HALT_STATE:
                ones = sum(1 for v in tape.values() if v == 1)
                return steps, ones, dict(tape), True

            symbol = tape[head]
            if symbol not in self.transitions.get(state, {}):
                # Undefined transition — treat as halt
                ones = sum(1 for v in tape.values() if v == 1)
                return steps, ones, dict(tape), True

            write, direction, next_state = self.transitions[state][symbol]
            tape[head] = write
            head += 1 if direction == "R" else -1
            state = next_state
            steps += 1

        # Did not halt within step limit
        ones = sum(1 for v in tape.values() if v == 1)
        return steps, ones, dict(tape), False

    def __repr__(self) -> str:
        return f"TuringMachine({self.to_compact()})"


# Known BB champions for testing
BB_CHAMPIONS = {
    2: {
        "notation": "1RB1LB_1LA1RZ",
        "sigma": 4,
        "steps": 6,
    },
    3: {
        # BB(3) sigma champion (sigma=6, 14 steps)
        # Note: S(3)=21 is achieved by a different machine that writes only 5 ones
        "notation": "1RB1RZ_0RC1RB_1LC1LA",
        "sigma": 6,
        "steps": 14,
    },
    4: {
        "notation": "1RB1LB_1LA0LC_1RZ1LD_1RD0RA",
        "sigma": 13,
        "steps": 107,
    },
    5: {
        "notation": "1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA",
        "sigma": 4098,
        "steps": 47176870,
    },
}


def verify_known_bb_values() -> Dict[int, Dict]:
    """Verify simulator against known BB values. Returns results dict."""
    results = {}
    for n, champion in BB_CHAMPIONS.items():
        tm = TuringMachine.from_compact(champion["notation"])
        max_steps = champion["steps"] * 2 if champion["steps"] < 10**8 else 10**8
        steps, ones, tape, halted = tm.simulate(max_steps=max_steps)
        results[n] = {
            "expected_sigma": champion["sigma"],
            "actual_sigma": ones,
            "expected_steps": champion["steps"],
            "actual_steps": steps,
            "halted": halted,
            "correct": halted and ones == champion["sigma"] and steps == champion["steps"],
        }
    return results


if __name__ == "__main__":
    print("Verifying known BB values...")
    results = verify_known_bb_values()
    for n, r in sorted(results.items()):
        status = "PASS" if r["correct"] else "FAIL"
        print(
            f"  BB({n}): sigma={r['actual_sigma']} (expected {r['expected_sigma']}), "
            f"steps={r['actual_steps']} (expected {r['expected_steps']}), "
            f"halted={r['halted']} [{status}]"
        )
