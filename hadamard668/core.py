from __future__ import annotations

import cmath
from itertools import product
from pathlib import Path
from typing import Iterable, List, Sequence


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def support_from_bits(bits: Sequence[int]) -> List[int]:
    return [idx for idx, bit in enumerate(bits) if bit]


def bits_from_support(length: int, support: Iterable[int]) -> List[int]:
    support_set = set(int(idx) % length for idx in support)
    return [1 if idx in support_set else 0 for idx in range(length)]


def decode_base8_columns(encoded: str, columns: int = 3) -> List[List[int]]:
    cleaned = "".join(ch for ch in encoded if ch.isdigit())
    vectors = [[0] * len(cleaned) for _ in range(columns)]
    for idx, ch in enumerate(cleaned):
        value = int(ch)
        masks = [1 << bit for bit in reversed(range(columns))]
        for bit, mask in enumerate(masks):
            vectors[bit][idx] = 1 if value & mask else 0
    return vectors


def parse_run_length_notation(text: str) -> List[int]:
    cleaned = "".join(ch for ch in text if ch not in " \n\t")
    result: List[int] = []
    idx = 0
    while idx < len(cleaned):
        if cleaned[idx] == "(":
            end = cleaned.index(")", idx)
            pattern = [int(part) for part in cleaned[idx + 1 : end].split(",") if part]
            idx = end + 1
            repeat_digits = []
            while idx < len(cleaned) and cleaned[idx].isdigit():
                repeat_digits.append(cleaned[idx])
                idx += 1
            repeat = int("".join(repeat_digits)) if repeat_digits else 1
            for _ in range(repeat):
                result.extend(pattern)
            continue
        digits = []
        while idx < len(cleaned) and cleaned[idx].isdigit():
            digits.append(cleaned[idx])
            idx += 1
        if digits:
            result.extend(int(digit) for digit in digits)
            continue
        raise ValueError(f"Unexpected token in run-length notation near index {idx}: {cleaned[idx:]}")
    return result


def alternating_pm1_from_runs(runs: Sequence[int], start: int = 1) -> List[int]:
    if start not in (-1, 1):
        raise ValueError("start must be -1 or 1")
    value = start
    sequence: List[int] = []
    for run in runs:
        sequence.extend([value] * int(run))
        value *= -1
    return sequence


def involution_zero(sequence: Sequence[int]) -> List[int]:
    length = len(sequence)
    if length % 2 != 1:
        raise ValueError("involution_zero is only defined here for odd sequence lengths")
    half = length // 2 + 1
    return [
        int(sequence[idx]) if idx < half else -int(sequence[idx])
        for idx in range(length)
    ]


def pointwise_product(left: Sequence[int], right: Sequence[int]) -> List[int]:
    if len(left) != len(right):
        raise ValueError("pointwise_product requires equal-length sequences")
    return [int(a) * int(b) for a, b in zip(left, right)]


def periodic_binary_autocorrelation_half(bits: Sequence[int]) -> List[int]:
    length = len(bits)
    half = length // 2
    return [
        sum(int(bits[idx]) * int(bits[(idx + shift) % length]) for idx in range(length))
        for shift in range(1, half + 1)
    ]


def periodic_pm1_autocorrelation(bits: Sequence[int]) -> List[int]:
    length = len(bits)
    return [
        sum(int(bits[idx]) * int(bits[(idx + shift) % length]) for idx in range(length))
        for shift in range(1, length)
    ]


def aperiodic_pm1_autocorrelation(bits: Sequence[int]) -> List[int]:
    length = len(bits)
    return [
        sum(int(bits[idx]) * int(bits[idx + shift]) for idx in range(length - shift))
        for shift in range(1, length)
    ]


def combined_aperiodic_pm1_autocorrelation(sequences: Sequence[Sequence[int]]) -> List[int]:
    if not sequences:
        return []
    length = len(sequences[0])
    if any(len(seq) != length for seq in sequences):
        raise ValueError("combined_aperiodic_pm1_autocorrelation requires equal-length sequences")
    combined = [0] * (length - 1)
    for sequence in sequences:
        corr = aperiodic_pm1_autocorrelation(sequence)
        combined = [left + right for left, right in zip(combined, corr)]
    return combined


def two_adic_modulus(values: Sequence[int]) -> int:
    nonzero = [abs(int(value)) for value in values if int(value) != 0]
    if not nonzero:
        return 0
    modulus = min(value & -value for value in nonzero)
    power = 1
    while power * 2 <= modulus:
        power *= 2
    return power


def l1_distance(left: Sequence[int], right: Sequence[int]) -> int:
    if len(left) != len(right):
        raise ValueError("l1_distance requires equal-length sequences")
    return sum(abs(int(a) - int(b)) for a, b in zip(left, right))


def max_abs(values: Sequence[int]) -> int:
    return max((abs(int(value)) for value in values), default=0)


def cyclic_canonical_binary(bits: Sequence[int]) -> str:
    text = "".join(str(int(bit)) for bit in bits)
    rev = text[::-1]
    variants = []
    for candidate in (text, rev):
        variants.extend(candidate[idx:] + candidate[:idx] for idx in range(len(candidate)))
    return min(variants)


def power_spectral_density(bits: Sequence[int]) -> List[float]:
    length = len(bits)
    values: List[float] = []
    for freq in range(length):
        total = sum(
            int(bits[idx]) * cmath.exp(-2j * cmath.pi * freq * idx / length)
            for idx in range(length)
        )
        values.append(float((total.real * total.real) + (total.imag * total.imag)))
    return values


def pm1_text(sequence: Sequence[int]) -> str:
    return "".join("+" if int(value) > 0 else "-" for value in sequence)


def signed_reversal_canonical_tuple(sequences: Sequence[Sequence[int]]) -> str:
    variants = []
    for reverse in (False, True):
        base = [
            list(reversed(sequence)) if reverse else list(sequence)
            for sequence in sequences
        ]
        for signs in product((-1, 1), repeat=len(base)):
            variant = [
                pm1_text(sign * int(value) for value in sequence)
                for sign, sequence in zip(signs, base)
            ]
            variants.append("|".join(variant))
    return min(variants)
