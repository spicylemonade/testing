from __future__ import annotations

from special_numbers.slopes import continued_fraction_terms, convergents


def ostrowski_digits(slope_id: str, n: int, max_terms: int = 24) -> list[int]:
    terms = continued_fraction_terms(slope_id, max_terms)
    convs = convergents(slope_id, max_terms)
    denominators = [q for _index, _p, q in convs]
    while denominators and denominators[-1] > n:
        if len(denominators) == 1:
            break
        denominators.pop()
    if not denominators:
        return [0]

    digits = [0] * len(denominators)
    remaining = n
    for idx in range(len(denominators) - 1, -1, -1):
        a_limit_index = min(idx + 1, len(terms) - 1)
        limit = terms[a_limit_index]
        q_i = denominators[idx]
        digit = min(limit, remaining // q_i)
        digits[idx] = int(digit)
        remaining -= int(digit) * q_i
    return digits


def matches_template(digits: list[int], template: str) -> bool:
    if template == "ost_single_nonzero_digit":
        return sum(1 for digit in digits if digit != 0) == 1
    if template == "ost_suffix_01":
        return len(digits) >= 2 and digits[0] == 0 and digits[1] == 1
    if template == "ost_suffix_001":
        return len(digits) >= 3 and digits[0] == 0 and digits[1] == 0 and digits[2] == 1
    raise KeyError(template)


def ostrowski_selector_indices(slope_id: str, *, template: str, count: int, max_n: int) -> list[int]:
    indices: list[int] = []
    for n in range(1, max_n + 1):
        digits = ostrowski_digits(slope_id, n)
        if matches_template(digits, template):
            indices.append(n)
        if len(indices) >= count:
            break
    return indices
