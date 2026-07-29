from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from operators.interval_membership.math import (
    EVALUATION_METHOD,
    OPERATOR,
    SHARPNESS_STATEMENT,
    THEOREM_ID,
    THEOREM_STATEMENT,
    adversarial_flip,
    fail_preserved,
    interval_membership,
    pass_preserved,
)


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    detail: str
    counterexamples: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN",)


def claim_is_interval_membership_preservation(claim: dict[str, Any]) -> bool:
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD
    )


def verify_interval_membership_preservation(claim: dict[str, Any]) -> VerifyResult:
    if not claim_is_interval_membership_preservation(claim):
        return VerifyResult(False, "claim_mismatch")
    if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
        return VerifyResult(False, "statement_mismatch")
    if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
        return VerifyResult(False, "sharpness_mismatch")
    rng = random.Random(11)
    failures: list[dict[str, Any]] = []
    for _ in range(400):
        a, b = rng.uniform(-4, 4), rng.uniform(-4, 4)
        L, U = (a, b) if a <= b else (b, a)
        x = rng.uniform(-5, 5)
        eps = rng.uniform(0, 2.5)
        i0 = interval_membership(x, L, U)
        samples = {x - eps, x, x + eps} if eps else {x}
        if pass_preserved(x, L, U, eps) and any(interval_membership(xp, L, U) != 1 for xp in samples):
            failures.append({"kind": "pass"})
        if fail_preserved(x, L, U, eps) and any(interval_membership(xp, L, U) != 0 for xp in samples):
            failures.append({"kind": "fail"})
        if pass_preserved(x, L, U, eps) or fail_preserved(x, L, U, eps):
            if adversarial_flip(x, L, U, eps) is not None:
                failures.append({"kind": "false_flip"})
        else:
            br = adversarial_flip(x, L, U, eps)
            if br is None or abs(br - x) > eps + 1e-9 or interval_membership(br, L, U) == i0:
                failures.append({"kind": "sharp", "x": x, "L": L, "U": U, "eps": eps, "br": br})
    if failures:
        return VerifyResult(False, f"failures:{len(failures)}", tuple(failures[:8]))
    return VerifyResult(True, "ok")
