"""Interval-membership selection: I(x)=1{L ≤ x ≤ U}, equality included."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

OPERATOR = "interval-membership"
THEOREM_ID = "interval-membership-preservation"
EVALUATION_METHOD = "INTERVAL_MEMBERSHIP_PRESERVATION_COMPUTATIONAL_V1"
THEOREM_STATEMENT = (
    "Let x,x'∈ℝ, ε≥0 with |x'-x|≤ε, and L≤U. Define I(x)=1{L≤x≤U}. "
    "(1) if L+ε≤x≤U−ε then I(x')=1; "
    "(2) if x<L−ε or x>U+ε then I(x')=0."
)
SHARPNESS_STATEMENT = (
    "If L≤x<L+ε then some admissible x' has I(x')=0; "
    "if U−ε<x≤U then some admissible x' has I(x')=0; "
    "if L−ε≤x<L then some admissible x' has I(x')=1; "
    "if U<x≤U+ε then some admissible x' has I(x')=1."
)


def _fin(name: str, v: float) -> float:
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        raise ValueError(f"{name} must be a real number")
    fv = float(v)
    if not math.isfinite(fv):
        raise ValueError(f"{name} must be finite")
    return fv


@dataclass(frozen=True)
class IntervalInstance:
    x: float
    L: float
    U: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", _fin("x", self.x))
        L, U = _fin("L", self.L), _fin("U", self.U)
        if L > U:
            raise ValueError("require L ≤ U")
        object.__setattr__(self, "L", L)
        object.__setattr__(self, "U", U)

    def decide(self) -> Literal[0, 1]:
        return 1 if self.L <= self.x <= self.U else 0


def interval_membership(x: float, L: float, U: float) -> Literal[0, 1]:
    return IntervalInstance(x, L, U).decide()


def pass_preserved(x: float, L: float, U: float, epsilon: float) -> bool:
    x, L, U, epsilon = _fin("x", x), _fin("L", L), _fin("U", U), _fin("epsilon", epsilon)
    if L > U or epsilon < 0:
        raise ValueError("require L≤U and ε≥0")
    return L + epsilon <= x <= U - epsilon


def fail_preserved(x: float, L: float, U: float, epsilon: float) -> bool:
    x, L, U, epsilon = _fin("x", x), _fin("L", L), _fin("U", U), _fin("epsilon", epsilon)
    if L > U or epsilon < 0:
        raise ValueError("require L≤U and ε≥0")
    return x < L - epsilon or x > U + epsilon


def adversarial_flip(x: float, L: float, U: float, epsilon: float) -> float | None:
    x, L, U, epsilon = _fin("x", x), _fin("L", L), _fin("U", U), _fin("epsilon", epsilon)
    if L > U or epsilon < 0:
        raise ValueError("require L≤U and ε≥0")
    if pass_preserved(x, L, U, epsilon) or fail_preserved(x, L, U, epsilon):
        return None
    inside = L <= x <= U
    if inside:
        # exit via nearer endpoint push of size ε
        if x - L <= U - x:
            return x - epsilon
        return x + epsilon
    # outside unstable: move onto the nearer endpoint (guarantees entry even for narrow intervals)
    if x < L:
        return L
    return U
