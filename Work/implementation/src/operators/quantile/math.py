"""Quantile selection via unique strict k-th order statistic (Real)."""

from __future__ import annotations

import math
from dataclasses import dataclass

OPERATOR = "quantile"
THEOREM_ID = "quantile-margin"
EVALUATION_METHOD = "QUANTILE_MARGIN_COMPUTATIONAL_V1"
THEOREM_STATEMENT = ('Let n≥2, s∈ℤ^n, k∈ℕ with k<n, ε≥0, and i a unique strict k-th smallest index (exactly k scores strictly below s_i and no other index shares s_i). If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then i remains the unique strict k-th smallest of s+δ. (Quantile selection uses this k-th order statistic core.)')
SHARPNESS_STATEMENT = ('If some rival j≠i has |s_i−s_j|≤2ε, there exists ‖δ‖_∞≤ε destroying unique strict k-th-smallest status of i.')


def _fin_scores(scores: tuple[float, ...]) -> tuple[float, ...]:
    if len(scores) < 2:
        raise ValueError("need n≥2")
    out = []
    for s in scores:
        if not isinstance(s, (int, float)) or isinstance(s, bool) or not math.isfinite(float(s)):
            raise ValueError("scores must be finite reals")
        out.append(float(s))
    return tuple(out)


def quantile_index(scores: tuple[float, ...], tau: float) -> int:
    """Lower τ-quantile index among distinct-value samples: k=floor(τ*(n-1))."""
    scores = _fin_scores(scores)
    if not (0.0 <= tau <= 1.0):
        raise ValueError("tau in [0,1]")
    n = len(scores)
    k = int(tau * (n - 1))
    order = sorted(range(n), key=lambda i: (scores[i], i))
    return order[k]


def count_lt(scores: tuple[float, ...], v: float) -> int:
    return sum(1 for s in scores if s < v)


def is_strict_kth(scores: tuple[float, ...], k: int, i: int) -> bool:
    scores = _fin_scores(scores)
    n = len(scores)
    if not (0 <= k < n and 0 <= i < n):
        return False
    if count_lt(scores, scores[i]) != k:
        return False
    return all(j == i or scores[j] != scores[i] for j in range(n))


def min_pairwise_gap(scores: tuple[float, ...]) -> float:
    scores = _fin_scores(scores)
    n = len(scores)
    g = float("inf")
    for i in range(n):
        for j in range(i + 1, n):
            g = min(g, abs(scores[i] - scores[j]))
    return g


def all_gaps_exceed(scores: tuple[float, ...], g: float) -> bool:
    return min_pairwise_gap(scores) > g


def invariance_holds(scores: tuple[float, ...], k: int, i: int, epsilon: float) -> bool:
    if epsilon < 0:
        raise ValueError("epsilon≥0")
    return is_strict_kth(scores, k, i) and all_gaps_exceed(scores, 2 * epsilon)


def adversarial_tie(scores: tuple[float, ...], i: int, j: int, epsilon: float) -> tuple[float, ...] | None:
    scores = _fin_scores(scores)
    if epsilon < 0 or i == j:
        return None
    d = scores[i] - scores[j]
    if abs(d) > 2 * epsilon:
        return None
    delta = [0.0] * len(scores)
    if d >= 0:
        if d <= epsilon:
            delta[i], delta[j] = -d, 0.0
        else:
            delta[i], delta[j] = -epsilon, d - epsilon
    else:
        if -d <= epsilon:
            delta[i], delta[j] = -d, 0.0
        else:
            delta[i], delta[j] = epsilon, d + epsilon
    return tuple(delta)
