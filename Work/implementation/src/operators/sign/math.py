"""Sign selection — trichotomy on a scalar score.

sign(x) ∈ {-1,0,1}: +1 if x>0, -1 if x<0, 0 if x=0.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

OPERATOR = "sign"
THEOREM_ID = "sign-preservation"
EVALUATION_METHOD = "SIGN_PRESERVATION_COMPUTATIONAL_V1"

THEOREM_STATEMENT = (
    "Let x,x'∈ℝ and ε≥0 with |x'-x|≤ε. Define sign(x)=1 if x>0, -1 if x<0, else 0. "
    "(1) if x>ε then sign(x')=1; (2) if x<-ε then sign(x')=-1; "
    "(3) if ε=0 and x=0 then sign(x')=0."
)

SHARPNESS_STATEMENT = (
    "If 0≤x≤ε and not (x>ε), some admissible x' has sign(x')≠1 when the clean sign is 1 "
    "or when x=0 with ε>0; symmetrically on the negative side. "
    "Explicitly: if 0<x≤ε then x'=x-ε≤0 flips +; if -ε≤x<0 then x'=x+ε≥0 flips -; "
    "if x=0 and ε>0 then x'=ε yields +1."
)


def _require_finite(name: str, v: float) -> float:
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        raise ValueError(f"{name} must be a real number")
    fv = float(v)
    if not math.isfinite(fv):
        raise ValueError(f"{name} must be finite")
    return fv


SignValue = Literal[-1, 0, 1]


@dataclass(frozen=True)
class SignInstance:
    x: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", _require_finite("x", self.x))

    def decide(self) -> SignValue:
        if self.x > 0:
            return 1
        if self.x < 0:
            return -1
        return 0


def sign_select(x: float) -> SignValue:
    return SignInstance(x).decide()


def plus_preserved(x: float, epsilon: float) -> bool:
    x = _require_finite("x", x)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    return x > epsilon


def minus_preserved(x: float, epsilon: float) -> bool:
    x = _require_finite("x", x)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    return x < -epsilon


def zero_preserved(x: float, epsilon: float) -> bool:
    x = _require_finite("x", x)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    return epsilon == 0 and x == 0


def sign_stable(x: float, epsilon: float) -> bool:
    s = sign_select(x)
    if s == 1:
        return plus_preserved(x, epsilon)
    if s == -1:
        return minus_preserved(x, epsilon)
    return zero_preserved(x, epsilon)


def adversarial_flip_sign(x: float, epsilon: float) -> float | None:
    x = _require_finite("x", x)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    if sign_stable(x, epsilon):
        return None
    s = sign_select(x)
    if s == 1:
        return x - epsilon
    if s == -1:
        return x + epsilon
    # x == 0, ε > 0
    return epsilon
