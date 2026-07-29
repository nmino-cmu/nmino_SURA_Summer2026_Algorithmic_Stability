"""Multi-threshold — count of thresholds passed under equality-passes convention.

Operator: C_T(x) = |{ T ∈ T | x ≥ T }| for a finite list of thresholds.
Each coordinate reuses AboveThreshold with the same equality convention.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


OPERATOR = "multi-threshold"
THEOREM_ID = "multi-threshold-count-preservation"
EVALUATION_METHOD = "MULTI_THRESHOLD_PRESERVATION_COMPUTATIONAL_V1"

THEOREM_STATEMENT = (
    "Let x,x'∈ℝ, ε≥0 with |x'-x|≤ε, and let T=(T_0,…,T_{n-1}) be a finite list of "
    "finite thresholds. Define C_T(x)=|{i: x≥T_i}|. If for every i either "
    "x≥T_i+ε or x<T_i−ε, then C_T(x')=C_T(x)."
)

SHARPNESS_STATEMENT = (
    "If some index j satisfies x∈[T_j−ε,T_j+ε), then there exists admissible x' "
    "with |x'-x|≤ε and C_T(x')≠C_T(x) (flip the j-th AboveThreshold bit)."
)


def _require_finite(name: str, v: float) -> float:
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        raise ValueError(f"{name} must be a real number")
    fv = float(v)
    if not math.isfinite(fv):
        raise ValueError(f"{name} must be finite")
    return fv


def _require_thresholds(thresholds: Sequence[float]) -> tuple[float, ...]:
    if not isinstance(thresholds, (list, tuple)):
        raise ValueError("thresholds must be a list or tuple")
    out: list[float] = []
    for i, t in enumerate(thresholds):
        out.append(_require_finite(f"T[{i}]", t))
    return tuple(out)


@dataclass(frozen=True)
class MultiThresholdInstance:
    """Score x with finite threshold list T. Equality passes per coordinate."""

    x: float
    thresholds: tuple[float, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", _require_finite("x", self.x))
        object.__setattr__(self, "thresholds", _require_thresholds(self.thresholds))

    def decide(self) -> int:
        return sum(1 for t in self.thresholds if self.x >= t)

    def pass_bits(self) -> tuple[int, ...]:
        return tuple(1 if self.x >= t else 0 for t in self.thresholds)


def multi_threshold_count(x: float, thresholds: Sequence[float]) -> int:
    return MultiThresholdInstance(x, tuple(thresholds)).decide()


def coordinate_stable(x: float, t: float, epsilon: float) -> bool:
    """True iff AboveThreshold at t is preserved under |x'-x|≤ε."""
    x = _require_finite("x", x)
    t = _require_finite("t", t)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    return x >= t + epsilon or x < t - epsilon


def multi_stable(x: float, thresholds: Sequence[float], epsilon: float) -> bool:
    """Primary stability predicate: every coordinate is ε-stable."""
    ts = _require_thresholds(thresholds)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    x = _require_finite("x", x)
    return all(coordinate_stable(x, t, epsilon) for t in ts)


def stability_margin(x: float, thresholds: Sequence[float]) -> float:
    """Structural quantity: min one-sided buffer to each cut (∞ if n=0).

    For each T_i: if x≥T_i use (x-T_i); if x<T_i use (T_i-x) but fail side is
    strict, so the fail buffer that guarantees invariance for all ε'<buffer is
    reported as (T_i-x) with the understanding that ε must be < that buffer.
    For computational checks we use: min over i of abs distance, with fail-side
    requiring strict inequality handled in multi_stable.
    """
    x = _require_finite("x", x)
    ts = _require_thresholds(thresholds)
    if not ts:
        return math.inf
    return min(abs(x - t) for t in ts)


def unstable_index(x: float, thresholds: Sequence[float], epsilon: float) -> int | None:
    """First index in the half-open unstable band, else None."""
    x = _require_finite("x", x)
    ts = _require_thresholds(thresholds)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    for i, t in enumerate(ts):
        if (t - epsilon) <= x < (t + epsilon):
            return i
    return None


def adversarial_flip(
    x: float, thresholds: Sequence[float], epsilon: float
) -> float | None:
    """If some coordinate is unstable, return x' flipping that bit; else None."""
    x = _require_finite("x", x)
    ts = _require_thresholds(thresholds)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    j = unstable_index(x, ts, epsilon)
    if j is None:
        return None
    t = ts[j]
    if x >= t:
        # currently pass; push down
        return x - epsilon
    return x + epsilon
