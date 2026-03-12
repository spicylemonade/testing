from __future__ import annotations

from dataclasses import dataclass, field

from special_numbers.beta_numeration import endpoint_indices
from special_numbers.ostrowski import ostrowski_selector_indices
from special_numbers.slopes import convergents


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
    normalized_residues = sorted({r % modulus for r in residues})
    residues_set = set(normalized_residues)
    indices: list[int] = []
    n = 1
    while len(indices) < count:
        if n % modulus in residues_set:
            indices.append(n)
        n += 1
    gap_pattern: list[int] = []
    if normalized_residues:
        for idx, residue in enumerate(normalized_residues):
            next_residue = normalized_residues[(idx + 1) % len(normalized_residues)]
            if idx + 1 < len(normalized_residues):
                gap_pattern.append(next_residue - residue)
            else:
                gap_pattern.append(modulus + next_residue - residue)
    return SelectorInstance(
        selector_id,
        "finite_union_of_arithmetic_progressions",
        indices,
        {
            "modulus": modulus,
            "residues": normalized_residues,
            "gap_pattern": gap_pattern,
        },
    )


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


def quadratic_convergent_even(slope_id: str, count: int) -> SelectorInstance:
    indices = [q for index, _p, q in convergents(slope_id, max(2 * count + 8, 24)) if index % 2 == 0][:count]
    return SelectorInstance("quadratic_convergent_even", "linear_recursive", indices, {"slope_id": slope_id})


def ostrowski_selector(slope_id: str, template: str, count: int, max_n: int = 200000) -> SelectorInstance:
    indices = ostrowski_selector_indices(slope_id, template=template, count=count, max_n=max_n)
    return SelectorInstance(template, "ostrowski_definable", indices, {"slope_id": slope_id})


def beta_endpoint_selector(slope_id: str, count: int, suffix: str = "10", max_n: int = 200000) -> SelectorInstance:
    indices = endpoint_indices(slope_id, suffix=suffix, count=count, max_n=max_n)
    return SelectorInstance("beta_endpoint_suffix_10", "linear_recursive", indices, {"slope_id": slope_id, "suffix": suffix})


def smoke_selector_bank(count: int) -> dict[str, SelectorInstance]:
    return {
        "ap_2_0": arithmetic_progression("ap_2_0", step=2, offset=0, count=count),
        "ap_3_1": arithmetic_progression("ap_3_1", step=3, offset=1, count=count),
        "union_mod3_01": finite_union("union_mod3_01", modulus=3, residues=[0, 1], count=count),
        "fib_indices": fibonacci_indices(count),
        "pell_indices": pell_indices(count),
        "padovan_indices": padovan_indices(count),
    }
