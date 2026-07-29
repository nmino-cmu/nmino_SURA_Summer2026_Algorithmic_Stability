"""Computational discharge for sign preservation."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from operators.sign.math import (
    EVALUATION_METHOD,
    OPERATOR,
    SHARPNESS_STATEMENT,
    THEOREM_ID,
    THEOREM_STATEMENT,
    adversarial_flip_sign,
    minus_preserved,
    plus_preserved,
    sign_select,
    sign_stable,
    zero_preserved,
)


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    detail: str
    counterexamples: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = (
        "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
        "SCALAR_FINITE_SCORES_ONLY",
    )


def claim_is_sign_preservation(claim: dict[str, Any]) -> bool:
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD
    )


def verify_sign_preservation(claim: dict[str, Any]) -> VerifyResult:
    if not claim_is_sign_preservation(claim):
        return VerifyResult(False, "claim_mismatch")
    if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
        return VerifyResult(False, "statement_mismatch")
    if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
        return VerifyResult(False, "sharpness_statement_mismatch")

    rng = random.Random(20260725)
    failures: list[dict[str, Any]] = []
    for _ in range(400):
        x = rng.uniform(-5, 5)
        eps = rng.uniform(0, 3)
        s0 = sign_select(x)
        samples = {x - eps, x, x + eps} if eps else {x}
        if plus_preserved(x, eps):
            if any(sign_select(xp) != 1 for xp in samples):
                failures.append({"kind": "plus", "x": x, "eps": eps})
        if minus_preserved(x, eps):
            if any(sign_select(xp) != -1 for xp in samples):
                failures.append({"kind": "minus", "x": x, "eps": eps})
        if zero_preserved(x, eps):
            if any(sign_select(xp) != 0 for xp in samples):
                failures.append({"kind": "zero", "x": x, "eps": eps})
        if sign_stable(x, eps):
            if adversarial_flip_sign(x, eps) is not None:
                failures.append({"kind": "stable_false_flip", "x": x, "eps": eps})
        else:
            br = adversarial_flip_sign(x, eps)
            if br is None or abs(br - x) > eps + 1e-9:
                failures.append({"kind": "bad_flip", "x": x, "eps": eps, "br": br})
            elif sign_select(br) == s0:
                failures.append({"kind": "sharp_fail", "x": x, "eps": eps, "br": br})

    # boundaries
    assert sign_select(0.0) == 0
    assert plus_preserved(1.0, 1.0) is False
    assert plus_preserved(1.0 + 1e-9, 1.0) is True or plus_preserved(2.0, 1.0)

    try:
        sign_select(float("nan"))
        failures.append({"kind": "nan"})
    except ValueError:
        pass

    if failures:
        return VerifyResult(False, f"failures:{len(failures)}", tuple(failures[:8]))
    return VerifyResult(True, "sign_preservation_ok")
