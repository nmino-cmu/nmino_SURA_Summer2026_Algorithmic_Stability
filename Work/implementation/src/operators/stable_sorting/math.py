"""Stable sorting — ranking-margin core (Real)."""
from __future__ import annotations
from operators.top_k.math import adversarial_tie, all_gaps_exceed, min_pairwise_gap, ranking_preserved

OPERATOR = "stable-sorting"
THEOREM_ID = "stable-sorting-margin"
EVALUATION_METHOD = "STABLE_SORTING_MARGIN_COMPUTATIONAL_V1"
THEOREM_STATEMENT = ('Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Stable sorting uses this ranking core.)')
SHARPNESS_STATEMENT = ('If some pair i≠j has |s_i−s_j|≤2ε, there exists ‖δ‖_∞≤ε forcing a value collision (ranking sharpness).')
