"""Thresholding / AboveThreshold — scalar deterministic + noisy portfolio scaffold.

Equality convention (fixed): A_T(x) = 1  ⟺  x ≥ T.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Literal


class SequentialLevel(str, Enum):
    """Honest capability ladder — Sparse Vector is not claimed verified."""

    SCALAR_ROBUSTNESS = "1_scalar_threshold_robustness"
    NOISY_SCALAR = "2_noisy_scalar_threshold"
    FIRST_CROSSING_FIXED = "3_first_crossing_fixed_queries"
    FIRST_CROSSING_ADAPTIVE = "4_first_crossing_adaptive"  # candidate only
    LIMITED_POSITIVE_RELEASES = "5_limited_positive_releases"  # candidate only
    FULL_SPARSE_VECTOR = "6_full_sparse_vector"  # not verified


OPERATOR = "thresholding"
THEOREM_ID_DETERMINISTIC = "threshold-output-preservation"
THEOREM_ID_NOISY = "bounded-noise-threshold"
EVALUATION_METHOD_DET = "THRESHOLD_PRESERVATION_COMPUTATIONAL_V1"
EVALUATION_METHOD_NOISY = "THRESHOLD_BOUNDED_NOISE_COMPUTATIONAL_V1"

THEOREM_STATEMENT_DET = (
    "Let x,x'∈ℝ and ε≥0 with |x'-x|≤ε. For A_T(x)=1{x≥T} with fixed T∈ℝ: "
    "(1) if x≥T+ε then A_T(x')=1; "
    "(2) if x<T-ε then A_T(x')=0; "
    "(3) if x∈[T-ε,T+ε) the output need not be invariant."
)

SHARPNESS_STATEMENT_DET = (
    "Under the same convention A_T(x)=1{x≥T}: if x∈[T,T+ε) there exists admissible x' "
    "with A_T(x')=0; if x∈[T-ε,T) there exists admissible x' with A_T(x')=1. "
    "At x=T+ε every admissible x' satisfies A_T(x')=1 (pass-side non-strict)."
)

THEOREM_STATEMENT_NOISY = (
    "Let η≥0 and ξ satisfy |ξ|≤η almost surely. For Ã_T(x)=1{x+ξ≥T} with fixed T∈ℝ: "
    "(1) if x≥T+η then Ã_T(x)=1 a.s.; "
    "(2) if x<T-η then Ã_T(x)=0 a.s.; "
    "(3) if x∈[T-η,T+η) the random output need not be a.s. constant."
)

SHARPNESS_STATEMENT_NOISY = (
    "There exist admissible laws of ξ with |ξ|≤η a.s. such that: if x∈[T,T+η) then "
    "P(Ã_T=0)>0; if x∈[T-η,T) then P(Ã_T=1)>0. At x=T+η, Ã_T=1 a.s. for every such ξ."
)


def _require_finite(name: str, v: float) -> float:
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        raise ValueError(f"{name} must be a real number")
    fv = float(v)
    if not math.isfinite(fv):
        raise ValueError(f"{name} must be finite")
    return fv


@dataclass(frozen=True)
class ThresholdInstance:
    """Scalar score x with fixed threshold T. Equality passes: x ≥ T → 1."""

    x: float
    T: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", _require_finite("x", self.x))
        object.__setattr__(self, "T", _require_finite("T", self.T))

    def decide(self) -> Literal[0, 1]:
        return 1 if self.x >= self.T else 0

    def signed_margin(self) -> float:
        """m(D) = x − T (positive ⇒ pass)."""
        return self.x - self.T

    def distance(self) -> float:
        """d(D) = |x − T|."""
        return abs(self.x - self.T)


def above_threshold(x: float, T: float) -> Literal[0, 1]:
    return ThresholdInstance(x, T).decide()


def pass_preserved(x: float, T: float, epsilon: float) -> bool:
    """True iff every |x'-x|≤ε yields A_T(x')=1."""
    x = _require_finite("x", x)
    T = _require_finite("T", T)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    return x >= T + epsilon


def fail_preserved(x: float, T: float, epsilon: float) -> bool:
    """True iff every |x'-x|≤ε yields A_T(x')=0."""
    x = _require_finite("x", x)
    T = _require_finite("T", T)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    return x < T - epsilon


def unstable_region(x: float, T: float, epsilon: float) -> bool:
    """True iff output need not be invariant: x ∈ [T−ε, T+ε)."""
    x = _require_finite("x", x)
    T = _require_finite("T", T)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    return (T - epsilon) <= x < (T + epsilon)


def adversarial_break_pass(x: float, T: float, epsilon: float) -> float | None:
    """If a pass can be flipped, return x' = x−ε < T; else None."""
    x = _require_finite("x", x)
    T = _require_finite("T", T)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    if x < T or x >= T + epsilon:
        return None
    return x - epsilon


def adversarial_break_fail(x: float, T: float, epsilon: float) -> float | None:
    """If a fail can be flipped, return x' = x+ε ≥ T; else None."""
    x = _require_finite("x", x)
    T = _require_finite("T", T)
    epsilon = _require_finite("epsilon", epsilon)
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    if x >= T or x < T - epsilon:
        return None
    return x + epsilon


# --- Noisy / set-valued / abstaining portfolio (mechanism candidates) ---


def noisy_query_only(x: float, T: float, xi: float) -> Literal[0, 1]:
    return above_threshold(x + xi, T)


def noisy_threshold_only(x: float, T: float, zeta: float) -> Literal[0, 1]:
    return above_threshold(x, T + zeta)


def noisy_both(x: float, T: float, xi: float, zeta: float) -> Literal[0, 1]:
    """Effective noise W = ξ − ζ (no independence assumed)."""
    return above_threshold(x + xi - zeta, T)


def abstaining_threshold(
    x: float, T: float, tau: float
) -> Literal[0, 1] | None:
    """Certified abstention aligned with preservation asymmetry.

    Releases 1 iff pass-preserved under ε=τ (x≥T+τ); releases 0 iff fail-preserved
    (x<T−τ, strict). Returns ⊥ on [T−τ, T+τ).

    Note: the naive closed rule x≤T−τ is *not* robust at x=T−τ when ε=τ, because
    x'=T still passes. We deliberately use the strict fail side.
    """
    x = _require_finite("x", x)
    T = _require_finite("T", T)
    tau = _require_finite("tau", tau)
    if tau < 0:
        raise ValueError("tau must be ≥ 0")
    if x >= T + tau:
        return 1
    if x < T - tau:
        return 0
    return None


def certified_set(
    x: float, T: float, epsilon: float
) -> frozenset[Literal[0, 1]]:
    """Set-valued selector: singleton if invariant, {0,1} if interval crosses T."""
    if pass_preserved(x, T, epsilon):
        return frozenset({1})
    if fail_preserved(x, T, epsilon):
        return frozenset({0})
    return frozenset({0, 1})


def laplace_pass_probability(x: float, T: float, scale: float) -> float:
    """P(x+ξ≥T) for ξ~Laplace(0,b), b=scale>0. Exact CDF identity."""
    x = _require_finite("x", x)
    T = _require_finite("T", T)
    scale = _require_finite("scale", scale)
    if scale <= 0:
        raise ValueError("scale must be > 0")
    m = x - T
    if m >= 0:
        return 1.0 - 0.5 * math.exp(-m / scale)
    return 0.5 * math.exp(m / scale)


# --- Sequential first-crossing (levels 3+; Sparse Vector not claimed) ---


def first_crossing(queries: tuple[float, ...], T: float) -> int | None:
    """τ = min{t: q_t ≥ T}; None if no crossing. Indices 0..n-1."""
    T = _require_finite("T", T)
    for t, q in enumerate(queries):
        q = _require_finite(f"q[{t}]", q)
        if q >= T:
            return t
    return None


def noisy_first_crossing(
    queries: tuple[float, ...],
    T: float,
    xi: tuple[float, ...],
    zeta: float,
) -> int | None:
    """τ̃ = min{t: q_t+ξ_t ≥ T+ζ}. Does not claim Sparse Vector privacy."""
    T = _require_finite("T", T)
    zeta = _require_finite("zeta", zeta)
    if len(xi) != len(queries):
        raise ValueError("xi length must match queries")
    for t, (q, noise) in enumerate(zip(queries, xi)):
        q = _require_finite(f"q[{t}]", q)
        noise = _require_finite(f"xi[{t}]", noise)
        if q + noise >= T + zeta:
            return t
    return None


LEVEL_STATUS: dict[SequentialLevel, str] = {
    SequentialLevel.SCALAR_ROBUSTNESS: "VERIFIED_COMPUTATIONAL",
    SequentialLevel.NOISY_SCALAR: "VERIFIED_COMPUTATIONAL_BOUNDED_NOISE",
    SequentialLevel.FIRST_CROSSING_FIXED: "IMPLEMENTED_NOT_PRIVACY_THEOREM",
    SequentialLevel.FIRST_CROSSING_ADAPTIVE: "SPECIFIED_CANDIDATE",
    SequentialLevel.LIMITED_POSITIVE_RELEASES: "SPECIFIED_CANDIDATE",
    SequentialLevel.FULL_SPARSE_VECTOR: "NOT_VERIFIED",
}
