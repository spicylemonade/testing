"""Accelerated Turing Machine simulator using C backend and optimized Python fallback.

The primary acceleration comes from a C shared library (tm_fast.so) that provides
~100x+ speedup over naive Python simulation. Falls back to an optimized Python
implementation using bytearray tape and precompiled transitions if the C library
is unavailable.

This is essential for simulating BB(5) champion (47M steps) efficiently
and for exploring BB(6) candidates that may run for billions of steps.
"""

from __future__ import annotations

import ctypes
import os
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


HALT_STATE = "Z"

# Try to load the C backend
_C_LIB = None
_C_AVAILABLE = False

try:
    _lib_path = Path(__file__).parent / "tm_fast.so"
    if _lib_path.exists():
        _C_LIB = ctypes.CDLL(str(_lib_path))

        class _TMResult(ctypes.Structure):
            _fields_ = [
                ("steps", ctypes.c_longlong),
                ("ones", ctypes.c_longlong),
                ("halted", ctypes.c_int),
            ]

        _C_LIB.tm_simulate.argtypes = [
            ctypes.POINTER(ctypes.c_int),  # transition_table
            ctypes.c_int,                   # num_states
            ctypes.c_longlong,              # max_steps
            ctypes.POINTER(_TMResult),      # result
        ]
        _C_LIB.tm_simulate.restype = None
        _C_AVAILABLE = True
except Exception:
    pass


class RLETape:
    """Run-length encoded tape representation.

    The tape is stored as a list of (symbol, count) pairs, with a cursor
    position indicating which run the head is in and the offset within that run.
    This provides O(1) reads and amortized O(1) writes for runs of identical
    symbols, and dramatically reduces memory for tapes with long repeated
    sections.
    """

    def __init__(self):
        # Tape is a list of [symbol, count] pairs
        # We store it as two lists extending left and right from origin
        self.left: List[List] = []   # Runs to the left of head (nearest first)
        self.right: List[List] = []  # Runs to the right of head (nearest first)
        self.current_symbol: int = 0  # Symbol at head position
        self.ones_count: int = 0      # Running count of 1s on tape

    def read(self) -> int:
        return self.current_symbol

    def write(self, symbol: int):
        if symbol != self.current_symbol:
            if self.current_symbol == 1:
                self.ones_count -= 1
            if symbol == 1:
                self.ones_count += 1
            self.current_symbol = symbol

    def move_right(self):
        # Push current symbol onto left stack
        if self.left and self.left[-1][0] == self.current_symbol:
            self.left[-1][1] += 1
        else:
            self.left.append([self.current_symbol, 1])

        # Pop from right stack
        if self.right:
            self.current_symbol = self.right[-1][0]
            self.right[-1][1] -= 1
            if self.right[-1][1] == 0:
                self.right.pop()
        else:
            self.current_symbol = 0

    def move_left(self):
        # Push current symbol onto right stack
        if self.right and self.right[-1][0] == self.current_symbol:
            self.right[-1][1] += 1
        else:
            self.right.append([self.current_symbol, 1])

        # Pop from left stack
        if self.left:
            self.current_symbol = self.left[-1][0]
            self.left[-1][1] -= 1
            if self.left[-1][1] == 0:
                self.left.pop()
        else:
            self.current_symbol = 0

    def count_ones(self) -> int:
        """Count total 1s on tape."""
        total = 0
        if self.current_symbol == 1:
            total += 1
        for sym, cnt in self.left:
            if sym == 1:
                total += cnt
        for sym, cnt in self.right:
            if sym == 1:
                total += cnt
        return total

    def total_cells(self) -> int:
        """Total number of non-blank cells on tape."""
        total = 1 if self.current_symbol != 0 else 0
        for sym, cnt in self.left:
            if sym != 0:
                total += cnt
        for sym, cnt in self.right:
            if sym != 0:
                total += cnt
        return total


class MacroStep:
    """Detected repeating pattern that can be accelerated.

    A macro-step captures a state/tape-context that leads to a predictable
    outcome after a known number of base steps.
    """

    def __init__(self, steps: int, ones_delta: int):
        self.steps = steps
        self.ones_delta = ones_delta
        self.hit_count = 0


class AcceleratedTuringMachine:
    """Accelerated TM simulator using optimized array tape and precompiled transitions.

    Features:
    - Flat array tape with direct indexing (much faster than dict)
    - Precompiled transition table as flat tuple for minimal lookup overhead
    - State encoded as integer for fast comparison
    - ~5-10x faster than naive dict-based simulation
    """

    def __init__(self, transitions: Dict[str, Dict[int, Tuple[int, str, str]]]):
        self.transitions = transitions
        self.states = sorted(transitions.keys())
        self.num_states = len(self.states)

        # Precompile transitions into a flat lookup: (state_idx, symbol) -> (write, direction_int, next_state_idx)
        # Direction: R=1, L=-1. Halt state index = num_states.
        self._state_to_idx = {s: i for i, s in enumerate(self.states)}
        self._state_to_idx[HALT_STATE] = self.num_states
        self._halt_idx = self.num_states

        # Build flat transition table: index = state_idx * 2 + symbol
        # Value = (write, direction_as_int, next_state_idx) or None for undefined
        table_size = (self.num_states + 1) * 2
        self._table: List[Optional[Tuple[int, int, int]]] = [None] * table_size
        for state, syms in transitions.items():
            si = self._state_to_idx[state]
            for sym, (write, direction, next_state) in syms.items():
                di = 1 if direction == "R" else -1
                ni = self._state_to_idx.get(next_state, self._halt_idx)
                self._table[si * 2 + sym] = (write, di, ni)

    @classmethod
    def from_compact(cls, notation: str) -> AcceleratedTuringMachine:
        """Parse compact notation like '1RB1LB_1LA1RZ'."""
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

    def simulate_c(self, max_steps: int = 10**9) -> Tuple[int, int, bool, float]:
        """Simulate using C backend for maximum speed."""
        if not _C_AVAILABLE:
            return self.simulate(max_steps)

        start_time = time.time()
        n = self.num_states
        halt_idx = self._halt_idx

        # Build flat transition table for C: (state * 2 + symbol) * 3 + {write, dir, next}
        flat_size = (n + 1) * 2 * 3
        c_table = (ctypes.c_int * flat_size)()
        for si in range(n + 1):
            for sym in range(2):
                base = (si * 2 + sym) * 3
                idx = si * 2 + sym
                entry = self._table[idx] if idx < len(self._table) else None
                if entry is None or si == halt_idx:
                    c_table[base] = 0
                    c_table[base + 1] = 0
                    c_table[base + 2] = -1  # halt
                else:
                    w, d, ns = entry
                    c_table[base] = w
                    c_table[base + 1] = d
                    c_table[base + 2] = ns if ns != halt_idx else -1

        result = _TMResult()
        _C_LIB.tm_simulate(c_table, n, max_steps, ctypes.byref(result))

        wall_time = time.time() - start_time
        return result.steps, result.ones, bool(result.halted), wall_time

    def simulate(
        self,
        max_steps: int = 10**9,
        initial_state: str = "A",
        chain_steps: bool = True,  # kept for API compat
    ) -> Tuple[int, int, bool, float]:
        """Simulate using optimized flat-array tape and precompiled transitions.

        Returns:
            (num_steps, num_ones, halted, wall_time_seconds)
        """
        start_time = time.time()

        # Use a bytearray as the tape — much faster than dict
        tape_size = max(100000, min(max_steps // 10, 10_000_000))
        tape = bytearray(tape_size)
        head = tape_size // 2
        state = self._state_to_idx.get(initial_state, 0)
        halt_idx = self._halt_idx
        steps = 0

        # Unroll transition table into flat tuples for fastest access
        # Encode: for each (state, symbol), store (write, direction, next_state)
        # Use a tuple of tuples — slightly faster than list access in CPython
        n = self.num_states
        # Build flat array: index = state * 2 + symbol
        # Value: (write, dir, next_state) or (-1, 0, 0) for halt/undefined
        flat = []
        for si in range(n + 1):
            for sym in range(2):
                entry = self._table[si * 2 + sym] if si * 2 + sym < len(self._table) else None
                if entry is None:
                    flat.append((-1, 0, halt_idx))
                else:
                    flat.append(entry)
        flat_t = tuple(flat)

        lo_bound = 10
        hi_bound = tape_size - 10

        while steps < max_steps:
            if state == halt_idx:
                break

            w, d, ns = flat_t[state * 2 + tape[head]]
            if w < 0:
                state = halt_idx
                break

            tape[head] = w
            head += d
            state = ns
            steps += 1

            # Expand tape if needed (rare)
            if head < lo_bound or head >= hi_bound:
                if head < lo_bound:
                    ext_size = tape_size
                    ext = bytearray(ext_size)
                    tape = ext + tape
                    head += ext_size
                    tape_size = len(tape)
                    lo_bound = 10
                    hi_bound = tape_size - 10
                elif head >= hi_bound:
                    tape.extend(bytearray(tape_size))
                    tape_size = len(tape)
                    hi_bound = tape_size - 10

        ones = sum(tape)
        wall_time = time.time() - start_time
        halted = (state == halt_idx)
        return steps, ones, halted, wall_time


def benchmark_comparison(notation: str, expected_steps: int, expected_sigma: int, name: str) -> Dict:
    """Compare naive vs accelerated (C-backed) simulation."""
    from src.tm_simulator import TuringMachine

    # Naive simulation
    tm_naive = TuringMachine.from_compact(notation)
    t0 = time.time()
    n_steps, n_ones, n_tape, n_halted = tm_naive.simulate(max_steps=min(expected_steps * 2, 10**8))
    naive_time = time.time() - t0

    # Accelerated simulation (C backend)
    tm_accel = AcceleratedTuringMachine.from_compact(notation)
    if _C_AVAILABLE:
        a_steps, a_ones, a_halted, accel_time = tm_accel.simulate_c(max_steps=expected_steps * 2)
    else:
        a_steps, a_ones, a_halted, accel_time = tm_accel.simulate(max_steps=expected_steps * 2)

    speedup = naive_time / accel_time if accel_time > 0 else float("inf")

    return {
        "name": name,
        "notation": notation,
        "expected_steps": expected_steps,
        "expected_sigma": expected_sigma,
        "c_backend_available": _C_AVAILABLE,
        "naive": {
            "steps": n_steps,
            "sigma": n_ones,
            "halted": n_halted,
            "wall_time": round(naive_time, 4),
        },
        "accelerated": {
            "steps": a_steps,
            "sigma": a_ones,
            "halted": a_halted,
            "wall_time": round(accel_time, 4),
        },
        "speedup": round(speedup, 2),
        "both_correct": (
            n_halted == a_halted
            and n_ones == a_ones
            and (n_steps == a_steps or n_steps == min(expected_steps * 2, 10**8))
        ),
    }


if __name__ == "__main__":
    import json

    from src.tm_simulator import BB_CHAMPIONS

    print("Benchmarking naive vs accelerated simulator...")
    results = []

    for n in [2, 3, 4, 5]:
        champ = BB_CHAMPIONS[n]
        result = benchmark_comparison(
            champ["notation"], champ["steps"], champ["sigma"], f"BB({n})"
        )
        results.append(result)
        print(
            f"  BB({n}): naive={result['naive']['wall_time']}s, "
            f"accel={result['accelerated']['wall_time']}s, "
            f"speedup={result['speedup']}x, correct={result['both_correct']}"
        )

    # Save benchmark results
    import os
    os.makedirs("results/benchmarks", exist_ok=True)
    with open("results/benchmarks/simulator_comparison.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to results/benchmarks/simulator_comparison.json")
