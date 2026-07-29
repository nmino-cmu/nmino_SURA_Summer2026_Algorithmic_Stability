
"""Top-k — ranking-margin core (Real)."""
from __future__ import annotations
from operators.quantile.math import adversarial_tie, all_gaps_exceed, min_pairwise_gap

OPERATOR = "top-k"
THEOREM_ID = "top-k-margin"
EVALUATION_METHOD = "TOP_K_MARGIN_COMPUTATIONAL_V1"
THEOREM_STATEMENT = ('Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Top-k selection uses this ranking core.)')
SHARPNESS_STATEMENT = ('If some pair i≠j has |s_i−s_j|≤2ε, there exists ‖δ‖_∞≤ε forcing a value collision (ranking sharpness).')

def ranking_preserved(scores, epsilon):
    return all_gaps_exceed(scores, 2 * epsilon)

def top_k_indices(scores, k):
    n=len(scores)
    if not (1<=k<=n): raise ValueError("k in 1..n")
    order=sorted(range(n), key=lambda i: (-scores[i], i))
    return tuple(sorted(order[:k]))
