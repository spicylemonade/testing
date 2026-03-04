#!/usr/bin/env python3
"""
Standalone BB(6) Candidate Verifier
====================================

Verifies the best Turing machine candidate found during the BB(6) search
campaign. This script is self-contained (uses only Python standard library)
and can be run by anyone to independently confirm results.

Usage:
    python3 verify.py

Exit code 0 = verified, 1 = verification failed.
"""


def simulate_tm(transition_table, max_steps=10_000_000):
    """Simulate a Turing machine from a blank tape.
    
    Args:
        transition_table: dict mapping (state, symbol) -> (write, direction, next_state)
            States are integers (0=A, 1=B, ...), directions: 0=L, 1=R
            next_state = -1 means HALT
        max_steps: maximum simulation steps before timeout
    
    Returns:
        (steps, ones_count, halted)
    """
    tape = {}  # sparse tape: position -> symbol (default 0)
    head = 0
    state = 0
    
    for step in range(1, max_steps + 1):
        symbol = tape.get(head, 0)
        key = (state, symbol)
        
        if key not in transition_table:
            # Undefined transition = halt
            ones = sum(1 for v in tape.values() if v == 1)
            return step, ones, True
        
        write, direction, next_state = transition_table[key]
        
        # Write
        if write == 1:
            tape[head] = 1
        elif write == 0:
            if head in tape:
                tape[head] = 0

        # Check halt
        if next_state == -1:
            ones = sum(1 for v in tape.values() if v == 1)
            return step, ones, True
        
        # Move
        head += 1 if direction == 1 else -1
        state = next_state
    
    ones = sum(1 for v in tape.values() if v == 1)
    return max_steps, ones, False


def parse_compact(notation):
    """Parse compact TM notation like '1RB0LD_1RC0RF_1LC1LA_0RE1RZ_1LF0RB_0RC0RE'.
    
    Each underscore-separated group is one state's transitions.
    Each group has 2 entries (for symbol 0 and symbol 1).
    Each entry is 3 chars: write_symbol, direction, next_state.
    Z = HALT state.
    """
    states_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'Z': -1}
    dir_map = {'L': 0, 'R': 1}
    
    table = {}
    groups = notation.split('_')
    
    for state_idx, group in enumerate(groups):
        # Each group has 6 chars: 2 entries of 3 chars each
        for sym in range(2):
            entry = group[sym * 3:(sym + 1) * 3]
            write = int(entry[0])
            direction = dir_map[entry[1]]
            next_state = states_map[entry[2]]
            table[(state_idx, sym)] = (write, direction, next_state)
    
    return table


def format_table(notation):
    """Pretty-print a transition table."""
    groups = notation.split('_')
    state_names = 'ABCDEF'
    
    print(f"  {'State':>5} | {'Read 0':>8} | {'Read 1':>8}")
    print(f"  {'-' * 5}-+-{'-' * 8}-+-{'-' * 8}")
    for i, group in enumerate(groups):
        e0 = group[:3]
        e1 = group[3:6]
        print(f"  {state_names[i]:>5} | {e0:>8} | {e1:>8}")


# ============================================================
# BEST CANDIDATE FROM SEARCH CAMPAIGN
# ============================================================
# Found via mutation search from Kropitz t15 champion
# Original: 1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE
# Mutation: state E, symbol 0: 0LE -> 0RE (direction change)
# ============================================================

BEST_CANDIDATE = "1RB0LD_1RC0RF_1LC1LA_0RE1RZ_1LF0RB_0RC0RE"
EXPECTED_SIGMA = 80
EXPECTED_STEPS = 2452


def main():
    print("=" * 60)
    print("BB(6) CANDIDATE VERIFICATION")
    print("=" * 60)
    print()
    print(f"Machine: {BEST_CANDIDATE}")
    print()
    print("Transition table:")
    format_table(BEST_CANDIDATE)
    print()
    
    print("Simulating from blank tape...")
    table = parse_compact(BEST_CANDIDATE)
    steps, sigma, halted = simulate_tm(table, max_steps=10_000_000)
    
    print()
    print(f"  Steps taken:  {steps}")
    print(f"  1s on tape:   {sigma} (sigma)")
    print(f"  Halted:       {halted}")
    print()
    
    # Verify against expected values
    checks = [
        ("Halted", halted, True),
        ("Sigma matches", sigma, EXPECTED_SIGMA),
        ("Steps match", steps, EXPECTED_STEPS),
    ]
    
    all_ok = True
    for name, actual, expected in checks:
        ok = actual == expected
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}: got {actual}, expected {expected}")
        if not ok:
            all_ok = False
    
    print()
    if all_ok:
        print("VERIFICATION PASSED")
        print(f"This machine writes {sigma} ones in {steps} steps on a 6-state 2-symbol Turing machine.")
        print()
        print("NOTE: This does NOT beat the current BB(6) record holder")
        print("(mxdys 2025: sigma > 2↑↑↑5, Kropitz 2022: sigma > 10↑↑15).")
        print("Those champions operate at scales far beyond step-by-step simulation.")
        print("Our best result from ~1M machines searched with step limit 10^6.")
    else:
        print("VERIFICATION FAILED")
    
    print("=" * 60)
    return 0 if all_ok else 1


if __name__ == "__main__":
    exit(main())
