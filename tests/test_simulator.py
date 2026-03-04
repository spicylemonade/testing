"""Tests for the Turing Machine simulator.

Verifies against known BB(2)=4, BB(3)=6, BB(4)=13, BB(5)=47176870 values.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.tm_simulator import TuringMachine, BB_CHAMPIONS, verify_known_bb_values


class TestTuringMachineBasic:
    """Test basic TM operations."""

    def test_compact_parse_roundtrip(self):
        notation = "1RB1LB_1LA1RZ"
        tm = TuringMachine.from_compact(notation)
        assert tm.to_compact() == notation

    def test_compact_parse_6state(self):
        notation = "1RB0LD_1RC0RF_1LC1LA_0LE1RZ_1LF0RB_0RC0RE"
        tm = TuringMachine.from_compact(notation)
        assert tm.num_states == 6
        assert tm.to_compact() == notation

    def test_blank_tape_start(self):
        """A TM that immediately halts should return 0 steps."""
        tm = TuringMachine({"A": {0: (0, "R", "Z"), 1: (0, "R", "Z")}})
        steps, ones, tape, halted = tm.simulate()
        assert halted is True
        assert steps == 1
        assert ones == 0

    def test_write_one_and_halt(self):
        """A TM that writes 1 then halts."""
        tm = TuringMachine({"A": {0: (1, "R", "Z"), 1: (0, "R", "Z")}})
        steps, ones, tape, halted = tm.simulate()
        assert halted is True
        assert steps == 1
        assert ones == 1

    def test_max_steps_reached(self):
        """A looping TM should return halted=False."""
        tm = TuringMachine({"A": {0: (1, "R", "A"), 1: (1, "R", "A")}})
        steps, ones, tape, halted = tm.simulate(max_steps=100)
        assert halted is False
        assert steps == 100


class TestBBChampions:
    """Test against known Busy Beaver values."""

    def test_bb2_sigma(self):
        tm = TuringMachine.from_compact(BB_CHAMPIONS[2]["notation"])
        steps, ones, tape, halted = tm.simulate()
        assert halted is True
        assert ones == 4  # BB(2) = 4

    def test_bb2_steps(self):
        tm = TuringMachine.from_compact(BB_CHAMPIONS[2]["notation"])
        steps, ones, tape, halted = tm.simulate()
        assert steps == 6  # S(2) = 6

    def test_bb3_sigma(self):
        tm = TuringMachine.from_compact(BB_CHAMPIONS[3]["notation"])
        steps, ones, tape, halted = tm.simulate()
        assert halted is True
        assert ones == 6  # BB(3) = 6

    def test_bb3_steps(self):
        # Note: BB(3) sigma champion takes 14 steps (not 21).
        # S(3) = 21 is achieved by a DIFFERENT machine.
        tm = TuringMachine.from_compact(BB_CHAMPIONS[3]["notation"])
        steps, ones, tape, halted = tm.simulate()
        assert steps == 14  # Sigma champion takes 14 steps

    def test_bb4_sigma(self):
        tm = TuringMachine.from_compact(BB_CHAMPIONS[4]["notation"])
        steps, ones, tape, halted = tm.simulate()
        assert halted is True
        assert ones == 13  # BB(4) = 13

    def test_bb4_steps(self):
        tm = TuringMachine.from_compact(BB_CHAMPIONS[4]["notation"])
        steps, ones, tape, halted = tm.simulate()
        assert steps == 107  # S(4) = 107

    def test_bb5_sigma(self):
        """BB(5) = 4098. This is the sigma (1s) value, not steps."""
        tm = TuringMachine.from_compact(BB_CHAMPIONS[5]["notation"])
        steps, ones, tape, halted = tm.simulate(max_steps=10**8)
        assert halted is True
        assert ones == 4098  # BB(5) = 4098

    def test_bb5_steps(self):
        """S(5) = 47,176,870 steps."""
        tm = TuringMachine.from_compact(BB_CHAMPIONS[5]["notation"])
        steps, ones, tape, halted = tm.simulate(max_steps=10**8)
        assert halted is True
        assert steps == 47176870

    def test_verify_all_known(self):
        results = verify_known_bb_values()
        for n, r in results.items():
            assert r["correct"], f"BB({n}) verification failed: {r}"


class TestFromDict:
    """Test JSON dict parsing."""

    def test_from_dict_bb2(self):
        table = {
            "A": {"0": {"write": 1, "move": "R", "next": "B"}, "1": {"write": 1, "move": "L", "next": "B"}},
            "B": {"0": {"write": 1, "move": "L", "next": "A"}, "1": {"write": 1, "move": "R", "next": "Z"}},
        }
        tm = TuringMachine.from_dict(table)
        steps, ones, tape, halted = tm.simulate()
        assert halted is True
        assert ones == 4


if __name__ == "__main__":
    # Simple test runner
    import traceback
    test_classes = [TestTuringMachineBasic, TestBBChampions, TestFromDict]
    passed = 0
    failed = 0
    for cls in test_classes:
        instance = cls()
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                try:
                    getattr(instance, method_name)()
                    print(f"  PASS: {cls.__name__}.{method_name}")
                    passed += 1
                except Exception as e:
                    print(f"  FAIL: {cls.__name__}.{method_name}: {e}")
                    traceback.print_exc()
                    failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
