"""Tests for halting deciders."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.deciders import (
    LoopDecider, CTLDecider,
    KNOWN_HALTING, KNOWN_NON_HALTING,
    validate_deciders,
)


class TestLoopDecider:
    """Test loop detection decider."""

    def test_halting_machines_detected(self):
        d = LoopDecider(max_steps=50000)
        for notation in KNOWN_HALTING:
            result = d.decide_from_compact(notation)
            assert result == "halts", f"{notation} should halt, got {result}"

    def test_no_false_positives(self):
        """Loop decider should never say a non-halting machine halts."""
        d = LoopDecider(max_steps=50000)
        for notation in KNOWN_NON_HALTING:
            result = d.decide_from_compact(notation)
            assert result != "halts", f"{notation} should not halt, got {result}"

    def test_some_non_halting_detected(self):
        """Loop decider should catch at least some non-halting machines."""
        d = LoopDecider(max_steps=50000)
        detected = sum(
            1 for n in KNOWN_NON_HALTING if d.decide_from_compact(n) == "non_halting"
        )
        assert detected >= 3, f"Should detect at least 3 non-halting, got {detected}"


class TestCTLDecider:
    """Test CTL decider."""

    def test_halting_machines_detected(self):
        d = CTLDecider(max_steps=50000)
        for notation in KNOWN_HALTING:
            result = d.decide_from_compact(notation)
            assert result == "halts", f"{notation} should halt, got {result}"

    def test_no_false_positives(self):
        """CTL decider should never say a non-halting machine halts."""
        d = CTLDecider(max_steps=50000)
        for notation in KNOWN_NON_HALTING:
            result = d.decide_from_compact(notation)
            assert result != "halts", f"{notation} should not halt, got {result}"

    def test_non_halting_detected(self):
        """CTL decider should catch most non-halting machines."""
        d = CTLDecider(max_steps=50000)
        detected = sum(
            1 for n in KNOWN_NON_HALTING if d.decide_from_compact(n) == "non_halting"
        )
        assert detected >= 5, f"Should detect at least 5 non-halting, got {detected}"


class TestCombined:
    """Test combining both deciders."""

    def test_combined_catches_all_known(self):
        """At least one decider should classify each known machine correctly."""
        loop_d = LoopDecider(max_steps=50000)
        ctl_d = CTLDecider(max_steps=50000)

        for notation in KNOWN_HALTING:
            loop_r = loop_d.decide_from_compact(notation)
            ctl_r = ctl_d.decide_from_compact(notation)
            assert loop_r == "halts" or ctl_r == "halts", \
                f"Neither decider classified {notation} as halting"

        for notation in KNOWN_NON_HALTING:
            loop_r = loop_d.decide_from_compact(notation)
            ctl_r = ctl_d.decide_from_compact(notation)
            combined = "non_halting" if (loop_r == "non_halting" or ctl_r == "non_halting") else "unknown"
            assert combined != "halts", f"Decider wrongly said {notation} halts"


class TestValidation:
    """Test the validation function."""

    def test_no_wrong_answers(self):
        results = validate_deciders()
        for name, data in results.items():
            assert data["wrong"] == 0, f"{name} gave wrong answers: {data['wrong']}"


if __name__ == "__main__":
    import traceback
    test_classes = [TestLoopDecider, TestCTLDecider, TestCombined, TestValidation]
    passed = 0
    failed = 0
    for cls in test_classes:
        instance = cls()
        for method_name in sorted(dir(instance)):
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
