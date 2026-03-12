from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SelectorInstance:
    selector_id: str
    family: str
    indices: list[int]
    metadata: dict[str, int | str] = field(default_factory=dict)


def arithmetic_progression(selector_id: str, step: int, offset: int, count: int) -> SelectorInstance:
    indices = [step * k + offset for k in range(1, count + 1)]
    return SelectorInstance(selector_id, "arithmetic_progression", indices, {"step": step, "offset": offset})


def finite_union(selector_id: str, modulus: int, residues: list[int], count: int) -> SelectorInstance:
    residues_set = {r % modulus for r in residues}
    indices: list[int] = []
    n = 1
    while len(indices) < count:
        if n % modulus in residues_set:
            indices.append(n)
        n += 1
    return SelectorInstance(selector_id, "finite_union_of_arithmetic_progressions", indices, {"modulus": modulus})


def fibonacci_indices(count: int) -> SelectorInstance:
    values = [1, 1]
    while len(values) < count + 2:
        values.append(values[-1] + values[-2])
    return SelectorInstance("fib_indices", "linear_recursive", values[1 : count + 1], {"template": "F_{k+2}"})


def pell_indices(count: int) -> SelectorInstance:
    values = [1, 2]
    while len(values) < count:
        values.append(2 * values[-1] + values[-2])
    return SelectorInstance("pell_indices", "linear_recursive", values[:count], {"template": "P_{k+1}"})


def padovan_indices(count: int) -> SelectorInstance:
    values = [1, 1, 1]
    while len(values) < count + 2:
        values.append(values[-2] + values[-3])
    return SelectorInstance("padovan_indices", "linear_recursive", values[2 : count + 2], {"template": "A_{k+3}"})


def smoke_selector_bank(count: int) -> dict[str, SelectorInstance]:
    return {
        "ap_2_0": arithmetic_progression("ap_2_0", step=2, offset=0, count=count),
        "ap_3_1": arithmetic_progression("ap_3_1", step=3, offset=1, count=count),
        "union_mod3_01": finite_union("union_mod3_01", modulus=3, residues=[0, 1], count=count),
        "fib_indices": fibonacci_indices(count),
        "pell_indices": pell_indices(count),
        "padovan_indices": padovan_indices(count),
    }
