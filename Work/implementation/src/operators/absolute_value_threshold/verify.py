"""Verify abs-threshold computationally."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from operators.absolute_value_threshold.math import (
    EVALUATION_METHOD,
    OPERATOR,
    SHARPNESS_STATEMENT,
    THEOREM_ID,
    THEOREM_STATEMENT,
    abs_stable,
    abs_threshold,
    adversarial_flip,
    fail_preserved,
    pass_preserved,
)


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    detail: str
    counterexamples: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN", "T_NONNEGATIVE")


def claim_is_abs_threshold_preservation(claim: dict[str, Any]) -> bool:
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD
    )


def verify_abs_threshold_preservation(claim: dict[str, Any]) -> VerifyResult:
    if not claim_is_abs_threshold_preservation(claim):
        return VerifyResult(False, "claim_mismatch")
    if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
        return VerifyResult(False, "statement_mismatch")
    if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
        return VerifyResult(False, "sharpness_mismatch")
    rng = random.Random(7)
    failures: list[dict[str, Any]] = []
    for _ in range(400):
        x = rng.uniform(-5, 5)
        T = rng.uniform(0, 4)
        eps = rng.uniform(0, 3)
        a0 = abs_threshold(x, T)
        samples = {x - eps, x, x + eps} if eps else {x}
        _ = a0
        if pass_preserved(x, T, eps) and any(abs_threshold(xp, T) != 1 for xp in samples):
            failures.append({"kind": "pass", "x": x, "T": T, "eps": eps})
        if fail_preserved(x, T, eps) and any(abs_threshold(xp, T) != 0 for xp in samples):
            failures.append({"kind": "fail", "x": x, "T": T, "eps": eps})
        # Sharpness witness when geometry matches Lean hypothesis
        if eps <= x and T <= x < T + eps:
            br = adversarial_flip(x, T, eps)
            if br is None or abs_threshold(br, T) != 0:
                failures.append({"kind": "sharp", "x": x, "T": T, "eps": eps, "br": br})
        elif abs_stable(x, T, eps) and adversarial_flip(x, T, eps) is not None:
            failures.append({"kind": "false_flip"})
    if failures:
        return VerifyResult(False, f"failures:{len(failures)}", tuple(failures[:8]))
    return VerifyResult(True, "ok")
