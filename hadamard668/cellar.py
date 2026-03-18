from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from hadamard668.artifacts import ELIAHOU_Q, ELIAHOU_S, build_control_79, build_seed_668_mod64, build_target_167
from hadamard668.core import (
    alternating_pm1_from_runs,
    bits_from_support,
    cyclic_canonical_binary,
    parse_run_length_notation,
    periodic_binary_autocorrelation_half,
)
from hadamard668.h1 import projected_pm1_seed
from hadamard668.verifiers import structured_qs_state


RESULTS_DIR = Path("results/experiments")


@dataclass(frozen=True)
class TailPanel:
    label: str
    length: int
    weight: int
    target: Tuple[int, ...]
    base_prefix: Tuple[int, ...]
    free_suffix_length: int
    anchor_kind: str
    anchor_label: str
    canonical_anchor_bits: Tuple[int, ...]

    @property
    def base_length(self) -> int:
        return len(self.base_prefix)

    @property
    def half(self) -> int:
        return self.length // 2


@dataclass(frozen=True)
class PrefixRecord:
    free_prefix: Tuple[int, ...]
    extendable: bool
    completion_indices: Tuple[int, ...]

    @property
    def depth(self) -> int:
        return len(self.free_prefix)


@dataclass(frozen=True)
class BlockSummary:
    length: int
    weight: int
    bits: str
    prefix_bits: str
    suffix_bits: str
    internal_pairs: Tuple[int, ...]

    def to_key(self) -> Tuple[object, ...]:
        return (
            self.length,
            self.weight,
            self.bits,
            self.prefix_bits,
            self.suffix_bits,
            self.internal_pairs,
        )


def canonical_bits(bits: Sequence[int]) -> List[int]:
    return [int(ch) for ch in cyclic_canonical_binary(bits)]


def _full_bits_from_prefix(panel: TailPanel, free_prefix: Sequence[int], fill: int = 0) -> List[int]:
    if len(free_prefix) > panel.free_suffix_length:
        raise ValueError("free_prefix exceeds the panel free suffix length")
    suffix = [int(fill)] * (panel.free_suffix_length - len(free_prefix))
    return [int(value) for value in panel.base_prefix] + [int(value) for value in free_prefix] + suffix


def make_tail_panel(
    *,
    label: str,
    full_bits: Sequence[int],
    weight: int,
    target: Sequence[int],
    free_suffix_length: int,
    anchor_kind: str,
    anchor_label: str,
) -> TailPanel:
    canonical = canonical_bits(full_bits)
    if sum(canonical) != int(weight):
        raise ValueError("canonical anchor has the wrong weight")
    if free_suffix_length <= 0 or free_suffix_length >= len(canonical):
        raise ValueError("free_suffix_length must be in the open interval (0, length)")
    base_prefix = canonical[:-free_suffix_length]
    if len(base_prefix) <= (len(canonical) // 2):
        raise ValueError("tail panels must fix more than half the word for the boundary theorem")
    return TailPanel(
        label=label,
        length=len(canonical),
        weight=int(weight),
        target=tuple(int(value) for value in target),
        base_prefix=tuple(int(value) for value in base_prefix),
        free_suffix_length=free_suffix_length,
        anchor_kind=anchor_kind,
        anchor_label=anchor_label,
        canonical_anchor_bits=tuple(int(value) for value in canonical),
    )


def all_panel_prefixes(panel: TailPanel) -> List[Tuple[int, ...]]:
    total_free_weight = panel.weight - sum(panel.base_prefix)
    prefixes: List[Tuple[int, ...]] = [tuple()]
    for depth in range(1, panel.free_suffix_length + 1):
        for mask in range(1 << depth):
            prefix = tuple(1 if mask & (1 << idx) else 0 for idx in range(depth))
            used = sum(prefix)
            remaining_slots = panel.free_suffix_length - depth
            if used > total_free_weight:
                continue
            if used + remaining_slots < total_free_weight:
                continue
            prefixes.append(prefix)
    return prefixes


def exact_completions(panel: TailPanel) -> List[Tuple[int, ...]]:
    total_free_weight = panel.weight - sum(panel.base_prefix)
    completions: List[Tuple[int, ...]] = []
    for ones in combinations(range(panel.free_suffix_length), total_free_weight):
        tail = [0] * panel.free_suffix_length
        for index in ones:
            tail[index] = 1
        full_bits = [int(value) for value in panel.base_prefix] + tail
        if periodic_binary_autocorrelation_half(full_bits) == list(panel.target):
            completions.append(tuple(tail))
    return completions


def prefix_records(panel: TailPanel) -> List[PrefixRecord]:
    completions = exact_completions(panel)
    prefixes = all_panel_prefixes(panel)
    records: List[PrefixRecord] = []
    for prefix in prefixes:
        matching = tuple(
            index
            for index, completion in enumerate(completions)
            if completion[: len(prefix)] == prefix
        )
        records.append(
            PrefixRecord(
                free_prefix=prefix,
                extendable=bool(matching),
                completion_indices=matching,
            )
        )
    return records


def boundary_debt_state(panel: TailPanel, free_prefix: Sequence[int]) -> Dict[str, object]:
    assigned = _full_bits_from_prefix(panel, free_prefix, fill=0)
    assigned_length = panel.base_length + len(free_prefix)
    assigned_bits = assigned[:assigned_length]
    return {
        "free_prefix_length": len(free_prefix),
        "assigned_length": assigned_length,
        "assigned_weight": sum(assigned_bits),
        "remaining_weight": panel.weight - sum(assigned_bits),
        "assigned_pairs": periodic_binary_autocorrelation_half(assigned),
        "left_boundary_bits": [int(value) for value in panel.base_prefix[: panel.half]],
        "right_boundary_bits": [int(value) for value in assigned_bits[-panel.half :]],
    }


def boundary_debt_key(panel: TailPanel, free_prefix: Sequence[int]) -> str:
    return json.dumps(boundary_debt_state(panel, free_prefix), sort_keys=True, separators=(",", ":"))


def _block_internal_pairs(bits: Sequence[int], horizon: int) -> Tuple[int, ...]:
    values: List[int] = []
    length = len(bits)
    for shift in range(1, horizon + 1):
        if shift >= length:
            values.append(0)
            continue
        values.append(sum(int(bits[idx]) * int(bits[idx + shift]) for idx in range(length - shift)))
    return tuple(values)


def make_block_summary(bits: Sequence[int], horizon: int) -> BlockSummary:
    text = "".join(str(int(value)) for value in bits)
    return BlockSummary(
        length=len(bits),
        weight=sum(int(value) for value in bits),
        bits=text,
        prefix_bits=text[:horizon],
        suffix_bits=text[-horizon:] if horizon else "",
        internal_pairs=_block_internal_pairs(bits, horizon),
    )


def merge_block_summaries(left: BlockSummary, right: BlockSummary, horizon: int) -> BlockSummary:
    bits = [int(ch) for ch in left.bits + right.bits]
    return make_block_summary(bits, horizon)


def dyadic_block_stack(free_prefix: Sequence[int], horizon: int) -> List[BlockSummary]:
    stack: List[BlockSummary] = []
    for bit in free_prefix:
        stack.append(make_block_summary([int(bit)], horizon=horizon))
        while len(stack) >= 2 and stack[-1].length == stack[-2].length:
            right = stack.pop()
            left = stack.pop()
            stack.append(merge_block_summaries(left, right, horizon=horizon))
    return stack


def cellar_state(panel: TailPanel, free_prefix: Sequence[int]) -> Dict[str, object]:
    return {
        "control_state": boundary_debt_state(panel, free_prefix),
        "stack": [
            {
                "length": block.length,
                "weight": block.weight,
                "bits": block.bits,
                "prefix_bits": block.prefix_bits,
                "suffix_bits": block.suffix_bits,
                "internal_pairs": list(block.internal_pairs),
            }
            for block in dyadic_block_stack(free_prefix, panel.half)
        ],
    }


def cellar_key(panel: TailPanel, free_prefix: Sequence[int]) -> str:
    return json.dumps(cellar_state(panel, free_prefix), sort_keys=True, separators=(",", ":"))


def signature_report(
    panel: TailPanel,
    records: Sequence[PrefixRecord],
    *,
    signature_name: str,
    signature_fn,
) -> Dict[str, object]:
    groups: Dict[str, List[PrefixRecord]] = {}
    for record in records:
        groups.setdefault(str(signature_fn(panel, record.free_prefix)), []).append(record)
    frontier_size = 0
    positive_groups = 0
    mixed_examples: List[Dict[str, object]] = []
    completion_mixed_examples: List[Dict[str, object]] = []
    for key, group in groups.items():
        positives = [record for record in group if record.extendable]
        negatives = [record for record in group if not record.extendable]
        if positives:
            frontier_size += len(group)
            positive_groups += 1
        if positives and negatives and len(mixed_examples) < 5:
            mixed_examples.append(
                {
                    "signature": key,
                    "extendable_prefixes": [list(record.free_prefix) for record in positives[:3]],
                    "nonextendable_prefixes": [list(record.free_prefix) for record in negatives[:3]],
                }
            )
        completion_sets = {record.completion_indices for record in group}
        if len(completion_sets) > 1 and len(completion_mixed_examples) < 5:
            completion_mixed_examples.append(
                {
                    "signature": key,
                    "completion_sets": [list(values) for values in sorted(completion_sets)],
                    "prefix_examples": [list(record.free_prefix) for record in group[:5]],
                }
            )
    extendable_count = sum(1 for record in records if record.extendable)
    return {
        "signature_name": signature_name,
        "group_count": len(groups),
        "positive_group_count": positive_groups,
        "extendable_prefix_count": extendable_count,
        "frontier_size": frontier_size,
        "frontier_ratio_vs_exact": (frontier_size / float(extendable_count)) if extendable_count else None,
        "pure": not mixed_examples,
        "mixed_example_count": len(mixed_examples),
        "mixed_examples": mixed_examples,
        "completion_set_pure": not completion_mixed_examples,
        "completion_mixed_example_count": len(completion_mixed_examples),
        "completion_mixed_examples": completion_mixed_examples,
    }


def panel_report(panel: TailPanel) -> Dict[str, object]:
    completions = exact_completions(panel)
    records = prefix_records(panel)
    boundary_report = signature_report(
        panel,
        records,
        signature_name="boundary_debt",
        signature_fn=boundary_debt_key,
    )
    cellar_report = signature_report(
        panel,
        records,
        signature_name="cellar_stack",
        signature_fn=cellar_key,
    )
    extendable_prefixes = [record.free_prefix for record in records if record.extendable]
    longest_prefix = max((len(prefix) for prefix in extendable_prefixes), default=0)
    return {
        "label": panel.label,
        "anchor_kind": panel.anchor_kind,
        "anchor_label": panel.anchor_label,
        "length": panel.length,
        "weight": panel.weight,
        "base_length": panel.base_length,
        "free_suffix_length": panel.free_suffix_length,
        "target_half_length": panel.half,
        "canonical_anchor_bits": list(panel.canonical_anchor_bits),
        "base_prefix": list(panel.base_prefix),
        "exact_completion_count": len(completions),
        "exact_completions": [list(completion) for completion in completions[:8]],
        "prefix_count": len(records),
        "extendable_prefix_count": len(extendable_prefixes),
        "longest_extendable_prefix_depth": longest_prefix,
        "boundary_debt_report": boundary_report,
        "cellar_report": cellar_report,
        "control_state_example": (
            boundary_debt_state(panel, completions[0][: min(4, len(completions[0]))])
            if completions
            else boundary_debt_state(panel, tuple())
        ),
        "cellar_state_example": (
            cellar_state(panel, completions[0][: min(4, len(completions[0]))])
            if completions
            else cellar_state(panel, tuple())
        ),
    }


def control_79_panel(free_suffix_length: int = 12) -> TailPanel:
    artifact = build_control_79()
    full_bits = bits_from_support(79, artifact["solution"]["support"])
    return make_tail_panel(
        label=f"control_4x79_tail{free_suffix_length}",
        full_bits=full_bits,
        weight=int(artifact["solution"]["weight"]),
        target=[int(value) for value in artifact["target_periodic_autocorrelation_half"]],
        free_suffix_length=free_suffix_length,
        anchor_kind="exact_control",
        anchor_label="control_4x79_solution",
    )


def top_h1_target_panels(limit: int = 6, free_suffix_length: int = 12) -> List[TailPanel]:
    runs_path = Path("results/experiments/h1_target_sweep.json")
    if not runs_path.exists():
        return []
    runs = json.loads(runs_path.read_text()).get("runs", [])
    target = build_target_167()
    seen: set[str] = set()
    panels: List[TailPanel] = []
    ordered = sorted(
        runs,
        key=lambda run: (
            int(run["best_state"]["closest_target_distance"]),
            int(run["best_state"]["max_defect_magnitude"]),
            str(run["method"]),
            int(run["deterministic_seed"]),
        ),
    )
    for run in ordered:
        support = [int(value) for value in run["best_state"]["support"]]
        full_bits = bits_from_support(167, support)
        canonical = "".join(str(value) for value in canonical_bits(full_bits))
        if canonical in seen:
            continue
        seen.add(canonical)
        label = (
            f"target_167_tail{free_suffix_length}::"
            f"{run['method']}::{run['seed_family']}::{run['deterministic_seed']}"
        )
        panels.append(
            make_tail_panel(
                label=label,
                full_bits=full_bits,
                weight=int(target["unknown_vector"]["required_weight"]),
                target=[int(value) for value in target["target_periodic_autocorrelation_half"]],
                free_suffix_length=free_suffix_length,
                anchor_kind="h1_target_best",
                anchor_label=f"{run['method']}::{run['seed_family']}::{run['deterministic_seed']}",
            )
        )
        if len(panels) >= limit:
            break
    return panels


def seed_projection_panels(free_suffix_length: int = 12) -> List[TailPanel]:
    target = build_target_167()
    q = alternating_pm1_from_runs(parse_run_length_notation(ELIAHOU_Q), start=1)
    s = alternating_pm1_from_runs(parse_run_length_notation(ELIAHOU_S), start=1)
    panels: List[TailPanel] = []

    def add_panel(label_suffix: str, anchor_label: str, degraded_s: Sequence[int]) -> None:
        projection = projected_pm1_seed(
            degraded_s,
            int(target["unknown_vector"]["required_weight"]),
            0,
        )
        panels.append(
            make_tail_panel(
                label=f"seed_projection_tail{free_suffix_length}::{label_suffix}",
                full_bits=projection["bits"],
                weight=int(target["unknown_vector"]["required_weight"]),
                target=[int(value) for value in target["target_periodic_autocorrelation_half"]],
                free_suffix_length=free_suffix_length,
                anchor_kind="seed_projection",
                anchor_label=anchor_label,
            )
        )

    def single_flip_state(index: int) -> Dict[str, object]:
        degraded = list(s)
        degraded[index] *= -1
        state = structured_qs_state(q, degraded, target_modulus=64)
        return {
            "index": index,
            "two_adic_modulus": int(state["two_adic_modulus"]),
            "degraded_s": degraded,
        }

    def clustered_state(start: int, width: int) -> Dict[str, object]:
        degraded = list(s)
        touched = []
        for offset in range(width):
            index = (start + offset) % len(degraded)
            degraded[index] *= -1
            touched.append(index)
        state = structured_qs_state(q, degraded, target_modulus=64)
        return {
            "indices": touched,
            "width": width,
            "two_adic_modulus": int(state["two_adic_modulus"]),
            "degraded_s": degraded,
        }

    best_single = min((single_flip_state(index) for index in range(len(s))), key=lambda item: (item["two_adic_modulus"], item["index"]))
    best_cluster3 = min((clustered_state(start, 3) for start in range(len(s))), key=lambda item: (item["two_adic_modulus"], item["indices"][0]))
    best_cluster5 = min((clustered_state(start, 5) for start in range(len(s))), key=lambda item: (item["two_adic_modulus"], item["indices"][0]))

    h2_flip = list(s)
    h2_flip[41] *= -1

    add_panel(
        label_suffix=f"single_flip_{best_single['index']}_mod{best_single['two_adic_modulus']}",
        anchor_label=f"eliahou_s_single_flip_{best_single['index']}_mod{best_single['two_adic_modulus']}",
        degraded_s=best_single["degraded_s"],
    )
    add_panel(
        label_suffix="single_flip_41_mod16",
        anchor_label="eliahou_s_single_flip_41_mod16",
        degraded_s=h2_flip,
    )
    add_panel(
        label_suffix=f"cluster3_{best_cluster3['indices'][0]}_{best_cluster3['indices'][-1]}_mod{best_cluster3['two_adic_modulus']}",
        anchor_label=(
            f"eliahou_s_cluster3_{best_cluster3['indices'][0]}_{best_cluster3['indices'][-1]}_mod{best_cluster3['two_adic_modulus']}"
        ),
        degraded_s=best_cluster3["degraded_s"],
    )
    add_panel(
        label_suffix=f"cluster5_{best_cluster5['indices'][0]}_{best_cluster5['indices'][-1]}_mod{best_cluster5['two_adic_modulus']}",
        anchor_label=(
            f"eliahou_s_cluster5_{best_cluster5['indices'][0]}_{best_cluster5['indices'][-1]}_mod{best_cluster5['two_adic_modulus']}"
        ),
        degraded_s=best_cluster5["degraded_s"],
    )
    return panels


def regularity_claim() -> Dict[str, object]:
    return {
        "name": "Tail-panel regularity hypothesis via boundary debt",
        "status": "conservative_no_go",
        "claim": (
            "On the exact tail-panel encoding used here, no stack-only split beyond the static boundary-debt control "
            "state was observed. The strongest supported claim is a no-go for the literal cellar branch under this "
            "encoding, not a universal theorem about all possible coarser static summaries."
        ),
        "proof_sketch": [
            "All future assignments lie in one contiguous suffix interval.",
            "For each cyclic shift k <= floor(n/2), every contribution involving an unread bit is either a suffix-internal pair, a pair crossing the current panel boundary, or a wrap pair back into the fixed left boundary.",
            "Suffix-internal pairs depend only on unread bits, crossing pairs depend only on the right boundary pattern of the assigned prefix, and wrap pairs depend only on the fixed left boundary pattern.",
            "All contributions already committed inside the assigned region are captured by the assigned pair vector.",
            "This motivates the boundary-debt control state as a sufficient exact residual summary for the recorded panels, but the current empirical packet only checks completion-set purity under the implemented encoding."
        ],
        "caveat": (
            "The implemented boundary-debt state is strong and can be prefix-identifying on the recorded panels. "
            "So the current result retires the cellar branch under this exact encoding, but does not yet prove that "
            "every weaker static summary would match the cellar stack."
        ),
    }


def exposed_prefix_indices(length: int, cut: int) -> List[int]:
    half = length // 2
    exposed: set[int] = set()
    for shift in range(1, half + 1):
        exposed.update(range(min(shift, cut)))
        exposed.update(range(max(0, cut - shift), cut))
    return sorted(exposed)


def exposure_report(length: int) -> Dict[str, object]:
    cuts: List[Dict[str, object]] = []
    all_full = True
    for cut in range(1, length):
        exposed = exposed_prefix_indices(length, cut)
        full = exposed == list(range(cut))
        all_full = all_full and full
        if cut in {1, length // 4, length // 2, length - 1}:
            cuts.append(
                {
                    "cut": cut,
                    "exposed_count": len(exposed),
                    "prefix_count": cut,
                    "all_prefix_bits_exposed": full,
                }
            )
    return {
        "length": length,
        "all_cuts_have_full_exposure": all_full,
        "sample_cuts": cuts,
    }


def run_analysis(
    *,
    control_free_suffix_length: int = 12,
    target_free_suffix_length: int = 12,
    target_limit: int = 6,
) -> Dict[str, object]:
    control_panel = control_79_panel(free_suffix_length=control_free_suffix_length)
    target_panels = top_h1_target_panels(limit=target_limit, free_suffix_length=target_free_suffix_length)
    seed_panels = seed_projection_panels(free_suffix_length=target_free_suffix_length)
    panel_reports = [panel_report(control_panel)]
    panel_reports.extend(panel_report(panel) for panel in target_panels)
    panel_reports.extend(panel_report(panel) for panel in seed_panels)
    return {
        "regularity_claim": regularity_claim(),
        "design": {
            "canonical_tokenization": (
                "Use the canonical dihedral bitstring of the support, then scan the free suffix left-to-right. "
                "After each appended bit, a dyadic carry schedule merges equal-size cellars, producing a visibly "
                "pushdown-style stack of contiguous block summaries."
            ),
            "control_state": (
                "Boundary debt: assigned pair vector, left boundary bits, right boundary bits, "
                "assigned/remaining weight, and assigned/free prefix length."
            ),
            "stack_alphabet": (
                "Dyadic block summaries carrying block length, weight, internal linear pair vector, "
                "and block prefix/suffix bit patterns."
            ),
            "acceptance_condition": (
                "Accept a prefix when its boundary-debt control state belongs to an extendable class; "
                "the cellar stack refines this state but no extra split was observed on the recorded exact tail panels."
            ),
            "matched_static_comparator": (
                "The static comparator uses the same canonical tokenization, the same exact tail-completion oracle, "
                "the same fixed panel budget, and the same equivalence accounting, but discards the cellar stack "
                "and keeps only the boundary-debt control state."
            ),
        },
        "exposure_reports": [
            exposure_report(79),
            exposure_report(167),
        ],
        "panels": panel_reports,
    }


def write_json(path: Path, payload: Mapping[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))
    return path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze tail-panel cellar automata on the Hadamard 668 anchors.")
    parser.add_argument("--output", type=Path, default=RESULTS_DIR / "cellar_phase6.json")
    parser.add_argument("--control-free-suffix", type=int, default=12)
    parser.add_argument("--target-free-suffix", type=int, default=12)
    parser.add_argument("--target-limit", type=int, default=6)
    args = parser.parse_args(argv)
    payload = run_analysis(
        control_free_suffix_length=args.control_free_suffix,
        target_free_suffix_length=args.target_free_suffix,
        target_limit=args.target_limit,
    )
    write_json(args.output, payload)
    print(str(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
