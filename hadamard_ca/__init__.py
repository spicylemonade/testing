"""Hadamard 668 cellular-automata research helpers."""

from .seed import (
    EXPECTED_EXCEPTIONAL_COEFFICIENTS,
    FRONTIER_PDF_SHA256,
    FRONTIER_PDF_URL,
    gs_matrix,
    published_frontier_coefficients,
    published_frontier_sequences,
    published_frontier_validation,
)
from .harness import SearchConfig, SearchResult, evaluate_state, objective_summary, run_harness

__all__ = [
    "EXPECTED_EXCEPTIONAL_COEFFICIENTS",
    "FRONTIER_PDF_SHA256",
    "FRONTIER_PDF_URL",
    "SearchConfig",
    "SearchResult",
    "evaluate_state",
    "gs_matrix",
    "objective_summary",
    "published_frontier_coefficients",
    "published_frontier_sequences",
    "published_frontier_validation",
    "run_harness",
]
