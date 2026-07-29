"""Absolute-value threshold: A(x)=1{|x|≥T} for T≥0, equality passes."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

OPERATOR = "absolute-value-threshold"
THEOREM_ID = "abs-threshold-preservation"
EVALUATION_METHOD = "ABS_THRESHOLD_PRESERVATION_COMPUTATIONAL_V1"
THEOREM_STATEMENT = (
    "Let x,x'∈ℝ, ε≥0 with |x'-x|≤ε, and T≥0. Define A(x)=1{|x|≥T}. "
    "(1) if |x|≥T+ε then A(x')=1; (2) if |x|+ε<T then A(x')=0."
)
SHARPNESS_STATEMENT = (
    "If ε≤x and T≤x<T+ε (nonnegative ray with room to push toward 0 without crossing), "
    "then x'=x−ε is admissible and A(x')=0."
)


def _fin(name: str, v: float) -> float:
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        raise ValueError(f"{name} must be a real number")
    fv = float(v)
    if not math.isfinite(fv):
        raise ValueError(f"{name} must be finite")
    return fv


@dataclass(frozen=True)
class AbsThresholdInstance:
    x: float
    T: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", _fin("x", self.x))
        t = _fin("T", self.T)
        if t < 0:
            raise ValueError("T must be ≥ 0")
        object.__setattr__(self, "T", t)

    def decide(self) -> Literal[0, 1]:
        return 1 if abs(self.x) >= self.T else 0


def abs_threshold(x: float, T: float) -> Literal[0, 1]:
    return AbsThresholdInstance(x, T).decide()


def pass_preserved(x: float, T: float, epsilon: float) -> bool:
    x, T, epsilon = _fin("x", x), _fin("T", T), _fin("epsilon", epsilon)
    if T < 0 or epsilon < 0:
        raise ValueError("T,epsilon must be ≥ 0")
    return abs(x) >= T + epsilon


def fail_preserved(x: float, T: float, epsilon: float) -> bool:
    x, T, epsilon = _fin("x", x), _fin("T", T), _fin("epsilon", epsilon)
    if T < 0 or epsilon < 0:
        raise ValueError("T,epsilon must be ≥ 0")
    return abs(x) + epsilon < T


def abs_stable(x: float, T: float, epsilon: float) -> bool:
    return pass_preserved(x, T, epsilon) or fail_preserved(x, T, epsilon)


def adversarial_flip(x: float, T: float, epsilon: float) -> float | None:
    """Sharpness witness on the nonnegative ray when ε≤x and T≤x<T+ε."""
    x, T, epsilon = _fin("x", x), _fin("T", T), _fin("epsilon", epsilon)
    if T < 0 or epsilon < 0:
        raise ValueError("T,epsilon must be ≥ 0")
    if epsilon <= x and T <= x < T + epsilon:
        return x - epsilon
    return None
