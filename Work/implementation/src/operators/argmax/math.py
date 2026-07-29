"""Argmax operator — finite deterministic scores, ∞-norm perturbations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArgmaxInstance:
    """Scores s ∈ ℝ^m; indices are 0..m-1 (maps to [m] in papers)."""

    scores: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.scores) < 2:
            raise ValueError("scores must have m≥2")

    @property
    def m(self) -> int:
        return len(self.scores)

    def maximizers(self) -> tuple[int, ...]:
        top = max(self.scores)
        return tuple(i for i, v in enumerate(self.scores) if v == top)

    def unique_maximizer(self) -> int | None:
        mx = self.maximizers()
        return mx[0] if len(mx) == 1 else None

    def margin(self) -> float | None:
        """γ(s) = s_{i*} − max_{j≠i*} s_j when i* unique; else None."""
        i_star = self.unique_maximizer()
        if i_star is None:
            return None
        others = [self.scores[j] for j in range(self.m) if j != i_star]
        return self.scores[i_star] - max(others)


def apply_perturbation(scores: tuple[float, ...], delta: tuple[float, ...]) -> tuple[float, ...]:
    if len(scores) != len(delta):
        raise ValueError("delta length mismatch")
    return tuple(s + d for s, d in zip(scores, delta))


def linf_norm(delta: tuple[float, ...]) -> float:
    return max(abs(d) for d in delta) if delta else 0.0


def invariance_holds(scores: tuple[float, ...], epsilon: float) -> bool:
    """True iff unique argmax is preserved under every ||δ||_∞ ≤ ε (exact check via worst case)."""
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    inst = ArgmaxInstance(scores)
    i_star = inst.unique_maximizer()
    if i_star is None:
        return False
    gamma = inst.margin()
    assert gamma is not None
    # Necessary and sufficient: γ > 2ε (strict; at equality adversarial δ ties or flips)
    return gamma > 2 * epsilon


def adversarial_break(scores: tuple[float, ...], epsilon: float) -> tuple[float, ...] | None:
    """If γ ≤ 2ε and unique winner exists, return δ with ||δ||_∞ ≤ ε that destroys uniqueness of i*."""
    if epsilon < 0:
        raise ValueError("epsilon must be ≥ 0")
    inst = ArgmaxInstance(scores)
    i_star = inst.unique_maximizer()
    if i_star is None:
        return None
    gamma = inst.margin()
    assert gamma is not None
    if gamma > 2 * epsilon:
        return None
    # second-place index
    j_star = max((j for j in range(inst.m) if j != i_star), key=lambda j: scores[j])
    delta = [0.0] * inst.m
    delta[i_star] = -epsilon
    delta[j_star] = epsilon
    return tuple(delta)


# Canonical theorem identifiers (must match sealed claims)
THEOREM_ID = "bounded-perturbation-margin"
OPERATOR = "argmax"
EVALUATION_METHOD = "ARGMAX_MARGIN_COMPUTATIONAL_V1"

THEOREM_STATEMENT = (
    "Let m≥2, s∈ℝ^m with unique maximizer i*=argmax_i s_i and margin "
    "γ(s)=s_{i*}−max_{j≠i*}s_j>0. Let ε≥0 and δ∈ℝ^m with ||δ||_∞≤ε. "
    "If γ(s)>2ε, then i* is the unique maximizer of s+δ."
)

SHARPNESS_STATEMENT = (
    "Under the same setup, if γ(s)≤2ε then there exists δ with ||δ||_∞≤ε "
    "such that i* is not the unique maximizer of s+δ."
)
