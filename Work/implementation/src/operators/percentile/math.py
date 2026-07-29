"""Percentile — unique strict k-th order statistic (Real)."""

from __future__ import annotations

from operators.quantile.math import (
    adversarial_tie,
    all_gaps_exceed,
    count_lt,
    invariance_holds,
    is_strict_kth,
    min_pairwise_gap,
    quantile_index,
)

OPERATOR = "percentile"
THEOREM_ID = "percentile-margin"
EVALUATION_METHOD = "PERCENTILE_MARGIN_COMPUTATIONAL_V1"
THEOREM_STATEMENT = ('Let n≥2, s∈ℤ^n, k∈ℕ with k<n, ε≥0, and i a unique strict k-th smallest index (exactly k scores strictly below s_i and no other index shares s_i). If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then i remains the unique strict k-th smallest of s+δ. (Percentile selection uses this k-th order statistic core.)')
SHARPNESS_STATEMENT = ('If some rival j≠i has |s_i−s_j|≤2ε, there exists ‖δ‖_∞≤ε destroying unique strict k-th-smallest status of i.')

__all__ = [
    "OPERATOR", "THEOREM_ID", "EVALUATION_METHOD", "THEOREM_STATEMENT", "SHARPNESS_STATEMENT",
    "is_strict_kth", "invariance_holds", "adversarial_tie", "all_gaps_exceed",
    "min_pairwise_gap", "count_lt", "quantile_index",
]
